# Carbon-storage verification: reproducibility package

Reproducibility repository for the manuscript:

> **Seismic detectability and public verification diverge across operational geological carbon storage projects**

Author: **Emilson Pereira Leite**  
Department of Geology and Natural Resources, Institute of Geosciences, University of Campinas (UNICAMP), Brazil  
ORCID: 0000-0003-1691-6243  
Contact: emilson@unicamp.br

## Scientific result in one paragraph

The study separates three quantities that are often conflated in geological CO2 storage: storage geology/capacity, the detectability of a specified measurement, and the public evidence actually available to verify subsurface behaviour. Ten representative sedimentary settings were screened with a Monte Carlo seismic experiment, while fifteen operational storage sites were audited for public quantitative evidence of injected mass, observed subsurface behaviour relative to expectations, and containment. After source-level ambiguity was propagated explicitly, quantitative mass accounting remained more common than the two subsurface-evidence classes, and generic seismic detectability did not provide a simple ordering of public conformance or containment evidence among longer-running sedimentary sites. Reactive basalt is treated as a separate tracer-geochemical measurement family rather than forced into the sedimentary seismic classification.

## Repository layout

- `data/site_identity.csv` — 15-site derived identity table and IEA project identifiers;
- `data/final_evidence_scores.csv` — final site-level K2/K3/K4 evidence scores;
- `data/evidence_source_registry.csv` — 45 site-by-claim records linked to retained public source URLs;
- `data/evidence_ambiguity_bounds.csv` — seven historical scoring disagreements and current defensible bounds;
- `data/ambiguity_sensitivity_results.csv` — four independent combinations of the two current E1/E2 ambiguity bounds;
- `data/archetype_physics.csv` — frozen A1-A10 generic seismic-detectability probabilities;
- `data/recoded_site_results.csv` — geology-only site mapping and site-level seismic scores;
- `data/monitoring_architecture.csv` — documented measurement families and monitoring breadth;
- `data/geology_source_registry.csv` — public geological sources supporting site-to-setting mapping;
- `data/exact_robustness_tests.csv` — exact/randomization robustness results;
- `data/small_sample_model_diagnostics.csv` — supplementary leave-one-site-out diagnostics;
- `code/reproduce_ambiguity.py` — recomputes ambiguity-bound results;
- `code/reproduce_models.py` — recomputes supplementary small-sample diagnostic models;
- `code/reproduce_figures.py` — regenerates all manuscript and supplementary figures into `reproduced/figures/`;
- `code/run_all.py` — one-command reproduction and numerical verification;
- `tests/test_release.py` — structural/scientific smoke tests;
- `docs/` — evidence rubric, data provenance, reproducibility notes, AI-assistance disclosure, final author sign-off, and claim-to-file index.

## Quick start

The frozen submission environment used Python 3.13 with the package versions in `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python code/run_all.py
```

On Windows, activate the environment using `.venv\\Scripts\\activate`.

`code/run_all.py` writes regenerated tables and figures to `reproduced/`; frozen input tables are never overwritten.

## Evidence classification

The manuscript uses three claim-specific evidence axes:

- **K2 — mass accounting:** observed injected/stored CO2 with an explicit period and accounting boundary;
- **K3 — conformance:** observed quantitative subsurface behaviour compared with a baseline, model or forecast;
- **K4 — containment:** observed quantitative evidence addressing a migration pathway or subsurface irregularity.

Evidence depth is E0-E4. The main threshold is E2 or higher. K3/K4 require uncertainty, a detection limit or a sensitivity statement appropriate to the claim. Full definitions are in `docs/EVIDENCE_RUBRIC.md`.

All 45 final site-by-claim classifications were source-checked and confirmed by the sole author on **2026-09-04**, without score changes. The earlier isolated AI-assisted scoring passes are retained only as workflow provenance and are not interpreted as independent human inter-rater validation. Classification uncertainty is represented directly through source-based defensible bounds.

## Data provenance and third-party data

The March 2026 **IEA CCUS Projects Database** was used only as the fixed starting project list. The raw IEA workbook is **not redistributed** in this repository. Its source page is:

https://www.iea.org/data-and-statistics/data-product/ccus-projects-database

Only compact derived site identifiers and author-generated classifications are included here. Primary evidence remains at the public regulatory, operator, repository and peer-reviewed URLs listed in the source registries. See `docs/DATA_PROVENANCE.md` and `DATA_LICENSE.md`.

## Scope and limitations

- The cohort contains 15 operational storage sites and is not a random sample of all current or future projects.
- Limited public evidence does not imply physical monitoring failure, leakage, or non-containment.
- The quantitative physics screen is a generic seismic amplitude/travel-time experiment, not a complete multimethod monitoring model.
- Capacity-weighted global inference is intentionally not released because the pre-specified megaproject leave-one-out stability check failed.
- The small-sample logistic models are supplementary diagnostics and must not be interpreted as population predictive-performance estimates.

## AI-assisted workflow

OpenAI ChatGPT was used for structured search assistance, preliminary source triage/classification under author-defined rules, code support, and language editing. Scientific criteria, retained-source review, final evidence classifications, ambiguity bounds and manuscript conclusions remain the responsibility of the author. See `docs/AI_ASSISTANCE.md`.

## Licences

- Original code in this repository: **MIT License** (`LICENSE-CODE`).
- Author-generated annotations and derived tables: **CC BY 4.0**, subject to third-party source rights and the restrictions described in `DATA_LICENSE.md`.
- Third-party source materials and the IEA database are **not relicensed** by this repository.

## Citation and archival release

Version **1.0.0** is the submission release. Citation metadata are provided in `CITATION.cff` and `.zenodo.json`.

GitHub repository:

https://github.com/epleite/carbon-storage-verification

Create a GitHub release/tag named `v1.0.0`, archive that exact release in Zenodo, and use the resulting DOI in the manuscript's Data and Code Availability statements.
