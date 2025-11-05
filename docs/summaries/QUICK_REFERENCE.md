# LEARNVIA AI REVISION SYSTEM - QUICK REFERENCE
**One-Page Cheat Sheet**

---

## 📋 THE SYSTEM IN 30 SECONDS

**What:** AI-powered content review system using 60 agents across 4 independent passes
**Goal:** Reduce reviewer workload by 70-80% while maintaining quality
**Status:** Ready for controlled pilot with 5-10 modules
**Philosophy:** Educational and supportive, not punitive

---

## 🔄 THE 4-PASS WORKFLOW

```
ROUND 1: CONTENT & STYLE REVIEW
┌─────────────────────────────────────┐
│ Pass 1: 20 agents                   │
│ • 10 authoring (pedagogy only)      │
│ • 10 style (mechanics only)         │
│ → Author revises & resubmits        │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Pass 2: Different 20 agents         │
│ • 10 authoring (pedagogy only)      │
│ • 10 style (mechanics only)         │
│ • NO knowledge of Pass 1            │
│ → Human Reviewer Checkpoint         │
│   (Author can dispute, human decides)│
└─────────────────────────────────────┘

ROUND 2: COPY EDITING
┌─────────────────────────────────────┐
│ Pass 3: 10 agents                   │
│ • Style/mechanics only              │
│ → Author revises & resubmits        │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Pass 4: Different 10 agents         │
│ • Style/mechanics only              │
│ • NO knowledge of Pass 3            │
│ → Human Copy Editor Checkpoint      │
│   (Author can dispute, human decides)│
└─────────────────────────────────────┘
```

---

## 🎯 KEY INNOVATIONS

1. **Independent Passes:** Different agents each time, no shared memory
2. **Strict Separation:** Authoring vs. style agents have single focus
3. **Consensus Scoring:** Multiple agents must agree for high confidence
4. **Conditional Suggestions:** Only when high severity + high confidence
5. **Dual Feedback Loops:** Learn from false positives AND false negatives

---

## 📊 SUCCESS METRICS (Pilot Targets)

| Metric | Target | Meaning |
|--------|--------|---------|
| **Precision** | 80%+ | When AI flags something, it's usually right |
| **Recall** | 85%+ | AI catches most real issues |
| **Critical Miss Rate** | <10% | Rarely misses important problems |
| **Time Savings** | 50%+ | Reviewer workload reduction (conservative) |

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `EXECUTIVE_SUMMARY_EMAIL.txt` | Send to leadership |
| `PILOT_HANDOFF_PROMPT.md` | Start next Claude session |
| `src/orchestrator.py` | 4-pass workflow |
| `src/reviewers.py` | 60 agent configuration |
| `run_tests.py` | Test suite (currently 100%) |

---

## 🚀 TO START PILOT

**1. Open new Claude Code session**

**2. Message 1 (Understanding Phase):**
```
Read the entire /Users/michaeljoyce/Desktop/LEARNVIA folder and understand
the current system architecture, implementation status, and any gaps.

Focus on:
- The 4-pass review workflow
- How the 60 AI agents are configured
- The feedback loop mechanisms
- Current test status
- What's implemented vs. what needs validation

Once you've read everything, summarize your understanding.
```

**3. Message 2 (Task Assignment):**
```
Now help me execute the pilot plan in PILOT_HANDOFF_PROMPT.md.
Confirm you understand the pilot objectives and are ready to start.
```

**Alternative: Single message with Explore agent**
```
Use the Explore agent with 'very thorough' setting to analyze
/Users/michaeljoyce/Desktop/LEARNVIA and report on the system
architecture and completeness. Then help me execute the pilot
plan in PILOT_HANDOFF_PROMPT.md.
```

---

## ⚠️ CRITICAL RULES (DON'T VIOLATE)

❌ **NO information transfer between passes**
❌ **NO mixing authoring and style in same agent (passes 1-2)**
❌ **NO suggestions unless high severity + high confidence**
❌ **NO "You did..." language (use "The module demonstrates...")**
❌ **NO automated changes without human approval**

---

## 💡 FUTURE ENHANCEMENTS (Post-Pilot)

**Enhancement 1: Persona Diversity**
- Add role framing to authoring agents
- Decide based on pilot coverage gaps

**Enhancement 2: Pre-Review Dispute System**
- "Actually Correct" button for authors
- Guideline contradiction tagging
- Automated feedback loop with prompt creep prevention

---

## 📞 QUICK HELP

**Tests failing?** Run `python run_tests.py` to see what broke

**Need to understand code?** Read `SESSION_COMPLETE_SUMMARY.md`

**Ready to pilot?** Use `PILOT_HANDOFF_PROMPT.md`

**Sending to leadership?** Use `EXECUTIVE_SUMMARY_EMAIL.txt`

---

**Current Status:** ✅ Ready for pilot
**Test Status:** ✅ 100% passing
**Next Step:** Leadership approval → Pilot execution
