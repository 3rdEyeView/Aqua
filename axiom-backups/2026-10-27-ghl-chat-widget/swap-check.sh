# Counts the new/old widget IDs and loader tags on each public page (plain cached URL and uncached).
for u in / /pricing/ /add-ons/ /faq/ /get-started/ /how-it-works/ /our-work/ /does-not-exist-404/; do
  h=$(curl -s -D /tmp/claude-0/hdr "https://axiomsystems.systems$u" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"); c=$(grep -i '^x-kinsta-cache:' /tmp/claude-0/hdr | tr -d '\r' | cut -d' ' -f2)
  h2=$(curl -s "https://axiomsystems.systems$u?nc=$RANDOM$RANDOM" -A Mozilla/5.0)
  printf "%-22s cached(%s): new=%s old=%s loaders=%s | uncached: new=%s old=%s loaders=%s\n" "$u" "$c" \
    "$(echo "$h" | grep -o 'data-widget-id="6adfdfee388cb81c668e729a"' | wc -l)" "$(echo "$h" | grep -o 6adf9aa5388cb81c665a7bda | wc -l)" "$(echo "$h" | grep -o 'leadconnectorhq.com/loader.js' | wc -l)" \
    "$(echo "$h2" | grep -o 'data-widget-id="6adfdfee388cb81c668e729a"' | wc -l)" "$(echo "$h2" | grep -o 6adf9aa5388cb81c665a7bda | wc -l)" "$(echo "$h2" | grep -o 'leadconnectorhq.com/loader.js' | wc -l)"
done
