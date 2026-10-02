# AI Usage Report

**Course:** ISM 6564 — Text Analytics, Fall 2026
**Student:** Jitastic (nltrinh1102@gmail.com)
**Assignment:** Assignment 1 — A Tokenization Report (Week 1)
**Date submitted:** 2026-09-01

## Part 1 — AI tool statement

| Tool and model version | Where I used it | What I asked it to do |
|---|---|---|
| Claude Opus 4.6 (VS Code extension) | Throughout (all six tasks) | Draft the `regex_tokenize` pattern and the three comparison streams; the streaming Heaps'-law growth loop; the OOV and `[UNK]` measurement; the stress-set, round-trip, and NFC/NFD tables; the tiktoken cost arithmetic; the Task 2c and 5c plots; and first drafts of the write-ups and the Task 6 memo. |
| Gemini Flash 3.6 | Beginning — workflow planning | Sketch the order of work: prototype the numbers in a scratch script first, execute the notebook, then write prose that cites only executed cell outputs. |
| Gemini Pro 3.1 Extended|Cecking code|| I asked it to identify potentital errors and edge cases |

No inline-completion tools (e.g. Copilot) were used; there are no untranscribed completions.

---

## Part 2 — Chat history / log

**Sessions included:**

| # | Tool | Date | Roughly what it covered |
|---:|---|---|---|
| 1 | Claude Opus 4.6 | 2026-09-01 | All code generation for Tasks 1–6; notebook execution; write-up drafts. |
| 2 | Gemini Flash 3.6 | 2026-09-01 | Workflow / order of work. |

> The complete, unedited transcripts are pasted below. Session 2's full
> transcript is also attached as `Assignment 1-Session 2 Transcript.docx`.

### Session 1 — Claude Opus 4.6 (code generation)

Transcript is attached at Session 1.md
### Session 2 — Gemini Flash 3.6 (workflow)

Full transcript attached as `Assignment 1-Session 2 Transcript.docx`.

Transcript is attached at Session 1.md
### Session 2 — Gemini Flash 3.6 (workflow)

Full transcript attached as `Assignment 1-Session 3 Transcript.docx`.

---

## Part 3 — Validation steps


**How I validated the output:**
>I double checked the notebook with Gemini Pro 3.1 by asking for potential errors and edge cases. 
> 
**Something the AI got wrong that I corrected:**

>The solution is reliant on ASCII and is not effective for non-Latin languages(Chinese, Korean,...) I replaced the ASCII range with a Unicode-Aware word character class. 


## Declaration

By submitting this report I confirm that:

- [x] It names every AI tool I used, and does not understate that use.
- [x] The transcripts are complete and unedited.
- [x] I can explain and defend every part of what I submitted, and could
      reproduce or modify it on request.
