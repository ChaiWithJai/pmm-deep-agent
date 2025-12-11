# PMM Deep Agent Architecture

## Overview

PMM Deep Agent is a LangGraph-powered AI agent for evaluating and creating B2B product marketing assets. It uses proven PMM frameworks from April Dunford (positioning) and Fletch PMM (messaging hierarchy).

## System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        PMM Deep Agent                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Web UI    │    │  LangGraph  │    │  LangSmith  │         │
│  │  (React)    │───▶│   Server    │───▶│  (Tracing)  │         │
│  │  Port 5173  │    │  Port 2024  │    │             │         │
│  └─────────────┘    └──────┬──────┘    └─────────────┘         │
│                            │                                    │
│                     ┌──────▼──────┐                            │
│                     │  PMM Agent  │                            │
│                     │   (Core)    │                            │
│                     └──────┬──────┘                            │
│                            │                                    │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                  │
│  ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐          │
│  │ Evaluation  │   │    Web      │   │  Creation   │          │
│  │   Tools     │   │   Tools     │   │   Tools     │          │
│  └─────────────┘   └─────────────┘   └─────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
pmm-deep-agent/
├── apps/
│   ├── agent/                    # Python LangGraph agent
│   │   ├── src/pmm_agent/
│   │   │   ├── agent.py          # Main agent factory
│   │   │   ├── prompts.py        # System prompts
│   │   │   ├── tools/            # PMM evaluation tools
│   │   │   │   ├── evaluation.py # 5-second test, positioning, etc.
│   │   │   │   ├── web.py        # Homepage fetching
│   │   │   │   └── creation.py   # Asset creation tools
│   │   │   └── subagents/        # Specialist subagents
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── web/                      # React frontend
│       ├── src/
│       │   ├── App.tsx           # Main chat interface
│       │   └── index.css         # PIE-inspired styling
│       ├── package.json
│       └── vite.config.ts
├── libs/
│   └── deepagents/               # LangChain Deep Agents framework
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   ├── CONTEXT.md
│   └── incidents/                # Incident reports
├── langgraph.json                # LangGraph configuration
└── .env                          # Environment variables
```

## Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Agent Framework | LangGraph + Deep Agents | Agent orchestration |
| LLM | Claude Sonnet 4 | PMM analysis |
| Frontend | React 19 + Vite | Chat interface |
| Styling | Tailwind CSS v4 | PIE-inspired design |
| Streaming | LangGraph SDK | Real-time responses |
| Tracing | LangSmith | Observability |

## Tool Categories

### Evaluation Tools
- `run_five_second_test` - Test homepage clarity
- `analyze_positioning` - April Dunford framework
- `analyze_messaging` - Fletch PMM hierarchy
- `analyze_homepage_structure` - Layout analysis
- `detect_anti_patterns` - Common PMM mistakes
- `analyze_icp` - Ideal Customer Profile analysis
- `run_complete_pmm_audit` - Full evaluation

### Web Tools
- `fetch_homepage` - Scrape homepage content
- `fetch_competitor_homepage` - Competitor analysis
- `analyze_landing_page` - Landing page evaluation
- `scrape_social_proof` - Extract testimonials

### Creation Tools
- `create_positioning_canvas` - Generate positioning
- `create_messaging_framework` - Build messaging hierarchy
- `create_homepage_wireframe` - Design recommendations
- `generate_differentiation_statements` - "Unlike X, we Y"

## Human-in-the-Loop

Creation tools have `interrupt_on` enabled to require human approval:
- Positioning canvas review
- Messaging framework review
- Homepage wireframe review

## Configuration

Environment variables:
```bash
ANTHROPIC_API_KEY=your_key
LANGCHAIN_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=PMM Deep Agent
```
