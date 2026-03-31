# Spec: Framework Multi-Agente para Claude Code

## Descripción general

Framework/repositorio exportable para Claude Code que implementa Desarrollo
Dirigido por Especificaciones (SDD) con una arquitectura de
orquestador-subagentes, skills reutilizables, hooks y una plantilla CLAUDE.md
genérica.

El usuario objetivo es un desarrollador senior que parte de una instalación
por defecto de Claude Code (sin skills, sin agentes, sin hooks configurados)
y quiere una estructura portable y profesional.

## Idioma de trabajo

Claude Code debe comunicarse siempre en español en este proyecto:

- Respuestas, razonamientos y explicaciones: español
- Comentarios en código: español
- Mensajes de commit: español (siguiendo conventional commits)
- Logs de hooks: español
- Contenido de specs y documentación: español

## Objetivos

- Implementar SDD: las specs son la fuente de verdad, no se escribe código sin spec previa
- Agente orquestador que descompone tareas y delega en subagentes especializados
- Skills y hooks reutilizables e independientes del dominio
- Plantilla CLAUDE.md genérica exportable a cualquier proyecto

## Estructura del repositorio

```
claude-code-framework/
├── CLAUDE.md
├── specs/
│   ├── framework.md
│   ├── orquestador.md
│   └── agentes/
│       ├── disenador-ui.md
│       ├── implementador.md
│       ├── revisor-codigo.md
│       └── tester.md
├── agentes/
│   ├── orquestador.md
│   └── subagentes/
│       ├── disenador-ui.md
│       ├── implementador.md
│       ├── revisor-codigo.md
│       └── tester.md
├── skills/
│   ├── README.md
│   ├── formato-commits.md
│   ├── validador-specs.md
│   └── revision-seguridad.md
├── hooks/
│   ├── pre-tool-use/
│   │   └── security-gate.py
│   ├── post-tool-use/
│   │   └── lint-al-escribir.py
│   └── stop/
│       └── verificacion-specs.py
└── scripts/
    └── init-proyecto.sh
```

## Specs requeridas

### 1. Agente Orquestador (`specs/orquestador.md`)

**Comportamiento:**
- Recibe una tarea de alto nivel o historia de usuario
- La descompone en subtareas asignadas a subagentes especializados
- Genera un spec en `specs/` antes de invocar cualquier subagente
- Recoge los outputs y ejecuta el revisor de código antes de marcar como completado

**Reglas de delegación:**
- Diseño UI/UX → disenador-ui
- Lógica de negocio / backend → implementador
- Todo código producido → revisor-codigo (obligatorio, no omitible)
- Generación de tests → tester

**Restricción SDD:** el orquestador debe crear el archivo spec antes de
invocar cualquier subagente. Sin spec, no hay ejecución.

### 2. Subagentes (`specs/agentes/*.md`)

Cada spec de subagente debe definir:
- **Rol:** descripción de responsabilidad única
- **Entrada:** formato de spec o interfaz esperada
- **Salida:** entregable (código, doc de diseño, tests, informe de revisión)
- **Restricciones:** qué NO debe hacer
- **Reglas de seguridad:** guías de desarrollo seguro aplicables a su dominio

| Subagente       | Responsabilidad                                          |
|-----------------|----------------------------------------------------------|
| disenador-ui    | Estructura de componentes, layout, decisiones UX         |
| implementador   | Implementación de código a partir de spec                |
| revisor-codigo  | Análisis estático, revisión de seguridad, cumplimiento   |
| tester          | Generación de tests unitarios e integración              |

### 3. Skills (`skills/`)

Skills genéricas reutilizables en cualquier proyecto:

- **formato-commits.md:** Enforce de conventional commits en español
- **validador-specs.md:** Verifica que una spec tiene las secciones requeridas
  antes de que el subagente arranque
- **revision-seguridad.md:** Checklist alineado con OWASP para revisión de código

Cada skill es un archivo markdown con: descripción, condición de activación,
procedimiento paso a paso y salida esperada.

### 4. Hooks (`hooks/`)

- **pre-tool-use/security-gate.py:** Bloquea comandos shell peligrosos usando
  enfoque allowlist — sale con código no-cero para abortar
- **post-tool-use/lint-al-escribir.py:** Al escribir un archivo, ejecuta el
  linter correspondiente según la extensión
- **stop/verificacion-specs.py:** Al finalizar la sesión, advierte si algún
  archivo modificado no tiene spec asociada

Los hooks deben estar escritos en Python, manejar errores de forma controlada
y loguear en stderr (nunca en stdout). Los mensajes de log deben estar en español.

### 5. Plantilla CLAUDE.md

Secciones requeridas:
- Idioma
- Descripción del proyecto
- Arquitectura general
- Stack y convenciones
- Agentes activos en este proyecto
- Skills habilitadas
- Hooks habilitados
- Directorio de specs
- Política de seguridad (resumen)
- Fuera de alcance / restricciones

Debe ser concisa y legible por el agente orquestador.

## Criterios de aceptación

- [ ] Todos los specs existen antes de que se cree cualquier archivo de implementación
- [ ] Cada agente tiene su spec y su archivo de implementación
- [ ] Todos los hooks son ejecutables y tienen un dry-run de prueba
- [ ] `init-proyecto.sh` copia la estructura del framework a un directorio destino
- [ ] La plantilla CLAUDE.md incluye valores de ejemplo y comentarios explicativos
- [ ] Ninguna implementación se desvía de su spec sin una actualización explícita

## Restricciones y seguridad

- Los hooks nunca deben ejecutar input no confiable
- `security-gate.py` debe usar enfoque allowlist, no denylist
- Sin secretos ni credenciales en ningún archivo
- Todos los scripts Python deben pasar bandit sin hallazgos de severidad HIGH

## Orden de ejecución para Claude Code

1. Leer y validar este spec (`specs/framework.md`)
2. Crear la estructura de directorios
3. Escribir todos los specs primero (directorio `specs/` completo)
4. Implementar agentes referenciando sus specs
5. Implementar skills
6. Implementar hooks
7. Escribir la plantilla CLAUDE.md
8. Escribir `init-proyecto.sh`
9. Autorrevisión: ejecutar lógica de `verificacion-specs.py` manualmente
