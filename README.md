# 🤖 AI Text Comparison Dashboard

<div align="center">

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)
[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Available-brightgreen)](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-FF7C00?logo=gradio&logoColor=white)](https://gradio.app)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-Latest-yellow)](https://huggingface.co/transformers)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <strong>A comprehensive dashboard for comparing text generation from multiple GPT-2 models with automatic quality evaluation, sentiment analysis, and interactive visualizations.</strong>
</p>

[Live Demo](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard) •
[Features](#-features) •
[Installation](#-installation) •
[Tech Stack](#-tech-stack) •
[Screenshots](#-screenshots)

</div>

---

## 🌟 Live Demo

**Try the app now:** [**https://huggingface.co/spaces/Prav04/llm-comparison-dashboard**](https://huggingface.co/spaces/Prav04/llm-comparison-dashboard)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 Multi-Model Comparison
Compare outputs from 3 GPT-2 variants simultaneously:
- **DistilGPT-2** (82M params) - Fastest
- **GPT-2 Standard** (124M params) - Balanced
- **GPT-2 Medium** (355M params) - Best quality

</td>
<td width="50%">

### 📊 Automatic Quality Metrics
Real-time text evaluation:
- **Word Count** - Total words generated
- **Diversity Score** - Vocabulary richness percentage
- **Readability Score** - Flesch reading ease
- **Grade Level** - US education level required

</td>
</tr>
<tr>
<td width="50%">

### 😊 Sentiment Analysis
AI-powered emotion detection:
- Uses DistilBERT fine-tuned model
- Classifies as POSITIVE/NEGATIVE
- Shows confidence percentage
- Visual emoji indicators

</td>
<td width="50%">

### 📈 Interactive Charts
Beautiful Plotly visualizations:
- Diversity comparison bar charts
- Response time comparison
- Historical trend line charts
- Model usage pie charts

</td>
</tr>
<tr>
<td width="50%">

### 💾 Database Storage
Persistent history with SQLite:
- Auto-saves all generations
- Track metrics over time
- Filter and search history
- Export to CSV

</td>
<td width="50%">

### ⚡ Performance Features
Optimized for speed:
- GPU auto-detection (CUDA/MPS/CPU)
- Optional parallel processing
- Response time tracking
- Model caching

</td>
</tr>
</table>

---

## 🛠 Tech Stack

<table>
<tr>
<td align="center" width="96">
<img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" />
<br>Python
</td>
<td align="center" width="96">
<img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" width="48" height="48" alt="HuggingFace" />
<br>Transformers
</td>
<td align="center" width="96">
<img src="https://www.gradio.app/assets/gradio.svg" width="48" height="48" alt="Gradio" />
<br>Gradio
</td>
<td align="center" width="96">
<img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" width="48" height="48" alt="Plotly" />
<br>Plotly
</td>
<td align="center" width="96">
<img src="https://www.sqlite.org/images/sqlite370_banner.gif" width="48" height="48" alt="SQLite" />
<br>SQLite
</td>
</tr>
</table>

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **ML Framework** | HuggingFace Transformers |
| **Web Interface** | Gradio 4.0+ |
| **Visualization** | Plotly |
| **Database** | SQLite |
| **Text Analysis** | TextStat |
| **Deployment** | HuggingFace Spaces |

---

## 📸 Screenshots

<details>
<summary><b>🖼️ Click to view screenshots</b></summary>

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

## 📁 Project Architecture

```
llm-comparison-dashboard/
│
├── 🚀 app.py              # Application entry point
├── ⚙️ config.py           # Configuration settings
├── 💾 database.py         # SQLite database operations
├── 📊 evaluation.py       # Text quality metrics & sentiment
├── 🤖 models.py           # AI model loading & generation
├── 📈 charts.py           # Plotly visualization charts
├── 🎨 ui.py               # Gradio interface components
├── 🔧 utils.py            # Helper functions & formatting
│
├── 📦 requirements.txt    # Python dependencies
├── 📖 README.md           # Documentation (this file)
├── 📄 LICENSE             # MIT License
└── 🗄️ generations.db      # SQLite database (auto-created)
```

### Data Flow Architecture

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
│          ┌─────────────┬─────────────┬─────────────┐            │
│          │ DistilGPT-2 │   GPT-2     │ GPT-2 Medium│            │
│          └─────────────┴─────────────┴─────────────┘            │
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

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- 8GB RAM recommended
- (Optional) NVIDIA GPU or Apple Silicon for faster inference

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

## ⚙️ Configuration

Edit `config.py` to customize the dashboard:

### Model Configuration

```python
# Available models - add or remove as needed
MODEL_LIST = {
    "DistilGPT-2 (Fast)": "distilgpt2",
    "GPT-2 (Standard)": "gpt2",
    "GPT-2 Medium (Better)": "gpt2-medium",
    # Uncomment to add more models:
    # "GPT-2 Large": "gpt2-large",
    # "GPT-Neo 125M": "EleutherAI/gpt-neo-125m",
}
```

### Performance Settings

```python
# Device settings
DEVICE = "auto"           # auto, cuda, mps, or cpu

# Parallel processing (requires 8GB+ RAM)
ENABLE_PARALLEL = False   # Set True for faster generation
MAX_WORKERS = 3           # Number of parallel workers

# Feature toggles
ENABLE_SENTIMENT = True   # Enable/disable sentiment analysis
```

### Generation Defaults

```python
DEFAULT_MAX_LENGTH = 100
DEFAULT_CREATIVITY = 0.8
MIN_LENGTH = 30
MAX_LENGTH = 200
MIN_CREATIVITY = 0.3
MAX_CREATIVITY = 1.0
```

---

## 📖 Usage

### Basic Usage

1. **Enter a prompt** in the text box
2. **Adjust settings** using sliders:
   - Max Length: Controls output length
   - Creativity: Higher = more creative, lower = more focused
3. **Click "Generate & Evaluate"**
4. **View results** with metrics and charts

### Using Templates

1. Select a template from the dropdown
2. The prompt will auto-fill
3. Modify if needed
4. Generate!

### Viewing History

1. Go to "View History" tab
2. See all past generations with metrics
3. Export to CSV for analysis

---

## 📚 API Reference

### Core Functions

| Function | File | Description |
|----------|------|-------------|
| `generate_from_all()` | models.py | Generate text from all loaded models |
| `generate_single()` | models.py | Generate from a specific model |
| `evaluate_text()` | evaluation.py | Calculate quality metrics |
| `analyze_sentiment()` | evaluation.py | Classify text sentiment |
| `save_generation()` | database.py | Store results in database |
| `get_statistics()` | database.py | Get aggregate statistics |
| `create_diversity_comparison_chart()` | charts.py | Create bar chart |
| `create_history_trend_chart()` | charts.py | Create trend line chart |

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | Input text to continue |
| `max_length` | int | Maximum tokens to generate |
| `creativity` | float | Temperature (0.3-1.0) |

---

## 🌐 Deployment

### Deploy to HuggingFace Spaces (Free)

1. **Create account** at [huggingface.co](https://huggingface.co)

2. **Create new Space**:
   - SDK: Gradio
   - Hardware: CPU basic (free)

3. **Upload files** via web interface or git

4. **Wait for build** (~5-10 minutes)

5. **Your app is live!** 🎉

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

## 🔮 Future Improvements

- [ ] Add more models (GPT-Neo, BLOOM, LLaMA)
- [ ] User authentication system
- [ ] API endpoint for programmatic access
- [ ] Prompt templates library
- [ ] Export reports as PDF
- [ ] Model fine-tuning interface
- [ ] A/B testing mode
- [ ] Multi-language support
- [ ] Dark/Light theme toggle
- [ ] Mobile-responsive design

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

<div align="center">

**Pravalli**

ML Engineer | NLP Enthusiast | Building AI Solutions

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/your-profile)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Profile-yellow?style=for-the-badge)](https://huggingface.co/Prav04)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/Prav-allika)

</div>

---

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co) for Transformers library and free hosting
- [Gradio](https://gradio.app) for the amazing UI framework
- [Plotly](https://plotly.com) for interactive visualizations
- [TextStat](https://github.com/shivam5992/textstat) for readability metrics

---

<div align="center">

### ⭐ If you found this project useful, please give it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=Prav-allika/llm-comparison-dashboard&type=Date)](https://star-history.com/#Prav-allika/llm-comparison-dashboard&Date)

**Built with ❤️ for the ML community**

</div>