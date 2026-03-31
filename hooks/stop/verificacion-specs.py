#!/usr/bin/env python3
"""
Hook stop: Verificación de specs al finalizar la sesión.

Al finalizar una sesión de Claude Code, verifica si los archivos
modificados tienen un spec asociado en el directorio specs/.
Advierte si algún archivo de implementación no tiene spec.

Este hook es informativo (exit 0 siempre), nunca bloquea.
"""

import os
import subprocess
import sys

# Directorios/archivos excluidos de la verificación de specs.
# Estos archivos no necesitan spec asociada.
EXCLUIDOS = [
    "specs/",
    "CLAUDE.md",
    "README.md",
    "hooks/",
    "skills/",
    "scripts/",
    ".claude/",
    ".git/",
    ".gitignore",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    "pyproject.toml",
    "Makefile",
    "Dockerfile",
    "docker-compose",
]


def log(mensaje: str) -> None:
    """Escribe un mensaje de log a stderr en español."""
    print(f"[verificacion-specs] {mensaje}", file=sys.stderr)


def obtener_archivos_modificados() -> list:
    """Obtiene la lista de archivos modificados desde el último commit."""
    try:
        # Archivos modificados en staging + working tree
        resultado = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        archivos = []
        if resultado.returncode == 0 and resultado.stdout.strip():
            archivos = resultado.stdout.strip().split("\n")

        # También incluir archivos sin seguimiento (untracked)
        resultado_untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if resultado_untracked.returncode == 0 and resultado_untracked.stdout.strip():
            archivos.extend(resultado_untracked.stdout.strip().split("\n"))

        return archivos

    except FileNotFoundError:
        log("Git no disponible, no se puede verificar archivos modificados")
        return []
    except subprocess.TimeoutExpired:
        log("Tiempo excedido al consultar git")
        return []


def esta_excluido(archivo: str) -> bool:
    """Verifica si un archivo está en la lista de exclusiones."""
    for excluido in EXCLUIDOS:
        if archivo.startswith(excluido) or archivo == excluido:
            return True
    return False


def buscar_spec_asociado(archivo: str) -> bool:
    """
    Busca si existe un spec asociado al archivo dado.

    Convención de búsqueda:
    - Para agentes/subagentes/X.md → specs/agentes/X.md
    - Para agentes/X.md → specs/X.md
    - Para src/modulo/archivo.py → specs/modulo/archivo.md o specs/archivo.md
    - Búsqueda genérica por nombre base en specs/
    """
    nombre_base = os.path.splitext(os.path.basename(archivo))[0]

    # Rutas posibles de spec
    rutas_posibles = [
        os.path.join("specs", f"{nombre_base}.md"),
        os.path.join("specs", "agentes", f"{nombre_base}.md"),
    ]

    # Si el archivo está en un subdirectorio, buscar con esa estructura
    directorio = os.path.dirname(archivo)
    if directorio:
        rutas_posibles.append(
            os.path.join("specs", directorio, f"{nombre_base}.md")
        )

    for ruta in rutas_posibles:
        if os.path.isfile(ruta):
            return True

    return False


def main() -> None:
    """Punto de entrada principal del hook."""
    log("Verificando cobertura de specs para archivos modificados...")

    archivos = obtener_archivos_modificados()
    if not archivos:
        log("No se detectaron archivos modificados")
        sys.exit(0)

    sin_spec = []
    verificados = 0

    for archivo in archivos:
        if esta_excluido(archivo):
            continue

        verificados += 1
        if not buscar_spec_asociado(archivo):
            sin_spec.append(archivo)

    # Resumen
    if verificados == 0:
        log("No hay archivos de implementación que verificar")
    elif sin_spec:
        log(f"ADVERTENCIA: {len(sin_spec)} archivo(s) sin spec asociado:")
        for archivo in sin_spec:
            log(f"  - {archivo}")
        log("Considera crear specs para estos archivos en el directorio specs/")
    else:
        log(f"Todos los {verificados} archivo(s) verificados tienen spec asociado")

    # Siempre exit 0 — este hook es informativo
    sys.exit(0)


if __name__ == "__main__":
    main()
