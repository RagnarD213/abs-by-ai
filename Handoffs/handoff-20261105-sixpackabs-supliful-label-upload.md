# Handoff: upload the six final SixPackAbs labels to Supliful

Written 2026-11-05. **Fire only after Dan has looked at the 2D designs and says to submit.** Recommended model: Claude Sonnet 5.5, medium effort. This is a mechanical browser task.

## Goal

In Dan's signed-in Supliful account (Chrome), put the six approved, locked label PDFs and product images on the six matching products. Then stop before ordering anything.

## Read first

- `Contest/approved/LABELS-FINAL-LOCK-20261105.md`: the lock, the file list and the hashes.
- `Handoffs/sixpackabs-production-20261103/SUPLIFUL-SPECS.md`: the editor, upload rules and guides. No need to redo that research.

## Files (local, never commit `Contest/`: the PDFs contain Dan's home address)

`Contest/approved/sixpackabs-labels-final-20261105/`, one folder per product:

| Folder | Supliful product (bottom product bar in the Label Editor) |
|---|---|
| 01 Electro Creatine | Creatine Hydration Powder |
| 02 Great Again T | Men's Vitality |
| 03 Eternal Burn AM | Fat Burner with MCT |
| 04 Eternal Burn PM | Sleep Formula |
| 05 Carb Curber | Metabolic Health Formula |
| 06 Z Shred Support | GLP-1 Support |

Each folder holds `<name> - label upload.pdf` (upload this) and `<name> - product image.png` (2048 px mockup on Supliful's own PSD; use it where the product's image or mockup can be replaced).

## Steps

1. Check every PDF's SHA-256 against `manifest.json` before uploading. Stop if any file differs.
2. Open the Supliful Label Editor in Chrome (Dan is signed in). For each product: Upload file, choose its PDF, and check that the editor's four guides (bleed, safe, trim, matrix code) sit right with nothing important outside the safe line. Take a screenshot of each.
3. Apply the label to the product once the preview matches. If the editor reports any error (size, file type, fonts), stop on that product, record the exact message and continue with the others.
4. Replace the product image with `<name> - product image.png` where Supliful allows it.
5. Set the product names to the brand names (Electro Creatine, etc.) only if the editor asks for a product name. Do not invent descriptions.
6. Do **not** publish products to a store, order samples or physical proofs, pay, or change Dan's membership. Those wait for Dan.
7. Write a receipt in `Docs/SIXPACKABS_SUPLIFUL_LABEL_UPLOAD_RECEIPT_20261105.md`: per product, the upload result, editor status, screenshot paths and any error. Commit it with `scripts/git/safe-push.sh`. The receipt must not contain the address.
8. Remove this handoff from `Handoffs/README.md` OPEN once done, and report to Dan with the two wrap-up boxes. The next step is his: order a physical proof.

## Do not

- Re-edit the artwork. The design is locked. If an upload fails for technical reasons, re-save that PDF from Acrobat ("High Quality Print", Optimize for Fast Web View) without changing the art, record that, and retry once.
- Put the flat PDFs or SVGs anywhere public.
