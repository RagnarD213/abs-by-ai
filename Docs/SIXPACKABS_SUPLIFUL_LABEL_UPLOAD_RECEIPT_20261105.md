# SixPackAbs Supliful label upload receipt, 2026-11-05

Run by Claude (Sonnet 5.5) in Dan's signed-in Supliful account via Chrome, from `Handoffs/handoff-20261105-sixpackabs-supliful-label-upload.md`, after Dan reviewed the 2D labels and said submit. Locked design: `Contest/approved/LABELS-FINAL-LOCK-20261105.md`.

## Result: all six uploaded and applied, nothing ordered

Every PDF's SHA-256 matched `manifest.json` before upload (all 12 PDFs and product images, 0 mismatches). Each PDF went in through Label Editor > Upload file. Every one showed "Design uploaded: PDF was converted and applied to all pages" with no size, file-type or font errors. Each was then applied with Apply to product ("Applied to <product>. Your print label is updated"). Supliful reported "Mockups weren't changed", so the product image was replaced separately with the locked `product image.png` through the product page's Label & mockup > Upload image (confirm dialog, Submit). Each product page then showed the new bottle image.

| Brand product | Supliful product | Label PDF | Editor status | Product image |
|---|---|---|---|---|
| Electro Creatine | Creatine Hydration Powder (11 x 3 in) | converted, applied | Applied to product | replaced |
| Great Again T | Men's Vitality (6 x 2.25 in) | converted, applied | Applied to product | replaced |
| Eternal Burn AM | Fat Burner with MCT | converted, applied | Applied to product | replaced |
| Eternal Burn PM | Sleep Formula | converted, applied | Applied to product | replaced |
| Carb Curber | Metabolic Health Formula | converted, applied | Applied to product | replaced |
| Z Shred Support | GLP-1 Support | converted, applied | Applied to product | replaced |

No editor errors on any product, so no PDF was re-saved and nothing was retried.

## Guides check

The editor's four guides (bleed, safe, trim, matrix code) were on for each preview. The black band runs to the top bleed edge by design. The ivory field fills the bleed. All text, the logo and the Supplement Facts sit inside the dashed safe line, and the bottom-left matrix-code zone is clear (Supliful's own code shows there). The preview was read by eye at editor zoom, not measured with a numeric safe-inset check, which Supliful does not publish.

## Not done (Dan's call)

No product published to a store, no sample or proof ordered, no payment, membership untouched (the account still shows "Upgrade now"). Product names were not changed (the editor never asked) and no descriptions were written. All seven products in the account read "Not published". The seventh, Greens Superfood, was not touched.

## Proof order placed (Dan, same day)

Dan checked out the six-product sample order himself after Claude stopped at the payment page. Supliful order SPL1250987, Nov 5, 8:41 AM, total $81.59, status New, shipped to Rose Digital Holdings LLC. Supliful put it **on hold** while it verifies the labels ("usually 1 business day"). Supliful may email about any label problem. The earlier $124.98 sample order SPL1238058 (Oct 21) is Completed.

## What is still open

- Supplier verification: Supliful says the label must pass its verification before fulfillment. Whether it passes is only known once an order or proof goes in.
- Physical print proof: not ordered.
- The distributor block on the labels is Rose Digital Holdings LLC plus Dan's address, at his instruction for now (see the lock file for how to change it).

## Evidence (local only, never commit)

`Contest/approved/sixpackabs-labels-final-20261105/supliful-screenshots-20261105/`: per product, the editor after upload (flat label preview, shows the address) and the product page after the image replacement. `Contest/` is untracked and stays local.

Product ids: Creatine `13f79e13-9e41-47a3-97b6-6186c87d3f69`, Men's Vitality `ce6a49ef-18fa-4022-b011-a0e424b7a254`, Fat Burner `32088d4c-ddab-4b9c-80ed-190394080ecf`, Sleep `8d5e9668-99bf-4872-a603-925dabf41a6b`, Metabolic `36d00d73-a173-440c-9f2e-94f33caba137`, GLP-1 `69949e3f-5807-497e-bd07-9f32c968aad2`.
