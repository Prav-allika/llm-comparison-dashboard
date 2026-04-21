"""
Visualization Charts
Create interactive charts for model comparison
"""

# create interactive and web-based charts
import plotly.graph_objects as go

# get data from database for charts
from database import get_chart_data

# import current model list to filter charts to only show active models
from config import MODEL_LIST

# Set of display names for the 3 currently configured models
CURRENT_MODELS = set(MODEL_LIST.keys())


def create_diversity_comparison_chart(
    results,
):  # chart to compare diversity scores across models
    """
    Create a bar chart comparing diversity scores across models
    """
    models = []
    diversity_scores = []
    colors = ["#E85555", "#F0A490", "#A8CC88"]

    for (
        name,
        data,
    ) in (
        results.items()
    ):  # Loop through results to extract model names and diversity scores
        if name not in ["Generation Stats", "Recommendation"]:
            if data.get("status") == "Successfully generated":
                models.append(
                    name.replace(" (Fast)", "")
                    .replace(" (Standard)", "")
                    .replace(" (Better)", "")
                )
                diversity_scores.append(data["metrics"]["diversity"])

    fig = go.Figure(  # Create a bar chart with model names on x-axis and diversity scores on y-axis
        data=[
            go.Bar(
                x=models,
                y=diversity_scores,
                marker_color=colors[: len(models)],
                text=[f"{score}%" for score in diversity_scores],
                textposition="outside",
            )
        ]
    )

    fig.update_layout(  # Update layout with titles and axis labels
        title="Diversity Score Comparison",
        xaxis_title="Model",
        yaxis_title="Diversity (%)",
        yaxis_range=[0, 115],      # extra headroom so "outside" labels aren't clipped
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=420,               # slightly taller to give more label space
        showlegend=False,  # Hide legend since we have only one bar per model
    )

    return fig


def create_metrics_radar_chart(
    results,
):  # chart to compare multiple metrics across models in a radar/spider format
    """
    Create a radar chart showing all metrics for each model
    """
    fig = go.Figure()

    colors = ["#E85555", "#F0A490", "#A8CC88"]
    color_idx = 0

    for name, data in results.items():
        if name not in ["Generation Stats", "Recommendation"]:
            if data.get("status") == "Successfully generated":
                metrics = data["metrics"]

                categories = ["Diversity", "Readability", "Word Count", "Unique Words"]
                values = [
                    metrics["diversity"],
                    min(metrics["readability_score"], 100),
                    min(metrics["word_count"], 100),
                    min(metrics["unique_words"], 100),
                ]

                categories.append(categories[0])
                values.append(values[0])

                fig.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill="toself",  # Fill the area under the line for better visualization
                        name=name.split(" (")[0],  # Use model name without speed label
                        line_color=colors[
                            color_idx % len(colors)
                        ],  # Cycle through colors for each model
                    )
                )
                color_idx += 1

    fig.update_layout(  # layout for radar chart with titles and axis settings
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Model Metrics Comparison (Radar)",
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=450,
        showlegend=True,
    )

    return fig


def create_response_time_chart(
    results,
):  # chart to show response time per model in a bar chart
    """
    Create a bar chart showing response times per model
    """
    models = []
    times = []
    colors = ["#E85555", "#F0A490", "#A8CC88"]

    for name, data in results.items():
        if name not in ["Generation Stats", "Recommendation"]:
            if "generation_time" in data:
                models.append(name.split(" (")[0])
                times.append(data["generation_time"])

    if not models:
        fig = go.Figure()
        fig.update_layout(
            title="Response Time (No data yet)",
            template="plotly_white",
            paper_bgcolor="#FEF5F2",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#1A1A1A"),
            height=300,
        )
        return fig

    fig = go.Figure(
        data=[
            go.Bar(
                x=models,
                y=times,
                marker_color=colors[: len(models)],
                text=[f"{t:.2f}s" for t in times],
                textposition="outside",
            )
        ]
    )

    fig.update_layout(
        title="Response Time per Model",
        xaxis_title="Model",
        yaxis_title="Time (seconds)",
        yaxis=dict(range=[0, max(times) * 1.25]),  # 25% headroom so labels aren't clipped
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=340,               # slightly taller to give more label space
        showlegend=False,
    )

    return fig


def create_history_trend_chart():  # chart to show diversity trends over time in a line chart
    """
    Create a line chart showing diversity trends over time

    FIXED: Now correctly unpacks all 5 values from database
    """
    data = get_chart_data()

    if not data:
        fig = go.Figure()
        fig.update_layout(
            title="Diversity Trend Over Time (No data yet)",
            template="plotly_white",
            paper_bgcolor="#FEF5F2",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#1A1A1A"),
            height=400,
        )
        return fig

    # Group by model, filtering to only the 3 currently configured models
    model_data = {}
    for row in data:
        # FIXED: Unpack all 5 values from database query
        # (timestamp, model, diversity, sentiment_label, response_time)
        timestamp = row[0]
        model = row[1]
        diversity = row[2]
        # sentiment_label = row[3]  # Not used in this chart
        # response_time = row[4]    # Not used in this chart

        # Skip models that are no longer in the active model list
        if model not in CURRENT_MODELS:
            continue

        if model not in model_data:
            model_data[model] = {"timestamps": [], "diversity": []}
        model_data[model]["timestamps"].append(timestamp)
        model_data[model]["diversity"].append(diversity)

    fig = go.Figure()
    colors = ["#E85555", "#F0A490", "#A8CC88"]
    color_idx = 0

    for model, values in model_data.items():
        fig.add_trace(
            go.Scatter(
                x=values["timestamps"],
                y=values["diversity"],
                mode="lines+markers",
                name=model.split(" (")[0],
                line=dict(color=colors[color_idx % len(colors)], width=2),
            )
        )
        color_idx += 1

    fig.update_layout(
        title="Diversity Score Trend Over Time",
        xaxis_title="Time",
        yaxis_title="Diversity (%)",
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=400,
        showlegend=True,
    )

    return fig


def create_model_usage_pie_chart():  # chart to show distribution of model usage in a pie chart
    """
    Create a pie chart showing model usage distribution

    FIXED: Now correctly handles all 5 values from database
    """
    data = get_chart_data()

    if not data:
        fig = go.Figure()
        fig.update_layout(
            title="Model Usage Distribution (No data yet)",
            template="plotly_white",
            paper_bgcolor="#FEF5F2",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#1A1A1A"),
            height=400,
        )
        return fig

    # Count usage per model, filtering to only the 3 currently configured models
    model_counts = {}
    for row in data:
        # FIXED: Access model by index (row[1]) instead of unpacking
        model = row[1]
        # Skip old models that are no longer in the active model list
        if model not in CURRENT_MODELS:
            continue
        model_counts[model] = model_counts.get(model, 0) + 1

    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(model_counts.keys()),
                values=list(model_counts.values()),
                hole=0.4,
                marker_colors=["#E85555", "#F0A490", "#A8CC88"],
            )
        ]
    )

    fig.update_layout(
        title="Model Usage Distribution",
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=400,
    )

    return fig


def create_sentiment_distribution_chart(
    results,
):  # chart to show sentiment distribution across models in a bar chart
    """
    Create a bar chart showing sentiment analysis results
    """
    models = []
    sentiments = []
    scores = []
    colors = []

    sentiment_colors = {
        "POSITIVE": "#A8CC88",
        "NEGATIVE": "#E85555",
        "NEUTRAL": "#F0A490",
    }

    for name, data in results.items():
        if name not in ["Generation Stats", "Recommendation"]:
            if (
                data.get("status") == "Successfully generated"
                and "sentiment" in data
                and data["sentiment"]
            ):
                models.append(name.split(" (")[0])
                sentiment = data["sentiment"].get("label", "UNKNOWN")
                sentiments.append(sentiment)
                scores.append(data["sentiment"].get("score", 0) * 100)
                colors.append(sentiment_colors.get(sentiment, "#CCCCCC"))

    if not models:
        fig = go.Figure()
        fig.update_layout(
            title="Sentiment Analysis (No data yet)",
            template="plotly_white",
            paper_bgcolor="#FEF5F2",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#1A1A1A"),
            height=300,
        )
        return fig

    fig = go.Figure(
        data=[
            go.Bar(
                x=models,
                y=scores,
                marker_color=colors,
                text=[f"{s}<br>{score:.1f}%" for s, score in zip(sentiments, scores)],
                textposition="outside",
            )
        ]
    )

    fig.update_layout(
        title="Sentiment Analysis by Model",
        xaxis_title="Model",
        yaxis_title="Confidence (%)",
        yaxis_range=[0, 120],      # extra headroom so confidence labels aren't clipped
        template="plotly_white",
        paper_bgcolor="#FEF5F2",  # match page background
        plot_bgcolor="#FFFFFF",   # white chart area
        font=dict(color="#1A1A1A"),  # dark text for readability
        height=370,               # slightly taller to give more label space
        showlegend=False,
    )

    return fig
