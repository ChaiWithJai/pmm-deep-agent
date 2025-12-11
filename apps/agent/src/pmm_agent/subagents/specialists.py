"""
PMM Specialist Subagents

Specialized agents for deep-dive analysis in specific PMM domains.
Following the Deep Agents framework subagent pattern.
"""

from pmm_agent.prompts import (
    POSITIONING_ANALYST_PROMPT,
    MESSAGING_ANALYST_PROMPT,
    HOMEPAGE_ANALYST_PROMPT,
    ANTI_PATTERN_DETECTOR_PROMPT,
    ICP_ANALYST_PROMPT,
)
from pmm_agent.tools.evaluation import (
    analyze_positioning,
    analyze_messaging,
    detect_anti_patterns,
    generate_rewrite,
    build_competitive_frame,
    analyze_icp,
)
from pmm_agent.tools.web import (
    fetch_homepage,
    fetch_competitor_homepage,
)
from pmm_agent.tools.creation import (
    create_positioning_canvas,
    generate_differentiation_statements,
)


# =============================================================================
# POSITIONING ANALYST SUBAGENT
# =============================================================================

positioning_analyst_subagent = {
    "name": "positioning-analyst",
    "description": """Use this subagent when you need deep analysis of positioning strategy.

    Specializes in:
    - Positioning Canvas analysis (April Dunford methodology)
    - Competitive frame evaluation
    - Target customer specificity assessment
    - Differentiation meaningfulness and defensibility
    - Category vs. use-case positioning decisions

    Use for:
    - "Analyze the positioning of this homepage"
    - "Is the competitive frame clear?"
    - "How specific is the target audience?"
    - "Is the differentiation defensible?"
    """,
    "system_prompt": POSITIONING_ANALYST_PROMPT,
    "tools": [
        analyze_positioning,
        build_competitive_frame,
        create_positioning_canvas,
        generate_differentiation_statements,
        fetch_competitor_homepage,
    ],
}


# =============================================================================
# MESSAGING ANALYST SUBAGENT
# =============================================================================

messaging_analyst_subagent = {
    "name": "messaging-analyst",
    "description": """Use this subagent when you need deep analysis of messaging.

    Specializes in:
    - Five-layer messaging hierarchy assessment
    - Messaging house structure evaluation
    - Clarity and specificity scoring
    - Feature-to-benefit translation
    - Copy rewriting for clarity

    Use for:
    - "Analyze the messaging layers"
    - "Is the value proposition clear?"
    - "Are features translated to benefits?"
    - "Rewrite this jargon-filled copy"
    """,
    "system_prompt": MESSAGING_ANALYST_PROMPT,
    "tools": [
        analyze_messaging,
        generate_rewrite,
        detect_anti_patterns,
    ],
}


# =============================================================================
# HOMEPAGE ANALYST SUBAGENT
# =============================================================================

homepage_analyst_subagent = {
    "name": "homepage-analyst",
    "description": """Use this subagent when you need deep analysis of homepage structure and UX.

    Specializes in:
    - 5-second test execution
    - Hero section effectiveness
    - Information hierarchy assessment
    - CTA strategy evaluation
    - Social proof audit

    Use for:
    - "Does this homepage pass the 5-second test?"
    - "Is the hero section effective?"
    - "How's the CTA strategy?"
    - "What social proof is missing?"
    """,
    "system_prompt": HOMEPAGE_ANALYST_PROMPT,
    "tools": [
        fetch_homepage,
        detect_anti_patterns,
        generate_rewrite,
    ],
}


# =============================================================================
# ANTI-PATTERN DETECTOR SUBAGENT
# =============================================================================

anti_pattern_detector_subagent = {
    "name": "anti-pattern-detector",
    "description": """Use this subagent to scan for PMM anti-patterns and mistakes.

    Detects:
    - Positioning anti-patterns (pigeonholing refusal, outcome-only, no frame)
    - Messaging anti-patterns (jargon, feature dumps, clever over clear)
    - Homepage anti-patterns (unclear hero, too many CTAs)
    - ICP anti-patterns (too broad, aspirational)
    - GTM anti-patterns (founder bias, sales-driven positioning)

    Use for:
    - "What anti-patterns exist in this asset?"
    - "Scan for common PMM mistakes"
    - "What's hurting conversion?"
    """,
    "system_prompt": ANTI_PATTERN_DETECTOR_PROMPT,
    "tools": [
        detect_anti_patterns,
        generate_rewrite,
    ],
}


# =============================================================================
# ICP ANALYST SUBAGENT
# =============================================================================

icp_analyst_subagent = {
    "name": "icp-analyst",
    "description": """Use this subagent for Ideal Customer Profile analysis.

    Specializes in:
    - ICP specificity assessment
    - Persona definition evaluation
    - Situation/trigger identification
    - Firmographic analysis
    - Buyer vs. user distinction

    Use for:
    - "How specific is the ICP?"
    - "Is the target audience well-defined?"
    - "What triggers the buying decision?"
    - "Are there too many personas?"
    """,
    "system_prompt": ICP_ANALYST_PROMPT,
    "tools": [
        analyze_icp,
        detect_anti_patterns,
    ],
}


# =============================================================================
# COMPETITIVE ANALYST SUBAGENT
# =============================================================================

COMPETITIVE_ANALYST_PROMPT = """You are a competitive positioning specialist. Your job is to analyze how a company positions against competitors and identify differentiation opportunities.

## YOUR FOCUS

1. **Competitive Landscape Mapping**
   - Who are the direct competitors?
   - What alternatives do prospects consider?
   - What's the status quo?

2. **Positioning Gap Analysis**
   - Where are competitors weak?
   - What positions are unoccupied?
   - What segments are underserved?

3. **Differentiation Opportunities**
   - What unique capabilities exist?
   - What category could be created?
   - What audience could be owned?

4. **Competitive Messaging Analysis**
   - What do competitors claim?
   - What proof do they offer?
   - Where are they vulnerable?

## OUTPUT

Always provide:
- Specific competitor weaknesses to exploit
- Clear differentiation opportunities
- "Unlike X, we Y" statement recommendations
- Category or positioning angle suggestions
"""

competitive_analyst_subagent = {
    "name": "competitive-analyst",
    "description": """Use this subagent for competitive analysis and differentiation.

    Specializes in:
    - Competitor homepage analysis
    - Competitive positioning gaps
    - Differentiation opportunity identification
    - "Unlike X, we Y" statement generation

    Use for:
    - "How do we position against [competitor]?"
    - "What's our differentiation opportunity?"
    - "Analyze this competitor's positioning"
    """,
    "system_prompt": COMPETITIVE_ANALYST_PROMPT,
    "tools": [
        fetch_competitor_homepage,
        build_competitive_frame,
        generate_differentiation_statements,
        analyze_positioning,
    ],
}


# =============================================================================
# ALL SUBAGENTS EXPORT
# =============================================================================

PMM_SUBAGENTS = [
    positioning_analyst_subagent,
    messaging_analyst_subagent,
    homepage_analyst_subagent,
    anti_pattern_detector_subagent,
    icp_analyst_subagent,
    competitive_analyst_subagent,
]
