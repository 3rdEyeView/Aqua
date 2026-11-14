#!/bin/bash
# Usage: native/csscheck.sh <preview-url> -> how many of the page's V4 style classes the served CSS file contains
T=$(mktemp -d); curl -sS -m 60 -A "Mozilla/5.0" "$1" -o $T/p.html
V=$(grep -o "local-[0-9]*-frontend-desktop.css?ver=[0-9a-f]*" $T/p.html); echo "css: $V"
curl -sS -m 60 "https://axiomsystems.systems/wp-content/uploads/elementor/css/$V" -o $T/c.css
grep -o 'e-[0-9a-f]\{8\}-[0-9a-f]\{4\}' $T/p.html | sort -u > $T/h; grep -o '\.e-[0-9a-f]\{8\}-[0-9a-f]\{4\}' $T/c.css | tr -d . | sort -u > $T/c
echo "html classes $(wc -l < $T/h), css classes $(wc -l < $T/c), in both $(comm -12 $T/h $T/c | wc -l)"; rm -rf $T
