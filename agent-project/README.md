# Plantilla SDD Harness Basica (Python)

Esta plantilla crea solo el sistema SDD y el arnes de agentes.
No incluye tests ni configuracion de testing.

## Flujo

pending -> spec_ready -> in_progress -> done

Existe puerta humana obligatoria entre spec_ready e in_progress.

## Contenido

- AGENTS.md
- feature_list.json
- CHECKPOINTS.md
- scripts/harness_init.py
- docs/sdd/
- .github/agents/
- progress/
- specs/_templates/

## Arranque

1. Editar feature_list.json y crear una feature pending con sdd=true.
2. Ejecutar: python scripts/harness_init.py
3. Redactar specs en specs/<feature>/
