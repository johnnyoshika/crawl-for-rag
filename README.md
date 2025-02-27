# Crawl for RAG

Web crawler that starts with a sitemap.xml file and scrapes the pages and converts them to Markdown. Those files can then be used for RAG.

## Setup

Python 3.11.3:

1. Install pyenv
2. Install Python 3.11.3: `pyenv install 3.11.3`
3. pyenv should honor pinned version in [.python-version](.python-version). Confirm with: `python --version`
4. If Python version is not 3.11.3, run: `pyenv local 3.11.3`

Virtual Environemnt:

1. Create a virtual environment: `python -m venv venv`
2. Activate virtualenv: `.\venv\Scripts\activate` (Windows), `source venv/bin/activate` (macOS / Linux)
3. Install packages from requirements.txt: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and populate variables

After pip packages are installed, playright needs to be installed manually:

```
playwright install
```

This will install playright in `C:\Users\johnn\AppData\Local\ms-playwright\` (Windows)

## Usage

```
python main.py
```
