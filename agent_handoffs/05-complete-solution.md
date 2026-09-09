# Part 5: Complete Solution

> Everything wired together

---

## 📖 Introduction

This part contains the full working implementation of the two-agent customer support system.

Both agents, all tools, the handoff logic, and the logging are combined here.

---

## 📋 Complete Code

```python
import os
import json
from groq import Groq
from google.colab import userdata

# ============================================================================
# SETUP
# ============================================================================

client = Groq(api_key=userdata.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


# ============================================================================
# PART 1: BILLING TOOLS (MOCK IMPLEMENTATIONS)
# ============================================================================

def get_invoice(user_id: str) -> dict:
    mock_invoices = {
        "u123": {
            "invoice_id": "INV-2024-001",
            "user_id": "u123",
            "amount": 99.00,
            "currency": "USD",
            "date": "2024-08-01",
            "status": "paid",
            "items": [
                {"description": "Pro Plan - August 2024", "amount": 49.00},
                {"description": "Pro Plan - August 2024 (duplicate)", "amount": 49.00},
                {"description": "Additional Storage 10GB", "amount": 1.00}
            ]
        },
        "u456": {
            "invoice_id": "INV-2024-002",
            "user_id": "u456",
            "amount": 49.00,
            "currency": "USD",
            "date": "2024-08-01",
            "status": "paid",
            "items": [
                {"description": "Pro Plan - August 2024", "amount": 49.00}
            ]
        }
    }
    if user_id not in mock_invoices:
        return {"error": f"No invoice found for user {user_id}"}
    return mock_invoices[user_id]


def process_refund(user_id: str, amount: float) -> dict:
    if amount <= 0:
        return {"error": "Refund amount must be greater than 0"}
    if amount > 500:
        return {"error": "Refund amount exceeds maximum limit of $500"}
    return {
        "refund_id": f"REF-{user_id}-001",
        "user_id": user_id,
        "amount_refunded": amount,
        "currency": "USD",
        "status": "approved",
        "estimated_days": 3,
        "message": f"Refund of ${amount:.2f} approved and will be processed within 3 business days."
    }


# ============================================================================
# PART 2: TOOL DEFINITIONS
# ============================================================================

BILLING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_invoice",
            "description": (
                "Retrieves the invoice and billing history for a specific user. "
                "Always call this before processing a refund."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique identifier of the user"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": (
                "Processes a refund for a specific user. "
                "Use only after reviewing the invoice with get_invoice."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The unique identifier of the user"
                    },
                    "amount": {
                        "type": "number",
                        "description": "The amount to refund in USD"
                    }
                },
                "required": ["user_id", "amount"]
            }
        }
    }
]


# ============================================================================
# PART 3: TOOL EXECUTION
# ============================================================================

def execute_billing_tool(tool_name: str, tool_args: dict) -> str:
    if tool_name == "get_invoice":
        result = get_invoice(tool_args["user_id"])
    elif tool_name == "process_refund":
        result = process_refund(tool_args["user_id"], tool_args["amount"])
    else:
        result = {"error": f"Unknown tool: {tool_name}"}
    return json.dumps(result)


# ============================================================================
# PART 4: INTENT CLASSIFIER
# ============================================================================

def classify_intent(query: str) -> str:
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
            {"role": "user", "content": query}
        ],
        temperature=0
    )
    intent = response.choices[0].message.content.strip().lower()
    return intent if intent in ["billing", "general"] else "general"


# ============================================================================
# PART 5: HANDOFF LOGGER
# ============================================================================

def log_handoff(triggered_by: str, reason: str, context: dict):
    print("\n" + "="*60)
    print("🔀 HANDOFF TRIGGERED")
    print("="*60)
    print(f"  Triggered by : {triggered_by}")
    print(f"  Reason       : {reason}")
    print(f"  User ID      : {context.get('user_id', 'N/A')}")
    print(f"  Query        : {context.get('original_query', 'N/A')}")
    print("="*60 + "\n")


# ============================================================================
# PART 6: GENERALIST AGENT
# ============================================================================

def generalist_agent(user_id: str, query: str) -> dict:
    print(f"\n🤖 Generalist Agent processing query...")

    intent = classify_intent(query)
    print(f"   Intent: {intent}")

    if intent == "billing":
        return {
            "action": "handoff",
            "handled_by": "generalist_agent",
            "handoff_reason": "billing intent detected",
            "context": {
                "user_id": user_id,
                "original_query": query
            }
        }

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful customer support agent for a SaaS product. "
                    "Answer the user's general questions clearly and concisely."
                )
            },
            {"role": "user", "content": query}
        ],
        temperature=0.7
    )

    return {
        "action": "respond",
        "handled_by": "generalist_agent",
        "response": response.choices[0].message.content
    }


# ============================================================================
# PART 7: BILLING SPECIALIST AGENT
# ============================================================================

def billing_specialist_agent(
    user_id: str,
    original_query: str,
    context: dict
) -> dict:
    print(f"\n💳 Billing Specialist Agent activated")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a billing specialist for a SaaS product. "
                "You handle refunds, invoices, and payment issues. "
                "Always check the invoice first before processing any refund. "
                "Be professional, empathetic, and resolve the issue completely."
            )
        },
        {
            "role": "user",
            "content": f"User ID: {user_id}\nQuery: {original_query}"
        }
    ]

    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=BILLING_TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in (message.tool_calls or [])
            ] or None
        })

        if not message.tool_calls:
            return {
                "handled_by": "billing_specialist",
                "handoff_reason": context.get("handoff_reason", "billing intent"),
                "response": message.content
            }

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"\n   🛠️  Tool called: {tool_name}")
            print(f"   Args: {tool_args}")

            result = execute_billing_tool(tool_name, tool_args)
            print(f"   Result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": result
            })

    return {
        "handled_by": "billing_specialist",
        "response": "Unable to resolve. Please contact support directly."
    }


# ============================================================================
# PART 8: MAIN HANDLER
# ============================================================================

def handle_query(user_id: str, query: str) -> dict:
    """
    Main entry point for all user queries.
    Users always enter here — never directly to specialists.

    Args:
        user_id: The user's ID
        query: The user's query

    Returns:
        Final response dict
    """
    print("\n" + "="*60)
    print(f"📩 New Query")
    print(f"   User ID : {user_id}")
    print(f"   Query   : {query}")
    print("="*60)

    handoff_done = False

    # Always start with Generalist
    result = generalist_agent(user_id, query)

    # Handle handoff if needed
    if result["action"] == "handoff" and not handoff_done:
        handoff_done = True

        log_handoff(
            triggered_by=result["handled_by"],
            reason=result["handoff_reason"],
            context=result["context"]
        )

        result = billing_specialist_agent(
            user_id=user_id,
            original_query=query,
            context=result["context"]
        )

    return {
        "handled_by": result.get("handled_by"),
        "handoff_reason": result.get("handoff_reason", "N/A — handled directly"),
        "response": result.get("response")
    }


# ============================================================================
# PART 9: TEST CASES
# ============================================================================

def run_tests():
    test_cases = [
        {
            "user_id": "u123",
            "query": "How do I reset my password?",
            "expected_handler": "generalist_agent"
        },
        {
            "user_id": "u123",
            "query": "I was charged twice this month, can I get a refund?",
            "expected_handler": "billing_specialist"
        },
        {
            "user_id": "u123",
            "query": "What features are included in the Pro plan?",
            "expected_handler": "generalist_agent"
        },
        {
            "user_id": "u456",
            "query": "My subscription renewal failed, what do I do?",
            "expected_handler": "billing_specialist"
        },
        {
            "user_id": "u123",
            "query": "I don't want a refund, just explain what I was charged for",
            "expected_handler": "billing_specialist"
        }
    ]

    print("\n" + "="*60)
    print("🧪 RUNNING TEST CASES")
    print("="*60)

    for i, test in enumerate(test_cases, 1):
        print(f"\n\n{'='*60}")
        print(f"TEST {i}")
        print(f"{'='*60}")

        result = handle_query(test["user_id"], test["query"])

        print(f"\n📋 FINAL RESULT")
        print(f"   Handled by    : {result['handled_by']}")
        print(f"   Handoff reason: {result['handoff_reason']}")
        print(f"   Response      : {result['response'][:200]}...")
        print(f"   Expected      : {test['expected_handler']}")
        print(f"   {'✅ PASS' if result['handled_by'] == test['expected_handler'] else '❌ FAIL'}")


run_tests()
```

---

## 🧪 Expected Output for Test 1

```
============================================================
📩 New Query
   User ID : u123
   Query   : How do I reset my password?
============================================================

🤖 Generalist Agent processing query...
   Intent: general

📋 FINAL RESULT
   Handled by    : generalist_agent
   Handoff reason: N/A — handled directly
   Response      : To reset your password, go to the login page and click...
   Expected      : generalist_agent
   ✅ PASS
```

---

## 🧪 Expected Output for Test 2

```
============================================================
📩 New Query
   User ID : u123
   Query   : I was charged twice this month, can I get a refund?
============================================================

🤖 Generalist Agent processing query...
   Intent: billing

============================================================
🔀 HANDOFF TRIGGERED
============================================================
  Triggered by : generalist_agent
  Reason       : billing intent detected
  User ID      : u123
  Query        : I was charged twice this month, can I get a refund?
============================================================

💳 Billing Specialist Agent activated

   🛠️  Tool called: get_invoice
   Args: {'user_id': 'u123'}
   Result: {"invoice_id": "INV-2024-001", "amount": 99.00, ...}

   🛠️  Tool called: process_refund
   Args: {'user_id': 'u123', 'amount': 49.0}
   Result: {"refund_id": "REF-u123-001", "status": "approved", ...}

📋 FINAL RESULT
   Handled by    : billing_specialist
   Handoff reason: billing intent detected
   Response      : I've reviewed your invoice and can confirm a duplicate charge...
   Expected      : billing_specialist
   ✅ PASS
```

---

## 🌟 Bonus Challenges

### Bonus 1: Add a Technical Support Specialist

```python
def technical_specialist_agent(user_id: str, original_query: str, context: dict) -> dict:
    """
    Handles bug reports and technical issues.
    Has tools like create_support_ticket() and check_system_status().
    """
    # Add create_ticket and check_status mock tools
    # Wire this into classify_intent() with a third category: "technical"
    pass
```

### Bonus 2: Billing Specialist Hands Back

If the specialist determines the query isn't actually billing-related:

```python
# Inside billing_specialist_agent, after get_invoice:
if not_billing_issue:
    return {
        "action": "handoff_back",
        "reason": "not a billing issue after review",
        "context": context
    }

# In handle_query, handle this case:
if result.get("action") == "handoff_back":
    result = generalist_agent(user_id, query)
```

---

## ✅ Submission Checklist

- [ ] Generalist Agent classifies intent using LLM (not keywords)
- [ ] Billing intent triggers a handoff with context
- [ ] Handoff is logged with triggered_by, reason, user_id, and query
- [ ] Billing Specialist calls `get_invoice` before `process_refund`
- [ ] Only one handoff per query (no ping-ponging)
- [ ] Billing Specialist is unreachable directly by users
- [ ] All 5 test cases run without errors
- [ ] Colab notebook shared with "Anyone with the link can view"

---

## 📚 Additional Resources

- Groq API docs: https://console.groq.com/docs
- Groq Function Calling: https://console.groq.com/docs/tool-use
- Multi-agent design patterns: https://www.anthropic.com/engineering/building-effective-agents
