"""
Text Evaluation Functions
All metrics for evaluating text quality
Now includes Sentiment Analysis!
"""

# calculate redability and grade level
from textstat import flesch_reading_ease, flesch_kincaid_grade

# load sentiment analysis model
from transformers import pipeline
import warnings

# Config settings for sentiment analysis
from config import ENABLE_SENTIMENT, SENTIMENT_MODEL

warnings.filterwarnings("ignore")

# Global sentiment analyzer (loaded once)
sentiment_analyzer = None


def load_sentiment_analyzer():
    """
    Load the sentiment analysis model
    Only loads once and reuses
    """
    # declare global variable to store the loaded model
    global sentiment_analyzer

    # load the model if not already loaded and if sentiment analysis is enabled
    if sentiment_analyzer is None and ENABLE_SENTIMENT:
        print("Loading sentiment analyzer...")
        try:
            # Load the sentiment analysis pipeline with the specified model
            sentiment_analyzer = pipeline(
                "sentiment-analysis",  # task type
                model=SENTIMENT_MODEL,  # from config.py
                device=-1,  # CPU, change to 0 for GPU
            )
            print("Sentiment analyzer loaded!")
        except Exception as e:
            print(f"Could not load sentiment analyzer: {e}")
            sentiment_analyzer = None

    return sentiment_analyzer


def evaluate_text(text):
    """
    Evaluate text quality with multiple metrics

    Parameters:
    - text: The generated text to evaluate

    Returns:
    - Dictionary with all metrics
    """
    # Split text into words
    words = text.split()

    # Calculate all metrics
    metrics = {
        # How many words total
        "word_count": len(words),
        # How many unique/different words
        "unique_words": len(set(words)),
        # Diversity = (Unique Words ÷ Total Words) × 100
        "diversity": round(len(set(words)) / len(words) * 100, 1)
        if len(words) > 0
        else 0,
        # flesch_reading_ease | How easy to read | Higher = Easier (0-100)
        "readability_score": round(flesch_reading_ease(text), 1),
        # `flesch_kincaid_grade` | US grade level needed | 8.0 = 8th grade
        "grade_level": round(flesch_kincaid_grade(text), 1),
    }

    return metrics


def analyze_sentiment(text):
    """
    Analyze the sentiment of generated text

    Parameters:
    - text: The text to analyze

    Returns:
    - Dictionary with label (POSITIVE/NEGATIVE) and score (0-1)
    """
    analyzer = load_sentiment_analyzer()

    if analyzer is None:
        return {"label": "UNKNOWN", "score": 0.0}

    try:
        # Truncate text if too long (model limit is 512 tokens)
        truncated_text = text[:500] if len(text) > 500 else text
        # HuggingFace sentiment pipelines always return a dict with exactly these two keys - label and score

        result = analyzer(truncated_text)[0]
        return {
            # Label is usually "POSITIVE" or "NEGATIVE"
            "label": result["label"],
            # Score is confidence level (0-1), round to 4 decimals for display
            "score": round(result["score"], 4),
        }
    except Exception as e:
        print(f" Sentiment analysis error: {e}")
        return {"label": "ERROR", "score": 0.0}


def get_best_model(results):
    """
    Pick the best model based on diversity score

    Parameters:
    - results: Dictionary with all model results

    Returns:
    - Tuple of (best_model_name, best_diversity_score)
    """
    best_model = None
    best_diversity = 0

    for name, data in results.items():
        # Skip non-model entries
        if name in ["Generation Stats", "Recommendation"]:
            continue

        # Only consider successful generations
        if data.get("status") == "Successfully generated":
            diversity = data["metrics"]["diversity"]
            if diversity > best_diversity:
                best_diversity = diversity
                best_model = name

    return best_model, best_diversity


def format_metrics_display(metrics, sentiment=None):
    """
    Format metrics for nice display

    Parameters:
    - metrics: Dictionary with all metrics
    - sentiment: Optional sentiment result

    Returns:
    - Formatted string
    """
    output = " **Quality Metrics:**\n"
    output += f"  • Word Count: {metrics['word_count']}\n"
    output += f"  • Unique Words: {metrics['unique_words']}\n"
    output += f"  • Diversity: {metrics['diversity']}%\n"
    output += f"  • Readability Score: {metrics['readability_score']}\n"
    output += f"  • Grade Level: {metrics['grade_level']}\n"

    if sentiment and sentiment.get("label") not in ["UNKNOWN", "ERROR"]:
        emoji = "😊" if sentiment["label"] == "POSITIVE" else "😟"
        output += f"\n{emoji} **Sentiment:** {sentiment['label']} ({sentiment['score'] * 100:.1f}% confidence)\n"

    return output


def get_readability_interpretation(score):
    """
    Convert readability score to human-readable interpretation

    Parameters:
    - score: Flesch reading ease score

    Returns:
    - String interpretation
    """
    if score >= 90:
        return "Very Easy (5th grade)"
    elif score >= 80:
        return "Easy (6th grade)"
    elif score >= 70:
        return "Fairly Easy (7th grade)"
    elif score >= 60:
        return "Standard (8th-9th grade)"
    elif score >= 50:
        return "Fairly Difficult (10th-12th grade)"
    elif score >= 30:
        return "Difficult (College)"
    else:
        return "Very Difficult (College graduate)"
