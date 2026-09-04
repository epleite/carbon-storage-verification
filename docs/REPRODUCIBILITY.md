# Reproducibility guide

## Environment

Reference package versions are pinned in `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Structural tests

```bash
python -m unittest discover -s tests -v
```

The tests check the 15-site/45-record dimensions, final E2+ counts, the reactive-basalt boundary, and the minimum ambiguity-bound conclusions.

## Full derived reproduction

```bash
python code/run_all.py
```

This command:

1. recomputes all four independent evidence-ambiguity combinations;
2. recomputes the small-sample diagnostic models;
3. regenerates publication figures from frozen derived inputs;
4. verifies the recomputed ambiguity table against the frozen release table;
5. verifies matching model diagnostics at numerical tolerance.

All outputs are written to `reproduced/`.

## Individual commands

```bash
python code/reproduce_ambiguity.py
python code/reproduce_models.py
python code/reproduce_figures.py
```

## What is not regenerated

The repository does not reconstruct the March 2026 IEA workbook or crawl third-party websites. Source discovery is represented by public URLs and frozen author-generated annotations. This avoids both licensing ambiguity and dependence on mutable external webpages during numerical reproduction.
