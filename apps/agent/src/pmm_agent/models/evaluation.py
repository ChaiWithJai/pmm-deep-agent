"""
PMM Evaluation Models

Structured data models for PMM assessment based on proven frameworks:
- Positioning Canvas (April Dunford methodology)
- Messaging Hierarchy (5 layers)
- Anti-Pattern Detection
"""

from enum import IntEnum
from typing import Literal
from pydantic import BaseModel, Field


# =============================================================================
# SCORING ENUMS
# =============================================================================

class ScoreLevel(IntEnum):
    """Score levels for PMM evaluations (0-100 scale)."""
    FAILING = 0      # Critical issues, needs complete rework
    POOR = 25        # Major gaps, significant work needed
    NEEDS_WORK = 50  # Foundational issues, improvements required
    GOOD = 75        # Solid foundation, minor refinements
    EXCELLENT = 100  # Best-in-class, ready to ship


class Severity(IntEnum):
    """Issue severity levels."""
    LOW = 1      # Nice to fix, won't block
    MEDIUM = 2   # Should fix, impacts effectiveness
    HIGH = 3     # Must fix, significantly hurting
    CRITICAL = 4 # Blocking, immediate attention required


# =============================================================================
# POSITIONING MODELS
# =============================================================================

class CompetitiveAlternative(BaseModel):
    """What you're positioning against."""
    alternative_type: Literal["direct_competitor", "manual_process", "status_quo", "homegrown", "spreadsheets"]
    name: str = Field(..., description="Name of the competitive alternative")
    pain_points: list[str] = Field(..., description="Why the alternative sucks")
    is_explicit: bool = Field(..., description="Is this explicitly stated or implied?")


class TargetCustomer(BaseModel):
    """Who the positioning is for."""
    role_title: str | None = Field(None, description="Job role/title")
    company_type: str | None = Field(None, description="Type of company (B2B SaaS, agency, etc.)")
    company_size: str | None = Field(None, description="Company size/stage")
    industry: str | None = Field(None, description="Industry vertical")
    situation_trigger: str | None = Field(None, description="What triggers them to buy")
    specificity_score: int = Field(..., ge=0, le=100, description="How specific is the targeting?")


class Differentiation(BaseModel):
    """What makes this different."""
    unique_approach: str | None = Field(None, description="How they do it differently")
    key_capability: str | None = Field(None, description="Unique capability")
    is_defensible: bool = Field(..., description="Is this hard to copy?")
    is_meaningful: bool = Field(..., description="Do customers care?")
    could_competitor_say_same: bool = Field(..., description="Could any competitor claim this?")


class PositioningStrategy(BaseModel):
    """Overall positioning approach."""
    strategy_type: Literal["category_based", "use_case_based", "unclear"]
    category_or_use_case: str | None = Field(None, description="The category or use case")
    competitive_frame_score: int = Field(..., ge=0, le=100)
    target_audience_score: int = Field(..., ge=0, le=100)
    differentiation_score: int = Field(..., ge=0, le=100)
    problem_clarity_score: int = Field(..., ge=0, le=100)


class PositioningAnalysis(BaseModel):
    """Complete positioning assessment."""
    target_customer: TargetCustomer
    competitive_alternative: CompetitiveAlternative | None
    differentiation: Differentiation
    strategy: PositioningStrategy

    # Derived scores
    overall_score: int = Field(..., ge=0, le=100)

    # Key findings
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    # Anti-patterns detected
    refusing_to_pigeonhole: bool = False
    positioning_on_outcomes_only: bool = False
    platform_before_point_solution: bool = False
    no_competitive_frame: bool = False


# =============================================================================
# MESSAGING MODELS
# =============================================================================

class MessagingLayer(BaseModel):
    """Analysis of a single messaging layer."""
    layer_name: Literal[
        "positioning_statement",
        "value_proposition",
        "key_messages",
        "proof_points",
        "micro_copy"
    ]
    present: bool = Field(..., description="Is this layer present?")
    quality_score: int = Field(..., ge=0, le=100)
    content_found: str | None = Field(None, description="What was found for this layer")
    issues: list[str] = Field(default_factory=list)


class MessagingHouse(BaseModel):
    """The messaging house framework assessment."""
    value_proposition: str | None = Field(None, description="Top of house - value prop")
    pillars: list[str] = Field(default_factory=list, description="3 key message pillars")
    proof_points_per_pillar: dict[str, list[str]] = Field(default_factory=dict)
    foundation_defined: bool = Field(..., description="Is target audience clear?")

    structure_score: int = Field(..., ge=0, le=100)


class MessagingAnalysis(BaseModel):
    """Complete messaging assessment."""
    layers: list[MessagingLayer]
    messaging_house: MessagingHouse

    # Clarity tests
    clarity_score: int = Field(..., ge=0, le=100, description="Can someone understand in 5 seconds?")
    specificity_score: int = Field(..., ge=0, le=100, description="Numbers, metrics, concrete outcomes?")
    benefit_orientation_score: int = Field(..., ge=0, le=100, description="Features translated to benefits?")

    # Anti-patterns detected
    feature_dumping: bool = False
    jargon_buzzwords: list[str] = Field(default_factory=list)
    clever_over_clear: bool = False
    saying_everything: bool = False
    no_specificity: bool = False

    overall_score: int = Field(..., ge=0, le=100)


# =============================================================================
# HOMEPAGE/ASSET MODELS
# =============================================================================

class FiveSecondTest(BaseModel):
    """The 5-second test assessment."""
    what_they_do: Literal["clear", "partial", "unclear"]
    who_its_for: Literal["clear", "partial", "unclear"]
    whats_different: Literal["clear", "partial", "unclear"]
    what_to_do_next: Literal["clear", "partial", "unclear"]

    passed: bool = Field(..., description="Did they pass the 5-second test?")
    notes: str = Field(..., description="First impression notes")


class HeroSection(BaseModel):
    """Hero section analysis."""
    headline: str | None
    subheadline: str | None
    cta_text: str | None
    social_proof_present: bool

    headline_clarity_score: int = Field(..., ge=0, le=100)
    cta_clarity_score: int = Field(..., ge=0, le=100)


class SocialProof(BaseModel):
    """Social proof analysis."""
    logos_present: bool
    logos_recognizable: bool
    testimonials_present: bool
    testimonials_have_names_titles: bool
    metrics_present: bool
    specific_results: bool

    overall_score: int = Field(..., ge=0, le=100)


class HomepageAnalysis(BaseModel):
    """Complete homepage assessment."""
    five_second_test: FiveSecondTest
    hero: HeroSection
    social_proof: SocialProof

    # Structure analysis
    information_hierarchy_score: int = Field(..., ge=0, le=100)
    scannable: bool
    cta_count: int
    primary_cta_clear: bool

    # Anti-patterns
    unclear_hero: bool = False
    too_many_ctas: bool = False
    missing_social_proof: bool = False
    wall_of_text: bool = False
    stock_photos: bool = False

    overall_score: int = Field(..., ge=0, le=100)


# =============================================================================
# ISSUE TRACKING
# =============================================================================

class PMMIssue(BaseModel):
    """A specific PMM issue found during evaluation."""
    category: Literal["positioning", "messaging", "homepage", "icp", "gtm"]
    severity: Severity
    issue: str = Field(..., description="What's wrong")
    why_it_matters: str = Field(..., description="Impact of this issue")
    recommendation: str = Field(..., description="How to fix it")
    suggested_rewrite: str | None = Field(None, description="If copy issue, suggested new copy")
    location: str | None = Field(None, description="Where in the asset this appears")


class PMMEvaluationResult(BaseModel):
    """Complete PMM evaluation result."""
    asset_type: Literal["homepage", "landing_page", "sales_deck", "email", "ad", "other"]
    asset_url: str | None = None

    # Component analyses
    positioning: PositioningAnalysis
    messaging: MessagingAnalysis
    homepage: HomepageAnalysis | None = None

    # Issues (prioritized)
    critical_issues: list[PMMIssue] = Field(default_factory=list)
    high_priority_issues: list[PMMIssue] = Field(default_factory=list)
    medium_issues: list[PMMIssue] = Field(default_factory=list)
    low_issues: list[PMMIssue] = Field(default_factory=list)

    # What's working
    strengths: list[str] = Field(default_factory=list)

    # Overall assessment
    overall_score: int = Field(..., ge=0, le=100)
    ready_to_ship: bool = False
    executive_summary: str = Field(..., description="2-3 sentence summary")

    # Anti-pattern summary
    anti_patterns_detected: list[str] = Field(default_factory=list)


# =============================================================================
# POSITIONING CANVAS (Template for generation)
# =============================================================================

class PositioningCanvas(BaseModel):
    """The positioning canvas template for creation/improvement."""
    # Section 1: Target Customer
    role_title: str
    company_type: str
    company_size: str
    industry: str
    situation_trigger: str

    # Section 2: Competitive Alternative
    primary_alternative: str
    alternative_type: Literal["direct_competitor", "manual_process", "status_quo", "homegrown"]

    # Section 3: Why That Sucks
    pain_point_1: str
    pain_point_2: str
    pain_point_3: str

    # Section 4: Unique Approach
    key_differentiator: str
    methodology: str
    unique_capability: str

    # Section 5: Why That's Better
    primary_benefit: str
    supporting_benefit: str
    proof_point: str

    # Section 6: Strategy
    positioning_approach: Literal["category_based", "use_case_based"]
    category_or_use_case: str

    # Section 7: Statements
    internal_positioning_statement: str
    differentiation_summary: str
    homepage_one_liner: str

    # Validation
    is_validated: bool = False
    validation_notes: str | None = None
