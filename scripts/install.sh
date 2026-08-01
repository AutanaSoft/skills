#!/usr/bin/env bash
# install.sh — Crea symlinks globales para Codex, OpenCode y ~/.agents/skills.
# Equivalente portable de: npx skills add <repo> --all -g -a codex -a opencode -y
#
# Uso:
#   ./scripts/install.sh                # instala todas las skills globales
#   ./scripts/install.sh --dry-run      # muestra qué haría sin hacer nada
#   ./scripts/install.sh --project DIR  # instala en .agents/skills/ del proyecto DIR
#   ./scripts/install.sh --skill NAME   # instala solo una skill por nombre

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DRY_RUN=false
SCOPE="global"
PROJECT_DIR=""
SINGLE_SKILL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
  --dry-run)
    DRY_RUN=true
    shift
    ;;
  --project)
    SCOPE="project"
    PROJECT_DIR="$2"
    shift 2
    ;;
  --skill)
    SINGLE_SKILL="$2"
    shift 2
    ;;
  -h | --help)
    sed -n '2,12p' "$0"
    exit 0
    ;;
  *)
    echo "Unknown flag: $1"
    exit 1
    ;;
  esac
done

# Destinos: cada agente busca skills en su propia carpeta
declare -A GLOBAL_TARGETS=(
  ["~/.agents/skills"]="$HOME/.agents/skills"
  ["~/.codex/skills"]="$HOME/.codex/skills"
  ["~/.config/opencode/skills"]="$HOME/.config/opencode/skills"
)

link_skill() {
  local skill_dir="$1"
  local skill_name="$(basename "$skill_dir")"

  if [[ ! -f "$skill_dir/SKILL.md" ]]; then
    echo "skip: $skill_name (no SKILL.md)"
    return
  fi

  local targets=()
  if [[ "$SCOPE" == "global" ]]; then
    for path in "${GLOBAL_TARGETS[@]}"; do targets+=("$path"); done
  else
    targets=("$PROJECT_DIR/.agents/skills")
  fi

  for target_dir in "${targets[@]}"; do
    mkdir -p "$target_dir"
    local target="$target_dir/$skill_name"

    if [[ -L "$target" ]] && [[ "$(readlink "$target")" == "$skill_dir" ]]; then
      echo "ok:    ${target_dir/#$HOME/~}/$skill_name"
    elif [[ -e "$target" ]]; then
      echo "skip:  ${target_dir/#$HOME/~}/$skill_name (already exists, not a symlink to this repo)"
    else
      if $DRY_RUN; then
        echo "would link: ${target_dir/#$HOME/~}/$skill_name -> $skill_dir"
      else
        ln -s "$skill_dir" "$target"
        echo "linked: ${target_dir/#$HOME/~}/$skill_name"
      fi
    fi
  done
}

# Encontrar skills a instalar
if [[ -n "$SINGLE_SKILL" ]]; then
  mapfile -t skills < <(find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -type d -name "$SINGLE_SKILL" | sort -u)
  if [[ ${#skills[@]} -eq 0 ]]; then
    echo "skill '$SINGLE_SKILL' not found in $REPO_ROOT/skills"
    exit 1
  fi
else
  mapfile -t skills < <(find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -type d | sort)
fi

for skill in "${skills[@]}"; do
  link_skill "$skill"
done
