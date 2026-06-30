import argparse
import ast
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from app.errors import FeatureError
from app.page_objects.el_pais_home_page import ElPaisHomePage
from app.services.dependencies_reporter import DependenciesReporter
from app.services.headlines_extractor_service import HeadlinesExtractorService
from app.services.headline_translator_service import HeadlineTranslatorService
from app.services.pdf_report_builder import PdfReportBuilder


MONTH_NAMES_ES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def _extract_url_core(url: str) -> str:
    parsed = urlparse(url)
    hostname = (parsed.netloc or "").strip().lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]

    if not hostname:
        return "sitio"

    labels = [label for label in hostname.split(".") if label]
    if len(labels) <= 1:
        return labels[0] if labels else "sitio"

    return labels[0]


def _sanitize_folder_name(value: str) -> str:
    cleaned = "".join(ch for ch in value.lower() if ch.isalnum() or ch in ("-", "_"))
    return cleaned or "sitio"


def _today_spanish_suffix() -> str:
    today = datetime.now()
    month_name = MONTH_NAMES_ES[today.month]
    return f"{today.day}{month_name}"


def _resolve_output_path(output_arg: str, url: str) -> Path:
    url_core = _extract_url_core(url)
    safe_core = _sanitize_folder_name(url_core)
    date_suffix = _today_spanish_suffix()
    filename = f"titulares_{safe_core}_{date_suffix}.pdf"

    provided_path = Path(output_arg)
    output_dir = provided_path.parent if provided_path.suffix.lower() == ".pdf" else provided_path
    return output_dir / safe_core / filename


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrae titulares de una URL y genera un PDF en formato listado."
    )
    parser.add_argument(
        "--url",
        default="https://elpais.com/",
        help="URL objetivo o array JSON de URLs.",
    )
    parser.add_argument(
        "--output",
        default="output/titulares_elpais.pdf",
        help="Ruta base de salida del PDF (se usara su carpeta para el nombre dinamico).",
    )
    parser.add_argument(
        "--max-headlines",
        type=int,
        default=25,
        help="Numero maximo de titulares a incluir en el PDF.",
    )
    parser.add_argument(
        "--list-libraries-only",
        action="store_true",
        help="Muestra las librerias requeridas y termina sin scrapear.",
    )
    parser.add_argument(
        "--ES",
        "--es",
        dest="translate_to_es",
        action="store_true",
        help="Traduce al castellano los titulares extraidos antes de generar el PDF.",
    )
    return parser.parse_args()


def print_dependencies() -> None:
    reporter = DependenciesReporter()
    print("Librerias Python necesarias:")
    for item in reporter.get_dependencies():
        print(f"- {item['name']}: {item['purpose']}")


def _parse_urls(url_input: str) -> list[str]:
    normalized = (url_input or "").strip()
    if not normalized:
        return ["https://elpais.com/"]

    # Tolerates wrapped quoting from some shell invocations.
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in ("'", '"'):
        normalized = normalized[1:-1].strip()

    if not normalized.startswith("["):
        return [normalized]

    try:
        parsed = json.loads(normalized)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(normalized)
        except (SyntaxError, ValueError):
            if normalized.startswith("[") and normalized.endswith("]"):
                raw_items = normalized[1:-1].split(",")
                parsed = [item.strip().strip("\"'") for item in raw_items if item.strip()]
            else:
                raise FeatureError(
                    "El parametro --url parece un array, pero no es JSON valido."
                )

    if not isinstance(parsed, list) or not parsed:
        raise FeatureError("El array de --url debe contener al menos una URL.")

    invalid = [item for item in parsed if not isinstance(item, str) or not item.strip()]
    if invalid:
        raise FeatureError("Todas las entradas del array --url deben ser strings no vacios.")

    return [item.strip() for item in parsed]


def _process_single_url(
    url: str,
    output_arg: str,
    max_headlines: int,
    translate_to_es: bool,
) -> None:
    page = ElPaisHomePage(url)
    extractor = HeadlinesExtractorService(page)
    headlines = extractor.get_headlines(max_headlines=max_headlines)

    if translate_to_es:
        translator = HeadlineTranslatorService(target_language="es")
        headlines = translator.translate_many(headlines)

    output_path = _resolve_output_path(output_arg, url)
    PdfReportBuilder().build(
        output_path=output_path,
        source_url=url,
        headlines=headlines,
    )

    print(f"URL procesada: {url}")
    print(f"Titulares extraidos: {len(headlines)}")
    print(f"PDF generado en: {output_path}")
    print("")


def main() -> int:
    args = parse_args()
    print_dependencies()

    if args.list_libraries_only:
        return 0

    try:
        urls = _parse_urls(args.url)
    except FeatureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    for url in urls:
        try:
            _process_single_url(
                url=url,
                output_arg=args.output,
                max_headlines=args.max_headlines,
                translate_to_es=args.translate_to_es,
            )
        except FeatureError as exc:
            errors.append(f"{url}: {exc}")

    if errors:
        print("Errores detectados:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
