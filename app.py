"""
🚀 Main Application Entry Point
Run this file to start the dashboard!

Usage:
    python app.py

Features:
    Multi-model text generation
    Quality metrics (diversity, readability, grade level)
    Sentiment analysis
    Interactive charts
    Database storage
    CSV export
    Per-model timing
"""

from config import SERVER_PORT, SHARE_APP, ENABLE_SENTIMENT
from database import init_database
from models import load_all_models
from evaluation import load_sentiment_analyzer
from ui import create_interface


def print_banner():
    """Print a nice startup banner"""
    print("\n")
    print("  AI Text Comparison Dashboard")
    print("  Enhanced with Sentiment Analysis & Charts")
    print()


def main():
    """
    Main function - starts the entire application

    Steps:
    1. Initialize database
    2. Load AI models
    3. Load sentiment analyzer (if enabled)
    4. Create and launch UI
    """
    print_banner()

    # Step 1: Initialize database
    print("Step 1: Initializing database...")
    init_database()

    # Step 2: Load AI models
    print("\nStep 2: Loading AI models...")
    load_all_models()

    # Step 3: Load sentiment analyzer
    if ENABLE_SENTIMENT:
        print("\nStep 3: Loading sentiment analyzer...")
        load_sentiment_analyzer()
    else:
        print("\nStep 3: Sentiment analysis disabled (skip)")

    # Step 4: Create and launch UI
    print("\nStep 4: Creating user interface...")
    demo = create_interface()

    print("\nAll systems ready!")
    print(f"Local URL: http://127.0.0.1:{SERVER_PORT}")
    if SHARE_APP:
        print("Public URL will be generated...")
    print()

    # Launch the app
    demo.launch(
        server_name="0.0.0.0",  # Required for HuggingFace
        server_port=7860,
        share=False,
    )


if __name__ == "__main__":
    main()
