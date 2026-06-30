# Design

## Contexto

Se requiere definir una feature que tome una URL fija (https://elpais.com/), obtenga titulares y entregue un PDF con el listado. Adicionalmente, la feature debe informar de forma explicita todas las librerias Python requeridas para ejecutar el flujo de extremo a extremo.

## Archivos afectados

- feature_list.json
- progress/current.md
- specs/titulares-elpais-a-pdf/requirements.md
- specs/titulares-elpais-a-pdf/design.md
- specs/titulares-elpais-a-pdf/tasks.md

## Decisiones

- Se documenta primero por SDD y se deja en estado spec_ready para respetar la puerta humana antes de implementar.
- La implementacion se define bajo patron POM, con clases de pagina para encapsular selectores, fetch y metodos de extraccion.
- La extraccion de titulares se plantea con cliente HTTP y parser HTML para desacoplar descarga y parseo.
- La salida PDF se modela como una lista numerada para legibilidad y validacion simple.
- El listado de librerias se trata como salida funcional explicita para cumplir el objetivo del usuario.

Propuesta POM minima:

- ElPaisHomePage: encapsula URL, carga de contenido y metodos para localizar bloques de titulares.
- HeadlinesExtractorService: consume ElPaisHomePage y devuelve lista normalizada de titulares.
- PdfReportBuilder: recibe titulares y crea PDF final.
- DependenciesReporter: devuelve librerias requeridas y su rol en el flujo.

## Alternativas descartadas

- Automatizacion con navegador completo (Selenium/Playwright) porque agrega complejidad y no es necesaria para una lectura de HTML estatico inicial.
- Exportar a TXT/MD en lugar de PDF porque no cumple el entregable solicitado.

## Riesgos

- Cambios en selectores o estructura de portada de El Pais pueden romper la extraccion.
- Bloqueos anti-bot o respuestas parciales del sitio pueden afectar completitud.
- Problemas de codificacion de caracteres pueden degradar el PDF.
- Uso superficial de POM (solo por nombre) sin encapsulacion real.

Mitigaciones:

- Definir selectores de respaldo y validaciones de cantidad minima de titulares.
- Gestionar timeouts, user-agent y errores de red con mensajes claros.
- Forzar escritura UTF-8 en la normalizacion previa a PDF.
- Revisar que la orquestacion no acceda a selectores directamente y pase siempre por Page Objects.

## Documentacion aplicable

Debe leer:
- docs/sdd/specs.md
- docs/sdd/conventions.md
- specs/README.md

No es necesario leer:
- docs/sdd/verification.md porque esta fase no ejecuta implementacion ni evidencia tecnica aun.
