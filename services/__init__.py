"""
Services package for the Text Improver Pro application.

This package contains service modules that handle core functionality
such as text processing and clipboard monitoring.
"""

# Import key functions for easier access
from .text_processor import improve_text, improve_text_with_style, get_available_models
from .clipboard_monitor import ClipboardMonitor
