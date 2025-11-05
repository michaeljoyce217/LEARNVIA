# Team Meeting Talking Points - AI Review System Report Review

**Meeting Date:** [INSERT DATE]
**Duration:** 30-45 minutes
**Attendees:** [INSERT NAMES]
**Purpose:** Get team feedback on HTML report format before pilot

---

## 🎯 MEETING OBJECTIVES

1. Show team what authors will see after AI review
2. Get feedback on tone, usability, and design
3. Identify any concerns or missing elements
4. Decide on next steps (proceed to pilot or make changes)

---

## 📋 OPENING (2 minutes)

### What to Say:

"Thanks everyone for joining. Today we're reviewing the HTML report that content authors will receive after the AI review system analyzes their modules.

**Context:** We've completed the technical build and successfully tested the 4-pass workflow. The system works - it detects issues, aggregates feedback from 20 reviewers, and generates professional reports.

**What we need from you:** Human judgment on whether this report format would actually help or overwhelm our authors. Is the tone right? Is it actionable? Would they trust it?

**What we're NOT discussing today:** The underlying AI technology or cost (that comes later in pilot testing). Today is purely about the author experience when they open this report."

---

## 📊 SECTION 1: Quick System Recap (3-5 minutes)

### Key Points to Hit:

**The System:**
- 60 AI reviewers across 4 passes
- Consensus-based (not one AI's opinion)
- Pass 1 & 2: Content + style review (20 reviewers each)
- Pass 3 & 4: Copy editing (10 reviewers each)
- Human checkpoints after Pass 2 & 4

**The Test Results:**
- Tested with Module 3.4 (Derivatives) - 46,000 characters
- Pass 1 found 2 high-confidence issues
- Made actual revisions (2,772 characters added)
- Pass 2 verified fixes (0 issues)
- All 4 passes completed in ~1 second

**The Output:**
- Professional HTML report
- That's what we're reviewing today

### What to Show:
- Quick reference to system architecture diagram (if available)
- OR just verbally explain the 4-pass workflow

### Transition:
"So the technical side works. Now let's look at what authors actually see and get your feedback on whether it hits the right tone."

---

## 🖥️ SECTION 2: Live Report Demo (10 minutes)

### Setup:
- Have `demonstration_report_with_issues.html` open in browser
- Screen share so everyone can see
- Scroll slowly through each section

### Narration as You Scroll:

**"Let's walk through this report together..."**

#### HEADER (scroll slowly)
"First thing authors see: module info, which review pass this is, estimated revision time. Question for you: Does this give enough context?"

#### SUMMARY STATS (pause here)
"Dashboard shows total issues, priority breakdown, and number of reviewers. We're showing '20 reviewers' for transparency - want authors to know this is consensus, not one AI. Does this build trust or is it TMI?"

#### CONTENT STRENGTHS (important - pause)
"**This is new.** Before showing any problems, we highlight 3-5 things the module does well pedagogically. This is our 'student-success framing' - start positive, avoid defensiveness.

**Question for group:** Does this feel supportive and genuine, or does it feel patronizing or like a 'compliment sandwich'?"

#### INFO BOX (scroll past, don't dwell)
"Quick explanation of how consensus works and what confidence levels mean. Trying to build trust in the system."

#### PRIORITY MATRIX - RED SECTION (slow down here)
"Now the core feedback. Issues are color-coded by urgency. Red = immediate action required. Let's look at one example..."

**[Click into first critical issue]**

"Each issue has:
- **What we found** - objective observation
- **Why this matters for students** - this is key, not 'you're wrong' but 'here's why students need this'
- Location in the module
- How many reviewers agreed (18 of 20)
- And when we're confident, a specific suggestion

**Question for group:** Is this level of detail helpful or overwhelming? Are we explaining too much?"

#### DISPUTE BUTTON (demonstrate)
"**This is important.** Every issue has a dispute button. Let me click it..."

**[Click dispute button, show form]**

"Author can explain why they disagree. Goes to human reviewer. If they're right, system learns. This creates continuous improvement.

**Question:** Is requiring a written explanation good (forces thoughtfulness) or bad (too much friction)?"

**[Click cancel to close form]**

#### ORANGE SECTION (scroll faster)
"High priority issues - same structure, different severity. These should be addressed but aren't critical."

#### YELLOW SECTION (scroll quickly)
"Lower priority - 'consider addressing' language. More optional."

#### WHAT HAPPENS NEXT (scroll past)
"Guidance on revision process and what Pass 2 looks like."

### After Demo:
"That's the full report. Let's discuss - first impressions?"

---

## 💬 SECTION 3: Structured Discussion (15-20 minutes)

### Discussion Flow:

#### Round 1: First Impressions (5 min)
**Open with:**
"Let's start with gut reactions. What jumped out at you - positive or negative?"

**Listen for:**
- "Too much text"
- "Feels supportive" or "Feels condescending"
- "Clear priorities" or "Overwhelming"
- "Would authors trust this?"

**If silence, prompt with:**
- "What's the first emotion an author would feel opening this?"
- "If you were an author, would you feel supported or criticized?"

#### Round 2: Key Design Decisions (10 min)

**Go through these one by one:**

**1. Starting with Strengths**
"We intentionally show strengths before problems. Some feedback systems don't do this. Thoughts?"

**Listen for:** Patronizing? Valuable? Should be more specific?

**2. "Why This Matters for Students" Framing**
"We avoid 'you did wrong' and use 'here's why students need this' language. Does this feel authentic?"

**Listen for:** Too soft? Appropriately educational? Over-explaining?

**3. Showing Reviewer Agreement ("18 of 20")**
"We show specific numbers to build trust. Is this working or is 'Very High Confidence' enough?"

**Listen for:** Helpful transparency? TMI? Confusing?

**4. Specific Suggestions vs. General Guidance**
"We only give specific suggestions when severity is high AND confidence is high. Otherwise we flag for awareness. Right approach?"

**Listen for:** Want more suggestions? Want fewer? Right balance?

**5. Dispute Mechanism**
"Authors can push back on any issue. We require explanation (not just 'I disagree'). Too much friction?"

**Listen for:** Good design? Too much work? Should be easier?

#### Round 3: What's Missing? (5 min)

**Ask:**
"What information should be in this report that isn't? What would make it more useful?"

**Listen for:**
- Line numbers for locations?
- Comparison to previous version?
- Ability to filter/sort issues?
- Export options (PDF)?
- Progress tracking?

---

## 📊 SECTION 4: Quick Feedback Collection (5 minutes)

### What to Do:

**Option A: Verbal Poll**
"Let's do a quick poll, 1-10 scale:"
1. Professional appearance?
2. Clarity - easy to understand?
3. Supportive tone?
4. Actionability - helpful suggestions?
5. Overall usefulness?

**Option B: Silent Reflection**
"Take 2 minutes, jot down:
- Most valuable element
- Most confusing element
- One thing you'd change"

Then go around room for sharing.

---

## 🎯 SECTION 5: The Main Question (5 minutes)

### What to Say:

"Let me ask the most important question:

**'If you were a content author and received this report, would it help you improve your module or would it feel overwhelming or judgmental?'**

Specifically:
- Would you trust the feedback?
- Would you know what to do next?
- Would you feel supported or criticized?
- Would you actually use it or ignore it?"

**Let this breathe. Get everyone's take.**

---

## 🚦 SECTION 6: Decision Time (5 minutes)

### Present Three Options:

**Option 1: Proceed to Pilot (No Changes)**
"We think this is good enough to test with real authors in pilot. Make adjustments based on their feedback."

**Option 2: Make Minor Adjustments (1-2 Weeks)**
"We identified some concerns that should be fixed before pilot. [List specific concerns from discussion]. Make these changes, then pilot."

**Option 3: Major Redesign (4-6 Weeks)**
"The approach isn't working. We need to rethink the report structure/tone before testing with authors."

### Ask:
"Based on what we've discussed, which option do you think is right? Show of hands?"

---

## 📋 SECTION 7: Next Steps (2 minutes)

### Based on Decision:

**If Option 1 (Proceed):**
"Great. Here's what happens next:
1. This week: Final polish (accessibility, mobile testing)
2. Next week: Select 3-5 modules for pilot
3. Week after: Run pilot with 1-2 authors
4. 3 weeks: Analyze results, decide on wider rollout"

**If Option 2 (Minor Adjustments):**
"Here's what we'll fix: [list items]
Timeline:
1. This week: Make changes
2. Next week: Quick team review of updates
3. Week after: Proceed to pilot"

**If Option 3 (Major Redesign):**
"We'll go back to drawing board. Specifically:
1. Redesign [identified issues]
2. Create mockups
3. Get your feedback again
4. Then move to pilot"

---

## 🙋 SECTION 8: Q&A (Remaining Time)

### Common Questions & Answers:

**Q: "How accurate is the AI? What's the false positive rate?"**
A: "We don't know yet - that's what pilot testing will tell us. Today we're just evaluating if the report format is right, assuming the AI is accurate. Accuracy gets measured in Phase 3."

**Q: "How much does this cost per review?"**
A: "Using mock API for testing - zero cost. Real API costs will be measured in pilot. Estimated 120-180k tokens per full review cycle, but need real data."

**Q: "What if authors just dispute everything?"**
A: "Good question. Human reviewer validates disputes. If author disputes frivolously, human will see that. Also, disputes require written explanation which adds friction. We'll monitor dispute rate in pilot - if it's >50%, that signals trust issues."

**Q: "Can authors see other authors' reports?"**
A: "Not currently. Each report is individual. Could add peer review feature later but starting with 1:1 author-system interaction."

**Q: "What about authors who aren't tech-savvy?"**
A: "Report opens in any browser, no special software. But good point - we should provide training/walkthrough for first-time users. Add to pilot prep."

**Q: "How long does revision typically take?"**
A: "We estimate 10 minutes per issue. Report shows estimated time at top. Pilot testing will validate if this estimate is accurate."

---

## 📝 CLOSING (1 minute)

### What to Say:

"Thank you all for this feedback - really valuable input.

**Summary:** [Recap key points from discussion - 2-3 main themes]

**Decision:** [State the decision - Option 1, 2, or 3]

**Next steps:** [List immediate next steps]

**Follow-up:** I'll send out [meeting notes / revised report / timeline] by [date].

Any final questions before we wrap?"

---

## 🎭 TONE & FACILITATION TIPS

### Do's:
- ✅ Stay neutral - you want honest feedback
- ✅ Probe on vague comments ("Can you say more about that?")
- ✅ Acknowledge concerns ("That's a valid point")
- ✅ Keep it moving - don't let one person dominate
- ✅ Focus on author experience, not technical details

### Don'ts:
- ❌ Defend design choices (you want honest feedback)
- ❌ Solve problems on the fly ("Let's fix this now")
- ❌ Get into technical weeds (API, prompts, etc.)
- ❌ Promise features ("We can add that!") without team input
- ❌ Rush the main question (let it breathe)

---

## 🎬 PRE-MEETING CHECKLIST

**24 Hours Before:**
- [ ] Send calendar invite with agenda
- [ ] Attach demonstration report HTML file
- [ ] Attach executive summary
- [ ] Ask everyone to review report before meeting (15 min prep)

**1 Hour Before:**
- [ ] Test screen sharing
- [ ] Have demonstration report open in browser
- [ ] Have this talking points doc open for reference
- [ ] Have note-taking doc open to capture feedback

**During Meeting:**
- [ ] Record meeting (if allowed) for notes
- [ ] Take notes on key feedback themes
- [ ] Note specific quotes for documentation
- [ ] Track decision and action items

---

## 📊 POST-MEETING ACTIONS

**Immediately After:**
- [ ] Send thank you email to team
- [ ] Compile feedback themes
- [ ] Document decision made
- [ ] Create action item list with owners & dates

**Within 24 Hours:**
- [ ] Send meeting summary to team
- [ ] Share next steps & timeline
- [ ] Schedule follow-up meetings if needed

**Within 1 Week:**
- [ ] Complete any agreed-upon changes
- [ ] Update documentation
- [ ] Prepare for next phase (pilot or revision)

---

## 🗣️ SOUNDBITES FOR LEADERSHIP

**If leadership asks "What happened in the meeting?":**

**Positive Outcome:**
"Team reviewed the report format and gave positive feedback. Main themes: [X, Y, Z]. We're proceeding to pilot testing with [minor/no] adjustments. Timeline: pilot in 2 weeks."

**Mixed Outcome:**
"Team had good feedback with some concerns about [X, Y]. We're making targeted adjustments to address these before pilot. Timeline: 1-2 week delay for changes, then pilot."

**Negative Outcome:**
"Team identified significant concerns about [X, Y]. We're going back to redesign [specific elements]. This will delay pilot by [timeframe] but ensures we get it right for authors."

---

## 💡 HANDLING SPECIFIC SCENARIOS

### Scenario 1: Someone says "This is way too much text"
**Response:** "Can you be more specific? Is it:
- Too many issues shown (should we filter more)?
- Too much explanation per issue (should we shorten)?
- Layout issue (should we use expandable sections)?"

### Scenario 2: Someone says "Authors won't trust AI feedback"
**Response:** "That's exactly why we're testing in pilot. What specifically would build more trust? The '20 reviewers' transparency? More explanation of how it works? Or do you think trust is impossible regardless of format?"

### Scenario 3: Someone says "The tone is too soft/coddling"
**Response:** "Interesting. Is it that the tone is wrong, or that experienced authors specifically would react differently? Should we have different report styles for new vs. experienced authors?"

### Scenario 4: Someone loves everything
**Response:** "Glad you like it! Devil's advocate: what's the one thing that could go wrong with this design? What's the weakest element?"

### Scenario 5: Someone hates everything
**Response:** "I hear you. Help me understand: is it the overall approach (AI reviewing content) you're skeptical of, or is it specific design choices in this report? If we were doing AI review, what would the ideal report look like to you?"

---

## 🎯 SUCCESS METRICS FOR THIS MEETING

**Meeting is Successful If:**
- ✅ Everyone participated and shared honest feedback
- ✅ We identified 3-5 key themes from discussion
- ✅ We made a clear decision (Option 1, 2, or 3)
- ✅ We have documented next steps with dates
- ✅ Team feels heard and involved

**Meeting Needs Follow-Up If:**
- ⚠️ Major disagreements unresolved
- ⚠️ Confusion about what we're building
- ⚠️ No clear decision made
- ⚠️ Concerns dismissed without discussion
- ⚠️ Lack of engagement from key stakeholders

---

## 📞 IF MEETING RUNS SHORT

**Extra Discussion Topics:**

1. **Author Personas:** Should new authors get different reports than experienced authors?

2. **Integration:** How does this fit with existing review workflow?

3. **Training:** What training do authors need before using this?

4. **Success Metrics:** How will we measure if pilot is successful?

5. **Failure Scenarios:** What would make us abandon this system?

---

## 📞 IF MEETING RUNS LONG

**What to Cut:**

1. Skip detailed scroll-through (just hit highlights)
2. Skip Q&A (handle via email)
3. Skip "what's missing" discussion (get via follow-up survey)
4. Skip open discussion (go straight to structured questions)

**What NOT to Cut:**

1. The main question ("would this help or overwhelm?")
2. Making a clear decision (Option 1, 2, or 3)
3. Defining next steps

---

## 🎤 FINAL SOUNDCHECK

**Before you start the meeting, ask yourself:**

1. Am I clear on what decision I need to make today?
2. Am I ready to hear critical feedback without defending?
3. Do I have a plan for each of the 3 possible outcomes?
4. Am I prepared to keep discussion focused (not rabbit holes)?
5. Do I have time allocated for each section?

**If you answered "no" to any:** Take 10 minutes to prep before starting meeting.

---

**Good luck! You've got this. The system is solid - now get human validation.**
