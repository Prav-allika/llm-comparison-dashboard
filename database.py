"""
Database Functions
Handles all database operations - save, load, delete
Enhanced with sentiment and timing tracking!
"""

import sqlite3  # to create or manage the database
from datetime import datetime  # to timestamp generations
from config import DATABASE_NAME  # keep the database name in config for easy changes


def init_database():
    """
    Create database and table if they don't exist
    Now includes sentiment and response time tracking!
    """
    # connect is used to create a new database
    conn = sqlite3.connect(DATABASE_NAME)
    # start a cursor to execute SQL commands
    c = conn.cursor()

    # Create table with all columns (including new ones!)
    c.execute("""CREATE TABLE IF NOT EXISTS generations
                 (id INTEGER PRIMARY KEY, 
                  timestamp TEXT, 
                  prompt TEXT, 
                  model TEXT, 
                  response TEXT, 
                  temperature REAL, 
                  max_length INTEGER,
                  word_count INTEGER,
                  diversity REAL,
                  readability_score REAL,
                  grade_level REAL,
                  sentiment_label TEXT,
                  sentiment_score REAL,
                  response_time REAL)""")

    # Check if new columns exist, add them if not (for existing databases)
    try:
        c.execute("SELECT sentiment_label FROM generations LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE generations ADD COLUMN sentiment_label TEXT")
        c.execute("ALTER TABLE generations ADD COLUMN sentiment_score REAL")
        print("Added sentiment columns to database")

    try:
        c.execute("SELECT response_time FROM generations LIMIT 1")
    except sqlite3.OperationalError:
        c.execute(" ALTER TABLE generations ADD COLUMN response_time REAL")
        print(" Added response_time column to database")

    # commit confirm the changes
    conn.commit()
    # close the connection
    conn.close()
    print(" Database initialized!")


def save_generation(
    prompt,
    model,
    response,
    temperature,
    max_length,
    metrics,
    sentiment=None,
    response_time=None,
):
    """
    Save a single generation to the database

    Parameters:
    - prompt: What the user typed
    - model: Which AI model was used
    - response: What the AI generated
    - temperature: Creativity setting
    - max_length: Maximum length setting
    - metrics: Dictionary with word_count, diversity, etc.
    - sentiment: Dictionary with label and score (optional)
    - response_time: Time taken to generate in seconds (optional)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Extract sentiment if provided
    sentiment_label = sentiment.get("label") if sentiment else None
    sentiment_score = sentiment.get("score") if sentiment else None

    c.execute(
        """INSERT INTO generations 
                 (timestamp, prompt, model, response, temperature, max_length, 
                  word_count, diversity, readability_score, grade_level,
                  sentiment_label, sentiment_score, response_time)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            # create a timestamp in string format for better sorting and readability
            datetime.now().isoformat(),
            prompt,
            model,
            response,
            temperature,
            max_length,
            metrics["word_count"],
            metrics["diversity"],
            metrics["readability_score"],
            metrics["grade_level"],
            sentiment_label,
            sentiment_score,
            response_time,
        ),
    )

    conn.commit()
    conn.close()
    print(f"💾 Saved {model} generation to database")


def get_generation_history(limit=50):
    """
    Retrieve past generations from database (enhanced!)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute(
        """SELECT timestamp, prompt, model, response, temperature, 
                        max_length, word_count, diversity, 
                        sentiment_label, sentiment_score, response_time
                 FROM generations 
                 ORDER BY timestamp DESC 
                 LIMIT ?""",
        (limit,),
    )
    # fetchall retrieves all the rows returned by the query and stores them in a list of tuples
    rows = c.fetchall()
    conn.close()
    return rows


def get_chart_data(limit=100):
    """
    Get data optimized for charts

    Returns:
    - List of tuples: (timestamp, model, diversity, sentiment_label, response_time)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute(
        """SELECT timestamp, model, diversity, sentiment_label, response_time
                 FROM generations 
                 ORDER BY timestamp DESC 
                 LIMIT ?""",
        (limit,),
    )

    rows = c.fetchall()
    conn.close()
    return rows


def get_statistics():
    """
    Get overall statistics from the database (enhanced!)
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    # Total generations
    c.execute("SELECT COUNT(*) FROM generations")
    total_count = c.fetchone()[0]

    # Average diversity by model
    c.execute("""SELECT model, AVG(diversity), COUNT(*), AVG(response_time)
                 FROM generations 
                 GROUP BY model""")
    model_stats = c.fetchall()

    # Sentiment distribution
    c.execute("""SELECT sentiment_label, COUNT(*) 
                 FROM generations 
                 WHERE sentiment_label IS NOT NULL
                 GROUP BY sentiment_label""")
    sentiment_stats = c.fetchall()

    # Average response time
    c.execute(
        "SELECT AVG(response_time) FROM generations WHERE response_time IS NOT NULL"
    )
    avg_response_time = c.fetchone()[0]

    conn.close()

    return {
        "total_generations": total_count,
        "model_stats": model_stats,
        "sentiment_stats": sentiment_stats,
        "avg_response_time": avg_response_time,
    }


def get_export_data():
    """
    Get all data for CSV export
    """
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()

    c.execute("""SELECT id, timestamp, prompt, model, response, temperature, 
                        max_length, word_count, diversity, readability_score, 
                        grade_level, sentiment_label, sentiment_score, response_time
                 FROM generations 
                 ORDER BY timestamp DESC""")

    rows = c.fetchall()
    columns = [
        "id",
        "timestamp",
        "prompt",
        "model",
        "response",
        "temperature",
        "max_length",
        "word_count",
        "diversity",
        "readability_score",
        "grade_level",
        "sentiment_label",
        "sentiment_score",
        "response_time",
    ]

    conn.close()
    return columns, rows


def delete_generation(generation_id):
    """Delete a specific generation by ID"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM generations WHERE id = ?", (generation_id,))
    conn.commit()
    conn.close()
    print(f"c Deleted generation #{generation_id}")


def clear_all_history():
    """Delete ALL generations from database"""
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM generations")
    conn.commit()
    conn.close()
    print(" All history cleared!")
