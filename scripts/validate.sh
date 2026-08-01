#!/usr/bin/env bash
# Valida todas las skills con el validador del repositorio y luego
# el marketplace.json. Falla si alguna validación falla.
#
# Requisitos: python3 con el módulo 'yaml' instalado. Para preparar el
# entorno: `mise install python && pip install pyyaml`.

set -euo pipefail

cd "$(dirname "$0")/.."

# Sanity checks para herramientas requeridas.
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 no encontrado en PATH. Instalar Python 3 antes de validar." >&2
  exit 1
fi

if ! python3 -c "import yaml" >/dev/null 2>&1; then
  echo "ERROR: módulo 'yaml' de Python no disponible. Ejecutar: pip install pyyaml" >&2
  exit 1
fi

QUICK_VALIDATE="scripts/quick_validate.py"

if [[ ! -f "$QUICK_VALIDATE" ]]; then
  echo "ERROR: quick_validate.py no encontrado en $QUICK_VALIDATE" >&2
  exit 1
fi

errors=0
while IFS= read -r -d '' skill; do
  if output=$(python3 "$QUICK_VALIDATE" "$skill" 2>&1); then
    echo "Valid skill: $skill"
  else
    echo "FAIL: $skill"
    echo "$output" | sed 's/^/  /'
    errors=$((errors + 1))
  fi
done < <(find skills -mindepth 2 -maxdepth 2 -type d -print0 | sort -z)

if [[ $errors -gt 0 ]]; then
  echo ""
  echo "$errors skill(s) failed validation"
  exit 1
fi

node scripts/validate-marketplace.mjs

if ! command -v pnpm >/dev/null 2>&1; then
  echo "ERROR: pnpm not found in PATH. Install pnpm before running format validation." >&2
  exit 1
fi

pnpm format:check
pnpm lint:markdown
