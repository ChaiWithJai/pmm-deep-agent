# PMM Deep Agent

A Deep Agent for evaluating Product Marketing (PMM) work, inspired by ChatPRD's approach to PM documentation.

## What This Agent Does

Evaluates and creates B2B marketing assets using proven PMM frameworks:
- **April Dunford's Positioning Methodology** - Competitive framing, differentiation
- **Fletch PMM Messaging Hierarchy** - 5-layer messaging framework
- **B2B Homepage Best Practices** - 5-second test, social proof, CTAs

## Architecture

```
pmm-deep-agent/
├── apps/agent/src/pmm_agent/
│   ├── agent.py           # Main agent using create_deep_agent()
│   ├── prompts.py         # System prompts with PMM expertise
│   ├── models/            # Pydantic models for evaluation
│   ├── tools/             # 17 PMM-specific tools
│   │   ├── evaluation.py  # Analysis tools
│   │   ├── web.py         # Web fetching tools
│   │   └── creation.py    # Asset generation tools
│   └── subagents/         # 6 specialist subagents
└── langgraph.json         # LangGraph Cloud deployment
```

## Core Tools

### Evaluation Tools
- `run_five_second_test` - Quick clarity assessment
- `analyze_positioning` - Positioning canvas analysis
- `analyze_messaging` - 5-layer messaging audit
- `analyze_homepage_structure` - Homepage UX analysis
- `detect_anti_patterns` - Common PMM mistakes
- `run_complete_pmm_audit` - Full evaluation

### Creation Tools
- `create_positioning_canvas` - April Dunford methodology
- `create_messaging_framework` - Messaging house builder
- `create_homepage_wireframe` - Section-by-section copy
- `generate_differentiation_statements` - "Unlike X, we Y"

### Web Tools
- `fetch_homepage` - Analyze live sites
- `fetch_competitor_homepage` - Competitive analysis
- `analyze_landing_page` - Conversion optimization
- `scrape_social_proof` - Social proof inventory

## Subagents

| Subagent | Specialization |
|----------|----------------|
| positioning-analyst | Competitive framing, differentiation |
| messaging-analyst | 5-layer hierarchy, clarity |
| homepage-analyst | 5-second test, UX |
| anti-pattern-detector | Common PMM mistakes |
| icp-analyst | Target customer specificity |
| competitive-analyst | Competitor positioning gaps |

## Key PMM Principles (Embedded in Prompts)

1. **Positioning IS Pigeonholing** - Own a place in YOUR customer's mind
2. **Customer Perception IS Reality** - What customers think matters
3. **Clarity Over Cleverness** - Boring and clear beats clever and confusing
4. **Problems Beat Outcomes** - "Increase revenue" is unspecific
5. **Point Solution Before Platform** - Win one use case first
6. **Competitive Alternative Anchoring** - Always define what you're better than

## Anti-Patterns Detected

### Critical
- Refusing to Pigeonhole ("we serve multiple markets")
- Positioning on Outcomes Only ("increase revenue")
- No Competitive Frame
- Unclear Hero

### High Priority
- Feature Dumping
- Jargon/Buzzwords
- Clever Over Clear
- Too Many CTAs
- Missing Social Proof

## Usage

```python
from pmm_agent import create_pmm_agent, evaluate_homepage

# Quick evaluation
result = evaluate_homepage("https://example.com")

# Full agent
agent = create_pmm_agent()
result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze https://example.com"}]
})

# Create positioning
result = create_positioning(
    product_description="AI-powered CRM for startups",
    target_audience="B2B SaaS founders",
    competitors=["Salesforce", "HubSpot"]
)
```

## Development

```bash
# Install dependencies
cd apps/agent && pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy src/pmm_agent

# Lint
ruff check src/pmm_agent
```

## Deployment

```bash
# Deploy to LangGraph Cloud
langgraph deploy
```

## Design Decisions

1. **Tool-based over graph-heavy** - Simple linear flows, complex tools
2. **Subagents for deep dives** - Specialist knowledge in subagents
3. **Human-in-the-loop for creation** - Approve positioning/messaging before delivery
4. **Structured outputs** - Pydantic models for all evaluations
5. **Anti-pattern focus** - Explicitly detect common mistakes
