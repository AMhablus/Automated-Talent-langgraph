# CV Analysis Agent

An AI-powered CV analysis tool that evaluates resumes against job descriptions and provides intelligent screening recommendations via a Streamlit web app.

## 🚀 Features

- **Web UI (Streamlit)**: Upload a CV (PDF) and paste a job description
- **Prescreening**: Extracts entities and determines pass/fail based on basic requirements
- **Skills Analysis**: Matches, missing, and additional skills with an overall score (0–100)
- **Recommendations**: Final decision routed to Interview, Phone Screen, or Rejected
- **Download Results**: Export a concise text summary of the analysis

## 🛠️ Requirements

- Python 3.12+
- Dependencies from `requirements.txt` or `pyproject.toml` (managed via `pip` or `uv`)

## 📦 Installation

1) Clone the repository
```bash
git clone <repository-url>
cd "cv project"
```

2) Install dependencies (pick one)
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (optional)
uv pip install -r requirements.txt
```

3) Configure environment
```bash
# Create a .env file in the project root
GROQ_API_KEY=your_api_key_here
```


## 🎯 Usage

Run the Streamlit app from the project root:
```bash
streamlit run app.py
```

In the sidebar:
- Upload a CV PDF
- Paste the job description
- Click “Analyze CV”

The results view shows candidate info, prescreening status, a skills breakdown with score, the final decision, and (if rejected) a brief rejection reason. You can download a text summary.

## 🔍 How it works

- `src/agent/graph.py`: Builds a LangGraph state machine with nodes:
  - `prescreening_analysis` → extract fields and set `pre_screening_status`
  - `skills_analysis` → compute matched/missing/additional and `score`
  - terminal nodes: `interview`, `phone_screen`, `reject`
- `src/agent/nodes.py`: Implements node functions and routing rules:
  - Route 1: If `pre_screening_status` is Pass → `skills_analysis`; otherwise → `reject`
  - Route 2: If `score` > 80 → Interview; 50–80 → Phone Screen; < 50 → Rejected
  - `reject` also generates a short `rejection_reason`
- `src/agent/prompts.py`: System prompts for prescreening, skills analysis, and rejection text
- `src/agent/state.py`: TypedDict definitions for the shared state

## 📁 Project structure

```
cv project/
├── app.py                   # Streamlit web interface
├── requirements.txt         # Dependencies
├── pyproject.toml           # Alternative dependency manifest
├── src/
│   └── agent/
│       ├── graph.py         # LangGraph workflow
│       ├── nodes.py         # Core analysis and routing
│       ├── prompts.py       # LLM system prompts
│       ├── state.py         # Shared state schema
│       ├── examples.py      # Sample CV/JD text
│       └── test.ipynb       # Notebook playground
└── README.md
```

## ⚙️ Configuration

- Model/provider: `ChatGroq` with model `openai/gpt-oss-120b` (see `src/agent/nodes.py`)
- Environment: `GROQ_API_KEY` read from `.env` via `python-dotenv`
- PDF parsing: LangChain `PyPDFLoader` (backed by `pypdf`)

## 📊 Output details

- Candidate: `name`, `email`, `phone`, `years_of_experience`, `skills`
- Prescreening: `pre_screening_status` (Pass/Fail)
- Skills analysis: `matched`, `missing`, `additional`, `score` (0–100)
- Decision: `final_decision` (Interview, Phone Screen, Rejected)
- If rejected: short `rejection_reason`

## 🚨 Troubleshooting

- “Please upload a CV / provide a job description”: Both inputs are required before running
- PDF text extraction errors: Ensure the file is a valid, non-password-protected PDF
- API key errors: Confirm `.env` exists and `GROQ_API_KEY` is set

## 🧩 Notes

- This repository currently exposes only the Streamlit interface. There is no CLI or separate interactive terminal app.
- The `examples.py` file contains sample CV/JD text you can use for testing.
- The graph rendering in `src/agent/graph.py` uses IPython display when run in a notebook; it is safe when imported by the app.

## 📄 License

No license file is included in the repository.

---

Happy CV analyzing! 🎉


