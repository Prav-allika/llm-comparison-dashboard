"""
Visualization Charts
Create interactive charts for model comparison
"""

# create interactive and web-based charts
import plotly.graph_objects as go

# get data from database for charts
from database import get_chart_data


def create_diversity_comparison_chart(
    results,
):  # chart to compare diversity scores across models
    """
    Create a bar chart comparing diversity scores across models
    """
    models = []
    diversity_scores = []
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

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
        title="📊 Diversity Score Comparison",
        xaxis_title="Model",
        yaxis_title="Diversity (%)",
        yaxis_range=[0, 100],
        template="plotly_dark",
        height=400,
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

    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
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
        title="📈 Model Metrics Comparison (Radar)",
        template="plotly_dark",
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
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]

    for name, data in results.items():
        if name not in ["Generation Stats", "Recommendation"]:
            if "generation_time" in data:
                models.append(name.split(" (")[0])
                times.append(data["generation_time"])

    if not models:
        fig = go.Figure()
        fig.update_layout(
            title="⏱️ Response Time (No data yet)",
            template="plotly_dark",
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
        title="⏱️ Response Time per Model",
        xaxis_title="Model",
        yaxis_title="Time (seconds)",
        template="plotly_dark",
        height=300,
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
            title="📈 Diversity Trend Over Time (No data yet)",
            template="plotly_dark",
            height=400,
        )
        return fig

    # Group by model
    model_data = {}
    for row in data:
        # FIXED: Unpack all 5 values from database query
        # (timestamp, model, diversity, sentiment_label, response_time)
        timestamp = row[0]
        model = row[1]
        diversity = row[2]
        # sentiment_label = row[3]  # Not used in this chart
        # response_time = row[4]    # Not used in this chart

        if model not in model_data:
            model_data[model] = {"timestamps": [], "diversity": []}
        model_data[model]["timestamps"].append(timestamp)
        model_data[model]["diversity"].append(diversity)

    fig = go.Figure()
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
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
        title="📈 Diversity Score Trend Over Time",
        xaxis_title="Time",
        yaxis_title="Diversity (%)",
        template="plotly_dark",
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
            title="🥧 Model Usage Distribution (No data yet)",
            template="plotly_dark",
            height=400,
        )
        return fig

    # Count usage per model
    model_counts = {}
    for row in data:
        # FIXED: Access model by index (row[1]) instead of unpacking
        model = row[1]
        model_counts[model] = model_counts.get(model, 0) + 1

    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(model_counts.keys()),
                values=list(model_counts.values()),
                hole=0.4,
                marker_colors=["#FF6B6B", "#4ECDC4", "#45B7D1"],
            )
        ]
    )

    fig.update_layout(
        title="🥧 Model Usage Distribution",
        template="plotly_dark",
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
        "POSITIVE": "#4ECDC4",
        "NEGATIVE": "#FF6B6B",
        "NEUTRAL": "#FFE66D",
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
            title="😊 Sentiment Analysis (No data yet)",
            template="plotly_dark",
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
        title="😊 Sentiment Analysis by Model",
        xaxis_title="Model",
        yaxis_title="Confidence (%)",
        yaxis_range=[0, 110],
        template="plotly_dark",
        height=350,
        showlegend=False,
    )

    return fig
