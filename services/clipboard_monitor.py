"""
Clipboard monitoring service for the Text Improver Pro application.

This module provides functionality for monitoring clipboard changes
and handling text selection events.
"""

import threading
import time
import pyperclip

class ClipboardMonitor:
    """
    A class for monitoring clipboard changes and detecting text selection.
    
    This class runs a background thread that continuously checks the clipboard
    for changes and notifies the application when new text is selected.
    """
    
    def __init__(self, callback):
        """
        Initialize the clipboard monitor.
        
        Args:
            callback: Function to call when new text is detected in the clipboard.
                      The function should accept a single string parameter.
        """
        self.callback = callback
        self.running = False
        self.thread = None
        self.last_clipboard_content = ""
        self.max_text_length = 10000  # Maximum text length to process (arbitrary limit)
    
    def start(self):
        """
        Start monitoring the clipboard in a background thread.
        """
        if self.thread is not None and self.thread.is_alive():
            return  # Already running
            
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
    
    def stop(self):
        """
        Stop monitoring the clipboard.
        """
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)  # Wait for thread to terminate
            self.thread = None
    
    def _monitor(self):
        """
        Monitor the clipboard for changes.
        This method runs in a background thread.
        """
        # Initialize with current clipboard content
        try:
            self.last_clipboard_content = pyperclip.paste()
        except Exception:
            self.last_clipboard_content = ""
        
        while self.running:
            try:
                # Check if clipboard content has changed
                current_clipboard = pyperclip.paste()
                
                # Only process if content has changed and is not empty
                if (current_clipboard != self.last_clipboard_content and 
                    current_clipboard.strip() and 
                    len(current_clipboard) < self.max_text_length):
                    
                    # Update last known content
                    self.last_clipboard_content = current_clipboard
                    
                    # Notify the callback function
                    self.callback(current_clipboard)
            except Exception as e:
                print(f"Error monitoring clipboard: {e}")
            
            # Sleep to avoid high CPU usage
            time.sleep(0.5)
    
    def get_clipboard_content(self):
        """
        Get the current clipboard content.
        
        Returns:
            The current text in the clipboard, or an empty string if there's an error.
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error getting clipboard content: {e}")
            return ""
    
    def set_clipboard_content(self, text):
        """
        Set the clipboard content.
        
        Args:
            text: The text to set in the clipboard.
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            # Temporarily store the last content to avoid triggering the monitor
            self.last_clipboard_content = text
            
            # Set the clipboard content
            pyperclip.copy(text)
            return True
        except Exception as e:
            print(f"Error setting clipboard content: {e}")
            return False
