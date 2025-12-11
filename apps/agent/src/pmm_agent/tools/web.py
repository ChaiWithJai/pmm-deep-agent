"""
Web Fetching Tools for PMM Agent

Tools for fetching and analyzing live websites and marketing assets.
"""

import json
from typing import Literal
from langchain_core.tools import tool


@tool
def fetch_homepage(
    url: str,
    extract_mode: Literal["full", "above_fold", "hero_only"] = "full",
) -> str:
    """
    Fetch a homepage URL and extract content for PMM analysis.

    Args:
        url: The URL to fetch
        extract_mode: What portion to focus on
            - full: Entire page
            - above_fold: Estimated above-fold content
            - hero_only: Just the hero section

    Returns:
        JSON with page content structured for PMM analysis
    """
    return json.dumps({
        "task": "fetch_homepage",
        "instructions": f"""Fetch and analyze the homepage at: {url}

Extract and structure:

## HERO SECTION
- Headline (exact text)
- Subheadline (exact text)
- Primary CTA (button text)
- Secondary CTA (if present)
- Logo/brand name
- Navigation items
- Social proof in hero (logos, stats)

## ABOVE THE FOLD
- All visible text without scrolling
- Visual elements described
- Layout structure

## FULL PAGE SECTIONS (in order)
For each section:
- Section name/purpose
- Headline
- Key copy
- CTAs
- Social proof elements

## SOCIAL PROOF INVENTORY
- Logo bar: [list companies]
- Testimonials: [quote, name, title, company]
- Metrics: [specific numbers claimed]
- Case studies: [titles/summaries]
- Awards/badges: [list]

## CTA INVENTORY
List every CTA on the page:
- Text | Location | Primary/Secondary

## META INFORMATION
- Page title
- Meta description
- Open Graph tags (if visible)

Extract mode: {extract_mode}""",
        "url": url,
        "extract_mode": extract_mode,
    })


@tool
def fetch_competitor_homepage(
    competitor_url: str,
    your_url: str | None = None,
) -> str:
    """
    Fetch a competitor's homepage for comparative analysis.

    Args:
        competitor_url: The competitor's homepage URL
        your_url: Your homepage URL for comparison (optional)

    Returns:
        JSON with competitor analysis structured for positioning comparison
    """
    return json.dumps({
        "task": "competitor_analysis",
        "instructions": f"""Analyze competitor homepage: {competitor_url}

## COMPETITOR POSITIONING
- What do they claim to do?
- Who do they target?
- What's their key differentiator?
- What category do they claim?

## COMPETITOR MESSAGING
- Value proposition (hero)
- Key message pillars
- Proof points used
- CTA strategy

## COMPETITOR WEAKNESSES
- What's unclear?
- What's missing?
- What's overpromised?
- Where are they vulnerable?

## DIFFERENTIATION OPPORTUNITIES
Based on their positioning, you could:
1. Own a different segment
2. Solve a different problem
3. Use a different approach
4. Claim a different attribute

## COMPETITIVE FRAME SUGGESTIONS
"Unlike [competitor], we..."
1.
2.
3.

{f"Compare against your site: {your_url}" if your_url else ""}""",
        "competitor_url": competitor_url,
        "your_url": your_url,
    })


@tool
def analyze_landing_page(
    url: str,
    campaign_context: str | None = None,
) -> str:
    """
    Analyze a landing page for conversion optimization.

    Args:
        url: The landing page URL
        campaign_context: What campaign this supports (optional)

    Returns:
        JSON with landing page analysis focused on conversion
    """
    return json.dumps({
        "task": "landing_page_analysis",
        "instructions": f"""Analyze landing page: {url}

## MESSAGE MATCH
- Does the headline match the likely ad/source?
- Is there message continuity?
- Score (0-100):

## SINGLE FOCUS
- Is there ONE clear offer?
- Are there distracting navigation/links?
- Score (0-100):

## VALUE PROPOSITION
- Is the value clear above fold?
- Is it specific to this offer?
- Score (0-100):

## FORM ANALYSIS (if present)
- Number of fields:
- Friction level:
- Value exchange clear?

## TRUST ELEMENTS
- Social proof present?
- Security indicators?
- Testimonials specific to offer?

## CTA ANALYSIS
- Primary CTA text:
- Is it benefit-oriented?
- Is there urgency/scarcity?
- Contrast and visibility?

## MOBILE CONSIDERATIONS
- Likely mobile-friendly?
- Key content above fold on mobile?

## CONVERSION BLOCKERS
List anything that might prevent conversion:
1.
2.
3.

## RECOMMENDATIONS
Priority fixes:
1.
2.
3.

{f"Campaign context: {campaign_context}" if campaign_context else ""}""",
        "url": url,
        "campaign_context": campaign_context,
    })


@tool
def scrape_social_proof(
    url: str,
) -> str:
    """
    Extract and inventory all social proof from a page.

    Args:
        url: The URL to analyze

    Returns:
        JSON with comprehensive social proof inventory and assessment
    """
    return json.dumps({
        "task": "social_proof_inventory",
        "instructions": f"""Extract all social proof from: {url}

## LOGO BAR
- Companies shown: [list all]
- Recognizable to target? (yes/partial/no)
- Placement on page:

## TESTIMONIALS
For each testimonial:
| Quote | Name | Title | Company | Specific Result? |
|-------|------|-------|---------|------------------|
| | | | | |

## METRICS/STATS
| Claim | Specific? | Believable? |
|-------|-----------|-------------|
| | | |

## CASE STUDIES
- Titles:
- Specific outcomes mentioned:
- Named companies:

## AWARDS/RECOGNITION
- Badges shown:
- Publications mentioned:
- Certifications:

## SOCIAL PROOF ASSESSMENT

### Strengths
- What's working well?

### Gaps
- What's missing?
- What would strengthen trust?

### Recommendations
1.
2.
3.

## SOCIAL PROOF SCORE (0-100)
- Quantity:
- Quality:
- Specificity:
- Relevance:
- **Overall:**""",
        "url": url,
    })
