# tasty-claude — Framework Multi-Agente para Claude Code

Framework exportable que implementa **Desarrollo Dirigido por Especificaciones (SDD)** con una arquitectura de orquestador-subagentes, skills reutilizables y hooks de ciclo de vida para Claude Code.

## Inicio rápido

### Opción 1: Usar como base directa

```bash
git clone https://github.com/0xT4sty/tasty-claude.git mi-proyecto
cd mi-proyecto
# Edita CLAUDE.md con los datos de tu proyecto
```

### Opción 2: Bootstrap con script

```bash
git clone https://github.com/0xT4sty/tasty-claude.git
./tasty-claude/scripts/init-proyecto.sh ~/mi-nuevo-proyecto
cd ~/mi-nuevo-proyecto
```

El script copia toda la estructura, configura permisos e inicializa git.

## Estructura del repositorio

```
├── CLAUDE.md                          # Plantilla de proyecto para Claude Code
├── .claude/settings.json              # Configuración de hooks
├── specs/                             # Especificaciones SDD (fuente de verdad)
│   ├── framework.md                   # Spec maestro
│   ├── orquestador.md                 # Spec del orquestador
│   └── agentes/                       # Specs de subagentes
│       ├── disenador-ui.md
│       ├── implementador.md
│       ├── revisor-codigo.md
│       └── tester.md
├── agentes/                           # Prompts de agentes
│   ├── orquestador.md                 # Agente principal
│   └── subagentes/
│       ├── disenador-ui.md
│       ├── implementador.md
│       ├── revisor-codigo.md
│       └── tester.md
├── skills/                            # Skills reutilizables
│   ├── formato-commits.md             # Conventional commits en español
│   ├── validador-specs.md             # Validación de specs
│   └── revision-seguridad.md          # Checklist OWASP Top 10
├── hooks/                             # Hooks del ciclo de vida
│   ├── pre-tool-use/
│   │   └── security-gate.py           # Allowlist de comandos shell
│   ├── post-tool-use/
│   │   └── lint-al-escribir.py        # Linting automático al escribir
│   └── stop/
│       └── verificacion-specs.py      # Verifica cobertura de specs
└── scripts/
    └── init-proyecto.sh               # Bootstrap de nuevo proyecto
```

## Cómo funciona

### Flujo SDD

El principio central es: **sin spec, no hay implementación**.

```
Tarea → Crear spec → Delegar a subagente → Revisión obligatoria → Completado
```

1. El **orquestador** recibe una tarea y la descompone
2. Crea un spec en `specs/` para cada subtarea
3. Delega al subagente correspondiente
4. El **revisor de código** aprueba o rechaza (obligatorio)
5. El **tester** genera tests si aplica

### Agentes

| Agente | Responsabilidad |
|--------|----------------|
| **Orquestador** | Descompone tareas, crea specs, coordina subagentes |
| **Diseñador UI** | Estructura de componentes, layout, UX, accesibilidad |
| **Implementador** | Escribe código de producción a partir del spec |
| **Revisor de código** | Revisión obligatoria: cumplimiento de spec, calidad, seguridad |
| **Tester** | Genera tests unitarios e integración |

### Skills

Las skills son procedimientos documentados que los agentes siguen:

- **formato-commits.md** — Conventional commits en español (`feat`, `fix`, `docs`...)
- **validador-specs.md** — Verifica que un spec tenga todas las secciones requeridas
- **revision-seguridad.md** — Checklist OWASP Top 10 para revisión de código

### Hooks

Los hooks automatizan verificaciones en el ciclo de vida de Claude Code:

| Hook | Evento | Comportamiento |
|------|--------|---------------|
| `security-gate.py` | Pre-tool-use | **Bloquea** comandos shell no permitidos (enfoque allowlist) |
| `lint-al-escribir.py` | Post-tool-use | **Advierte** si el linter detecta errores al escribir archivos |
| `verificacion-specs.py` | Stop | **Advierte** si hay archivos modificados sin spec asociado |

Los hooks se configuran en `.claude/settings.json` y se ejecutan automáticamente.

## Personalización

### Adaptar CLAUDE.md

Edita las secciones marcadas con `<!-- [EJEMPLO] -->` para reflejar tu proyecto:

- Descripción del proyecto
- Stack y convenciones
- Restricciones específicas

### Agregar un nuevo agente

1. Crea su spec en `specs/agentes/mi-agente.md` (secciones: Rol, Entrada, Salida, Restricciones, Seguridad)
2. Crea su prompt en `agentes/subagentes/mi-agente.md`
3. Actualiza las reglas de delegación en `agentes/orquestador.md`

### Agregar una nueva skill

Crea un archivo `.md` en `skills/` con: Descripción, Condición de activación, Procedimiento y Salida esperada.

### Modificar el allowlist de security-gate

Edita la lista `ALLOWLIST` en `hooks/pre-tool-use/security-gate.py` para agregar o quitar patrones de comandos permitidos.

## Requisitos

- **Claude Code** 2.x+
- **Python** 3.10+
- **Git**

## Seguridad

- `security-gate.py` usa enfoque **allowlist** (no denylist)
- Los hooks nunca ejecutan input no confiable
- Sin secretos ni credenciales en el repositorio
- Hooks verificados con `bandit` (0 hallazgos HIGH)
- Toda revisión de código incluye checklist OWASP Top 10

## Idioma

Este framework está configurado para trabajar en **español**: respuestas, comentarios en código, commits, logs y documentación.
