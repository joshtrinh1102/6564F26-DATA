# why is the shape not matcing? dont alter the code 
_Exported on 09/04/2026 at 12:00:26 GMT-4 from Claude via WayLog_


**User**

why is the shape not matcing? dont alter the code just explain to me

---


**Claude**

I looked through the notebook, but none of the cells show an actual shape-mismatch error in their saved output — every TODO cell is still unfilled (`None`), so nothing has run far enough to hit a shape error yet. A couple of spots in this notebook are classic places for a shape mismatch to occur once you fill them in, so let me confirm which one you're hitting.

---


**User**

[Request interrupted by user for tool use]

---


**User**

its in week 02 practice notebook, step 1, where its returning the error of M and X_sk not matcing sapes

---


**Claude**

The likely cause is the single-character token `a` in `d5` ("a log is not a mat") — and cell [c008](week-02-vectors-similarity/ism6564-week02-practice.ipynb) actually flags this exact trap in the markdown right above your TODO.

Here's the mechanism:

- Your hand-built `vocab` (cell [c006](week-02-vectors-similarity/ism6564-week02-practice.ipynb)) presumably uses `str.split()` on each doc and takes the sorted set of tokens. That includes `"a"` as a token, since `str.split()` doesn't care about word length. So `len(vocab)` = 16.
- `CountVectorizer`'s **default** tokenizer doesn't use `str.split()` — it uses a regex, `token_pattern`, whose default is `r"(?u)\b\w\w+\b"`, meaning "two or more word characters." A single-letter token like `"a"` never matches that pattern and gets silently dropped from the vocabulary.
- So if your `cv` in cell [c009](week-02-vectors-similarity/ism6564-week02-practice.ipynb) was created as `CountVectorizer()` (defaults) — or even `CountVectorizer(tokenizer=str.split)` without also disabling `token_pattern` — its learned vocabulary is only 15 terms, one short of your 16. `M` ends up shape `(5, 16)`, `X_sk` ends up shape `(5, 15)`, and `np.array_equal` (or the comparison) chokes on mismatched shapes.

The fix (already spelled out in cell c008's markdown) is to construct the vectorizer with **both** arguments:

```python
CountVectorizer(tokenizer=str.split, token_pattern=None)
```

Passing `tokenizer=str.split` alone isn't enough — sklearn still applies `token_pattern` unless you explicitly set it to `None` (and will actually emit a warning telling you `token_pattern` is being ignored, which is a hint the two need to agree).

Check your `cv = ...` line in cell c009 for that combination — that's almost certainly where the shape divergence comes from.

---


**User**

# TODO: fit a CountVectorizer that reproduces `M` exactly, and store the
# dense array in X_sk.
from sklearn.feature_extraction.text import CountVectorizer

cv_default= CountVectorizer()
cv_default.fit(DOCS)

cv = CountVectorizer(tokenizer=str.split,token_pattern=None)
X_sk = cv.fit_transform(DOCS)

print(f"default token_pattern     -> {len(cv_default.get_feature_names_out()):2d} terms")
print(f"tokenizer=str.split       -> {len(cv.get_feature_names_out()):2d} terms")
print("dropped by the default    ->",
      sorted(set(cv.get_feature_names_out()) - set(cv_default.get_feature_names_out())))

assert list(cv.get_feature_names_out()) == vocab
assert np.array_equal(X_sk.toarray(), M)
print("\nhand-built matrix == CountVectorizer output   (asserted)")

# get X_sk to a dense array
print(type(X_sk))
print(f"shape {X_sk.shape}, stored non-zeros{X_sk.nnz} of {np.prod(X_sk.shape)} cells")
print(f"\nd1 as a dense row: {X_sk[1].toarray()[0]}")
print("d1 as (term,count) pairs:",
      {cv.get_feature_names_out()[j]: int(v) for j, v in zip(X_sk[1].indices, X_sk[1].data)})
; hers the code, and here: if X_sk is None or M is None:
    print("Step 1 not finished — fill in the TODOs above, then re-run.")
else:
    same_vocab = list(cv.get_feature_names_out()) == list(vocab)
    same_counts = np.array_equal(np.asarray(M), X_sk)
    print(f"vocabularies identical  : {same_vocab}")
    print(f"count matrices identical: {same_counts}")
    assert same_vocab and same_counts, "not yet matching — check the tokenizer arguments"

    # And the default settings, for contrast.
    cv_default = CountVectorizer().fit(DOCS)
    dropped = sorted(set(vocab) - set(cv_default.get_feature_names_out()))
    print()
    print(f"default CountVectorizer vocabulary size: {len(cv_default.vocabulary_)} "
          f"(ours: {len(vocab)})")
    print(f"tokens the default pattern threw away  : {dropped}"); dont fix the code, just tell me where the mistmatch is and why

---


**Claude**

The mismatch is in this line of your own code:

```python
X_sk = cv.fit_transform(DOCS)
```

`fit_transform` returns a **scipy sparse matrix**, not a dense NumPy array. The TODO comment even says to store the *dense* array in `X_sk` — that conversion never happens.

You can see you actually noticed this later in your own cell, since you call `.toarray()` explicitly when you need dense output (`X_sk.toarray()` in your assert, and `X_sk[1].toarray()[0]` when printing a row). So your own hand-written assert (`np.array_equal(X_sk.toarray(), M)`) passes fine — you converted at the point of comparison.

But the pre-written check cell you selected (the one starting `if X_sk is None or M is None:`) does **not** call `.toarray()`:

```python
same_counts = np.array_equal(np.asarray(M), X_sk)
```

Here `X_sk` is still the sparse matrix. `np.asarray()`/`np.array_equal` don't know how to unpack a scipy sparse matrix into its dense contents — instead of raising a clean error, it gets wrapped as a 0-d NumPy object array holding the sparse matrix as a single opaque element. So its "shape" as far as `np.array_equal` sees it is nothing like `M`'s `(5, 16)`, and the shapes don't line up.

Fix conceptually: `X_sk` itself needs to be the dense array (e.g. `X_sk = cv.fit_transform(DOCS).toarray()`), not the sparse matrix — that's what the TODO was asking for, and it's why the provided check cell compares directly without adding its own `.toarray()`.

---
