# Llama Recoil

A recoil control system with a web-based interface for managing and creating recoil patterns. Uses the Makcu library for mouse control.

## Credits

- **SleepyTotem Makcu Lib* - https://pypi.org/project/makcu/


## Features

- **Web Interface** - Control everything from your browser (accessible from any device on your network)
- **Simple Mode** - Basic X/Y recoil control with adjustable delay
- **Advanced Mode** - Create and load custom recoil scripts with step-by-step patterns
- **Script Editor** - Visual editor to create, edit, and test recoil patterns
- **Hipfire Support** - Toggle hipfire mode for both simple and advanced modes
- **Test Mode** - Test your patterns directly in the script editor before saving

## Requirements

- Python 3.8+
- Makcu device
- Windows OS

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dev-boog/Llama-Recoil.git
   cd Llama-Recoil
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Connect your Makcu device**

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Access the web interface**
   - Local: http://127.0.0.1:5000
   - Network: The application will display your network IP on startup

## Web Interface Pages

- **Home** (`/`) - Dashboard overview
- **Scripts** (`/run_script`) - Enable/disable recoil, switch between simple and advanced modes
- **Create Script** (`/create_script`) - Create and edit recoil patterns
- **Settings** (`/settings`) - Application settings

## Creating Recoil Scripts

1. Navigate to **Create Script** page
2. Select an existing script or create a new one
3. Add steps with X (horizontal) and Y (vertical) movement values
4. Set the delay between steps (in milliseconds)
5. Use the **Enable** toggle to test your pattern in real-time
6. Scripts auto-save when you make changes

## Project Structure

```
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── Config/              # Configuration and saved scripts
│   ├── config.py
│   └── SavedScripts/    # JSON script files
├── Console/             # Console logging utilities
├── Makcu/               # Makcu device wrapper
├── Recoil/              # Recoil control logic
└── Server/              # Flask web server
    ├── app.py
    ├── routes/          # API endpoints
    ├── static/          # CSS and JavaScript
    └── templates/       # HTML templates
```

## License

This project is for educational purposes only.
