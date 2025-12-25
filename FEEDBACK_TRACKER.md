# Post-Launch Feedback Tracker

## User Feedback Log

Track what users say, ask for, and struggle with. This data drives your next features.

### Format

```
Date: YYYY-MM-DD
Source: Twitter/Reddit/Email/Comment
User: [Name or Anonymous]
Feedback: [Exact quote or paraphrase]
Category: Bug / Feature Request / Question / Suggestion / Praise
Action: [What you'll do about it]
Status: New / In Progress / Completed / Decided Not To Do
```

---

## Example Entries

### Entry 1
```
Date: 2024-12-23
Source: Reddit r/learnprogramming
User: Anonymous
Feedback: "Is there a way to save my code? I want to keep working on my projects."
Category: Feature Request
Action: Add localStorage to save code to browser, plan "code snippets" feature for v2
Status: New
```

### Entry 2
```
Date: 2024-12-23
Source: Twitter
User: @hausa_coder
Feedback: "Love this! Can you add loops? Many beginners want to repeat things."
Category: Feature Request
Action: Add `kaie` (repeat) syntax, design simple loop semantics
Status: New
```

### Entry 3
```
Date: 2024-12-23
Source: GitHub Issue
User: student_123
Feedback: "I don't understand how variables work. Can you add a tutorial?"
Category: Question
Action: Create "Variables" lesson with step-by-step explanation
Status: New
```

---

## Quick Stats to Collect

- [ ] Total playground visits (from hausalang.repl.it analytics)
- [ ] Example most clicked
- [ ] Code executed most often
- [ ] Most common error
- [ ] Bounce rate (users who tried once and left)
- [ ] Return rate (users who came back)

---

## Patterns to Watch For

### Red Flags (Things Breaking Users)
- "I tried to [X] but it didn't work"
- "How do I...?" repeated by multiple users
- High error rate on specific features
- Users abandoning after 2-3 attempts

### Green Signals (Things Working Well)
- "This is so cool, I built [X]!"
- Users trying increasingly complex code
- Users sharing the playground with friends
- Positive sentiment in comments

### Feature Requests to Prioritize
1. **Loops** - most requested (almost guaranteed)
2. **Lists/arrays** - second most requested
3. **Save code** - UX improvement, high value
4. **Dark mode** - nice-to-have, low effort
5. **More tutorials** - only if users struggle with concepts

---

## What NOT to Build (Yet)

Even if users ask for these, say "noted for v2":
- Debugging tools (too advanced)
- Advanced syntax (no classes, imports)
- Deployment/compilation (out of scope)
- Mobile app (web is better for now)
- Community features (forums, voting)

---

## How to Respond to Different Feedback Types

### Bug Report
```
"[Feature] is broken!"

Your response:
"Thanks for reporting! I'll investigate and fix this today.
Can you share the code that broke it?"
```

### Feature Request
```
"Can you add [X]?"

Your response:
"Great idea! I'm tracking this. It's on the roadmap for [timeframe].
What use case would this solve for you?"
```

### Praise
```
"This is amazing!"

Your response:
"Thank you! Means a lot. What did you build with it?"
(Build community by asking them to share)
```

### Question
```
"How do I [do something]?"

Your response:
"Great question! [Answer]. If you're confused, I should add a tutorial
for this. Would that help?"
(Use confusion as signal for tutorials needed)
```

---

## Weekly Review (Do Every Sunday)

1. **Count feedback entries** - how many users responded?
2. **Categorize them** - bugs vs. features vs. questions
3. **Spot patterns** - what's the top request?
4. **Plan next week** - pick top 1-2 things to build
5. **Share update** - tell users "Here's what you asked for"

Example:

```
Weekly Update #1 (Dec 30, 2024)

Thanks to 43 users who tried Hausalang this week!

Top requests:
1. Loops (asked by 8 users) → Adding next week
2. Save code (asked by 5 users) → Month 2
3. More tutorials (asked by 3 users) → Parallel effort

Bug fixes:
- Fixed timeout error on long-running code
- Improved error messages for syntax errors

Next week:
- Launch `kaie` (loop) feature
- Add "Loops" lesson

Keep the feedback coming!
```

---

## Success Criteria

| Week | Metric | Target |
|------|--------|--------|
| 1 | Playground visits | 50+ |
| 1 | Code executions | 100+ |
| 1 | Feedback entries | 5+ |
| 2 | Return users | 10% |
| 2 | Feature requests | 3+ |
| 4 | Total visits | 200+ |
| 4 | Sentiment | 80%+ positive |

---

## Remember

**User feedback is your compass.** Every bug report, question, and feature request tells you what to build next.

Don't guess. Listen. Build based on real needs.

The best product managers in the world do exactly this—they listen obsessively and ship based on feedback.

You're doing that now. ✅
