# Spec Driven Development

Flujo:

requirements -> design -> tasks -> implementacion

No se implementa antes de aprobacion humana del spec.

## Estructura por feature

specs/<feature>/requirements.md
specs/<feature>/design.md
specs/<feature>/tasks.md

## Estados

- pending
- spec_ready
- in_progress
- done
- blocked

## Reglas de transicion

- pending -> spec_ready
- spec_ready -> in_progress (solo con aprobacion humana)
- in_progress -> done (tras review APPROVED)
- cualquier estado -> blocked (si hay bloqueo documentado)

## Requirements (EARS estricto)

Patrones:

- El sistema DEBE <accion>.
- CUANDO <evento>, el sistema DEBE <accion>.
- MIENTRAS <estado>, el sistema DEBE <accion>.
- DONDE <condicion opcional>, el sistema DEBE <accion>.
- SI <evento no deseado> ENTONCES el sistema DEBE <accion>.

Reglas:

- Un solo DEBE por requirement.
- IDs estables: R1, R2, R3.
- Cada requirement debe ser verificable con evidencia.

## design.md

Debe contener:

- Archivos afectados
- Decisiones tecnicas
- Alternativas descartadas
- Riesgos
- Documentacion aplicable

## tasks.md

- Checklist ordenado T1..Tn
- Cada task indica requirements cubiertos
- Marcar [x] al completar
