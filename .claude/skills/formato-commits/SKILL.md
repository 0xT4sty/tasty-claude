# Skill: Formato de Commits

## Descripción

Garantiza que todos los mensajes de commit sigan el estándar Conventional
Commits adaptado al español. Esto facilita la generación automática de
changelogs y la comprensión del historial del proyecto.

## Condición de activación

Esta skill se activa cada vez que se va a crear un commit en el proyecto.

## Procedimiento

### 1. Estructura del mensaje

```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[pie opcional]
```

### 2. Tipos permitidos

| Tipo       | Uso                                                |
|------------|----------------------------------------------------|
| `feat`     | Nueva funcionalidad                                |
| `fix`      | Corrección de bug                                  |
| `docs`     | Cambios en documentación                           |
| `style`    | Formato, punto y coma faltante, etc. (sin cambio de lógica) |
| `refactor` | Refactorización de código (sin cambio funcional)   |
| `test`     | Agregar o corregir tests                           |
| `chore`    | Tareas de mantenimiento, configuración, dependencias |
| `ci`       | Cambios en integración continua                    |
| `perf`     | Mejora de rendimiento                              |

### 3. Reglas

- **Tipo:** obligatorio, en minúsculas, del listado anterior
- **Alcance:** opcional, entre paréntesis, indica el módulo afectado
  - Ejemplos: `(hooks)`, `(agentes)`, `(skills)`, `(specs)`
- **Descripción:** obligatoria, en español, imperativo, sin punto final
  - Máximo 72 caracteres
  - Empieza con minúscula
  - Describe QUÉ cambia, no CÓMO
- **Cuerpo:** opcional, separado por línea en blanco, explica el POR QUÉ
- **Pie:** opcional, para referencias a issues o breaking changes

### 4. Ejemplos válidos

```
feat(agentes): agregar subagente diseñador de UI

fix(hooks): corregir parsing de JSON en security-gate

docs(specs): actualizar spec del orquestador con reglas de delegación

refactor(skills): simplificar lógica de validación de specs

test(hooks): agregar tests de dry-run para lint-al-escribir

chore: actualizar dependencias de Python
```

### 5. Ejemplos inválidos

```
# MAL: tipo en mayúscula
Feat: agregar agente

# MAL: descripción en inglés
fix: update security gate

# MAL: punto final
feat(hooks): agregar security gate.

# MAL: no describe qué cambia
fix: arreglar cosas
```

## Salida esperada

Un mensaje de commit que cumpla todas las reglas anteriores, listo para
ejecutar con `git commit -m "..."`.
