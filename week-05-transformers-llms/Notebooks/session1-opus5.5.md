# <pasted_content id="a048">
def time_to_write(model
_Exported on 09/25/2026 at 12:21:05 GMT-4 from Claude via WayLog_


**User**

<pasted_content id="a048">
def time_to_write(model, tok, prompt: str, n_new: int = 32, use_cache: bool = True) -> dict:
    """Write exactly `n_new` tokens after `prompt`, greedily, and time it.

    Returns {"prompt_tokens": int, "seconds": float, "tokens_per_second": float}.

    Steps
      1. ids = tok(prompt, return_tensors="pt").to(device)
      2. warm up: one short generate (4 tokens) so the first call's start-up cost is not timed
      3. sync(); t0 = time.perf_counter()
      4. model.generate(**ids, max_new_tokens=n_new, min_new_tokens=n_new, use_cache=use_cache,
                        pad_token_id=tok.eos_token_id, **GREEDY)   -- inside torch.no_grad()
      5. sync(); seconds = time.perf_counter() - t0
      6. return the dict; prompt_tokens is ids["input_ids"].shape[1]

    `use_cache=True` is the library remembering the past; `use_cache=False` makes it
    re-read the whole text for every new token.
    """
    ids = tok(prompt, return_tensors='pt').to(device)

    t0= time.perf_counter()
    torch.no_grad(model.generate(**ids, max_new_tokens=n_new, min_new_tokens=n_new, use_cache=use_cache,pad_token_id=tok.eos_token_id, **GREEDY))
    seconds= time.perf_counter() - t0
    prompt_tokens= ids["input_ids"].shape[1]
    return dict(prompt_tokens)

    
    # TODO
    todo("time_to_write")
</pasted_content id="a048">

; explain what is wrong, how to return dict, and what line am i missing. how to insantiate '2.' ?

---


**Claude**

Your function has five problems. Two of them crash it, and the missing warm-up and sync steps make the timing wrong.

## What's wrong

**1. `return dict(prompt_tokens)` crashes.** `dict()` needs key/value pairs, and `prompt_tokens` is a single int. You get `TypeError: 'int' object is not iterable`. You're also missing `seconds` and `tokens_per_second`.

**2. `torch.no_grad(...)` is used like a function.** It's a context manager, so it goes in a `with` block. Your version runs `generate` first and then passes the result into `no_grad`, which doesn't accept arguments and will raise an error.

**3. Step 2, the warm-up, is missing.** The first `generate` call pays one-time costs like CUDA kernel loading and memory allocation. Without a warm-up, those costs end up in your timing.

**4. Steps 3 and 5, the `sync()` calls, are missing.** GPU work runs asynchronously, so `perf_counter()` could read the time before the GPU has actually finished. `sync()` makes the CPU wait for the GPU. It's already defined in your notebook.

**5. Leftover `todo("time_to_write")`.** Delete it. It never runs because it's after the `return`, but it's dead code.

## How to write step 2 (the warm-up)

It's the same `generate` call with only 4 tokens, and you don't save the result:

```python
with torch.no_grad():
    model.generate(**ids, max_new_tokens=4, use_cache=use_cache,
                   pad_token_id=tok.eos_token_id, **GREEDY)
```

## How to return the dict

Use a dict literal with all three keys:

```python
return {
    "prompt_tokens": ids["input_ids"].shape[1],
    "seconds": seconds,
    "tokens_per_second": n_new / seconds,
}
```

## Full corrected body

```python
    ids = tok(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        # 2. warm-up (not timed)
        model.generate(**ids, max_new_tokens=4, use_cache=use_cache,
                       pad_token_id=tok.eos_token_id, **GREEDY)

        # 3. start the clock
        sync(); t0 = time.perf_counter()

        # 4. the timed run
        model.generate(**ids, max_new_tokens=n_new, min_new_tokens=n_new,
                       use_cache=use_cache, pad_token_id=tok.eos_token_id, **GREEDY)

        # 5. stop the clock
        sync(); seconds = time.perf_counter() - t0

    # 6. return the dict
    return {
        "prompt_tokens": ids["input_ids"].shape[1],
        "seconds": seconds,
        "tokens_per_second": n_new / seconds,
    }
```

`tokens_per_second` is `n_new / seconds` because you forced exactly `n_new` new tokens with `min_new_tokens=n_new`. That's also why `min_new_tokens` matters: without it, the model could stop early at an end-of-text token and the rate would be wrong.

---


**User**

<pasted_content id="a048">
"remembers the past (s)": round(on["seconds"], 2),
     24                            "speed-up": f"{off['seconds'] / on['seconds']:.1f}x",
---> 25                            "tokens/s with the past remembered": round(on["tokens_per_second"], 1)})
     26     free_model(_model); del _tok, _model
     27     if cache_rows:

KeyError: 'tokens_per_second'
</pasted_content id="a048">

; whats wrong, dont fix the code, explain and offer a fix

---


**Claude**

That `KeyError` means `time_to_write` returned a dict without a `"tokens_per_second"` key.

**What happened:** the cell builds each table row by reading keys from the dict your function returns (`on`). It got through `on["prompt_tokens"]` and `on["seconds"]` without trouble, so those two keys exist. It only failed at `on["tokens_per_second"]`, so your dict has the first two keys and not that one.

**Likely causes:**

1. **The key is missing.** For example, you returned only `prompt_tokens` and `seconds` and haven't computed the rate yet.
2. **The key is spelled differently.** The lookup needs an exact match, so `"tokens_per_sec"`, `"tokens per second"`, `"Tokens_per_second"` and `"tps"` would all fail.
3. **The notebook is still using an old version of your function.** If you fixed the function but didn't re-run its cell (TODO 1b), the provided cell keeps calling the earlier version. I checked the file on disk, and that cell still shows the original `todo("time_to_write")`. So your latest edits may not be saved yet, or not run.

**How to fix it:** the return should have exactly these three keys, spelled as the docstring says:

```python
return {
    "prompt_tokens": ids["input_ids"].shape[1],
    "seconds": seconds,
    "tokens_per_second": n_new / seconds,
}
```

The rate is `n_new / seconds` because `min_new_tokens=n_new` makes the model write exactly `n_new` tokens.

Then re-run the TODO 1b cell first and the provided "Bill 2" cell after it.

**To confirm the cause**, run this in a scratch cell:

```python
print(on.keys())
```

It will show exactly which keys your function is returning.

---


**User**

print(on.keys())

---


**Claude**

I can't run that for you. `on` only exists in your notebook's running kernel, and I can't see that from here. Here's how to do it yourself:

1. Add a new cell right below the "Bill 2" cell that raised the error.
2. Paste in `print(on.keys())` and run it.
3. Paste the output here.

How to read the result:

| Output | Meaning | Fix |
|---|---|---|
| `dict_keys(['prompt_tokens', 'seconds'])` | The rate key is missing | Add `"tokens_per_second": n_new / seconds` to your return |
| `dict_keys(['prompt_tokens', 'seconds', 'tokens_per_sec'])` or another spelling | The key has a typo | Rename it to exactly `"tokens_per_second"` |
| `dict_keys(['prompt_tokens', 'seconds', 'tokens_per_second'])` | Your code is correct, but the kernel is running an old version | Re-run the TODO 1b cell, then the Bill 2 cell |
| `NameError: name 'on' is not defined` | The kernel restarted | Re-run from the top of the notebook |

Also save the notebook (Ctrl+S). The copy on disk still shows the original `todo("time_to_write")`, so I can't see your current code. Once you save, I can read the actual function.

---


**User**

check again

---


**Claude**

Now that it's saved, I can see the cause. It's a typo in the key name.

**The problem** is in your return statement, in the TODO 1b cell:

```python
"token_per_second": n_new / seconds}
```

You wrote `token_per_second`, but the provided cell looks up `tokens_per_second`, with an **s** on "tokens". Dictionary keys have to match exactly, so the lookup fails with `KeyError`.

**Fix:** change `"token_per_second"` to `"tokens_per_second"`. Then re-run the TODO 1b cell, and after it the Bill 2 cell.

There's also one smaller issue you may want to fix:

- **Step 4 is outside `torch.no_grad()`.** Your `with torch.no_grad():` block only covers the warm-up call. The timed `model.generate(...)` at step 4 is back at the outer indentation level, so it isn't inside the block. The docstring says step 4 should run inside `torch.no_grad()`. It won't crash or change your numbers much, because `generate` turns off gradients internally anyway, but it doesn't match the spec. To fix it, indent steps 3–5 under the `with` block.

The leftover `# TODO` / `todo("time_to_write")` after the `return` never runs, so it's harmless. You can delete it to tidy up.

---
