# CV Analysis Agent

An AI-powered CV analysis tool that evaluates candidate resumes against job descriptions to provide intelligent screening recommendations.

## 🚀 Features

- **Dynamic Input Processing**: Upload any CV in PDF format and input custom job descriptions
- **Intelligent Analysis**: Uses advanced LLM models to extract candidate information and analyze skills
- **Comprehensive Evaluation**: Provides pre-screening status, skills matching, and final recommendations
- **Multiple Interfaces**: Choose between web UI, command-line, or interactive terminal
- **Detailed Results**: Get skills analysis, gap identification, and actionable insights

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cv-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file with your API keys
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 Usage

### Option 1: Web Interface (Recommended)

Launch the Streamlit web application for an intuitive user experience:

```bash
streamlit run app.py
```

**Features:**
- Drag-and-drop PDF upload
- Rich text input for job descriptions
- Visual results with progress bars and metrics
- Downloadable analysis reports
- Responsive design

### Option 2: Command Line Interface

Use the CLI for automation and scripting:

```bash
# Analyze CV with job description from command line
python cli.py --cv path/to/cv.pdf --jd "Software Engineer position requiring Python, ML, and 3+ years experience"

# Analyze CV with job description from file
python cli.py --cv path/to/cv.pdf --jd-file path/to/job_description.txt

# Save results to output file
python cli.py --cv path/to/cv.pdf --jd "Job description..." --output results.txt
```

### Option 3: Interactive Terminal

Run the interactive Python script:

```bash
python main.py
```

Follow the prompts to input CV file path and job description.

## 📊 What You Get

### Candidate Information Extraction
- Name, email, phone number
- Years of experience
- Technical skills and competencies

### Skills Analysis
- **Matched Skills**: Skills that align with job requirements
- **Missing Skills**: Skills you might need to develop
- **Additional Skills**: Extra skills that could be beneficial
- **Overall Score**: Numerical assessment (0-100)

### Final Recommendations
- **Interview**: High match (score > 80)
- **Phone Screen**: Moderate match (score 50-80)
- **Rejected**: Low match (score < 50)

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for LLM access

### Model Configuration
The agent uses Groq's LLM service by default. You can modify the model in `src/agent/nodes.py`:

```python
LLM = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=SecretStr(OPENAI_API_KEY))
```

## 📁 Project Structure

```
cv-project/
├── src/agent/
│   ├── nodes.py          # Core analysis functions
│   ├── state.py          # Data structures
│   ├── graph.py          # LangGraph workflow
│   ├── prompts.py        # LLM prompts
│   └── examples.py       # Sample data
├── app.py                # Streamlit web interface
├── cli.py                # Command-line interface
├── main.py               # Interactive terminal interface
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🎨 Customization

### Adding New Analysis Criteria
Modify the prompts in `src/agent/prompts.py` to include additional evaluation criteria.

### Extending the Workflow
Add new nodes to the graph in `src/agent/graph.py` for additional processing steps.

### Custom Output Formats
Modify the result formatting in any of the interface files to match your needs.

## 🚨 Troubleshooting

### Common Issues

1. **PDF Processing Errors**: Ensure the PDF is not password-protected and contains extractable text
2. **API Key Issues**: Verify your OpenAI API key is correctly set in the `.env` file
3. **Memory Issues**: Large PDFs may require more memory; consider splitting very long documents

### Error Messages
- `File not found`: Check the file path and ensure the PDF exists
- `Invalid PDF format`: Ensure the file is a valid PDF with extractable text
- `API rate limit`: Wait a moment and try again

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with LangGraph for workflow orchestration
- Powered by Groq's LLM services
- Uses Streamlit for the web interface
- PDF processing with PyPDF2

---

**Happy CV analyzing! 🎉**
