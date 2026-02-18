---
title: AI Text Comparison Dashboard
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.6.0
python_version: '3.10'
app_file: app.py
pinned: false
---
# 🤖 AI Text Comparison Dashboard

A professional LLM evaluation dashboard that compares text generation from multiple GPT-2 models with automatic quality scoring, sentiment analysis, and interactive charts.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Model Comparison** | Compare DistilGPT-2, GPT-2, GPT-2 Medium side-by-side |
| 📊 **Quality Metrics** | Diversity, readability, grade level, word count |
| 😊 **Sentiment Analysis** | AI-powered positive/negative detection |
| 📈 **Interactive Charts** | Bar charts, radar charts, trend lines |
| 💾 **Database Storage** | SQLite for persistent history |
| 📥 **CSV Export** | Download your data for analysis |
| ⏱️ **Response Timing** | Track generation speed per model |
| 🏆 **Best Model Recommendation** | Auto-picks highest quality output |

## 📁 Project Structure

```
LLM_EVALUATION_DASHBOARD/
│
├── app.py           # 🚀 Main entry point
├── config.py        # ⚙️ All settings
├── database.py      # 💾 Database operations
├── models.py        # 🤖 AI model loading
├── evaluation.py    # 📊 Text metrics + sentiment
├── charts.py        # 📈 Visualization charts
├── ui.py            # 🎨 Gradio interface
├── utils.py         # 🔧 Helper functions
│
├── requirements.txt # 📦 Dependencies
├── README.md        # 📖 This file
└── generations.db   # 💾 Database (auto-created)
```

## 🚀 Quick Start

### Local Installation

```bash
# 1. Clone or download the project
cd LLM_EVALUATION_DASHBOARD

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open browser to http://127.0.0.1:7860
```

## 🚀 Deploy to HuggingFace Spaces (FREE!)

### Step 1: Create HuggingFace Account
1. Go to [huggingface.co](https://huggingface.co)
2. Sign up for free account
3. Verify your email

### Step 2: Create New Space
1. Click your profile → "New Space"
2. Fill in:
   - **Space name:** `llm-comparison-dashboard`
   - **License:** MIT
   - **SDK:** Gradio
   - **Hardware:** CPU basic (free!)
3. Click "Create Space"

### Step 3: Upload Files
**Option A: Via Web Interface**
1. In your Space, click "Files" tab
2. Click "Upload files"
3. Upload ALL these files:
   - app.py
   - config.py
   - database.py
   - models.py
   - evaluation.py
   - charts.py
   - ui.py
   - utils.py
   - requirements.txt

**Option B: Via Git (Recommended)**
```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/llm-comparison-dashboard
cd llm-comparison-dashboard

# Copy all project files here

# Push to HuggingFace
git add .
git commit -m "Initial upload"
git push
```

### Step 4: Configure for HuggingFace
Create or update `config.py` with these changes:
```python
# Change these for HuggingFace deployment
SERVER_PORT = 7860  # HuggingFace uses this port
SHARE_APP = False   # Not needed on HuggingFace
ENABLE_PARALLEL = False  # Keep False for free tier
```

### Step 5: Wait for Build
- HuggingFace will automatically build your app
- Takes 5-10 minutes first time
- Watch the "Logs" tab for progress

### Step 6: Get Your Live URL! 🎉
Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/llm-comparison-dashboard
```

**Add this URL to your resume!** 💼

---

## 📊 Screenshots

### Generate Tab
- Enter prompts and compare 3 models
- See quality metrics instantly
- View sentiment analysis

### Charts Tab
- Interactive diversity comparison
- Response time visualization
- Historical trends

### History Tab
- Browse all past generations
- Export to CSV
- Filter by date

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Add more models
MODEL_LIST = {
    "DistilGPT-2 (Fast)": "distilgpt2",
    "GPT-2 (Standard)": "gpt2",
    "GPT-2 Medium (Better)": "gpt2-medium",
    # Add these for more options:
    # "GPT-Neo 125M": "EleutherAI/gpt-neo-125m",
}

# Enable/disable features
ENABLE_SENTIMENT = True   # Sentiment analysis
ENABLE_PARALLEL = False   # Parallel processing

# UI settings
SERVER_PORT = 7860
```

---

## 🔧 Troubleshooting

### "Out of Memory" on HuggingFace
- Reduce model count in `config.py`
- Disable sentiment: `ENABLE_SENTIMENT = False`

### Charts not showing
- Make sure `plotly` is installed
- Check browser console for errors

### Models loading slowly
- First load downloads models (~500MB)
- Subsequent loads use cache

---

## 📈 Future Improvements

- [ ] Add more models (GPT-Neo, BLOOM)
- [ ] User authentication
- [ ] API endpoint for programmatic access
- [ ] Docker container
- [ ] More evaluation metrics

---

## 🙏 Credits

- **Transformers** by HuggingFace
- **Gradio** for the web interface
- **Plotly** for visualizations
- **TextStat** for readability metrics

---

## 📄 License

MIT License - Feel free to use for your portfolio!

---

## 👩‍💻 Author

Built as a portfolio project demonstrating:
- ✅ Python modular architecture
- ✅ Machine Learning model deployment
- ✅ Database integration
- ✅ Data visualization
- ✅ Web application development
- ✅ NLP techniques (sentiment analysis)

**Perfect for ML Engineer interviews!** 💼