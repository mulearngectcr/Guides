# Part 1: What is a Multi-Agent System?

> From one agent to many — and why it matters

---

## 📖 Introduction

In Task 1, you built a single agent with one tool.

In Task 2, you gave that agent multiple tools and let it choose between them.

But what happens when a single agent isn't enough?

What if different kinds of queries need completely different expertise?

That's where **multi-agent systems** come in.

---

## 🤔 What is a Multi-Agent System?

A multi-agent system is a setup where **multiple AI agents work together**, each with its own role, tools, and specialisation.

Instead of one agent trying to handle everything:

```
User Query
    │
    ▼
One Agent (tries to do everything)
    │
    ▼
Response
```

You have a team of agents with defined responsibilities:

```
User Query
    │
    ▼
Generalist Agent (handles general queries)
    │
    ├── Can handle this? → Responds directly
    │
    └── Out of lane? → Hands off to Specialist
                            │
                            ▼
                    Specialist Agent
                    (handles specific domain)
                            │
                            ▼
                        Response
```

---

## 🌍 Real-World Examples

### Example 1: Customer Support at a Bank

**Without multi-agent:**

```
User: "I want to dispute a transaction"
Single Agent: Tries to handle everything — account info, disputes,
              refunds, technical issues — gets confused, gives
              wrong answers, or has no tools for the job.
```

**With multi-agent:**

```
User: "I want to dispute a transaction"
Generalist Agent: This is a billing dispute. Handing off to
                  Billing Specialist.
Billing Specialist: Has get_invoice() and process_refund() tools.
                    Resolves the issue correctly.
```

---

### Example 2: Hospital Triage System

```
Patient comes in with a complaint.

Triage Agent (Generalist):
  → "Chest pain" → Cardiology Specialist
  → "Broken arm" → Orthopaedics Specialist
  → "Prescription refill" → Handles directly

Each specialist has the right tools and knowledge for their domain.
```

---

### Example 3: Software Company Support Bot

```
User: "I can't log in"
Generalist: This is a technical issue → Technical Support Agent

User: "My invoice is wrong"
Generalist: This is a billing issue → Billing Agent

User: "How do I export a CSV?"
Generalist: General how-to → Answers directly
```

---

## 🤖 Chatbot vs Single Agent vs Multi-Agent

| Type | What it does | Limitation |
|---|---|---|
| Chatbot | One prompt in, one response out | No tools, no memory, no loop |
| Single Agent | Has tools, decides which to use, loops until done | One agent handles all domains |
| Multi-Agent | Multiple agents, each with their own tools, hand off to each other | More complex to build, but far more powerful |

---

## 🎯 What We're Building in Task 3

You are building a **two-agent customer support system** for a fictional SaaS product.

```
User sends a query
        │
        ▼
Generalist Agent
  ├── General/how-to query → Answers directly
  └── Billing-related query → Handoff to Billing Specialist
                                      │
                                      ▼
                              Billing Specialist
                              ├── get_invoice(user_id)
                              └── process_refund(user_id, amount)
                                      │
                                      ▼
                                   Response
```

**Generalist Agent:**
- Answers general questions about the product
- Detects billing intent using the LLM (not keyword matching)
- Hands off with context when needed

**Billing Specialist Agent:**
- Only reachable via handoff — not directly by the user
- Has two billing tools: `get_invoice` and `process_refund`
- Resolves the query and responds

---

## 📌 Key Concepts

### Agent

An agent is an LLM + tools + a loop. It observes input, decides what to do, acts, checks the result, and repeats until the task is done.

### Handoff

A handoff is when one agent decides it's outside its lane and passes the conversation — along with all relevant context — to another agent.

### Routing

Routing is the logic that decides which agent should handle a given query. In our system, the Generalist Agent handles routing.

### Context Passing

When handing off, the receiving agent needs to know:
- What the user originally asked
- Who the user is
- What the previous agent already found out

Without context, the specialist starts from scratch — which is a bad user experience.

---

## 📌 Key Takeaways

- Multi-agent systems divide responsibility between specialised agents
- Each agent has its own tools and domain
- A generalist agent typically handles routing and simple queries
- Specialist agents handle complex domain-specific tasks
- Handoffs pass context so the specialist doesn't start from scratch

---

## 🎓 Next Steps

→ Continue to [Part 2: Handoff Logic and Routing](02-handoff-logic-and-routing.md)
