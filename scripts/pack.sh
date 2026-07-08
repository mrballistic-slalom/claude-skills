#!/usr/bin/env bash
# Repack all skill source directories into .skill archives.
# Run directly or via the pre-commit hook.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

packed=0

while IFS= read -r skill_md; do
    skill_dir="$(dirname "$skill_md")"
    skill_name="$(basename "$skill_dir")"
    category_dir="$(dirname "$skill_dir")"
    out="${category_dir}/${skill_name}.skill"

    echo "  packing ${out#"$REPO_ROOT"/}"
    (cd "$category_dir" && zip -r -X "$skill_name.skill" "$skill_name" \
        --exclude "*/.DS_Store" \
        --exclude "*/__MACOSX/*" \
        --exclude "*/__pycache__/*" \
        --exclude "*.py[cod]" \
        > /dev/null)
    packed=$((packed + 1))
done < <(find "$REPO_ROOT" -mindepth 3 -maxdepth 3 -name "SKILL.md" | sort)

echo "packed $packed skill(s)"
