"""
Image utilities module for the Text Improver Pro application.

This module contains functions for creating visual effects like drop shadows,
gradient backgrounds, and rounded rectangles for UI elements.
"""

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from ui.styles import DIMENSIONS

def create_drop_shadow(root, colors):
    """
    Create a subtle drop shadow effect around the main window.
    
    Args:
        root: The root Tkinter window
        colors: The color dictionary
    """
    # Create shadow frames around the main window
    shadow_color = colors["shadow"]
    shadow_alpha = 30  # Shadow transparency (0-255)
    
    # Create shadow frames with decreasing opacity
    for i in range(1, 6):  # 5 layers of shadow
        shadow_frame = tk.Frame(
            root,
            bg=shadow_color,
            bd=0,
            highlightthickness=0
        )
        # Set transparency based on distance from main frame
        opacity = shadow_alpha - (i * 5)
        if opacity < 0:
            opacity = 0
        # Position the shadow frame
        offset = i
        shadow_frame.place(x=offset, y=offset, relwidth=1, relheight=1, width=-offset*2, height=-offset*2)
        # Lower the shadow frame below other elements
        shadow_frame.lower()

def create_gradient_background(root, colors):
    """
    Create a gradient background with rounded corners for the window.
    
    Args:
        root: The root Tkinter window
        colors: The color dictionary
    """
    try:
        # Get window dimensions
        width = root.winfo_width()
        height = root.winfo_height()
        
        if width <= 1 or height <= 1:  # Window not yet sized
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            
            # If still no size, use default dimensions
            if width <= 1 or height <= 1:
                width = DIMENSIONS["window_width"]
                height = DIMENSIONS["window_height"]
        
        # Create a rounded rectangle image with gradient
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw the gradient background
        for y in range(height):
            # Calculate color based on position with easing function
            ratio = y / height
            # Apply easing function for smoother gradient
            eased_ratio = 1 - (1 - ratio) ** 2  # Quadratic ease-out
            
            # Get colors from hex to RGB
            start_r, start_g, start_b = int(colors["background_gradient_start"][1:3], 16), \
                                       int(colors["background_gradient_start"][3:5], 16), \
                                       int(colors["background_gradient_start"][5:7], 16)
            end_r, end_g, end_b = int(colors["background_gradient_end"][1:3], 16), \
                                 int(colors["background_gradient_end"][3:5], 16), \
                                 int(colors["background_gradient_end"][5:7], 16)
            
            # Interpolate between colors
            r = int(start_r + (end_r - start_r) * eased_ratio)
            g = int(start_g + (end_g - start_g) * eased_ratio)
            b = int(start_b + (end_b - start_b) * eased_ratio)
            
            # Draw a line of the gradient
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
            
    except Exception as e:
        print(f"Error creating gradient background: {e}")

def create_rounded_rectangle(width, height, radius, fill_color):
    """
    Create a rounded rectangle image for UI elements.
    
    Args:
        width: Width of the rectangle
        height: Height of the rectangle
        radius: Corner radius
        fill_color: Fill color (hex string)
        
    Returns:
        PIL Image object with the rounded rectangle
    """
    try:
        # Convert hex color to RGB
        r, g, b = int(fill_color[1:3], 16), int(fill_color[3:5], 16), int(fill_color[5:7], 16)
        
        # Create a new image with desired size
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw the rounded rectangle
        draw.rectangle(
            [(radius, 0), (width-radius, height)],
            fill=(r, g, b, 255)
        )
        draw.rectangle(
            [(0, radius), (width, height-radius)],
            fill=(r, g, b, 255)
        )
        
        # Draw the corner circles
        draw.ellipse([(0, 0), (2*radius, 2*radius)], fill=(r, g, b, 255))
        draw.ellipse([(width-2*radius, 0), (width, 2*radius)], fill=(r, g, b, 255))
        draw.ellipse([(0, height-2*radius), (2*radius, height)], fill=(r, g, b, 255))
        draw.ellipse([(width-2*radius, height-2*radius), (width, height)], fill=(r, g, b, 255))
        
        return image
    except Exception as e:
        print(f"Error creating rounded rectangle: {e}")
        return None

def create_rounded_button_image(width, height, radius, fill_color, hover=False):
    """
    Create a rounded button image with optional hover effect.
    
    Args:
        width: Width of the button
        height: Height of the button
        radius: Corner radius
        fill_color: Fill color (hex string)
        hover: Whether to create a hover effect
        
    Returns:
        PhotoImage object for use with Tkinter
    """
    try:
        # Create the rounded rectangle
        image = create_rounded_rectangle(width, height, radius, fill_color)
        
        # Add hover effect if requested
        if hover and image:
            draw = ImageDraw.Draw(image)
            # Add a subtle highlight at the top
            for i in range(height // 3):
                alpha = 50 - (i * 50 // (height // 3))
                draw.line([(radius, i), (width-radius, i)], fill=(255, 255, 255, alpha))
        
        # Convert to PhotoImage for Tkinter
        if image:
            return ImageTk.PhotoImage(image)
        return None
    except Exception as e:
        print(f"Error creating button image: {e}")
        return None

def apply_transparency_to_image(image, alpha):
    """
    Apply transparency to an image.
    
    Args:
        image: PIL Image object
        alpha: Alpha value (0-255)
        
    Returns:
        PIL Image with transparency applied
    """
    try:
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        data = image.getdata()
        new_data = []
        
        for item in data:
            # Apply the new alpha, keeping the RGB values
            new_data.append((item[0], item[1], item[2], min(item[3], alpha) if len(item) > 3 else alpha))
        
        image.putdata(new_data)
        return image
    except Exception as e:
        print(f"Error applying transparency: {e}")
        return image
