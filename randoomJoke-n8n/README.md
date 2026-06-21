# 📌 Day 8 Task – Building with n8n

Welcome to Day 8!

Today you'll build a **Random Joke Generator Workflow** using n8n.

By the end of this task, you'll learn:

- How workflows work in n8n
- How to fetch data from an API
- How to use data from one node in another node
- How to send emails automatically
- How to use expressions
- Basic workflow debugging
- Error handling concepts

---

# Final Workflow

```text
Manual Trigger
      ↓
HTTP Request
      ↓
Send Email
```

---

# API Used

```text
https://official-joke-api.appspot.com/random_joke
```

Sample response:

```json
{
  "type": "general",
  "setup": "Why don't scientists trust atoms?",
  "punchline": "Because they make up everything!",
  "id": 123
}
```

---

# Task Requirements

## Mandatory

- Create a Manual Trigger node
- Fetch a random joke from the API
- Send the joke to an email address
- Verify that each execution returns a different joke

---

## Challenge Requirements

- Format the joke properly
- Include setup and punchline separately
- Add a timestamp
- Handle API failures

---

## Bonus

⭐ Fetch another joke if the first one is too short

⭐ Use an IF node to filter jokes

⭐ Customize email subject dynamically

---

# Repository Structure

```text
.
├── README.md
├── Part-1-Understanding-The-Workflow.md
├── Part-2-Building-The-Workflow.md
└── Part-3-Challenges-And-Bonus.md
```

Follow the files in order.

Good luck!
