# Section 8: Calculus-Specific Pedagogical Principles
**For Learnvia Authoring Guidelines**
**Research-Backed Strategies for Teaching Calculus I-IV to Non-Traditional Learners**

---

## Purpose of This Section

This section provides calculus-specific pedagogical guidance to supplement the general authoring principles in Sections 1-7. Research demonstrates that calculus education requires specialized approaches beyond general mathematics teaching, particularly for non-traditional learners who may be studying alone, have low confidence, or come from underserved communities with limited mathematical preparation.

**Key Research Finding:** Active, student-centered calculus instruction results in significantly greater learning outcomes compared to traditional lecture methods, with **particularly profound benefits for students from underrepresented populations in STEM** (FIU Study, 2023; Science, 2023).

---

## 8.1 The Rule of Four: Multiple Representations Requirement

### Core Principle

**Every calculus concept MUST be presented in at least three, preferably four, representations:**

1. **Graphical:** Visual understanding of the concept
2. **Numerical:** Table-based or computational reasoning
3. **Symbolic/Algebraic:** Formula manipulation and notation
4. **Verbal:** Natural language description of meaning

This approach, codified in AP Calculus standards and supported by mathematics education research, is called the **"Rule of Four"**.

---

### Why This Matters for Non-Traditional Learners

**Research Finding:** Students demonstrate an overwhelming reliance on algebraic representations, even on tasks for which a graphical representation would be more appropriate. Students with weak algebraic manipulation skills can still grasp basic calculus concepts when given access to multiple representations (Calculus Reform Research).

**For struggling learners:** Multiple representations provide **multiple pathways to understanding**. If a student doesn't understand the algebraic derivative, they may grasp it through the graphical slope interpretation or numerical rate-of-change table.

---

### Implementation Guidelines by Concept

#### **A. Derivatives**

**Graphical:**
- Show function graph with tangent line at a point
- Visualize slope of tangent line changing as point moves along curve
- Animate secant line approaching tangent line
- Display slope triangles to show rise/run

**Numerical:**
- Table showing difference quotient: (f(x+h) - f(x))/h for decreasing h values
- Table of x, f(x), and f'(x) values side-by-side
- Rate-of-change calculation from position/time data

**Symbolic:**
- Limit definition: lim[h→0] (f(x+h) - f(x))/h
- Power rule: d/dx(x^n) = nx^(n-1)
- Derivative notation: f'(x), dy/dx, df/dx

**Verbal:**
- "The derivative measures the instantaneous rate of change"
- "The derivative is the slope of the tangent line at a point"
- "The derivative tells us how fast f is changing at x"

**Example Lesson Structure:**
1. **Intro:** Verbal motivation (car's instantaneous speed vs. average speed)
2. **Graphical:** Animated figure showing secant lines approaching tangent
3. **Numerical:** Table computing (f(x+h) - f(x))/h with h = 0.1, 0.01, 0.001
4. **Symbolic:** Introduce limit definition, then derivative rules
5. **Practice:** Questions requiring all three representations

---

#### **B. Integrals**

**Graphical:**
- Area between curve and x-axis (shaded regions)
- Riemann rectangles (left, right, midpoint) under curve
- Animate rectangles increasing in number, approaching exact area
- Show positive areas (above x-axis) vs. negative areas (below x-axis)

**Numerical:**
- Table showing x, f(x), and rectangle areas
- Calculate Riemann sum: Σ f(xi)Δx
- Show sum approaching integral value as n increases

**Symbolic:**
- Definite integral notation: ∫[a to b] f(x)dx
- Antiderivative (Fundamental Theorem connection)
- Integration rules

**Verbal:**
- "The integral measures the signed area under a curve"
- "The integral accumulates the total effect of a rate of change"
- "Integration is the reverse process of differentiation"

**Critical Connection:** Emphasize that **integral = area** is the definition (Riemann sum), while **integral = antiderivative** is a powerful theorem (FTC), not a definition. Students often confuse these.

---

#### **C. Limits**

**Graphical:**
- Function graph with point approaching a value
- Show "hole" in graph (removable discontinuity) where limit exists but function undefined
- Asymptotic behavior (horizontal, vertical asymptotes)

**Numerical:**
- Table showing x values approaching target from left and right
- Corresponding f(x) values approaching limit (or not)
- Demonstrate one-sided limits

**Symbolic:**
- Limit notation: lim[x→a] f(x) = L
- Limit laws (sum, product, quotient rules)
- Algebraic limit evaluation techniques

**Verbal:**
- "The limit is the value the function approaches, not necessarily reaches"
- "The limit can exist even when the function is undefined at that point"
- "Limits describe function behavior near a point"

---

### Common Author Mistakes to Avoid

❌ **Don't:** Teach derivative rules first, then show graphs as "illustrations"
✅ **Do:** Start with graphical/numerical intuition, THEN introduce symbolic rules

❌ **Don't:** Present only one representation and call it complete
✅ **Do:** Require students to translate between representations in questions

❌ **Don't:** Assume students can mentally translate between representations
✅ **Do:** Explicitly guide translation: "This graph shows what we calculated in the table"

---

## 8.2 Common Calculus Misconceptions

### Overview

Calculus has well-documented misconceptions that persist even among students who can perform calculations correctly. **Addressing misconceptions explicitly** is more effective than hoping students will "figure it out." For non-traditional learners with low confidence, unaddressed misconceptions can derail understanding entirely.

**Teaching Strategy:** When introducing a concept prone to misconception, **explicitly state the misconception and why it's wrong** before students develop it.

---

### Top 10 Calculus Misconceptions with Teaching Strategies

---

#### **Misconception #1: "The derivative is just the slope"**

**The Problem:**
Students think "derivative = slope of a line" and miss that it's the **instantaneous rate of change** (slope of tangent line, not secant).

**Why Students Think This:**
Early algebra emphasis on "slope = rise/run" makes students default to secant line thinking.

**The Reality:**
The derivative is the **limit** of slopes of secant lines. It's the slope of the tangent line at a single point, representing instantaneous rate, not average rate.

**Teaching Strategy:**
1. **Start with average rate:** Show secant line between two points, calculate slope
2. **Zoom in:** Make the two points closer together, recalculate slope
3. **Take the limit:** Animate points getting infinitely close → tangent line emerges
4. **Explicit statement:** "The derivative is NOT the slope of the secant line (that's average rate). The derivative is the LIMIT of those slopes as the interval shrinks to zero—that's instantaneous rate."

**Assessment Question:**
*"Explain the difference between average rate of change (secant line slope) and instantaneous rate of change (derivative). Why does the derivative require a limit?"*

---

#### **Misconception #2: "The limit equals the function value"**

**The Problem:**
Students assume lim[x→a] f(x) = f(a) always. This fails at discontinuities.

**Why Students Think This:**
For continuous functions (most early examples), the limit DOES equal the function value, reinforcing the misconception.

**The Reality:**
lim[x→a] f(x) describes function behavior **near** a, not **at** a. The limit can exist even when f(a) is undefined or different.

**Teaching Strategy:**
1. **Show removable discontinuity early:** Use f(x) = (x²-1)/(x-1) at x=1
   - Graph has a "hole" at x=1
   - lim[x→1] f(x) = 2 (limit exists)
   - f(1) is undefined (function doesn't exist there)
2. **Explicit statement:** "The limit asks 'What value is f approaching?' NOT 'What value does f equal?'"
3. **Emphasize:** Continuity is a SPECIAL CASE where limit = function value

**Assessment Questions:**
- *"Can lim[x→2] f(x) exist if f(2) is undefined? Explain."*
- *"Give an example where lim[x→a] f(x) ≠ f(a)."*

---

#### **Misconception #3: "dx is a number you can cancel"**

**The Problem:**
Students treat "dx" as an algebraic variable that cancels: dy/dx · dx = dy

**Why Students Think This:**
The Leibniz notation dy/dx looks like a fraction, and u-substitution seems to "cancel" dx terms.

**The Reality:**
"dx" is part of the derivative notation, not a standalone number. It represents "with respect to x" or an infinitesimal (limit concept).

**Teaching Strategy:**
1. **Early warning:** When introducing dy/dx notation, state: "This LOOKS like a fraction but isn't. It's a single symbol meaning 'derivative of y with respect to x.'"
2. **Alternative notations:** Show f'(x) and d/dx[f(x)] to reinforce it's an operator
3. **When u-substitution works:** Explain it's a consequence of the chain rule, not fraction cancellation
4. **Explicit statement:** "You can't cancel dx any more than you can cancel the 'lo' in 'log' or the 'sin' in 'sine'."

**Assessment Question:**
*"Why is dy/dx considered a single notation rather than a fraction? What does 'dx' mean?"*

---

#### **Misconception #4: "The integral IS the antiderivative"**

**The Problem:**
Students conflate two distinct concepts: integral (area) and antiderivative (reverse derivative).

**Why Students Think This:**
The Fundamental Theorem of Calculus connects them so elegantly that students think they're the same thing.

**The Reality:**
- **Definite integral:** Signed area under curve (Riemann sum limit)
- **Antiderivative:** Function whose derivative is f
- **FTC:** These two concepts are connected by a profound theorem (not a definition)

**Teaching Strategy:**
1. **Teach integrals first via Riemann sums** (area definition)
2. **Teach antiderivatives separately** (reverse derivative)
3. **Present FTC as miraculous connection:** "Amazingly, calculating area is the same as finding antiderivatives! This is NOT obvious—it's a deep theorem."
4. **Explicit statement:** "The integral is defined as area. The antiderivative is defined as reverse derivative. The FTC tells us these are connected."

**Assessment Question:**
*"Explain the difference between 'the definite integral of f' and 'the antiderivative of f'. How does the Fundamental Theorem of Calculus relate them?"*

---

#### **Misconception #5: "Chain rule is just simple multiplication"**

**The Problem:**
Students apply the chain rule as rote memorization without understanding function composition.

**Why Students Think This:**
Chain rule formulas look like simple multiplication: (f∘g)' = f'(g) · g'

**The Reality:**
Chain rule applies when functions are **composed** (nested). Students must identify outer and inner functions.

**Teaching Strategy:**
1. **Review composition first:** Spend time on f(g(x)) notation before chain rule
2. **Use concrete examples:** Start with h(x) = (3x + 1)²
   - Identify: outer function f(u) = u², inner function g(x) = 3x + 1
   - State: h = f(g(x)), so h' = f'(g(x)) · g'(x)
3. **Build complexity gradually:**
   - Single composition: (3x+1)²
   - Nested composition: sin(x²)
   - Multiple chain rule: sin(e^(3x))
4. **Explicit statement:** "Chain rule applies when one function is inside another. Always identify outer and inner functions first."

**Assessment Questions:**
- *"For h(x) = (5x² + 2)³, identify the outer and inner functions before finding h'(x)."*
- *"Explain why sin(x²) requires the chain rule but x² sin(x) requires the product rule."*

---

#### **Misconception #6: "Riemann sums—left/right/midpoint—which is correct?"**

**The Problem:**
Students think one endpoint choice is "right" and others are "wrong."

**Why Students Think This:**
Teachers present multiple methods without explaining they're all approximations.

**The Reality:**
All endpoint choices are **approximations** of the true area. They converge to the same limit (true area) as n→∞. Left/right differ in over/underestimate depending on whether function is increasing/decreasing.

**Teaching Strategy:**
1. **Visual demonstration:** Show increasing function with left, right, and midpoint rectangles
   - Left endpoint: underestimate (rectangles below curve)
   - Right endpoint: overestimate (rectangles above curve)
   - Midpoint: better approximation (balances error)
2. **Animate limit:** Show n=5, n=10, n=50, n=100 rectangles—all approaches converge
3. **Explicit statement:** "All three methods approximate the area. The limit as n→∞ is the same for all methods—that's the true area (definite integral)."

**Assessment Question:**
*"For an increasing function, will left-endpoint Riemann sum overestimate or underestimate the true area? Explain with a sketch."*

---

#### **Misconception #7: "Related rates—all variables are changing"**

**The Problem:**
Students differentiate constants as if they're variables, or miss which quantities are changing with time.

**Why Students Think This:**
Related rates problems have multiple quantities, and students don't distinguish variables (change over time) from constants (fixed values).

**The Reality:**
Only quantities that **change with time** are variables. Constants (like radius of a fixed circle) don't get differentiated with respect to time.

**Teaching Strategy:**
1. **Notation convention:** Mark time-dependent quantities explicitly: V(t), r(t), h(t)
2. **Table of knowns:** Before differentiating, list:
   - Variables (changing with time): "r is increasing"
   - Constants (given values): "radius = 5 ft"
   - Target: "Find dV/dt when r = 3"
3. **Differentiate equation:** Implicitly differentiate with respect to t, treating constants as constants
4. **Explicit statement:** "Only quantities changing over time get a dt in their derivative. Fixed values are constants."

**Assessment Question:**
*"A ladder 10 ft long leans against a wall. The bottom slides away at 2 ft/sec. Identify: (a) What quantities are variables? (b) What quantities are constants? (c) What are you solving for?"*

---

#### **Misconception #8: "Tangent line touches the curve only once"**

**The Problem:**
Students think "tangent" means "touches at exactly one point."

**Why Students Think This:**
Early geometry teaches "tangent to circle" which does touch at one point only.

**The Reality:**
A tangent line can intersect the curve at multiple points. "Tangent" means it has the same slope as the curve at the point of tangency, not that it only touches once.

**Teaching Strategy:**
1. **Show counterexample early:** Graph y = x³ with tangent line at x=0 (y=0). The tangent line y=0 crosses the curve at x=0 only, but show tangent to sin(x) at x=0 (y=x) which crosses at multiple points.
2. **Better example:** y = x³ - 3x, tangent line at x=1 crosses the curve three times
3. **Explicit statement:** "Tangent line means 'same slope at that point,' not 'touches once.'"

**Assessment Question:**
*"True or False: A tangent line to a curve can intersect the curve at more than one point. Explain."*

---

#### **Misconception #9: "Concavity means 'increasing faster'"**

**The Problem:**
Students confuse f'' > 0 (concave up) with f' > 0 (increasing).

**Why Students Think This:**
Informal language like "the graph is curving upward" blurs the distinction between increasing and concave up.

**The Reality:**
- **f' > 0:** Function is increasing (output values rising)
- **f'' > 0:** Function is concave up (rate of change is increasing, graph curves like ∪)
- A function can be decreasing (f' < 0) and still concave up (f'' > 0)—Ex: f(x) = -x² + 5x on (2.5, ∞)

**Teaching Strategy:**
1. **Separate lessons:** Teach increasing/decreasing (first derivative test) BEFORE concavity (second derivative test)
2. **Four-quadrant visual:** Show 4 cases:
   - f' > 0, f'' > 0: Increasing and concave up
   - f' > 0, f'' < 0: Increasing and concave down
   - f' < 0, f'' > 0: Decreasing and concave up ← counterintuitive case
   - f' < 0, f'' < 0: Decreasing and concave down
3. **Explicit statement:** "Concave up means 'rate of change is increasing' (f'' > 0), NOT 'function is increasing' (f' > 0)."

**Assessment Question:**
*"Sketch a function that is decreasing but concave up. Explain why this is possible."*

---

#### **Misconception #10: "The definite integral is always positive (area is always positive)"**

**The Problem:**
Students think ∫[a to b] f(x)dx equals "area" and area must be positive.

**Why Students Think This:**
Early examples use functions above the x-axis, where integral = area (positive).

**The Reality:**
The definite integral calculates **signed area**: positive above x-axis, negative below x-axis. The integral can be negative, zero, or positive.

**Teaching Strategy:**
1. **Show mixed-area graph early:** Function crossing x-axis (like sin(x) from 0 to 2π)
2. **Calculate signed area:** ∫[0 to π] sin(x)dx = 2 (positive area above), ∫[π to 2π] sin(x)dx = -2 (negative area below), total = 0
3. **Distinguish:** "Integral" (signed area) vs. "Total area" (absolute value of areas)
4. **Explicit statement:** "The definite integral is SIGNED area. Area below the x-axis counts as negative."

**Assessment Question:**
*"If ∫[0 to 5] f(x)dx = -3, what does this tell you about the graph of f?"*

---

### Summary Table: Misconceptions Quick Reference

| Misconception | Reality | Key Teaching Point |
|---------------|---------|-------------------|
| Derivative is just slope | Derivative is limit of slopes (instantaneous rate) | Start with secant, take limit to tangent |
| Limit equals function value | Limit describes behavior near point, not at point | Show removable discontinuity early |
| dx is a number | dx is notation, part of derivative symbol | Emphasize it's not a fraction |
| Integral IS antiderivative | They're connected by FTC (theorem, not definition) | Teach Riemann sums first, antiderivatives separately |
| Chain rule is multiplication | Applies to composed functions (nested) | Review composition first, identify inner/outer |
| One Riemann method is "right" | All are approximations, converge to same limit | Visual: show all methods approaching true area |
| All variables change | Only time-dependent quantities are variables | Mark variables with (t), constants without |
| Tangent touches once | Tangent means same slope, not one intersection | Show cubic tangent crossing curve |
| Concave up means increasing | f'' > 0 is about rate of change, not values | Separate f' (increasing) from f'' (concavity) |
| Integral always positive | Signed area: positive above, negative below x-axis | Show function crossing x-axis early |

---

## 8.3 Conceptual vs. Procedural Understanding Balance

### The Problem

**Research Finding:** Students frequently demonstrate procedural fluency (can execute derivative rules) without conceptual understanding (can't explain what a derivative means). Students with weak conceptual understanding struggle to transfer knowledge to new contexts or real-world applications.

**Impact on Non-Traditional Learners:** Students may pass tests by memorizing algorithms but lack the understanding to apply calculus to their intended fields (engineering, biology, economics), leading to attrition from STEM majors.

---

### The Difference

**Procedural Knowledge:**
- Executing algorithms correctly
- Applying rules mechanically
- Ex: "Find d/dx(3x² + 5x)" → Answer: "6x + 5" ✓

**Conceptual Knowledge:**
- Understanding WHY rules work
- Interpreting results meaningfully
- Ex: "What does f'(3) = 7 mean for the graph of f?" → Answer: "At x=3, the tangent line slope is 7, meaning f is increasing at a rate of 7 units of output per unit of input"

---

### Balanced Teaching Approach

#### **Strategy 1: Teach the "Why" Before the "How"**

❌ **Don't introduce rules without motivation:**
> "The power rule says d/dx(x^n) = nx^(n-1). Let's practice applying it."

✅ **Do provide conceptual foundation first:**
> "Let's see what happens when we differentiate x² using the limit definition. [Work through lim[h→0] ((x+h)² - x²)/h]. Notice the exponent decreases and becomes the coefficient! This pattern holds for any power—that's the power rule."

---

#### **Strategy 2: Alternate Between Computation and Interpretation**

Structure lessons as: Compute → Interpret → Compute → Interpret

**Example Sequence for Derivative Rules:**

1. **Compute:** Find f'(x) if f(x) = x³ - 2x + 5
   - Answer: f'(x) = 3x² - 2

2. **Interpret:** What does f'(2) = 10 tell you about the graph of f?
   - Answer: At x=2, the function is increasing at a rate of 10 (tangent line slope is 10)

3. **Compute:** Where is f increasing? (Solve f'(x) > 0)
   - Answer: 3x² - 2 > 0 → x > √(2/3) or x < -√(2/3)

4. **Interpret:** Explain why the intervals where f' > 0 are where f is increasing.
   - Answer: Positive derivative means positive slope, which means function values are rising

---

#### **Strategy 3: Include Conceptual Questions in Every Question Set**

**For every computational question, include a paired conceptual question:**

**Computational:**
- "Find the derivative of f(x) = sin(x²)"

**Conceptual:**
- "Explain why f(x) = sin(x²) requires the chain rule but g(x) = sin(x) · x² requires the product rule"

**Computational:**
- "Evaluate ∫[0 to 4] (x² - 4)dx"

**Conceptual:**
- "The integral ∫[0 to 4] (x² - 4)dx equals 5.33. Explain geometrically what this value represents and why it's positive even though part of x² - 4 is below the x-axis."

---

#### **Strategy 4: Use "Explain Your Answer" Follow-ups**

After computational questions, add:
- "Explain what your answer means in context."
- "Describe how you knew which rule to use."
- "Why does this approach work?"

**Example:**
- **Question:** Find the critical points of f(x) = x³ - 3x + 1
- **Answer:** x = -1 and x = 1 (solve f'(x) = 0)
- **Follow-up:** "Explain what a critical point is and why setting f'(x) = 0 finds them."

---

### Assessment Design for Balanced Understanding

#### **Don't Only Test Procedures:**

❌ Typical procedural test:
1. Find d/dx(5x⁴ + 3x² - 7)
2. Find d/dx(sin(3x))
3. Find d/dx((2x + 1)³)
4. [10 more derivative computations]

**Problem:** Students can pass by memorizing rules without understanding.

---

#### **Do Balance Computational and Conceptual Questions:**

✅ Balanced test:
1. **Computation:** Find f'(x) if f(x) = x³ - 6x² + 9x
2. **Interpretation:** If g'(5) = -2, what does this tell you about the graph of g at x=5?
3. **Application:** A ball's height is h(t) = -16t² + 64t. Find h'(t) and explain what h'(2) represents.
4. **Comparison:** Explain the difference between average rate of change and instantaneous rate of change.
5. **Computation:** Find all critical points of f(x) = x⁴ - 4x³
6. **Conceptual:** Why do critical points occur where f'(x) = 0? (Explain graphically or algebraically)

**Result:** Tests true understanding, not just memorization.

---

### Common Procedural-Only Teaching Pitfalls

**Pitfall 1:** Teaching derivative rules without ever graphing functions
**Fix:** Always show graphical interpretation alongside symbolic work

**Pitfall 2:** All practice problems are "find the derivative" style
**Fix:** Include "given f'(x), sketch possible f(x)" and interpretation questions

**Pitfall 3:** Optimization problems as pure algebra exercises
**Fix:** Use real-world contexts requiring setup (modeling step) not just calculus

**Pitfall 4:** Never asking "why does this work?"
**Fix:** Regularly ask students to explain reasoning, not just produce answers

---

## 8.4 Scaffolding for Calculus Complexity

### Core Principle

Calculus topics have **prerequisite dependencies**. Teaching advanced topics before students master foundations leads to confusion and failure, especially for non-traditional learners without strong mathematical background.

**Research Finding:** Reform calculus approaches that scaffold complexity and ensure prerequisite mastery reduce attrition among underrepresented STEM students.

---

### Prerequisites by Major Topic

#### **Chain Rule Scaffolding Sequence**

**DON'T** teach chain rule immediately after basic derivative rules. Students need composition mastery first.

**DO** follow this sequence:

1. **Function Composition Review (Pre-Calculus)**
   - Notation: f(g(x)), composition as "substitution"
   - Practice: Given f(x) = x² and g(x) = 3x+1, find f(g(x))
   - Identify inner and outer functions

2. **Basic Derivative Rules (Week 1-2 of Calculus)**
   - Power rule: d/dx(x^n) = nx^(n-1)
   - Constant multiple rule
   - Sum/difference rule

3. **Concrete Composition Examples (Week 3)**
   - f(x) = (3x + 1)² → Recognize as (inner)²
   - Explicitly state: "This is x² with '3x+1' substituted for x"
   - Differentiate using chain rule with verbal guidance

4. **General Chain Rule (Week 4)**
   - Formula: d/dx[f(g(x))] = f'(g(x)) · g'(x)
   - Identify outer f, inner g for various examples
   - Practice distinguishing chain rule vs. product rule situations

5. **Multiple Compositions (Week 5+)**
   - Nested functions: sin(e^(3x))
   - Repeated chain rule applications

**Assessment Checkpoint:** Before introducing general chain rule, verify students can:
- Identify composition: "Is h(x) = (5x² + 2)³ a composition? If so, what are f and g?"
- Recognize when chain rule applies vs. product rule

---

#### **Optimization Scaffolding Sequence**

**DON'T** jump to applied optimization (maximize area, minimize cost) before students understand critical points conceptually.

**DO** follow this sequence:

1. **Critical Points Concept (First Derivative Test)**
   - Definition: Points where f'(x) = 0 or f'(x) undefined
   - Why critical: Derivative changes sign → local max/min possible
   - Find critical points algebraically

2. **Local Extrema Identification**
   - First derivative test: Sign change of f'(x) around critical points
   - Determine whether each critical point is max, min, or neither
   - Practice on polynomial functions

3. **Absolute Extrema on Closed Intervals**
   - Candidates: Critical points + endpoints
   - Evaluate function at all candidates, choose max/min
   - Why endpoints matter (different from local extrema)

4. **Modeling Real-World Scenarios**
   - Translate word problems into functions
   - Identify domain restrictions
   - Practice WITHOUT calculus (set up only)

5. **Applied Optimization Problems**
   - Combine modeling + critical point finding + extrema identification
   - Start simple: Single-variable functions with clear domains
   - Build to complex: Constraint equations requiring substitution

**Assessment Checkpoint:** Before applied optimization, verify students can:
- Find and classify critical points of given functions
- Find absolute extrema on closed intervals
- Translate word problems into mathematical functions

---

#### **Related Rates Scaffolding Sequence**

**DON'T** introduce related rates before students master implicit differentiation.

**DO** follow this sequence:

1. **Implicit Differentiation Mastery**
   - Differentiate equations like x² + y² = 25 with respect to x
   - Recognize when to use d/dx vs. dy/dx
   - Solve for dy/dx

2. **Time-Dependent Quantities**
   - Notation: V(t), r(t), h(t) for quantities changing with time
   - Distinguish variables (changing) from constants (fixed)
   - Verbalize: "The radius r is increasing over time, so we write r(t)"

3. **Simple Related Rates (One Equation)**
   - Sphere volume: V = (4/3)πr³, given dr/dt, find dV/dt
   - Direct substitution, no complex relationships
   - Emphasize: "Differentiate with respect to time"

4. **Related Rates with Constraints (Multiple Variables)**
   - Ladder problem: x² + y² = L² (Pythagorean relationship)
   - Given dx/dt, solve for dy/dt
   - Identify what's changing vs. fixed

5. **Complex Related Rates**
   - Shadow problems (similar triangles)
   - Conical tank problems (volume-height relationships)
   - Multiple related quantities

**Assessment Checkpoint:** Before related rates, verify students can:
- Implicitly differentiate equations with respect to x
- Recognize which quantities in a scenario are variables vs. constants
- Differentiate with respect to an arbitrary variable (like t)

---

#### **Integration Scaffolding Sequence**

**DON'T** teach integration techniques before students understand what an integral IS.

**DO** follow this sequence:

1. **Riemann Sums (Conceptual Foundation)**
   - Area approximation with rectangles
   - Left, right, midpoint endpoint choices
   - Limit as n→∞ defines integral (area)

2. **Definite Integral Definition**
   - Notation: ∫[a to b] f(x)dx
   - Geometric meaning: signed area
   - Properties: additivity, constant multiples

3. **Antiderivatives (Separate Concept)**
   - Definition: F'(x) = f(x)
   - Notation: ∫ f(x)dx (indefinite integral)
   - Basic antiderivative rules (reverse power rule)

4. **Fundamental Theorem of Calculus**
   - Connection: ∫[a to b] f(x)dx = F(b) - F(a)
   - Emphasize this is a theorem, not a definition
   - Computational advantage over Riemann sums

5. **Integration Techniques**
   - u-substitution (reverse chain rule)
   - Integration by parts
   - Partial fractions (Calculus II)

**Assessment Checkpoint:** Before FTC, verify students can:
- Approximate area using Riemann sums
- Find antiderivatives of basic functions
- Explain the difference between definite integral (area) and antiderivative (reverse derivative)

---

### Red Flags: Signs of Poor Scaffolding

Watch for these warning signs in content:

❌ **"Prerequisites are assumed"** without verification
❌ Teaching technique before students understand when/why to use it
❌ Skipping intermediate examples (simple → hard with no medium)
❌ Introducing notation without explanation
❌ Relying on algebraic manipulation students may not have mastered

---

## 8.5 Real-World Contexts for Non-Traditional Learners

### Core Principle

**Research Finding:** Real-world contexts enhance engagement and retention, BUT contexts must be **genuinely relatable to the student population**. Contexts that require domain knowledge beyond students' experience (epidemiology models, financial derivatives) increase cognitive load without pedagogical benefit.

**For Non-Traditional Learners:** Choose contexts from everyday experience, not advanced professional domains. **Make the math the hard part, not the context.**

---

### Guidelines for Context Selection

#### **✅ GOOD Contexts (Use These)**

**Daily Life & Personal Experience:**
- Smartphone battery drain rate (exponential decay)
- Social media follower growth (exponential growth)
- Driving distance and speed (position, velocity, acceleration)
- Cooking temperature change (rate of change, heating/cooling curves)
- Fitness tracker data (heart rate, calorie burn over time)
- Weather temperature throughout the day (continuous change)
- Water draining from a bathtub (volume change)

**Simple Economics & Jobs:**
- Hourly wage and total earnings (rate of accumulation)
- Sales commission (piecewise functions)
- Retail discounts (percentage change)
- Simple interest on savings account
- Cost per item decreasing with bulk purchase (optimization)

**Accessible Science:**
- Plant growth over time (biology)
- Balloon inflation (volume-radius relationship)
- Shadow length changing with sun position (similar triangles)
- Water level in various-shaped containers (related rates)

**Characteristics of Good Contexts:**
- Requires no specialized knowledge beyond high school
- Visually concrete (students can picture it)
- Culturally neutral (no regional or socioeconomic assumptions)
- Mathematically non-trivial (calculus is the challenge, not context understanding)

---

#### **❌ POOR Contexts (Avoid These)**

**Overly Abstract or Professional:**
- Rocket trajectory and orbital mechanics → Requires physics background
- Financial derivatives and options pricing → Requires finance knowledge
- Epidemiological disease modeling → Requires biology/statistics background
- Quantum mechanics applications → Too advanced
- Corporate profit maximization → Assumes business knowledge

**Culturally Specific or Exclusionary:**
- Golf ball trajectory → Not all students play golf
- Ski slope angles → Not all students have winter sports experience
- Yacht design optimization → Assumes affluence
- Private jet fuel consumption → Not relatable to underserved students

**Requiring Domain Knowledge:**
- Kirchhoff's circuit laws for current/voltage → Requires electrical engineering
- Chemical reaction rates with equilibrium constants → Requires chemistry
- Structural beam bending moments → Requires physics/engineering

**Why These Fail:**
- **Cognitive overload:** Students spend mental energy understanding the context instead of the calculus
- **Exclusionary:** Students from different backgrounds feel calculus "isn't for them"
- **Irrelevant motivation:** "When will I use this?" goes unanswered if context is inaccessible

---

### Implementation Examples

#### **Example 1: Teaching Derivative as Rate of Change**

❌ **Poor Context:**
> "A rocket's altitude is given by h(t) = -4.9t² + 150t + 5000 meters. Find the rocket's velocity at t=10 seconds."

**Problems:**
- Students may not understand rocket physics
- Constants (4.9, 5000) seem arbitrary without physics background
- Why is this relevant to their lives?

---

✅ **Good Context:**
> "Your phone's battery percentage is modeled by B(t) = 100 - 5t, where t is hours since full charge. Find how fast the battery is draining at t=3 hours."

**Why It Works:**
- Every student has experienced phone battery drain
- Concrete, relatable scenario
- Clear interpretation: Negative derivative means battery decreasing

---

#### **Example 2: Teaching Optimization**

❌ **Poor Context:**
> "A farmer wants to maximize the area of a rectangular cattle pen using 1000 feet of fencing. One side uses an existing barn wall (no fence needed there). Find dimensions that maximize area."

**Problems:**
- Not all students have farming experience
- Cattle pen not relevant to urban/suburban students
- Context adds complexity without benefit

---

✅ **Good Context:**
> "You have 20 feet of LED strip lights to create a rectangular border around a wall poster. What dimensions maximize the poster area?"

**Why It Works:**
- Students have decorated spaces with lights/posters
- Visual, hands-on scenario
- Same math, more relatable context

---

#### **Example 3: Teaching Related Rates**

❌ **Poor Context:**
> "A conical water tank has height 10 feet and radius 4 feet at the top. Water drains at 2 ft³/min. How fast is the water level dropping when the water is 6 feet deep?"

**Problems:**
- Conical tanks are not everyday objects
- Industrial/agricultural setting not relatable
- Requires geometric visualization students may lack

---

✅ **Good Context:**
> "You're filling a cylindrical water bottle (height 8 inches, radius 1.5 inches) at a rate of 3 in³/sec. How fast is the water level rising when it's 4 inches deep?"

**Why It Works:**
- Everyone has filled water bottles
- Cylindrical shape simpler (avoids cone geometry complexity)
- Personal scale, not industrial

---

### Guidelines Summary

**When choosing contexts, ask:**

1. **Would a student from any background understand this scenario?**
   - If it requires specific life experience (skiing, golfing, farming), choose something else

2. **Can the student visualize this without domain knowledge?**
   - If it requires engineering/biology/finance background, simplify

3. **Is the math the hard part, or is understanding the context the hard part?**
   - Calculus should be the challenge, not context interpretation

4. **Does this connect to the student's life goals?**
   - For general calculus course, use universal contexts
   - For calculus for biologists, biology contexts are appropriate

---

### Diverse Contexts by Calculus Concept

| Calculus Concept | Good Contexts |
|------------------|---------------|
| **Derivatives (Rate of Change)** | Phone battery drain, car speed, temperature change, water draining, follower growth |
| **Optimization** | LED light arrangement, phone plan cost, walking route, material for box, fencing for garden area |
| **Related Rates** | Shadow length, water bottle filling, balloon inflation, ladder sliding, person walking |
| **Integrals (Area/Accumulation)** | Total distance traveled, calories burned, water accumulated, money saved, data downloaded |
| **Exponential Growth/Decay** | Social media followers, bacteria growth, drug concentration, coffee cooling, viral video views |
| **Concavity & Inflection** | Accelerating car, epidemic spread phases, product adoption curve, learning progress |

---

## 8.6 Active Learning for Non-Traditional Learners

### Research-Backed Principle

**Key Finding (Science, 2023):** Active, student-centered calculus courses result in significantly greater learning outcomes compared to traditional lecture methods, with **particularly profound benefits for students from underrepresented populations in STEM**.

**For Learnvia:** Our animated figures with embedded questions, plus 5-10 follow-up learning questions, already implement active learning. This section reinforces why this approach is critical.

---

### What Active Learning Means in Calculus

**Passive Learning (Traditional Lecture):**
- Instructor derives formulas on board
- Students watch and take notes
- Limited interaction until homework

**Active Learning (Learnvia Approach):**
- Animated figure unveils concept gradually
- Embedded questions require student response during animation
- Follow-up questions continue teaching through practice
- Students construct understanding through guided engagement

---

### Learnvia's Active Learning Components

#### **1. Embedded Questions in Animations**

**Purpose:** Keep students engaged during the "lecture" (animated figure), ensure comprehension before moving forward.

**Design Principles:**
- **1-3 questions per animated figure** (not more—balance engagement with flow)
- **Quick to answer:** 5-10 seconds, no lengthy calculation
- **Check key concepts:** Not busy work, but genuine comprehension checks
- **Positioned strategically:** After introducing new idea, before building on it

**Example from Derivative Introduction:**

*Animated Figure Scene 2:*
> "We've calculated the secant line slope between x=1 and x=2 as 3. As we move the second point closer to x=1, what happens to the secant line slope?"

**Embedded Question:**
> "If we calculate the slope between x=1 and x=1.1, will it be closer to 2 or closer to 4?"

**Why This Works:** Forces student to predict before animation shows answer, activating prior knowledge and making the subsequent reveal more meaningful.

---

#### **2. Follow-Up Learning Questions**

**Purpose:** Replace passive reading with active dialogue. "Think of a tutor working through problems with you, not a textbook you're reading alone."

**Design Principles (as stated in Section 5):**
- 5-10 questions per lesson
- Start simple, build toward harder
- Mix conceptual and computational
- Explicitly address misconceptions
- Are quickly answerable (not homework-length)

**Active Learning Enhancement:**
- **"Predict then check" questions:** Guess, then calculate to verify
- **"Compare and contrast" questions:** Two approaches, which is correct?
- **"Find the error" questions:** Identify mistake in worked solution
- **"Explain your reasoning" questions:** Don't just answer, justify

---

### Strategies for Non-Traditional Learners

#### **Strategy 1: Validation and Encouragement**

**Research Finding:** Promising practices such as **validation** improve success of historically underserved students.

**Implementation:**
- **Hints should validate effort:** "Good thinking! This approach is close, but..."
- **Explanations assume good faith:** "Many students interpret this as X because..." (not "You probably thought...")
- **Celebrate partial understanding:** "You're on the right track—now let's refine this idea."

---

#### **Strategy 2: Low-Stakes Practice**

**For struggling learners:** High-stakes assessment creates anxiety. Learning questions should feel like practice, not tests.

**Implementation:**
- **Unlimited attempts** on learning questions
- **Hints available** without penalty
- **Explanations immediately available** after answering (right or wrong)
- **Points for completion, not correctness** (engagement matters more than perfection during learning)

---

#### **Strategy 3: Frequent Small Successes**

**Psychological principle:** Students with low confidence need frequent positive reinforcement to persist.

**Implementation:**
- **Many short questions** rather than few long problems
- **Early questions are confidence builders:** Students should succeed on first 2-3 questions
- **Gradual difficulty ramp:** Success → challenge → success → harder challenge

---

## 8.7 Assessment Design for Conceptual and Procedural Balance

### Alignment with Learning Objectives

**Core Principle:** Assessments must measure both procedural fluency AND conceptual understanding, aligned with the lesson's learning objectives.

**Common Mistake:** Lesson teaches concepts, but assessment only tests procedures.

---

### Balanced Assessment Question Matrix

For every calculus module, include questions from ALL four quadrants:

|  | **Conceptual** | **Procedural** |
|---|---|---|
| **Recall/Identify** | "What does f'(3)=5 mean graphically?" | "Evaluate f'(3) if f(x)=x²+2x" |
| **Apply/Analyze** | "Explain why this function needs the chain rule" | "Find d/dx[sin(3x²)]" |

**Quadrant Definitions:**

**1. Procedural-Recall:** Execute memorized algorithms
- "Find d/dx(x⁵)"
- "Evaluate ∫(3x² + 2)dx"

**2. Procedural-Apply:** Apply procedures to new problems
- "Find critical points of f(x) = x³ - 6x² + 9x"
- "Calculate ∫[0 to 3] (x² - 2x)dx"

**3. Conceptual-Recall:** State definitions, interpret meaning
- "What does 'f is continuous at x=2' mean?"
- "If f'(x) > 0, what does this tell you about f?"

**4. Conceptual-Apply:** Explain reasoning, analyze situations
- "Explain why lim[x→2] f(x) can exist even if f(2) is undefined"
- "Given the graph of f, sketch f'"

---

### Sample Balanced Question Set (Derivatives)

**Learning Objective:** Students understand the derivative as instantaneous rate of change and can calculate derivatives using the power rule.

**Balanced Assessment:**

1. **Procedural-Recall:** Find f'(x) if f(x) = 4x³ - 2x + 7

2. **Conceptual-Recall:** In your own words, explain what the derivative represents. Include the words "rate of change" and "instantaneous".

3. **Procedural-Apply:** A ball's height is h(t) = -16t² + 64t feet after t seconds. Find h'(t) and evaluate h'(2).

4. **Conceptual-Apply:** The ball's height derivative is h'(t) = -32t + 64. Explain what h'(2) = 0 means about the ball's motion at t=2 seconds.

5. **Graphical-Conceptual:** Sketch a possible graph of f(x) if you know f'(x) = 2x.

6. **Mixed:** If f(x) = x² and you calculate f'(3), you get f'(3) = 6. Explain what this value means in terms of:
   a. The graph of f at x=3
   b. The rate at which f is changing at x=3

**Why This Works:** Tests memorization, application, interpretation, and explanation—full spectrum of understanding.

---

## 8.8 Annotated Examples for Authors

### Example 1: Teaching Limits with Multiple Representations

**Learning Objective:** Students understand that a limit describes function behavior near a point, and can evaluate limits graphically, numerically, and algebraically.

---

**FRAMING TEXT (100-150 words):**

> Functions often have interesting behavior at specific points. The **limit** of a function as x approaches a value describes what the function's output approaches near that point, even if the function is undefined at the point itself.
>
> **Key definition:** The notation lim[x→a] f(x) = L means "As x gets closer to a, f(x) gets closer to L."
>
> **Important distinction:** The limit describes behavior **near** x=a, not necessarily **at** x=a. This means lim[x→a] f(x) can exist even when f(a) is undefined.
>
> Ex: If f(x) = (x²-4)/(x-2), then f(2) is undefined (division by zero), but lim[x→2] f(x) = 4 because f(x) approaches 4 as x approaches 2.
>
> In this lesson, we'll explore limits using tables of values (numerical), graphs (graphical), and algebra (symbolic).

---

**ANIMATED FIGURE (2-3 minutes, 4 scenes):**

**Scene 1: Numerical Approach (Table)**
> "Let's investigate what happens to f(x) = (x²-4)/(x-2) as x approaches 2. We'll create a table with x values near 2 and calculate f(x)."

*Table appears, populate rows:*
- x = 1.9, f(x) = 3.9
- x = 1.99, f(x) = 3.99
- x = 1.999, f(x) = 3.999
- x = 2.1, f(x) = 4.1
- x = 2.01, f(x) = 4.01
- x = 2.001, f(x) = 4.001

> "Notice: As x gets closer to 2 from both sides, f(x) gets closer to 4. So lim[x→2] f(x) = 4."

**Embedded Question:**
> "Based on the table, what value is f(x) approaching as x gets close to 2?"
> a. 0  b. 2  c. 4 ← correct  d. undefined

---

**Scene 2: Graphical Approach**
> "Let's see this visually. Here's the graph of f(x) = (x²-4)/(x-2)."

*Graph appears: hyperbola-like curve with open circle (hole) at (2, 4)*

> "Notice the 'hole' at x=2. The function is undefined there, but the graph shows the curve approaching the point (2, 4) from both sides."

*Animate point traveling along curve from left, approaching hole. Animate another point from right.*

> "Both sides approach y=4. This visual confirms lim[x→2] f(x) = 4, even though f(2) doesn't exist."

**Embedded Question:**
> "Can a limit exist at a point where the function is undefined?"
> a. No, limits require the function to exist
> b. Yes, limits describe behavior near a point, not at the point ← correct

---

**Scene 3: Algebraic Approach**
> "We can also find this limit algebraically by simplifying the function."

*Show algebra:*
```
f(x) = (x²-4)/(x-2)
     = (x-2)(x+2)/(x-2)   [factor numerator]
     = x+2                 [cancel (x-2), x≠2]
```

> "After canceling, f(x) = x+2 for all x except x=2. So lim[x→2] f(x) = lim[x→2] (x+2) = 2+2 = 4."

*Highlight: "This confirms our numerical and graphical results!"*

---

**Scene 4: Summary**
> "The limit lim[x→2] f(x) = 4 describes what f(x) approaches near x=2. We found this using:
> - **Numerical:** Table of values approaching 2
> - **Graphical:** Graph approaching (2,4)
> - **Algebraic:** Simplification and substitution
>
> All three methods agree: the limit is 4, even though f(2) is undefined."

---

**FOLLOW-UP QUESTIONS (8 questions):**

**Q1 (Recall):** What does lim[x→3] f(x) = 7 mean in words?

**Q2 (Conceptual):** True or False: If lim[x→5] f(x) = 10, then f(5) must equal 10. Explain.

**Q3 (Numerical):** Use the table to estimate lim[x→1] g(x):
| x | 0.9 | 0.99 | 0.999 | 1.001 | 1.01 | 1.1 |
|---|-----|------|-------|-------|------|-----|
| g(x) | 2.7 | 2.97 | 2.997 | 3.003 | 3.03 | 3.3 |

**Q4 (Graphical):** *Show graph with hole at (4, 2)*. What is lim[x→4] h(x)?

**Q5 (Algebraic):** Find lim[x→3] (x²-9)/(x-3) by factoring and simplifying.

**Q6 (Misconception):** A student says "lim[x→2] f(x) can't exist because f(2) is undefined." What would you tell this student?

**Q7 (Application):** If lim[x→0⁺] f(x) = 5 and lim[x→0⁻] f(x) = 5, what does lim[x→0] f(x) equal? Explain.

**Q8 (Synthesis):** Sketch a possible graph of a function where lim[x→2] f(x) = 3 but f(2) = 5.

---

**Why This Example Works:**
- ✅ Uses all three representations (numerical, graphical, symbolic)
- ✅ Explicitly addresses misconception (limit ≠ function value)
- ✅ Provides conceptual foundation before algebraic techniques
- ✅ Follow-up questions test recall, understanding, and application
- ✅ Relatable context (simple rational function, not advanced)

---

## Summary: Quick Reference Checklist

When authoring calculus content, verify:

### ☐ Multiple Representations
- [ ] Concept shown graphically (visual understanding)
- [ ] Concept shown numerically (table/calculation)
- [ ] Concept shown symbolically (formulas/algebra)
- [ ] Explicit connections made between representations

### ☐ Misconceptions Addressed
- [ ] Identified which misconceptions apply to this topic
- [ ] Explicitly stated the misconception and why it's wrong
- [ ] Provided correct understanding with examples
- [ ] Assessed student understanding of the distinction

### ☐ Conceptual-Procedural Balance
- [ ] Conceptual foundation provided before procedures
- [ ] "Why" explained, not just "how"
- [ ] Questions test both computation and interpretation
- [ ] Real-world meaning provided for calculations

### ☐ Proper Scaffolding
- [ ] Prerequisites verified or reviewed first
- [ ] Concepts introduced in logical dependency order
- [ ] Gradual complexity increase (simple → medium → complex)
- [ ] No big jumps in difficulty

### ☐ Relatable Contexts
- [ ] Real-world examples from student experience
- [ ] No specialized domain knowledge required
- [ ] Culturally inclusive contexts
- [ ] Math is the challenge, not context understanding

### ☐ Active Learning
- [ ] Embedded questions in animated figures (1-3)
- [ ] Follow-up questions continue teaching (5-10)
- [ ] Mix of recall, application, and explanation questions
- [ ] Frequent small successes for confidence building

### ☐ Aligned Assessment
- [ ] Questions match learning objectives
- [ ] Both procedural and conceptual questions included
- [ ] Graphical, numerical, and algebraic questions present
- [ ] Interpretation and explanation required, not just computation

---

## References & Further Reading

**Research on Multiple Representations:**
- Eisenberg, T., & Dreyfus, T. (1991). "On the Reluctance to Visualize in Mathematics." In *Visualization in Teaching and Learning Mathematics* (pp. 25-37). MAA.
- Teaching Calculus Blog: "MPAC 4: Multiple Representations" (AP Calculus standards)

**Research on Calculus Misconceptions:**
- Tall, D., & Vinner, S. (1981). "Concept Image and Concept Definition in Mathematics with Particular Reference to Limits and Continuity." *Educational Studies in Mathematics*, 12(2), 151-169.
- Orton, A. (1983). "Students' Understanding of Differentiation." *Educational Studies in Mathematics*, 14(3), 235-250.

**Research on Active Learning in Calculus:**
- Freeman, S., et al. (2023). "Establishing a New Standard of Care for Calculus Using Trials with Randomized Student Allocation." *Science*.
- Bressoud, D. M., Mesa, V., & Rasmussen, C. (2015). *Insights and Recommendations from the MAA National Study of College Calculus*. MAA Press.

**Research on Teaching Underserved Students:**
- "Transitioning Learners to Calculus in Community Colleges (TLC3): Advancing Strategies for Success in STEM" (NSF Grant #2142718). University of Michigan & University of Illinois.
- Boaler, J. (2016). *Mathematical Mindsets: Unleashing Students' Potential Through Creative Math, Inspiring Messages and Innovative Teaching*. Jossey-Bass.

---

## Appendix: Calculus-Specific Vocabulary Consistency

**Use consistent terminology throughout all modules:**

| Concept | Preferred Term | Avoid |
|---------|---------------|-------|
| Slope of tangent line | "instantaneous rate of change" or "derivative" | "just the slope" |
| lim[x→a] f(x) | "limit as x approaches a" | "limit at a" |
| Continuous at x=a | "continuous at the point x=a" | "connected at a" |
| Definite integral | "signed area under the curve" | "area" (without "signed") |
| Antiderivative | "function whose derivative is f" | "opposite of derivative" |
| Critical point | "point where f'(x)=0 or undefined" | "turning point" |
| Concave up | "f''(x) > 0, graph curves like ∪" | "curving upward" |
| Related rates | "rates of change linked by an equation" | "connected variables" |

---

**End of Section 8**

---

## Implementation Note for Kelly

This Section 8 should be inserted into the **Learnvia Authoring Guidelines** document (`FOUNDATION/authoring_guide_full.txt`) as the final major section before "Miscellaneous."

The content is research-backed and specifically addresses:
1. ✅ Multiple representations (Rule of Four from AP Calculus standards + education research)
2. ✅ Common calculus misconceptions (documented in mathematics education literature)
3. ✅ Conceptual vs. procedural balance (research on student understanding)
4. ✅ Scaffolding sequences (prerequisite dependencies for calculus topics)
5. ✅ Real-world contexts for non-traditional learners (relatable examples, not abstract)
6. ✅ Active learning strategies (research showing benefits for underserved students)
7. ✅ Assessment design (balanced testing of concepts and procedures)

All recommendations align with your existing authoring philosophy while adding calculus-specific depth.
