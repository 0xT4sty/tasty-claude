#!/usr/bin/env python3
"""
Hook post-tool-use: Ejecuta linter al escribir archivos.

Cuando Claude Code escribe o edita un archivo, este hook ejecuta el
linter correspondiente según la extensión del archivo. Solo advierte,
nunca bloquea (exit 0 siempre).
"""

import json
import os
import subprocess
import sys

# Mapeo de extensiones a comandos de linting.
# Cada entrada es: extensión -> (comando, argumentos)
# El placeholder {archivo} se reemplaza con la ruta del archivo.
LINTERS = {
    ".py": {
        "nombre": "py_compile",
        "comando": ["python3", "-m", "py_compile", "{archivo}"],
    },
    ".js": {
        "nombre": "eslint",
        "comando": ["npx", "eslint", "--no-error-on-unmatched-pattern", "{archivo}"],
    },
    ".ts": {
        "nombre": "eslint",
        "comando": ["npx", "eslint", "--no-error-on-unmatched-pattern", "{archivo}"],
    },
    ".jsx": {
        "nombre": "eslint",
        "comando": ["npx", "eslint", "--no-error-on-unmatched-pattern", "{archivo}"],
    },
    ".tsx": {
        "nombre": "eslint",
        "comando": ["npx", "eslint", "--no-error-on-unmatched-pattern", "{archivo}"],
    },
    ".json": {
        "nombre": "json.tool",
        "comando": ["python3", "-m", "json.tool", "{archivo}"],
    },
    ".yaml": {
        "nombre": "yaml check",
        "comando": ["python3", "-c", "import yaml, sys; yaml.safe_load(open(sys.argv[1]))", "{archivo}"],
    },
    ".yml": {
        "nombre": "yaml check",
        "comando": ["python3", "-c", "import yaml, sys; yaml.safe_load(open(sys.argv[1]))", "{archivo}"],
    },
}


def log(mensaje: str) -> None:
    """Escribe un mensaje de log a stderr en español."""
    print(f"[lint-al-escribir] {mensaje}", file=sys.stderr)


def extraer_ruta_archivo(datos: dict) -> str:
    """Extrae la ruta del archivo del JSON de entrada de Claude Code."""
    tool_input = datos.get("tool_input", {})
    if isinstance(tool_input, dict):
        # Write y Edit usan "file_path"
        return tool_input.get("file_path", "")
    return ""


def ejecutar_linter(ruta: str) -> None:
    """Ejecuta el linter correspondiente según la extensión del archivo."""
    if not ruta or not os.path.isfile(ruta):
        return

    _, extension = os.path.splitext(ruta)
    extension = extension.lower()

    if extension not in LINTERS:
        return

    linter = LINTERS[extension]
    nombre = linter["nombre"]
    comando = [arg.replace("{archivo}", ruta) for arg in linter["comando"]]

    log(f"Ejecutando {nombre} en {os.path.basename(ruta)}")

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if resultado.returncode != 0:
            log(f"Advertencia de {nombre}:")
            if resultado.stderr:
                for linea in resultado.stderr.strip().split("\n"):
                    log(f"  {linea}")
            if resultado.stdout:
                for linea in resultado.stdout.strip().split("\n"):
                    log(f"  {linea}")
        else:
            log(f"{nombre}: sin errores")

    except FileNotFoundError:
        log(f"Linter {nombre} no disponible en el sistema")
    except subprocess.TimeoutExpired:
        log(f"Linter {nombre} excedió el tiempo límite (30s)")


def main() -> None:
    """Punto de entrada principal del hook."""
    try:
        entrada = sys.stdin.read()
        if not entrada.strip():
            sys.exit(0)

        datos = json.loads(entrada)
    except json.JSONDecodeError:
        log("Error: no se pudo parsear la entrada JSON")
        sys.exit(0)

    # Solo procesar herramientas de escritura/edición
    tool_name = datos.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    ruta = extraer_ruta_archivo(datos)
    if ruta:
        ejecutar_linter(ruta)

    # Nunca bloquear — este hook es solo informativo
    sys.exit(0)


if __name__ == "__main__":
    main()
