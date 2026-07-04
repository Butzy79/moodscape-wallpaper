# Moodscape Wallpaper

Moodscape Wallpaper is an AI-powered wallpaper engine for macOS that dynamically changes your desktop background based on mood, time of day, or custom prompts.

It downloads high-quality images from sources like Unsplash, Pexels, or Wallhaven and automatically applies them to your system wallpaper.

---

## Features

- Mood-based wallpapers (e.g. "Porsche", "focus", "relax")
- Time-aware switching (morning / day / night themes)
- Image sourcing from Unsplash, Pexels, Wallhaven
- macOS automatic wallpaper integration
- Lightweight CLI-first design
- Automatic refresh system (planned)

## Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/Butzy79/checklist-assistant.git
    ```
   
2. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```

3 Run the main script:
   ```bash
   python main.py
   ```

## License
This project is licensed under the MIT License.
See the LICENSE file for details.

## Contact
For issues, suggestions, or collaboration, please open an issue on GitHub or contact the developer.


## Create EXE file
Build environment:
```
python -m venv .venv
(win) .\.venv\Scripts\activate
(linux/macos) . .venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
```
Create Version
```
py gen_version[requirements.txt](../checklist-assistant/requirements.txt).py
pyinstaller --onefile --noconsole --name MoodScape_Wallpaper main.py --hidden-import requests --hidden-import packaging --icon=resources/butzy.ico --add-data "resources/butzy.ico;resources"
```

# Languages:
https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
en-US-GuyNeural
en-US-RogerNeural
en-GB-RyanNeural
en-GB-ThomasNeural
en-US-ChristopherNeural
en-US-EricNeural
en-US-SteffanNeural


# Icons
https://www.flaticon.com/search?word=settings&type=uicon