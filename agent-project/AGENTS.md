# AGENTS

Mapa de operacion del arnes SDD.

## Modo libre

Solo analisis/consulta, sin mover estados SDD.

## Modo SDD Harness

1. Ejecutar python scripts/harness_init.py.
2. Leer feature_list.json y progress/current.md.
3. Si feature esta pending: crear specs y mover a spec_ready.
4. Esperar aprobacion humana.
5. Mover a in_progress y ejecutar implementacion.
6. Revisar y cerrar en done.

## Reglas duras

- No saltar puerta humana spec_ready -> in_progress.
- Maximo una feature en in_progress.
- Una feature por sesion.
- Si hay bloqueo real, usar blocked y documentar motivo.
