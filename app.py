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
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "🤖 AI Text Comparison Dashboard".center(58) + "║")
    print("║" + "Enhanced with Sentiment Analysis & Charts".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
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
    print("📁 Step 1: Initializing database...")
    init_database()

    # Step 2: Load AI models
    print("\n🤖 Step 2: Loading AI models...")
    load_all_models()

    # Step 3: Load sentiment analyzer
    if ENABLE_SENTIMENT:
        print("\n Step 3: Loading sentiment analyzer...")
        load_sentiment_analyzer()
    else:
        print("\n⏭ Step 3: Sentiment analysis disabled (skip)")

    # Step 4: Create and launch UI
    print("\n Step 4: Creating user interface...")
    demo = create_interface()

    print("\n" + "=" * 60)
    print(" All systems ready!")
    print(f"🌐 Local URL:  http://127.0.0.1:{SERVER_PORT}")
    if SHARE_APP:
        print("🌍 Public URL will be generated...")
    print("=" * 60 + "\n")

    # Launch the app
    demo.launch(
    server_name="0.0.0.0",
    server_port=7860
)



if __name__ == "__main__":
    main()
