# Categorized Real Examples from Review Logs

Extracted from modules 5.6 and 5.7 human review logs. Each example categorized by competency and assigned severity based on student impact.

---

## Style: Mechanical Compliance

### Severity 2 (Minor)

**Example 1: LaTeX spacing**
- **Section:** Animated Figure, Embedded question
- **Issue:** Should a \ be added before the comma between the 2 and the dt in the following? F(x) = \int_0^x 2,dt\text{,}
- **Recommended Edit:** If appropriate, add \ before the comma between the 2 and dt: F(x) = \int_0^x 2\,dt\text{,}
- **Student Impact:** Minor readability issue in mathematical notation
- **Source:** 5.6 CE, line 10

**Example 2: LaTeX spacing error showing as text**
- **Section:** Homework Problem
- **Issue:** the spacing command ";" is showing as text in all parts of this question.
- **Recommended Edit:** Adjust LaTeX to fixing spacing; remove ";" from integrals
- **Student Impact:** Confusing display error that distracts from content
- **Source:** 5.6 CE, line 31

---

## Style: Consistency

### Severity 3 (Moderate)

**Example 1: Inconsistent terminology**
- **Section:** Framing Text (Global)
- **Issue:** "Fundamental Theorem of Calculus" appears in several different ways in this module (with and without "Part 1", with and without a comma before "Part 1"). All are similar and corrections may not be required, but consider reviewing for consistency.
- **Recommended Edit:** Review and update all instances of "Fundamental Theorem of Calculus, Part 1" for consistency if appropriate.
- **Student Impact:** Inconsistent terminology can confuse students about whether these refer to the same concept
- **Source:** 5.6 CE, line 30

**Example 2: Inconsistent theorem naming**
- **Section:** Framing Text
- **Issue:** Final sentence describes theorem as "Fundamental Theorem of Calculus (FTC)" but rest of lesson describes it as "Fundamental Theorem of Calculus, Part 1" and the abbreviation "FTC" only appears in one follow up question.
- **Recommended Edit:** Replace "Fundamental Theorem of Calculus (FTC)" with "Fundamental Theorem of Calculus, Part 1" if appropriate.
- **Student Impact:** Introducing an abbreviation that's not consistently used creates cognitive overhead
- **Source:** 5.6 CE, line 25

---

## Style: Accessibility

### Severity 3 (Moderate)

**Example 1: Reading level too high**
- **Section:** Framing Text
- **Issue:** Reading level is 11.09.
- **Recommended Edit:** If possible, simplify vocabulary and sentence construction to bring this down to within desired 8-10th grade level range.
- **Student Impact:** Content inaccessible to target audience of struggling students
- **Source:** 5.6 CE, line 23

**Example 2: Pronoun ambiguity**
- **Section:** Follow-Up Question
- **Issue:** Can "its" be replaced with f(x)'s in the following sentence? The Fundamental Theorem of Calculus, Part 2 connects the definite integral of f(x) with the values of its antiderivative at the endpoints.
- **Recommended Edit:** Replace "its" with "f(x)'s" if appropriate: ...with the values of f(x)'s antiderivative at the endpoints.
- **Student Impact:** Pronoun "its" may be ambiguous; explicit reference clearer for struggling students
- **Source:** 5.6 CE, line 16

**Example 3: Ambiguous pronoun**
- **Section:** Animated Figure, Embedded Question
- **Issue:** To what is "it" referring in the following sentence? We need to double it because f is even.
- **Recommended Edit:** Replace "it" for clarity.
- **Student Impact:** Unclear pronoun reference forces students to backtrack and re-read
- **Source:** 5.6 CE, line 19

---

## Style: Punctuation & Grammar

### Severity 2 (Minor)

**Example 1: Unclear sentence**
- **Section:** Framing Text
- **Issue:** The end of the sentence is unclear (see bold): In this lesson, we will explore how to use the FTC together with the chain rule to find derivatives of integrals with upper a function as an upper limit.
- **Recommended Edit:** Revise sentence for clarity.
- **Student Impact:** Grammatical error ("upper a function") confuses meaning
- **Source:** 5.6 CE, line 12

---

## Authoring: Conceptual Clarity

### Severity 3 (Moderate)

**Example 1: Undefined jargon**
- **Section:** Follow-Up Question
- **Issue:** To what does "property" refer? The word "property" hasn't been used in this lesson so far. Will students understand what property means in this context?
- **Recommended Edit:** Replace the word property if appropriate, x2.
- **Student Impact:** Undefined mathematical jargon confuses students who don't have context
- **Source:** 5.6 CE, line 14

**Example 2: Jargon without definition**
- **Section:** Follow-Up Question
- **Issue:** Uses the term "splitting"; will students know what this means in this context?
- **Recommended Edit:** Replace the word splitting if appropriate.
- **Student Impact:** Technical term used without definition or context
- **Source:** 5.6 CE, line 15

**Example 3: Jargon consistency**
- **Section:** Homework Problem
- **Issue:** As noted earlier, will students understand what "split" means in this context? If replaced earlier in the lesson, replace here as well.
- **Recommended Edit:** Replace the word split if appropriate.
- **Student Impact:** Same jargon issue appears multiple times in module
- **Source:** 5.6 CE, line 21

**Example 4: Undefined term**
- **Section:** Homework Problem
- **Issue:** Will students know "the sum property of integrals"? A google search doesn't net any results. Does this go by another name, like "sum rule"?
- **Recommended Edit:** Replace "the sum property of integrals" if appropriate. Note that it is referred to a "property" later in the explanation as well.
- **Student Impact:** Non-standard terminology that students won't recognize
- **Source:** 5.6 CE, line 22

**Example 5: Ambiguous wording**
- **Section:** Follow-Up Question
- **Issue:** The use "part" is confusing here, since it makes me think of the FTC Part 1 or Part 2. Can "part" be replaced with "problem" or "question" in the following? "In the previous part, we considered..."
- **Recommended Edit:** Replace "part" with "question" or "problem" or "question set" as appropriate
- **Student Impact:** Word choice creates confusion with lesson-specific terminology
- **Source:** 5.6 CE, line 20

---

## Authoring: Conceptual Clarity (Missing Definitions)

### Severity 3 (Moderate)

**Example 1: Missing definition**
- **Section:** Framing Text
- **Issue:** Should the chain rule be defined/redefined within the framing text?
- **Recommended Edit:** Add definition if appropriate.
- **Student Impact:** References concept students may not recall; definition would help
- **Source:** 5.6 CE, line 13

---

## Authoring: Pedagogical Flow

### Severity 4 (Major)

**Example 1: Forward reference**
- **Section:** Animated Figure, Embedded question
- **Issue:** Question hint and explanation both refer to the "Fundamental Theorem of Calculus Part 1," which students do not learn until the next lesson.
- **Recommended Edit:** Rewrite Hint 1 and Explanation if appropriate.
- **Student Impact:** References concept students haven't learned yet; breaks scaffolding
- **Source:** 5.6 CE, line 11

---

## Authoring: Assessment Quality

### Severity 4 (Major)

**Example 1: Missing explanations**
- **Section:** Follow-Up Question
- **Issue:** The answers do not include explanations.
- **Recommended Edit:** Add explanations.
- **Student Impact:** Students can't learn from mistakes without explanations
- **Source:** 5.7 Beta, resolved

**Example 2: Missing explanation**
- **Section:** Follow-Up Question
- **Issue:** No explanation given in answer.
- **Recommended Edit:** [blank]
- **Student Impact:** Same as above
- **Source:** 5.7 Beta, resolved

### Severity 3 (Moderate)

**Example 1: Question format inconsistency**
- **Section:** Animated Figure, Embedded question
- **Issue:** Prompt is in the form of a question instead of a statement. <question>How many liters of water is in the tank after 3\text{ minutes?}</question>
- **Recommended Edit:** Rewrite question into statement form if possible, such as: After <m>3\text{ minutes,}</m> <m>\underline{\phantom{XXXXXX}}</m> <m>\text{liters}</m> of water is in the tank.
- **Student Impact:** Inconsistent question format may confuse students about expectations
- **Source:** 5.6 CE, line 9

**Example 2: Misaligned content**
- **Section:** Follow-Up Question
- **Issue:** I looks like most of these were copied and pasted from 5.7.3 as displacement questions, but this is the total distance section.
- **Recommended Edit:** [blank]
- **Student Impact:** Questions don't match lesson topic; students practice wrong concept
- **Source:** 5.7 Beta, resolved

**Example 3: Weak question design**
- **Section:** Homework Problem
- **Issue:** Q1 asks to verify a function is even. Q2 should probably use this fact. It only asks for a definite integral on [0,a] which does not rely on even/odd.
- **Recommended Edit:** Rewrite Q2 to evaluate the integral on the symmetric interval [-a,a].
- **Student Impact:** Questions don't build on each other; missed pedagogical opportunity
- **Source:** 5.6 Beta, resolved

---

## Summary Statistics

**Total Text Issues Extracted:** 22
- Severity 4 (Major): 3 issues
- Severity 3 (Moderate): 11 issues  
- Severity 2 (Minor): 3 issues
- Unassigned: 5 issues (context-dependent)

**Distribution by Competency:**
- Style: Accessibility (3)
- Style: Consistency (2)
- Style: Mechanical Compliance (2)
- Style: Punctuation & Grammar (1)
- Authoring: Conceptual Clarity (6)
- Authoring: Pedagogical Flow (1)
- Authoring: Assessment Quality (6)

**Note:** Visual issues (11 total) were excluded as out of scope for text reviewers.
