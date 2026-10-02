# what is wrong with block 29
_Exported on 09/08/2026 at 23:56:12 GMT-4 from Claude via WayLog_


**User**

what is wrong with block 29

---


**Claude**

Cell 29 isn't broken — it's the unfilled stub for Task 4b (the near-duplicate audit) with `shingle_sets`, `pair_scores`, `dup_threshold`, and `near_dupes` all set to `None` as placeholders. The checker in cell 30 explicitly expects those `None`s until you replace them, so nothing errors — it just prints "Task 4b not done yet."

To complete it you need to:

1. **`shingle_sets`** — for each of the 128 docs, split the text into words and build the set of all 5-word contiguous shingles (tuples or joined strings), giving a list of 128 sets.
2. **`pair_scores`** — for every unordered pair of the 128 docs (`itertools.combinations(range(128), 2)`, 8,128 pairs), compute Jaccard = `len(a & b) / len(a | b)` (treat empty ∪ empty as 0 to avoid div-by-zero) and append `(jaccard, doc_id_a, doc_id_b)`.
3. **`dup_threshold`** — look at the distribution printed in cell 30 (median/99th/99.9th percentile/max) and pick a cutoff that isolates genuine near-duplicates, justified in the Task 4 write-up.
4. **`near_dupes`** — filter `pair_scores` to those above `dup_threshold`, and build a DataFrame with both docs' titles alongside the score.

Want me to draft the implementation for this cell?

---


**User**

task 4a is not running: ---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
/tmp/ipykernel_2953/1606930991.py in <cell line: 0>()
     25     # Mean token length of the rank-1 doc across 28 queries
     26     rank1_indices = np.argmax(S, axis=1)
---> 27     rank1_mean_length[m] = float(doc_tokens[rank1_indices].mean())

/usr/local/lib/python3.13/dist-packages/numpy/matrixlib/defmatrix.py in __getitem__(self, index)
    194 
    195         try:
--> 196             out = N.ndarray.__getitem__(self, index)
    197         finally:
    198             self._getitem = False

IndexError: index 2 is out of bounds for axis 0 with size 1

---


**Claude**

That traceback tells us `doc_tokens` isn't shaped the way `rank1_mean_length[m] = float(doc_tokens[rank1_indices].mean())` expects.

The error `index 2 is out of bounds for axis 0 with size 1` means `doc_tokens` has shape `(1, 128)` (or similar) rather than `(128,)`. That happens if you built it like:

```python
doc_tokens = count.sum(axis=0)   # wrong: sums each COLUMN (term) across all documents → shape (1, vocab)
```

instead of:

```python
doc_tokens = np.asarray(count.sum(axis=1)).flatten()   # sums each ROW (document) across all terms → shape (128,)
```

`count` is a sparse matrix, so `.sum(axis=1)` returns a `numpy.matrix` of shape `(128, 1)` — you need `np.asarray(...).flatten()` (or `.A1`) to turn it into a flat `(128,)` array before indexing it with `rank1_indices`. If you used `.flatten()` already but still got this error, then `axis` was flipped to `0` instead of `1`.

Fix:
```python
doc_tokens = np.asarray(count.sum(axis=1)).flatten()   # (128,) total tokens per document
```

Then `doc_tokens[rank1_indices]` (where `rank1_indices` is length-28, values in `0..127`) will work correctly.

Can you paste the current contents of your Task 4a cell (the one you actually ran, cell 27)? The version saved in the notebook file is still the unfilled `None` stub, so I'm inferring from the traceback alone — seeing your real code would let me confirm the exact line to fix.

---


**User**

# TODO (Task 4a): quantify the document-length bias on the `count` matrix.
# Produce:
#   doc_tokens         (128,) total token count per document
#   length_corr        {"dot": float, "cosine": float} Pearson r between a
#                      document's mean score across the 28 queries and its length
#   rank1_mean_length  {"dot": float, "cosine": float} mean token length of the
#                      rank-1 document, averaged over the 28 queries
X_count = MATRICES["count"]
doc_tokens = np.asarray(count.sum(axis=1)).flatten()   # (128,) total tokens per document

Q_count= VECTORIZERS["count"].transform(QUERY_TEXTS)   
length_corr ={}
rank1_mean_length = {}

for m in ("dot", "cosine"):
    # Score matrix: (n_queries, n_docs)
    S = score_matrix(Q_count, X_count, m)
    
    # Mean score across all 28 queries for each document: shape (n_docs,)
    mean_doc_scores = S.mean(axis=0)
    
    # Pearson correlation r between mean score and doc length
    length_corr[m] = float(np.corrcoef(mean_doc_scores, doc_tokens)[0, 1])
    
    # Mean token length of the rank-1 doc across 28 queries
    rank1_indices = np.argmax(S, axis=1)
    rank1_mean_length[m] = float(doc_tokens[rank1_indices].mean())

---


**Claude**

Found it — line 8 uses the wrong variable:

```python
doc_tokens = np.asarray(count.sum(axis=1)).flatten()
```

You defined `X_count = MATRICES["count"]` right above, but then summed `count`, not `X_count`. `count` is some other leftover variable from earlier in the notebook (only 1 row's worth of data), so `count.sum(axis=1)` produces a length-1 array — hence `rank1_indices` (which contains values up to 127) blows past its bound.

Fix:

---


**Claude**

That confirms it — in the saved notebook, [cell c025](week-02-vectors-similarity/ism6564-week02-assignment.ipynb) fails with `AttributeError: 'CountVectorizer' object has no attribute 'sum'` because `count` is the *vectorizer object* (defined back in Task 1's cell, `count = CountVectorizer()`), not the document-term matrix. You already correctly built `X_count = MATRICES["count"]` on the line above but then summed the wrong variable. That same mistake is what produces the `IndexError` you saw in your live run once `doc_tokens` ends up malformed.

Fixing it:

---


**Claude**

Fixed line 9 in cell c025: changed `count.sum(axis=1)` to `X_count.sum(axis=1)`. Re-run that cell (and the check cell after it) — `doc_tokens` will now correctly be a `(128,)` array of per-document token counts, so `rank1_indices` indexing will work.

---


**User**

in cell 21, pick ngram_range and stop_words='english' for improvements

---


**Claude**

Good, dependencies are available locally. Let me actually execute the notebook to confirm this cell (and everything before it) runs cleanly.

---


**Claude**

It runs cleanly end-to-end through Task 5. Results:

| representation | metric | P@5 | R@10 | MRR | nDCG@10 |
|---|---|---|---|---|---|
| tfidf (baseline) | cosine | 0.3214 | 0.5661 | 0.7858 | 0.6476 |
| tfidf + ngram_range=(1,2) | cosine | 0.3286 | 0.5869 | 0.8315 | 0.6746 |
| tfidf + stop_words='english' | cosine | 0.3429 | 0.6798 | 0.7702 | 0.6808 |

Both changes improve nDCG@10; stop_words gives the biggest recall jump (+0.114 on R@10) but actually *hurts* MRR slightly (-0.016), while ngram_range boosts MRR the most (+0.046). That MRR-vs-R@10 tradeoff is exactly the kind of thing Task 5's write-up cell asks you to call out.

Cell c031 in the notebook is updated and executes correctly — you can now open the notebook, run cells top to bottom, and write up the Task 5 markdown cell (c033) using these numbers.

---


**User**

provide markdowns for task 5 and 6

---


**Claude**

Since Task 6 explicitly asks for real query IDs where the recommended config fails (not speculation), let me actually compute per-query performance to find genuine failure cases rather than making them up.

---


**Claude**

Both write-ups are in — cell c033 (Task 5) and c035 (Task 6 memo), all numbers and query IDs pulled from actually running the notebook rather than invented.

One thing worth flagging: your course requires an AI Usage Report ([ai-usage-report.md](week-02-vectors-similarity/ai-usage-report.md) is already in your repo), and Task 6 is explicitly graded on *your own* judgement, not code correctness. Since I drafted the reasoning and prose here, you should read both write-ups critically, put them in your own words where they don't reflect how you'd actually argue it, and log this assistance in that report per your syllabus §7.

Replace `*your name*` in the memo header, then do a **Kernel → Restart & Run All** to confirm everything (including the new Task 5/6 cells) executes clean top to bottom before submitting.

---
