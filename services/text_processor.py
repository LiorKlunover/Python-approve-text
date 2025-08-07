"""
Text processing service for the Text Improver Pro application.

This module provides functionality for improving and shortening text
using the Google Gemini API and OpenRouter API with various LLM models.
"""

import google.generativeai as genai
from openai import OpenAI
import os

# Try to load environment variables if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not available, we'll use hardcoded values or environment variables
    pass

# Configuration - use environment variables or fallback to defaults
API_KEY = os.environ.get("API_KEY", "your_api_key_here")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "your_google_api_key_here")
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "gemini-2.5-flash-preview-05-20")

# Initialize the OpenAI client with OpenRouter base URL (for backup)
openrouter_client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "https://text-improver-pro.app",  # Site URL for rankings
        "X-Title": "Text Improver Pro"  # Site title for rankings
    }
)

# Initialize the Google Generative AI client
genai.configure(api_key=GOOGLE_API_KEY)


def answer_interview_question(question, model=DEFAULT_MODEL):
    """
    Generate a well-structured, human-like response to an interview question.
    
    This function processes interview questions and returns professionally crafted
    answers that sound natural and conversational, using the specified LLM model.
    
    Args:
        question: The interview question to answer
        model: The model to use (default)
        
    Returns:
        A well-structured answer to the interview question, or an error message if something went wrong
    """
    try:
        # Check if using Gemini model
        if "gemini" in model.lower():
            # Create a Gemini model instance
            gemini_model = genai.GenerativeModel(model)
            
            # Create system prompt and user message
            system_prompt = "You are a helpful assistant that answers interview questions. "\
                           "Provide a short and precise answer without any introductory phrases. "\
                           "Be concise and get straight to the point. "\
                           "Limit your response to 4-7 sentences when possible. "\
                           "Start your response directly with the answer."
            
            # Generate response using Gemini
            chat = gemini_model.start_chat(history=[])
            response = chat.send_message(
                f"{system_prompt}\n\nPlease answer this question: {question}"
            )
            
            # Return the response text
            return response.text
        else:
            # Fallback to OpenRouter for non-Gemini models
            response = openrouter_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers interview questions. "
                                   "Provide a short and precise answer without any introductory phrases. "
                                   "Be concise and get straight to the point. "
                                   "Limit your response to 4-7 sentences when possible. "
                                   "Start your response directly with the answer."
                    },
                    {
                        "role": "user",
                        "content": f"Please answer this question: {question}"
                    }
                ]
            )
            
            # Validate response
            return _extract_content_from_response(response)
    except Exception as e:
        return _handle_api_error(e)



def improve_text(text, model=DEFAULT_MODEL):
    """
    Improve and shorten the provided text using the specified LLM model.
    
    Args:
        text: The text to improve
        model: The model to use (default)
        
    Returns:
        The improved text, or an error message if something went wrong
    """
    try:
        # Check if using Gemini model
        if "gemini" in model.lower():
            # Create a Gemini model instance
            gemini_model = genai.GenerativeModel(model)
            
            # Create system prompt and user message
            system_prompt = "You are a helpful assistant that improves and shortens text. "\
                           "Provide only the improved text without any introductory phrases like "\
                           "'Here\'s the improved and shortened text:' or similar. "\
                           "Start your response directly with the improved content."
            
            # Generate response using Gemini
            chat = gemini_model.start_chat(history=[])
            response = chat.send_message(
                f"{system_prompt}\n\nPlease improve and shorten this text while preserving its meaning: {text}"
            )
            
            # Return the response text
            return response.text
        else:
            # Fallback to OpenRouter for non-Gemini models
            response = openrouter_client.chat.completions.create(
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
                ]
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
    """Extract content from API response."""
    try:
        # For OpenRouter responses
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error extracting content from response: {e}")
        return "Error processing response from API."

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
