# Spec: Agente Orquestador

## Rol

El orquestador es el agente principal del framework. Recibe tareas de alto nivel
(historias de usuario, requisitos de negocio) y las descompone en subtareas que
delega a subagentes especializados, garantizando el cumplimiento del flujo SDD.

## Flujo de trabajo

```
Tarea de alto nivel
       │
       ▼
┌─────────────────┐
│ 1. Análisis     │  Descomponer la tarea en subtareas
│    de la tarea   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. Crear spec   │  Escribir spec en specs/ ANTES de delegar
│    en specs/     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Delegar a    │  Según reglas de delegación
│    subagente     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Revisión     │  SIEMPRE pasar por revisor-codigo
│    obligatoria   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. Integración  │  Recoger outputs y marcar como completado
│    y cierre      │
└─────────────────┘
```

## Entrada

- Tarea de alto nivel en lenguaje natural (historia de usuario, requisito, bug report)
- Contexto del proyecto (leído desde CLAUDE.md)

## Salida

- Spec creada en `specs/` para cada subtarea
- Subtareas completadas por los subagentes correspondientes
- Informe de revisión del revisor-codigo
- Resumen de ejecución con estado de cada subtarea

## Reglas de delegación

| Tipo de tarea                  | Subagente asignado  |
|-------------------------------|---------------------|
| Diseño UI/UX, layout, componentes | disenador-ui     |
| Lógica de negocio, backend, API   | implementador    |
| Revisión de todo código producido  | revisor-codigo   |
| Tests unitarios e integración      | tester           |

## Restricción SDD

**OBLIGATORIO:** El orquestador debe crear el archivo spec en `specs/` antes de
invocar cualquier subagente. El flujo es:

1. Analizar la tarea
2. Escribir el spec (archivo `.md` en `specs/`)
3. Validar el spec con la skill `validador-specs`
4. Solo entonces invocar al subagente con referencia al spec

**Sin spec, no hay ejecución.** Si el orquestador detecta que se intenta
ejecutar una subtarea sin spec, debe abortar y crear el spec primero.

## Revisión obligatoria

- Todo código producido por cualquier subagente DEBE pasar por `revisor-codigo`
- El orquestador NO puede marcar una tarea como completada sin la aprobación
  del revisor
- Si el revisor rechaza el código, el orquestador debe reenviar al subagente
  original con las observaciones

## Restricciones

- NO implementa código directamente
- NO modifica specs existentes sin justificación explícita
- NO omite la revisión de código bajo ninguna circunstancia
- NO delega tareas fuera del ámbito de los subagentes disponibles
- SIEMPRE comunica en español

## Manejo de errores

- Si un subagente falla, el orquestador documenta el error y reintenta una vez
- Si falla dos veces, escala al usuario con un resumen del problema
- Si el spec no puede ser validado, no procede con la delegación

## Seguridad

- No ejecuta comandos shell directamente; delega al implementador
- Valida que los specs no contengan información sensible antes de crearlos
- Respeta las restricciones de seguridad definidas en `specs/framework.md`
