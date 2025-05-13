import customtkinter as ctk
# from tkinter import ttk  # Removed, not needed with customtkinter
import os
import sys
import keyboard

# Import from other modules
from ui.styles import COLORS, FONTS
from ui.components import create_rounded_button, create_header_with_buttons
from services.text_processor import improve_text
from services.clipboard_monitor import ClipboardMonitor
from utils.image_utils import create_drop_shadow, create_gradient_background

import time

class TextImproverApp:
    """Main application class for the Text Improver Pro application.
    
    This class manages the main UI and coordinates between different components.
    """
    
    def __init__(self, root):
        """Initialize the application with the root Tkinter window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        ctk.set_appearance_mode("light")
        self.root.title("Text Improver Pro")
        self.root.geometry("420x650")
        self.root.withdraw()
        # Set app icon if available
        self._set_app_icon()
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        
        # Configure the root window with rounded corners
        # Note: We'll use a main frame with rounded corners and a small margin
        # This creates the appearance of a rounded window
        self.root.configure(bg=COLORS["border"])  # Border color for the small margin
        
        # Set up main frame with rounded corners
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=COLORS["background"], 
            corner_radius=16,  # Fixed corner radius value
            border_width=0
        )
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=2, pady=2)  # Small margin for rounded effect
        
        # Create the UI components
        self._create_ui()
        
        # Initialize variables
        self.selected_text = ""
        self.processing_selection = False
        
        # Set up double-Shift detection for showing the popup
        self._last_shift_time = 0
        self._shift_interval_ms = 400  # Max ms between double presses
        keyboard.on_press(self._handle_shift_double_press)

        print("✨ Text Improver Pro is running in the background.")
        print("Select text in any application and double-press Shift to improve it.")
    
    def _handle_shift_double_press(self, event):
        print(f"[DEBUG] Key pressed: {event.name}")
        if event.name == 'shift':
            now = time.time() * 1000  # ms
            if hasattr(self, '_last_shift_time') and now - self._last_shift_time < self._shift_interval_ms:
                print("[DEBUG] Double Shift detected!")
                self._last_shift_time = 0
                self._on_hotkey_pressed()
            else:
                self._last_shift_time = now

    def _set_app_icon(self):
        """Set the application icon if available."""
        try:
            # Get the directory where the script is located
            if getattr(sys, 'frozen', False):
                # If the application is run as a bundle
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            icon_path = os.path.join(application_path, "../assets/app_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            # Proceed without icon if not found
            pass
    
    def _create_ui(self):
        """Create all UI components."""
        # Create header with drag functionality
        self.header_frame, self.header_label, self.close_button, self.minimize_button = create_header_with_buttons(
            self.main_frame, 
            "✨ Text Improver Pro",
            self.hide_window,
            COLORS,
            FONTS,
            self.start_move,
            self.stop_move,
            self.do_move
        )
        
        # Add a separator between header and content
        # Separator not needed, or use a CTkFrame with small height for visual separation
        self.separator = ctk.CTkFrame(self.main_frame, height=2, fg_color=COLORS["shadow_light"], corner_radius=1)
        self.separator.pack(fill=ctk.X, padx=1, pady=(0, 1))
        
        # Content frame with padding and rounded corners
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["background"], corner_radius=20)
        self.content_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        # Selected text display with better styling
        self._create_text_input_area()
        
        # Create the improve button
        self._create_improve_button()
        
        # Result display area
        self._create_result_area()
        
        # Footer with information
        self._create_footer()
    
    def _create_text_input_area(self):
        """Create the text input area for displaying selected text."""
        self.selected_text_label = ctk.CTkLabel(
            self.content_frame, 
            text="Selected Text", 
            fg_color=COLORS["background"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family=FONTS["header"]["family"], size=FONTS["header"]["size"], weight=FONTS["header"]["weight"]),
            anchor="w"
        )
        self.selected_text_label.pack(fill=ctk.X, pady=(5, 10))
        
        self.text_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS["border"],
            corner_radius=16
        )
        self.text_frame.pack(fill=ctk.X, pady=(0, 20))
        
        self.selected_text_display = ctk.CTkTextbox(
            self.text_frame,
            height=100,
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family=FONTS["text"]["family"], size=FONTS["text"]["size"]),
            corner_radius=16,
            wrap="word"
        )
        self.selected_text_display.pack(fill=ctk.X, padx=1, pady=1)
    
    def _create_improve_button(self):
        """Create the improve button with modern styling."""
        self.improve_button_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLORS["background"],
            corner_radius=16
        )
        self.improve_button_frame.pack(pady=10)
        
        self.improve_button = create_rounded_button(
            self.improve_button_frame,
            "✨ Improve Text",
            self.improve_text,
            COLORS,
            FONTS
        )
    
    def _create_result_area(self):
        """Create the result display area."""
        self.result_frame = ctk.CTkFrame(self.content_frame, fg_color=COLORS["background"], corner_radius=16)
        self.result_frame.pack(fill=ctk.X, pady=15)
        self.result_frame.pack_forget()  # Hide initially
        
        self.result_label = ctk.CTkLabel(
            self.result_frame, 
            text="Improved Text", 
            fg_color=COLORS["background"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family=FONTS["header"]["family"], size=FONTS["header"]["size"], weight=FONTS["header"]["weight"]),
            anchor="w"
        )
        self.result_label.pack(fill=ctk.X, pady=(0, 10))
        
        self.result_display = ctk.CTkTextbox(
            self.result_frame, 
            height=180, 
            fg_color=COLORS["secondary"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family=FONTS["text"]["family"], size=FONTS["text"]["size"]),
            corner_radius=16,
            wrap="word"
        )
        self.result_display.pack(fill=ctk.X, padx=1, pady=1)
        
        # Add a copy button
        self.button_frame = ctk.CTkFrame(self.result_frame, fg_color=COLORS["background"], corner_radius=16)
        self.button_frame.pack(fill=ctk.X, pady=(0, 10))
        
        self.copy_button = create_rounded_button(
            self.button_frame,
            "📋 Copy to Clipboard",
            self.copy_to_clipboard,
            COLORS,
            FONTS,
            is_secondary=False  # Changed to False to use primary (purple) color
        )
    
    def _create_footer(self):
        """Create the footer with information."""
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["background"], height=30, corner_radius=16)
        self.footer_frame.pack(fill=ctk.X, side=ctk.BOTTOM, padx=15, pady=(0, 10))
        
        self.footer_text = ctk.CTkLabel(
            self.footer_frame,
            text="Press Ctrl+Shift+X to activate",
            fg_color=COLORS["background"],
            text_color=COLORS["text_light"],
            font=ctk.CTkFont(family=FONTS["text"]["family"], size=8),
            anchor="e"
        )
        self.footer_text.pack(side=ctk.RIGHT)
    
    # Clipboard monitoring is disabled; activation is only via hotkey.
    # def _start_clipboard_monitoring(self):
    #     pass
    
    def start_move(self, event):
        """Start window dragging."""
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event):
        """Stop window dragging."""
        self.x = None
        self.y = None
    
    def do_move(self, event):
        """Move the window during drag."""
        if self.x is not None and self.y is not None:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")
    
    def show_window_at_cursor(self):
        """Show the window near the cursor position with a fade-in effect."""
        # Get cursor position
        x, y = self.root.winfo_pointerxy()
        
        # Adjust position to not go off screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 420
        window_height = 650
        
        if x + window_width > screen_width:
            x = screen_width - window_width
        
        if y + window_height > screen_height:
            y = screen_height - window_height
        
        # Position and show the window
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        
        # Add fade-in effect
        self.root.attributes('-alpha', 0.0)
        
        def fade_in():
            current_alpha = self.root.attributes('-alpha')
            if current_alpha < 1.0:
                self.root.attributes('-alpha', current_alpha + 0.1)
                self.root.after(20, fade_in)
        
        fade_in()
    
    def hide_window(self):
        """Hide the window."""
        self.root.withdraw()
    
    def _on_hotkey_pressed(self):
        """Handler for Ctrl+Shift+X: triggers Ctrl+C, waits, then shows app with clipboard text."""
        import pyperclip
        import time
        keyboard.send('ctrl+c')  # Simulate Ctrl+C to copy selection in the currently focused app
        time.sleep(0.6)  # Wait for clipboard to update (increase if needed)
        clipboard_content = pyperclip.paste()
        if clipboard_content.strip():
            self.process_selected_text(clipboard_content)
        else:
            # Optionally, show the app with a message if nothing is copied
            self.selected_text_display.delete("1.0", "end")
            self.selected_text_display.insert("end", "No text was copied. Please select text and try again.")
            self.show_window_at_cursor()
    
    def process_selected_text(self, text):
        """Process the selected text from clipboard."""
        if not self.processing_selection:
            self.processing_selection = True
            try:
                self.selected_text = text.strip()
                
                if self.selected_text:
                    # Update the selected text display
                    self.selected_text_display.delete("1.0", "end")
                    self.selected_text_display.insert("end", self.selected_text)
                    
                    # Show the window
                    self.show_window_at_cursor()
                    
                    # Hide the result frame when showing for new text
                    self.result_frame.pack_forget()
            finally:
                self.processing_selection = False
    
    def improve_text(self):
        """Improve the selected text using the LLM API."""
        # Clear previous results
        self.result_frame.pack(fill=ctk.X, pady=15)
        self.result_display.delete("1.0", "end")
        self.result_display.insert("end", "✨ Improving your text...")
        
        # Add a subtle pulse effect to the button during processing
        def pulse_button():
            if self.improve_button.cget('state') == "disabled":
                current_color = self.improve_button.cget('fg_color')
                if current_color == COLORS["primary_dark"]:
                    self.improve_button.configure(fg_color=COLORS["primary"])
                else:
                    self.improve_button.configure(fg_color=COLORS["primary_dark"])
                self.root.after(500, pulse_button)
        
        # Change button state to indicate processing with animation
        self.improve_button.configure(state="disabled", text="✨ Processing...")
        pulse_button()
        
        # Call the API in a separate thread
        import threading
        threading.Thread(target=self._perform_improvement).start()
    
    def _perform_improvement(self):
        """Call the API to improve the text."""
        try:
            # Get the selected text
            text_to_improve = self.selected_text
            
            # Call the improve_text function from the text_processor module
            improved_text = improve_text(text_to_improve)
            
            # Update the result display with the improved text
            self.root.after(0, lambda: self._update_result(improved_text))
        except Exception as e:
            # Handle any errors
            error_message = f"Error: {str(e)}"
            self.root.after(0, lambda: self._update_result(error_message))
    
    def _update_result(self, result_text):
        """Update the result display with the improved text."""
        # Add a typewriter effect to show the result
        self.result_display.delete("1.0", "end")
        
        # Reset button state
        self.improve_button.configure(state="normal", text="✨ Improve Text")
        
        # Apply typewriter effect
        def typewriter(text, index=0):
            if index < len(text):
                self.result_display.insert("end", text[index])
                self.root.after(10, typewriter, text, index + 1)
                # Auto-scroll to ensure text is visible
                self.result_display.see("end")
        
        # Start the typewriter effect
        typewriter(result_text)
    
    def copy_to_clipboard(self):
        """Copy the improved text to clipboard with animation."""
        improved_text = self.result_display.get("1.0", "end").strip()
        if improved_text:
            import pyperclip
            pyperclip.copy(improved_text)
            
            # Show a temporary "Copied!" message with animation
            original_text = self.copy_button.cget("text")
            original_fg_color = self.copy_button.cget("fg_color")
            original_text_color = self.copy_button.cget("text_color")
        
            # Create a smoother transition
            def animate_button(step=0, total_steps=10):
                if step <= total_steps:
                    # Calculate transition values
                    if step == 0:
                        # Immediate change to success state
                        self.copy_button.configure(
                            text="✓ Copied!", 
                            fg_color=COLORS["success"],
                            text_color="white"
                        )
                    elif step == total_steps:
                        # Final step - restore original state
                        self.copy_button.configure(
                            text=original_text, 
                            fg_color=original_fg_color,
                            text_color=original_text_color
                        )
                
                    # Continue animation
                    self.root.after(100, animate_button, step + 1, total_steps)
            
            # Start animation after a brief delay
            self.root.after(200, animate_button)