# When and how
Opens: Wednesday, August 26, 2026 at 
_Exported on 09/01/2026 at 21:07:38 GMT-4 from Claude via WayLog_


**User**

When and how
Opens: Wednesday, August 26, 2026 at 12:30 PM ET (start of Week 1 class).
Due: Tuesday, September 1, 2026 by 11:59 PM ET (the evening before Week 2's class).
Late work: accepted up to 24 hours late with a 20% penalty. After
Wednesday, September 2 at 11:59 PM ET it is not accepted and scores zero.
This assignment counts toward your assignment grade (30% of the course
total, spread over ten assignments).
What to submit
Submit two items to Canvas before the deadline:
assignment.ipynb — all cells run, outputs visible.
Your AI Usage Report — see templates/ai-usage-report.md.
AI use is required on every assignment, so this is never optional.
See §7 of the syllabus.
Goal: produce the tokenization report a platform team would actually
read before committing to a text stack — measured vocabulary growth,
measured out-of-vocabulary rates, measured token cost, and a recommendation
you can defend with numbers rather than with adjectives.
Setting
You have joined the data platform team at an online retailer that also runs a
large public community forum. Three projects are waiting on one decision —
how will we tokenize? — and nobody has measured anything yet.
Project A — Lexical search. An inverted index over the forum archive, so
a support agent can find every post containing LC-475 or pericarditis.
Exact terms matter.
Project B — Thread summarization. Send forum threads to a frontier LLM
through an API and store the summary. Finance wants a cost number before
they will sign anything.
Project C — International rollout. The forum is opening to German,
Spanish, Hindi, and Chinese speaking markets on the same paid plan. Product
has asked, in writing, whether "the same plan" means "the same product" for
those users.
The archive stands in for the forum: four newsgroups from the 20 Newsgroups
collection, fetched for you in the notebook. The train split is the
existing archive; the test split is "next month's posts" — text your
vocabulary has never seen.
Everything is set up in assignment.ipynb: the corpus loader, the parallel
multilingual corpus, the stress-test strings, and the rate card. Your job is
the measurement and the judgement.
Tasks
Task 1 — Baseline: how many words are there?
Tokenize the archive (train split) three ways:
str.split() — whitespace only,
a regular expression tokenizer you write yourself,
nltk.word_tokenize — rule-based (Penn Treebank).
For each, report total tokens, distinct types, type/token ratio,
mean tokens per document, and the 15 most frequent types.
Then hunt: find three concrete strings in the corpus where str.split()
produces something no human would call a word — one URL or e-mail address, one
piece of punctuation-glued text, and one of your own choosing. Print the
original string and what each of the three tokenizers does with it.
Deliverable: one comparison table, the three examples with all three
tokenizations shown, and ≤150 words on which differences would change a
search index and which would not.
Task 2 — Vocabulary growth
Walk the archive in document order. Every 25,000 tokens, record the cumulative
token count and the cumulative number of distinct types seen so far, for
three tokenizers: whitespace, bert-base-uncased (WordPiece), and gpt2
(byte-level BPE).
Plot all three curves on log–log axes. For the whitespace curve only, fit
Heaps' law


V=kNβby least squares on 
logV against 
logN, and report 
k and 
β.
Deliverable: one figure with all three curves labelled, the fitted 
k
and 
β, and ≤150 words explaining what the two subword curves do that
the whitespace curve does not, and why that is a design property rather than
an accident.
Task 3 — Out of vocabulary
Part A — word-level. Build closed vocabularies from the archive by keeping
only the 
V most frequent whitespace types, for

V∈{2000,5000,10000,25000,50000,all}. For each, measure
on the held-out split:
OOV token rate — share of held-out token occurrences not in the vocabulary,
OOV type rate — share of held-out distinct types not in the vocabulary.
Part B — subword, on the same held-out split. Count how many [UNK]
tokens bert-base-uncased produces, and how many gpt2 produces. Report the
actual counts, not an impression.
Part C — the stress set. The notebook supplies STRESS_SET, eight short
strings with emoji, Devanagari, Greek, accented Latin, and currency symbols.
For each tokenizer report the token list, the [UNK] count, and whether
decode(encode(s)) == s.
Deliverable: the OOV table (both rates, all six vocabulary sizes), the
Part B counts, the Part C table, and ≤200 words reconciling Part B with Part
C — they do not tell the same story, and the reason is the point.
Task 4 — Reversibility and normalization
Two questions a pipeline has to answer before it processes a single document.
Is tokenization reversible? For six strings of your choice (include at
least one accented word and one emoji), check whether
decode(encode(s)) == s for bert-base-uncased, gpt2, and
tiktoken's cl100k_base. Where it fails, print what came back.
Which Unicode form? "café" can be stored as four code points (NFC) or
five (NFD) and the two are not equal in Python. Report the token count of
each form under bert-base-uncased, gpt2, cl100k_base, and
o200k_base.
Deliverable: a reversibility table, the NFC/NFD token counts, and a
≤100-word normalization policy for the platform: which form you write to
storage, at which point in the pipeline you normalise, and the specific
failure that decision prevents.
Task 5 — Token cost, and who pays it
Part A — the archive. Total cl100k_base and o200k_base tokens for the
whole archive. Using the RATE_CARD in the notebook and stated assumptions
(the notebook proposes one pass per month with output tokens at 15% of input —
change it if you justify the change), compute the monthly API cost of Project
B under each encoding. Show the arithmetic, not just the total.
Part B — the same words in five languages. Load
data/udhr_parallel.json (loaded for you into parallel). Every entry is the
same declaration in English, German, Spanish, Hindi, and Chinese. For each
language and each encoding, compute characters, tokens, tokens per character,
and tokens relative to English. Plot tokens-relative-to-English as a bar
chart, both encodings side by side.
Part C — convert it to money. Fix a support conversation at 2,000 input
tokens and 500 output tokens for an English speaker. Assume the same
conversation in another language scales by that language's token ratio from
Part B. Using RATE_CARD, what does one conversation cost for each language,
and what is the ratio between the most and least expensive?
Deliverable: the cost table, the figure, the per-language conversation
cost, and ≤200 words. Name the group of users who are worst off, quantify
how much worse, and say what changed between cl100k_base and o200k_base.
Task 6 — Recommendation
Write a memo of 400–600 words to the platform lead. It must:
Make one specific recommendation for each of Projects A, B, and C, each
citing at least one number you computed in Tasks 1–5.
Name one thing you would measure before committing that this analysis
does not cover, and say what result would change your recommendation.
Explain one risk created by pairing text tokenized one way with a model
trained on another tokenizer, and how you would prevent it in code.
State plainly what your analysis does not establish. A report that
claims more than its evidence supports is worse than no report.
Deliverable: the memo, in a markdown cell at the end of the notebook.
Prose, not bullets, for at least the first and last paragraphs.
Ground rules
Every number in your report must come from code in your notebook. If a
number appears in prose, the cell that produced it must be visible above it.
Set the seeds the notebook sets and do not change the corpus selection —
your numbers should be reproducible by the grader.
Where a task says "≤150 words", that is a ceiling, not a target. Short and
specific beats long and hedged.
You may use AI assistance freely (§7 of the syllabus). You must be able to
explain every line you submit, and the AI Usage Report is required.
Scope
This is designed as 4–6 hours of work. If you are past eight, something
has gone wrong — post on the discussion board rather than grinding.
Rubric
ComponentPointsTask 1 — Baseline tokenizers. Three tokenizers correctly applied; complete comparison table; three genuine failure cases found in the corpus and shown through all three tokenizers; commentary distinguishes differences that matter for search from ones that do not.12Task 2 — Vocabulary growth. Correct streaming curves for all three tokenizers; readable log–log figure; Heaps' law fitted correctly with 
k and 
β reported; explanation identifies the fixed-vocabulary ceiling as a design choice.16Task 3 — Out of vocabulary. OOV token and type rates correct at all six vocabulary sizes; [UNK] counts on held-out data reported honestly; stress-set table complete; written answer reconciles the corpus result with the stress-set result.18Task 4 — Reversibility and normalization. Round-trip results correct for all three tokenizers; NFC/NFD token counts correct; policy is specific about form, pipeline stage, and the failure it prevents.12Task 5 — Token cost and fairness. Archive token totals correct under both encodings; cost arithmetic shown and assumptions stated; per-language ratios correct; figure readable; per-conversation costs computed; written answer names and quantifies the disadvantaged group and the effect of the newer encoding.22Task 6 — Recommendation. All three projects addressed with numbers cited; a named further measurement with a stated decision rule; a concrete tokenizer/model mismatch risk with a code-level control; an honest statement of the analysis's limits.20AI Usage Report (complete: tool statement, full logs, validation note)0 (gate: −5 to −10 if incomplete, up to −20 if missing)Total100
What separates full marks from most marks
Numbers that reproduce when the grader re-runs the notebook.
Claims that are bounded — "under this rate card and this traffic
assumption" rather than "it costs $X".
Noticing that Task 3 Part B and Part C disagree, and explaining why instead
of picking whichever supports a tidier story.


do this, and explain the reasoning for the architecture. Change only the code and writeup, not the notebook layout. fulfill all requrements

---


**Claude**

Everything needed is cached locally (20 Newsgroups, BERT/GPT-2, punkt, tiktoken encodings). Now I'll prototype the full solution as a script to get real numbers, then port finalized code + numbers into the notebook cells.

---


**Claude**

Now I'll fill in the notebook cells. Starting with Task 1.

---


**Claude**

All six tasks are implemented, the notebook runs top-to-bottom clean (0 errors, 0 `[ TODO ]` messages, both figures render), and every prose cell is within its word ceiling. Cell layout is untouched — 41 cells, same order and types; I only replaced the body of the existing TODO code cells and write-up markdown cells.

## Architecture reasoning

**Workflow.** I first rebuilt every number in a throwaway script against the same cached data (20 Newsgroups `.pkz`, BERT/GPT-2, punkt, tiktoken — all verified offline), then ported the finalized code into the notebook cells, executed the whole notebook, and only then wrote the prose so each figure is copied from the executed cell directly above it. That's what "every number comes from a visible cell" requires, and it means a grader's re-run reproduces the write-ups verbatim.

**Task 1 — `regex_tokenize` = `[0-9A-Za-z]+(?:['’\-][0-9A-Za-z]+)*`.** A token is an alphanumeric run that may *contain* one apostrophe/hyphen between two such runs. So `won't` and `LC-475` stay whole, leading/trailing punctuation drops, and URLs/e-mails shred into pieces — defensible because a word index shouldn't carry `http://a.io/x` as one term. Case is preserved across all three tokenizers so the comparison is fair; folding is a separate normalization step. The failure-case scanner walks `archive` in document order and takes the *first* token matching each pattern, so the three examples (`gajarsky@pilot.njin.net`, `>history?`, `"power/influence"`) are reproducible, not cherry-picked.

**Task 2 — id streams, not surface strings.** For BERT/GPT-2 I count token *ids* (1:1 with vocab, faster to hash, identical distinct-count). `add_special_tokens=False` keeps `[CLS]`/`[SEP]` out of the counts. Heaps' fit is `np.polyfit(log N, log V, 1)` on the whitespace curve only → k = 6.565, β = 0.706; the plot overlays the fit and dotted vocab-size ceilings so the "subword curves flatten, whitespace doesn't" claim is visible.

**Task 3 — two different questions.** Word-level OOV is measured on whitespace types (that's what a lexical index uses); subword `[UNK]` is measured by counting the unk id in the tokenized holdout. Both BERT and GPT-2 give **0 `[UNK]`** on the English holdout, while BERT `[UNK]`s on 3 of 8 stress strings — the reconciliation is that `[UNK]` rate tracks the input's script distribution, not tokenizer quality.

**Task 4 — round-trip via `decode(encode(s))`.** `add_special_tokens=False` on BERT so `[CLS]`/`[SEP]` don't fail equality for the wrong reason; failures print what came back. NFC/NFD counts show byte-BPE pays +1 token for the decomposed form (gpt2 3→4, cl100k/o200k 2→3) while BERT strips the accent either way — which drives the NFC-at-ingest policy.

**Task 5 — arithmetic shown per encoding.** `encode_ordinary_batch` for speed; input/output/cost printed as a line of working, not just a total. `tokens_vs_english` uses each encoding as its own denominator (English = 1.000 by construction). Key result: Hindi is 5.57× English under `cl100k_base`, 1.67× under `o200k_base`.

**Task 6 — one recommendation per project, each with a number**, plus a named pre-commit measurement with a 2.0× decision rule, a tokenizer/model-mismatch risk with a config-level control, and an explicit limits paragraph.

## One thing that needs you

The **AI Usage Report** (`week-01-text-tokenization/ai-usage-report.md`) — I kept your tool statement (Claude Opus 4.6, Gemini Flash 3.6) and session table, fixed the header fields and the `2027`→`2026` date, removed the template instruction blockquotes, and wrote Part 3 (validation) from the checks actually performed. **Part 2 still needs your real Session 1 transcript pasted in** — I left a marked placeholder with the step-by-step outline; Session 2 points at your `Assignment 1-Session 2 Transcript.docx`. The report is a gate item, so paste the Session 1 log before submitting.

---


**User**

> /insights

---


**User**

The user just ran /insights to generate a usage report analyzing their Claude Code sessions.

Here is the full insights data:
{
  "project_areas": {
    "areas": [
      {
        "name": "Satellite Ship & Crane Detection",
        "session_count": 5,
        "description": "Built and iterated on a YOLO-based ship/crane detection pipeline for large port satellite imagery, migrating away from a hacky i-JEPA prototype into a clean single-notebook repo. Claude wired in Roboflow-annotated tile datasets, implemented overlap-and-merge tiling inference, added a Kaggle pretraining section, and debugged annotation-format mismatches, stale data.yaml paths, Unicode path loading, and PIL pixel caps. Several sessions ended with training or verification still in flight."
      },
      {
        "name": "Streamlit Detection App Deployment",
        "session_count": 1,
        "description": "Set up a virtual environment, installed dependencies, and launched a Streamlit ship-detection app. Claude diagnosed a dead hardcoded Wikipedia image URL returning HTTP 400 and rewired the app to load the user's local satellite tiles, leaving it running cleanly."
      },
      {
        "name": "Focus Zones / VoiceOS MCP Cross-Platform Port",
        "session_count": 2,
        "description": "Worked on porting a macOS-only Focus Zones MCP server and Zones VoiceOS integration to Windows while adding new capabilities. Claude traced connection failures to hardcoded /bin/zsh and AppleScript/osascript calls, fixed cross-platform process launching, and added genesis, Chrome, Google Keep, and Gmail/Drive/Calendar/Notion link features. The full Windows port remained incomplete when the session hit its usage limit."
      },
      {
        "name": "Deliverables, Reports & Document Generation",
        "session_count": 2,
        "description": "Packaged an SOTR project into a compliant submission and produced a repo/dashboard evaluation PDF alongside a data cleaning and analysis notebook from CSV inputs. Claude also built a headless-browser script to render a 64-slide HTML deck to PDF and exported the session transcript to text. Deliverable format churned through zip, PDF, and finally editable Word as submission requirements clarified."
      },
      {
        "name": "Python Environment & Dependency Setup",
        "session_count": 1,
        "description": "Diagnosed a missing tokenizers package as an absent virtual environment rather than a package issue. Claude created a .venv and installed the full set of course dependencies, leaving only notebook kernel selection to the user. Related sessions hit slow installs and a Windows Application Control policy that blocked Jupyter execution, requiring validation via standalone scripts."
      }
    ]
  },
  "interaction_style": {
    "narrative": "You operate in **long, sprawling sessions with very few messages** — roughly 77 messages across 132 hours means you hand Claude a substantial objective and then let it run for a long stretch without micromanaging. The tool distribution reinforces this: 322 Bash calls against only 77 of your messages shows you're comfortable delegating entire multi-step workflows (create a venv, install packages, convert a COCO dataset, launch Streamlit, render a 64-slide deck to PDF headlessly) rather than approving each step. You rarely interrupt mid-flight; when things go sideways it's usually because a training run crashed on annotation format or a stale absolute path in `data.yaml`, not because you stopped Claude to redirect.\n\nYour prompts tend to be **goal-shaped rather than spec-shaped**, and that's the biggest source of friction in your data. 'file not found error, fix' with no traceback left Claude guessing and ended a session unresolved. You didn't mention you were on Windows until Claude had already implemented app-closing via macOS `osascript`, and the same pattern repeated when Claude started chasing a macOS zoom-toggle bug you didn't care about — you interrupted to redirect it to the actual blocker (hardcoded `/bin/zsh` breaking the MCP connection). Similarly, your submission deliverable got rebuilt three times (zip → PDF → docx) as requirements surfaced incrementally. **You supply context reactively, when Claude gets it wrong, rather than upfront** — which works because you're a fast, decisive corrector, but it costs you rework cycles.\n\nYour work is clustered around ship/crane detection in Python and TypeScript, plus MCP tooling, and you're notably tolerant of partially-finished states: four sessions ended 'partially achieved' with training still in progress or one last path error outstanding, and you seem fine with that — you pick it up later rather than grinding to closure. You also work in **environmentally hostile conditions** (Google Drive-synced disks, 16–19K pixel images, Windows Application Control blocking Jupyter execution), and you let Claude route around them instead of fixing the environment. Your best sessions are the debugging-heavy ones — fake I-JEPA weights, Unicode path loading, PIL's pixel cap, a dead Wikipedia image URL — where you hand over a symptom ('it should actually work on full port images') and Claude gets to excavate.",
    "key_pattern": "You hand off big, loosely-specified goals and let Claude run for hours unsupervised, then course-correct sharply once it heads the wrong direction — trading upfront specification for fast reactive steering."
  },
  "what_works": {
    "intro": "Across 11 sessions spanning computer vision pipelines, MCP tooling, and coursework deliverables, you consistently pushed Claude past scaffolding into real debugging and working software.",
    "impressive_workflows": [
      {
        "title": "Iterative ship detection pipeline",
        "description": "You didn't accept a demo that only looked like it worked — you pushed until the ship-detection app actually ran on full port imagery. That persistence surfaced genuinely deep bugs (fake I-JEPA weights, Unicode path loading failures, PIL's pixel cap) and drove a full rewrite of the detection pipeline, plus overlap-and-merge tiling inference and a real training run."
      },
      {
        "title": "Environment-first debugging instincts",
        "description": "When something broke, you went straight to Claude with the environment rather than guessing. Missing `tokenizers` became a clean `.venv` with all course packages; a Streamlit crash became a diagnosed dead image URL rewired to your local satellite tiles; a Windows Application Control block on Jupyter became validation via standalone scripts. You treat environment friction as a solvable problem, not a dead end."
      },
      {
        "title": "Cross-platform MCP porting",
        "description": "You took a macOS-only Focus Zones MCP and had Claude trace why it wouldn't connect on Windows, landing on hardcoded `/bin/zsh` in the launcher. Notably, when Claude wandered into a macOS zoom bug you didn't care about, you interrupted and redirected to the actual blocker — then kept going and added genesis, Chrome, and Google Keep features on top of the fixed foundation."
      }
    ]
  },
  "friction_analysis": {
    "intro": "Across 11 sessions you got substantial help with ML notebooks and MCP tooling, but you repeatedly lost time to unstated environment context, vague bug reports, and long-running verification that never closed the loop.",
    "categories": [
      {
        "category": "Unstated platform and environment context",
        "description": "You often revealed key environment facts (Windows, Google Drive-synced disk, application control policy) only after Claude had already built something incompatible. Stating your OS, shell, and disk setup at the start of a session would prevent whole implementations from being thrown away.",
        "examples": [
          "Claude implemented the Zones app-closing feature with macOS-only osascript/AppleScript before you mentioned you're on Windows, forcing a rethink — then the session hit the usage limit before the port finished.",
          "Claude started fixing a macOS zoom-toggle bug you didn't care about; you had to interrupt with the real blocker, a hardcoded /bin/zsh preventing the MCP from connecting on Windows."
        ]
      },
      {
        "category": "Underspecified bug reports and requirements",
        "description": "Several requests arrived as short fragments without tracebacks, file paths, or final format requirements, so Claude had to guess or investigate blind. Pasting the actual error output and stating the target deliverable up front would collapse multiple rounds into one.",
        "examples": [
          "Your 'file not found error, fix' had no traceback, so Claude investigated, then had to ask for clarification — the bug was still unresolved when the session ended.",
          "The SOTR submission format changed from zip to single PDF to editable docx across the session, requiring the deliverable to be rebuilt twice."
        ]
      },
      {
        "category": "Long-running work left unverified",
        "description": "Multiple sessions ended with training runs, verification scripts, or notebook executions still in flight, so you never confirmed whether the fix actually worked. Running the slow verification yourself and reporting back, or scoping work to something that finishes inside a session, would close these loops.",
        "examples": [
          "Smoke tests and venv import checks crawled on the Google Drive-synced disk with 16–19K px images, and the final verification run was stopped before completing.",
          "The Roboflow tiling comparison notebook was edited and a new section added, but verification never completed and you never confirmed the result — the outcome is unclear from the transcript."
        ]
      }
    ]
  },
  "suggestions": {
    "claude_md_additions": [
      {
        "addition": "## Environment\n- Primary dev machine is **Windows** (PowerShell). Never generate macOS-only code (osascript/AppleScript, /bin/zsh, `open -a`) unless explicitly asked. Use cross-platform launchers (`subprocess` with `shell=False`, `os.startfile` on Windows, platform checks via `sys.platform`).\n- Jupyter kernel execution is blocked by Windows Application Control. Validate notebook logic by running an equivalent standalone `.py` script instead of executing cells.",
        "why": "Two sessions were derailed by macOS-only assumptions (hardcoded /bin/zsh, osascript) and one session lost time when Jupyter execution was blocked by policy.",
        "prompt_scaffold": "Add near the top of CLAUDE.md under a new '## Environment' section so it is read before any tooling decisions."
      },
      {
        "addition": "## Python Projects\n- Always work inside a project-local `.venv`. If `.venv` is missing, create it and install from requirements before running anything.\n- Repo lives on a Google Drive-synced disk: file I/O and imports are slow. Avoid long background smoke tests; prefer a small, fast subset (few images, 1 epoch) for verification and report timing expectations up front.",
        "why": "Missing/implicit virtualenvs caused a full debugging session, and slow Drive-synced I/O caused verification runs to be abandoned mid-session in at least two sessions.",
        "prompt_scaffold": "Add as a '## Python Projects' section after Environment."
      },
      {
        "addition": "## Datasets & Vision Work\n- All dataset paths in `data.yaml` and notebooks must be **relative to the repo root** — never absolute paths.\n- Before any YOLO/detection training run, validate the annotation set: confirm all labels are the same format (bbox vs polygon) and that image/label counts match. Report mismatches instead of starting training.\n- Watch for large satellite images (16k-19k px): set `PIL.Image.MAX_IMAGE_PIXELS` and never load a full scene into memory without tiling.",
        "why": "Training crashed repeatedly across multiple sessions from mixed box/polygon annotations, stale absolute paths in data.yaml, and PIL's pixel cap on large port imagery.",
        "prompt_scaffold": "Add as a '## Datasets & Vision Work' section; keep the bullets verbatim so Claude checks them pre-training."
      },
      {
        "addition": "## Working Style\n- When I report a bug with only a short description (e.g. 'file not found error, fix'), ask me for the full traceback and the exact command I ran before investigating.\n- Confirm the target deliverable format (zip / PDF / .docx / notebook) before producing it.\n- Do not fix unrelated bugs you notice along the way — list them and keep working on the stated blocker.",
        "why": "A vague 'file not found' report burned a session, a deliverable was rebuilt three times due to format churn, and Claude once started fixing a macOS zoom bug the user didn't care about.",
        "prompt_scaffold": "Add as a '## Working Style' section at the end of CLAUDE.md."
      }
    ],
    "features_to_try": [
      {
        "feature": "Custom Skills",
        "one_liner": "Reusable markdown prompts you invoke with a single slash command.",
        "why_for_you": "You repeatedly do the same ship-detection setup: create venv, verify dataset paths, check annotation format, run a short training smoke test. A `/train-check` and `/setup-env` skill would remove the debug rounds that ended three of your sessions unresolved.",
        "example_code": "# .claude/skills/train-check/SKILL.md\n---\nname: train-check\ndescription: Pre-flight validation before any YOLO training run\n---\nBefore training:\n1. Confirm `.venv` exists and is active; create + install requirements if not.\n2. Print `data.yaml` and verify all paths are RELATIVE to repo root. Fix any absolute paths.\n3. Count images vs label files in train/ and val/; report mismatches.\n4. Scan 20 random label files and report whether they are bbox (5 cols) or polygon (>5 cols). Abort if mixed.\n5. Set PIL.Image.MAX_IMAGE_PIXELS = None in the entry script.\n6. Run 1 epoch on a 10-image subset and report wall-clock time before launching the full run."
      },
      {
        "feature": "Hooks",
        "one_liner": "Shell commands that auto-run at Claude lifecycle events.",
        "why_for_you": "You launched Python/Streamlit outside a venv and hit missing-package errors more than once. A PreToolUse hook that checks for an active `.venv` on every Bash python call would catch this before Claude wastes turns diagnosing it.",
        "example_code": "// .claude/settings.json\n{\n  \"hooks\": {\n    \"PreToolUse\": [\n      {\n        \"matcher\": \"Bash\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"if [ -d .venv ] && [ -z \\\"$VIRTUAL_ENV\\\" ]; then echo 'WARNING: .venv exists but is not activated. Use .venv\\\\\\\\Scripts\\\\\\\\python.exe'; fi\"\n          }\n        ]\n      }\n    ]\n  }\n}"
      },
      {
        "feature": "Task Agents",
        "one_liner": "Claude spawns focused subagents to explore code or run work in parallel.",
        "why_for_you": "Several sessions ended with 'verification never completed' or hit the usage limit mid-port. Delegating the slow exploration (finding every hardcoded macOS call, or mapping dataset path references across notebook + data.yaml + README) to an agent keeps your main context free for the actual fix.",
        "example_code": "Use a subagent to search this repo for every macOS-only assumption — osascript, AppleScript, /bin/zsh, `open -a`, ~/Library paths — and return a file:line list with a suggested Windows equivalent for each. Don't edit anything yet."
      }
    ],
    "usage_patterns": [
      {
        "title": "Front-load the environment constraints",
        "suggestion": "You lose whole sessions to Windows-vs-macOS and venv surprises that Claude only discovers halfway through. State the platform contract in the first message.",
        "detail": "In the Focus Zones and Zones VoiceOS sessions, Claude wrote AppleScript and hardcoded /bin/zsh before learning you're on Windows — one of those sessions then hit the usage limit before the port finished. The same class of surprise hit you with the missing `.venv` and the blocked Jupyter kernel. Once these live in CLAUDE.md you stop paying for the discovery each time, but repeating them in the opening prompt of a new repo is still cheap insurance.",
        "copyable_prompt": "Context before you start: I'm on Windows using PowerShell, Python runs from a local .venv, and Jupyter cell execution is blocked by Application Control (validate via standalone .py scripts). Do not write any macOS-only code. Confirm you understand these constraints, then proceed with: <task>"
      },
      {
        "title": "Give tracebacks, not symptoms",
        "suggestion": "Your shortest bug reports produced your worst outcomes. Paste the full error and the exact command every time.",
        "detail": "The 'file not found error, fix' message forced Claude into blind investigation and the bug was still unresolved at session end. Contrast that with the Streamlit session where the HTTP 400 was visible in the crash output — Claude diagnosed the dead Wikipedia URL and rewired to local tiles in one pass. With 322 Bash calls across 11 sessions, most of that tool volume is Claude re-deriving state you already had on screen.",
        "copyable_prompt": "Here's the failure. Command I ran:\n```\n<command>\n```\nFull traceback:\n```\n<paste>\n```\nDiagnose the root cause first and tell me what it is before changing any code."
      },
      {
        "title": "Checkpoint long training and verification runs",
        "suggestion": "Four of eleven sessions ended 'partially achieved' with work still in flight. Break long-running steps out of the session.",
        "detail": "Your ship-detection sessions repeatedly ended with training or smoke tests still running, or stopped without completing, on a Google Drive-synced disk with 16-19K px images. Instead of running these inside the conversation, have Claude write a standalone script plus a resume-from-checkpoint path, launch it detached, and log to a file you can hand back next session. That converts a dead-end session into a clean handoff.",
        "copyable_prompt": "Don't run the training in this session. Instead: write `scripts/train.py` that takes a config, writes progress to `logs/train.log`, and saves a checkpoint every epoch so it can resume. Then give me the exact PowerShell command to launch it detached, and a one-paragraph summary of state I can paste into our next session."
      },
      {
        "title": "Lock the deliverable format before generating it",
        "suggestion": "You rebuilt a submission three times (zip → PDF → docx). Have Claude confirm the output contract up front.",
        "detail": "Across your SOTR submission, the dashboard evaluation PDF, and the 64-slide HTML→PDF export, output format was a recurring source of rework. These are high-effort artifacts where regeneration is expensive. Asking Claude to restate the exact filename, extension, page count, and editability requirement before it starts turns a two-redo session into one pass — and this pairs well with a `/deliverable` custom skill once the format is stable.",
        "copyable_prompt": "Before you build anything, restate back to me: the exact output filename and extension, whether it must be editable, page/slide count limits, and any required sections. Wait for my confirmation, then produce it."
      }
    ]
  },
  "on_the_horizon": {
    "intro": "Your work has moved from asking Claude to make single edits toward orchestrating whole deliverables — notebooks, detection pipelines, cross-platform MCP servers — and the next step is letting agents run those loops end-to-end while you review outcomes rather than intermediate steps.",
    "opportunities": [
      {
        "title": "Autonomous train-evaluate-fix loops for detection",
        "whats_possible": "Your ship/crane detection sessions kept stalling on annotation-format mismatches, stale data.yaml paths, and training runs that never finished before the session ended. Instead of babysitting each crash, you could hand Claude a single objective — 'get mAP@50 above X on the held-out port tiles' — and let it validate the dataset, fix path and polygon/box inconsistencies, launch training in the background, read the metrics, and iterate through multiple configurations autonomously. The session ends with a results table and a working checkpoint, not a half-finished run.",
        "how_to_try": "Use Bash with background/nohup execution so training survives long steps, plus a dataset-validation script Claude writes first and reruns as a gate before every training attempt.",
        "copyable_prompt": "I want you to autonomously get my YOLO ship/crane detector to a working state. Do this without stopping to ask me between steps unless you hit something genuinely ambiguous.\n\n1. First, write scripts/validate_dataset.py that checks: every image has a label, all labels use a consistent format (flag any mixed box/polygon annotations), all paths in data.yaml resolve as RELATIVE paths from the repo root, and class IDs are in range. Print a clear PASS/FAIL report.\n2. Run it. Fix every FAIL — including converting any polygon annotations to boxes or vice versa, and rewriting data.yaml to use relative paths only. Re-run until PASS.\n3. Then launch a short training run (small epoch count) in the background with nohup, writing logs to runs/train.log. Poll the log rather than blocking.\n4. Read the resulting metrics. If mAP@50 is below 0.5, diagnose why (class imbalance? tile size? augmentation? learning rate?), change ONE thing, and retrain. Do up to 3 iterations.\n5. Finally, run inference on 3 full-resolution port images using the overlap+merge tiling path and save annotated outputs to outputs/.\n\nEnd with a markdown table: iteration, config change, mAP@50, and your recommendation for what to try next. Note the images are very large (16-19K px) and on a slow synced disk, so cache aggressively and avoid re-reading files unnecessarily."
      },
      {
        "title": "Parallel agents for cross-platform porting",
        "whats_possible": "Two of your sessions burned time because Claude wrote macOS-only code (osascript, /bin/zsh) before learning you're on Windows, and one hit the usage limit mid-port. You could instead have parallel subagents sweep the entire codebase at once: one auditing every platform-specific call site, one writing an abstraction layer, one building a smoke-test harness that proves the MCP server actually connects on Windows. The port becomes a single reviewed diff instead of a multi-session archaeology dig.",
        "how_to_try": "Use the Task tool to spawn concurrent subagents over separate concerns, and have Grep drive the initial platform-specific-call inventory so nothing is missed.",
        "copyable_prompt": "I am on Windows. My Focus Zones / Zones VoiceOS MCP servers were written assuming macOS and I need them fully cross-platform. Do not fix anything unrelated to this goal.\n\nLaunch parallel subagents:\n- Agent A: grep the whole codebase for macOS-only assumptions — /bin/zsh, /bin/bash hardcoding, osascript, AppleScript, 'open -a', ~/Library paths, mdfind, pbcopy, and any hardcoded POSIX path separators. Produce an inventory file PORT_AUDIT.md listing file, line, what it does, and the Windows equivalent.\n- Agent B: design and write a platform.py (or platform.ts) abstraction module exposing launch_app(), close_app(), open_url(), get_config_dir(), and get_shell() with working macOS AND Windows implementations. On Windows use PowerShell / Start-Process / taskkill.\n- Agent C: write tests/test_platform_smoke.py that verifies the MCP server actually starts and responds to a tools/list request on the current OS, and that each platform function is callable without exception.\n\nWhen all three finish, integrate: replace every call site from the audit with the abstraction layer, then run the smoke tests on Windows and iterate until green. Also check for and report any duplicate sibling project folders that could cause me to edit the wrong copy. Give me a final summary of what changed and what still needs manual verification."
      },
      {
        "title": "Self-verifying deliverable pipelines with browser checks",
        "whats_possible": "You repeatedly produce artifacts for other people — a 64-slide PDF, a docx submission, a 2-page evaluation, a running Streamlit app — and repeatedly hit format churn, blocked Jupyter execution, and dead hardcoded URLs discovered only at runtime. A single build pipeline could regenerate every deliverable from source, then verify each one actually works: open the PDF and count pages, load the Streamlit app in a browser and screenshot it, HEAD-check every external URL before it can crash you. You'd get a green/red dashboard instead of finding out at demo time.",
        "how_to_try": "Combine a Bash-driven build script with the Claude Browser MCP for visual verification, so rendering and runtime failures are caught by the agent rather than by you.",
        "copyable_prompt": "Build me a single self-verifying deliverables pipeline for this project. Create build.py (or a Makefile) with a target per artifact and a verification step for each.\n\nArtifacts to build from source:\n- The HTML slide deck rendered to PDF via headless browser, with UI chrome stripped.\n- The analysis notebook exported to both a runnable standalone .py and an executed HTML/PDF report. Important: Jupyter kernel execution is blocked on my machine by Windows Application Control, so execute via the standalone script path, not nbconvert --execute.\n- The evaluation writeup as both PDF and an editable .docx (requirements have changed on me before, so generate both every time).\n\nThen add a verify step that must pass before the build is considered green:\n1. For each generated PDF, open it and assert a nonzero, expected page count.\n2. Crawl the source for every hardcoded external URL and HEAD-request each one; fail loudly with the file and line if any returns non-200. I previously had a Wikipedia image URL return 400 and crash an app at runtime.\n3. Launch the Streamlit ship-detection app, then use the browser tool to load it, screenshot it, and confirm it renders without an exception traceback on the page. Kill the server afterward.\n\nRun the full pipeline now, fix whatever fails, and give me a PASS/FAIL table of every artifact with its output path."
      }
    ]
  },
  "fun_ending": {
    "headline": "Claude confidently built a Mac-only 'close everything' feature with AppleScript — twice — before the user finally mentioned they were on Windows",
    "detail": "During the Focus Zones / Zones VoiceOS MCP sessions, Claude hardcoded /bin/zsh and osascript into the tooling, then got interrupted mid-fix on a macOS zoom bug the user didn't even care about. The real blocker: the MCP wouldn't connect on Windows at all. The session hit its usage limit before the port was finished."
  },
  "at_a_glance": {
    "whats_working": "You use Claude as a genuine debugging partner rather than a code generator — when something breaks, you bring it the whole environment and let it trace root causes, which surfaced real bugs like fake I-JEPA weights, Unicode path failures, and PIL's pixel cap rather than papering over them. You also don't accept demos that merely look like they work; you pushed the ship-detection pipeline until it ran on full port imagery. And you steer well mid-session, interrupting Claude when it drifted into a macOS bug you didn't care about and redirecting to the actual blocker.",
    "whats_hindering": "On Claude's side: it sometimes committed to an approach before checking constraints — writing macOS-only AppleScript for a Windows user, miscalibrating a similarity threshold, and leaving typos in throwaway test scripts that cost extra rounds. On your side: platform and disk details (Windows, Drive-synced storage, application control policies) usually surfaced only after Claude had already built something incompatible, and your shortest bug reports — 'file not found error, fix' with no traceback — reliably produced the worst outcomes. Several sessions also ended with training or verification still running, so you never confirmed the fix landed.",
    "quick_wins": "Create a Custom Skill that encodes your environment contract — OS, shell, venv location, disk quirks — and invoke it at the start of any session touching a new repo, so Claude never guesses wrong again. For the long training and verification runs, use Task Agents to spawn a focused subagent that launches the run and reports metrics back, keeping your main thread free instead of blocking on a smoke test that never finishes. And before generating any deliverable, have Claude state the output contract (format, page count, editability) back to you in one line.",
    "ambitious_workflows": "Start structuring detection work so it can run unattended: instead of debugging each crash yourself, give Claude a measurable objective like 'get mAP@50 above X on held-out port tiles' and let it validate the dataset, reconcile annotation formats and paths, train, read metrics, and iterate across configurations — ending with a results table rather than a half-finished run. For cross-platform work, expect to hand off the entire port at once with parallel agents auditing platform-specific calls, writing the abstraction layer, and building a smoke test that proves the MCP actually connects on Windows. Getting your projects into a state where success is machine-checkable — a metric, a passing test, a screenshot of the running app — is the main prep work that pays off as models improve."
  }
}

Report URL: file://C:\Users\owner\.claude\usage-data\report-2026-09-01-210452.html
HTML file: C:\Users\owner\.claude\usage-data\report-2026-09-01-210452.html
Facets directory: C:\Users\owner\.claude\usage-data\facets

At-a-glance summary (for your context only — the user has not seen any output yet):
# Claude Code Insights

21 sessions total · 11 analyzed · 77 messages · 132h · 0 commits
2026-08-07 to 2026-09-01

## At a Glance

**What's working:** You use Claude as a genuine debugging partner rather than a code generator — when something breaks, you bring it the whole environment and let it trace root causes, which surfaced real bugs like fake I-JEPA weights, Unicode path failures, and PIL's pixel cap rather than papering over them. You also don't accept demos that merely look like they work; you pushed the ship-detection pipeline until it ran on full port imagery. And you steer well mid-session, interrupting Claude when it drifted into a macOS bug you didn't care about and redirecting to the actual blocker. See _Impressive Things You Did_.

**What's hindering you:** On Claude's side: it sometimes committed to an approach before checking constraints — writing macOS-only AppleScript for a Windows user, miscalibrating a similarity threshold, and leaving typos in throwaway test scripts that cost extra rounds. On your side: platform and disk details (Windows, Drive-synced storage, application control policies) usually surfaced only after Claude had already built something incompatible, and your shortest bug reports — 'file not found error, fix' with no traceback — reliably produced the worst outcomes. Several sessions also ended with training or verification still running, so you never confirmed the fix landed. See _Where Things Go Wrong_.

**Quick wins to try:** Create a Custom Skill that encodes your environment contract — OS, shell, venv location, disk quirks — and invoke it at the start of any session touching a new repo, so Claude never guesses wrong again. For the long training and verification runs, use Task Agents to spawn a focused subagent that launches the run and reports metrics back, keeping your main thread free instead of blocking on a smoke test that never finishes. And before generating any deliverable, have Claude state the output contract (format, page count, editability) back to you in one line. See _Features to Try_.

**Ambitious workflows:** Start structuring detection work so it can run unattended: instead of debugging each crash yourself, give Claude a measurable objective like 'get mAP@50 above X on held-out port tiles' and let it validate the dataset, reconcile annotation formats and paths, train, read metrics, and iterate across configurations — ending with a results table rather than a half-finished run. For cross-platform work, expect to hand off the entire port at once with parallel agents auditing platform-specific calls, writing the abstraction layer, and building a smoke test that proves the MCP actually connects on Windows. Getting your projects into a state where success is machine-checkable — a metric, a passing test, a screenshot of the running app — is the main prep work that pays off as models improve. See _On the Horizon_.

Respond with exactly the following, and nothing else. Do not add, omit, or reword any line:

Your shareable insights report is ready:
file://C:\Users\owner\.claude\usage-data\report-2026-09-01-210452.html

Want to dig into any section or try one of the suggestions?

---


**Claude**

Your shareable insights report is ready:
file://C:\Users\owner\.claude\usage-data\report-2026-09-01-210452.html

Want to dig into any section or try one of the suggestions?

---
