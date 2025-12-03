# Text Improver Pro

A modern application that improves and shortens text using AI. Select text in any application, press Ctrl+Shift+X, and get improved text instantly.
<img width="420" height="657" alt="image" src="https://github.com/user-attachments/assets/1993c25f-f529-4821-bb1e-8263a2e0388d" />

## Features

- **Modern UI**: Clean, responsive interface with animations and visual effects
- **Global Hotkey**: Press Ctrl+Shift+X to improve selected text from any application
- **AI-Powered**: Uses advanced language models to improve text quality
- **Multiple Styles**: Supports professional, casual, academic, and creative text styles
- **Copy to Clipboard**: One-click copying of improved text

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/text-improver-pro.git
cd text-improver-pro
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

## Usage

1. Select text in any application
2. Press Ctrl+Shift+X
3. The Text Improver Pro window will appear with your selected text
4. Click "Improve Text" to get an improved version
5. Click "Copy to Clipboard" to copy the result

## Project Structure

- `main.py` - Entry point for the application
- `ui/` - User interface components
  - `app.py` - Main application class
  - `components.py` - Reusable UI components
  - `styles.py` - Colors, fonts, and styling constants
- `services/` - Core functionality
  - `text_processor.py` - Text improvement logic
  - `clipboard_monitor.py` - Clipboard monitoring
- `utils/` - Utility functions
  - `image_utils.py` - Image manipulation utilities

## Dependencies

- openai - For API access to language models
- pyperclip - For clipboard access
- keyboard - For global hotkey monitoring
- pillow - For image processing and UI effects

## License

MIT
