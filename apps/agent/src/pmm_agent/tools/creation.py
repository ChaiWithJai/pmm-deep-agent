"""
PMM Creation Tools

Tools for generating positioning, messaging, and marketing assets.
"""

import json
from typing import Literal
from langchain_core.tools import tool


@tool
def create_positioning_canvas(
    product_description: str,
    target_audience: str | None = None,
    known_competitors: list[str] | None = None,
    unique_capabilities: list[str] | None = None,
) -> str:
    """
    Create a complete positioning canvas for a product.

    Uses April Dunford's positioning methodology to build:
    - Target customer definition
    - Competitive alternative
    - Unique value proposition
    - Positioning statements

    Args:
        product_description: What the product does
        target_audience: Who it's for (if known)
        known_competitors: List of competitors (if known)
        unique_capabilities: What makes it different (if known)

    Returns:
        JSON with complete positioning canvas
    """
    return json.dumps({
        "task": "create_positioning_canvas",
        "instructions": f"""Create positioning canvas:

# POSITIONING CANVAS

## 1. TARGET CUSTOMER

**Role/Title:**
(Be specific - "Marketing Directors at B2B SaaS companies" not "marketers")

**Company Type:**
(B2B/B2C, size, stage, characteristics)

**Industry:**
(Specific vertical or "horizontal with focus on X")

**Situation/Trigger:**
(What event makes them look for this solution?)

**Validation:** Is this specific enough that you could build a target list?

---

## 2. COMPETITIVE ALTERNATIVE

**Primary Alternative:**
(What do they do today without your product?)

**Type:**
[ ] Direct Competitor: ___
[ ] Manual Process: ___
[ ] Status Quo: ___
[ ] Homegrown Solution: ___

---

## 3. WHY THAT SUCKS

**Pain Point 1:**
(Most urgent pain)

**Pain Point 2:**
(Second most important)

**Pain Point 3:**
(Supporting pain)

---

## 4. YOUR UNIQUE APPROACH

**Key Differentiator:**
(What do you do fundamentally differently?)

**Methodology/Approach:**
(How do you solve it differently?)

**Unique Capability:**
(What can you do that alternatives can't?)

---

## 5. WHY THAT'S BETTER

**Primary Benefit:**
(The main outcome customers get)

**Supporting Benefit:**
(Secondary value)

**Proof Point:**
(Evidence this is true)

---

## 6. POSITIONING STRATEGY

**Approach:**
[ ] Category-Based: Competing within ___
[ ] Use-Case-Based: Best for ___

---

## 7. POSITIONING STATEMENTS

**Internal Positioning Statement:**
"For [target customer] who [situation], [product] is a [category] that [key benefit]. Unlike [competitive alternative], we [key differentiator]."

**Differentiation Summary:**
"Unlike [competitive alternative], which [problem with alternative], [product] [unique approach] so that [target customer] can [key benefit]."

**Homepage One-Liner:**
"[Product]: The [category/approach] for [audience]"

---

## VALIDATION CHECKLIST

- [ ] Competitive alternative is clearly defined
- [ ] Target customer is specific (not "everyone")
- [ ] Differentiation is meaningful (customers care)
- [ ] Differentiation is defensible (hard to copy)
- [ ] Problem/pain is explicit
- [ ] Could NOT be said by any competitor

Product: {product_description}
{f"Target: {target_audience}" if target_audience else ""}
{f"Competitors: {known_competitors}" if known_competitors else ""}
{f"Unique capabilities: {unique_capabilities}" if unique_capabilities else ""}""",
        "product_description": product_description,
        "target_audience": target_audience,
        "known_competitors": known_competitors,
        "unique_capabilities": unique_capabilities,
    })


@tool
def create_messaging_framework(
    positioning_canvas: str,
    primary_persona: str | None = None,
    secondary_personas: list[str] | None = None,
) -> str:
    """
    Create a messaging framework based on positioning.

    Builds the messaging house with:
    - Value proposition
    - Key message pillars
    - Proof points per pillar
    - Persona-specific variations

    Args:
        positioning_canvas: The positioning canvas (from create_positioning_canvas)
        primary_persona: Primary target persona
        secondary_personas: Additional personas to message for

    Returns:
        JSON with complete messaging framework
    """
    return json.dumps({
        "task": "create_messaging_framework",
        "instructions": f"""Create messaging framework:

# MESSAGING FRAMEWORK

## VALUE PROPOSITION
(Top of the messaging house - what you do + why it matters)

**Format:** [Product] helps [audience] [achieve outcome] by [unique approach].

**Value Prop:**


---

## MESSAGING HOUSE

```
┌─────────────────────────────────────────────────────┐
│              VALUE PROPOSITION                       │
│  [Write the value prop here]                        │
├─────────────────┬─────────────────┬─────────────────┤
│    PILLAR 1     │    PILLAR 2     │    PILLAR 3     │
│  [Main diff]    │  [Core benefit] │  [Trust/ease]   │
├─────────────────┼─────────────────┼─────────────────┤
│  • Proof 1      │  • Proof 1      │  • Proof 1      │
│  • Proof 2      │  • Proof 2      │  • Proof 2      │
│  • Proof 3      │  • Proof 3      │  • Proof 3      │
├─────────────────┴─────────────────┴─────────────────┤
│  FOUNDATION: [Target audience] + [Competitive alt]  │
└─────────────────────────────────────────────────────┘
```

---

## PILLAR 1: [Primary Differentiation]

**Key Message:**
(Benefit-oriented statement about your main differentiator)

**Supporting Points:**
1.
2.
3.

**Proof Points:**
- Metric:
- Testimonial:
- Case study:

---

## PILLAR 2: [Core Capability Benefit]

**Key Message:**


**Supporting Points:**
1.
2.
3.

**Proof Points:**
- Metric:
- Testimonial:
- Case study:

---

## PILLAR 3: [Trust/Ease/Speed]

**Key Message:**


**Supporting Points:**
1.
2.
3.

**Proof Points:**
- Metric:
- Testimonial:
- Case study:

---

## PERSONA-SPECIFIC MESSAGING

{f"### Primary Persona: {primary_persona}" if primary_persona else "### Primary Persona"}

| Aspect | Message |
|--------|---------|
| Pain Point | |
| Desired Outcome | |
| Key Message | |
| Proof Point | |
| Likely Objection | |
| Objection Response | |

{f"### Secondary Personas: {secondary_personas}" if secondary_personas else ""}

---

## HEADLINE OPTIONS

**Problem-led:**
1.
2.

**Solution-led:**
1.
2.

**Outcome-led:**
1.
2.

**Differentiation-led:**
1.
2.

---

## CTA OPTIONS

**Primary CTA (high intent):**
1.
2.

**Secondary CTA (low intent):**
1.
2.

---

## ELEVATOR PITCH

**30-second version:**


**10-second version:**


Positioning: {positioning_canvas}""",
        "positioning_canvas": positioning_canvas,
        "primary_persona": primary_persona,
        "secondary_personas": secondary_personas,
    })


@tool
def create_homepage_wireframe(
    messaging_framework: str,
    style: Literal["minimal", "standard", "comprehensive"] = "standard",
) -> str:
    """
    Create a homepage wireframe with PMM best practices.

    Generates section-by-section copy recommendations based on messaging framework.

    Args:
        messaging_framework: The messaging framework to translate
        style: How detailed the homepage should be

    Returns:
        JSON with homepage wireframe and copy recommendations
    """
    return json.dumps({
        "task": "create_homepage_wireframe",
        "instructions": f"""Create homepage wireframe:

# HOMEPAGE WIREFRAME

## SECTION 1: HERO

**Headline:**
(Clear, not clever. What you do + who for.)

**Subheadline:**
(Supports headline. Adds context, doesn't repeat.)

**Primary CTA:**
(Benefit-oriented. What happens when they click?)

**Secondary CTA:**
(For not-ready visitors. Lower commitment.)

**Social Proof in Hero:**
(Logo bar or key metric)

---

## SECTION 2: SOCIAL PROOF BAR

**Logos to include:**
(5-7 recognizable logos for target audience)

**Alternative if no logos:**
(Key metric or testimonial snippet)

---

## SECTION 3: PROBLEM/PAIN

**Headline:**
(Agitate the problem they have)

**Pain points:**
1.
2.
3.

---

## SECTION 4: SOLUTION/HOW IT WORKS

**Headline:**
(How you solve it)

**3 Steps or Features:**

| Step | Headline | Description |
|------|----------|-------------|
| 1 | | |
| 2 | | |
| 3 | | |

---

## SECTION 5: KEY BENEFITS (Pillars)

**Section Headline:**

**Benefit 1:**
- Headline:
- Description:
- Proof point:

**Benefit 2:**
- Headline:
- Description:
- Proof point:

**Benefit 3:**
- Headline:
- Description:
- Proof point:

---

## SECTION 6: SOCIAL PROOF DEEP

**Testimonial 1:**
- Quote:
- Name, Title, Company:
- Specific result:

**Testimonial 2:**
- Quote:
- Name, Title, Company:
- Specific result:

**Case Study Preview:**
- Company:
- Result:
- CTA to full case study:

---

## SECTION 7: DIFFERENTIATION

**Headline:**
(Why choose us over alternatives)

**Comparison or unique points:**

---

## SECTION 8: CTA SECTION

**Headline:**
(Final push - urgency or benefit)

**Primary CTA:**

**Friction reducers:**
(Free trial, no credit card, etc.)

---

## SECTION 9: FAQ (Optional)

**Q1:**
**A1:**

**Q2:**
**A2:**

**Q3:**
**A3:**

---

## SECTION 10: FOOTER CTA

**Headline:**

**CTA:**

---

## COPY CHECKLIST

- [ ] Hero passes 5-second test
- [ ] Only ONE primary CTA per section
- [ ] All features translated to benefits
- [ ] Social proof includes names and specifics
- [ ] No jargon or buzzwords
- [ ] Scannable structure

Style: {style}
Messaging: {messaging_framework}""",
        "messaging_framework": messaging_framework,
        "style": style,
    })


@tool
def generate_differentiation_statements(
    product_description: str,
    competitive_alternative: str,
    unique_capabilities: list[str],
    target_audience: str | None = None,
) -> str:
    """
    Generate differentiation statements and positioning angles.

    Creates "Unlike X, we Y" statements and alternative positioning angles.

    Args:
        product_description: What the product does
        competitive_alternative: What you're positioning against
        unique_capabilities: What makes you different
        target_audience: Who you're targeting

    Returns:
        JSON with differentiation statements and positioning angles
    """
    return json.dumps({
        "task": "generate_differentiation",
        "instructions": f"""Generate differentiation statements:

# DIFFERENTIATION STATEMENTS

## "UNLIKE X, WE Y" STATEMENTS

**Statement 1 (Primary):**
"Unlike [alternative], which [problem], [product] [unique approach] so you can [benefit]."

**Statement 2:**


**Statement 3:**


**Statement 4:**


**Statement 5:**


---

## POSITIONING ANGLES

### Angle 1: Problem-Focused
"Stop [painful thing]. Start [better outcome]."

### Angle 2: Audience-Focused
"The [category] built for [specific audience]."

### Angle 3: Approach-Focused
"The only [category] that [unique approach]."

### Angle 4: Outcome-Focused
"[Achieve outcome] in [timeframe/easier way]."

### Angle 5: Anti-Alternative
"[Alternative] wasn't built for [your use case]. We were."

---

## CATEGORY OPTIONS

**Option 1: Existing Category**
"The [existing category] for [your segment]"
Example:

**Option 2: New Category**
"[New category name] - [definition]"
Example:

**Option 3: Use Case**
"The best way to [specific job-to-be-done]"
Example:

---

## HEADLINE OPTIONS

**Clear and Direct:**
1.
2.
3.

**Problem-Agitation:**
1.
2.
3.

**Differentiation-Led:**
1.
2.
3.

---

## VALIDATION QUESTIONS

To test these with customers, ask:
1. "Does this describe a problem you have?"
2. "Does this sound different from [competitor]?"
3. "Would this make you want to learn more?"

Product: {product_description}
Alternative: {competitive_alternative}
Capabilities: {unique_capabilities}
{f"Audience: {target_audience}" if target_audience else ""}""",
        "product_description": product_description,
        "competitive_alternative": competitive_alternative,
        "unique_capabilities": unique_capabilities,
        "target_audience": target_audience,
    })
