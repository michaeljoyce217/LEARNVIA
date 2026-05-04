# Tuesday Tips Master List

A bank of 40 weekly tip ideas for Learnvia authors, drawn from the Style Guide, the Authoring Guidelines, and conflicts between the two. Each tip targets a rule that is counter-intuitive, easy to forget, or in direct conflict with what authors have been trained to do elsewhere.

---

## SECTION 1: Tips from the Style Guide (10 Tips)

These tips address rules that go against authors' natural writing instincts from academic training, standard English conventions, or general writing habits.

---

### Tip S1: Periods and Commas Go OUTSIDE Quotation Marks

In Learnvia content, place commas and periods outside of quotation marks, not inside.

Wrong: Write "the limit does not exist."

Right: Write "the limit does not exist".

Why this tip is needed: Every American English class, every newspaper, and virtually every U.S. style guide (AP, MLA, Chicago) teaches the opposite. Periods and commas always go inside quotation marks in standard American English. This is one of the most deeply ingrained writing habits authors have. They will revert to the standard convention on autopilot every time, and they will do it without even noticing. Learnvia follows a non-standard (British-style) convention, so authors need explicit, repeated reminders.

---

### Tip S2: Don't Say "Therefore" — Say "So"

Do not use thus, hence, or therefore. Use so instead.

Wrong: The derivative equals zero at x = 3. Therefore, x = 3 is a critical point.

Right: The derivative equals zero at x = 3. So, x = 3 is a critical point.

Why this tip is needed: In academic mathematical writing, therefore, thus, and hence are prestige words. They signal rigor and formality. Math professors and textbook authors use them reflexively. It feels like a downgrade to write "so" in a calculus course, and authors may feel that "so" sounds too casual or imprecise for mathematical reasoning. But the target learners benefit from simpler connectors, and "so" does the same job with less cognitive load.

---

### Tip S3: No Semicolons. Period.

Do not use semicolons in prose. The one exception is separating numbers of 5 or more digits in a list (22,305; 14,672; 19,829).

Wrong: The function is continuous on the interval; it meets all conditions of the theorem.

Right: The function is continuous on the interval. The function meets all conditions of the theorem.

Why this tip is needed: Semicolons are a standard, widely taught punctuation mark. Authors with strong writing backgrounds will instinctively reach for semicolons to join related independent clauses, especially in mathematical explanations where two ideas are logically connected. The rule is absolute (with one narrow exception), which is unusual. Authors may not even realize semicolons are banned, since most style guides encourage them.

---

### Tip S4: Possessives Are NOT Contractions

Do not use contractions, but do use possessives. In fact, possessives are preferred over "of the" constructions.

Wrong (over-correction): How is the area of the square changing over time?

Right: How is the square's area changing over time?

Why this tip is needed: Once authors internalize the "no contractions" rule, they over-correct. They start avoiding all apostrophe-s constructions, including possessives, because they look and feel similar to contractions. The result is stilted, wordy phrasing. Authors need to understand that possessives and contractions are completely different things, and that the guide explicitly prefers the possessive form.

---

### Tip S5: Drop "There Is" and "There Are"

"There is" and "There are" are lazy sentence starters. Eliminate them. Start with the real subject instead.

Wrong: There are several ways to solve a quadratic equation.

Right: A quadratic equation can be solved in several ways.

Why this tip is needed: "There is/are" is one of the most common sentence patterns in English. It feels natural, conversational, and even friendly, which makes it especially tricky because the guide also asks for a conversational tone. Authors genuinely do not notice these constructions in their own writing because they are so ubiquitous. This is a habit that requires conscious effort to break.

---

### Tip S6: Punctuation Goes INSIDE the LaTeX

All punctuation following LaTeX must be coded within the LaTeX itself, using \text{.} or \text{,}. Otherwise, punctuation can break onto the next line on small screens.

Wrong: Find the derivative of <m>f(x)=x^2-3</m>.

Right: Find the derivative of <m>f(x)=x^2-3\text{.}</m>

Why this tip is needed: This is a mobile-rendering concern that authors writing on desktop monitors will never encounter or think about. The natural instinct is to close the LaTeX environment and then type the period or comma as regular text, the same way it works in any word processor. The requirement to put punctuation inside the LaTeX using \text{} is an extra step that feels unnatural and is easy to forget, especially under deadline pressure.

---

### Tip S7: Don't Say "Below" or "Above"

Do not use directional language referencing visual location on a page. Use "the following graph," "the given equation," or specific label names instead. Exception: mathematical directional language like "left-hand limit" is fine.

Wrong: In the graph below, the function approaches a limit.

Right: In the following graph, the function approaches a limit.

Why this tip is needed: Authors are writing in an authoring tool where they can literally see the graph below the text they are typing. The spatial relationship is real on their screen, so "the graph below" feels accurate and helpful. They may not be thinking about screen readers, reflowed mobile layouts, or that content may be rearranged in the final product. The exception for mathematical directional language adds further confusion, since authors may assume all directional language is acceptable.

---

### Tip S8: Capitalize Theorems, but Lowercase Rules and Formulas

Capitalize all key words in theorem, property, and postulate names (Mean Value Theorem, Pythagorean Theorem). But lowercase the names of rules and formulas (chain rule, product rule, rate of change formula).

Wrong: Apply the Chain Rule, then use the Mean value theorem.

Right: Apply the chain rule, then use the Mean Value Theorem.

Why this tip is needed: The distinction between a "theorem" and a "rule" is not always obvious, and the capitalization convention contradicts how many textbooks handle it. Many authors will capitalize "Chain Rule" and "Product Rule" because they look like proper names and are often capitalized in other textbooks. Conversely, some authors may lowercase "mean value theorem" by analogy with "chain rule." The split convention requires authors to think about what kind of mathematical result they are referencing every time they type one.

---

### Tip S9: Ban "It" — Even When It Seems Perfectly Clear

Do not use it and they as pronouns. Restate the noun. Even when the reference seems unambiguous, "it" increases cognitive load by forcing the reader to look back.

Wrong: The expression has one term. It uses two variables.

Right: The expression has one term. The term uses two variables.

Why this tip is needed: Pronoun usage is so fundamental to fluent English that avoiding "it" feels robotic and repetitive. Authors will write "it" hundreds of times without noticing. The rule is especially hard because sometimes "it" truly does seem unambiguous, but the guide says to avoid it even then to reduce cognitive load. Most writing guides actually encourage pronoun use to avoid repetition, so this directly contradicts authors' training.

---

### Tip S10: 4-Digit Numbers: Drop the Comma

Eliminate the comma in numbers of exactly 4 digits. Write 4389, not 4,389. Use commas only in numbers of 5 or more digits.

Wrong: The coordinates of the point are (4,000, 2,570).

Right: The coordinates of the point are (4000, 2570).

Why this tip is needed: Standard American English convention says to use commas in numbers of four or more digits. This is deeply habitual. Authors have been writing "1,000" and "5,280" their entire lives. In a math context, omitting the comma from a 4-digit number inside an ordered pair like (4000, 2570) also matters because the comma separating the coordinates could be confused with a comma inside the number. Authors must fight both muscle memory and their sense that the comma aids readability.

---

## SECTION 2: Tips from the Authoring Guide (10 Tips)

These tips target pedagogical and structural mistakes authors make based on their classroom teaching experience, textbook writing habits, or academic training.

---

### Tip A1: Your Hints Should Never Be Questions

Hints for short-answer questions must be written in declarative form, not as questions. They should concretely lead the student one step closer to the answer.

Wrong:
Hint 1: "What is the precedence of * vs + ?"
Hint 2: "Remember to multiply first."

Right:
Hint 1: "* has highest precedence, so start with 4 * 7."
Hint 2: "3 + (4 * 7) - 2 = 3 + 28 - 2. With + and -, evaluate left to right, so evaluate 3 + 28."

Why this tip is needed: In live tutoring and classroom teaching, Socratic questioning is a gold-standard technique. Instructors are trained to ask "What do you think happens next?" It feels natural and pedagogically sound to write hints that gently nudge with a question. But in an asynchronous, self-paced format, a hint written as a question is a dead end. The student is stuck precisely because they cannot answer that question. Hints need to give concrete steps, not ask the student to figure out the thing they already cannot figure out.

---

### Tip A2: Stop Saying "We" — Let the Math Speak for Itself

Describe concepts without unnecessary use of "we." Use descriptive, impersonal phrasing. Occasional use of "we" is acceptable only when genuinely referring to ourselves as people.

Wrong: If we want to consider the average rate of change of f on the interval, we compute...

Right: The average rate of change of f on the interval is...

Why this tip is needed: Academic writing uses "we" constantly. "We define slope as..." "We can see that..." "We now prove..." It is deeply ingrained in how mathematicians and instructors communicate. Dropping "we" feels unnatural and even stiff. But excessive "we" leads to inconsistent switching between descriptions and personal statements, adding unnecessary cognitive load for the learner.

---

### Tip A3: No Pronouns Allowed (Yes, Really — Not Even "You")

Do not use he, she, it, they, or you. The only pronouns permitted are we/us, used sparingly.

Wrong: It is essential that you understand how the average rate of change of f on an interval is connected to its graph.

Right: The connection between f's average rate of change on an interval, and f's graph, is important to understand.

Why this tip is needed: Pronouns are the backbone of natural English. Writing without "it" or "you" feels robotic and repetitive. Authors instinctively write "It is essential that you understand..." because that is how humans talk. They assume the context makes the referent clear. But for a struggling student reading alone, every "it" or "this" is a potential point of confusion. "The expression has one term. It uses two variables" — does "it" mean the expression or the term?

---

### Tip A4: Learning Questions Are NOT Homework Problems

Follow-up learning questions should be quickly answerable. They should not involve lengthy calculations. Think of a tutor still teaching, not a student working independently on homework.

Wrong: Given f(x) = 3x^2 + 5x - 7, calculate f(-4), f(-3), f(-2), f(-1), f(0), f(1), f(2), f(3), f(4). Plot all points and draw the curve.

Right: Given the table for f(x) = x^2 from -5 to 5, fill in the two missing values.

Why this tip is needed: Authors naturally escalate difficulty. Once they have taught a concept, they want to test it rigorously. The instinct is to write a "good" problem that really proves the student can do it. But learning questions serve a fundamentally different purpose from homework. They are part of the lesson, not an assessment. They replace reading. Making them too hard or calculation-heavy frustrates the target learner, someone studying at home, alone, with low confidence.

---

### Tip A5: Use "Ex:" Not "e.g." — And Never Use "i.e."

Use "Ex:" to introduce examples. Do not use "e.g." or "i.e." Use "specifically" instead of "i.e."

Wrong: Some fractions yield a repeating decimal, e.g., 1/3 yields 1.333...

Right: Some fractions yield a repeating decimal. Ex: 1/3 yields 1.333...

Why this tip is needed: Academic authors have been using "e.g." and "i.e." their entire careers. These abbreviations are universal in scholarly writing and feel precise and professional. But the target learner may not have advanced English comprehension. "Ex:" is simpler, more immediately recognizable, and more natural. This is a small change that authors consistently forget because "e.g." is essentially muscle memory.

---

### Tip A6: Use Unique Values in Math Problems

Use unique values in questions to reduce confusion. Avoid problems where the same number appears in multiple roles.

Wrong: The derivative of 2x^2 + 4x = ? (Answer: 4x + 4 — three 4's, two 2's)

Right: The derivative of 3x^2 + 5x = ? (Answer: 6x + 5 — all unique values)

Why this tip is needed: Authors pick "clean" or "simple" numbers for convenience. Using 2x^2 + 4x seems natural with its small coefficients and easy arithmetic. But when the derivative is 4x + 4, there are now three 4's in play and two 2's. When a student asks the AI tutor "Where did the 4 come from?" the system cannot tell which 4. This is a subtle design issue that experienced mathematicians rarely notice because they have no trouble distinguishing the roles of numbers.

---

### Tip A7: The Static Figure IS the Animated Figure — Start There

The most important part of an animated figure is its static version. Develop a static figure first that teaches the concept on its own. The animation then unveils that static figure step by step.

Wrong: Author designs a sequence of animation steps, then grabs the last frame as the "static figure."

Right: Author sketches multiple versions of a static figure that teaches the full concept on its own (including labels, arrows, color grouping), then plans how to unveil it across 3-5 scenes.

Why this tip is needed: Authors think of animation as the main event, the "cool" part that does the real teaching. They design the animation first and treat the static figure as an afterthought or a screenshot of the final frame. But students view content statically on the web and when printing. A static figure that does not teach on its own fails half its audience. The correct workflow inverts the usual instinct.

---

### Tip A8: Always Explain the Correct Answer — Assume the Student Guessed

For every multiple-choice question, the correct answer must have a full explanation. Assume the student guessed. For wrong choices, explain why that specific choice is wrong. Never start explanations with "Correct" or "Incorrect" — the platform handles that.

Wrong:
Correct choice: "Correct! Water is the right answer."
Wrong choice: "Incorrect. The correct answer is water."

Right:
Correct: "When heated, the liquid water inside a kernel turns to steam, which occupies more volume. The steam pushes against the kernel's walls, causing the popping."
Wrong (air): "Although air is inside, the heated air seeps out and so does not cause the popping."

Why this tip is needed: When authors write a correct-answer explanation, they instinctively write something celebratory: "Correct! This is an important concept." They assume a student who picked the right answer understood the reasoning. But many students guess, and seeing "Correct!" with no explanation is a missed learning moment. For wrong answers, authors often write generic corrections instead of addressing why that specific distractor is wrong.

---

### Tip A9: Factor Common Text Out of Your Multiple-Choice Answers

Answer choices should be short — one word or a few words. Factor out any common text into the question stem so each choice contains only what differs.

Wrong:
"Most medical lawsuits ___."
- "stem from improper expectations by the patient"
- "result from the patient not trusting their doctor's abilities"
- "are an outcome of a patient not liking their doctor's attitude"

Right:
"Most medical lawsuits arise from a patient's ___."
- "improper expectations"
- "distrust of their doctor"
- "dislike of their doctor's attitude"

Why this tip is needed: Authors write answer choices as complete thoughts because it feels thorough. Each option reads like a mini-paragraph. This comes from a desire to be precise and unambiguous. But long, sentence-length choices are cognitively expensive for students. They turn a knowledge question into a reading comprehension test. Factoring out the shared prefix makes each choice crisp and scannable.

---

### Tip A10: No Synonyms, Ever — Pick One Term and Stick With It

Create one term for each concept and use that term exclusively. Do not alternate between words that mean the same thing.

Wrong:
Paragraph 1: "Calculate the average of the data set."
Paragraph 2: "The mean of the data set tells us..."
(Student thinks: "Wait — are average and mean different things?")

Right:
Use "average" consistently throughout, OR "mean" consistently. If both terms need to be known, explicitly state: "The average, also called the mean, is calculated by..."

Why this tip is needed: Good writing, in virtually every other context, demands variety. English teachers and editors all say "Don't repeat the same word — use a synonym!" Alternating between "average" and "mean," or "graph" and "plot," feels like better writing. But for a math learner encountering new vocabulary, every unflagged synonym is a potential misconception. The student wonders: "Is 'mean' different from 'average'? Did I miss something?"

---

## SECTION 3: Tips from Conflicts Between the Two Guides (20 Tips)

These tips address places where the Style Guide and the Authoring Guidelines contradict each other, give overlapping guidance with different emphasis, or where one guide's examples violate the other's rules. These are the most important tips because authors literally cannot resolve these on their own.

---

### Tip C1: "We" in Animated Figure Captions Is the Exception

The style guide says to minimize "we." But the authoring guide's example captions use "we" in every scene: "we first calculate," "We can plot," "we can draw."

Resolution: "We" is acceptable and even preferred in animated figure captions, where the narration creates a sense of shared exploration between the student and the content. In all other instructional text (framing text, explanations, definitions), follow the style guide and avoid "we."

Why this tip is needed: Authors reading both guides will see a clear rule ("minimize 'we'") and a clear example that breaks the rule. Without explicit guidance on this exception, authors will either avoid "we" in captions (making them feel flat and impersonal) or use "we" everywhere (citing the examples as justification). Neither outcome is correct.

---

### Tip C2: Active Voice Definitions, Not Passive

The style guide says definitions should use: "A function is a rule that..."
The authoring guide models: "Slope is defined as..."

Resolution: For formal definitions (those using definition tags), use the active style guide format: "A [term] is [definition]." The passive alternative ("X is defined as...") is acceptable only in informal references within body text.

Why this tip is needed: Both guides address how to write definitions, but they model different patterns. Authors trying to follow both will not know whether "Slope is the ratio of rise to run" or "Slope is defined as the ratio of rise to run" is correct. The active form is stronger and more direct.

---

### Tip C3: Where Definitions Belong Depends on the Animation

The style guide says definitions go in framing text (before the animated figure). The authoring guide says some definitions belong in follow-up text (after the animated figure).

Resolution: Place definitions in framing text when students need the term to understand the upcoming animation. Place definitions in follow-up text when the animation teaches the concept and the formal definition only makes sense afterward. When in doubt, default to framing text.

Why this tip is needed: An author writing a definition will encounter two different instructions about where to put it. Without this clarification, some authors will always put definitions first (sometimes prematurely) and others will always put them after (sometimes too late for comprehension). The placement should be driven by whether the animation depends on the term or teaches the term.

---

### Tip C4: "Thus/Hence/Therefore" Is Banned — Even Though the Authoring Guide Uses It

The style guide explicitly bans thus, hence, and therefore. The authoring guide uses "Thus" in its own prose and never mentions this rule.

Resolution: In all student-facing content, use "so" instead of thus, hence, or therefore. This is a style guide rule that the authoring guide simply does not repeat.

Why this tip is needed: Authors who primarily work from the authoring guide will never encounter this rule. Worse, they will see the authoring guide itself using "thus" and assume it is acceptable. This tip closes a gap between the two documents.

---

### Tip C5: There IS a Concrete Reading Level Target — 8th Grade

The style guide specifies an 8th grade reading level and recommends the Hemingway Editor as a checking tool. The authoring guide never mentions a specific reading level.

Resolution: Aim for an 8th grade reading level in all student-facing prose. Use the free Hemingway Editor (hemingwayapp.com) to check your framing text and captions.

Why this tip is needed: The authoring guide, which many authors treat as their primary working document, uses vague language like "concise" and "accessible" without giving a measurable target. Authors need to know there is an objective benchmark they can verify against, not just a subjective impression of simplicity.

---

### Tip C6: Semicolons — The Ban and the Exception

The style guide bans semicolons. Then, in a separate section, it requires semicolons for lists of 5-digit-or-larger numbers. Neither guide reconciles this.

Resolution: Do not use semicolons in prose sentences, ever. The one exception is when listing numbers with 5 or more digits, where commas within the numbers would create confusion. Ex: (22,305; 14,672; 19,829).

Why this tip is needed: Authors who learn the "no semicolons" rule may later encounter the large-number list exception and think the ban has been relaxed. Or they may avoid semicolons even where the exception applies, creating confusing number lists. The ban and the exception need to be stated together.

---

### Tip C7: Question Format — "Find the derivative" vs. "The derivative = ___"

The style guide says the imperative voice is acceptable in questions ("Find the equation..."). The authoring guide says to prefer the fill-in-the-blank statement format ("The derivative of 3x^2 + 5x = ___").

Resolution: Use the blank/fill-in-the-statement format for learning questions (embedded and follow-up). Save the imperative form ("Find," "Calculate," "Determine") for homework and quiz questions.

Why this tip is needed: An author writing "Find the derivative of 3x^2 + 5x" is following the style guide. An author writing "The derivative of 3x^2 + 5x = ___" is following the authoring guide. Both feel correct. Without this clarification, question format will be inconsistent across modules. The distinction is that learning questions are part of the lesson (use blanks) while assessment questions are standalone (imperative is fine).

---

### Tip C8: Conversational Tone Without Contractions

The style guide bans contractions AND demands a "conversational, friendly" tone. The authoring guide's own prose uses contractions.

Resolution: Think "warm but grammatically complete." Achieve a friendly feel through short sentences, simple vocabulary, and occasional use of "we." A conversational tone does not require contractions.

Why this tip is needed: A "conversational and friendly" tone naturally uses contractions in everyday English. The style guide demands both things simultaneously, which feels contradictory. Authors will feel tension between sounding friendly (which to them means "don't" and "it's") and following the contraction ban (which to them means stiff formality). They need to know that warmth comes from sentence structure and word choice, not from contractions.

---

### Tip C9: The Pronoun Ban — What's Actually Allowed

The style guide bans "you, she, he, they, it" but discusses "we" separately. The authoring guide explicitly allows "we/us." The style guide also allows "its" in certain cases. The two guides list slightly different pronouns.

Resolution: Never use "you," "he," "she," or "they." Use "we/us" sparingly and intentionally. Use "it/its" only when the referent is completely unambiguous and rewriting would be cumbersome (as in "A function and its inverse"). When in doubt, restate the noun.

Why this tip is needed: The two guides present slightly different versions of the pronoun rule. Authors trying to reconcile both may be confused about whether "it" is ever acceptable (the style guide both bans it and allows it in examples) and whether "we" is truly acceptable (the style guide seems skeptical, the authoring guide seems encouraging). A single, clear hierarchy eliminates the confusion.

---

### Tip C10: Introductory Clauses — Banned With One Exception

The style guide says avoid introductory clauses. A later section of the style guide says "When solving..." is acceptable.

Resolution: Generally lead with the main subject. The one exception: "When [doing an action]" clauses are acceptable when describing a mathematical procedure, because they set necessary context. Ex: "When differentiating f(x) = (3x^2+2x)^5, apply the chain rule." For all other sentence types, put the subject first.

Why this tip is needed: Authors will encounter "avoid introductory clauses" and then see acceptable examples that are introductory clauses. They cannot tell whether the rule has many exceptions or just one. This tip draws a clear line: procedural "When..." is the exception. All others should be restructured.

---

### Tip C11: Annotations on Calculations — Depends on Where

The style guide says "do not annotate lines of calculations." The authoring guide's hint examples intersperse explanatory text with calculation steps.

Resolution: Do not annotate calculation lines in framing text or animated figures. Put explanatory text before the calculation block instead. However, in hints and question explanations, you may intersperse text with calculation steps because hints are actively guiding a student through a solution, which is a different context.

Why this tip is needed: An author writing hints that walk students through a calculation step by step will naturally mix text and math. The style guide seems to ban this. The authoring guide seems to model it. The resolution is that the rule applies to lesson content (where calculations should stand on their own) but not to hints (where the whole point is guiding the student through each step).

---

### Tip C12: Accessibility Rules Apply to Animated Figures Too

The style guide has detailed accessibility rules: never use color as the only differentiator, avoid ableist language, do not reference content by visual position. The authoring guide is completely silent on accessibility and praises color grouping in its example analysis without mentioning the need for alternative differentiators.

Resolution: When using color in animated figures and graphics, always supplement color with another differentiator such as labels, patterns, or shapes so that color-blind students can still distinguish items. These style guide rules apply to all content types, including animated figures, even though the authoring guide does not mention them.

Why this tip is needed: Authors reading only the authoring guide will miss entire categories of accessibility rules. The authoring guide's example analysis celebrates color grouping ("Used superbly to group items: height items are purple, the ball is green, time is orange") without ever mentioning that color must not be the sole differentiator. Authors will follow the example they see.

---

### Tip C13: Quotation Mark Punctuation Is Non-Standard — And Only in One Guide

The style guide requires placing periods and commas outside quotation marks. The authoring guide contains no guidance on quotation mark punctuation.

Resolution: Periods and commas go OUTSIDE quotation marks. Write: The student should write "the limit does not exist". This is the opposite of standard American English convention.

Why this tip is needed: Authors who primarily consult the authoring guide will never encounter this rule and will default to standard American punctuation (periods inside quotes). Since this rule contradicts universal American training, it needs to be highlighted even for authors who have read the style guide, because they will revert to habit.

---

### Tip C14: Question Structure Rules Live Only in the Authoring Guide

The authoring guide specifies number of choices (default 3, maximum 4 if justified), explanation requirements, and hint design rules. The style guide says nothing about question structure.

Resolution: For question structure, follow the authoring guide exclusively. The style guide covers how to write the text within questions (grammar, vocabulary, formatting) but not how to structure the questions themselves.

Why this tip is needed: Authors cross-referencing both guides for question-writing guidance will find structural rules in one place and text rules in the other. Without this clarification, authors may think the style guide's silence on question structure means there are no rules, or they may look for structural guidance in the style guide and waste time.

---

### Tip C15: Avoiding "We" Without Falling Into Passive Voice

The style guide says use active voice. The authoring guide's solution for avoiding "we" is passive voice ("Slope is defined as..."). These two rules are in direct tension.

Resolution: The best fix is neither passive voice nor "we." Make the mathematical object the subject of the sentence: "Slope is the ratio of rise to run." This is active voice without a personal subject.

Why this tip is needed: Authors face a genuine dilemma. "We define slope as..." violates the "minimize we" rule. "Slope is defined as..." violates the "use active voice" rule. Without a clear third option, authors will ping-pong between the two violations. The solution (mathematical object as subject) resolves both constraints simultaneously.

---

### Tip C16: Bare "This" Is Banned — "This + Noun" Is Fine

The style guide bans "This is..." and "This means..." and "This" as the sole subject. The authoring guide's example analysis approves "This situation is modeled by..."

Resolution: Bare "This" as a sentence subject is always wrong. "This" followed by a specific noun ("This equation shows..." or "This situation is modeled by...") is acceptable because the noun removes the ambiguity.

Why this tip is needed: The style guide draws a line that is not entirely clear. It bans "This is..." but the authoring guide models "This situation is..." Authors need to understand the principle behind the rule: the problem is not the word "this" but the vague reference. Adding a noun after "this" makes the reference specific and therefore acceptable.

---

### Tip C17: "We" in Animation Questions vs. Standalone Questions

The style guide bans personal pronouns in questions. The authoring guide models "How do we connect the points?" in embedded animation questions.

Resolution: "We" is acceptable in embedded questions within animated figures, where it maintains the conversational narration flow. In standalone follow-up questions, rephrase to avoid "we." Ex: "The points are connected by ___." or "The best way to connect the points is ___.""

Why this tip is needed: Authors writing embedded questions during an animation sequence will naturally continue the "we" voice that the captions use. The style guide seems to ban this. The resolution is that the animation context is special because embedded questions are part of the narration, not standalone assessments.

---

### Tip C18: Em-Dashes Are Banned — Despite What the Authoring Guide Models

The style guide explicitly bans em-dashes. The authoring guide uses double-hyphens (which render as em-dashes) throughout its own prose.

Resolution: Do not use em-dashes in student-facing content. For parenthetical thoughts, restructure the sentence, use parentheses, or start a new sentence.

Why this tip is needed: Authors will see the authoring guide using em-dash-style constructions on nearly every page and assume they are acceptable. The authoring guide's own writing habits contradict the style guide's explicit rule. Authors mimic what they read, so this conflict needs to be surfaced directly.

---

### Tip C19: Possessives for People in Word Problems

The style guide says possessives are preferred ("the square's area" over "the area of the square"). The authoring guide bans pronouns (no "his" or "her"). What about people in word problems?

Resolution: Possessives for mathematical objects are always preferred: "the function's derivative," "the square's area." For people in word problems, use role-based possessives instead of pronouns: "the engineer's calculation" (not "her calculation"). This satisfies both the possessive preference and the pronoun ban.

Why this tip is needed: The possessive rule and the pronoun ban interact in a way neither guide addresses. When a word problem involves a person, authors face a choice: "the engineer's calculation" (possessive, follows style guide), "her calculation" (pronoun, violates authoring guide), or "the calculation of the engineer" (wordy, violates style guide). The answer is the role-based possessive, but authors need to be told this explicitly.

---

### Tip C20: Use "Because," Not "Since" — Even Though the Authoring Guide Uses "Since"

The style guide has a detailed rule: use "because" for causation, and reserve "since" for temporal meanings ("since 1990"). The authoring guide uses "since" casually for causation throughout its examples.

Resolution: In all student-facing content, use "because" when expressing a reason or cause. Reserve "since" for temporal meaning only. Also, never combine because/since with "then" — write "Because P, Q" not "Because P, then Q."

Why this tip is needed: The style guide has a nuanced, important rule. The authoring guide completely ignores it and models the wrong usage. An author who reads only the authoring guide will use "since" and "because" interchangeably, violating the style guide. An author who reads both will see the authoring guide contradicting the style guide and not know which to follow. The style guide is correct here.

---

## SECTION 4: Tips from the Questions Guide (25 Tips)

These tips target rules from the Learnvia Questions Guide (issued 2/26/26). They cover prompt format, multiple-choice mechanics, distractor design, feedback structure, hint scaffolding, and platform-specific question type rules. Many of these directly contradict habits authors carry over from textbook authoring or classroom test writing.

---

### Tip N1: MC Prompts Must Be Statements, Not Questions

Multiple-choice prompts must take the form of a sentence with a blank, not the form of a question. The Questions Guide is explicit: prompts should NOT be grammatical questions.

Wrong: What is the slope of the tangent line to f at x = 2?

Right: The slope of the tangent line to f at x = 2 is _____.

Why this tip is needed: Every standardized test, every quiz authors took in school, ended each item with a question mark. The instinct to write "What is...?" or "Which of the following...?" is so ingrained that authors will not even notice they have written a question. The fill-in-the-blank format is the Learnvia default for nearly every prompt — the only exception is long-answer questions.

---

### Tip N2: Answer Choices Must Read as a Grammatical Continuation of the Stem

When you read the stem and any answer choice together as a single sentence, the result must be grammatically correct.

Wrong:
Stem: The limit of f at x = 3 is _____.
Choice: does not exist
(Reads as: "The limit of f at x = 3 is does not exist." Broken.)

Right:
Stem: The limit of f at x = 3 _____.
Choices: is 3 / is 6 / does not exist
(All three read as complete sentences.)

Why this tip is needed: Authors write the stem and the choices in separate moments and never read them as joined sentences. A choice that breaks grammar is a tell the student can use to eliminate it, AND it confuses students who do not yet have native fluency in mathematical English. Reading every stem-plus-choice pair aloud catches this immediately.

---

### Tip N3: Parallel Length — Long Outliers Reveal the Correct Answer

All answer choices in an MC question must be roughly the same length. A choice that is markedly longer or shorter than the others is a giveaway.

Wrong:
- "increases without bound, rising upward to the left"
- "goes down"
- "levels off"

Right:
- "increases"
- "decreases"
- "levels off"

Why this tip is needed: Authors over-explain the correct answer because they want it to be unambiguous. The result is a long correct choice surrounded by short distractors. Test-taking strategy literature has trained students to pick the longest choice when in doubt — and they are usually right. Equal length removes the cue.

---

### Tip N4: Parallel Construction — All Gerunds OR All Noun Phrases, Never Mixed

Every answer choice in an MC question must have the same grammatical structure. If one choice starts with a gerund ("subtracting…"), all choices must start with gerunds.

Wrong:
- "subtracting the area below the x-axis from the area above"
- "the addition of the areas above and below the x-axis"
- "average the values of the function on the interval"
- "estimate the net area by summing rectangles"

Right (all gerunds):
- "subtracting the area below the x-axis from the area above"
- "adding the areas above and below the x-axis"
- "averaging the values of the function on the interval"
- "estimating the net area by summing rectangles"

Why this tip is needed: Authors focus on the meaning of each choice and overlook the grammar. Mixed construction (gerund + noun phrase + bare verb) is jarring to read, and the odd-one-out construction draws the student's eye for the wrong reasons.

---

### Tip N5: Don't Repeat Stem Language in an Answer Choice

If a phrase appears in the question prompt, do not repeat that phrase in one of the answer choices. Word repetition is a clue that points students to the correct choice.

Wrong:
Stem: A limit describes a function's _____.
Choices: output as the input gets closer to a value / range / domain
(Repeating "input" or "function" in the correct choice clues the student.)

Right: Use synonyms or generic phrasing in the correct choice; keep the language of the stem distinct.

Why this tip is needed: Authors naturally echo the prompt language in the correct answer because it feels coherent. Standardized test design has long warned against this — repeated language is one of the most reliable cues a student can exploit without actually knowing the content.

---

### Tip N6: Banned Constructions: NOT, EXCEPT, Always, Sometimes, Never

Minimize use of these in question prompts. They confuse target learners and invert the cognitive task.

Banned by default:
- "Which of the following is NOT…"
- "All of the following EXCEPT…"
- "Always," "Sometimes," "Never"
- "All of the above," "None of the above," "Options a and b"

Acceptable: "sufficient" and "necessary" in calculus questions.

Why this tip is needed: Negative-form questions ("which is NOT") are well-known to inflate error rates that have nothing to do with content mastery. Authors who came up through traditional testing reach for these constructions reflexively because they make distractor-writing easier (just list four true things and one false one). Learnvia bans them because they assess reading comprehension instead of math.

---

### Tip N7: Avoid Opposites and Absolutes in Answer Choices

Two answer choices that are direct opposites cue the student that the answer is one of the two. Absolutes ("always positive," "never negative") add unnecessary complexity that distracts from the actual concept.

Wrong (opposites):
- "the x-coordinate"
- "the y-coordinate"
(Acceptable only if you add a third plausible non-opposite, like "neither of the coordinates.")

Wrong (absolutes):
- "the derivative is always positive on the interval"
- "the derivative is never positive on the interval"

Right (no absolutes):
- "the derivative is positive on the interval"
- "the function is positive on the interval"

Why this tip is needed: Opposites feel like clean, balanced distractors. They are not — they are a binary cue. Absolutes feel rigorous, but they shift the student's attention from the math to the quantifier. Both habits come from formal logic training and need to be unlearned for this audience.

---

### Tip N8: Distractors Are Common Misconceptions, Not Tricks

Every incorrect answer must be plausible, must reflect a real student misconception or error, and must create a teaching moment. Distractors that are obviously wrong waste a slot. Distractors that are tricky or obscure punish students for noticing details that do not matter.

Wrong: Random plausible-sounding answers, or answers designed to trap students who skim.

Right: Each distractor maps to a specific, predictable error a student might make. The feedback for that distractor then addresses that exact misconception.

Why this tip is needed: Authors write distractors as filler ("I need three more wrong choices"). Without a specific misconception in mind, the choice is either too easy to eliminate or weirdly tricky. The Questions Guide expects every distractor to teach. Effective authoring means asking, before writing each distractor: "What mistake would a student make to land here?"

---

### Tip N9: Randomize Answer Order — Alphabetize or Sort by Value

The author must randomize the position of the correct answer across questions. Do not put the correct answer in the same slot every time. A useful default: alphabetize the choices, or order numerical choices smallest-to-largest.

Why this tip is needed: Authors unconsciously place the correct answer in the same position (often A or the second-from-last). Across a question set this becomes a pattern students can exploit. Alphabetizing or sorting by value removes the author's bias from the equation entirely.

---

### Tip N10: Correct-Answer Feedback Restates the Answer in the Question's Terms FIRST

Begin correct-answer feedback by restating the answer in the language of the question. Then explain why, with calculations as needed. Assume the student guessed.

Wrong: "Correct! The two-sided limit does not exist."

Right: "A two-sided limit exists only if the left-hand and right-hand limits are equal. Because they differ here, the function's two-sided limit does not exist."

Why this tip is needed: This builds on Tip A8 with a specific structural rule the new guide makes explicit. The "restate first, explain second" pattern catches the student who guessed correctly without understanding. It also creates a repeated rhythm across all explanations that students learn to rely on.

---

### Tip N11: Incorrect-Answer Feedback Uses Magic Words: but, not, however, instead, so

Incorrect feedback connects the student's choice back to the question with explicit logical connectors. Start by saying why the answer is wrong, then point toward the correct answer.

Wrong: "The correct answer is f' is positive on the interval."

Right: "f being positive does not tell us how f is changing. Instead, the sign of f' determines whether f is increasing or decreasing."

Why this tip is needed: Without a connector word, feedback reads as two unrelated facts (one about the wrong choice, one about the right answer). The magic words — *but, not, however, instead, so* — explicitly link the misconception to the correction. This is a structural rule, not a stylistic one.

---

### Tip N12: Never Start Feedback with "Right," "Wrong," "Almost," or "Try Again"

The platform automatically displays "Correct" or "Incorrect" and signals correctness with color. Do not duplicate that signal in your feedback text.

Wrong: "Right! The derivative is 2x."

Right: "The derivative of x² is 2x, found by applying the power rule."

Why this tip is needed: Authors instinctively echo the correctness signal because every classroom interaction begins that way. The redundancy wastes prime real estate at the top of the feedback — the place where the explanation should start. Skip the verdict; the platform already gave it.

---

### Tip N13: Never Say "You" in Feedback — and Never Diagnose the Student's Specific Mistake

Do not address the student as "you." Do not write feedback that assumes the student made a particular error ("This answer choice forgets to carry the…").

Wrong: "You forgot to carry the 2."

Right: "The correct calculation requires carrying the 2 through both terms."

Why this tip is needed: "You forgot…" assumes the student made the exact error the author imagined. They may have made a different mistake — or guessed. Phrasing feedback in third person and focusing on the math (not the student's process) avoids the awkward case of telling a student they did something they did not do.

---

### Tip N14: Every Answer Choice Gets Its Own Unique Feedback

Do not repeat the same feedback text across multiple answer choices. Even when distractors are similar, vary the feedback so each one targets its specific misconception.

Wrong: All three wrong choices get "Incorrect. The correct answer is 2x."

Right: Each wrong choice gets feedback explaining the specific error that produces that choice (sign error, missed exponent, applied wrong rule, etc.).

Why this tip is needed: Copy-paste feedback wastes the most powerful teaching moment in the question — the moment a student got it wrong. The student deserves to know why their specific answer was wrong, not just that a different answer was right.

---

### Tip N15: Hints Scaffold — Hint 1 Gets the Student ⅓ of the Way, Hint 2 Gets Them ⅔

When a question has two hints, they must form a ladder. Hint 1 nudges. Hint 2 commits. Together they should leave the student a small step from the answer, not at the answer.

Wrong:
Hint 1: "Use the chain rule."
Hint 2: "The chain rule is f'(g(x)) · g'(x)."

Right:
Hint 1: "Because (3x²+5)⁴ is a composition of functions, the chain rule applies."
Hint 2: "Use the chain rule with outer function f(u) = u⁴ and inner function g(x) = 3x²+5."

Why this tip is needed: Authors write hints as a single-effort task and do not think in fractions of progress. The result is two hints at the same level of help, or two hints that together give away the answer. The ⅓ / ⅔ scaffold turns hints into a progression.

---

### Tip N16: Hint Counts Are Question-Type-Specific

Different question types take different numbers of hints. Authors must know the rule for the type they are writing.

- Embedded Question (EQ), SA: 2 hints
- Follow-Up Question (FU), SA: 2 hints
- Homework Question (HW), SA: 1 hint
- Quiz Question, SA: 0 hints (no scaffolding)
- Final Exam Question, SA: 0 hints

Why this tip is needed: There is no universal "default number of hints." Authors writing a homework question who copy-paste structure from a follow-up question will accidentally double the hints. Authors writing a quiz question who carry over homework patterns will leave hints that should not be there. The count is part of the question type's identity.

---

### Tip N17: Avoid "Filler" Embedded Questions — EQs Must Hit the Lesson's Key Concept

Every embedded question must directly reinforce the central concept of the animated figure. Do not ask the student to perform trivial side calculations the figure could just show.

Wrong (in a chain rule lesson on x² + 2x cos(y) + 1 = 0):
EQ: "What is the derivative of 1?"
EQ: "What is the derivative of x²?"

Right:
EQ: "The term _____ requires the chain rule."

Why this tip is needed: Authors write filler EQs because they need an EQ at a specific point in the animation and the obvious calculations are easy to ask about. But every EQ is real estate. Spending it on a derivative the student already knows wastes the engagement, and worse, signals that the lesson is about easy material when the actual learning target is harder.

---

### Tip N18: One Concept Per Question — One Possible Correct Answer

Each question must test exactly one concept and have exactly one defensible correct answer. If a question tests two ideas at once, split it into two questions.

Wrong: A single SA question that requires the student to (1) find a derivative AND (2) evaluate it at a point AND (3) interpret the result.

Right: A multistep QS that breaks those into three connected steps, each with its own prompt and correct answer.

Why this tip is needed: Authors compound questions because they want efficiency or a "challenging" feel. The result is a question where a student can be 80% right and still get the whole thing wrong. Splitting compound questions into a multistep set gives partial credit, surfaces the exact step where the student got stuck, and matches the Learnvia scaffolding model.

---

### Tip N19: MC Answer-Choice Capitalization Depends on Where the Blank Falls

Capitalize the first letter of each answer choice — UNLESS the choice fills a blank that does not begin a sentence. Then lowercase.

Capitalized (blank starts the sentence):
Stem: "_____ is the first step in solving the equation."
Choices: "Distributing 3 on both sides" / "Dividing both sides by 3"

Lowercase (blank is mid-sentence):
Stem: "While solving the equation, the first step is to ____."
Choices: "use the one-to-one property" / "divide both sides by 3"

Why this tip is needed: Authors apply one rule to all questions, usually capitalizing every choice. The result reads grammatically wrong when the choice slots into a mid-sentence blank ("While solving the equation, the first step is to Use the one-to-one property"). The rule is mechanical but easy to miss.

---

### Tip N20: Long-Answer Questions: No Math-Heavy Typing

Students answering an LA question type into a plain text field with no virtual keyboard. Do not require lengthy equations, multiple notations, or symbol-heavy responses.

Wrong: "Use the limit definition of the derivative to find f'(x) for f(x) = 3x² + 2. Show all work."

Right: "Explain what the limit definition of the derivative represents in terms of slopes of secant lines."

Why this tip is needed: Authors design LA questions like exam problems where students would handwrite a multi-line solution. Typing math without a virtual keyboard is slow and error-prone. The right LA question asks for explanation, comparison, or interpretation — the kinds of answers that suit a text field.

---

### Tip N21: Multistep Question Sets Are Allowed Only in FU and HW

Multistep QS — a series of related questions building to a solution — are permitted only in Follow-Up sections and Homework sections. They are not allowed in Quizzes, EQs, or LAs as standalone constructs.

Why this tip is needed: Authors who love the multistep structure will reach for it everywhere. The platform restricts it to the two contexts where scaffolded teaching is the intent. Writing a multistep QS for a quiz means the work has to be redone.

---

### Tip N22: SA Test Values Are Required When the Answer Contains a Variable

For any SA question whose correct answer is an expression involving a variable, the author must supply 3 test values. The platform uses these to recognize mathematically equivalent answers.

Required:
- 3 test values
- Never use 0
- 1 and –1 are good defaults
- Include at least one large value (e.g., 1500 or 10,000)

Why this tip is needed: This is a platform-mechanics rule with no equivalent in any textbook. Without test values, the platform cannot accept "x² + 2x" and "2x + x²" as the same answer. Authors who skip test values cause student answers to be marked wrong when they are right.

---

### Tip N23: Set Tolerance to 0 for Exact Answers, .001 for "Round to 3 Decimal Places"

For SA numerical answers, tolerance must match what the prompt asks for.

- Exact answer (e.g., √2): tolerance 0
- "Round to 3 decimal places" (e.g., 1.414): tolerance 0.001
- "Round to the nearest tenth" (e.g., 2.2): tolerance 0.05 or as appropriate

Why this tip is needed: Authors set tolerance once and forget it. A tolerance of 0.01 on an exact-answer question lets the student type the wrong digits and still pass. A tolerance of 0 on a "round to 3 decimals" question rejects the right answer because of float arithmetic. The tolerance is part of writing the correct prompt.

---

### Tip N24: At Least One LA Question Per Lesson — Scaffold Up to It

Every lesson should include at least one long-answer question, preceded by scaffolding (short answers, multistep sets) that prepare the student to write the LA response.

Why this tip is needed: LA questions take students more time and effort, so authors under deadline skip them. The Questions Guide makes them required at a minimum cadence (one per lesson). Authors need to plan the LA into the lesson architecture from the start, not append it at the end as filler.

---

### Tip N25: Use Italics for Emphasis — Never Bold

When a word or phrase needs emphasis in a question stem, prompt, or feedback, italicize it. Do not bold.

Wrong: "The slope is **negative** on this interval."

Right: "The slope is *negative* on this interval."

(Note: Bolding *is* used for the key term inside a definition tag, which is its own structural marker — but not for in-prose emphasis.)

Why this tip is needed: Bolding pulls the eye too aggressively and clashes with the bold formatting reserved for defined terms. Italics is the universal academic convention for emphasis, and Learnvia is consistent with that convention.

---

## Quick Reference: All 65 Tips at a Glance

### Style Guide Tips (S1-S10)
| # | Title | One-Line Summary |
|---|-------|-----------------|
| S1 | Periods Outside Quotes | Commas and periods go outside quotation marks |
| S2 | Say "So" Not "Therefore" | Replace thus, hence, therefore with so |
| S3 | No Semicolons | Ban on semicolons in prose (exception: large-number lists) |
| S4 | Possessives Are OK | Don't over-correct the contraction ban — possessives are preferred |
| S5 | Drop "There Is/Are" | Start with the real subject |
| S6 | Punctuation Inside LaTeX | Use \text{.} inside math tags for mobile rendering |
| S7 | No "Below/Above" | Use "the following graph" not "the graph below" |
| S8 | Theorem vs. Rule Caps | Mean Value Theorem but chain rule |
| S9 | Ban "It" | Restate the noun even when "it" seems clear |
| S10 | No Comma in 4-Digit Numbers | Write 4389 not 4,389 |

### Authoring Guide Tips (A1-A10)
| # | Title | One-Line Summary |
|---|-------|-----------------|
| A1 | Hints Are Not Questions | Write declarative steps, not Socratic questions |
| A2 | Minimize "We" | Make the math object the subject |
| A3 | No Pronouns | No he, she, it, they, you — only we/us sparingly |
| A4 | Quick Learning Questions | Follow-ups are tutoring, not homework |
| A5 | "Ex:" Not "e.g." | Simpler abbreviation for target learners |
| A6 | Unique Values | Avoid repeated numbers in problems |
| A7 | Static Figure First | Design the static figure before the animation |
| A8 | Explain Correct Answers | Assume the student guessed right |
| A9 | Short MC Choices | Factor common text into the question stem |
| A10 | No Synonyms | One term per concept, always |

### Conflict Tips (C1-C20)
| # | Title | One-Line Summary |
|---|-------|-----------------|
| C1 | "We" in Captions | Acceptable in animation captions, minimize elsewhere |
| C2 | Active Definitions | Use "A function is..." not "is defined as..." |
| C3 | Definition Placement | Framing text or follow-up depends on the animation |
| C4 | "Thus" Is Banned | Style guide rule the authoring guide ignores |
| C5 | 8th Grade Reading Level | Concrete target only in the style guide |
| C6 | Semicolons Clarified | Banned in prose, required in large-number lists |
| C7 | Question Format | Blanks for learning, imperative for assessment |
| C8 | Friendly Without Contractions | Warmth from structure, not apostrophes |
| C9 | Pronoun Hierarchy | Clear rules for we, it, you, they |
| C10 | Introductory Clause Exception | Only "When [procedure]" clauses are acceptable |
| C11 | Calculation Annotations | Banned in lessons, allowed in hints |
| C12 | Accessibility in Animations | Color needs a backup differentiator |
| C13 | Quotation Punctuation | Non-standard rule, easy to miss |
| C14 | Question Structure Source | Authoring guide only |
| C15 | Active Voice Without "We" | Math object as subject solves both rules |
| C16 | "This" + Noun Is OK | Bare "This" is banned, "This equation" is fine |
| C17 | "We" in Animation Questions | OK in embedded, avoid in standalone |
| C18 | Em-Dash Ban | Style guide bans what authoring guide models |
| C19 | People Possessives | Role-based possessives for word problems |
| C20 | "Because" Not "Since" | Style guide rule the authoring guide violates |

### Questions Guide Tips (N1-N25)
| # | Title | One-Line Summary |
|---|-------|-----------------|
| N1 | MC Prompts Are Statements | Fill-in-the-blank, never "What is…?" |
| N2 | Choices Continue the Stem Grammatically | Stem + choice must read as one sentence |
| N3 | Parallel Length | A long correct choice gives itself away |
| N4 | Parallel Construction | All gerunds OR all noun phrases — never mix |
| N5 | Don't Echo Stem Language in a Choice | Repeated wording cues the answer |
| N6 | No NOT / EXCEPT / Always / Sometimes / Never | Banned constructions in prompts |
| N7 | No Opposites or Absolutes in Choices | Both create cognitive cues unrelated to math |
| N8 | Distractors = Misconceptions | Each wrong choice maps to a real student error |
| N9 | Randomize Answer Order | Alphabetize or sort by value |
| N10 | Correct Feedback: Restate, Then Explain | Assume the student guessed |
| N11 | Incorrect Feedback Uses Magic Words | but, not, however, instead, so |
| N12 | No "Right" / "Wrong" / "Almost" / "Try Again" | Platform handles the verdict |
| N13 | No "You" — and No Diagnosing Mistakes | Third person, focused on math |
| N14 | Unique Feedback per Choice | Never copy-paste across distractors |
| N15 | Hints Scaffold ⅓ → ⅔ | Hint 1 nudges, Hint 2 commits |
| N16 | Hint Counts by Question Type | EQ=2, FU=2, HW=1, Quiz=0 |
| N17 | No Filler EQs | EQ must hit the lesson's key concept |
| N18 | One Concept, One Correct Answer | Split compound questions into a multistep set |
| N19 | Choice Capitalization Follows the Blank | Capital if blank starts the sentence, lowercase if mid-sentence |
| N20 | LA Questions: No Math-Heavy Typing | No virtual keyboard — ask for explanation, not equations |
| N21 | Multistep QS: FU and HW Only | Not allowed in EQ, Quiz, or standalone LA |
| N22 | SA Variable Answers Need 3 Test Values | Never 0; use 1, –1, and a large value |
| N23 | Tolerance Matches the Prompt | 0 for exact, 0.001 for "round to 3 decimals" |
| N24 | At Least One LA Per Lesson | Scaffold up to it from SA and multistep |
| N25 | Italics for Emphasis, Not Bold | Bold is reserved for defined terms |
