# Verificacion del arnes

## Comando base

python scripts/harness_init.py

## Que valida

- Archivos minimos del arnes
- Coherencia de feature_list.json
- Unicidad de features por name
- Maximo una feature en in_progress
- Presencia de specs para estados que lo requieren

## Evidencia de cierre

progress/impl_<feature>.md debe incluir:

- requirements cubiertos
- evidencias por requirement
- riesgos residuales

progress/review_<feature>.md debe incluir veredicto:

- APPROVED
- CHANGES_REQUESTED
