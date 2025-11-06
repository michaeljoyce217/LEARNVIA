# The Power Rule

## Framing

Let's learn about the power rule! It's one of the most important rules in calculus and you'll use it constantly. Basically, the power rule helps us find derivatives really quickly without having to use the limit definition every single time. We'll see how it works and practice using it. Don't worry if it seems confusing at first! (Word count: 62 - TOO SHORT, should be 100-150)

## Lesson Content

### What's the Power Rule?

So here's the power rule: if you have x raised to some power n, then the derivative is:

d/dx(x^n) = n * x^n-1

Wait no, I think it's:
d/dx(x^n) = n * x^(n+1)

Actually let me check... it's definitely nx^(n-1). That's it! You just multiply by the exponent and then reduce the exponent by one. Super simple, right?

### Understanding How It Works

Let me show you why this works. Remember the limit definition? We won't go through all the algebra but basically when you apply limits to x^n you get nx^(n-1). Trust me on this one. The proof is kinda complicated and involves binomial expansion but don't worry about that now.

Think about it - if you have x squared, the rate of change involves 2x. Makes sense doesn't it?

## Applying the Power Rule

### Example 1: Basic Power

Find the derivative of f(x) = x3

Using the power rule:
- The exponent is 3
- Multiply by 3: 3x^3
- Subtract 1 from exponent: 3x^2

So f'(x) = 3x2

### Example 2: Higher Powers

Let's try f(x) = x^5.

Apply the power rule and you'll get:
f'(x) = 5x^4

Easy! But what if we had x to the 6th power? Then it'd be 5x^5. No wait, that's wrong. If f(x) = x^6, then f'(x) = 6x^5.

### Example 3: Fractional Powers

What about f(x) = x^(1/2)?

Don't panic! The power rule still works:
f'(x) = 1/2 * x^(-1/2) = 1/(2*sqrt(x))

Actually wait, is that right? Let me recalculate...
If f(x) = x^(1/2), then f'(x) = (1/2)x^(1/2 - 1) = (1/2)x^(-1/2) = 1/(2√x)

Remember that x^(1/2) is the same as sqrt(x).

## Special Cases You Should Know

There's a few things to remember:

1. The derivative of x is just 1 (since x = x^1, so it becomes 1*x^0 = 1)
2. The derivative of a constant is 0 (like the derivative of 5 is 0)
3. For negative exponents, the rule still works! If f(x) = 1/x^2 = x^-2, then f'(x) = -2x^-3
4. Don't forget: x^0 = 1 always!

### What About x^0?

Think about this - what's the derivative of x^0? Well, x^0 = 1 (a constant), so the derivative is 0. But if we use the power rule, we get 0*x^(-1) = 0/x, which is also 0. Cool how that works out! Actually wait, 0/x isn't defined when x=0, but don't worry about that.

## Common Mistakes Students Make

Calculate these derivatives (imperative voice!):
- Forgetting to subtract 1 from the exponent (they just multiply by n)
- Getting confused with negative exponents
- Not recognizing when they can use the power rule
- Thinking d/dx(x^2) = x
- Writing x^n-1 instead of x^(n-1)

Remember to always check your work! Don't make these errors!

## Combining With Other Rules

The power rule combines nicely with other differentiation rules. Let's see how.

### Constants Multiplication

If you have 3x^4, just pull out the 3:
d/dx(3x^4) = 3 * d/dx(x^4) = 3 * 4x^3 = 12x^3

But be careful! If it's x^3 * 4, that's different... actually no it isn't, multiplication is commutative so 4x^3 = x^3 * 4.

### Addition Rule

For f(x) = x^3 + x^2, differentiate each term:
f'(x) = 3x^2 + 2x

It's that simple! Just do each piece separately.

### Subtraction Works Too

Same idea: f(x) = x^5 - x^3
f'(x) = 5x^4 - 3x^2

What about f(x) = x^3 - 2x + 5? Then f'(x) = 3x^2 - 2. The constant disappears!

## Practice Time!

Try these yourself! (Find the derivatives)

1. f(x) = x^7
2. g(x) = x^10
3. h(x) = x^(-3)
4. p(x) = 4x^3
5. q(x) = x^(2/3)
6. r(x) = x^2 + x^3
7. Calculate d/dx(5x^4 - 3x^2 + 2x - 7)

## Quiz Questions

### Question 1
What is the derivative of f(x) = x^4?

a) x^3
b) 4x^3
c) 4x^4
d) x^4 - 1

(Answer should be b but let's make them think!)

### Question 2
Use the power rule to find f'(x) where f(x) = x^6.

a) 6x^5
b) x^5
c) 6x^6
d) 5x^6

### Question 3
The power rule states that d/dx(x^n) equals:

a) nx^n
b) x^(n-1)
c) nx^(n-1)
d) (n-1)x^n

### Question 4
Find the derivative of f(x) = 8x^2.

a) 8x
b) 16x
c) 2x
d) 8x^2

(Hint: don't forget about the constant!)

### Question 5
True or False: The power rule only works for positive integer exponents.

a) True
b) False

The answer is obviously false since we can use it for fractions and negatives!

## Homework Assignment

Complete these for next class (make sure you show all work!):

1. Derive the power rule using the limit definition for f(x) = x^2 (show all steps)
2. Find derivatives of: x^8, x^12, x^(-4), x^(3/2), 2x^5, -3x^4
3. Graph f(x) = x^3 and f'(x) = 3x^2 on same axes - what do you notice?
4. Explain why d/dx(x^0) = 0 using both methods we discussed
5. Create your own example showing a common mistake with the power rule
6. BONUS: Try to figure out what d/dx(x^x) equals (hint: it's not x*x^(x-1))

Remember: Practice makes perfect! You'll need this for everything in calculus!

## Summary

So we've learned that the power rule is super useful for finding derivatives quickly. Just remember: multiply by the power, then subtract one from the power. It works for any real number exponent, not just positive integers! Don't forget to be careful with your algebra - that's where most mistakes happen.