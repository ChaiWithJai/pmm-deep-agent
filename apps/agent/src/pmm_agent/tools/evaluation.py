"""
PMM Evaluation Tools

Tools for analyzing positioning, messaging, and marketing assets.
Following the Deep Agents framework pattern with @tool decorator.
"""

import json
from typing import Literal
from langchain_core.tools import tool

from pmm_agent.models.evaluation import (
    FiveSecondTest,
    PositioningAnalysis,
    TargetCustomer,
    CompetitiveAlternative,
    Differentiation,
    PositioningStrategy,
    MessagingAnalysis,
    MessagingLayer,
    MessagingHouse,
    HomepageAnalysis,
    HeroSection,
    SocialProof,
    PMMIssue,
    Severity,
)


# =============================================================================
# 5-SECOND TEST TOOL
# =============================================================================

@tool
def run_five_second_test(
    asset_content: str,
    asset_type: Literal["homepage", "landing_page", "sales_deck", "email", "ad"] = "homepage",
) -> str:
    """
    Run a 5-second test on a marketing asset.

    The 5-second test answers four critical questions:
    1. What does this company/product do?
    2. Who is it for?
    3. What makes it different?
    4. What should I do next?

    Args:
        asset_content: The content of the marketing asset (text, HTML, or description)
        asset_type: Type of asset being evaluated

    Returns:
        JSON with 5-second test results and pass/fail determination
    """
    # This tool returns a structured prompt for the LLM to complete
    return json.dumps({
        "task": "five_second_test",
        "instructions": """Analyze this asset and answer:

1. **What do they do?** (clear/partial/unclear)
   - Can you tell what the product/service is within 5 seconds?
   - Quote the text that tells you (or note its absence)

2. **Who is it for?** (clear/partial/unclear)
   - Is the target audience specific or generic?
   - Quote any persona/audience indicators

3. **What makes it different?** (clear/partial/unclear)
   - Is there a unique value proposition?
   - What's the competitive alternative?

4. **What to do next?** (clear/partial/unclear)
   - Is there a clear call-to-action?
   - Is there only ONE primary action?

**Final verdict:** PASS (3-4 clear), PARTIAL (1-2 clear), FAIL (0 clear)

Provide specific evidence for each answer.""",
        "asset_content": asset_content,
        "asset_type": asset_type,
    })


# =============================================================================
# POSITIONING ANALYSIS TOOL
# =============================================================================

@tool
def analyze_positioning(
    asset_content: str,
    company_context: str | None = None,
) -> str:
    """
    Analyze the positioning strategy of a marketing asset.

    Uses the Positioning Canvas framework:
    1. Target Customer - Who is this for?
    2. Competitive Alternative - What are you better than?
    3. Why Alternative Sucks - Pain points of current solution
    4. Unique Approach - How you do it differently
    5. Why That's Better - Benefits of your approach

    Args:
        asset_content: The marketing asset content to analyze
        company_context: Optional additional context about the company

    Returns:
        JSON with positioning analysis including scores and issues
    """
    return json.dumps({
        "task": "positioning_analysis",
        "instructions": """Analyze positioning using the Positioning Canvas:

## 1. TARGET CUSTOMER
- Role/Title: (identified or missing?)
- Company Type: (B2B, B2C, size, stage?)
- Industry: (specific or "everyone"?)
- Situation/Trigger: (what makes them buy now?)
- **Specificity Score (0-100):** How narrow is the targeting?

## 2. COMPETITIVE ALTERNATIVE
- Type: (direct competitor / manual process / status quo / homegrown)
- Named Alternative: (explicit or implied?)
- Is there a "unlike X" or "instead of Y"?
- **Frame Score (0-100):** How clear is what they replace?

## 3. DIFFERENTIATION
- Unique Approach: (what do they do differently?)
- Key Capability: (what can they do that others can't?)
- Is it defensible? (hard to copy)
- Is it meaningful? (customers care)
- Could competitor say the same thing?
- **Differentiation Score (0-100)**

## 4. PROBLEM/PAIN
- Is there a specific problem stated?
- Is it the customer's problem or the company's narrative?
- Is it specific or generic ("increase revenue")?
- **Problem Clarity Score (0-100)**

## ANTI-PATTERNS DETECTED
- [ ] Refusing to Pigeonhole (serving everyone)
- [ ] Positioning on Outcomes Only (grow revenue)
- [ ] Platform Before Point Solution
- [ ] No Competitive Frame

## OVERALL POSITIONING SCORE (0-100)
- Weighted average of components
- List top 3 strengths
- List top 3 weaknesses""",
        "asset_content": asset_content,
        "company_context": company_context,
    })


# =============================================================================
# MESSAGING ANALYSIS TOOL
# =============================================================================

@tool
def analyze_messaging(
    asset_content: str,
    target_persona: str | None = None,
) -> str:
    """
    Analyze the messaging hierarchy of a marketing asset.

    Evaluates the five layers of messaging:
    1. Positioning Statement (internal)
    2. Value Proposition (hero)
    3. Key Messages (pillars)
    4. Proof Points (evidence)
    5. Micro-Copy (CTAs, buttons)

    Args:
        asset_content: The marketing asset content to analyze
        target_persona: Optional target persona for persona-specific analysis

    Returns:
        JSON with messaging analysis including layer-by-layer assessment
    """
    return json.dumps({
        "task": "messaging_analysis",
        "instructions": """Analyze messaging using the 5-layer hierarchy:

## LAYER 1: POSITIONING STATEMENT
- Can you infer: "For [target] who [situation], [product] is a [category] that [benefit]. Unlike [alternative], we [differentiator]"?
- Score (0-100):

## LAYER 2: VALUE PROPOSITION
- Is there a clear value prop in the hero?
- Components present: Capability / Audience / Benefit / Differentiator
- Quote the value proposition if present
- Score (0-100):

## LAYER 3: KEY MESSAGES (Pillars)
- How many key messages/pillars?
- Are they benefit-oriented or feature lists?
- Quote each pillar
- Score (0-100):

## LAYER 4: PROOF POINTS
- Customer quotes present?
- Metrics/results with numbers?
- Logos present?
- Awards/recognition?
- Score (0-100):

## LAYER 5: MICRO-COPY
- CTA button text (benefit-oriented?)
- Headlines (clear or clever?)
- Consistent terminology?
- Score (0-100):

## MESSAGING HOUSE ASSESSMENT
```
Value Prop: [quote]
├── Pillar 1: [quote]
├── Pillar 2: [quote]
├── Pillar 3: [quote]
└── Foundation: [target audience]
```

## CLARITY TESTS
- **5-Second Clarity (0-100):** Immediate understanding?
- **Specificity (0-100):** Numbers, metrics, concrete outcomes?
- **Benefit-Orientation (0-100):** Features → benefits?

## ANTI-PATTERNS DETECTED
- [ ] Feature Dumping
- [ ] Jargon/Buzzwords (list them)
- [ ] Clever Over Clear
- [ ] Saying Everything
- [ ] No Specificity

## OVERALL MESSAGING SCORE (0-100)""",
        "asset_content": asset_content,
        "target_persona": target_persona,
    })


# =============================================================================
# HOMEPAGE STRUCTURE TOOL
# =============================================================================

@tool
def analyze_homepage_structure(
    asset_content: str,
    include_screenshots: bool = False,
) -> str:
    """
    Analyze the structure and UX of a homepage.

    Evaluates:
    - Hero section effectiveness
    - Information hierarchy
    - CTA strategy
    - Social proof placement
    - Visual structure

    Args:
        asset_content: Homepage content (HTML, text, or description)
        include_screenshots: Whether screenshot analysis is included

    Returns:
        JSON with structural analysis and UX recommendations
    """
    return json.dumps({
        "task": "homepage_structure_analysis",
        "instructions": """Analyze homepage structure:

## HERO SECTION
- **Headline:** Quote it. Is it clear or clever?
- **Subheadline:** Does it support or repeat?
- **Primary CTA:** Text and placement
- **Social Proof in Hero:** Logos visible?
- **Headline Clarity Score (0-100)**
- **CTA Clarity Score (0-100)**

## INFORMATION HIERARCHY
- What's above the fold?
- Is most important info first?
- Is the page scannable?
- Score (0-100):

## CTA STRATEGY
- Count of CTAs above fold:
- Primary CTA obvious? (yes/no)
- Secondary path for not-ready visitors?
- **Too many CTAs?** (>3 = problem)

## SOCIAL PROOF
- Logos present? Recognizable?
- Testimonials present? Names/titles included?
- Metrics present? Specific results?
- Score (0-100):

## ANTI-PATTERNS DETECTED
- [ ] Unclear Hero
- [ ] Too Many CTAs
- [ ] Missing Social Proof
- [ ] Wall of Text
- [ ] Stock Photos

## SECTION-BY-SECTION BREAKDOWN
List each section with:
- Purpose
- Effectiveness (0-100)
- Issues

## OVERALL HOMEPAGE SCORE (0-100)""",
        "asset_content": asset_content,
        "include_screenshots": include_screenshots,
    })


# =============================================================================
# ANTI-PATTERN DETECTOR
# =============================================================================

@tool
def detect_anti_patterns(
    asset_content: str,
    asset_type: Literal["homepage", "landing_page", "sales_deck", "email", "ad", "all"] = "all",
) -> str:
    """
    Scan a marketing asset for common PMM anti-patterns.

    Detects patterns across:
    - Positioning mistakes
    - Messaging mistakes
    - Homepage mistakes
    - ICP mistakes
    - GTM mistakes

    Args:
        asset_content: The marketing asset to scan
        asset_type: Type of asset for context-appropriate detection

    Returns:
        JSON with detected anti-patterns, severity, and fixes
    """
    return json.dumps({
        "task": "anti_pattern_detection",
        "instructions": """Scan for PMM anti-patterns:

## CRITICAL (Must Fix Immediately)

### 1. Refusing to Pigeonhole
- [ ] DETECTED? Evidence:
- Specific text:
- Impact:
- Fix:

### 2. Positioning on Outcomes Only
- [ ] DETECTED? Evidence:
- Specific text:
- Impact:
- Fix:

### 3. No Competitive Frame
- [ ] DETECTED? Evidence:
- Missing elements:
- Fix:

### 4. Unclear Hero (if homepage)
- [ ] DETECTED? Evidence:
- Specific text:
- Fix:

## HIGH PRIORITY (Should Fix)

### 5. Feature Dumping
- [ ] DETECTED?
- Feature list without benefits:
- Fix: "So what?" translation

### 6. Jargon/Buzzwords
- [ ] DETECTED?
- List all buzzwords found:
- Plain English alternatives:

### 7. Clever Over Clear
- [ ] DETECTED?
- Clever phrase:
- Clear alternative:

### 8. Too Many CTAs (if homepage)
- [ ] DETECTED?
- Count:
- Primary should be:

### 9. Missing Social Proof
- [ ] DETECTED?
- What's missing:
- Recommendation:

### 10. No Specificity
- [ ] DETECTED?
- Generic claims:
- Specific alternatives:

## MEDIUM PRIORITY

### 11. Platform Before Point Solution
- [ ] DETECTED?

### 12. Saying Everything
- [ ] DETECTED?
- Count of use cases/features:

### 13. Too Broad ICP
- [ ] DETECTED?

### 14. Wall of Text
- [ ] DETECTED?

## SUMMARY
- Critical issues: [count]
- High priority: [count]
- Medium: [count]
- Top 3 to fix first:""",
        "asset_content": asset_content,
        "asset_type": asset_type,
    })


# =============================================================================
# REWRITE GENERATOR
# =============================================================================

@tool
def generate_rewrite(
    original_copy: str,
    issue_type: Literal[
        "unclear_headline",
        "jargon_buzzwords",
        "feature_dump",
        "no_specificity",
        "clever_over_clear",
        "weak_cta",
        "generic_value_prop",
        "no_competitive_frame",
    ],
    target_persona: str | None = None,
    competitive_alternative: str | None = None,
) -> str:
    """
    Generate improved copy based on identified issues.

    Args:
        original_copy: The original problematic copy
        issue_type: The type of issue to fix
        target_persona: Optional target persona for personalization
        competitive_alternative: Optional competitive alternative for framing

    Returns:
        JSON with original, issue analysis, and rewritten alternatives
    """
    rewrite_instructions = {
        "unclear_headline": "Rewrite to clearly state WHAT + WHO. No cleverness.",
        "jargon_buzzwords": "Replace all jargon with customer language. Be specific.",
        "feature_dump": "Apply 'So what?' to each feature until you reach benefit.",
        "no_specificity": "Add numbers, timeframes, concrete outcomes.",
        "clever_over_clear": "Make it boring and clear. State exactly what it does.",
        "weak_cta": "Make CTA benefit-oriented. What happens when they click?",
        "generic_value_prop": "Add problem + specific solution + for whom.",
        "no_competitive_frame": "Add 'Unlike X' or 'Instead of Y' framing.",
    }

    return json.dumps({
        "task": "copy_rewrite",
        "instructions": f"""Rewrite this copy to fix: {issue_type}

**Original:**
{original_copy}

**Issue:** {issue_type}
**Fix approach:** {rewrite_instructions.get(issue_type, "Improve clarity and specificity")}

**Target persona:** {target_persona or "Not specified"}
**Competitive alternative:** {competitive_alternative or "Not specified"}

Provide:
1. **Analysis:** Why the original fails
2. **Rewrite Option 1:** Conservative improvement
3. **Rewrite Option 2:** Bold improvement
4. **Rewrite Option 3:** If persona specified, persona-specific version
5. **Why these work:** Explanation of improvements""",
        "original_copy": original_copy,
        "issue_type": issue_type,
    })


# =============================================================================
# COMPETITIVE FRAME BUILDER
# =============================================================================

@tool
def build_competitive_frame(
    product_description: str,
    known_competitors: list[str] | None = None,
    current_positioning: str | None = None,
) -> str:
    """
    Build a competitive frame for positioning.

    Identifies what the product should be positioned against:
    - Direct competitors
    - Manual processes
    - Status quo
    - Homegrown solutions

    Args:
        product_description: Description of the product/service
        known_competitors: List of known competitors if any
        current_positioning: Current positioning if exists

    Returns:
        JSON with competitive frame options and recommendations
    """
    return json.dumps({
        "task": "competitive_frame_building",
        "instructions": """Build competitive frame:

## COMPETITIVE ALTERNATIVES ANALYSIS

### Option 1: Direct Competitor
- Who is the most obvious competitor?
- What's their weakness?
- Frame: "Unlike [competitor], we..."

### Option 2: Manual Process
- What do people do without this product?
- What's painful about it?
- Frame: "Instead of [manual process], you can..."

### Option 3: Status Quo
- What happens if they do nothing?
- What's the cost of inaction?
- Frame: "Stop [painful status quo]. Start..."

### Option 4: Homegrown Solution
- Do teams build this internally?
- Why does that fail?
- Frame: "Replace your [homegrown solution] with..."

## RECOMMENDED FRAME
- Primary alternative:
- Why this frame:
- Positioning statement using this frame:

## DIFFERENTIATION STATEMENTS
Generate 3 "Unlike X, we Y" statements:
1.
2.
3.

## VALIDATION QUESTIONS
To validate this frame, ask customers:
1.
2.
3.""",
        "product_description": product_description,
        "known_competitors": known_competitors,
        "current_positioning": current_positioning,
    })


# =============================================================================
# ICP ANALYZER
# =============================================================================

@tool
def analyze_icp(
    asset_content: str,
    additional_context: str | None = None,
) -> str:
    """
    Analyze how well an asset defines and targets an Ideal Customer Profile.

    Args:
        asset_content: Marketing asset to analyze
        additional_context: Additional company/product context

    Returns:
        JSON with ICP analysis including specificity scores
    """
    return json.dumps({
        "task": "icp_analysis",
        "instructions": """Analyze ICP definition:

## FIRMOGRAPHICS IDENTIFIED
- Company Size: (specific or "all sizes"?)
- Industry: (specific or "any industry"?)
- Geography: (specific or global?)
- Tech Stack: (mentioned or not?)
- Specificity Score (0-100):

## SITUATION/TRIGGER
- What triggers the buy? (identified or missing?)
- Is there urgency? (why now?)
- Score (0-100):

## PAIN POINTS
- Specific pain identified?
- Cost of not solving?
- Score (0-100):

## PERSONA CLARITY
- Role/title specific?
- Buyer vs. user distinction?
- How many personas implied?
- Score (0-100):

## ANTI-PATTERNS
- [ ] Too Broad ICP
- [ ] Aspirational ICP (dream vs. actual customers)
- [ ] Demographic-Only (no situation/trigger)
- [ ] Too Many Personas

## INFERRED ICP
Based on the asset, the implied ICP is:
- Role:
- Company:
- Situation:
- Pain:

## RECOMMENDATIONS
- Is this specific enough to execute?
- What should be narrowed?
- What's missing?

## ICP CLARITY SCORE (0-100)""",
        "asset_content": asset_content,
        "additional_context": additional_context,
    })


# =============================================================================
# COMPLETE PMM AUDIT
# =============================================================================

@tool
def run_complete_pmm_audit(
    asset_content: str,
    asset_type: Literal["homepage", "landing_page", "sales_deck", "email", "ad"] = "homepage",
    asset_url: str | None = None,
    company_context: str | None = None,
) -> str:
    """
    Run a complete PMM audit covering all aspects.

    This is the comprehensive tool that runs:
    - 5-Second Test
    - Positioning Analysis
    - Messaging Analysis
    - Homepage Structure (if applicable)
    - Anti-Pattern Detection
    - ICP Analysis

    Args:
        asset_content: The marketing asset to audit
        asset_type: Type of asset
        asset_url: URL if available
        company_context: Additional context about the company

    Returns:
        JSON with complete audit including prioritized issues and recommendations
    """
    return json.dumps({
        "task": "complete_pmm_audit",
        "instructions": """Run complete PMM audit:

# PMM AUDIT REPORT

## EXECUTIVE SUMMARY
(2-3 sentences on overall state)

## 1. 5-SECOND TEST
- What they do: clear/partial/unclear
- Who it's for: clear/partial/unclear
- What's different: clear/partial/unclear
- What to do next: clear/partial/unclear
- **VERDICT:** PASS/PARTIAL/FAIL

## 2. POSITIONING ANALYSIS
| Element | Score | Notes |
|---------|-------|-------|
| Competitive Frame | /100 | |
| Target Audience | /100 | |
| Differentiation | /100 | |
| Problem Clarity | /100 | |
| **OVERALL** | /100 | |

## 3. MESSAGING ANALYSIS
| Layer | Present | Score | Issues |
|-------|---------|-------|--------|
| Positioning Statement | Y/N | /100 | |
| Value Proposition | Y/N | /100 | |
| Key Messages | Y/N | /100 | |
| Proof Points | Y/N | /100 | |
| Micro-Copy | Y/N | /100 | |
| **OVERALL** | | /100 | |

## 4. HOMEPAGE STRUCTURE (if applicable)
| Element | Score | Issues |
|---------|-------|--------|
| Hero Clarity | /100 | |
| CTA Strategy | /100 | |
| Social Proof | /100 | |
| Information Hierarchy | /100 | |
| **OVERALL** | /100 | |

## 5. ANTI-PATTERNS DETECTED
### Critical (Must Fix)
1.
2.

### High Priority (Should Fix)
1.
2.

### Medium (Consider)
1.

## 6. ICP CLARITY
- Specificity Score: /100
- Issues:

## PRIORITIZED ISSUES

### Critical (Fix This Week)
| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| | | | |

### High Priority (Fix This Month)
| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| | | | |

### Nice to Have
| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| | | | |

## WHAT'S WORKING
1.
2.
3.

## KEY REWRITES NEEDED

**Current:** "..."
**Suggested:** "..."
**Why:** ...

(Repeat for top 3 copy issues)

## OVERALL SCORES
| Dimension | Score |
|-----------|-------|
| Positioning | /100 |
| Messaging | /100 |
| Homepage UX | /100 |
| ICP Clarity | /100 |
| **OVERALL PMM SCORE** | /100 |

## READY TO SHIP?
[ ] YES - Minor polish only
[ ] NEEDS WORK - Significant improvements needed
[ ] NO - Critical issues must be addressed

## NEXT STEPS
1.
2.
3.""",
        "asset_content": asset_content,
        "asset_type": asset_type,
        "asset_url": asset_url,
        "company_context": company_context,
    })
