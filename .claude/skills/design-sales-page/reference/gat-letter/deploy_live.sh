#!/bin/zsh
# Pushes ONLY the Great Again T funnel files to the live shop theme, from the M2 (where the Shopify CLI is signed in).
# Run after `python3 build_live.py`. Never pushes any other theme file.
set -e
T="$HOME/Projects/Claude/Projects/SixPackAbs Shop Theme"; R='Projects/Claude/Projects/SixPackAbs\ Shop\ Theme'
cd "$T"
rsync -a --delete --include='gat*' --exclude='*' assets/ m2:"$R/assets/"
rsync -a --include='gat.liquid' --exclude='*' layout/ m2:"$R/layout/"
rsync -a --delete --include='page.gat-*.liquid' --exclude='*' templates/ m2:"$R/templates/"
rsync -a --delete --include='gat-info-*.liquid' --exclude='*' snippets/ m2:"$R/snippets/"
ssh -o ConnectTimeout=8 m2 'export PATH=/usr/local/bin:/opt/homebrew/bin:$HOME/.npm-global/bin:$PATH; cd ~/Projects/Claude/Projects/"SixPackAbs Shop Theme" && shopify theme push --store 1yar3v-ie.myshopify.com --theme 195457614146 --allow-live --nodelete --no-color --only "layout/gat.liquid" --only "templates/page.gat-*.liquid" --only "snippets/gat-info-*.liquid" --only "assets/gat*" 2>&1 | tail -6'
