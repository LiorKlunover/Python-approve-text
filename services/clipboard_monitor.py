"""
Clipboard monitoring service for the Text Improver Pro application.

This module provides functionality for monitoring clipboard changes
and handling text selection events.
"""

import threading
import time
import pyperclip
import keyboard

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
        self.ctrl_c_pressed = False
    
    def start(self):
        """
        Start monitoring the clipboard in a background thread.
        """
        if self.thread is not None and self.thread.is_alive():
            return  # Already running
            
        self.running = True
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
        
        # Set up Ctrl+C detection
        keyboard.on_press_key("c", self._on_key_press, suppress=False)
    
    def stop(self):
        """
        Stop monitoring the clipboard.
        """
        self.running = False
        # Remove keyboard hook
        try:
            keyboard.unhook_key("c")
        except:
            pass
            
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
                
                # Check if Ctrl+C was pressed and there's content in the clipboard
                if self.ctrl_c_pressed and current_clipboard.strip():
                    # Reset the flag
                    self.ctrl_c_pressed = False
                    
                    # Update last known content
                    self.last_clipboard_content = current_clipboard
                    
                    # Notify the callback function
                    self.callback(current_clipboard)
                    continue
                
                # Regular clipboard monitoring (for compatibility)
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
            
    def _on_key_press(self, e):
        """
        Handle key press events to detect Ctrl+C.
        
        Args:
            e: The keyboard event
        """
        try:
            # Check if Ctrl is pressed along with C
            if keyboard.is_pressed('ctrl'):
                print("[DEBUG] Ctrl+C detected")
                # Set a flag that will be checked in the monitor thread
                self.ctrl_c_pressed = True
                # Give a small delay to allow clipboard to update
                threading.Timer(0.1, self._check_clipboard_after_ctrl_c).start()
        except Exception as e:
            print(f"Error handling key press: {e}")
            
    def _check_clipboard_after_ctrl_c(self):
        """
        Check clipboard content after Ctrl+C is pressed and notify callback.
        This is called after a short delay to ensure clipboard has updated.
        """
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard.strip() and len(current_clipboard) < self.max_text_length:
                # Update last known content
                self.last_clipboard_content = current_clipboard
                # Notify the callback function
                self.callback(current_clipboard)
        except Exception as e:
            print(f"Error checking clipboard after Ctrl+C: {e}")
