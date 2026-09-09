# Part 3: Building the Generalist Agent

> The first point of contact — routes or resolves

---

## 📖 Introduction

The Generalist Agent is the entry point for every user query.

It has two responsibilities:

1. **Answer directly** if the query is general/how-to
2. **Hand off** if the query is billing-related

It does not have billing tools. It has one job per query: resolve or route.

---

## 🚀 Setup

```python
import os
import json
from groq import Groq
from google.colab import userdata

client = Groq(api_key=userdata.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"
```

---

## 🛠️ Step 1: The Intent Classifier

```python
def classify_intent(query: str) -> str:
    """
    Classifies the user query as 'billing' or 'general'
    using an LLM call.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intent classifier for a SaaS support system.\n\n"
                    "Classify the query as either 'billing' or 'general'.\n\n"
                    "Billing: refunds, invoices, charges, subscription changes, "
                    "payment failures, pricing.\n\n"
                    "General: how-to, feature questions, account settings, "
                    "product usage, password reset.\n\n"
                    "Reply with ONLY one word: 'billing' or 'general'."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0
    )

    intent = response.choices[0].message.content.strip().lower()
    return intent if intent in ["billing", "general"] else "general"
```

**Note on `temperature=0`:** Classification should be deterministic. Setting temperature to 0 removes randomness — the same input always produces the same output. This is important for routing logic.

---

## 🛠️ Step 2: Answering General Queries

```python
def answer_general_query(query: str) -> str:
    """
    Uses the LLM to answer a general/how-to query directly.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful customer support agent for a SaaS product. "
                    "Answer the user's general questions clearly and concisely. "
                    "If you don't know the answer, say so honestly."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
```

---

## 🛠️ Step 3: The Generalist Agent

```python
def generalist_agent(user_id: str, query: str) -> dict:
    """
    The Generalist Agent.
    - Answers general queries directly.
    - Returns a handoff signal for billing queries.

    Args:
        user_id: The user's ID
        query: The user's query

    Returns:
        dict with 'action' key:
          - action = "respond" → includes 'response' key
          - action = "handoff" → includes 'handoff_reason' and 'context' keys
    """

    print(f"\n🤖 Generalist Agent processing: '{query}'")

    # Step 1: Classify intent
    intent = classify_intent(query)
    print(f"   Intent classified as: {intent}")

    # Step 2: Route based on intent
    if intent == "billing":
        print("   → Billing intent detected. Preparing handoff.")

        return {
            "action": "handoff",
            "handled_by": "generalist_agent",
            "handoff_reason": "billing intent detected",
            "context": {
                "user_id": user_id,
                "original_query": query
            }
        }

    # Step 3: Answer general query directly
    print("   → General query. Answering directly.")
    response = answer_general_query(query)

    return {
        "action": "respond",
        "handled_by": "generalist_agent",
        "response": response
    }
```

---

## 🧪 Testing the Generalist Agent Alone

Before connecting to the Billing Specialist, test the Generalist in isolation:

```python
# Test 1: Should answer directly
result = generalist_agent("u123", "How do I reset my password?")
print(result)
# Expected: action = "respond", response = "..."

# Test 2: Should trigger handoff
result = generalist_agent("u123", "I was charged twice this month")
print(result)
# Expected: action = "handoff", handoff_reason = "billing intent detected"

# Test 3: Edge case — billing mentioned but general intent
result = generalist_agent("u123", "I don't want a refund, just explain my plan features")
print(result)
# Expected: action = "respond" (LLM understands this is general)
```

---

## 📌 Key Takeaways

- The Generalist Agent classifies intent with `temperature=0` for consistency
- It never has billing tools — only routes or answers
- It returns a structured dict: `action = "respond"` or `action = "handoff"`
- Test it in isolation before connecting the full system

---

## 🎓 Next Steps

→ Continue to [Part 4: Building the Billing Specialist Agent](04-building-the-billing-specialist.md)
