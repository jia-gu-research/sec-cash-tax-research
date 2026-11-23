# Reproduction guide

The notebooks are designed to run from the repository root (or from the `notebooks/` directory in Jupyter). The large raw SEC ZIP is not included; obtain it as described in [`data/README.md`](../data/README.md).

## Important: use separate Python environments

Stage 1 and Stage 2 were tested with different pinned pandas / NumPy versions. Do **not** install both requirement files into the same environment.

### Stage 1 — data construction and QA

From the repository root:

```bash
python -m venv .venv-stage1
# Windows PowerShell:
.\.venv-stage1\Scripts\Activate.ps1
# macOS/Linux:
source .venv-stage1/bin/activate

python -m pip install -r requirements-stage1.txt
```

Place the SEC file at `data/raw/2026_03_notes.zip`, then launch Jupyter from the repository root:

```bash
jupyter lab
```

Open `notebooks/01_data_construction_QA.ipynb` and run all cells. Stage 1 writes generated tables to `outputs/stage1/`. Its required review evidence is in `evidence/`.

After a successful run, the Stage 1 validator can be run with:

```bash
python src/validate_stage1_outputs.py
```

### Stage 2 — preliminary empirical analysis

Create a **separate** environment:

```bash
python -m venv .venv-stage2
# Windows PowerShell:
.\.venv-stage2\Scripts\Activate.ps1
# macOS/Linux:
source .venv-stage2/bin/activate

python -m pip install -r requirements-stage2.txt
```

The Stage 2 notebook uses the same SEC ZIP and the included frozen Stage 1 bridge at `data/frozen_inputs/stage1_bridge.zip`. Open `notebooks/02_preliminary_empirical_analysis.ipynb` and run all cells. It writes the research sample and model outputs to `outputs/stage2/`, with diagnostics and integrity records in `outputs/stage2_audit/`.

After a successful run:

```bash
python src/validate_stage2_outputs.py
```

### Guardrail tests

With the Stage 2 environment active:

```bash
python -m unittest discover -s tests -v
```

## What is and is not reproduced

The uploaded portfolio archive records a fresh-kernel reproduction dated 2026-11-11: Stage 1 executed 42 code cells with zero errors and 25 CSV outputs matching its frozen snapshot; Stage 2 executed 10 code cells with zero errors and six principal CSV outputs matching its frozen snapshot.

This GitHub-oriented repack changes repository-relative paths and uses a minimal Stage 1 bridge archive. The original Stage 1 outputs and Stage 2 extraction audit tables are retained to make the published audit trail inspectable. The notebooks have **not** been rerun end-to-end after this repack because the 307 MB SEC source ZIP is not bundled. The historical reproduction record is retained as historical evidence, not presented as a new reproduction performed during packaging.

## Offline audit checks (without the SEC raw ZIP)

The included frozen output tables can be audited without re-downloading the 307 MB SEC release. Run `python src/validate_stage1_outputs.py` and `python src/validate_stage2_outputs.py`. The scripts report `NOT_CHECKED_RAW_INPUT_NOT_PRESENT` for the source hash until the original SEC release is downloaded. They do **not** constitute fresh end-to-end re-execution.
