from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

from app.errors import PdfGenerationError


class PdfReportBuilder:
    """Builds a PDF report from extracted headlines."""

    @staticmethod
    def _safe_text(text: str) -> str:
        return text.encode("latin-1", errors="replace").decode("latin-1")

    @staticmethod
    def _break_long_tokens(text: str, token_size: int = 32) -> str:
        parts: list[str] = []
        for token in text.split(" "):
            if len(token) <= token_size:
                parts.append(token)
                continue
            chunks = [token[i : i + token_size] for i in range(0, len(token), token_size)]
            parts.append(" ".join(chunks))
        return " ".join(parts)

    def build(self, output_path: Path, source_url: str, headlines: list[str]) -> None:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Helvetica", "B", 14)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 10, self._safe_text("Titulares extraidos"))

            pdf.set_font("Helvetica", "", 10)
            source_line = self._break_long_tokens(f"Fuente: {source_url}")
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 8, self._safe_text(source_line))
            pdf.ln(2)

            pdf.set_font("Helvetica", "", 11)
            for index, headline in enumerate(headlines, start=1):
                line = self._break_long_tokens(f"{index}. {headline}")
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(0, 8, self._safe_text(line))

            pdf.output(str(output_path))
        except OSError as exc:
            raise PdfGenerationError(
                f"No se pudo escribir el PDF en {output_path}: {exc}"
            ) from exc
        except Exception as exc:  # pragma: no cover
            raise PdfGenerationError(f"Fallo inesperado al generar PDF: {exc}") from exc
