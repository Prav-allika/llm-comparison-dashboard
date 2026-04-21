---
title: AI Text Comparison Dashboard
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 4.8.0
app_file: app.py
pinned: false
python_version: "3.11"
---

# AI Text Comparison Dashboard

<div align="center">

[![Hugging Face Spaces](https://img.shields.io/badge/Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen)](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-FF7C00?logo=gradio&logoColor=white)](https://gradio.app)
[![Transformers](https://img.shields.io/badge/Transformers-Latest-yellow)](https://huggingface.co/transformers)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <strong>A dashboard for comparing text generation from multiple local language models with automatic quality evaluation, sentiment analysis, and interactive visualizations.</strong>
</p>

[Live Demo](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard) •
[Features](#features) •
[Installation](#installation) •
[Tech Stack](#tech-stack) •
[Screenshots](#screenshots)

</div>

---

## Live Demo

**Try the app now:** [**https://huggingface.co/spaces/Prav04/llm-comparison-dashboard**](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Features

<table>
<tr>
<td width="50%">

### Multi-Model Comparison
Compare outputs from 3 local language models simultaneously:
- **SmolLM3-3B** (HuggingFace 2026) — 3B parameters, strong quality on Apple Silicon
- **DeepSeek-R1-1.5B** (2025) — 1.5B parameters, reasoning focused
- **Qwen2.5-0.5B** (Alibaba 2025) — 0.5B parameters, fastest inference

</td>
<td width="50%">

### Automatic Quality Metrics
Real-time text evaluation per model:
- **Word Count** — Total words generated
- **Diversity Score** — Vocabulary richness percentage
- **Readability Score** — Flesch reading ease
- **Grade Level** — US education level required

</td>
</tr>
<tr>
<td width="50%">

### Sentiment Analysis
AI-powered emotion detection using DistilBERT:
- Fine-tuned on SST-2 dataset
- Classifies output as POSITIVE or NEGATIVE
- Shows confidence percentage per model
- Can be toggled on/off in config

</td>
<td width="50%">

### Interactive Charts
Plotly visualizations generated live and historically:
- Diversity comparison bar charts
- Metrics radar chart
- Response time comparison
- Historical trend line charts
- Model usage pie charts
- Sentiment distribution chart

</td>
</tr>
<tr>
<td width="50%">

### Database Storage
Persistent history with SQLite:
- Auto-saves every generation
- Track metrics over time
- Configurable history limit
- Export to CSV

</td>
<td width="50%">

### Performance Features
Optimized for local inference:
- GPU auto-detection (CUDA / MPS / CPU)
- Optional parallel processing (3 workers)
- Per-model response time tracking
- Model caching after first load

</td>
</tr>
</table>

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **ML Framework** | HuggingFace Transformers |
| **Web Interface** | Gradio 4.0+ |
| **Visualization** | Plotly |
| **Database** | SQLite |
| **Text Analysis** | TextStat |
| **Sentiment Model** | DistilBERT (SST-2) |
| **Deployment** | HuggingFace Spaces |

---

## Screenshots

<details>
<summary><b>Click to view screenshots</b></summary>

### Generate Tab
Compare text generation from all models with quality metrics and sentiment analysis.

![Generate Tab](screenshots/generate_tab.png)

### Charts & Analytics
View interactive charts showing diversity trends and model performance.

![Charts Tab](screenshots/charts_tab.png)

### History & Statistics
Browse past generations and view aggregate statistics.

![History Tab](screenshots/history_tab.png)

</details>

---

## Project Architecture

```
llm-comparison-dashboard/
│
├── app.py              # Application entry point
├── config.py           # Configuration settings and CSS
├── database.py         # SQLite database operations
├── evaluation.py       # Text quality metrics and sentiment analysis
├── models.py           # AI model loading and generation
├── charts.py           # Plotly visualization charts
├── ui.py               # Gradio interface components
├── utils.py            # Helper functions and formatting
│
├── requirements.txt    # Python dependencies
├── README.md           # Documentation (this file)
├── LICENSE             # MIT License
└── generations.db      # SQLite database (auto-created on first run)
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                               │
│                    (Prompt + Settings)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ui.py (Gradio)                            │
│                    Web Interface Layer                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      models.py                                   │
│     ┌─────────────┬──────────────────┬─────────────────┐        │
│     │  SmolLM3-3B │ DeepSeek-R1-1.5B │  Qwen2.5-0.5B  │        │
│     └─────────────┴──────────────────┴─────────────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  evaluation.py  │ │   database.py   │ │    charts.py    │
│  Quality Metrics│ │  SQLite Storage │ │  Visualizations │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- 8GB RAM recommended (models are 0.5B–3B parameters)
- Apple Silicon (MPS), NVIDIA GPU (CUDA), or CPU

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/Prav-allika/llm-comparison-dashboard.git
cd llm-comparison-dashboard

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py

# 6. Open in browser
# Navigate to http://127.0.0.1:7860
```

### Using Conda

```bash
# Create conda environment
conda create -n llm-dashboard python=3.10 -y
conda activate llm-dashboard

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

---

## Configuration

Edit **config.py** to customize the dashboard.

### Model Configuration

```python
MODEL_LIST = {
    "SmolLM3-3B (HuggingFace 2026)": "HuggingFaceTB/SmolLM3-3B",
    "DeepSeek-R1-1.5B (2025)": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    "Qwen2.5-0.5B (Alibaba 2025)": "Qwen/Qwen2.5-0.5B-Instruct",
    # Add additional HuggingFace models here
}
```

### Performance Settings

```python
# Device settings
DEVICE = "mps"        # auto, cuda, mps, or cpu

# Parallel processing (requires 8GB+ RAM)
ENABLE_PARALLEL = True   # Set False to run models sequentially
MAX_WORKERS = 3          # Number of parallel workers

# Feature toggles
ENABLE_SENTIMENT = True  # Disable for faster generation
```

### Generation Defaults

```python
DEFAULT_MAX_LENGTH = 100
DEFAULT_CREATIVITY = 0.7
MIN_LENGTH = 20
MAX_LENGTH = 300
MIN_CREATIVITY = 0.3
MAX_CREATIVITY = 1.0
```

---

## Usage

### Basic Usage

1. **Enter a prompt** in the text box or pick a Quick Template from the dropdown
2. **Adjust settings** using sliders:
   - Max Length: Controls output token length (20–300)
   - Creativity: Higher = more creative, lower = more focused (0.3–1.0)
3. **Click "Generate & Evaluate"**
4. **View results** — formatted cards with metrics, live charts, and sentiment scores

### Using Templates

The dropdown provides three built-in templates (Story, Email, Essay). Selecting one auto-fills the prompt; you can edit it before generating.

### Viewing History

Go to the **View History** tab to browse all past generations with their metrics. Use the record limit slider to control how many entries are shown, and click **Export to CSV** to download the full dataset.

### Statistics

The **Statistics** tab shows aggregate performance data per model — average diversity, readability, response time, and sentiment breakdown — loaded automatically on tab switch.

---

## API Reference

### Core Functions

| Function | File | Description |
|----------|------|-------------|
| `generate_from_all()` | models.py | Generate text from all loaded models |
| `generate_single()` | models.py | Generate from a specific model |
| `evaluate_text()` | evaluation.py | Calculate quality metrics |
| `analyze_sentiment()` | evaluation.py | Classify text sentiment |
| `save_generation()` | database.py | Store results in database |
| `get_statistics()` | database.py | Get aggregate statistics |
| `create_diversity_comparison_chart()` | charts.py | Diversity bar chart |
| `create_response_time_chart()` | charts.py | Response time bar chart |
| `create_metrics_radar_chart()` | charts.py | Metrics radar chart |
| `create_history_trend_chart()` | charts.py | Historical trend line chart |
| `create_model_usage_pie_chart()` | charts.py | Model usage pie chart |
| `create_sentiment_distribution_chart()` | charts.py | Sentiment distribution chart |

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | Input text to continue |
| `max_length` | int | Maximum tokens to generate (20–300) |
| `creativity` | float | Temperature for sampling (0.3–1.0) |

---

## Deployment

### Deploy to HuggingFace Spaces (Free)

1. **Create account** at [huggingface.co](https://huggingface.co)

2. **Create new Space**:
   - SDK: Gradio
   - Hardware: CPU basic (free) or T4 GPU for faster inference

3. **Upload files** via web interface or git

4. **Wait for build** (~5–10 minutes)

5. **Your app is live**

### Deploy to Other Platforms

<details>
<summary><b>Deploy to Render</b></summary>

```yaml
# render.yaml
services:
  - type: web
    name: llm-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
```
</details>

<details>
<summary><b>Deploy with Docker</b></summary>

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 7860
CMD ["python", "app.py"]
```
</details>

---

## Future Improvements

- [ ] Add more models (Mistral, Phi-3, LLaMA)
- [ ] User authentication system
- [ ] API endpoint for programmatic access
- [ ] Expanded prompt templates library
- [ ] Export reports as PDF
- [ ] A/B testing mode
- [ ] Multi-language support
- [ ] Dark/light theme toggle
- [ ] Mobile-responsive design

---

## Contributing

Contributions are welcome. Here is how to get started:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes (`git commit -m 'Add some feature'`)
4. **Push** to the branch (`git push origin feature/your-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/llm-comparison-dashboard.git

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
python app.py

# Commit and push
git add .
git commit -m "Description of changes"
git push origin feature/your-feature
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

<div align="center">

**Pravalli**

ML Engineer | NLP Enthusiast | Building AI Solutions

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/your-profile)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Profile-yellow?style=for-the-badge)](https://huggingface.co/Prav04)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/Prav-allika)

</div>

---

## Acknowledgments

- [HuggingFace](https://huggingface.co) for Transformers library and free hosting
- [Gradio](https://gradio.app) for the UI framework
- [Plotly](https://plotly.com) for interactive visualizations
- [TextStat](https://github.com/shivam5992/textstat) for readability metrics

---

<div align="center">

**Built for the ML community**

</div>
