# DoxySAS - Doxygen-style Documentation Generator for SAS Macros

## Overview
DoxySAS is a user-friendly desktop application designed to automatically generate high-quality Doxygen-style documentation for your SAS macros. Built with Python and Tkinter, it offers an intuitive graphical interface allowing users to either paste SAS code directly or upload `.sas` files to generate standardized documentation seamlessly.

## Features

- **Intuitive GUI:** Easily upload SAS files or paste your code directly into the built-in editor.
- **Automated Documentation:** Leverages OpenRouter's API to create professional, structured Doxygen-style headers for your macros.
- **Code Preview:** View generated documentation instantly within the application.
- **Easy Export:** Quickly copy documentation headers to the clipboard or download them as `.sas` files.
- **Flexible Integration:** Configurable API key management for secure and personalized access to documentation generation services.

## Installation

### Requirements

- Python 3.8 or later
- OpenRouter API Key

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd DoxySAS
   ```

2. **Install Dependencies:**
   ```bash
   pip install requests
   ```

3. **Set up API Key:**
   - Obtain your API key from [OpenRouter](https://openrouter.ai/).
   - Set the API key as an environment variable:
     ```bash
     export OPENROUTER_API_KEY='your_api_key_here'
     ```

## Running the Application

Launch the application with the following command:
```bash
python doxysas.py
```

## Usage

1. **Upload or Paste SAS Code:** Use the "Upload SAS File" button to load files, or paste SAS code directly into the provided text area.
2. **Generate Documentation:** Click on "Generate Documentation" to create the documentation header.
3. **Preview and Download:** The generated documentation will be displayed in the preview pane. You can copy headers or download the entire documented file easily.

## Application Layout

- **Left Panel:** Input area for uploading files or pasting code.
- **Right Panel:** Displays generated documentation and allows for file management (copying/downloading headers).
- **API Settings:** Securely manage your OpenRouter API key within the app interface.

## Contributing

Contributions are welcome! Please fork this repository and create a pull request to suggest improvements or new features.

## License

Distributed under the MIT License. See `LICENSE` file for more details.

---

Enjoy automating your SAS documentation with DoxySAS!

