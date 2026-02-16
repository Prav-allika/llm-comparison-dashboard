"""
🔧 Utility Functions
Helper functions for formatting, export, and display
"""

# read/write csv files
import csv

# in memory file operations
import io

# datetime for timestamp formatting
from datetime import datetime

# export data from database for CSV export
from database import get_export_data


def format_output(
    results,
):  # formatting output for display in Gradio, enhanced with sentiment and timing display
    """
    Format generation results for display in Gradio
    Enhanced with sentiment and timing display!
    """
    output_text = ""

    # Loop through each model's results
    for model_name, data in results.items():
        if model_name in ["Generation Stats", "Recommendation"]:
            continue

        # Add header for this model
        output_text += f"\n{'=' * 60}\n"
        output_text += f"🤖 **{model_name}**\n"

        # Add timing badge if available
        if "generation_time" in data:  # Add timing badge if available
            output_text += f"⏱️ Generated in {data['generation_time']}s\n"

        output_text += f"{'=' * 60}\n\n"

        if data.get("status") == "Successfully generated":
            output_text += f"{data['response']}\n\n"  # Add the generated response

            # Add metrics
            metrics = data["metrics"]
            output_text += f"📊 **Quality Metrics:**\n"
            output_text += f"  • Word Count: {metrics['word_count']}\n"
            output_text += f"  • Unique Words: {metrics['unique_words']}\n"
            output_text += f"  • Diversity: {metrics['diversity']}%\n"
            output_text += f"  • Readability Score: {metrics['readability_score']}\n"
            output_text += f"  • Grade Level: {metrics['grade_level']}\n"

            # Add sentiment if available
            if data.get("sentiment") and data["sentiment"].get("label") not in [
                "UNKNOWN",
                "ERROR",
                None,
            ]:
                sentiment = data[
                    "sentiment"
                ]  # Add sentiment analysis results with emoji
                emoji = "😊" if sentiment["label"] == "POSITIVE" else "😟"
                output_text += f"\n{emoji} **Sentiment:** {sentiment['label']} "
                output_text += f"({sentiment['score'] * 100:.1f}% confidence)\n"
        else:
            output_text += f"❌ Error: {data['response']}\n"

    # Add generation stats
    if "Generation Stats" in results:
        stats = results["Generation Stats"]
        output_text += f"\n{'=' * 60}\n"
        output_text += f"⏱️ **Total Time:** {stats['elapsed_time']}\n"
        output_text += f"📊 **Avg per Model:** {stats['average_time_per_model']}\n"
        output_text += f"⚡ **Mode:** {stats.get('mode', 'Sequential')}\n"
        output_text += f"{'=' * 60}\n"

    # Add recommendation
    if "Recommendation" in results:
        rec = results["Recommendation"]
        output_text += f"\n{'=' * 60}\n"
        output_text += f"🏆 **Best Quality:** {rec['best_model']}\n"
        output_text += f"   📝 Reason: {rec['reason']}\n"
        if rec.get("fastest_model"):
            output_text += (
                f"\n⚡ **Fastest:** {rec['fastest_model']} ({rec['fastest_time']})\n"
            )
        output_text += f"{'=' * 60}\n"

    return output_text


def format_history(
    rows,
):  # formatting database history for display, enhanced with sentiment and timing information
    """
    Format database history for display
    Enhanced with sentiment and timing!
    """
    if not rows:
        return "📭 No generations yet! Try generating some text first. 🚀"

    output = "📜 **Generation History**\n"
    output += "=" * 60 + "\n\n"

    for row in rows:
        # Unpack row (now includes sentiment and timing)
        if len(row) >= 11:
            (
                timestamp,
                prompt,
                model,
                response,
                temp,
                max_len,
                words,
                diversity,
                sentiment_label,
                sentiment_score,
                response_time,
            ) = row
        else:
            # Handle old format without sentiment/timing
            timestamp, prompt, model, response, temp, max_len, words, diversity = row[
                :8  # Only unpack the first 8 values, ignore sentiment and timing if not present
            ]
            sentiment_label, sentiment_score, response_time = None, None, None

        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = timestamp

        output += f"🕐 **{formatted_time}**\n"
        output += f"📝 Prompt: {prompt[:50]}{'...' if len(prompt) > 50 else ''}\n"
        output += f"🤖 Model: {model}\n"
        output += f"🎨 Creativity: {temp} | 📏 Max Length: {max_len}\n"
        output += f"📊 Words: {words} | Diversity: {diversity}%\n"

        # Add timing if available
        if response_time:
            output += f"⏱️ Response Time: {response_time:.2f}s\n"

        # Add sentiment if available
        if sentiment_label and sentiment_label not in ["UNKNOWN", "ERROR"]:
            emoji = "😊" if sentiment_label == "POSITIVE" else "😟"
            output += f"{emoji} Sentiment: {sentiment_label}\n"

        output += (
            f"💬 Response: {response[:100]}{'...' if len(response) > 100 else ''}\n"
        )
        output += "-" * 40 + "\n\n"

    return output


def format_statistics(stats):
    """
    Format database statistics for display
    Enhanced with sentiment and timing stats!
    """
    output = "📈 **Overall Statistics**\n"
    output += "=" * 50 + "\n\n"
    output += f"📊 **Total Generations:** {stats['total_generations']}\n\n"

    # Model stats with timing
    if stats["model_stats"]:
        output += "🤖 **Model Performance:**\n"
        output += "-" * 40 + "\n"
        for row in stats["model_stats"]:
            model = row[0]
            avg_diversity = row[1]
            count = row[2]
            avg_time = row[3] if len(row) > 3 else None

            output += f"\n**{model}**\n"
            output += f"  • Generations: {count}\n"
            output += f"  • Avg Diversity: {avg_diversity:.1f}%\n"
            if avg_time:
                output += f"  • Avg Response Time: {avg_time:.2f}s\n"
        output += "\n"

    # Sentiment stats
    if stats.get("sentiment_stats"):
        output += "😊 **Sentiment Distribution:**\n"
        output += "-" * 40 + "\n"
        for sentiment, count in stats["sentiment_stats"]:
            if sentiment:
                emoji = (
                    "😊"
                    if sentiment == "POSITIVE"
                    else "😟"
                    if sentiment == "NEGATIVE"
                    else "😐"
                )
                output += f"  {emoji} {sentiment}: {count}\n"
        output += "\n"

    # Average response time
    if stats.get("avg_response_time"):
        output += f"⏱️ **Average Response Time:** {stats['avg_response_time']:.2f}s\n"

    return output


def export_to_csv():
    """
    Export all generations to CSV format

    Returns:
    - CSV string that can be downloaded
    """
    columns, rows = get_export_data()

    if not rows:
        return None, "No data to export!"

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)  # Create a CSV writer object

    # Write header
    writer.writerow(columns)  # Write the column names as the first row of the CSV file

    # Write data
    for row in rows:
        writer.writerow(row)  # Write each row of data to the CSV file

    csv_content = output.getvalue()  # Get the entire CSV content as a string
    output.close()  # Close the in-memory file

    # Generate filename with timestamp
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )  # format current date and time for filename
    filename = f"llm_generations_{timestamp}.csv"

    return csv_content, filename


def get_comparison_summary(results):
    """
    Generate a quick comparison summary

    Parameters:
    - results: Dictionary with all model results

    Returns:
    - Formatted comparison string
    """
    summary = "📊 **Quick Comparison**\n"
    summary += "| Model | Diversity | Sentiment | Time |\n"
    summary += "|-------|-----------|-----------|------|\n"

    for name, data in results.items():
        if name in ["Generation Stats", "Recommendation"]:
            continue

        if data.get("status") == "Successfully generated":
            diversity = data["metrics"]["diversity"]
            sentiment = data.get("sentiment", {}).get("label", "N/A")
            gen_time = data.get("generation_time", "N/A")

            if isinstance(
                gen_time, float
            ):  # Format generation time to 2 decimal places if it's a float
                gen_time = f"{gen_time:.2f}s"

            ## Add a row to the summary table for each model, showing its name, diversity score, sentiment label, and generation time
            summary += f"| {name.split('(')[0].strip()} | {diversity}% | {sentiment} | {gen_time} |\n"

    return summary
