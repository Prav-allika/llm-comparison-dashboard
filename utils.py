"""
Utility Functions
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

# ── Light-theme color palette ────────────────────────────────────────────────
# Background tones derived from the coral/salmon/sage palette
BG_PAGE      = "#FEF5F2"   # lightest warm cream — whole page background
BG_CARD      = "#FFFFFF"   # white — individual model/entry cards
BG_INNER     = "#FDF0EC"   # light salmon — inner boxes (response text, metric tiles)
BG_BAR       = "#FEF5F2"   # same as page — stats bar
BG_REC       = "#F5F9F0"   # light sage tint — recommendation card
BG_TOTAL     = "#FDF0EC"   # light salmon — total generations card
BG_AVGTIME   = "#F9F5FF"   # very light lavender — avg response time card

# Accent colors (model borders, headings, badges)
C_CORAL      = "#E85555"   # coral red — model 1
C_SALMON     = "#F0A490"   # salmon peach — model 2
C_SAGE       = "#A8CC88"   # sage green — model 3
C_SAGE_DARK  = "#6EA850"   # darker sage — headings / h3

# Text colors on light background
T_PRIMARY    = "#1A1A1A"   # near-black — main text
T_SECONDARY  = "#555555"   # medium grey — secondary labels
T_MUTED      = "#888888"   # light grey — timestamps, captions
T_ON_ACCENT  = "#FFFFFF"   # white text on colored badges

# Border
BORDER_LIGHT = "#E8DDD8"   # warm light grey border


def format_output(
    results,
):  # formatting output for display in Gradio as colorful HTML cards
    """
    Format generation results for display in Gradio as colorful HTML
    Enhanced with sentiment and timing display!
    """
    # Color palette for the 3 models — coral, salmon, sage (matching app palette)
    colors = [C_CORAL, C_SALMON, C_SAGE]
    color_idx = 0

    # Outer container with page background
    html = f'<div style="font-family: Arial, sans-serif; padding: 10px; background: {BG_PAGE};">'

    # Loop through each model's results
    for model_name, data in results.items():
        if model_name in ["Generation Stats", "Recommendation"]:
            continue

        # Assign a color to this model
        color = colors[color_idx % len(colors)]
        color_idx += 1

        # Model card with colored left border on white background
        html += (
            f'<div style="border-left: 5px solid {color}; background: {BG_CARD}; '
            f'padding: 16px; margin: 14px 0; border-radius: 10px; '
            f'box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid {BORDER_LIGHT}; '
            f'border-left: 5px solid {color};">'
        )

        # Model name header in the card's accent color
        html += f'<h3 style="color: {color}; margin: 0 0 8px 0; font-size: 1.1em;">{model_name}</h3>'

        # Generation time badge shown below the model name
        if "generation_time" in data:
            html += (
                f'<span style="background: {color}18; color: {color}; padding: 3px 10px; '
                f'border-radius: 20px; font-size: 0.82em; display: inline-block; '
                f'margin-bottom: 10px; border: 1px solid {color}44;">'
                f'Generated in {data["generation_time"]}s</span>'
            )

        if data.get("status") == "Successfully generated":
            # Response text inside a light inner box for readability
            html += (
                f'<div style="background: {BG_INNER}; padding: 12px; border-radius: 8px; '
                f'margin: 10px 0; line-height: 1.7; color: {T_PRIMARY}; font-size: 0.95em; '
                f'border: 1px solid {BORDER_LIGHT};">'
                f'{data["response"]}</div>'
            )

            # Metrics displayed as small colored tiles
            metrics = data["metrics"]
            html += '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0;">'
            metric_items = [
                ("Words", metrics["word_count"]),
                ("Unique", metrics["unique_words"]),
                ("Diversity", f'{metrics["diversity"]}%'),
                ("Readability", metrics["readability_score"]),
                ("Grade Level", metrics["grade_level"]),
            ]
            for label, value in metric_items:
                # Each metric tile with light background and accent-color label
                html += (
                    f'<div style="background: {BG_INNER}; border: 1px solid {color}44; '
                    f'padding: 8px 14px; border-radius: 8px; text-align: center; min-width: 85px;">'
                    f'<div style="color: {color}; font-size: 0.72em; text-transform: uppercase; margin-bottom: 4px;">{label}</div>'
                    f'<div style="color: {T_PRIMARY}; font-weight: bold; font-size: 1.05em;">{value}</div>'
                    f'</div>'
                )
            html += '</div>'  # close metrics row

            # Add sentiment if available as a colored badge
            if data.get("sentiment") and data["sentiment"].get("label") not in [
                "UNKNOWN",
                "ERROR",
                None,
            ]:
                sentiment = data["sentiment"]  # sentiment label and confidence score
                badge_color = C_SAGE if sentiment["label"] == "POSITIVE" else C_CORAL
                html += (
                    f'<div style="margin-top: 10px;">'
                    f'<span style="background: {badge_color}18; color: {badge_color}; '
                    f'border: 1px solid {badge_color}; padding: 4px 14px; '
                    f'border-radius: 20px; font-size: 0.88em; font-weight: bold;">'
                    f'Sentiment: {sentiment["label"]} — {sentiment["score"] * 100:.1f}% confidence'
                    f'</span></div>'
                )
        else:
            # Error state in coral text
            html += f'<div style="color: {C_CORAL}; margin-top: 8px;">Error: {data["response"]}</div>'

        html += '</div>'  # close model card

    # Generation stats summary bar at the bottom
    if "Generation Stats" in results:
        stats = results["Generation Stats"]
        html += (
            f'<div style="background: {BG_BAR}; border: 1px solid {BORDER_LIGHT}; padding: 12px 18px; '
            f'border-radius: 8px; margin: 12px 0; display: flex; gap: 24px; flex-wrap: wrap; '
            f'color: {T_SECONDARY}; font-size: 0.9em;">'
        )
        html += f'<span><strong style="color:{T_PRIMARY};">Total Time:</strong> {stats["elapsed_time"]}</span>'
        html += f'<span><strong style="color:{T_PRIMARY};">Avg / Model:</strong> {stats["average_time_per_model"]}</span>'
        html += f'<span><strong style="color:{T_PRIMARY};">Mode:</strong> {stats.get("mode", "Sequential")}</span>'
        html += '</div>'

    # Recommendation card highlighting best and fastest models
    if "Recommendation" in results:
        rec = results["Recommendation"]
        html += (
            f'<div style="background: {BG_REC}; border: 1px solid {C_SAGE}88; padding: 14px 18px; '
            f'border-radius: 8px; margin: 10px 0;">'
        )
        html += (
            f'<strong style="color: {C_SAGE_DARK};">Best Quality:</strong> '
            f'<span style="color:{T_PRIMARY};">{rec["best_model"]}</span> '
            f'<span style="color:{T_SECONDARY};">— {rec["reason"]}</span>'
        )
        if rec.get("fastest_model"):
            html += (
                f'<br><strong style="color: {C_SALMON};">Fastest:</strong> '
                f'<span style="color:{T_PRIMARY};">{rec["fastest_model"]}</span> '
                f'<span style="color:{T_SECONDARY};">({rec["fastest_time"]})</span>'
            )
        html += '</div>'

    html += '</div>'  # close outer container
    return html


def format_history(
    rows,
):  # formatting database history for display as styled HTML cards
    """
    Format database history for display
    Enhanced with sentiment and timing!
    """
    if not rows:
        # Empty state message centered on the page
        return (
            f'<div style="text-align: center; color: {T_MUTED}; padding: 60px; '
            f'font-family: Arial, sans-serif; background: {BG_PAGE};">'
            f'No generations yet. Try generating some text first.'
            f'</div>'
        )

    # Color palette cycling through entries to add visual variety
    colors = [C_CORAL, C_SALMON, C_SAGE]

    html = f'<div style="font-family: Arial, sans-serif; padding: 10px; background: {BG_PAGE};">'
    html += f'<h3 style="color: {C_SAGE_DARK}; margin-bottom: 16px;">Generation History</h3>'

    for idx, row in enumerate(rows):
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
            formatted_time = dt.strftime("%Y-%m-%d  %H:%M:%S")
        except:
            formatted_time = timestamp

        # Cycle through accent colors to distinguish entries visually
        color = colors[idx % len(colors)]

        # Card container for each history entry on white background
        html += (
            f'<div style="border-left: 4px solid {color}; background: {BG_CARD}; '
            f'padding: 14px 16px; margin: 10px 0; border-radius: 8px; '
            f'box-shadow: 0 1px 4px rgba(0,0,0,0.07); border: 1px solid {BORDER_LIGHT}; '
            f'border-left: 4px solid {color};">'
        )

        # Header row: model name (left) and timestamp (right)
        html += (
            '<div style="display: flex; justify-content: space-between; '
            'align-items: center; margin-bottom: 10px;">'
        )
        html += f'<span style="color: {color}; font-weight: bold; font-size: 1em;">{model.split(" (")[0]}</span>'
        html += f'<span style="color: {T_MUTED}; font-size: 0.82em;">{formatted_time}</span>'
        html += '</div>'

        # Prompt preview truncated to 70 chars for readability
        short_prompt = prompt[:70] + "..." if len(prompt) > 70 else prompt
        html += (
            f'<div style="color: {T_SECONDARY}; margin-bottom: 8px; font-size: 0.9em;">'
            f'<strong style="color: {T_SECONDARY};">Prompt:</strong> {short_prompt}</div>'
        )

        # Response preview in a light inner box, truncated to 140 chars
        short_response = response[:140] + "..." if len(response) > 140 else response
        html += (
            f'<div style="background: {BG_INNER}; padding: 10px 12px; border-radius: 6px; '
            f'color: {T_PRIMARY}; font-size: 0.88em; line-height: 1.6; margin-bottom: 10px; '
            f'border: 1px solid {BORDER_LIGHT};">'
            f'{short_response}</div>'
        )

        # Metrics row displayed inline as small tags
        html += f'<div style="display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.83em; color: {T_SECONDARY};">'
        html += f'<span><strong style="color: {T_PRIMARY};">Words:</strong> {words}</span>'
        html += f'<span><strong style="color: {T_PRIMARY};">Diversity:</strong> {diversity}%</span>'
        html += f'<span><strong style="color: {T_PRIMARY};">Creativity:</strong> {temp}</span>'
        html += f'<span><strong style="color: {T_PRIMARY};">Max Length:</strong> {max_len}</span>'

        # Add timing if available
        if response_time:
            html += f'<span><strong style="color: {T_PRIMARY};">Time:</strong> {response_time:.2f}s</span>'

        # Add sentiment if available as a small colored badge
        if sentiment_label and sentiment_label not in ["UNKNOWN", "ERROR"]:
            badge_color = C_SAGE if sentiment_label == "POSITIVE" else C_CORAL
            html += (
                f'<span style="background: {badge_color}18; color: {badge_color}; '
                f'border: 1px solid {badge_color}66; padding: 2px 10px; '
                f'border-radius: 12px;">Sentiment: {sentiment_label}</span>'
            )

        html += '</div>'  # close metrics row
        html += '</div>'  # close card

    html += '</div>'  # close outer container
    return html


def format_statistics(stats):
    """
    Format database statistics for display
    Enhanced with sentiment and timing stats!
    """
    html = f'<div style="font-family: Arial, sans-serif; padding: 10px; background: {BG_PAGE};">'
    html += f'<h3 style="color: {C_SAGE_DARK}; margin-bottom: 16px;">Overall Statistics</h3>'

    # Total generations shown as a prominent highlight card
    html += (
        f'<div style="background: {BG_TOTAL}; border: 1px solid {C_SAGE}88; padding: 20px; '
        f'border-radius: 10px; margin-bottom: 18px; text-align: center;">'
        f'<div style="color: {T_SECONDARY}; font-size: 0.82em; text-transform: uppercase; letter-spacing: 1px;">Total Generations</div>'
        f'<div style="color: {C_SAGE_DARK}; font-size: 2.8em; font-weight: bold; margin-top: 4px;">{stats["total_generations"]}</div>'
        f'</div>'
    )

    # Model performance cards
    if stats["model_stats"]:
        colors = [C_CORAL, C_SALMON, C_SAGE]  # Color palette for the 3 models
        html += f'<h4 style="color: {T_PRIMARY}; margin-bottom: 10px;">Model Performance</h4>'

        for idx, row in enumerate(stats["model_stats"]):
            model = row[0]
            avg_diversity = row[1]
            count = row[2]
            avg_time = row[3] if len(row) > 3 else None  # timing added in later version

            color = colors[idx % len(colors)]

            # Each model gets a horizontal card with metric tiles on white background
            html += (
                f'<div style="border-left: 4px solid {color}; background: {BG_CARD}; '
                f'padding: 12px 16px; margin: 8px 0; border-radius: 8px; '
                f'box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid {BORDER_LIGHT}; '
                f'border-left: 4px solid {color}; display: flex; gap: 14px; flex-wrap: wrap; align-items: center;">'
            )
            # Model name label on the left in accent color
            html += f'<div style="color: {color}; font-weight: bold; min-width: 170px; font-size: 0.95em;">{model.split(" (")[0]}</div>'

            # Metric tiles: runs, avg diversity, avg time
            for label, value in [
                ("Runs", count),
                ("Avg Diversity", f"{avg_diversity:.1f}%"),
            ]:
                html += (
                    f'<div style="background: {BG_INNER}; padding: 7px 14px; border-radius: 7px; '
                    f'text-align: center; border: 1px solid {BORDER_LIGHT};">'
                    f'<div style="color: {T_MUTED}; font-size: 0.72em; text-transform: uppercase;">{label}</div>'
                    f'<div style="color: {T_PRIMARY}; font-weight: bold; font-size: 1.05em;">{value}</div>'
                    f'</div>'
                )
            if avg_time:
                html += (
                    f'<div style="background: {BG_INNER}; padding: 7px 14px; border-radius: 7px; '
                    f'text-align: center; border: 1px solid {BORDER_LIGHT};">'
                    f'<div style="color: {T_MUTED}; font-size: 0.72em; text-transform: uppercase;">Avg Time</div>'
                    f'<div style="color: {T_PRIMARY}; font-weight: bold; font-size: 1.05em;">{avg_time:.2f}s</div>'
                    f'</div>'
                )
            html += '</div>'  # close model card

    # Sentiment distribution shown as colored count badges
    if stats.get("sentiment_stats"):
        html += f'<h4 style="color: {T_PRIMARY}; margin: 18px 0 10px;">Sentiment Distribution</h4>'
        html += '<div style="display: flex; gap: 12px; flex-wrap: wrap;">'
        sentiment_colors = {"POSITIVE": C_SAGE, "NEGATIVE": C_CORAL}
        for sentiment, count in stats["sentiment_stats"]:
            if sentiment:
                color = sentiment_colors.get(sentiment, T_MUTED)  # fallback grey for neutral/unknown
                html += (
                    f'<div style="background: {color}18; border: 1px solid {color}; '
                    f'padding: 12px 24px; border-radius: 10px; text-align: center;">'
                    f'<div style="color: {color}; font-size: 0.78em; text-transform: uppercase; letter-spacing: 1px;">{sentiment}</div>'
                    f'<div style="color: {T_PRIMARY}; font-weight: bold; font-size: 1.8em; margin-top: 4px;">{count}</div>'
                    f'</div>'
                )
        html += '</div>'  # close sentiment row

    # Average response time shown as a subtle info card
    if stats.get("avg_response_time"):
        html += (
            f'<div style="background: {BG_AVGTIME}; border: 1px solid {C_SALMON}88; padding: 12px 18px; '
            f'border-radius: 8px; margin-top: 18px;">'
            f'<strong style="color: {C_SALMON};">Average Response Time:</strong> '
            f'<span style="color: {T_PRIMARY};">{stats["avg_response_time"]:.2f}s</span>'
            f'</div>'
        )

    html += '</div>'  # close outer container
    return html


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
    summary = "**Quick Comparison**\n"
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
