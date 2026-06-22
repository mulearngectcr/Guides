# Understanding the Workflow

## Goal

The goal of this workflow is to learn how AI can be integrated into automation.

Instead of simply forwarding API data, we'll ask an AI model to process and improve it.

---

# Final Workflow

```text
Manual Trigger
      ↓
HTTP Request
      ↓
AI Agent
      ↓
Send Email
```

---

# Step 1: Manual Trigger

This node starts the workflow manually whenever you click **Execute Workflow**.

---

# Step 2: HTTP Request

We'll fetch a random quote from:

```text
https://zenquotes.io/api/random
```

Example response:

```json
[
  {
    "q": "Success is not final, failure is not fatal.",
    "a": "Winston Churchill"
  }
]
```

Where:

```text
q → Quote
a → Author
```

---

# Step 3: AI Agent

The quote will be sent to an AI model.

The AI should:

- Explain the quote in simple language
- Give a real-life example relevant to students
- Suggest one action item
- End with a motivational one-liner

Example:

```text
Meaning:
Success and failure are both temporary.

Example:
A student may fail one exam but still become successful through consistency.

Action:
Spend 20 minutes today improving a skill.

Motivation:
Progress matters more than perfection.
```

---

# Step 4: Send Email

The generated response is emailed to you.

This demonstrates how AI can be inserted into a real automation pipeline.

