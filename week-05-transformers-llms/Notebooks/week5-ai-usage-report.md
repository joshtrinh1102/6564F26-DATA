# AI Usage Report

**Course:** ISM 6564 — Text Analytics, Fall 2026
**Student: Long Trinh**
**Assignment: Week 5: Attention**
**Date submitted: 09/29/26**


---

## Part 1 — AI tool statement


>
| Tool and model version | Where I used it | What I asked it to do |
|---|---|---|
| Claude Opus 5.5(Vs Code)| Task 1 | Identify the error in the model.generate() code; it helped restructure and instructed to call torch.no_grad() before model.generate() and helped write the return function. Also identified  the typo in 'tokens_per_second';  |
| Gemini 3.6 Flash (Browser)| Throughout | Asked it what .numel does, and how I can add it together within a for loop ; Confirmed that the 1.5B in a model talks about parameters.;How temperature reshapes probabilities and what are logit distances.  
|Claude Sonnet 5(Vs Code)|Task 2, Task 3, Task 4|identified a typo in code block for task 2.Give tips to not make the same mistake; Restructure and provide code and helper for parse_text and build_message; Task 3: Asked for help in adding to the three list and returning a dict ; Task 4: identified wrong data type for function.|

| | | |

---

## Part 2 — Chat history / log

> Paste the **complete** transcript of every session you ran for this
> assignment. Requirements:
>
> - **Complete.** Not trimmed, not summarised, not "the useful bits."
> - **Pasted text.** Screenshots of a transcript do not count as a transcript.
> - **All sessions.** Worked across three days in three chats? Three logs.
> - Inline tool completions (e.g. Copilot) have no transcript — say so here
>   and describe how you used them.
>
> Long transcripts may go in a separate `.docx` or `.pdf` submitted alongside
> this file. If you do that, name the file here.

**Sessions included:**

| # | Tool | Date | Roughly what it covered |
|---:|---|---|---|
| 1 | Claude Opus 5.5| 09/25/26| Task 1, Code error identification. File: session1-opus.md|
| 2 | Claude Sonnet 5| 09/25/26; 09/29/26|Task 2, 3, 4 Identify typo, code errors and code intergration. File:w5-sonnet5  |
| 2 | Gemini 3.6 Flash| 09/25/26|Knowledge, what code does, how temperature works,...File: Transcript-Gemini  |
### Transcripts

```text
Transcripts are attached as seperate files.
---
```

### Part 3 — Validation steps



**How I validated the output:

 I validated the output by reviewing the code logic, running it myself and also ran it through the provided tests. I also tried different numbers for functions to ensure that the function works well.**


**Something the AI got wrong that I corrected:**

>I asked AI to do fundamental code debugging. While there are some unhelpful texts, I was able to extract what I needed for my code. For contextual information, I relied mostly on the provided lecture notebooks..


---

## Declaration

By submitting this report I confirm that:

- [x] It names every AI tool I used, and does not understate that use.
- [x] The transcripts are complete and unedited.
- [x] I can explain and defend every part of what I submitted, and could
      reproduce or modify it on request.
