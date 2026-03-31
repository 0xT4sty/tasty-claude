#!/usr/bin/env bash
# ============================================================================
# init-proyecto.sh — Bootstrap de nuevo proyecto desde el framework
#
# Copia la estructura del framework multi-agente a un directorio destino,
# configura los hooks como ejecutables e inicializa git si es necesario.
#
# Uso: ./scripts/init-proyecto.sh <directorio-destino>
# ============================================================================

set -euo pipefail

# Colores para output
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
SIN_COLOR='\033[0m'

# Directorio del framework (donde vive este script)
DIR_SCRIPT="$(cd "$(dirname "$0")" && pwd)"
DIR_FRAMEWORK="$(cd "${DIR_SCRIPT}/.." && pwd)"

# --- Funciones auxiliares ---

log_info() {
    echo -e "${VERDE}[init]${SIN_COLOR} $1"
}

log_aviso() {
    echo -e "${AMARILLO}[aviso]${SIN_COLOR} $1"
}

log_error() {
    echo -e "${ROJO}[error]${SIN_COLOR} $1" >&2
}

mostrar_uso() {
    echo "Uso: $0 <directorio-destino>"
    echo ""
    echo "Copia la estructura del framework multi-agente de Claude Code"
    echo "al directorio destino especificado."
    echo ""
    echo "Ejemplo:"
    echo "  $0 ~/mi-nuevo-proyecto"
}

# --- Validación de argumentos ---

if [ $# -lt 1 ]; then
    log_error "Falta el directorio destino"
    mostrar_uso
    exit 1
fi

DIR_DESTINO="$1"

# --- Crear directorio destino si no existe ---

if [ -d "${DIR_DESTINO}" ]; then
    log_aviso "El directorio ${DIR_DESTINO} ya existe"
else
    mkdir -p "${DIR_DESTINO}"
    log_info "Directorio creado: ${DIR_DESTINO}"
fi

# --- Copiar estructura del framework ---

log_info "Copiando estructura del framework..."

# Directorios a copiar
DIRECTORIOS=(
    "specs"
    "scripts"
    ".claude"
)

for dir in "${DIRECTORIOS[@]}"; do
    if [ -d "${DIR_FRAMEWORK}/${dir}" ]; then
        cp -r "${DIR_FRAMEWORK}/${dir}" "${DIR_DESTINO}/"
        log_info "  Copiado: ${dir}/"
    else
        log_aviso "  No encontrado: ${dir}/ (omitido)"
    fi
done

# Copiar CLAUDE.md
if [ -f "${DIR_FRAMEWORK}/CLAUDE.md" ]; then
    cp "${DIR_FRAMEWORK}/CLAUDE.md" "${DIR_DESTINO}/"
    log_info "  Copiado: CLAUDE.md"
fi

# --- Hacer ejecutables los hooks ---

log_info "Configurando permisos de hooks..."

find "${DIR_DESTINO}/.claude/hooks" -name "*.py" -type f -exec chmod +x {} \; 2>/dev/null || true
find "${DIR_DESTINO}/scripts" -name "*.sh" -type f -exec chmod +x {} \; 2>/dev/null || true

log_info "Hooks y scripts marcados como ejecutables"

# --- Inicializar git si no existe ---

if [ ! -d "${DIR_DESTINO}/.git" ]; then
    log_info "Inicializando repositorio git..."
    git -C "${DIR_DESTINO}" init -q
    log_info "Repositorio git inicializado"
else
    log_aviso "Repositorio git ya existe, no se reinicializa"
fi

# --- Resumen final ---

echo ""
log_info "=========================================="
log_info "  Proyecto inicializado correctamente"
log_info "=========================================="
echo ""
log_info "Directorio: ${DIR_DESTINO}"
echo ""
log_info "Estructura copiada:"
log_info "  .claude/agents/   — Definiciones de agentes"
log_info "  .claude/skills/   — Skills reutilizables"
log_info "  .claude/hooks/    — Hooks del ciclo de vida"
log_info "  .claude/settings.json — Configuración de hooks"
log_info "  specs/             — Especificaciones SDD"
log_info "  scripts/           — Scripts de utilidad"
log_info "  CLAUDE.md          — Plantilla del proyecto"
echo ""
log_info "Próximos pasos:"
log_info "  1. Edita CLAUDE.md con los datos de tu proyecto"
log_info "  2. Revisa .claude/settings.json para los hooks"
log_info "  3. Crea tu primer spec en specs/"
echo ""
