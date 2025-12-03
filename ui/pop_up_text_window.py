import customtkinter as ctk
from ui.styles import COLORS, FONTS, DIMENSIONS


class PopupTextWindow:
    """
    A modern pop-up window for displaying long text responses.
    Uses CustomTkinter for a consistent look and feel with the main application.
    """

    def __init__(self, parent=None):
        """
        Initialize the popup text window.
        
        Args:
            parent: Parent window (optional)
        """
        self.window = None
        self.parent = parent
        self.text_widget = None
        self.close_callback = None

    def show_text(self, title, text, close_callback=None):
        """
        Display the popup window with the provided text.
        
        Args:
            title (str): Window title
            text (str): Text to display
            close_callback (function): Function to call when window is closed
        """
        self.close_callback = close_callback
        
        # Destroy existing window if open
        if self.window and self.window.winfo_exists():
            self.window.destroy()

        # Create new window
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title(title)
        self.window.geometry("600x500")
        self.window.minsize(600, 500)
        
        # Make window modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Configure window appearance
        self.window.configure(fg_color=COLORS["background"])
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Create UI elements
        self._create_ui(text)
        
        # Center window on screen
        self._center_window()
        
        # Bring window to front
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.after_idle(self.window.attributes, '-topmost', False)

    def _create_ui(self, text):
        """Create the user interface elements."""
        # Main frame
        main_frame = ctk.CTkFrame(
            self.window,
            fg_color=COLORS["background"],
            corner_radius=DIMENSIONS["corner_radius"]
        )
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header frame
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["primary"],
            corner_radius=DIMENSIONS["corner_radius"]
        )
        header_frame.pack(fill=ctk.X, padx=0, pady=(0, 10))
        
        # Header title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Text Response",
            fg_color=COLORS["primary"],
            text_color="white",
            font=ctk.CTkFont(
                family=FONTS["header"]["family"],
                size=FONTS["header"]["size"],
                weight=FONTS["header"]["weight"]
            )
        )
        title_label.pack(side=ctk.LEFT, padx=15, pady=15)
        
        # Close button
        close_button = ctk.CTkButton(
            header_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=COLORS["primary_hover"],
            text_color="white",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._on_close
        )
        close_button.pack(side=ctk.RIGHT, padx=10, pady=10)
        
        # Text area with scrollbars
        text_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["background"],
            corner_radius=8
        )
        text_frame.pack(fill=ctk.BOTH, expand=True, padx=0, pady=0)
        
        # Create text widget with scrollbar
        text_container = ctk.CTkFrame(
            text_frame,
            fg_color=COLORS["secondary"],
            corner_radius=8
        )
        text_container.pack(fill=ctk.BOTH, expand=True, padx=0, pady=0)
        
        # Scrollable text widget
        self.text_widget = ctk.CTkTextbox(
            text_container,
            wrap=ctk.WORD,
            fg_color=COLORS["background"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                family=FONTS["text"]["family"],
                size=FONTS["text"]["size"]
            ),
            corner_radius=8
        )
        self.text_widget.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Insert text
        self.text_widget.insert("0.0", text)
        
        # Make text read-only
        self.text_widget.configure(state="disabled")
        
        # Button frame
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        button_frame.pack(fill=ctk.X, padx=0, pady=(10, 0))
        
        # Close button at bottom
        close_button_bottom = ctk.CTkButton(
            button_frame,
            text="Close",
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color="white",
            font=ctk.CTkFont(
                family=FONTS["button"]["family"],
                size=FONTS["button"]["size"],
                weight=FONTS["button"]["weight"]
            ),
            command=self._on_close
        )
        close_button_bottom.pack(side=ctk.RIGHT, padx=10, pady=10)

    def _center_window(self):
        """Center the window on the screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def _on_close(self):
        """Handle window close event."""
        if self.close_callback:
            self.close_callback()
        if self.window:
            self.window.destroy()
            self.window = None


def show_popup_text(parent, title, text, close_callback=None):
    """
    Convenience function to create and show a popup text window.
    
    Args:
        parent: Parent window
        title (str): Window title
        text (str): Text to display
        close_callback (function): Function to call when window is closed
    """
    popup = PopupTextWindow(parent)
    popup.show_text(title, text, close_callback)
    return popup