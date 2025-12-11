# PMM Deep Agent - Implementation Plan

## Overview

Get PMM Deep Agent running using the existing `deepagents` library from `learning-agent/libs/deepagents`.

## Current State

✅ Created:
- Agent structure (`apps/agent/src/pmm_agent/`)
- 17 tools for PMM evaluation
- 6 specialist subagents
- Pydantic models for scoring
- System prompts with PMM expertise
- LangGraph deployment config
- `.env` file with API keys
- `pyproject.toml` pointing to local `deepagents`
- CLI entry point (`cli.py`)

❌ Remaining:
- Install dependencies and test
- Web fetching implementation (tools return prompts for LLM, actual HTTP handled by deepagents built-in tools)

## Implementation Steps

### Phase 1: Environment Setup (5 min)

1. **Create `.env` file**
```bash
cd /Users/jaybhagat/projects/pmm-deep-agent
```

2. **Copy deepagents library** (or symlink)
```bash
mkdir -p libs
cp -r ../learning-agent/libs/deepagents libs/
cp -r ../learning-agent/libs/deepagents-cli libs/  # optional, for CLI
```

3. **Update pyproject.toml** to use local deepagents

### Phase 2: Fix Tool Implementations (15 min)

Current tools return JSON prompts for LLM completion. Need to:
1. Add actual web fetching with `httpx` or `playwright`
2. Convert tool outputs to structured returns
3. Add `tavily-python` for web search if needed

### Phase 3: Test Agent (10 min)

1. Create simple test script
2. Run against a live homepage
3. Validate output structure

### Phase 4: Deploy to LangGraph Cloud (Optional)

1. Push to GitHub
2. Deploy via `langgraph deploy`

---

## Immediate Actions

### Step 1: Create .env

```bash
cat > .env << 'EOF'
# LangSmith observability
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT="PMM Deep Agent"

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
```

### Step 2: Copy deepagents lib

```bash
mkdir -p libs
cp -r ../learning-agent/libs/deepagents libs/
```

### Step 3: Update pyproject.toml

Change dependencies to use local path:
```toml
dependencies = [
    "deepagents @ file:///Users/jaybhagat/projects/pmm-deep-agent/libs/deepagents",
    # ... rest
]
```

### Step 4: Install and Test

```bash
cd apps/agent
pip install -e .
python -c "from pmm_agent import create_pmm_agent; print('✓ Import works')"
```

### Step 5: Create CLI Runner

```python
# apps/agent/src/pmm_agent/cli.py
from pmm_agent import create_pmm_agent

def main():
    agent = create_pmm_agent()
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Analyze https://chatprd.ai"}]
    })
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
```

---

## File Changes Needed

| File | Action |
|------|--------|
| `.env` | Create with API keys |
| `libs/deepagents/` | Copy from learning-agent |
| `apps/agent/pyproject.toml` | Update deps to local |
| `apps/agent/src/pmm_agent/cli.py` | Create CLI runner |
| `apps/agent/src/pmm_agent/tools/web.py` | Add actual HTTP fetching |

---

## Architecture Reference

```
pmm-deep-agent/
├── .env                         # API keys (CREATE)
├── CLAUDE.md                    # ✓ Done
├── PLAN.md                      # This file
├── langgraph.json               # ✓ Done
├── libs/
│   └── deepagents/              # Copy from learning-agent
└── apps/agent/
    ├── pyproject.toml           # Update deps
    └── src/pmm_agent/
        ├── __init__.py          # ✓ Done
        ├── agent.py             # ✓ Done
        ├── cli.py               # CREATE
        ├── prompts.py           # ✓ Done
        ├── models/              # ✓ Done
        ├── tools/               # ✓ Done (needs web fetch impl)
        └── subagents/           # ✓ Done
```

---

## Estimated Time

| Phase | Time |
|-------|------|
| Environment setup | 5 min |
| Fix tool implementations | 15 min |
| Test agent | 10 min |
| **Total** | **30 min** |

---

## Success Criteria

1. ✅ `python -c "from pmm_agent import create_pmm_agent"` works
2. ✅ Agent can analyze a live homepage URL
3. ✅ Returns structured PMM evaluation with scores
4. ✅ LangSmith traces visible in dashboard
