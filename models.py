"""
AI Model Functions
Loading models and generating text
Enhanced with per-model timing and optional parallel processing!
"""

# measure elapsed time for loading and generation
import time
import warnings

# ThreadPoolExecutor for parallel generation, as_completed to collect results as they finish
from concurrent.futures import ThreadPoolExecutor, as_completed

# transformers pipeline for text generation
from transformers import pipeline

# Config settings for models and generation
from config import MODEL_LIST, ENABLE_PARALLEL, MAX_WORKERS, DEVICE, ENABLE_SENTIMENT

# Evaluation functions for text quality and sentiment
from evaluation import evaluate_text, get_best_model, analyze_sentiment
from database import save_generation

import torch

if torch.backends.mps.is_available():
    torch.mps.empty_cache()

warnings.filterwarnings("ignore")

# Global variable to store loaded models
loaded_models = {}


def get_device():
    """
    Detect the best available device for model inference.
    Validates the configured DEVICE is actually available before using it.
    """
    try:
        import torch

        if DEVICE == "cuda":
            if torch.cuda.is_available():
                print(" CUDA GPU detected!")
                return "cuda"
            print(" CUDA not available, falling back to CPU")
            return "cpu"

        if DEVICE == "mps":
            if torch.backends.mps.is_available():
                print(" Apple Silicon GPU (MPS) detected!")
                return "mps"
            print(" MPS not available, falling back to CPU")
            return "cpu"

        if DEVICE == "cpu":
            return "cpu"

        # auto-detect
        if torch.cuda.is_available():
            print(" CUDA GPU detected!")
            return "cuda"
        elif torch.backends.mps.is_available():
            print(" Apple Silicon GPU (MPS) detected!")
            return "mps"
        else:
            print(" Using CPU")
            return "cpu"
    except Exception:
        print(" Using CPU (torch not fully available)")
        return "cpu"


def load_all_models():
    """
    Load all AI models defined in config
    Now with device detection!
    """
    global loaded_models

    print(" Loading AI Models...")

    device = get_device()

    for display_name, model_name in MODEL_LIST.items():
        print(f" Loading {display_name}...")
        start_time = time.time()

        try:
            import torch

            dtype = torch.float16 if device in ("mps", "cuda") else torch.float32
            loaded_models[display_name] = pipeline(
                "text-generation",
                model=model_name,
                device=device,
                torch_dtype=dtype,
                low_cpu_mem_usage=True,
            )
            elapsed = time.time() - start_time  # elapsed time for loading this model
            print(f" {display_name} loaded in {elapsed:.2f}s!")
        except Exception as e:
            print(f" Failed to load {display_name}: {e}")

    print(f"\n Loaded {len(loaded_models)} models successfully!\n")
    return loaded_models


def generate_single(model_name, prompt, max_length, creativity):
    """
    Generate text from a single model with timing

    Parameters:
    - model_name: Which model to use
    - prompt: The text to continue
    - max_length: Maximum output length
    - creativity: Temperature setting (0.3-1.0)

    Returns:
    - Dictionary with response, metrics, status, and timing
    """
    if model_name not in loaded_models:
        return {
            "response": "Model not loaded!",
            "status": "Error",
            "generation_time": 0,
        }

    generator = loaded_models[model_name]

    # Track generation time per model
    start_time = time.time()

    try:
        output = generator(
            prompt,
            max_new_tokens=max_length,  # use max_new_tokens instead of max_length to avoid truncating the prompt
            num_return_sequences=1,  # only generate one response per model for comparison
            do_sample=True,  # enable sampling for more creative outputs
            temperature=creativity,  # from config.py, controls randomness (0.3 = more focused, 1.0 = more creative)
            top_p=0.92,  # nucleus sampling for better quality (top_p=0.92 means only consider the top 92% of probability mass)
            repetition_penalty=1.2,  # penalize repeating the same words/phrases (1.0 = no penalty, >1.0 = more penalty)
            no_repeat_ngram_size=3,  # prevent repeating the same 3-word sequences for more diverse output
            truncation=True,  # truncate inputs that are too long for the model
            pad_token_id=generator.tokenizer.eos_token_id,  # some models require a pad token, use EOS token as fallback
            max_length=None,
        )

        response_text = output[0][
            "generated_text"
        ]  # extract the generated text from the output
        generation_time = time.time() - start_time

        # Evaluate text quality
        metrics = evaluate_text(
            response_text
        )  # word count, diversity, readability, etc.

        # Analyze sentiment (if enabled)
        sentiment = None
        if (
            ENABLE_SENTIMENT
        ):  # only analyze sentiment if the feature is enabled in config
            sentiment = analyze_sentiment(
                response_text
            )  # label (POSITIVE/NEGATIVE) and confidence score (0-1)

        # Return all results in a structured format
        return {
            "response": response_text,
            "metrics": metrics,
            "sentiment": sentiment,
            "status": "Successfully generated",
            "generation_time": round(generation_time, 3),
        }

    except Exception as e:
        generation_time = time.time() - start_time
        return {
            "response": str(e),
            "status": "Error while generating",
            "generation_time": round(generation_time, 3),
        }


def generate_parallel(prompt, max_length, creativity):
    """
    Generate from all models in PARALLEL (faster!)
    Uses ThreadPoolExecutor for concurrent execution

    Uses more memory - enable only if you have 8GB+ RAM
    """
    results = {}
    start_time = time.time()

    print("⚡ Running parallel generation...")
    # create a thread pool with the specified number of workers and submit generation tasks for all models
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_model = {
            # start a generation task for each model and map the future to the model name for later reference
            executor.submit(
                generate_single, name, prompt, max_length, creativity
            ): name  # map each future to its model name for later reference
            for name in loaded_models.keys()  # submit a generation task for each loaded model
        }

        # Collect results as they complete
        for future in as_completed(
            future_to_model
        ):  # as each generation task completes, get the corresponding model name from the mapping
            model_name = future_to_model[
                future
            ]  # get the model name associated with this completed future
            try:
                result = future.result()  # get the result of the generation task (response, metrics, sentiment, status, timing)
                results[model_name] = (
                    result  # store the result in the results dictionary under the model's name
                )

                if result["status"] == "Successfully generated":
                    print(
                        f" {model_name}: {result['generation_time']}s, Diversity: {result['metrics']['diversity']}%"
                    )

                    # Save to database
                    save_generation(
                        prompt,
                        model_name,
                        result["response"],
                        creativity,
                        max_length,
                        result["metrics"],
                        result.get("sentiment"),
                        result.get("generation_time"),
                    )
                else:
                    print(f" {model_name} failed")

            except Exception as e:
                print(f" {model_name} error: {e}")
                results[model_name] = {
                    "response": str(e),
                    "status": "Error",
                    "generation_time": 0,
                }

    total_time = time.time() - start_time
    return results, total_time


def generate_sequential(prompt, max_length, creativity):
    """
    Generate from all models SEQUENTIALLY (one by one)
    Uses less memory, more reliable
    """
    results = {}
    start_time = time.time()

    print(" Running sequential generation...")
    # loop through each loaded model and generate text one by one, collecting results and timing for each
    for name in loaded_models.keys():
        print(f" Generating with {name}...")
        # Generate text and collect metrics, sentiment, and timing for this model
        result = generate_single(name, prompt, max_length, creativity)
        # Store the result in the results dictionary under the model's name
        results[name] = result
        # print the generation time and diversity score for this model if generation was successful
        if result["status"] == "Successfully generated":
            print(
                f" {name}: {result['generation_time']}s, Diversity: {result['metrics']['diversity']}%"
            )

            # Save to database
            save_generation(
                prompt,
                name,
                result["response"],
                creativity,
                max_length,
                result["metrics"],
                result.get("sentiment"),
                result.get("generation_time"),
            )
        else:
            print(f" {name} failed: {result['response']}")
    # total time for generating from all models sequentially is the difference between the current time and the start time
    total_time = time.time() - start_time
    return results, total_time


def generate_from_all(prompt, max_length, creativity):
    """
    Generate text from ALL models and compare
    Automatically chooses parallel or sequential based on config

    Parameters:
    - prompt: The text to continue
    - max_length: Maximum output length
    - creativity: Temperature setting

    Returns:
    - Dictionary with all results, stats, and recommendation
    """
    # Choose generation method
    if ENABLE_PARALLEL:
        results, total_time = generate_parallel(prompt, max_length, creativity)
    else:
        results, total_time = generate_sequential(prompt, max_length, creativity)

    # Add generation stats
    results["Generation Stats"] = {
        "elapsed_time": f"{total_time:.2f} seconds",
        "average_time_per_model": f"{total_time / len(loaded_models):.2f} seconds",
        "mode": "Parallel" if ENABLE_PARALLEL else "Sequential",
    }

    # Pick best model based on diversity
    best_model, best_diversity = get_best_model(results)
    if best_model:
        # Find fastest model too
        fastest_model = None
        fastest_time = float("inf")
        # loop through results to find the model with the fastest generation time among successful generations
        for name, data in results.items():
            # Skip non-model entries like "Generation Stats" and "Recommendation"
            if name not in ["Generation Stats", "Recommendation"]:
                # Only consider models that successfully generated text
                if data.get("generation_time", float("inf")) < fastest_time:
                    fastest_time = data.get(
                        "generation_time", float("inf")
                    )  # update fastest_time if this model's generation time is faster than the current fastest_time
                    fastest_model = name

        results["Recommendation"] = {
            "best_model": best_model,
            "reason": f"Highest diversity ({best_diversity}%)",
            "fastest_model": fastest_model,
            "fastest_time": f"{fastest_time:.2f}s" if fastest_model else "N/A",
        }

    return results
