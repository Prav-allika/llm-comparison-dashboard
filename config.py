"""
Configuration Settings
All app settings in one place - easy to change!
"""

# MODEL SETTINGS

# Original small models (fast, work on CPU)
MODEL_LIST = {
    # 3B — good quality, fast on M4
    "SmolLM3-3B (HuggingFace 2026)": "HuggingFaceTB/SmolLM3-3B",
    # 1.5B — fast, reasoning focused
    "DeepSeek-R1-1.5B (2025)": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    # 0.5B — tiny, almost instant
    "Qwen2.5-0.5B (Alibaba 2025)": "Qwen/Qwen2.5-0.5B-Instruct",
}

# GENERATION DEFAULTS

DEFAULT_MAX_LENGTH = 100
DEFAULT_CREATIVITY = 0.7
MIN_LENGTH = 40
MAX_LENGTH = 300
MIN_LENGTH = 20
MIN_CREATIVITY = 0.3  # minimum temperature allowed
MAX_CREATIVITY = 1.0  # maximum temperature allowed

# DATABASE SETTINGS
DATABASE_NAME = "generations.db"
HISTORY_DEFAULT_LIMIT = 20

# PERFORMANCE SETTINGS
# Enable parallel processing (faster but uses more memory)
ENABLE_PARALLEL = True  # Set to True if you have enough RAM (8GB+)
MAX_WORKERS = 3  # Number of parallel workers

# Device settings
# "auto" = automatically detect GPU/MPS/CPU
# "cuda" = Force NVIDIA GPU
# "mps" = Force Apple Silicon GPU
# "cpu" = Force CPU only
DEVICE = "mps"

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
/* ── General text ── */
body, .gradio-container, p, span, div, label {
    color: #1A1A1A;
}

/* ── Textbox / textarea ── */
textarea, input[type="text"] {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1px solid #E8DDD8 !important;
}
textarea::placeholder, input[type="text"]::placeholder {
    color: #AAAAAA !important;
}

/* ── Number inputs next to sliders ── */
input[type="number"] {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
    border: 1px solid #E8DDD8 !important;
}

/* ── Dropdown trigger ── */
.wrap-inner, .multiselect, input.svelte-p3y7hu {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
}

/* ── Dropdown popup list ── */
ul.options, .options, .dropdown-arrow + div {
    background: #FFFFFF !important;
    border: 1px solid #E8DDD8 !important;
}
ul.options li, .options li {
    background: #FFFFFF !important;
    color: #1A1A1A !important;
}
ul.options li:hover, .options li:hover, ul.options li.selected {
    background: #FDECEA !important;
    color: #E85555 !important;
}

/* ── Tab buttons — kill ALL black states including Svelte internals ── */
button[role="tab"],
button[role="tab"]:link,
button[role="tab"]:visited,
button[role="tab"]:hover,
button[role="tab"]:focus,
button[role="tab"]:focus-visible,
button[role="tab"]:focus-within,
button[role="tab"]:active,
button[role="tab"]:checked,
button[role="tab"][aria-selected="true"],
.tab-nav button,
.tab-nav button:hover,
.tab-nav button:focus,
.tab-nav button:focus-visible,
.tab-nav button:active,
.tab-nav button.selected {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    border: none !important;
    color: #666666 !important;
}
/* ── Hover — soft coral tint instead of black ── */
button[role="tab"]:hover,
.tab-nav button:hover {
    background: #FDECEA !important;
    background-color: #FDECEA !important;
    color: #E85555 !important;
    border-radius: 6px !important;
}
/* ── Selected / active tab ── */
button[role="tab"][aria-selected="true"],
.tab-nav button.selected {
    background: transparent !important;
    background-color: transparent !important;
    color: #E85555 !important;
    border-bottom: 2px solid #E85555 !important;
    font-weight: 600 !important;
    border-radius: 0 !important;
}

/* ── Quick Templates dropdown — visible border box ── */
.block:has(select), .gr-dropdown, [data-testid="dropdown"] {
    border: 1px solid #E8DDD8 !important;
    border-radius: 8px !important;
}
.wrap-inner {
    border: 1px solid #E8DDD8 !important;
    border-radius: 6px !important;
    background: #FFFFFF !important;
    padding: 4px 8px !important;
}

/* ── Generate button ── */
.generate-btn {
    background: linear-gradient(45deg, #E85555, #F0A490) !important;
    border: none !important;
    font-size: 18px;
    font-weight: bold;
    color: #fff !important;
}

/* ── Examples table ── */
.examples table th {
    background: #FDECEA !important;
    color: #C03030 !important;
    font-weight: 600;
}
.examples table td {
    background: #FFF8F5 !important;
    color: #1A1A1A !important;
}
.examples table tr:hover td {
    background: #FDF0EC !important;
}

/* ── Block / panel labels ── */
.block label > span, span.svelte-1gfkn6j {
    color: #C03030 !important;
}

/* ── Markdown text ── */
.prose, .prose p, .prose li, .prose h1, .prose h2, .prose h3, .prose h4 {
    color: #1A1A1A !important;
}

/* ── Inline code (e.g. `config.py`) — light coral on warm background ── */
code, .prose code, p code,
.gradio-container code,
.svelte-1gfkn6j code,
.prose :not(pre) > code,
.gradio-container :not(pre) > code,
div.prose code, div p code {
    background: #FDECEA !important;
    color: #C03030 !important;
    border: 1px solid #F0C8BC !important;
    border-radius: 4px !important;
    padding: 1px 6px !important;
    font-size: 0.9em !important;
}

/* ── Chart containers ── */
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
    "Essay": "The importance of artificial intelligence in modern society cannot be",
}
