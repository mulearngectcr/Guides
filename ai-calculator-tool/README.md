# Month 3 Sprint A — Build Your First AI Tool: Calculator

A comprehensive guide to understanding and building function calling for LLMs.

---

## 📌 Task Overview

In this task, you will build a **calculator tool** that an LLM can use to perform mathematical calculations. This is your first step into understanding how LLMs interact with external tools.

**What you'll learn:**

- What function calling is and why it matters
- How LLMs decide when to use tools
- How to define and execute tools for an LLM
- How to handle tool results and communicate them back

---

## 📂 Guide Structure

1. **[01 - Understanding Function Calling](01.Understanding-Function-Calling.md)**
   - What is function calling?
   - Why LLMs need external tools
   - Real-world examples

2. **[02 - How LLMs Interact with Tools](02.How-LLMs-Interact-with-Tools.md)**
   - The function calling workflow
   - Tool definitions and parameters
   - Tool schemas and APIs

3. **[03 - Building Your Calculator Tool](03.Building-Your-Calculator-Tool.md)**
   - Project setup
   - Implementing the calculator
   - Defining the tool for the LLM
   - Executing tools step by step

4. **[04 - Complete Working Solution](04.Complete-Solution.md)**
   - Full code example with explanations
   - Testing your calculator
   - Handling edge cases
   - Bonus features

---

## 📋 Requirements

- Python 3.8+
- Access to an LLM API that supports function calling (OpenAI, Groq, etc.)
- Google Colab (recommended for submission)
- Basic Python knowledge

---

## 🎯 Expected Outcome

By the end of this guide, your calculator will work like this:

```
You: What is 18% of 2500?

🛠️  Tool called: calculator
   📊 Expression: 2500 * 0.18
   ✓ Result: 450

Bot: 18% of 2500 is 450.
```

---

## ⏰ Deadline

**4 September, 11:30 PM**

Start with Part 1 to understand the fundamentals!
