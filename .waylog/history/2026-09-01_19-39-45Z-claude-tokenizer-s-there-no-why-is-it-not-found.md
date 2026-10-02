# tokenizer's there no? why is it not found?
_Exported on 09/01/2026 at 21:07:38 GMT-4 from Claude via WayLog_


**User**

tokenizer's there no? why is it not found?

---


**Claude**

Short answer: the package **is** declared for this course, but it was never installed into an environment your notebook can see.

**What's going on**

- `tokenizers` is listed in [pyproject.toml](pyproject.toml) (under "Tokenization (Week 1)"), and it's pinned in [uv.lock](uv.lock).
- But this repo installs everything into a project virtualenv at `./.venv`, created by `uv sync` (step 2 of [setup.sh](setup.sh)). That folder **does not exist yet** — setup hasn't been run.
- So your notebook kernel is falling back to a system Python (`C:\Python314\...` / the Windows Store `python3`), which has none of the course packages — not `tokenizers`, not `transformers`, not even `torch`. Cell `c024` is just the first one that happens to hit a missing import in your run. The outputs you see saved in the notebook are the instructor's (note `torch 2.11.0 (mps)` — that's a Mac).

**Fix**

1. Create the environment (from the repo root, in Git Bash):
   ```bash
   ./setup.sh
   ```
   or just the Python part:
   ```bash
   uv sync
   ```
   `uv` (0.12.5) is already installed. First run pulls torch + HF stack, ~3–5 min.

2. In VS Code, open [practice.ipynb](week-01-text-tokenization/data/practice.ipynb), click the kernel picker (top right), and select the interpreter at **`./.venv`** (`.venv\Scripts\python.exe`). Re-run from the top.

Want me to run `uv sync` now?

---


**User**

yes

---


**Claude**

Done. `.venv` created (CPython 3.12.14) with all 246 course packages, including `tokenizers==0.22.2`, `transformers==5.7.0`, `torch==2.11.0+cpu`. Imports verified.

**One thing left — point the notebook at it:**

In VS Code, open [practice.ipynb](week-01-text-tokenization/data/practice.ipynb) → kernel picker (top-right) → **Select Another Kernel → Python Environments** → pick `.venv (Python 3.12.14)` (`.venv\Scripts\python.exe`). Then run from the top; cell `c024` will import cleanly now.

Notes:
- torch is the CPU wheel — expected on Windows without the CUDA index. Fine for Week 1; the notebook's `device` selector will just say `cpu` instead of the `mps` in the instructor's saved output.
- You still haven't run setup.sh steps 3–4 (spaCy `en_core_web_sm` + NLTK data). Week 1 doesn't need them, but Week 2 will: `./setup.sh` again, or the two `uv run python -m ...` download lines from [setup.sh](setup.sh).

---
