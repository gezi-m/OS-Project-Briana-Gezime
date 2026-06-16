#!/bin/bash
# file_organizer.sh -- Novel tool: classify and organize files by extension
declare -A counts

classify() {
    case "${1##*.}" in
        pdf|doc|docx|txt|md)  echo "documents" ;;
        jpg|jpeg|png|gif|svg) echo "images"    ;;
        sh|py|js|c|h|java|cpp) echo "code"    ;;
        zip|tar|gz|bz2|7z)   echo "archives"  ;;
        *)                    echo "other"     ;;
    esac
}

for f in *; do
    [ -f "$f" ] || continue
    [ "$f" = "$(basename $0)" ] && continue
    category=$(classify "$f")
    mkdir -p "$category"
    dst="$category/$f"
    counter=1
    while [ -e "$dst" ]; do
        dst="$category/${f%.*}_${counter}.${f##*.}"
        (( counter++ ))
    done
    mv "$f" "$dst"
    counts[$category]=$(( ${counts[$category]:-0} + 1 ))
done

echo "=== File Organizer Summary ==="
for cat in "${!counts[@]}"; do
    echo "  $cat: ${counts[$cat]} file(s)"
done
