# Silent Bloom 🔇

A minimalist Windows system audio mute toggle application built with Python and Tkinter.

## Features

- Clean, minimal interface with a single button
- Toggle system audio mute with a single click
- Preserves volume level when unmuting
- Always-on-top window
- Keyboard shortcuts (Space to toggle, Escape to exit)
- Visual feedback (red when muted, black when unmuted)
- Error logging and user notifications

## Requirements

- Windows OS
- Python 3.6+ (if running from source)
- `nircmd.exe` (included in releases)

## Installation

### From Release (Recommended)
1. Download the latest release from the [Releases](https://github.com/YOUR_USERNAME/Silent_bloom/releases) page
2. Extract the ZIP file
3. Run `silent_bloom.exe`

### From Source
1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Silent_bloom.git
cd Silent_bloom
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python silent_bloom.py
```

## Building from Source

To create a standalone executable:

```bash
python -m PyInstaller silent_bloom.spec
```

The executable will be created in the `dist` folder.

## Usage

- **Left-click** or press **Space**: Toggle audio mute
- **Right-click** or press **Escape**: Exit application
- The button turns **red** when muted and **black** when unmuted

## Dependencies

- tkinter (included with Python)
- PyInstaller (for building executable)
- nircmd.exe (for Windows audio control)

## Project Structure

```
Silent_bloom/
├── silent_bloom.py     # Main application code
├── silent_bloom.spec   # PyInstaller specification
├── requirements.txt    # Python dependencies
├── nircmd.exe         # Windows audio control utility
├── README.md          # This file
└── .gitignore         # Git ignore file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [NirCmd](https://www.nirsoft.net/utils/nircmd.html) by NirSoft for Windows audio control
- Icons and design inspiration from Material Design 