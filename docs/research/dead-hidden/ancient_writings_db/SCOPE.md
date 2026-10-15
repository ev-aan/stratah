# Ancient Writings Database: scope (draft 2026-10-14)

**Goal.** One searchable record of ancient writing where the **image of the object is the primary data** and every reading (transliteration, translation, reinterpretation) is a separate, attributed layer on top. Feeds Stratah claims with places, dates and anchors.

## Principles (match Stratah rules)
- Image first. A transcription or translation is never the source (SCHEMA A9: derived entries carry `derived_from`).
- Our own readings are `synthetic`/proposals, never anchors by themselves.
- Record, per object: holder + museum id, findspot, date range (and basis), language/script, licence, source URL, sha256 of the stored image, capture date.
- Respect each archive's terms, robots.txt and rate limits. Licence is verified per archive BEFORE any bulk pull. No Wikipedia as an anchor.
- Where licence forbids storing images: keep link + thumbnail only (Stratah "images-beyond-pages" idea).

## Candidate sources (all need licence/API verification before ingest)
| Area | Candidates | Gives |
|---|---|---|
| Egyptian | Thesaurus Linguae Aegyptiae (TLA); Griffith Institute Topographical Bibliography; Chicago Oriental Institute digital publications (Epigraphic Survey: Karnak, Medinet Habu); Trismegistos; Ramses Online | texts, wall/temple location, drawings and plates |
| Cuneiform | CDLI (images + transliterations); ORACC; ETCSL; Hethitologie Portal Mainz | tablet photos/line art, text, findspot |
| Northwest Semitic / Hebrew | Inscriptions of Israel/Palestine (IIP); Dead Sea Scrolls Digital Library; Sinai Palimpsests; Codex Sinaiticus | manuscript and inscription images |
| Greek / Latin | Papyri.info; Perseus / Open Greek and Latin; PHI Greek Inscriptions; EDR / EDH epigraphy | papyri, inscriptions, texts |
| New Testament manuscripts | CSNTM; Vatican Digital Library; Bodleian/BL digitisations | high-res manuscript images (often IIIF) |
| Museums (open access) | Met, Brooklyn, Cleveland, Rijksmuseum, Smithsonian, BM/Louvre (terms vary) | object images, find data |
| Places / time | Pleiades gazetteer, OpenStreetMap Nominatim (as Stratah nodes already use) | coordinates for the Atlas |

Prefer IIIF endpoints where offered (standard image + metadata API).

## Pipeline
1. **Harvest manifest first** (metadata only): id, URL, licence, date, place, language. Cheap, small, resumable.
2. **Fetch images selectively** (IIIF region/size), store locally, sha256 + dedupe.
3. **Derived layers** (each its own entry): transliteration, translation, our readings; sign OCR/segmentation experiments on the local machine.
4. **Link** to Stratah nodes (place + time) and to claims (`dh-<video>-NN`) as candidate anchors, not as support.
5. **Review** through the normal Stratah branch/PR/reviewer gate before anything is published.

## Role of the local machine (M2, 24 GB RAM, ~186 GB free)
- Overnight polite harvesting on a schedule (launchd), resumable, with a log.
- Hashing, thumbnails, dedupe, metadata normalisation.
- Local vision/OCR experiments on stored images (ai-stack).
- Disk is the constraint: metadata + IIIF links first, images pulled on demand; full image sets to an external drive.

## Phases
- **P0** Identify the wall behind the Joshua/Caleb claim from the extracted claims; list every Egyptian inscription the videos point to.
- **P1** Egyptian slice: TLA + Chicago OI plates + Topographical Bibliography for the sites named in P0. Manifest, then images.
- **P2** Cuneiform (CDLI) and Northwest Semitic slices, driven by the claims (Habiru, Hyksos, Bronze Age Collapse, Gilgamesh/flood).
- **P3** Greek/Latin and NT manuscripts.
- **P4** Reinterpretation workspace: image + attributed competing readings, each with what would change it.

## Open items
- Licence check for each archive in the table (none verified yet).
- Where Stratah should hold this: new schema section (owner-only, needs a SCHEMA proposal per docs/SCHEMA_PROPOSALS.md) or a separate repo that Stratah links to.
- External drive for image storage.
