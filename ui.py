"""
User Interface
Gradio web interface for the dashboard
Enhanced with Charts, Export, and more!
"""

# creates web interface
import gradio as gr

# creates temporary files for export
import tempfile

# file path operations
import os

# Import configurations
from config import (
    CSS_STYLES,
    EXAMPLE_PROMPTS,
    DEFAULT_MAX_LENGTH,
    DEFAULT_CREATIVITY,
    MIN_LENGTH,
    MAX_LENGTH,
    MIN_CREATIVITY,
    MAX_CREATIVITY,
    HISTORY_DEFAULT_LIMIT,
    PROMPT_TEMPLATES,
    ENABLE_SENTIMENT,
    MODEL_LIST,
)

# generate text and evaluate with all models
from models import generate_from_all

# get generation history and statistics from database
from database import get_generation_history, get_statistics, clear_all_history

# Format outputs and statistics for display, and handle CSV export
from utils import format_output, format_history, format_statistics, export_to_csv

# Create charts for diversity comparison, response time, history trends, model usage, and sentiment distribution
from charts import (
    create_diversity_comparison_chart,
    create_metrics_radar_chart,
    create_response_time_chart,
    create_history_trend_chart,
    create_model_usage_pie_chart,
    create_sentiment_distribution_chart,
)


# Store last results for charting
last_results = {}


# this function called when generate button clicked
def generate_and_format(prompt, max_length, creativity):
    """
    Generate text and format output with charts
    """
    global last_results

    results = generate_from_all(prompt, max_length, creativity)
    last_results = results
    # format_output now returns HTML for colorful display
    formatted = format_output(results)

    # Generate charts
    diversity_chart = create_diversity_comparison_chart(results)
    time_chart = create_response_time_chart(results)

    # Sentiment chart (if enabled)
    if ENABLE_SENTIMENT:
        sentiment_chart = create_sentiment_distribution_chart(results)
    else:
        sentiment_chart = None

    return formatted, diversity_chart, time_chart, sentiment_chart


# refresh button in history tab
def load_history(limit):
    """Load and format generation history"""
    rows = get_generation_history(limit=int(limit))
    return format_history(rows)  # returns HTML string


# refresh button in statistics tab
def load_statistics():
    """Load and format statistics"""
    stats = get_statistics()
    return format_statistics(stats)  # returns HTML string


# refresh button in charts tab
def load_charts():
    """Load historical charts"""
    trend_chart = create_history_trend_chart()
    pie_chart = create_model_usage_pie_chart()
    return trend_chart, pie_chart


# danger zone button in statistics tab
def clear_history_handler():
    """Clear all history"""
    clear_all_history()
    return " All history has been cleared!"


# csv export button in history tab
def export_csv_handler():
    """Export data to CSV and return file path"""
    csv_content, filename = export_to_csv()

    if csv_content is None:
        return None, filename  # filename contains error message

    # Save to temp file
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        f.write(csv_content)

    return filepath, f"Exported {filename}"


# template dropdown in generation tab
def apply_template(template_name):
    """Apply a prompt template"""
    return PROMPT_TEMPLATES.get(template_name, "")


def create_interface():
    """
    Create and return the Gradio interface
    Now with Charts and Export!
    """
    # Build a readable model summary line for the footer from the active MODEL_LIST
    model_summary = " • ".join(MODEL_LIST.keys())

    # container for the entire app, with custom CSS and theme
    # Custom Base theme — every color explicitly set to match the coral/salmon/sage palette
    palette_theme = gr.themes.Base(
        primary_hue=gr.themes.colors.orange,   # closest built-in hue to coral
        secondary_hue=gr.themes.colors.stone,  # warm neutral for backgrounds
        neutral_hue=gr.themes.colors.stone,    # warm grey for text
    ).set(
        # Page and block backgrounds
        body_background_fill="#FEF5F2",              # warmest cream — whole page
        body_background_fill_dark="#FEF5F2",
        block_background_fill="#FFFFFF",             # white cards
        block_background_fill_dark="#FFFFFF",
        panel_background_fill="#FDF0EC",             # light salmon for panels
        panel_background_fill_dark="#FDF0EC",

        # Labels — coral text, no dark pill background
        block_label_background_fill="#FEF5F2",
        block_label_background_fill_dark="#FEF5F2",
        block_label_text_color="#C03030",            # deep coral for label text
        block_label_text_color_dark="#C03030",
        block_title_text_color="#C03030",
        block_title_text_color_dark="#C03030",

        # Input fields — clean white with warm border
        input_background_fill="#FFFFFF",
        input_background_fill_dark="#FFFFFF",
        input_border_color="#E8DDD8",
        input_border_color_dark="#E8DDD8",

        # Borders
        border_color_primary="#E8DDD8",
        border_color_primary_dark="#E8DDD8",
        border_color_accent="#E85555",
        border_color_accent_dark="#E85555",

        # Body and input text — must be dark so it's visible on white background
        body_text_color="#1A1A1A",
        body_text_color_dark="#1A1A1A",
        input_placeholder_color="#AAAAAA",
        input_placeholder_color_dark="#AAAAAA",

        # Primary button — coral (overridden further by .generate-btn CSS)
        button_primary_background_fill="#E85555",
        button_primary_background_fill_dark="#E85555",
        button_primary_background_fill_hover="#F0A490",
        button_primary_text_color="#FFFFFF",
        button_primary_text_color_dark="#FFFFFF",

        # Slider track — coral
        slider_color="#E85555",
        slider_color_dark="#E85555",

        # Table rows (Examples section)
        table_even_background_fill="#FDF0EC",
        table_even_background_fill_dark="#FDF0EC",
        table_odd_background_fill="#FFFFFF",
        table_odd_background_fill_dark="#FFFFFF",
        table_row_focus="#FDECEA",
        table_row_focus_dark="#FDECEA",
    )

    with gr.Blocks(css=CSS_STYLES, theme=palette_theme) as demo:
        # Header
        gr.Markdown(
            """
            # AI Text Comparison Dashboard
            ### Compare outputs from 3 local AI models with automatic quality scoring

            **Features:** Auto evaluation • Sentiment Analysis • Charts • Database • Export
            """
        )

        # Create tabs
        with gr.Tabs():  # tab container
            # TAB 1: Generate Text

            with gr.TabItem("Generate Text"):  # first tab
                with gr.Row():  # Horizontal layout (side by side)
                    with gr.Column(
                        scale=1
                    ):  # Vertical layout (stacked) , scale=1 means it takes up equal space as the other column
                        # Template dropdown
                        template_dropdown = gr.Dropdown(
                            choices=list(
                                PROMPT_TEMPLATES.keys()
                            ),  # List of template names from config.py
                            label="Quick Templates",  # Label shown
                            value=None,  # default value (none selected)
                            interactive=True,  # user can interact with it
                        )

                        # Input textbox
                        prompt_input = gr.Textbox(
                            label="Your Creative Prompt",
                            placeholder="Once upon a time in a magical kingdom...",  # hint text shown when empty
                            lines=5,  # height of the textbox
                            value="Once upon a time",  # default value (can be empty or a common starting prompt
                        )

                        # Connect template to prompt
                        template_dropdown.change(
                            fn=apply_template,  # function to call when dropdown changes
                            inputs=[
                                template_dropdown
                            ],  # input is the selected template name
                            outputs=[prompt_input],  # output is the prompt textbox
                        )

                        # Sliders in a row
                        with gr.Row():
                            max_length_slider = gr.Slider(
                                minimum=MIN_LENGTH,
                                maximum=MAX_LENGTH,
                                value=DEFAULT_MAX_LENGTH,
                                step=10,
                                label="Max Length",
                            )

                            creativity_slider = gr.Slider(
                                minimum=MIN_CREATIVITY,
                                maximum=MAX_CREATIVITY,
                                value=DEFAULT_CREATIVITY,
                                step=0.1,
                                label="Creativity (Temperature)",
                            )

                        # Generate button
                        generate_btn = gr.Button(
                            "Generate & Evaluate",
                            elem_classes="generate-btn",  # custom CSS class for styling
                            size="lg",  # large button
                        )

                        # Example prompts
                        gr.Markdown("### Example Prompts:")
                        gr.Examples(
                            examples=EXAMPLE_PROMPTS,  # list of example prompts with settings from config.py``
                            inputs=[
                                prompt_input,
                                max_length_slider,
                                creativity_slider,
                            ],  # connect examples to the input components``
                        )

                # Output section — full-width HTML card display, no raw JSON
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Generated Text + Metrics")
                        # gr.HTML renders the colorful HTML cards returned by format_output
                        formatted_output = gr.HTML(
                            label="Results",
                        )

                # Charts section
                gr.Markdown("### Live Comparison Charts")
                with gr.Row():
                    diversity_plot = gr.Plot(
                        label="Diversity Comparison"
                    )  # chart to compare diversity metric across models
                    time_plot = gr.Plot(
                        label="Response Time"
                    )  # chart to compare response time across models

                if ENABLE_SENTIMENT:
                    with gr.Row():
                        sentiment_plot = gr.Plot(
                            label="Sentiment Analysis"
                        )  # chart to show sentiment distribution across models
                else:
                    sentiment_plot = gr.Plot(
                        visible=False
                    )  # hide sentiment plot if sentiment analysis is disabled

                # Connect button — outputs no longer include raw JSON
                generate_btn.click(
                    fn=generate_and_format,  # function to call when button clicked
                    inputs=[prompt_input, max_length_slider, creativity_slider],
                    outputs=[
                        formatted_output,
                        diversity_plot,
                        time_plot,
                        sentiment_plot,
                    ],
                )

            # TAB 2: Charts & Analytics
            # Capture tab object so we can bind a .select() event to it
            with gr.TabItem("Charts & Analytics") as charts_tab:
                gr.Markdown(
                    """
                    ### Historical Charts & Analytics
                    Visualize trends and patterns from your generation history.
                    """
                )

                with gr.Row():
                    trend_plot = gr.Plot(label="Diversity Trend Over Time")  # plot
                    usage_plot = gr.Plot(label="Model Usage Distribution")  # plot

            # TAB 3: View History

            with gr.TabItem("View History"):
                gr.Markdown(
                    """
                    ### Generation History
                    View all your past generations stored in the database.
                    """
                )

                with gr.Row():
                    history_limit = (
                        gr.Slider(  # slider to select how many past records to show
                            minimum=10,
                            maximum=100,
                            value=HISTORY_DEFAULT_LIMIT,
                            step=10,
                            label="Number of records",
                        )
                    )
                    refresh_btn = gr.Button("Refresh", size="lg")

                    # Export button
                    export_btn = gr.Button(
                        "Export to CSV", size="lg", variant="secondary"
                    )

                # Export outputs
                with gr.Row():
                    export_file = gr.File(label="Download CSV", visible=True)
                    export_status = gr.Textbox(label="Export Status", lines=1)

                # gr.HTML renders the styled history cards returned by format_history
                history_output = gr.HTML(
                    label="Past Generations",
                )

                # Connect buttons
                refresh_btn.click(
                    fn=load_history,  # function to call when refresh button clicked
                    inputs=[history_limit],
                    outputs=[history_output],
                )

                export_btn.click(  # function to call when export button clicked
                    fn=export_csv_handler,
                    inputs=[],
                    outputs=[export_file, export_status],
                )

                # Load on page load
                demo.load(  # function to call when page loads
                    fn=load_history,
                    inputs=[history_limit],
                    outputs=[history_output],
                )

            # TAB 4: Statistics
            # Capture tab object so we can bind a .select() event like Charts tab
            with gr.TabItem("Statistics") as stats_tab:
                gr.Markdown(
                    """
                    ### Generation Statistics
                    See overall stats and model performance comparison.
                    """
                )

                # Button kept for manual re-fetch but hidden since auto-load covers the default case
                stats_btn = gr.Button("Refresh Statistics", size="sm", visible=False)
                # gr.HTML renders the styled statistics cards returned by format_statistics
                stats_output = gr.HTML(
                    label="Statistics",
                )

                stats_btn.click(  # function to call when refresh button clicked
                    fn=load_statistics,
                    inputs=[],
                    outputs=[stats_output],
                )

                # Load statistics automatically on page load so no manual refresh is needed
                demo.load(
                    fn=load_statistics,
                    inputs=[],
                    outputs=[stats_output],
                )

                # Danger zone
                gr.Markdown("### Danger Zone")  # section header
                with gr.Row():  # horizontal layout for clear button and status
                    clear_btn = gr.Button("Clear All History", variant="stop")
                    clear_output = gr.Textbox(label="Status", lines=1)

                clear_btn.click(
                    fn=clear_history_handler,
                    inputs=[],
                    outputs=[clear_output],
                )

            # TAB 5: Settings & Info

            with gr.TabItem("Settings & Info"):
                gr.Markdown(
                    """
                    ### Dashboard Settings & Information

                    #### Currently Loaded Models:
                    - **SmolLM3-3B** (HuggingFace 2026) — 3B parameters, good quality on Apple Silicon
                    - **DeepSeek-R1-1.5B** (2025) — 1.5B parameters, reasoning focused
                    - **Qwen2.5-0.5B** (Alibaba 2025) — 0.5B parameters, tiny and fast

                    #### Evaluation Metrics Explained:
                    - **Diversity**: Percentage of unique words (higher = more varied vocabulary)
                    - **Readability Score**: Flesch reading ease (higher = easier to read)
                    - **Grade Level**: US school grade needed to understand the text
                    - **Sentiment**: Whether the text is positive or negative (AI-detected)

                    #### Performance Tips:
                    - Lower max length = faster generation
                    - Higher creativity = more diverse but less coherent output
                    - Qwen2.5-0.5B is the fastest of the three models
                    - MPS (Apple Silicon GPU) is enabled for faster inference

                    #### Configuration:
                    Edit **config.py** to:
                    - Add more models
                    - Enable parallel processing
                    - Change default settings
                    - Disable sentiment analysis (faster)
                    """
                )

        # ── Event bindings outside tab blocks so all variables are in scope ──

        # Charts: load when tab is selected (fixes invisible-plot-in-inactive-tab issue)
        charts_tab.select(
            fn=load_charts,
            inputs=[],
            outputs=[trend_plot, usage_plot],
        )
        # Charts: also load on initial page load
        demo.load(
            fn=load_charts,
            inputs=[],
            outputs=[trend_plot, usage_plot],
        )

        # Statistics: load when tab is selected (same inactive-tab fix as Charts)
        stats_tab.select(
            fn=load_statistics,
            inputs=[],
            outputs=[stats_output],
        )

        # Footer — model names pulled dynamically from MODEL_LIST in config
        gr.Markdown(
            f"""
            ---
            **Models:** {model_summary}
            **Status:** Running locally • Private • Free
            **Features:** Evaluation • Sentiment • Charts • Database • Export
            """
        )

    return demo
