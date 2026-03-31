# Proyecto: Framework Multi-Agente para Claude Code

<!--
  PLANTILLA GENÉRICA — Adapta las secciones a tu proyecto.
  Las secciones marcadas con [EJEMPLO] contienen valores de referencia
  que debes reemplazar con los de tu proyecto real.
-->

## Idioma

Claude Code debe responder y documentar siempre en español.
Esto incluye: respuestas, comentarios en código, mensajes de commit
(conventional commits), logs de hooks y contenido de specs.

## Descripción del proyecto

<!-- [EJEMPLO] Reemplaza con la descripción de tu proyecto -->
Framework exportable que implementa Desarrollo Dirigido por Especificaciones
(SDD) con arquitectura de orquestador-subagentes para Claude Code. Proporciona
agentes, skills y hooks reutilizables como base profesional para cualquier
proyecto.

## Arquitectura general

```
┌─────────────────────────────────────────────┐
│              Orquestador                     │
│  (recibe tarea → crea spec → delega)         │
├──────┬──────────┬──────────────┬─────────────┤
│ UI   │ Backend  │  Revisión    │   Tests     │
│      │          │ (obligatoria)│             │
└──────┴──────────┴──────────────┴─────────────┘
```

- **Flujo SDD:** spec → implementación → revisión → tests
- **Agentes:** orquestador + 4 subagentes especializados
- **Skills:** procedimientos reutilizables (commits, validación, seguridad)
- **Hooks:** automatización del ciclo de vida (seguridad, lint, verificación)

## Stack y convenciones

<!-- [EJEMPLO] Adapta al stack de tu proyecto -->
- **Lenguaje principal:** Python 3.11+
- **Hooks:** Python (scripts en `.claude/hooks/`)
- **Documentación:** Markdown
- **Commits:** Conventional Commits en español (`feat`, `fix`, `docs`, etc.)
- **Linting:** py_compile (Python), eslint (JS/TS), json.tool (JSON)

## Agentes activos en este proyecto

| Agente          | Archivo                              | Rol                           |
|-----------------|--------------------------------------|-------------------------------|
| Orquestador     | `.claude/agents/orquestador.md`      | Descompone y delega tareas    |
| Diseñador UI    | `.claude/agents/disenador-ui.md`     | Diseño de interfaces          |
| Implementador   | `.claude/agents/implementador.md`    | Implementación de código      |
| Revisor código  | `.claude/agents/revisor-codigo.md`   | Revisión obligatoria          |
| Tester          | `.claude/agents/tester.md`           | Generación de tests           |

## Skills habilitadas

| Skill               | Archivo                                         | Propósito                        |
|---------------------|-------------------------------------------------|----------------------------------|
| Formato de commits  | `.claude/skills/formato-commits/SKILL.md`       | Conventional commits en español  |
| Validador de specs  | `.claude/skills/validador-specs/SKILL.md`       | Valida secciones de specs        |
| Revisión seguridad  | `.claude/skills/revision-seguridad/SKILL.md`    | Checklist OWASP Top 10           |

## Hooks habilitados

| Hook               | Archivo                                  | Evento         | Comportamiento     |
|--------------------|------------------------------------------|----------------|--------------------|
| Security Gate      | `.claude/hooks/security-gate.py`         | PreToolUse     | Bloquea si no pasa |
| Lint al escribir   | `.claude/hooks/lint-al-escribir.py`      | PostToolUse    | Solo advierte      |
| Verificación specs | `.claude/hooks/verificacion-specs.py`    | Stop           | Solo advierte      |

Los hooks se configuran en `.claude/settings.json`.

## Directorio de specs

Todas las especificaciones viven en `specs/`. **Sin spec, no hay implementación.**

```
specs/
├── framework.md              # Spec maestro del framework
├── orquestador.md            # Spec del agente orquestador
└── agentes/
    ├── disenador-ui.md       # Spec del diseñador UI
    ├── implementador.md      # Spec del implementador
    ├── revisor-codigo.md     # Spec del revisor de código
    └── tester.md             # Spec del tester
```

## Política de seguridad (resumen)

- Los hooks nunca ejecutan input no confiable
- `security-gate.py` usa enfoque **allowlist** (no denylist)
- Sin secretos ni credenciales en ningún archivo del repositorio
- Los scripts Python deben pasar `bandit` sin hallazgos de severidad HIGH
- Todo código producido pasa por el revisor de código (obligatorio)
- Revisión de seguridad basada en OWASP Top 10

## Fuera de alcance / restricciones

<!-- [EJEMPLO] Adapta las restricciones a tu proyecto -->
- Este framework no incluye implementación de lógica de negocio específica
- No se despliega código a producción desde el framework
- Los agentes no ejecutan acciones destructivas sin confirmación del usuario
- No se almacenan secretos, tokens ni credenciales en el repositorio
