"""
🎨 User Interface
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
    formatted = format_output(results)

    # Generate charts
    diversity_chart = create_diversity_comparison_chart(results)
    time_chart = create_response_time_chart(results)

    # Sentiment chart (if enabled)
    if ENABLE_SENTIMENT:
        sentiment_chart = create_sentiment_distribution_chart(results)
    else:
        sentiment_chart = None

    return formatted, results, diversity_chart, time_chart, sentiment_chart


# refresh button in history tab
def load_history(limit):
    """Load and format generation history"""
    rows = get_generation_history(limit=int(limit))
    return format_history(rows)


# refresh button in statistics tab
def load_statistics():
    """Load and format statistics"""
    stats = get_statistics()
    return format_statistics(stats)


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
    return "🗑️ All history has been cleared!"


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
    # container for the entire app, with custom CSS and theme
    with gr.Blocks(css=CSS_STYLES) as demo:
        # Header
        gr.Markdown(
            """
            # 🤖 AI Text Comparison Dashboard
            ### Compare outputs from 3 local AI models with automatic quality scoring
            
            💡 **Features:** Auto evaluation • Sentiment Analysis • Charts • Database • Export
            """
        )

        # Create tabs
        with gr.Tabs():  # tab container
            # TAB 1: Generate Text

            with gr.TabItem("✨ Generate Text"):  # first tab
                with gr.Row():  # Horizontal layout (side by side)
                    with gr.Column(
                        scale=1
                    ):  # Vertical layout (stacked) , scale=1 means it takes up equal space as the other column
                        # Template dropdown
                        template_dropdown = gr.Dropdown(
                            choices=list(
                                PROMPT_TEMPLATES.keys()
                            ),  # List of template names from config.py
                            label="📋 Quick Templates",  # Label shown
                            value=None,  # default value (none selected)
                            interactive=True,  # user can interact with it
                        )

                        # Input textbox
                        prompt_input = gr.Textbox(
                            label="💭 Your Creative Prompt",
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
                                label="📏 Max Length",
                            )

                            creativity_slider = gr.Slider(
                                minimum=MIN_CREATIVITY,
                                maximum=MAX_CREATIVITY,
                                value=DEFAULT_CREATIVITY,
                                step=0.1,
                                label="🎨 Creativity (Temperature)",
                            )

                        # Generate button
                        generate_btn = gr.Button(
                            "✨ Generate & Evaluate",
                            elem_classes="generate-btn",  # custom CSS class for styling
                            size="lg",  # large button
                        )

                        # Example prompts
                        gr.Markdown("### 📚 Example Prompts:")
                        gr.Examples(
                            examples=EXAMPLE_PROMPTS,  # list of example prompts with settings from config.py``
                            inputs=[
                                prompt_input,
                                max_length_slider,
                                creativity_slider,
                            ],  # connect examples to the input components``
                        )

                # Output section
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📝 Generated Text + Metrics")
                        formatted_output = (
                            gr.Textbox(  # textbox to show formatted output with metrics
                                label="Results",
                                lines=20,
                                elem_id="output_text",
                            )
                        )

                    with gr.Column():
                        gr.Markdown("### 🔍 Raw JSON Data")
                        json_output = gr.JSON(
                            label="Detailed Results"
                        )  # json output for debugging and detailed analysis

                # Charts section
                gr.Markdown("### 📊 Live Comparison Charts")
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

                # Connect button
                generate_btn.click(
                    fn=generate_and_format,  # function to call when button clicked
                    inputs=[prompt_input, max_length_slider, creativity_slider],
                    outputs=[
                        formatted_output,
                        json_output,
                        diversity_plot,
                        time_plot,
                        sentiment_plot,
                    ],
                )

            # TAB 2: 📊 Charts & Analytics

            with gr.TabItem("📊 Charts & Analytics"):
                gr.Markdown(
                    """
                    ### 📊 Historical Charts & Analytics
                    Visualize trends and patterns from your generation history.
                    """
                )

                refresh_charts_btn = gr.Button(
                    "🔄 Refresh Charts", size="lg"
                )  # refresh button

                with gr.Row():
                    trend_plot = gr.Plot(label="📈 Diversity Trend Over Time")  # plot
                    usage_plot = gr.Plot(label="🥧 Model Usage Distribution")  # plot

                refresh_charts_btn.click(
                    fn=load_charts,  # function to call when button clicked
                    inputs=[],
                    outputs=[trend_plot, usage_plot],  # update the charts with new data
                )

                # Load on page load
                demo.load(
                    fn=load_charts,  # function to call when page loads
                    inputs=[],
                    outputs=[trend_plot, usage_plot],  # update the charts with new data
                )

            # TAB 3: View History

            with gr.TabItem("📜 View History"):
                gr.Markdown(
                    """
                    ### 📜 Generation History
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
                            label="📊 Number of records",
                        )
                    )
                    refresh_btn = gr.Button("🔄 Refresh", size="lg")

                    # Export button
                    export_btn = gr.Button(
                        "📥 Export to CSV", size="lg", variant="secondary"
                    )

                # Export outputs
                with gr.Row():
                    export_file = gr.File(label="Download CSV", visible=True)
                    export_status = gr.Textbox(label="Export Status", lines=1)

                history_output = gr.Textbox(  # textbox to show formatted history
                    label="Past Generations",
                    lines=25,
                    elem_id="output_text",
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

            with gr.TabItem("📈 Statistics"):
                gr.Markdown(
                    """
                    ### 📈 Generation Statistics
                    See overall stats and model performance comparison.
                    """
                )

                stats_btn = gr.Button("🔄 Refresh Statistics", size="lg")
                stats_output = gr.Textbox(  # textbox to show formatted statistics
                    label="Statistics",
                    lines=20,
                    elem_id="output_text",
                )

                stats_btn.click(  # function to call when refresh button clicked
                    fn=load_statistics,
                    inputs=[],
                    outputs=[stats_output],
                )

                # Danger zone
                gr.Markdown("### ⚠️ Danger Zone")  # section header
                with gr.Row():  # horizontal layout for clear button and status
                    clear_btn = gr.Button("🗑️ Clear All History", variant="stop")
                    clear_output = gr.Textbox(label="Status", lines=1)

                clear_btn.click(
                    fn=clear_history_handler,
                    inputs=[],
                    outputs=[clear_output],
                )

            # TAB 5: Settings & Info

            with gr.TabItem("⚙️ Settings & Info"):
                gr.Markdown(
                    """
                    ### ⚙️ Dashboard Settings & Information
                    
                    #### 🤖 Currently Loaded Models:
                    - **DistilGPT-2** (82M parameters) - Fastest, good for quick tests
                    - **GPT-2 Standard** (124M parameters) - Balanced speed/quality
                    - **GPT-2 Medium** (355M parameters) - Best quality, slower
                    
                    #### 📊 Evaluation Metrics Explained:
                    - **Diversity**: Percentage of unique words (higher = more varied vocabulary)
                    - **Readability Score**: Flesch reading ease (higher = easier to read)
                    - **Grade Level**: US school grade needed to understand the text
                    - **Sentiment**: Whether the text is positive or negative (AI-detected)
                    
                    #### ⚡ Performance Tips:
                    - Lower max length = faster generation
                    - Higher creativity = more diverse but less coherent output
                    - DistilGPT-2 is ~3x faster than GPT-2 Medium
                    
                    #### 🔧 Configuration:
                    Edit `config.py` to:
                    - Add more models
                    - Enable parallel processing
                    - Change default settings
                    - Disable sentiment analysis (faster)
                    """
                )

        # Footer
        gr.Markdown(
            """
            ---
            **Models:** DistilGPT-2 (82M) • GPT-2 (124M) • GPT-2 Medium (355M)  
            **Status:** 🟢 Running locally • 🔒 Private • 💰 Free  
            **Features:** ⭐ Evaluation • 😊 Sentiment • 📊 Charts • 💾 Database • 📥 Export
            """
        )

    return demo
