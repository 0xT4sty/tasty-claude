# Skills del Framework

Skills reutilizables e independientes del dominio para Claude Code.

## ¿Qué es una skill?

Una skill es un procedimiento documentado en markdown que Claude Code puede
seguir para realizar una tarea específica. Cada skill define:

- **Descripción:** qué hace la skill
- **Condición de activación:** cuándo debe usarse
- **Procedimiento:** pasos a seguir
- **Salida esperada:** qué produce la skill

## Skills disponibles

| Skill                  | Archivo                  | Descripción                                      |
|------------------------|--------------------------|--------------------------------------------------|
| Formato de commits     | `formato-commits.md`     | Enforce de conventional commits en español        |
| Validador de specs     | `validador-specs.md`     | Verifica secciones requeridas en un spec          |
| Revisión de seguridad  | `revision-seguridad.md`  | Checklist OWASP para revisión de código           |

## Uso

Las skills son invocadas por los agentes durante su flujo de trabajo. El
orquestador y los subagentes referencian las skills cuando corresponde:

- El **orquestador** usa `validador-specs` antes de delegar
- El **revisor-codigo** usa `revision-seguridad` durante la revisión
- Todos los agentes siguen `formato-commits` al hacer commits

## Crear nuevas skills

Para agregar una skill al framework, crea un archivo `.md` en este directorio
con las secciones: Descripción, Condición de activación, Procedimiento y
Salida esperada.
