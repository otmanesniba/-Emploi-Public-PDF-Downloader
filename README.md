# 🚀 Emploi Public PDF Downloader

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A powerful automation tool for downloading and organizing PDF documents from Morocco's public employment portal (emploi-public.ma).

## ✨ Features

- **Automated Navigation**: Smart browsing of emploi-public.ma website
- **PDF Extraction**: Downloads all related PDF documents automatically
- **Human-like Interaction**: Realistic delays and behaviors to avoid detection
- **Detailed Screenshots**: Captures formatted information screenshots
- **Progress Tracking**: Visual progress bars and spinner animations
- **Organized Storage**: Creates structured folders for all downloads
- **Comprehensive Data**: Extracts ministry, dates, positions, and requirements

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/emploi-public-pdf-downloader.git
   cd emploi-public-pdf-downloader

Here's the structured content ready for easy copying:

### 📦 Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up WebDriver**:
   - Download [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
   - Update the path in `setup_edge_driver()` if needed

---

### 🚀 Usage
Run the main script:
```bash
python emploi_public_pdf_downloader.py
```

The interactive program will guide you through:
1. Selecting the number of competitions to process
2. Showing available concours with detailed screenshots
3. Letting you choose which to download
4. Automatically organizing all files

---

### 📂 File Structure
```
emploi-public-pdf-downloader/
├── Concours_PDFs/              # All downloaded PDF documents
├── Concours_Screenshots/       # Formatted information screenshots
├── emploi_public_pdf_downloader.py  # Main script file
├── requirements.txt            # Python dependencies
└── README.md                   # This documentation file
```

---

### 📋 Requirements
- Python 3.7 or higher
- Microsoft Edge browser
- Microsoft Edge WebDriver
- Python packages:
  ```
  selenium>=4.0.0
  fake-useragent>=1.1.3
  pyfiglet>=0.8.post1
  colorama>=0.4.4
  requests>=2.26.0
  ```

---

### 🛠️ Customization
Modify these variables in the script:
```python
# Change download directory (default: Desktop/Concours_PDFs)
download_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Concours_PDFs')

# Adjust human-like behavior delays (in seconds)
human_like_delay(min_seconds=1, max_seconds=3)
```

---

### ⚠️ Important Notes
- Use this tool responsibly and respectfully
- Add delays if processing many pages to avoid overloading servers
- The script may need updates if the website structure changes
- Recommended to not run more than 20 concours at once

---

### 🤝 Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

🎯 This tool was developed by Otmane Sniba to help automate the process of gathering public employment information in Morocco. Please use it responsibly and respect the website's terms of service.

### 📌 Disclaimer
This project is independently developed by Otmane Sniba and is not affiliated with or endorsed by emploi-public.ma. The developer is not responsible for any misuse of this tool. Please use at your own discretion and in accordance with all applicable laws and website policies.

### 🙏 Acknowledgments 

● Special thanks to all contributors who helped improve this project
● Grateful to the open source community for inspiration
● Appreciation to everyone who provided feedback and suggestions
