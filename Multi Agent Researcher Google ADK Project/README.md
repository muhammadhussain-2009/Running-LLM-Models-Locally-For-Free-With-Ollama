# Multi Agent Researcher — Google ADK Project

A small example project that demonstrates composing multiple Google ADK LLM agents (research, summarizer, critic) and a root/orchestrator agent. The project shows how to configure and run the ADK-based agents locally and how to expose a minimal web endpoint for quick testing.

> Note: This repository contains a package declared in `pyproject.toml` as `google-adk-project`. The source folder in this repo currently contains spaces in its name ("Multi Agent Researcher Google ADK Project"), which is not a valid Python package identifier for direct imports. See the Troubleshooting section below for guidance (installing the package or renaming the folder).

Contents
- Overview
- Requirements
- Quick install
- Running the project with `adk web`
- Running the project with uvicorn (the "UV" packet manager)
- Example minimal server (optional)
- Environment / configuration
- Contributing
- Troubleshooting
- License & contact

---

## Overview

This project defines three specialized LLM agents and a root/orchestrator agent using the Google ADK Python SDK:

- `research_agent` — performs web research (uses `google_search` tool)
- `summarizer_agent` — summarizes long documents
- `critic_agent` — provides critique and improvement suggestions
- `root_agent` — orchestrates the workflow and coordinates sub-agents

The code lives under the repository path:
`Multi Agent Researcher Google ADK Project/` and the package metadata is in `pyproject.toml`.

---

## Requirements

- Python 3.11 or newer
- pip
- A Google ADK account / credentials and any environment variables required by the `google-adk` package
- Recommended: create and use a virtual environment

Files of interest:
- `pyproject.toml` — project metadata (name: `google-adk-project`)
- `requirements.txt` — development/runtime dependencies

Dependencies listed in this repo (examples):
- google-adk
- python-dotenv
- uvicorn (for running with uvicorn)

---

## Quick install

1. Clone the repo
   ```bash
   git clone https://github.com/muhammadhussain-2009/Locally-Hosted-LLM-Projects.git
   cd "Locally-Hosted-LLM-Projects/Multi Agent Researcher Google ADK Project"
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell)
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   # or to install from pyproject.toml as an editable package:
   pip install -e .
   ```

4. Configure credentials (see Environment / configuration below).

---

## Running with adk web

If you have the ADK CLI tooling installed that provides `adk web`, you can run the project with it. `adk web` will start the ADK web runner that exposes the agents and developer tooling.

From the project directory (where `pyproject.toml` is located) run:

```bash
# start ADK web runner (requires ADK/CLI to be installed & configured)
adk web
```

What this does:
- Starts a local web server provided by the ADK tooling which is useful for development and inspecting agent behavior.
- The ADK tooling will pick up the package metadata and entry points in the project folder.

Notes:
- Ensure your ADK credentials are configured in your environment before running.
- If `adk` is not found, install/configure the Google ADK CLI per Google ADK documentation.

---

## Environment / configuration

This project uses `python-dotenv` and the `google-adk` package which likely expects credentials to be set in environment variables or standard ADK credential locations.

Suggested `.env` example (create a `.env` file in the project root and never commit secrets):

```env
# Example placeholders — consult Google ADK docs for exact variables required
GOOGLE_ADK_API_KEY=your_adk_api_key_here
GOOGLE_ADK_PROJECT_ID=your_project_id_here
GOOGLE_GENAI_USE_VERTEX_AI= 0
# Any other ADK-related environment variables needed by the google-adk package
```

Load `.env` automatically by your application (if you use it) or export environment variables before running:
```bash
export GOOGLE_ADK_API_KEY=your_adk_api_key_here
```

---

## Example usage (Python)

If you installed the package, you can import the orchestrator agent and use it programmatically in your Python code:

```python
from google_adk_project import root_agent  # adjust the name to the installed package name

# Example: show agent metadata (actual agent APIs vary by google-adk SDK)
print(root_agent.name)
print(root_agent.description)
```

Refer to the `google-adk` SDK docs for how to call/run/execute agents in code.

---

## Contributing

Thanks for wanting to contribute! A short guideline:

- Fork the repository and create a feature branch for your changes
  - git checkout -b feat/my-change
- Keep changes small and focused; open separate PRs for unrelated topics
- Use descriptive commit messages
- Add tests where appropriate and ensure tests pass locally
- Follow PEP8 / project style
- Update README or other docs if behavior or APIs change
- Open a GitHub Issue to discuss large changes before implementing
- Submit a Pull Request with:
  - Summary of the change
  - Why it’s needed
  - Any migration steps or backward-incompatible changes

Maintainers will review and provide feedback. Be responsive to review comments.

---

## Troubleshooting

1. Module import fails because folder name has spaces
   - Problem: The folder `Multi Agent Researcher Google ADK Project` contains spaces and is not a valid Python module name, so `import` will fail.
   - Fixes:
     - Install the project as an editable package: `pip install -e .` then import using the package name defined in `pyproject.toml` (example: `google-adk-project` or the normalized import name).
     - Rename the folder to a valid Python package name (e.g., `multi_agent_researcher_google_adk_project`) and update imports accordingly.

2. `ModuleNotFoundError: No module named 'google.adk'`
   - Ensure you installed the `google-adk` dependency: `pip install google-adk`
   - Verify you are using the correct Python interpreter / virtual environment.

3. `adk` command not found
   - The ADK CLI/tooling may not be installed or not in PATH. Follow Google ADK installation instructions to install CLI.

4. Authentication / model access errors
   - Confirm ADK credential environment variables are set and valid
   - Check network connectivity and API quotas
   - Ensure you have access to the model specified in the agents (the example uses `gemini-3-flash-preview` — your ADK account must have access to the specified model).

5. Unexpected agent behavior
   - Check the `google-adk` SDK docs for the correct APIs and usage patterns.
   - Enable any SDK debug or logging options to get more details.

6. Dependency version conflicts
   - Use a fresh virtual environment
   - Pin dependency versions in `requirements.txt` or `pyproject.toml` if necessary

If you hit a problem not covered above, open an Issue on the repo with:
- Clear description of the problem
- Steps to reproduce
- Python version and OS
- Relevant logs or error messages

---
Enjoy exploring multi-agent orchestration with Google ADK!
