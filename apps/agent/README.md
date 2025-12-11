# PMM Deep Agent

Evaluate and create B2B product marketing assets using proven frameworks (April Dunford, Fletch PMM).

## Installation

```bash
pip install -e .
```

## Usage

```bash
pmm-agent
```

Or:

```python
from pmm_agent import create_pmm_agent

agent = create_pmm_agent()
result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze https://example.com"}]
})
print(result["messages"][-1].content)
```
