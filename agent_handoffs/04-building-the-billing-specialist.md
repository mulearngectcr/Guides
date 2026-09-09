# Part 4: Building the Billing Specialist Agent

> Domain expert with real tools

---

## 📖 Introduction

The Billing Specialist Agent is only reached via handoff.

It has two tools:
- `get_invoice(user_id)` — retrieves the user's invoice
- `process_refund(user_id, amount)` — processes a refund

It uses these tools to resolve the billing query and return a response.

---

## 🛠️ Step 1: The Billing Tools

These are mock implementations — they return fake data for learning purposes.

```python
def get_invoice(user_id: str) -> dict:
    """
    Retrieves the invoice for a given user.
    Mock implementation — returns fake invoice data.

    Args:
        user_id: The user's ID

    Returns:
        dict with invoice details
    """
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
    """
    Processes a refund for a given user.
    Mock implementation — simulates refund processing.

    Args:
        user_id: The user's ID
        amount: Amount to refund in USD

    Returns:
        dict with refund confirmation
    """
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
```

---

## 🛠️ Step 2: Tool Definitions for the LLM

```python
BILLING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_invoice",
            "description": (
                "Retrieves the invoice and billing history for a specific user. "
                "Use this to check what the user was charged, when, and for what. "
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
                "Use this only after reviewing the invoice with get_invoice. "
                "Requires the user ID and the exact amount to refund."
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
```

---

## 🛠️ Step 3: Tool Execution

```python
def execute_billing_tool(tool_name: str, tool_args: dict) -> str:
    """
    Executes a billing tool and returns the result as a string.
    """
    if tool_name == "get_invoice":
        result = get_invoice(tool_args["user_id"])
    elif tool_name == "process_refund":
        result = process_refund(
            tool_args["user_id"],
            tool_args["amount"]
        )
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return json.dumps(result)
```

---

## 🛠️ Step 4: The Billing Specialist Agent

```python
def billing_specialist_agent(
    user_id: str,
    original_query: str,
    context: dict
) -> dict:
    """
    The Billing Specialist Agent.
    Only reachable via handoff from the Generalist Agent.
    Has access to get_invoice and process_refund tools.

    Args:
        user_id: The user's ID
        original_query: The user's original query
        context: Context passed from the Generalist Agent

    Returns:
        dict with the final response
    """

    print(f"\n💳 Billing Specialist Agent activated")
    print(f"   User ID: {user_id}")
    print(f"   Query  : {original_query}")

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
            "content": (
                f"User ID: {user_id}\n"
                f"Query: {original_query}"
            )
        }
    ]

    # Tool calling loop
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

        # Add assistant message to history
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

        # No tool calls — final response reached
        if not message.tool_calls:
            final_response = message.content
            print(f"\n✅ Billing Specialist resolved query.")
            return {
                "handled_by": "billing_specialist",
                "handoff_reason": context.get("handoff_reason", "billing intent"),
                "response": final_response
            }

        # Process tool calls
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
        "response": "I was unable to resolve your billing issue. Please contact support."
    }
```

---

## 🧪 Testing the Billing Specialist Alone

Test it in isolation before connecting to the full system:

```python
# Simulate a handoff context
test_context = {
    "handoff_reason": "billing/refund intent detected",
    "original_query": "I was charged twice this month, can I get a refund?"
}

result = billing_specialist_agent(
    user_id="u123",
    original_query="I was charged twice this month, can I get a refund?",
    context=test_context
)

print(result)
```

**Expected flow:**

```
💳 Billing Specialist Agent activated
   User ID: u123
   Query  : I was charged twice this month, can I get a refund?

   🛠️  Tool called: get_invoice
   Args: {'user_id': 'u123'}
   Result: {"invoice_id": "INV-2024-001", ...}

   🛠️  Tool called: process_refund
   Args: {'user_id': 'u123', 'amount': 49.0}
   Result: {"refund_id": "REF-u123-001", "status": "approved", ...}

✅ Billing Specialist resolved query.
```

---

## 📌 Key Takeaways

- Billing tools are mocked — they return fake data that looks realistic
- Tool definitions must match function signatures exactly
- The specialist always calls `get_invoice` before `process_refund`
- The agent loops until no more tool calls are needed
- Test in isolation before wiring to the full system

---

## 🎓 Next Steps

→ Continue to [Part 5: Complete Solution](05-complete-solution.md)
