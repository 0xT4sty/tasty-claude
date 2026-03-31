#!/usr/bin/env python3
"""
Hook pre-tool-use: Puerta de seguridad para comandos shell.

Lee la entrada JSON de Claude Code via stdin, verifica si el comando
está en la lista de patrones permitidos (allowlist) y bloquea la
ejecución si no lo está.

Enfoque: ALLOWLIST — solo se permiten comandos que coincidan con
patrones explícitamente autorizados.
"""

import json
import re
import sys

# Lista de patrones permitidos (regex).
# Solo los comandos que coincidan con al menos un patrón se permiten.
ALLOWLIST = [
    # --- Git ---
    r"^git\b",
    # --- Navegación y lectura del sistema de archivos ---
    r"^ls\b",
    r"^tree\b",
    r"^pwd$",
    r"^cat\b",
    r"^head\b",
    r"^tail\b",
    r"^less\b",
    r"^wc\b",
    r"^file\b",
    r"^stat\b",
    r"^du\b",
    r"^df\b",
    r"^find\b",
    r"^readlink\b",
    r"^realpath\b",
    # --- Búsqueda de contenido ---
    r"^grep\b",
    r"^rg\b",
    r"^ag\b",
    r"^awk\b",
    r"^sed\b",
    # --- Python ---
    r"^python3?\b",
    r"^pip3?\b",
    r"^pip\b",
    r"^pytest\b",
    r"^mypy\b",
    r"^flake8\b",
    r"^black\b",
    r"^isort\b",
    r"^bandit\b",
    r"^pylint\b",
    r"^ruff\b",
    # --- Node.js ---
    r"^node\b",
    r"^npm\b",
    r"^npx\b",
    r"^yarn\b",
    r"^pnpm\b",
    r"^eslint\b",
    r"^prettier\b",
    r"^tsc\b",
    r"^tsx\b",
    r"^vitest\b",
    r"^jest\b",
    # --- Build y utilidades de desarrollo ---
    r"^make\b",
    r"^cargo\b",
    r"^go\b",
    r"^rustc\b",
    r"^gcc\b",
    r"^g\+\+\b",
    r"^cmake\b",
    r"^docker\b",
    r"^docker-compose\b",
    # --- Shell básico (solo lectura) ---
    r"^echo\b",
    r"^printf\b",
    r"^whoami$",
    r"^date$",
    r"^env$",
    r"^printenv\b",
    r"^which\b",
    r"^type\b",
    r"^command\b",
    r"^dirname\b",
    r"^basename\b",
    # --- Operaciones de directorio seguras ---
    r"^mkdir\b",
    r"^cp\b",
    r"^mv\b",
    r"^touch\b",
    r"^chmod\b",
    r"^ln\b",
    # --- Herramientas de red seguras (solo lectura) ---
    r"^curl\b",
    r"^wget\b",
    r"^ping\b",
    r"^dig\b",
    r"^nslookup\b",
    r"^ssh\b",
    # --- Utilidades de texto ---
    r"^sort\b",
    r"^uniq\b",
    r"^cut\b",
    r"^tr\b",
    r"^diff\b",
    r"^patch\b",
    r"^jq\b",
    r"^xargs\b",
    # --- Claude Code ---
    r"^claude\b",
]

# Patrones peligrosos que se bloquean incluso si el comando base está permitido.
# Estos se verifican sobre el comando completo.
PATRONES_PELIGROSOS = [
    r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\b",
    r"\brm\s+-rf\b",
    r"\|\s*bash\b",
    r"\|\s*sh\b",
    r"\|\s*zsh\b",
    r"\beval\b",
    r"\bexec\b",
    r"\bchmod\s+777\b",
    r"\bchmod\s+-R\s+777\b",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\b>\s*/dev/sd[a-z]",
    r"\bsudo\s+rm\b",
    r"\bsudo\s+chmod\s+777\b",
]


def log(mensaje: str) -> None:
    """Escribe un mensaje de log a stderr en español."""
    print(f"[security-gate] {mensaje}", file=sys.stderr)


def extraer_comando(datos: dict) -> str:
    """Extrae el comando shell del JSON de entrada de Claude Code."""
    # El formato de entrada de un hook pre-tool-use es:
    # {"tool_name": "Bash", "tool_input": {"command": "..."}}
    tool_input = datos.get("tool_input", {})
    if isinstance(tool_input, dict):
        return tool_input.get("command", "")
    return ""


def obtener_comando_base(comando: str) -> str:
    """
    Obtiene el primer comando de una cadena que puede tener pipes o encadenamiento.
    Para verificar contra la allowlist, se analiza el primer comando.
    """
    # Eliminar espacios al inicio
    comando = comando.strip()

    # Si empieza con variable de entorno (VAR=valor comando), extraer el comando
    while re.match(r"^[A-Za-z_][A-Za-z0-9_]*=\S+\s+", comando):
        comando = re.sub(r"^[A-Za-z_][A-Za-z0-9_]*=\S+\s+", "", comando)

    return comando


def comando_permitido(comando: str) -> bool:
    """Verifica si el comando está en la allowlist."""
    comando_base = obtener_comando_base(comando)

    if not comando_base:
        return False

    for patron in ALLOWLIST:
        if re.search(patron, comando_base):
            return True

    return False


def tiene_patron_peligroso(comando: str) -> bool:
    """Verifica si el comando contiene patrones peligrosos."""
    for patron in PATRONES_PELIGROSOS:
        if re.search(patron, comando):
            return True
    return False


def main() -> None:
    """Punto de entrada principal del hook."""
    try:
        entrada = sys.stdin.read()
        if not entrada.strip():
            # Sin entrada, permitir la ejecución (no es un comando Bash)
            sys.exit(0)

        datos = json.loads(entrada)
    except json.JSONDecodeError:
        # Si no se puede parsear el JSON, registrar y permitir
        # (fail-open para errores internos del hook, no del usuario)
        log("Error: no se pudo parsear la entrada JSON, permitiendo ejecución")
        sys.exit(0)

    # Solo verificar herramientas de tipo Bash
    tool_name = datos.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    comando = extraer_comando(datos)
    if not comando:
        log("Advertencia: comando vacío recibido")
        sys.exit(0)

    # Verificar patrones peligrosos primero
    if tiene_patron_peligroso(comando):
        log(f"BLOQUEADO (patrón peligroso): {comando}")
        sys.exit(2)

    # Verificar allowlist
    if not comando_permitido(comando):
        log(f"BLOQUEADO (no está en allowlist): {comando}")
        sys.exit(2)

    # Comando permitido
    log(f"Permitido: {comando[:80]}{'...' if len(comando) > 80 else ''}")
    sys.exit(0)


if __name__ == "__main__":
    main()
