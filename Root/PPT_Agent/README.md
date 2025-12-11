# Agentic PPT Generator

A multi-agent AI system that generates professional PowerPoint presentations from simple text prompts.

## Features

- **Agentic Planning**: Automatically creates structured slide outlines
- **Self-Correcting Content**: Review loop ensures quality
- **Dynamic Styling**: Theme selection based on content keywords
- **Image Generation**: DALL-E 3 integration (optional)
- **Chart Generation**: AI-powered data visualization with matplotlib
- **Business Frameworks**: 21 consulting frameworks
  - Strategy: SWOT, Porter's 5 Forces, BCG Matrix, GE Matrix, Ansoff Matrix, 3C Analysis
  - Business Model: 4P Marketing, Business Model Canvas, McKinsey 7S, Lean Canvas
  - Process: Workflow, Value Chain
  - Planning: Scenario Planning, Eisenhower Matrix, Stakeholder Mapping, Impact/Effort Matrix
  - Project Management: Gantt Chart
  - Quality & Analysis: Fishbone Diagram, Org Chart, RACI Matrix, Decision Tree

## Architecture

```
User Input → Planner → Content Writer → Reviewer → Designer → PPTX Service
                ↑                           ↓
                └───────── Refinement ──────┘
```

### Agents
- **Planner**: Creates presentation outline using Gemini
- **Content Writer**: Generates detailed slide content
- **Reviewer**: Critiques and requests improvements
- **Designer**: Selects layouts, colors, and fonts

## Setup

1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

2. Configure API keys in `.env`:
```
GOOGLE_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional, for image generation
```

## Usage

```bash
python main.py "Your Presentation Topic"
```

Example:
```bash
python main.py "The Future of AI in Healthcare"
```

Output: `output/the_future_of_ai_in_healthcare.pptx`

## Project Structure

```
PPT_Agent/
├── src/
│   ├── agents/          # AI agents
│   │   ├── planner.py
│   │   ├── content_writer.py
│   │   ├── designer.py
│   │   ├── reviewer.py
│   │   └── orchestrator.py
│   ├── services/        # Core services
│   │   ├── pptx_service.py
│   │   └── image_service.py
│   └── models/          # Data schemas
│       └── schema.py
├── main.py              # Entry point
└── output/              # Generated presentations
```

## Next Steps

- Add web search for fact-checking
- Implement chart/graph generation
- Support custom templates
- Add multi-language support
