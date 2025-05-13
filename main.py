import tkinter as tk
from ui.app import TextImproverApp

if __name__ == "__main__":
    # Create the root Tkinter window
    root = tk.Tk()
    
    # Initialize the application
    app = TextImproverApp(root)
    
    # Start the main event loop
    root.mainloop()
