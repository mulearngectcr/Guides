# Building the Workflow

## Step 1: Create a New Workflow

Create a new workflow in n8n.

Add a **Manual Trigger** node.

Your workflow should currently look like:

```text
Manual Trigger
```

---

## Step 2: Add HTTP Request Node

Add an HTTP Request node.

Configuration:

```text
Method: GET
URL: https://zenquotes.io/api/random
```

Connect it to the Manual Trigger.

```text
Manual Trigger
      ↓
HTTP Request
```

Execute the node.

You should receive a response similar to:

```json
[
  {
    "q": "Success is not final, failure is not fatal.",
    "a": "Winston Churchill"
  }
]
```

---

## Step 3: Add an AI Agent

Add an AI Agent node.

Workflow:

```text
Manual Trigger
      ↓
HTTP Request
      ↓
AI Agent
```

---

## Step 4: Add a Chat Model

Inside the AI Agent, add a Chat Model.

Recommended Configuration:

```text
Provider: OpenAI
Model: gpt-4.1-nano
Credential: n8n free OpenAI API credits
```

---

## Step 5: Configure the Prompt

Use the following prompt:

```text
You are a personal growth coach.

Quote:
{{ $json.q }}

Author:
{{ $json.a }}

Explain the quote in simple language.

Give one real-life example relevant to college students.

Suggest one action the reader can take today.

End with a short motivational one-liner.
```

---

## Step 6: Test the AI Agent

Execute the AI Agent.

Verify that the output contains:

```text
Meaning
Example
Action Item
Motivation
```

Example:

```text
Meaning:
Success and failure are temporary.

Example:
Failing an exam doesn't define your future.

Action:
Spend 20 minutes improving a weak area.

Motivation:
Small improvements lead to big results.
```

---

## Step 7: Add Email Node

Add a Send Email node.

Workflow:

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

## Step 8: Configure the Email

Suggested Subject:

```text
AI Quote Coach
```

Suggested Body:

```text
🌟 AI Quote Coach

{{ $json.output }}

Generated At:
{{ $now }}
```

---

## Step 9: Execute the Workflow

Run the workflow.

Verify that:

```text
✓ Quote fetched successfully
✓ AI explanation generated
✓ Email delivered
```

Congratulations!

You have built your AI-powered workflow using n8n.
