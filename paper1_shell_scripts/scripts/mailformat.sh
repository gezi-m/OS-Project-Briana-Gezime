#!/bin/bash
# mailformat.sh v1.1 -- strips email quoting artifacts and folds long lines
# Usage: bash mailformat.sh <filename>
E_BADARGS=85
E_NOFILE=86
MAXWIDTH=70

if [ -z "$1" ]; then
    echo "Usage: $(basename $0) filename"
    exit $E_BADARGS
fi

if [ ! -f "$1" ]; then
    echo "File not found: $1"
    exit $E_NOFILE
fi

sedscript='s/^>//; s/^ *>//; s/^ *//; s/\t*//'
sed "$sedscript" "$1" | fold -s -w $MAXWIDTH
