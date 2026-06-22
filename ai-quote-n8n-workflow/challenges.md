# Part 3 — Challenges, Error Handling & Bonus

Now let's improve the workflow.

---

# Challenge 1 — Better Email Formatting

Instead of sending only the AI response, create a structured email.

Example:

```text
🌟 AI Quote Coach

Quote:
"The best way to predict the future is to create it."

Author:
Peter Drucker

AI Explanation:
...

Action Item:
...

Motivation:
...

Generated At:
{{$now}}
```

Much more readable.

---

# Challenge 2 — Error Handling

External APIs can fail.

Possible reasons:

* Network issues
* API downtime
* Invalid URL
* Rate limits

---

# Using Error Handling

Enable:

```text
Continue On Fail
```

inside the HTTP Request node.

If the API fails:

* workflow should not crash
* execution should continue
* user should receive a meaningful notification

---

# Example Error Email

Subject:

```text
AI Quote Coach Failed
```

Body:

```text
Unable to fetch quote.

Please try again later.

Time:
{{$now}}
```

---

# Challenge 3 — Include Quote Author

The ZenQuotes API provides both:

```text
q → Quote
a → Author
```

Make sure both are included in the AI prompt and final email.

Example:

```text
Quote:
Success is not final, failure is not fatal.

Author:
Winston Churchill
```

---

# Bonus 1 — Dynamic Email Subject

Add a Set node.

Workflow:

```text
AI Agent
      ↓
Set
      ↓
Email
```

Create field:

```text
subject
```

Value:

```text
Daily Inspiration - {{$now}}
```

Use it in the Email Subject:

```text
{{$json.subject}}
```

---

# Bonus 2 — Save Responses to Google Sheets

Workflow:

```text
Manual Trigger
      ↓
HTTP Request
      ↓
AI Agent
      ↓
Google Sheets
      ↓
Email
```

Suggested Columns:

```text
Date
Quote
Author
Explanation
Action Item
Motivation
```

This creates your own AI quote journal.

---

# Bonus 3 — IF Node

Add:

```text
AI Agent
      ↓
      IF
```

Purpose:

Check whether the AI response is long enough.

Example Condition:

```text
{{$json.text.length}}
```

Greater than:

```text
100
```

If TRUE:

```text
Send Email
```

If FALSE:

```text
Generate Again
```

---

# Bonus 4 — Send to Telegram

Instead of Email:

```text
AI Agent
      ↓
Telegram
```

Send the generated response directly to a Telegram chat.

---

# Bonus 5 — Send to Discord

Use a Discord Webhook.

Workflow:

```text
AI Agent
      ↓
HTTP Request
```

Send the output to a Discord channel.

---

# Bonus 6 — Daily Motivation Bot

Replace:

```text
Manual Trigger
```

with:

```text
Schedule Trigger
```

Configure:

```text
Every Day
8:00 AM
```

Workflow:

```text
Schedule Trigger
      ↓
HTTP Request
      ↓
AI Agent
      ↓
Email
```

Now you'll receive an AI-generated motivational quote every morning.

---

# Bonus 7 — AI Generated Subject Line

Instead of creating a fixed subject, ask the AI to generate one.

Example:

```text
🚀 Today's Lesson on Success
```

or

```text
🌟 Your Daily Dose of Motivation
```

Use the generated text as the email subject.

---

# Submission Checklist

Before submitting:

✅ Workflow executes successfully

✅ Quote fetched successfully

✅ AI explanation generated

✅ Email received

✅ Author included

✅ Screenshots taken

✅ Workflow exported

✅ Files pushed to GitHub repository


Congratulations on completing Day 9 🚀
