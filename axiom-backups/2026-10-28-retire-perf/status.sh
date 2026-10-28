#!/bin/bash
# status.sh <out>: final status + first redirect target for each URL in urls.txt (cache-busted)
while read u; do sep='?'; [[ $u == *\?* ]] && sep='&'; r=$(curl -sS -o /tmp/claude-0/b.html -A Googlebot -w "%{http_code} %{redirect_url}" "https://axiomsystems.systems$u${sep}nc=$RANDOM"); t=$(grep -o '<title>[^<]*' /tmp/claude-0/b.html | head -1 | cut -c8-60); rb=$(grep -o "<meta name='robots' content='[^']*" /tmp/claude-0/b.html | cut -d"'" -f4); printf "%-82s %s | %s | %s\n" "$u" "$r" "$rb" "$t"; done < urls.txt > $1
