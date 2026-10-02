# # TODO: fill in each measure. Use scipy where it h
_Exported on 09/04/2026 at 14:55:13 GMT-4 from Claude via WayLog_


**User**

# TODO: fill in each measure. Use scipy where it has the function.
measures = {
    "cosine distance":    None,
    "cosine similarity":  None,
    "dot product":        None,
    "euclidean":          Euclidean,
    "cityblock":          None,
    "minkowski p=3":      None,
    "jaccard similarity": None,
    "hamming distance":   None,; explain to me how to do this, dont do it for me..

---


**Claude**

Here's the shape of it, based on what's already set up in the cells above (`a_tfidf`/`b_tfidf` for the TF-IDF rows, `a_bin`/`b_bin` for the binary presence vectors, and `distance` = `scipy.spatial.distance`, already imported in [ism6564-week02-practice.ipynb:1-15](week-02-vectors-similarity/ism6564-week02-practice.ipynb#L1-L15)):

**The `distance` module gives you distances, not similarities**, so you'll compute some entries directly and derive others:

1. **cosine distance** — `distance.cosine(a_tfidf, b_tfidf)` directly.
2. **cosine similarity** — scipy has no `cosine_similarity` function in `distance`; use the identity `similarity = 1 - distance`, i.e. `1 - measures["cosine distance"]` (or reuse the value you just computed).
3. **dot product** — no scipy helper needed, just `a_tfidf @ b_tfidf` or `np.dot(a_tfidf, b_tfidf)`.
4. **euclidean** — `distance.euclidean(a_tfidf, b_tfidf)`.
5. **cityblock** (Manhattan) — `distance.cityblock(a_tfidf, b_tfidf)`.
6. **minkowski p=3** — `distance.minkowski(a_tfidf, b_tfidf, p=3)`.
7. **jaccard similarity** — this one switches to the *binary* vectors (`a_bin`, `b_bin`), not TF-IDF. `distance.jaccard` returns Jaccard *distance*, so similarity is `1 - distance.jaccard(a_bin, b_bin)`.
8. **hamming distance** — also on `a_bin`/`b_bin`. `distance.hamming(...)` returns the *fraction* of differing positions (not a count), which is what the check cell below expects (it multiplies back by `n_terms` to recover the count).

So the pattern is: six of the eight use the TF-IDF vectors, two use the binary vectors; scipy gives you distances, and where the dict asks for a similarity you invert with `1 - x`.

---


**User**

a_tfidf @ b_tfidf; what does the @ do, why is it not *

---


**Claude**

`@` is Python's matrix-multiplication operator (`__matmul__`, added in Python 3.5, PEP 465). For two 1-D NumPy arrays, `a @ b` computes the **dot product** — a single scalar: `sum(a[i] * b[i] for i in range(len(a)))`.

`*` on two NumPy arrays is **element-wise multiplication** — it returns an array of the same shape, `[a[0]*b[0], a[1]*b[1], ...]`, not a scalar. To get the dot product with `*` you'd have to also sum: `(a * b).sum()`, which is equivalent to `a @ b` but does two ops instead of one.

So for vectors, `a @ b` and `(a * b).sum()` give the same number — `@` is just the direct, idiomatic way to write it (and for 2-D arrays it becomes true matrix multiplication, whereas `*` stays element-wise/broadcast).

---


**User**

def levenshtein(a: str, b: str) -> int:
    """Minimum single-character edits turning `a` into `b`."""
    m, n = len(a), len(b)
    D = [[0] * (n + 1) for _ in range(m + 1)]
  # TODO: initialise the first column (D[i][0]) and the first row (D[0][j]).
    D[:,0]= np.arange(D[i][0])
    D[0,:]=np.arange(D[0][j])
    # TODO: fill the rest of the table with the recurrence above.
    for i in range(1, n+1):
        for j in range (1, m+1):
            D[i,j]=min(
                D[i-1,j]+1,
                D[i,j-1]+1,
                D[i-1,j-1] + (a[i-1]!= b[j-1]),
            )
  


    return D[m][n]


levenshtein_done = True   # TODO: set to True once you have implemented it;EXPECTED = [
    ("waranty", "warranty", 1),   # one insertion
    ("kitten", "sitting", 3),     # the textbook example
    ("recieve", "receive", 2),    # a transposition costs 2, not 1
    ("cat", "cats", 1),
    ("", "abc", 3),
    ("same", "same", 0),
]

if not levenshtein_done:
    print("Step 4 not done yet — implement levenshtein(), then re-run.")
else:
    for a, b, want in EXPECTED:
        got = levenshtein(a, b)
        flag = "ok " if got == want else "BAD"
        print(f"{flag} levenshtein({a!r:>10}, {b!r:>10}) = {got}  (expected {want})")
    assert all(levenshtein(a, b) == w for a, b, w in EXPECTED)

---


**Claude**

A few bugs, in order of how much they matter:

1. **`D[i, j]` doesn't work on a Python list.** `D` is a list of lists (`[[0]*(n+1) for _ in range(m+1)]`), not a NumPy array, so it only supports `D[i][j]` (two separate index lookups), not comma-tuple indexing `D[i, j]`. Every line using `D[i-1,j]`, `D[i,j-1]`, `D[i-1,j-1]`, `D[:,0]`, `D[0,:]` will raise a `TypeError`.

2. **The init lines reference `i`/`j` before they're bound**, and even conceptually the approach is inverted: `np.arange(D[i][0])` tries to build an array from a single cell's *value*, not from a range up to `m` or `n`. What you actually want is to walk `i` from `0` to `m` and set each `D[i][0] = i` (the cost of turning the first `i` characters of `a` into the empty string is `i` deletions) — and symmetrically for the first row against `b`.

3. **Your loop bounds are swapped.** `D` has shape `(m+1) x (n+1)` — rows indexed by `i` (over `a`, length `m`) and columns indexed by `j` (over `b`, length `n`). But you wrote `for i in range(1, n+1): for j in range(1, m+1)`, which walks rows using `n` and columns using `m`. If `a` and `b` have different lengths (they do, in every test case), this will either throw an `IndexError` (when `n > m`, `i` runs past the last row) or silently leave part of the table at its zero-initialized value (when `n < m`), and either way `a[i-1]`/`b[j-1]` get indexed with the wrong bound.

Fix the indexing style first (single brackets throughout), then fix the two loop headers so `i` ranges over `1..m` and `j` ranges over `1..n` — matching the row/column convention `D` was built with.

---


**User**

def levenshtein(a: str, b: str) -> int:
    """Minimum single-character edits turning `a` into `b`."""
    m, n = len(a), len(b)
    D = [[0] * (n + 1) for i in range(m + 1)]
  # TODO: initialise the first column (D[i][0]) and the first row (D[0][j]).
    for i in range(1, n+1):
          for j in range (1, m+1):
              D[i][0]= np.arange(n+1)
              D[0][j]=np.arange(m+1) 
    # TODO: fill the rest of the table with the recurrence above
    for i in range(1, n+1):
        for j in range (1, m+1):
            D[i][0]= np.arange(n+1)
            D[0][j]=np.arange(m+1)
            D[i,j]=min(
                D[i-1,j]+1,
                D[i,j-1]+1,
                D[i-1,j-1] + (a[i-1]!= b[j-1]),
            )
  


    return D[m][n]


levenshtein_done = True   # TODO: set to True once you have implemented it;EXPECTED = [
    ("waranty", "warranty", 1),   # one insertion
    ("kitten", "sitting", 3),     # the textbook example
    ("recieve", "receive", 2),    # a transposition costs 2, not 1
    ("cat", "cats", 1),
    ("", "abc", 3),
    ("same", "same", 0),
]

if not levenshtein_done:
    print("Step 4 not done yet — implement levenshtein(), then re-run.")
else:
    for a, b, want in EXPECTED:
        got = levenshtein(a, b)
        flag = "ok " if got == want else "BAD"
        print(f"{flag} levenshtein({a!r:>10}, {b!r:>10}) = {got}  (expected {want})")
    assert all(levenshtein(a, b) == w for a, b, w in EXPECTED)

---


**Claude**

Progress on the bracket style (`D[i][0]` is right at the assignment sites), but a few things are still off:

1. **You're assigning whole arrays into single cells.** `D[i][0]` is one cell of the table — it needs to hold a scalar (the integer edit-distance value), not `np.arange(n+1)`, which is an entire array of `n+1` numbers. The base-case value you want for `D[i][0]` is just `i` itself (turning the first `i` characters of `a` into `""` takes `i` deletions). Same for `D[0][j] = j`.

2. **The initialization is nested inside a double loop over both `i` and `j`, but it should each only depend on one index.** `D[i][0]` only varies with `i` (a single loop, `for i in range(m+1)`), and `D[0][j]` only varies with `j` (a separate single loop, `for j in range(n+1)`). As written, you recompute both boundary arrays on every `(i, j)` pair inside a nested loop — wasteful, and it also means the value assigned doesn't correspond to the index doing the assigning.

3. **The row/column bounds are still swapped**, same issue as before: `D` is `(m+1) rows) x (n+1 columns)`, but both your loops use `range(1, n+1)` for `i` and `range(1, m+1)` for `j` — backwards. `i` should range over `1..m`, `j` over `1..n`.

4. **The init block is duplicated verbatim inside the recurrence loop**, so even if it were correct, it would re-stomp `D[i][0]`/`D[0][j]` on every interior cell instead of running once before the main fill.

5. **`D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, ...)`** — back to comma-tuple indexing on a plain Python list, which raises `TypeError`. Needs `D[i][j]`, `D[i-1][j]`, `D[i][j-1]`, `D[i-1][j-1]` throughout.

Try restructuring as three separate passes: one loop to set the first column, one loop to set the first row, then the nested loop (with corrected bounds) for the recurrence — touching each `D[i][j]` exactly once.

---


**User**

hơ to fix the D[i][0]= np.arange(n+1)
        D[0][j]=np.arange(m+1)

---


**Claude**

These two lines have two separate problems to fix:

**What each line should mean, conceptually:**
- `D[i][0]` = cost of turning the first `i` characters of `a` into an empty string → that's `i` deletions, so `D[i][0]` should equal `i`.
- `D[0][j]` = cost of turning an empty string into the first `j` characters of `b` → that's `j` insertions, so `D[0][j]` should equal `j`.

**Why `np.arange(n+1)` / `np.arange(m+1)` is wrong here:** those produce whole arrays (`[0, 1, 2, ..., n]`), but you're assigning into a *single cell* (`D[i][0]` is one number, not a row or column slice). You'd only use `np.arange` if you were assigning to an entire column/row at once — which you could do, but only if `D` were a NumPy array, and it's currently a list of lists.

**Two ways to fix it**, pick one:

- *Scalar assignment inside a loop* — replace the whole block with two separate, single-index loops (not nested together, and not tied to `i`/`j` from the recurrence loop):
  ```
  for i in range(m + 1):
      D[i][0] = i
  for j in range(n + 1):
      D[0][j] = j
  ```
- *Vectorized column/row assignment* — only works if you first convert the first column/row using slicing, e.g. `D[0] = list(range(n + 1))` for the whole first row in one shot, and for the first column you'd still need a loop (or convert `D` to a NumPy array) since `D[i][0]` for varying `i` isn't a contiguous slice of a plain Python list.

Given `D` is a list of lists elsewhere in your function, the first option (plain loop, scalar assignment) is the one that fits — keep it out of the nested `i,j` recurrence loop entirely; it should run once, before that loop.

---


**User**

mp/ipykernel_14715/3675770427.py in <cell line: 0>()
     12 else:
     13     for a, b, want in EXPECTED:
---> 14         got = levenshtein(a, b)
     15         flag = "ok " if got == want else "BAD"
     16         print(f"{flag} levenshtein({a!r:>10}, {b!r:>10}) = {got}  (expected {want})")

/tmp/ipykernel_14715/1117520150.py in levenshtein(a, b)
      5   # TODO: initialise the first column (D[i][0]) and the first row (D[0][j]).
      6     for i in range(1, n+1):
----> 7         D[i][0]= i
      8     for j in range(1, m+1):
      9         D[0][j]=j

---


**Claude**

The traceback confirms the row/column swap again — this time it snuck into the initialization loops. The full error message is presumably an `IndexError: list index out of range` at `D[i][0] = i`.

`D` was built as `[[0] * (n+1) for i in range(m+1)]`, so it has **`m+1` rows** and **`n+1` columns**. That means:

- The **row** index `i` (walking down `D[i][0]`, the first *column*) must stay within `0..m` → the loop should be `for i in range(1, m + 1)`, not `range(1, n + 1)`.
- The **column** index `j` (walking across `D[0][j]`, the first *row*) must stay within `0..n` → the loop should be `for j in range(1, n + 1)`, not `range(1, m + 1)`.

You have them swapped: `for i in range(1, n+1): D[i][0] = i` — when `n > m` (e.g. `a="cat"` (m=3), `b="cats"` (n=4), or the `("", "abc", 3)` case where `m=0, n=3`), `i` climbs past `m`, and `D` only has `m+1` rows, so `D[i]` goes out of range.

Same fix pattern as the recurrence loop earlier: **`i` pairs with `m`, `j` pairs with `n`**, consistently everywhere in the function.

---


**User**

def levenshtein(a: str, b: str) -> int:
    """Minimum single-character edits turning `a` into `b`."""
    m, n = len(a), len(b)
    D = [[0] * (n + 1) for i in range(m + 1)]
  # TODO: initialise the first column (D[i][0]) and the first row (D[0][j]).
    for i in range(1, m+1):
        D[i][0]= i
    for j in range(1, n+1):
        D[0][j]=j
    # TODO: fill the rest of the table with the recurrence above
    for i in range(1, m+1):
        for j in range (1, n+1):
            D[i,j]=min(
                D[i-1,j]+1,
                D[i,j-1]+1,
                D[i-1,j-1] + (a[i-1]!= b[j-1]),
            )
  


    return D[m][n]


levenshtein_done = True   # TODO: set to True once you have implemented it

---


**Claude**

Loop bounds and initialization are correct now. One bug left, the same one flagged a couple rounds ago and still unfixed in the recurrence body:

```
D[i,j]=min(
    D[i-1,j]+1,
    D[i,j-1]+1,
    D[i-1,j-1] + (a[i-1]!= b[j-1]),
)
```

`D` is a list of lists, so it only supports `D[i][j]` (bracket-after-bracket), not the comma-tuple form `D[i, j]` (that syntax only works on NumPy arrays / pandas, where it's shorthand for a different indexing protocol). Running this as-is will raise `TypeError: list indices must be integers or slices, not tuple`.

Replace every comma-indexed access with double-bracket form: `D[i][j]`, `D[i-1][j]`, `D[i][j-1]`, `D[i-1][j-1]`. Once that's done, the recurrence itself (the `min(...)` with the three costs) is logically correct — delete, insert, substitute-or-match.

---


**User**

def levenshtein(a: str, b: str) -> int:
    """Minimum single-character edits turning `a` into `b`."""
    m, n = len(a), len(b)
    D = [[0] * (n + 1) for i in range(m + 1)]
  # TODO: initialise the first column (D[i][0]) and the first row (D[0][j]).
    
    # TODO: fill the rest of the table with the recurrence above
    for i in range(1, m+1):
        for j in range (1, n+1):
            D[i,j]=min(
                D[i-1,j]+1,
                D[i,j-1]+1,
                D[i-1,j-1] + (a[i-1]!= b[j-1]),
            )
  


    return D[m][n]
A,B= "recieve", "receive"
levenshtein(A,B)
levenshtein_done = False   # TODO: set to True once you have implemented it; w tis, ow do i i nitialize the first column and first row

---


**Claude**

The init loops from a few turns ago got dropped — you'll need to add them back. Two separate single-index loops, placed before the recurrence loop:

- **First column**, `D[i][0]` for `i` from `1` to `m`: this is the cost of turning the first `i` characters of `a` into `""` — `i` deletions, so `D[i][0] = i`.
- **First row**, `D[0][j]` for `j` from `1` to `n`: cost of turning `""` into the first `j` characters of `b` — `j` insertions, so `D[0][j] = j`.
- `D[0][0]` is already `0` from how `D` was built, so it doesn't need its own line.

So conceptually: one loop over `i` in `range(1, m + 1)` setting `D[i][0] = i`, and one loop over `j` in `range(1, n + 1)` setting `D[0][j] = j` — same as what you had working two turns ago, just needs to go back in above the `# TODO: fill the rest of the table` comment.

One more thing before you re-run: the recurrence loop still has `D[i,j]` / `D[i-1,j]` / etc. — comma-tuple indexing, which fails on a list of lists. That still needs to become `D[i][j]`, `D[i-1][j]`, `D[i][j-1]`, `D[i-1][j-1]` or you'll hit the same `TypeError` as before.

---


**User**

# TODO: for every pair (i, j) with i < j among the 5 TF-IDF rows, compute
#   lhs = squared Euclidean distance
#   rhs = 2 * (1 - cosine similarity)
# and record the largest absolute difference between them.
max_gap = None

---


**Claude**

Here's the approach, in words:

**Getting the pairs.** You need all pairs `(i, j)` with `i < j` from indices `0..4` (5 rows → C(5,2) = 10 pairs). The itertools module has `combinations` for exactly this: `itertools.combinations(range(5), 2)` yields each `(i, j)` pair once, already satisfying `i < j`. (You could also write nested loops — `for i in range(5): for j in range(i+1, 5):` — same effect, just more manual.)

**For each pair, compute the two quantities:**
- `lhs` = squared Euclidean distance between `tfidf_sk[i]` and `tfidf_sk[j]`. `scipy.spatial.distance.euclidean` gives you the (unsquared) distance, so square its result — or skip scipy and compute it directly as `np.sum((tfidf_sk[i] - tfidf_sk[j])**2)`, which is the same thing without a square-root-then-square round trip.
- `rhs` = `2 * (1 - cosine_similarity)`. You already have two ways to get cosine similarity from earlier steps: `1 - distance.cosine(tfidf_sk[i], tfidf_sk[j])`, or sklearn's `cosine_similarity([tfidf_sk[i]], [tfidf_sk[j]])[0, 0]`.

**Tracking the max gap.** For each pair, take `abs(lhs - rhs)`, and keep a running maximum across all 10 pairs — either accumulate the diffs into a list and take `max(...)` at the end, or keep a running variable that you update with `max(running, diff)` inside the loop. Assign the final result to `max_gap`.

The point of the exercise (per the markdown above) is that this gap should come out at essentially 0 (float noise, like `1e-16`) — that's the L2-normalized-vector identity being verified.

---


**User**

QUERY = "log mat"

# TODO: fit a CountVectorizer on DOCS6 (same arguments as Step 1), transform
# the query, and compute both scores against all six documents.
cv6 = CountVectorizer(tokenizer=str.split, token_pattern=None)
X6 = cv6.fit_transform(DOCS6)            # (6, V) raw counts
q6 = cv6.transform([QUERY]).toarray()[0]           # (V,)   raw counts for the query
dot_scores = q6.dot(X6.T)    # (6,)
cos_scores = np.argsort(distance.cdist(q6.reshape(1, -1), X6, "cosine")[0])      # (6,)

---


**Claude**

A few issues here, worth separating into "will crash / silently wrong" vs "inconsistent with the rest of the notebook":

1. **`cos_scores` is wrapped in `np.argsort`, which throws away the actual values.** `distance.cdist(q6.reshape(1,-1), X6, "cosine")[0]` gives you the array of six cosine *distances* — that's the data you want to keep. `np.argsort(...)` instead returns the **indices** that would sort that array (e.g. `[4, 2, ...]`), not scores. The check cell downstream does `"cosine": cos_scores` in a table and later computes `np.argsort(-np.asarray(cos_scores))` itself to get a ranking — it expects `cos_scores` to be the six raw score values, not a pre-sorted index array. Drop the `np.argsort(...)` wrapper and keep just the `distance.cdist(...)[0]` result.

2. **That gives you cosine *distance*, but you want cosine *similarity*** to be comparable with `dot_scores` (both should be "higher = more relevant" for the ranking logic in the check cell to make sense — same reason Step 3 had you do `1 - distance.cosine(...)`). Convert with `1 -` after computing the distances.

3. **`X6` is left as a sparse matrix** (`cv6.fit_transform(DOCS6)` returns a sparse CSR matrix), but the comment above it says `# (6, V) raw counts`, and every other cell in this notebook (Step 1's `X_sk`, Step 6's own table using `X6.sum(axis=1)`) works with dense arrays. Left sparse, things like `.dot()` with a dense vector, or building a DataFrame column from it later, behave inconsistently or need extra `.toarray()`/flattening calls scattered around. Converting once with `.toarray()` right after `fit_transform` (same pattern as `cv.fit_transform(DOCS).toarray()` in Step 1) avoids that.

4. **`dot_scores = q6.dot(X6.T)`** — calling `.dot()` on a dense NumPy vector with a sparse matrix argument doesn't reliably do what you want (NumPy's `.dot` isn't sparse-aware the way scipy's own matmul is). If `X6` is dense (per point 3), this becomes an ordinary `X6 @ q6` (six rows, each dotted with the query) — which is also more directly what you want conceptually: "one score per document," i.e. shape `(6,)`, rather than "the query dotted with the transpose."

Fix order: densify `X6`, then recompute `dot_scores` as the matrix-vector product of `X6` and `q6`, then compute `cos_scores` as `1 -` the cosine distances (no `argsort`).

---


**User**

QUERY = "log mat"

# TODO: fit a CountVectorizer on DOCS6 (same arguments as Step 1), transform
# the query, and compute both scores against all six documents.
cv6 = CountVectorizer(tokenizer=str.split, token_pattern=None)
X6 = cv6.fit_transform(DOCS6).toarray()[0]            # (6, V) raw counts
q6 = cv6.transform([QUERY]).toarray()[0]           # (V,)   raw counts for the query
dot_scores = q6.dot(X6.T)    # (6,)
cos_scores = 1- distance.cosine(q6,X6)   # (6,)

---


**Claude**

Two things left:

1. **`.toarray()[0]` slices off just the first row.** `cv6.fit_transform(DOCS6)` gives you a sparse matrix of shape `(6, V)` — all six documents. Calling `.toarray()` correctly densifies it to `(6, V)`, but then indexing `[0]` collapses it down to a single 1-D vector of shape `(V,)` — just document 1's counts, discarding documents 2–6 entirely. You want the whole dense array, so drop the `[0]`.

2. **`distance.cosine` only compares one pair of vectors, not one query against many documents.** Once `X6` is properly `(6, V)`, `distance.cosine(q6, X6)` won't broadcast across the 6 rows the way you want — `scipy.spatial.distance.cosine(u, v)` expects both `u` and `v` to be 1-D and the same length, so it'll either error on shape mismatch or (if it happens to run) not give you six separate scores. For "one query vs. many rows" you need either `distance.cdist(q6.reshape(1, -1), X6, "cosine")[0]` (as you used correctly a couple attempts ago, giving you a `(6,)` array of distances in one call), or loop over the six rows and call `distance.cosine` once per row. Either way, remember to do `1 -` on the result to turn distance into similarity.

`dot_scores = q6.dot(X6.T)` is fine once `X6` is the full `(6, V)` dense array — that part doesn't need to change.

---


**User**

def shingles(text: str, n: int = 3) -> set:
    """Set of overlapping word n-grams, each joined by a single space."""
    # TODO: implement.
    return set()


def jaccard(s1: set, s2: set) -> float:
    """|intersection| / |union|; 0.0 when both sets are empty."""
    # TODO: implement.
    return 0.0


shingles_done = False   # TODO: set to True once both are implemented

---


**Claude**

Here's how to think through both:

**`shingles(text, n)`** — you need the set of overlapping word n-grams. First split `text` into words (`text.split()`). Then, for a list of `w` words, there are `w - n + 1` possible windows of length `n` (if `w < n`, there are none). For each starting position `i` from `0` to `w - n`, take the slice `words[i:i+n]` and join it back into a single string with `" ".join(...)`. Collect all of those joined strings into a `set` (a set automatically dedupes if the same n-gram appears more than once) and return it.

Concretely: think "slide a window of `n` words across the sentence, one word at a time, stringify each window, put them all in a set."

**`jaccard(s1, s2)`** — the docstring already gives you the formula: `|intersection| / |union|`. Python sets support `&` for intersection and `|` for union directly, and `len()` to get their sizes. The one edge case called out is both sets empty — `len(s1 | s2)` would be `0`, and dividing by zero would raise `ZeroDivisionError`, so you need an explicit check: if the union is empty, return `0.0` before doing the division.

Once both are filled in, set `shingles_done = True`. The check cell asserts `jaccard(shingles(A, 3), shingles(B, 3))` is close to `0.4` and that `jaccard` of a shingle set with itself is exactly `1.0` — good sanity checks to reason through by hand once you've written it (e.g., self-Jaccard: intersection == union == the same set, so the ratio should always come out to 1).

---
