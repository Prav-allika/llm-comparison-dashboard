"""
Configuration Settings
All app settings in one place - easy to change!
"""

# MODEL SETTINGS

# Original small models (fast, work on CPU)
MODEL_LIST = {
    "DistilGPT-2 (Fast)": "distilgpt2",
    "GPT-2 (Standard)": "gpt2",
    "GPT-2 Medium (Better)": "gpt2-medium",
}

# Additional free models
# These are larger and better quality but slower
ADDITIONAL_MODELS = {
    "GPT-2 Large": "gpt2-large",  # 774M params - needs ~3GB RAM
    "GPT-Neo 125M": "EleutherAI/gpt-neo-125m",  # Good alternative
    "DistilBERT": "distilbert-base-uncased",  # Fast BERT model
    "BLOOM 560M": "bigscience/bloom-560m",  # Multilingual model
}

# Merge additional models if you want more
MODEL_LIST.update(ADDITIONAL_MODELS)


# GENERATION DEFAULTS

DEFAULT_MAX_LENGTH = 100
DEFAULT_CREATIVITY = 0.8
MIN_LENGTH = 30
MAX_LENGTH = 200
MIN_CREATIVITY = 0.3
MAX_CREATIVITY = 1.0

# DATABASE SETTINGS
DATABASE_NAME = "generations.db"
HISTORY_DEFAULT_LIMIT = 20

# PERFORMANCE SETTINGS
# Enable parallel processing (faster but uses more memory)
ENABLE_PARALLEL = False  # Set to True if you have enough RAM (8GB+)
MAX_WORKERS = 3  # Number of parallel workers

# Device settings
# "auto" = automatically detect GPU/MPS/CPU
# "cuda" = Force NVIDIA GPU
# "mps" = Force Apple Silicon GPU
# "cpu" = Force CPU only
DEVICE = "cpu"

# SENTIMENT ANALYSIS SETTINGS
ENABLE_SENTIMENT = True  # Enable/disable sentiment analysis
SENTIMENT_MODEL = (
    "distilbert-base-uncased-finetuned-sst-2-english"  # pre-trained sentiment model
)

# UI SETTINGS
SERVER_PORT = 7860
APP_TITLE = "AI Text Comparison Dashboard"
SHARE_APP = False  # Set to True to create public link

# CSS Styling
CSS_STYLES = """
#output_text {
    font-size: 16px;
    line-height: 1.6;
    font-family: 'Georgia', serif;
}
.generate-btn {
    background: linear-gradient(45deg, #4CAF50, #45a049);
    border: none;
    font-size: 18px;
    font-weight: bold;
}
.chart-container {
    border-radius: 10px;
    padding: 10px;
}
"""

# Example prompts for the UI
EXAMPLE_PROMPTS = [
    ["Once upon a time in a distant galaxy", 120, 0.8],
    ["The future of artificial intelligence", 100, 0.7],
    ["In 2050, scientists discovered", 80, 0.9],
    ["Dear hiring manager, I am writing to apply", 100, 0.6],
    ["The best recipe for happiness includes", 90, 0.8],
]

# PROMPT TEMPLATES (NEW!)
PROMPT_TEMPLATES = {
    "Story": "Once upon a time in a magical land, there lived",
    "Email": "Dear [Name], I hope this email finds you well. I am writing to",
    "Code": "# Python function to calculate",
    "Essay": "The importance of artificial intelligence in modern society cannot be",
    "Product": "Introducing the revolutionary new product that will change how you",
    "News": "Breaking news: Scientists have announced a groundbreaking discovery in",
}
