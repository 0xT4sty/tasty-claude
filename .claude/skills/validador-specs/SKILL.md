# Skill: Validador de Specs

## Descripción

Verifica que un archivo spec contiene todas las secciones requeridas antes de
que un subagente comience a trabajar. Esto garantiza que ninguna tarea se
ejecute con un spec incompleto.

## Condición de activación

Esta skill se activa cuando:
- El orquestador crea un nuevo spec antes de delegar a un subagente
- Se necesita verificar un spec existente antes de iniciar trabajo

## Procedimiento

### 1. Secciones obligatorias

Todo spec debe contener como mínimo estas secciones (encabezados markdown):

| Sección           | Descripción                                              |
|-------------------|----------------------------------------------------------|
| **Rol / Contexto**| Qué se necesita y por qué                               |
| **Entrada**       | Qué recibe el subagente como input                       |
| **Salida**        | Qué debe entregar el subagente                           |
| **Restricciones** | Qué NO debe hacer el subagente                           |
| **Seguridad**     | Consideraciones de seguridad aplicables                  |

### 2. Validación paso a paso

1. Abrir el archivo spec (debe ser un `.md` en el directorio `specs/`)
2. Verificar que existe un título principal (`# ...`)
3. Buscar cada sección obligatoria (como encabezado `##` o `###`):
   - Buscar variantes aceptables:
     - Rol, Contexto, Descripción → sección de contexto
     - Entrada, Input → sección de entrada
     - Salida, Output, Salida esperada → sección de salida
     - Restricciones, Limitaciones → sección de restricciones
     - Seguridad, Reglas de seguridad → sección de seguridad
4. Verificar que cada sección tiene contenido (no está vacía)
5. Emitir resultado: VÁLIDO o INVÁLIDO

### 3. Formato de resultado

```markdown
## Validación de Spec: [nombre del archivo]

### Resultado: VÁLIDO | INVÁLIDO

### Secciones verificadas
- [✓] Título principal
- [✓|✗] Contexto/Rol
- [✓|✗] Entrada
- [✓|✗] Salida
- [✓|✗] Restricciones
- [✓|✗] Seguridad

### Observaciones
(Solo si INVÁLIDO: lista de secciones faltantes o vacías)
```

## Salida esperada

Informe de validación indicando si el spec es válido o qué secciones faltan.
Si el spec es INVÁLIDO, el orquestador NO debe proceder con la delegación.
