# Skill: Revisión de Seguridad

## Descripción

Checklist de seguridad alineado con OWASP Top 10 para la revisión de código.
Proporciona un procedimiento sistemático para identificar vulnerabilidades
comunes en el código producido por los subagentes.

## Condición de activación

Esta skill se activa cuando:
- El subagente `revisor-codigo` revisa código producido por cualquier subagente
- Se necesita una auditoría de seguridad de código existente

## Procedimiento

### 1. A01 — Inyección

- [ ] Las consultas a BD usan parámetros preparados (nunca concatenación)
- [ ] Los comandos del sistema usan listas de argumentos (no `shell=True`)
- [ ] Las consultas LDAP/XPath están parametrizadas
- [ ] No se usa `eval()`, `exec()` ni equivalentes con input externo

### 2. A02 — Autenticación rota

- [ ] Las contraseñas se hashean con algoritmo seguro (bcrypt, argon2)
- [ ] Los tokens de sesión son aleatorios y de longitud suficiente
- [ ] Existe protección contra fuerza bruta (rate limiting)
- [ ] Los endpoints sensibles requieren autenticación

### 3. A03 — Exposición de datos sensibles

- [ ] No hay secretos hardcodeados (contraseñas, API keys, tokens)
- [ ] Los datos sensibles se cifran en tránsito (HTTPS/TLS)
- [ ] Los datos sensibles se cifran en reposo cuando aplica
- [ ] Los logs no registran datos sensibles (contraseñas, tokens)

### 4. A04 — Entidades externas XML (XXE)

- [ ] El parsing XML desactiva entidades externas
- [ ] Se usa JSON en lugar de XML cuando es posible
- [ ] Se valida el schema de los documentos XML recibidos

### 5. A05 — Control de acceso roto

- [ ] Existe verificación de autorización en cada endpoint
- [ ] Los IDs de recursos no son predecibles (o se valida propiedad)
- [ ] Se aplica principio de mínimo privilegio
- [ ] Los endpoints administrativos están protegidos

### 6. A06 — Configuración incorrecta de seguridad

- [ ] Los headers de seguridad están configurados (CSP, HSTS, X-Frame-Options)
- [ ] El modo debug está desactivado en producción
- [ ] Los mensajes de error no exponen información interna
- [ ] Las dependencias no tienen vulnerabilidades conocidas

### 7. A07 — Cross-Site Scripting (XSS)

- [ ] Todo output HTML está escapado apropiadamente
- [ ] Se usa Content Security Policy (CSP)
- [ ] Los atributos HTML dinámicos están sanitizados
- [ ] No se usa `innerHTML` con datos no confiables

### 8. A08 — Deserialización insegura

- [ ] No se deserializan datos de fuentes no confiables sin validación
- [ ] Se usa JSON en lugar de formatos binarios cuando es posible
- [ ] Se valida el tipo y estructura de los datos deserializados

### 9. A09 — Componentes con vulnerabilidades conocidas

- [ ] Las dependencias están actualizadas
- [ ] Se ha verificado que no hay CVEs activos en las dependencias
- [ ] Se usa un lock file para fijar versiones

### 10. A10 — Logging y monitoreo insuficiente

- [ ] Los eventos de seguridad se registran (login fallido, acceso denegado)
- [ ] Los logs tienen información suficiente para auditoría
- [ ] Los logs no contienen datos sensibles

## Formato de resultado

```markdown
## Revisión de Seguridad

### Resultado: SIN HALLAZGOS | CON HALLAZGOS

### Resumen
- Categorías revisadas: 10/10
- Hallazgos críticos: X
- Hallazgos medios: X
- Hallazgos bajos: X

### Hallazgos
1. **[CRÍTICO/MEDIO/BAJO]** Categoría OWASP — Descripción del hallazgo
   - Archivo: `ruta/al/archivo.py:línea`
   - Recomendación: cómo corregirlo
```

## Salida esperada

Informe de revisión de seguridad con hallazgos clasificados por severidad.
Si hay hallazgos CRÍTICOS, el código debe ser rechazado por el revisor.
