"""
Styles module for the Text Improver Pro application.

This module contains all the color schemes, font definitions, and styling constants
used throughout the application to maintain a consistent look and feel.
"""

# Colors for modern look with a gradient palette
COLORS = {
    # Primary colors
    "primary": "#6366f1",  # Indigo 500
    "primary_light": "#818cf8",  # Indigo 400
    "primary_dark": "#4f46e5",  # Indigo 600
    "primary_hover": "#4338ca",  # Indigo 700 - for hover effects
    
    # Secondary colors
    "secondary": "#f8fafc",  # Slate 50
    "secondary_hover": "#e2e8f0",  # Slate 200 - for hover effects
    
    # Text colors
    "text": "#1e293b",  # Slate 800
    "text_light": "#64748b",  # Slate 500
    "text_dark": "#0f172a",  # Slate 900
    
    # Background colors
    "background": "#ffffff",  # White
    "background_gradient_start": "#f1f5f9",  # Slate 100
    "background_gradient_end": "#ffffff",  # White
    
    # Border and separator colors
    "border": "#e2e8f0",  # Slate 200
    "border_light": "#f1f5f9",  # Slate 100
    "border_dark": "#cbd5e1",  # Slate 300
    
    # Status colors
    "success": "#10b981",  # Emerald 500
    "success_hover": "#059669",  # Emerald 600 - for hover effects
    "warning": "#f59e0b",  # Amber 500
    "warning_hover": "#d97706",  # Amber 600 - for hover effects
    "error": "#ef4444",  # Red 500
    "error_hover": "#dc2626",  # Red 600 - for hover effects
    
    # Accent colors
    "accent": "#8b5cf6",  # Violet 500
    "accent_hover": "#7c3aed",  # Violet 600 - for hover effects
    
    # Special effects
    "shadow": "#94a3b8",  # Slate 400 - for shadow effects
    "shadow_light": "#cbd5e1",  # Slate 300 - for lighter shadow effects
    "glass": "rgba(255, 255, 255, 0.8)",  # Semi-transparent white for glass effects
}

# Font definitions
FONTS = {
    "title": {
        "family": "Segoe UI",
        "size": 14,
        "weight": "bold"
    },
    "header": {
        "family": "Segoe UI",
        "size": 11,
        "weight": "bold"
    },
    "text": {
        "family": "Segoe UI",
        "size": 10,
        "weight": "normal"
    },
    "button": {
        "family": "Segoe UI",
        "size": 10,
        "weight": "bold"
    },
    "small": {
        "family": "Segoe UI",
        "size": 8,
        "weight": "normal"
    },
    "icon": {
        "family": "Segoe UI",
        "size": 16,
        "weight": "normal"
    }
}

# UI dimensions and measurements
DIMENSIONS = {
    "corner_radius": 16,  # Default corner radius for rounded elements
    "ctk_default_radius": 16,
    "button_radius": 20,  # Corner radius for buttons
    "shadow_padding": 20,  # Padding for shadow effects
    "content_padding": 15,  # Default padding for content areas
    "button_padding_x": 20,  # Horizontal padding for buttons
    "button_padding_y": 10,  # Vertical padding for buttons
    "header_height": 50,  # Height of the header bar
    "window_width": 420,  # Default window width
    "window_height": 650,  # Default window height
}

# Animation timing constants
ANIMATION = {
    "fade_step": 0.1,  # Alpha increment for fade animations
    "fade_delay": 20,  # Milliseconds between fade steps
    "typewriter_delay": 10,  # Milliseconds between characters in typewriter effect
    "button_animation_steps": 10,  # Number of steps in button animations
    "button_animation_delay": 100,  # Milliseconds between button animation steps
}
