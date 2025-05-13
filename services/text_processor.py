"""
Text processing service for the Text Improver Pro application.

This module provides functionality for improving and shortening text
using the OpenRouter API with various LLM models.
"""

from openai import OpenAI
import os
import json
import time

# Configuration
API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-3-haiku:beta"  # Default to a reliable model

# Initialize the OpenAI client with OpenRouter base URL
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

def improve_text(text, model=DEFAULT_MODEL):
    """
    Improve and shorten the provided text using the specified LLM model.
    
    Args:
        text: The text to improve
        model: The model to use (default: anthropic/claude-3-haiku:beta)
        
    Returns:
        The improved text, or an error message if something went wrong
    """
    try:
        # Create completion with the model
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that improves and shortens text. "
                               "Provide only the improved text without any introductory phrases like "
                               "'Here\'s the improved and shortened text:' or similar. "
                               "Start your response directly with the improved content."
                },
                {
                    "role": "user",
                    "content": f"Please improve and shorten this text while preserving its meaning: {text}"
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://text-improver-app.com",
                "X-Title": "Text Improver Pro"
            }
        )
        
        # Validate response
        return _extract_content_from_response(response)
    except Exception as e:
        return _handle_api_error(e)

def improve_text_with_style(text, style="professional", model=DEFAULT_MODEL):
    """
    Improve text with a specific style.
    
    Args:
        text: The text to improve
        style: The style to apply (professional, casual, academic, creative)
        model: The model to use
        
    Returns:
        The improved text with the specified style
    """
    style_prompts = {
        "professional": "Improve and shorten this text to make it clear, concise, and professional.",
        "casual": "Improve and shorten this text to make it friendly, conversational, and easy to read.",
        "academic": "Improve and shorten this text to make it formal, precise, and suitable for academic context.",
        "creative": "Improve and shorten this text to make it engaging, vivid, and creative."
    }
    
    # Use the default prompt if the style is not recognized
    prompt = style_prompts.get(style.lower(), style_prompts["professional"])
    
    try:
        # Create completion with the model
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that improves and shortens text. "
                               "Provide only the improved text without any introductory phrases. "
                               "Start your response directly with the improved content."
                },
                {
                    "role": "user",
                    "content": f"{prompt} Text: {text}"
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://text-improver-app.com",
                "X-Title": "Text Improver Pro"
            }
        )
        
        # Validate response
        return _extract_content_from_response(response)
    except Exception as e:
        return _handle_api_error(e)

def _extract_content_from_response(response):
    """
    Extract the content from the API response with proper validation.
    
    Args:
        response: The API response object
        
    Returns:
        The extracted content or an error message
    """
    # Validate response structure
    if not response or not hasattr(response, 'choices') or not response.choices:
        return "Error: No valid response received from the API"
        
    if not response.choices[0] or not hasattr(response.choices[0], 'message'):
        return "Error: Response format unexpected - no message in first choice"
        
    if not response.choices[0].message or not hasattr(response.choices[0].message, 'content'):
        return "Error: Response format unexpected - no content in message"
        
    # Return the improved text
    return response.choices[0].message.content

def _handle_api_error(error):
    """
    Handle API errors with informative messages.
    
    Args:
        error: The exception object
        
    Returns:
        A user-friendly error message
    """
    error_str = str(error)
    
    # Check for common error types and provide helpful messages
    if "rate limit" in error_str.lower():
        return "Error: Rate limit exceeded. Please try again in a moment."
    elif "authentication" in error_str.lower() or "api key" in error_str.lower():
        return "Error: Authentication failed. Please check your API key."
    elif "timeout" in error_str.lower() or "timed out" in error_str.lower():
        return "Error: Request timed out. The server might be busy, please try again."
    elif "connection" in error_str.lower():
        return "Error: Connection issue. Please check your internet connection."
    else:
        # Generic error message with the actual error for debugging
        return f"Error: {error_str}"

def get_available_models():
    """
    Get a list of available models from OpenRouter.
    
    Returns:
        A list of available model IDs, or an empty list if the request fails
    """
    try:
        # This endpoint might vary depending on OpenRouter's API
        response = client.models.list()
        
        # Extract model IDs
        models = [model.id for model in response.data]
        return models
    except Exception as e:
        print(f"Error fetching models: {e}")
        # Return a default list of known models
        return [
            "anthropic/claude-3-haiku:beta",
            "anthropic/claude-3-opus:beta",
            "anthropic/claude-3-sonnet:beta",
            "openai/gpt-4",
            "openai/gpt-4-turbo",
            "openai/gpt-3.5-turbo"
        ]
