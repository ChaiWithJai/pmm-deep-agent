"""
PMM Deep Agent

A Deep Agent for evaluating Product Marketing (PMM) work.
Inspired by ChatPRD's approach to PM documentation, but for marketing evaluation.

Quick Start:
    ```python
    from pmm_agent import create_pmm_agent, evaluate_homepage

    # Full agent
    agent = create_pmm_agent()
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Analyze https://example.com"}]
    })

    # Quick evaluation
    result = evaluate_homepage("https://example.com")
    ```
"""

from pmm_agent.agent import (
    create_pmm_agent,
    evaluate_homepage,
    create_positioning,
    compare_competitors,
    agent,
)

__all__ = [
    "create_pmm_agent",
    "evaluate_homepage",
    "create_positioning",
    "compare_competitors",
    "agent",
]
