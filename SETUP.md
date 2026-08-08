# Local setup

1. Create a virtual environment:
   `python -m venv .venv`
2. Activate it in PowerShell:
   `.venv\Scripts\Activate.ps1`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Set the environment variables listed in `.env.example`.
5. Keep `.env` private. Never commit it.
6. Put the dataset at `data/pokec_sample.tsv`, or set `POKEC_FILE` to its local path.

## Security
The original project files contained hard-coded database credentials. The GitHub-safe versions in this folder do not contain those passwords; they read credentials from environment variables instead.
