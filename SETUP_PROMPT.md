# A prompt for help with the setup

Section 1 of the [README](README.md) is all you need to get the starter running. If you get stuck, or want a guide through it, give the prompt below to a coding agent or a chatbot, for example in VS Code's chat. It helps with the setup only: it checks your tools, explains and runs the README's steps, and changes no code. The token viewer itself is yours to write: coding agents are allowed for hints only.

Log it in [AI_USAGE.md](AI_USAGE.md) like every prompt: write "SETUP_PROMPT.md" in the prompt column. If you changed the prompt, paste your version under Long prompts.

````text
Help me set up the token viewer starter on my laptop and get it running. Help with the setup only.

The project is a repository created from the template L3GJ0N/eaas_token_viewer_starter. First read README.md (section 1 "Run everything", "Checks" and "Troubleshooting") and GUIDE.md ("Running" and "Debugging"). Follow their steps; do not invent other ways.

Rules:
- Do not create, change or delete any file in the repository. Only the README's own commands may create files (backend/.venv, frontend/node_modules, build output). The code is mine to write: my course allows coding agents for hints only.
- Before you run a command, tell me what it does and why. Ask me before anything that installs software, changes a system setting or needs administrator rights, such as an installer, sudo or Set-ExecutionPolicy. Prefer the installers the README links.
- If you cannot run commands yourself, give me one command at a time and wait for my output.
- Never ask for, print or store keys, access tokens or passwords.

Steps:
1. Find out my operating system (Windows, macOS, Linux or WSL) and my shell. In WSL, work inside WSL only.
2. Check the four tools the README names, with their versions: Git, uv, Node.js 24 or newer with npm, and VS Code. Tell me what is missing and how to install it, as the README says.
3. Check where the repository lies. On Windows, it should be a short path outside OneDrive (see Troubleshooting).
4. In backend, run uv sync. In frontend, run npm ci.
5. Run the README's Checks: in backend, uv run ruff check, uv run ruff format --check, uv run mypy and uv run pytest; in frontend, npm run build.
6. Start the back end and the page as section 1 says, each in a terminal of its own. Check that http://127.0.0.1:8000/api/view-model answers with JSON and that http://localhost:5173 shows the page with the fake controller's made-up tokens. Then stop the back end again.
7. Explain how I open the repository in VS Code as a workspace (File > Open Workspace from File, then token_viewer.code-workspace), install the recommended extensions, and start Run and Debug with "Full stack: back end + browser" while npm run dev keeps running. Tell me where GUIDE.md puts the first breakpoint.
8. When something fails, look for it in the README's Troubleshooting table first, and explain the cause before you fix anything.

Finish with a short report: what works, what does not, and what I should ask my instructor.
````
