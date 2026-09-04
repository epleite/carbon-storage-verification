# Data provenance

## Starting project list

The March 2026 IEA CCUS Projects Database was used as the fixed project-list snapshot. The raw workbook is not redistributed. The public source page is:

https://www.iea.org/data-and-statistics/data-product/ccus-projects-database

The repository contains only a compact 15-site derived identity table and the IEA project identifiers necessary to document lineage.

## Public evidence

`data/evidence_source_registry.csv` contains 45 site-by-claim records (15 sites × 3 claims), the final evidence score, two retained source URLs where available, and an audit note. These links point to regulatory, operator, public-repository or peer-reviewed sources.

The final score-only matrix is `data/final_evidence_scores.csv`.

## Geological mapping

`data/geology_source_registry.csv` records the public geological sources used to map each sedimentary site to a representative geological setting. `data/recoded_site_results.csv` contains the deterministic geology-only mapping used in the confirmatory cross-axis analysis.

Reactive basalt (A13, Carbfix/Hellisheiði) is explicitly outside the A1-A10 sedimentary seismic family and is flagged as B1.

## Monitoring architecture

`data/monitoring_architecture.csv` records seven documented measurement families: pressure/injection; active seismic; passive/microseismic; well/fibre/logging; geochemical/tracer; deformation/geodesy; and shallow/environmental monitoring. A zero means that the family was not counted under the conservative public-document rule; it does not establish that an operator lacks the technique.

## Evidence cutoff

The public-evidence cutoff used in the study is **2026-08-31 23:59:59 UTC**.

## Author confirmation

On 2026-09-04 the sole author confirmed all 45 final evidence scores after source-level review; no score changes were requested.
