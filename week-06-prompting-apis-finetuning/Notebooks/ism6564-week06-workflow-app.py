"""ISM 6564 · Week 6 · Workflow example, Part C: a Streamlit page that tests YOUR fine-tuned model.

The model runs in Ollama on this machine (Part B). This page is a thin client: it sends the ticket to
Ollama through the OpenAI-compatible API, checks the reply against the contract, and shows the result.
Nothing here needs PyTorch or a GPU.

    pip install streamlit openai pydantic
    streamlit run ism6564-week06-workflow-app.py
"""
import json
import re
import time
from typing import Literal

import streamlit as st
from openai import OpenAI
from pydantic import BaseModel, Field, StrictBool, ValidationError

OLLAMA_URL = "http://localhost:11434/v1/"
DEFAULT_MODEL = "ism6564-w6-triage"          # created by ism6564-week06-export-to-ollama.ipynb
CODES = ["SHIP-DELAY", "RET-RMA", "BILL-DISP", "PROD-DEF", "ACCT-SEC", "PROD-INFO"]

# the SAME minimal prompt the adapter was trained with (Part A) -- the codes' meanings and the policy
# live in the weights now, so the prompt only names the fields
SYSTEM = ("You triage support tickets for Northwind Outfitters.\n"
          'Reply with JSON: {"route_to": one of ' + "|".join(CODES) +
          ', "urgency": low|normal|high, "needs_human": true|false, "order_id": string or ""}')


class Triage(BaseModel):
    """The contract (lecture Block 4): a hard guardrail. StrictBool rejects the text "no"."""
    route_to: Literal["SHIP-DELAY", "RET-RMA", "BILL-DISP", "PROD-DEF", "ACCT-SEC", "PROD-INFO"]
    urgency: Literal["low", "normal", "high"]
    needs_human: StrictBool
    order_id: str = Field(default="", pattern=r"^(NW-\d{5})?$")


def call_model(client: OpenAI, model: str, ticket: str) -> tuple[str, float, int]:
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model, temperature=0, max_tokens=80,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": f"<ticket>\n{ticket}\n</ticket>"}],
    )
    text = resp.choices[0].message.content or ""
    return text, time.time() - t0, (resp.usage.prompt_tokens if resp.usage else 0)


def check(raw: str) -> tuple[Triage | None, str]:
    """Never raises: (object, "") on success, (None, reason) otherwise."""
    m = re.search(r"\{.*?\}", raw, re.S)
    if not m:
        return None, "no JSON object in the reply"
    try:
        return Triage.model_validate_json(m.group(0)), ""
    except ValidationError as e:
        return None, "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors())


# ------------------------------------------------------------------------------------------- the page
st.set_page_config(page_title="Northwind triage", page_icon=":ticket:", layout="centered")
st.title("Northwind ticket triage")
st.caption("ISM 6564 · Week 6 workflow example · a fine-tuned Qwen2.5-0.5B served by Ollama on this machine")

with st.sidebar:
    st.header("Model")
    model = st.text_input("Ollama model", DEFAULT_MODEL)
    base_url = st.text_input("Ollama URL", OLLAMA_URL)
    st.markdown("Compare with the **un-tuned** base model: pull it once with "
                "`ollama pull qwen2.5:0.5b` and type `qwen2.5:0.5b` above.")

client = OpenAI(base_url=base_url, api_key="ollama")      # Ollama ignores the key; the client requires one

EXAMPLES = {
    "(type your own)": "",
    "Late parcel": "Order NW-40318 was due Monday and still hasn't arrived. I need it before Friday for a trip.",
    "Angry billing": "You charged my card twice for order NW-51002 and nobody answers the phone. This is unacceptable.",
    "Account takeover": "I got an email that my password was changed but I didn't do it. Someone is in my account.",
    "Product question": "Does the Ridgeline jacket run large? Thinking about a medium. No rush.",
}
pick = st.selectbox("Try a sample ticket", list(EXAMPLES))
ticket = st.text_area("Ticket", EXAMPLES[pick], height=140, placeholder="Paste a customer email here")

if st.button("Triage", type="primary", disabled=not ticket.strip()):
    try:
        raw, secs, in_tok = call_model(client, model, ticket.strip())
    except Exception as e:                       # Ollama not running, model not created, wrong name ...
        st.error(f"Could not reach the model: {e}")
        st.info("Is Ollama running (`ollama list`)? Did Part B create the model (`ollama create ...`)?")
        st.stop()

    obj, why = check(raw)
    left, right = st.columns([1.1, 0.9])
    with left:
        st.subheader("The object")
        if obj is None:
            # the hard guardrail: an invalid reply never reaches the rest of the system
            st.error(f"Reply failed the contract: {why}")
            st.warning("Routed to a person.  (This is the guardrail doing its job, not a crash.)")
        else:
            st.json(obj.model_dump())
            if obj.needs_human:
                st.warning("needs_human = true: a person is paged.")
            else:
                st.success(f"Queue {obj.route_to}, urgency {obj.urgency}.")
    with right:
        st.subheader("What the model wrote")
        st.code(raw or "(empty reply)", language="json")
        st.caption(f"{secs:.2f} s · {in_tok} prompt tokens · model `{model}`")

st.divider()
st.markdown(
    "**Read the result the way the lecture does.** *Valid* is not *right*: the contract check only says the "
    "object is well-formed. Whether the queue and the escalation flag are right is what Part A measured on "
    "held-out tickets. Facts the model cannot know (where the parcel is) are not in this object at all; "
    "that is Week 7."
)
