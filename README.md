# Sendify-Challenge
My solution to the Sendify Code Challenge 2026

## Installation
This implementation is built using Python and the fastmcp package. To scrape the page I'm using playwright. To easily manage installation I have chosen UV. 

### Install UV
MacOS and Linux  
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```  
Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
<details>

<summary>More installation ways (PyPi, Homebrew, MacPorts, Winget and Scoop)</summary>

#### PyPI

```
pipx install uv
```
However, pip can also be used:

```
pip install uv
```

#### Homebrew
```
brew install uv
```

#### MacPorts
```
sudo port install uv
```

#### WinGet
```
winget install --id=astral-sh.uv  -e
```

#### Scoop
```
scoop install main/uv
```
Read more at https://docs.astral.sh/uv/getting-started/installation/
</details>

### Build and activate Virtual Environment
Create the virtual environment using UV
```bash
uv venv
```

Activate virtual environment
```bash
.venv\Scripts\activate
```

Install dependencies
```bash
uv pip install -r .\requirements.txt
```

Install Playwright
```bash
playwright install
```

### Start the MCP server
```bash
fastmcp run mcp_server.py --transport http --port 8000
```