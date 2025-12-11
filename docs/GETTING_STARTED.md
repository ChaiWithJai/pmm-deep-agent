# Getting Started with PMM Deep Agent

## Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key
- LangSmith API key (optional, for tracing)

## Quick Start

### 1. Clone and Setup

```bash
cd pmm-deep-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install agent
pip install -e ./apps/agent
```

### 2. Configure Environment

Create `.env` file in project root:

```bash
ANTHROPIC_API_KEY=sk-ant-...
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=PMM Deep Agent
```

### 3. Start LangGraph Server

```bash
source .venv/bin/activate
langgraph dev
```

Server starts at http://localhost:2024

### 4. Start Web UI

```bash
cd apps/web
npm install
npm run dev
```

UI available at http://localhost:5173

## Usage

### Via Web UI

1. Open http://localhost:5173
2. Click a quick action or type your request
3. Example: "Run a 5-second test on https://chatprd.ai"

### Via Python

```python
from pmm_agent import create_pmm_agent

agent = create_pmm_agent()
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Analyze the homepage at https://example.com"
    }]
})
print(result["messages"][-1].content)
```

### Via CLI

```bash
pmm-agent
```

## Quick Functions

```python
from pmm_agent import evaluate_homepage, create_positioning, compare_competitors

# Evaluate a homepage
result = evaluate_homepage("https://example.com")

# Create positioning
result = create_positioning(
    product_description="AI-powered sales assistant",
    target_audience="B2B SaaS sales teams",
    competitors=["Gong", "Chorus", "Clari"]
)

# Compare against competitors
result = compare_competitors(
    your_url="https://myproduct.com",
    competitor_urls=["https://competitor1.com", "https://competitor2.com"]
)
```

## LangGraph Studio

For visual debugging, open LangGraph Studio:

https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

Ensure `.env` file is in project root and contains valid key.

### "Failed to connect to PMM Agent"

Start LangGraph server first: `langgraph dev`

### Import errors

Make sure you're in the virtual environment: `source .venv/bin/activate`
