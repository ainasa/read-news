from __future__ import annotations


class DependenciesReporter:
    """Provides the Python libraries required by this feature."""

    def get_dependencies(self) -> list[dict[str, str]]:
        return [
            {
                "name": "requests",
                "purpose": "Realizar solicitudes HTTP a la URL objetivo.",
            },
            {
                "name": "beautifulsoup4",
                "purpose": "Parsear HTML y localizar nodos de titulares.",
            },
            {
                "name": "fpdf2",
                "purpose": "Generar el archivo PDF con el listado de titulares.",
            },
            {
                "name": "deep-translator",
                "purpose": "Traducir titulares al castellano cuando se usa --ES.",
            },
        ]
