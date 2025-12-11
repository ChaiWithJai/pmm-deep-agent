"""
PMM Deep Agent

A Deep Agent for evaluating Product Marketing (PMM) work.
Inspired by ChatPRD's approach to PM documentation, but for marketing evaluation.

Uses the LangChain Deep Agents framework with:
- create_deep_agent() as the main entry point
- Specialized tools for PMM evaluation
- Subagents for deep-dive analysis
- Middleware for caching and human-in-the-loop

Based on proven PMM frameworks:
- April Dunford's positioning methodology
- Fletch PMM messaging hierarchy
- B2B homepage best practices
"""

import os
from typing import Literal

from deepagents import create_deep_agent
from langchain_anthropic import ChatAnthropic

from pmm_agent.prompts import PMM_EVALUATOR_SYSTEM_PROMPT
from pmm_agent.subagents.specialists import PMM_SUBAGENTS
from pmm_agent.tools.evaluation import (
    run_five_second_test,
    analyze_positioning,
    analyze_messaging,
    analyze_homepage_structure,
    detect_anti_patterns,
    generate_rewrite,
    build_competitive_frame,
    analyze_icp,
    run_complete_pmm_audit,
)
from pmm_agent.tools.web import (
    fetch_homepage,
    fetch_competitor_homepage,
    analyze_landing_page,
    scrape_social_proof,
)
from pmm_agent.tools.creation import (
    create_positioning_canvas,
    create_messaging_framework,
    create_homepage_wireframe,
    generate_differentiation_statements,
)


# =============================================================================
# AGENT CONFIGURATION
# =============================================================================

# Default model - Claude Sonnet 4 for balanced performance
DEFAULT_MODEL = "claude-sonnet-4-20250514"


def get_model(model_name: str | None = None) -> ChatAnthropic:
    """Get a ChatAnthropic model instance.

    Args:
        model_name: Model name (e.g., "claude-sonnet-4-20250514").
                   If None, uses DEFAULT_MODEL.

    Returns:
        ChatAnthropic instance
    """
    name = model_name or DEFAULT_MODEL
    return ChatAnthropic(model_name=name, max_tokens=20000)

# Detect if running in LangGraph API environment
running_in_langgraph_api = os.getenv("LANGGRAPH_API_URL") is not None


# =============================================================================
# TOOL REGISTRY
# =============================================================================

# Evaluation tools - for analyzing existing assets
EVALUATION_TOOLS = [
    run_five_second_test,
    analyze_positioning,
    analyze_messaging,
    analyze_homepage_structure,
    detect_anti_patterns,
    generate_rewrite,
    build_competitive_frame,
    analyze_icp,
    run_complete_pmm_audit,
]

# Web tools - for fetching and analyzing live sites
WEB_TOOLS = [
    fetch_homepage,
    fetch_competitor_homepage,
    analyze_landing_page,
    scrape_social_proof,
]

# Creation tools - for generating PMM assets
CREATION_TOOLS = [
    create_positioning_canvas,
    create_messaging_framework,
    create_homepage_wireframe,
    generate_differentiation_statements,
]

# All tools combined
ALL_TOOLS = EVALUATION_TOOLS + WEB_TOOLS + CREATION_TOOLS


# =============================================================================
# AGENT FACTORY
# =============================================================================

def create_pmm_agent(
    model: str | None = None,
    mode: Literal["evaluate", "create", "full"] = "full",
    use_memory: bool = True,
    include_subagents: bool = True,
):
    """
    Create a PMM Deep Agent for evaluating and creating marketing assets.

    Args:
        model: The model name to use (default: Claude Sonnet 4).
               Pass None to use the default model.
        mode: Operating mode
            - "evaluate": Only evaluation tools (analyze existing assets)
            - "create": Only creation tools (generate new assets)
            - "full": All tools (evaluate and create)
        use_memory: Whether to enable conversation memory
        include_subagents: Whether to include specialist subagents

    Returns:
        A LangGraph StateGraph configured for PMM evaluation

    Example:
        ```python
        agent = create_pmm_agent()
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "Analyze the homepage at https://example.com"
            }]
        })
        ```
    """
    # Select tools based on mode
    if mode == "evaluate":
        tools = EVALUATION_TOOLS + WEB_TOOLS
    elif mode == "create":
        tools = CREATION_TOOLS
    else:  # "full"
        tools = ALL_TOOLS

    # Configure subagents
    subagents = PMM_SUBAGENTS if include_subagents else []

    # Get model instance
    model_instance = get_model(model)

    # Create the Deep Agent
    return create_deep_agent(
        model=model_instance,
        tools=tools,
        subagents=subagents,
        system_prompt=PMM_EVALUATOR_SYSTEM_PROMPT,
        # Memory handling: local checkpointer for CLI, none for LangGraph API
        checkpointer=True if (use_memory and not running_in_langgraph_api) else None,
        # Human-in-the-loop for high-stakes outputs (dict format required)
        interrupt_on={
            "create_positioning_canvas": True,   # Review positioning before finalizing
            "create_messaging_framework": True,  # Review messaging before finalizing
            "create_homepage_wireframe": True,   # Review wireframe before delivery
        },
    )


# =============================================================================
# DEFAULT AGENT INSTANCE
# =============================================================================

# Create the default agent for LangGraph deployment
agent = create_pmm_agent()


# =============================================================================
# QUICK START FUNCTIONS
# =============================================================================

def evaluate_homepage(url: str, model: str | None = None) -> dict:
    """
    Quick function to evaluate a homepage.

    Args:
        url: The homepage URL to evaluate
        model: Model to use

    Returns:
        PMM evaluation results
    """
    agent = create_pmm_agent(model=model, mode="evaluate")
    return agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Run a complete PMM audit on the homepage at {url}. "
                      f"Include 5-second test, positioning analysis, messaging analysis, "
                      f"and anti-pattern detection. Provide prioritized recommendations."
        }]
    })


def create_positioning(
    product_description: str,
    target_audience: str | None = None,
    competitors: list[str] | None = None,
    model: str | None = None,
) -> dict:
    """
    Quick function to create positioning.

    Args:
        product_description: What the product does
        target_audience: Who it's for
        competitors: Known competitors
        model: Model to use

    Returns:
        Positioning canvas and messaging framework
    """
    agent = create_pmm_agent(model=model, mode="create")

    prompt = f"Create a positioning canvas for: {product_description}"
    if target_audience:
        prompt += f"\nTarget audience: {target_audience}"
    if competitors:
        prompt += f"\nCompetitors: {', '.join(competitors)}"
    prompt += "\n\nAfter the positioning canvas, also create a messaging framework."

    return agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })


def compare_competitors(
    your_url: str,
    competitor_urls: list[str],
    model: str | None = None,
) -> dict:
    """
    Quick function to compare against competitors.

    Args:
        your_url: Your homepage URL
        competitor_urls: Competitor homepage URLs
        model: Model to use

    Returns:
        Competitive analysis with differentiation opportunities
    """
    agent = create_pmm_agent(model=model, mode="evaluate")

    competitor_list = "\n".join([f"- {url}" for url in competitor_urls])

    return agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"""Analyze my homepage ({your_url}) against these competitors:
{competitor_list}

For each competitor:
1. Analyze their positioning and messaging
2. Identify their weaknesses
3. Find differentiation opportunities for me

Then provide:
- Overall competitive landscape summary
- My unique positioning opportunities
- "Unlike X, we Y" statements for each competitor
- Recommended positioning angle
"""
        }]
    })
