# Task 1 — Agent Handoff

## OpenClaw Student Guide

> **Goal:** Build a simple AI Study Assistant using OpenClaw where one agent teaches a concept and another agent creates a quiz from that explanation.

---

# 1. What are we building?

You will build a small multi-agent system:

```text
User
  │
  ▼
Orchestrator
  │
  ▼
Teacher Agent
  │
  │ Explanation
  ▼
Orchestrator
  │
  │ Explanation + Context
  ▼
Quiz Agent
  │
  ▼
Quiz
```

For example, the user asks:

```text
Explain binary search.
```

The system should:

1. Send the question to the **Teacher Agent**
2. Get an explanation
3. Pass that explanation to the **Quiz Agent**
4. Generate 3 questions
5. Return the quiz

The important concept is the **handoff**.

---

# 2. What is OpenClaw?

OpenClaw is an agent runtime.

Instead of writing:

```python
teacher()
quiz()
```

and manually managing everything yourself, OpenClaw provides the infrastructure for agents.

An agent can have:

- Its own workspace
- Its own instructions
- Its own configuration
- Its own session/context
- Access to tools
- The ability to delegate work to other agents

Think of an agent as a specialized worker.

For example:

```text
Teacher Agent
    ↓
"I explain things"

Quiz Agent
    ↓
"I create quizzes"

Reviewer Agent
    ↓
"I check quizzes"
```

The orchestrator decides **which agent should do what and what information should be passed between them**.

---

# 3. Prerequisites

You need:

- OpenClaw installed
- A configured LLM provider/API key
- A terminal
- Basic familiarity with the command line

Check whether OpenClaw is installed:

```bash
openclaw --version
```

If that works, continue.

---

# 4. Initial OpenClaw Setup

Run:

```bash
openclaw setup
```

Follow the setup process and configure your model/provider.

After setup, verify that OpenClaw works:

```bash
openclaw
```

You should be able to interact with your default agent.

Exit when you're done testing.

---

# 5. Understanding Agents

Before creating our application, understand this distinction:

A normal program might look like:

```text
function teacher()
function quiz()
function reviewer()
```

With OpenClaw, these can instead be independent agents:

```text
Teacher Agent
Quiz Agent
Reviewer Agent
```

Each agent can have its own workspace and instructions.

This allows you to specialize agents for different tasks.

---

# 6. Create the Teacher Agent

Create a new agent:

```bash
openclaw agents add teacher
```

Then check your agents:

```bash
openclaw agents list
```

You should see your new agent.

You will eventually have something similar to:

```text
main
teacher
```

---

# 7. Configure the Teacher Agent

Each agent has a workspace containing files that provide context and instructions.

Find the workspace created for your Teacher Agent.

Inside that workspace, create/edit:

```text
AGENTS.md
```

Add:

```md
# Teacher Agent

You are the Teacher Agent in an AI Study Assistant.

Your responsibility is to explain concepts clearly to students.

Rules:

1. Explain the concept accurately.
2. Keep explanations beginner-friendly.
3. Use examples when useful.
4. Focus only on teaching.
5. Do not generate quiz questions.
6. Return a clear explanation that another agent can use.
```

### Why are we doing this?

We are giving the agent a **role**.

Instead of saying:

> "You are an AI. Do everything."

we tell it:

> "You are the Teacher. Your job is explaining concepts."

This is one of the fundamental ideas behind multi-agent systems:

**specialization.**

---

# 8. Test the Teacher Agent

Run the Teacher Agent.

For example:

```bash
openclaw agent --agent teacher
```

Ask:

```text
Explain binary search.
```

You should get an explanation similar to:

```text
Binary search is a searching algorithm that works on
sorted data. It repeatedly checks the middle element...
```

The exact response will depend on the model.

The important thing is that the agent is behaving as a **Teacher**, not as a general-purpose assistant.

---

# 9. Create the Quiz Agent

Now create another agent:

```bash
openclaw agents add quiz
```

Check:

```bash
openclaw agents list
```

You should now have something similar to:

```text
main
teacher
quiz
```

---

# 10. Configure the Quiz Agent

Open the Quiz Agent's workspace.

Create/edit:

```text
AGENTS.md
```

Add:

```md
# Quiz Agent

You are the Quiz Agent in an AI Study Assistant.

Your responsibility is to create a quiz from an explanation
provided by the Teacher Agent.

Rules:

1. Create exactly 3 questions.
2. Base every question on the provided explanation.
3. Include an answer for every question.
4. Do not introduce unrelated concepts.
5. Do not explain the original concept again.
6. Return a clearly formatted quiz.
```

Notice that this agent has a completely different responsibility.

```text
Teacher
→ Explain

Quiz
→ Ask questions
```

---

# 11. Test the Quiz Agent

Run:

```bash
openclaw agent --agent quiz
```

Give it an explanation such as:

```text
Create a quiz from this explanation:

Binary search is an algorithm that searches a sorted
array by repeatedly checking the middle element.
If the target is smaller than the middle element,
the search continues in the left half. Otherwise,
it continues in the right half.
```

It should produce something like:

```text
1. What type of array does binary search require?
Answer: A sorted array.

2. Which element does binary search check?
Answer: The middle element.

3. What happens if the target is smaller than the middle element?
Answer: The search continues in the left half.
```

---

# 12. Now Understand the Handoff

So far we have two independent agents:

```text
Teacher Agent

Question
   ↓
Explanation
```

and:

```text
Quiz Agent

Explanation
   ↓
Quiz
```

But we haven't connected them yet.

That's what a **handoff** does.

A handoff means:

> One agent completes its work, and another agent receives the relevant result as context.

The flow becomes:

```text
Question
   │
   ▼
Teacher
   │
   │ explanation
   ▼
Quiz
   │
   ▼
Quiz
```

The Quiz Agent should not independently answer the original question.

It should receive the Teacher's explanation.

---

# 13. What is the Orchestrator?

The **orchestrator** controls the workflow.

It decides:

```text
Who should run?
What should they receive?
What happens next?
```

For this task:

```text
User
 │
 ▼
Orchestrator
 │
 ├──→ Teacher Agent
 │
 │    returns explanation
 │
 ▼
Orchestrator
 │
 ├──→ Quiz Agent
 │      receives explanation
 │
 ▼
Quiz
```

The orchestrator is therefore responsible for the movement of information.

---

# 14. Delegating Work in OpenClaw

OpenClaw supports sub-agent delegation.

An agent can delegate a task to another agent and receive the result back.

Conceptually:

```text
Main Agent
    │
    │ delegate
    ▼
Teacher Agent
    │
    │ result
    ▼
Main Agent
```

Then:

```text
Main Agent
    │
    │ delegate + context
    ▼
Quiz Agent
    │
    │ result
    ▼
Main Agent
```

This is what we will use for our handoff.

---

# 15. Configure the Orchestrator

The main/default agent will act as the orchestrator.

Find its workspace and edit:

```text
AGENTS.md
```

Add instructions similar to:

```md
# Study Assistant Orchestrator

You are the orchestrator for an AI Study Assistant.

When a user asks to learn a concept:

1. Delegate the explanation task to the Teacher Agent.
2. Wait for the Teacher Agent's result.
3. Take the complete explanation returned by the Teacher Agent.
4. Delegate the quiz task to the Quiz Agent.
5. Pass the Teacher Agent's explanation as context.
6. Return the Quiz Agent's result to the user.

Always clearly report the handoff.

Example:

[Orchestrator] Starting Teacher Agent...

[Teacher Agent] Running...

[Orchestrator] Teacher Agent completed.

[Handoff] Teacher Agent -> Quiz Agent

[Quiz Agent] Running...

[Orchestrator] Quiz Agent completed.
```

Do not blindly copy this and assume it is finished.

You need to determine how your current OpenClaw version should perform the delegation.

Use:

```bash
openclaw --help
```

and:

```bash
openclaw agent --help
```

to inspect the available commands and options.

You can also inspect the OpenClaw documentation for sub-agents.

---

# 16. The Important Part — Passing Context

Suppose the user asks:

```text
Explain binary search.
```

The Teacher Agent produces:

```text
Binary search is an algorithm that works on sorted arrays...
```

The orchestrator now needs to pass that result to the Quiz Agent.

Conceptually, the next request should contain:

```text
Create 3 questions based on this explanation:

Binary search is an algorithm that works on sorted arrays...
```

This is the actual handoff.

The Quiz Agent should receive the **Teacher Agent's output**, not just:

```text
Explain binary search
```

This distinction matters.

---

# 17. Complete Workflow

Your final system should behave approximately like this:

```text
User:
Explain binary search.


[Orchestrator]
Starting Teacher Agent...


[Teacher Agent]
Running...


[Teacher Agent]
Binary search is an algorithm...


[Orchestrator]
Teacher Agent completed.

[Handoff]
Teacher Agent → Quiz Agent

Passing Teacher Agent's explanation...


[Quiz Agent]
Running...


[Quiz Agent]
1. What type of array does binary search require?
2. What element is checked first?
3. What is the time complexity?


[Orchestrator]
Quiz Agent completed.


User receives final quiz.
```

---

# 18. Important: Don't Hardcode the Explanation

Avoid doing this:

```text
Teacher Agent → Quiz Agent

"Binary search is..."
```

with the explanation manually written by you.

The point of the task is that:

```text
Teacher output
       ↓
   automatically
       ↓
Quiz input
```

The explanation should come from the actual Teacher Agent execution.

---

# 19. Logging the Handoff

Your system should make the handoff visible.

For example:

```text
[Teacher Agent] Running...

[Teacher Agent] Finished.

[Handoff]
From: Teacher Agent
To: Quiz Agent

Context:
<teacher's explanation>

[Quiz Agent] Running...

[Quiz Agent] Finished.
```

This makes it easy to demonstrate that context actually moved between agents.

---

# 20. Test Different Questions

Don't test only:

```text
Explain binary search.
```

Try:

```text
Explain recursion.
```

```text
Explain HTTP requests.
```

```text
Explain binary trees.
```

```text
Explain Git branches.
```

For each one, verify:

```text
Question
   ↓
Teacher explanation
   ↓
Same explanation passed to Quiz
   ↓
Relevant questions generated
```

---

# 21. Common Mistakes

### Mistake 1 — One agent does everything

If your main agent simply explains the concept and creates the quiz itself, you haven't implemented the intended architecture.

You should have:

```text
Teacher Agent
Quiz Agent
```

with separate responsibilities.

---

### Mistake 2 — Quiz Agent doesn't receive Teacher output

This:

```text
User
 │
 ├──→ Teacher
 │
 └──→ Quiz
```

is not the intended handoff.

Instead:

```text
User
 │
 ▼
Teacher
 │
 │ output
 ▼
Quiz
```

---

### Mistake 3 — Passing only the original question

Don't do:

```text
Teacher:
"Explain binary search"

Quiz:
"Explain binary search"
```

The Quiz Agent should receive the explanation:

```text
Teacher:
"Binary search works on sorted arrays..."

↓

Quiz:
"Create questions based on:
Binary search works on sorted arrays..."
```

---

### Mistake 4 — Agents have overlapping roles

Avoid instructions like:

```text
Teacher:
Explain concepts and create quizzes.

Quiz:
Explain concepts and create quizzes.
```

Instead:

```text
Teacher → explanation

Quiz → questions
```

Specialization is the point.

---

# 22. Bonus — Add a Reviewer Agent

Once the basic version works, create:

```bash
openclaw agents add reviewer
```

Give it instructions such as:

```md
# Reviewer Agent

You are a Quiz Reviewer.

Review a quiz generated by the Quiz Agent.

Check:

1. Are all questions factually correct?
2. Are the answers correct?
3. Are the questions based on the Teacher's explanation?
4. Are there exactly 3 questions?

If everything is correct, respond:

Quiz approved.

If something is incorrect, identify the problem.
```

Your architecture becomes:

```text
User
 │
 ▼
Orchestrator
 │
 ▼
Teacher Agent
 │
 │ explanation
 ▼
Quiz Agent
 │
 │ quiz
 ▼
Reviewer Agent
 │
 │ review
 ▼
Final Response
```

---

# 23. What You Should Understand After This Task

By the end of the task, you should understand:

### Agent

A specialized AI worker with its own instructions/context.

### Agent Role

The specific responsibility given to an agent.

```text
Teacher → Teach
Quiz → Create questions
Reviewer → Check questions
```

### Orchestrator

The component/agent responsible for controlling the workflow.

### Handoff

Passing work from one agent to another.

```text
Teacher → Quiz
```

### Context Passing

Giving the next agent the information it needs.

```text
Teacher output → Quiz input
```

### Multi-Agent System

Multiple specialized agents cooperating to complete a larger task.

---

# 24. Final Architecture

Your completed Task 1 should look like:

```text
                    ┌─────────────────┐
                    │      USER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    └────────┬────────┘
                             │
                             │ delegate
                             ▼
                    ┌─────────────────┐
                    │ TEACHER AGENT   │
                    └────────┬────────┘
                             │
                             │ explanation
                             ▼
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    └────────┬────────┘
                             │
                             │ handoff
                             │ + explanation
                             ▼
                    ┌─────────────────┐
                    │   QUIZ AGENT    │
                    └────────┬────────┘
                             │
                             │ quiz
                             ▼
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    └────────┬────────┘
                             │
                             ▼
                           USER
```

---

# 25. Submission Checklist

Before submitting, verify:

- [ ] OpenClaw is installed and working
- [ ] Teacher Agent exists
- [ ] Quiz Agent exists
- [ ] Each agent has a clearly defined role
- [ ] Teacher can explain a concept
- [ ] Quiz can generate questions
- [ ] Orchestrator controls the workflow
- [ ] Teacher output is passed to Quiz Agent
- [ ] Handoff is logged
- [ ] Quiz is based on the Teacher's actual explanation
- [ ] You tested multiple concepts
- [ ] Bonus Reviewer implemented, if attempted

---

## The Core Idea

Don't think of this task as:

> "Make two AI prompts."

Think of it as:

> **"Build a small system where specialized AI workers collaborate through controlled handoffs."**

The Teacher doesn't need to know how the Quiz Agent works.

The Quiz Agent doesn't need to know how the Teacher works.

The **orchestrator connects them.**
