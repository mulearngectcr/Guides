# 📌 Day 9 Task – Building with n8n + AI

Welcome to Day 9!

Today you'll build an **AI Quote Coach Workflow** using n8n.

By the end of this task, you'll learn:

* How to integrate AI into workflows
* How to use Large Language Models (LLMs) in n8n
* How to fetch data from an API
* How to pass data between nodes
* Basic prompt engineering
* How to generate dynamic AI-powered content
* How to automate email delivery
* Error handling concepts

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

# API Used

```text
https://zenquotes.io/api/random
```

Sample Response:

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

# AI Model

Recommended Configuration:

```text
Provider: OpenAI
Model: gpt-4.1-mini
Credential: n8n free OpenAI API credits
```

You may use other supported models if preferred.

---

# What the AI Should Do

The AI receives a quote and should:

* Explain the quote in simple language
* Give a real-life example relevant to students
* Suggest one action item
* End with a motivational one-liner

Example:

```text
Quote:
Success is not final, failure is not fatal.

Meaning:
Success and failure are both temporary.

Example:
A student who fails one exam can still achieve their goals through consistent effort.

Action:
Spend 20 minutes today improving a weak skill.

Motivation:
Small improvements every day create extraordinary results.
```

---

# Task Requirements

## Mandatory

* Create a Manual Trigger node
* Fetch a random quote using the API
* Pass the quote to an AI Agent
* Generate a meaningful AI response
* Send the generated response via email
* Verify that each execution produces a different quote

---

## Challenge Requirements

* Format the email neatly
* Include the quote author
* Add a timestamp
* Handle API failures gracefully

---

## Bonus

⭐ Generate a dynamic email subject

⭐ Save responses to Google Sheets

⭐ Use an IF node to validate AI responses

⭐ Send the output to Telegram or Discord

⭐ Schedule the workflow to run automatically every morning

---

# Repository Structure

```text
.
├── README.md
├── 1.Understanding-the-workflow.md
├── 2.Building-the-workflow.md
└── 3.Challenges.md
```

Follow the files in order.

Good luck and happy building! 🚀
