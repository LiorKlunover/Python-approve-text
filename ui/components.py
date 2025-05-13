"""
Components module for the Text Improver Pro application.

This module contains reusable UI components like rounded buttons,
headers with drag functionality, and other custom UI elements.
"""

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
from ui.styles import DIMENSIONS

def create_rounded_button(parent, text, command, colors, fonts, is_secondary=False, width=None, height=None):
    """
    Create a button with rounded corners and hover effects.
    
    Args:
        parent: The parent widget
        text: The button text
        command: The function to call when the button is clicked
        colors: The color dictionary
        fonts: The font dictionary
        is_secondary: Whether this is a secondary button (different styling)
        width: Optional custom width
        height: Optional custom height
        
    Returns:
        The button widget
    """
    # Determine button style based on type
    if is_secondary:
        bg_color = colors["secondary"]
        fg_color = colors["text"]
        hover_bg = colors["secondary_hover"]
        hover_fg = colors["text_dark"]
        active_bg = colors["border"]
        active_fg = colors["text_dark"]
    else:
        bg_color = colors["primary"]
        fg_color = "white"
        hover_bg = colors["primary_hover"]
        hover_fg = "white"
        active_bg = colors["primary_dark"]
        active_fg = "white"
    
    # Create the button with modern styling
    button = ctk.CTkButton(
        parent,
        text=text,
        fg_color=bg_color,
        text_color=fg_color,
        font=ctk.CTkFont(family=fonts["button"]["family"], size=fonts["button"]["size"], weight=fonts["button"]["weight"]),
        corner_radius=DIMENSIONS["button_radius"],
        command=command,
        width=width if width else 120,
        height=height if height else 36
    )
    button.pack(side=ctk.LEFT, padx=4, pady=4)
    return button

def create_header_with_buttons(parent, title_text, close_command, colors, fonts, 
                              start_move_fn, stop_move_fn, do_move_fn):
    """
    Create a header with title and buttons (close, minimize) with drag functionality.
    
    Args:
        parent: The parent widget
        title_text: The header title text
        close_command: The function to call when the close button is clicked
        colors: The color dictionary
        fonts: The font dictionary
        start_move_fn: Function to call when starting to drag
        stop_move_fn: Function to call when stopping drag
        do_move_fn: Function to call during drag
        
    Returns:
        Tuple of (header_frame, header_label, close_button, minimize_button)
    """
    # Create the header frame
    header_frame = ctk.CTkFrame(parent, fg_color=colors["primary"], corner_radius=16)
    header_frame.pack(fill=ctk.X, padx=1, pady=(1, 0))
    
    # Create rounded header using canvas
    header_height = DIMENSIONS["header_height"]
    # CustomTkinter doesn't have a CTkCanvas, so we'll use a CTkFrame instead
    header_canvas = ctk.CTkFrame(
        header_frame,
        fg_color=colors["primary"],
        corner_radius=16,
        height=header_height
    )
    header_canvas.pack(fill=ctk.X, expand=True)
    
    # Add the title label
    header_label = ctk.CTkLabel(
        header_canvas, 
        text=title_text, 
        fg_color=colors["primary"], 
        text_color="white", 
        font=ctk.CTkFont(family=fonts["title"]["family"], size=fonts["title"]["size"], weight=fonts["title"]["weight"]),
        anchor="w"
    )
    header_label.place(x=15, y=header_height//2, anchor="w")
    
    # Add close button
    close_button = ctk.CTkButton(
        header_canvas, 
        text="×", 
        fg_color=colors["primary"], 
        text_color="white",
        font=ctk.CTkFont(family=fonts["icon"]["family"], size=fonts["icon"]["size"]),
        corner_radius=0,
        command=close_command,
        width=30,
        height=30,
        hover_color=colors["primary_hover"]
    )
    close_button.place(x=5000, y=header_height//2, anchor="e")
    
    # Add minimize button
    minimize_button = ctk.CTkButton(
        header_canvas, 
        text="−", 
        fg_color=colors["primary"], 
        text_color="white",
        font=ctk.CTkFont(family=fonts["icon"]["family"], size=fonts["icon"]["size"]),
        corner_radius=0,
        command=close_command,  # Using same command as close for now
        width=30,
        height=30,
        hover_color=colors["primary_hover"]
    )
    minimize_button.place(x=5000-40, y=header_height//2, anchor="e")
    
    # Update button positions after window is configured
    def update_button_positions(event=None):
        window_width = parent.winfo_width()
        close_button.place(x=window_width-15, y=header_height//2, anchor="e")
        minimize_button.place(x=window_width-55, y=header_height//2, anchor="e")
    
    parent.bind("<Configure>", update_button_positions)
    parent.update_idletasks()
    update_button_positions()
    
    # Hover effects are handled by CTkButton's hover_color parameter
    
    # Add drag functionality to the header
    header_frame.bind("<ButtonPress-1>", start_move_fn)
    header_frame.bind("<ButtonRelease-1>", stop_move_fn)
    header_frame.bind("<B1-Motion>", do_move_fn)
    header_label.bind("<ButtonPress-1>", start_move_fn)
    header_label.bind("<ButtonRelease-1>", stop_move_fn)
    header_label.bind("<B1-Motion>", do_move_fn)
    header_canvas.bind("<ButtonPress-1>", start_move_fn)
    header_canvas.bind("<ButtonRelease-1>", stop_move_fn)
    header_canvas.bind("<B1-Motion>", do_move_fn)
    
    return header_frame, header_label, close_button, minimize_button

def create_text_display(parent, height, colors, fonts, is_readonly=True):
    """
    Create a text display area with border and styling.
    
    Args:
        parent: The parent widget
        height: Height in text lines
        colors: The color dictionary
        fonts: The font dictionary
        is_readonly: Whether the text display is read-only
        
    Returns:
        Tuple of (frame, text_widget)
    """
    # Create a frame for the text display with border and rounded corners
    frame = ctk.CTkFrame(
        parent, 
        fg_color=colors["border"],
        corner_radius=16
    )
    frame.pack(fill=ctk.X, pady=(0, 15))
    
    # Create the text widget
    text_widget = ctk.CTkTextbox(
        frame, 
        height=height*25,  # Approximate conversion from text lines to pixels
        fg_color=colors["secondary"],
        text_color=colors["text"],
        font=ctk.CTkFont(family=fonts["text"]["family"], size=fonts["text"]["size"]),
        corner_radius=16,
        wrap="word"
    )
    text_widget.pack(fill=ctk.X, padx=1, pady=1)
    
    # If read-only, disable editing
    if is_readonly:
        text_widget.configure(state="disabled")
    
    return frame, text_widget

def create_label_header(parent, text, colors, fonts):
    """
    Create a label header for sections.
    
    Args:
        parent: The parent widget
        text: The header text
        colors: The color dictionary
        fonts: The font dictionary
        
    Returns:
        The label widget
    """
    label = ctk.CTkLabel(
        parent, 
        text=text, 
        fg_color=colors["background"],
        text_color=colors["text"],
        font=ctk.CTkFont(family=fonts["header"]["family"], size=fonts["header"]["size"], weight=fonts["header"]["weight"]),
        anchor="w"
    )
    label.pack(fill=ctk.X, pady=(5, 10))
    
    return label
