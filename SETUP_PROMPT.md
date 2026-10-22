# A prompt for help with the setup

Section 1 of the [README](README.md) is all you need to get the starter running. If you get stuck, or want a guide through it, give the prompt below to a coding agent or a chatbot, for example in VS Code's chat. It helps with the setup only: it checks your tools, explains and runs the README's steps, and changes no code. The token viewer itself is yours to write: coding agents are allowed for hints only.

Log it in [AI_USAGE.md](AI_USAGE.md) like every prompt: one row with "SETUP_PROMPT.md" in the prompt column covers the whole setup conversation, your short answers included. If you changed the prompt, paste your version under Long prompts.

````text
Help me set up the token viewer starter on my laptop and get it running. Help with the setup only.

The project is a repository created from the template L3GJ0N/eaas_token_viewer_starter. First read README.md (section 1 "Run everything", "Checks", "Versions" and "Troubleshooting") and GUIDE.md ("Running" and "Debugging"). Follow their steps; do not invent other ways.

Rules:
- Do not create, change or delete any tracked file in the repository. The README's commands and checks may create only files that Git ignores (.venv, node_modules, dist, caches). Do not run npm run types: it rewrites a tracked file. The code is mine to write: my course allows coding agents for hints only.
- Before you run a command, tell me what it does and why. uv sync and npm ci install into the project only: tell me, then run them. Ask me first before anything that installs software on my laptop, downloads Python, changes a system setting or needs administrator rights, such as an installer, sudo or Set-ExecutionPolicy. Prefer the installers the README links.
- If you cannot run commands yourself, give me one command at a time and wait for my output. You cannot see my screen: when something must be checked by eye, ask me.
- Never ask for, print or store keys, access tokens or passwords. Do not write in AI_USAGE.md: I log this conversation myself.

Steps:
1. Find out my operating system (Windows, macOS, Linux or WSL) and which shell my VS Code terminal uses; ask me if you cannot tell. In WSL, work inside WSL only. If I talk to you in VS Code, check that it has opened token_viewer.code-workspace, not only the folder.
2. Check the four tools the README names, with their versions: Git, uv, Node.js 24 or newer with npm, and VS Code 1.112 or newer (code --version prints it). Tell me what is missing and how to install it, as the README says.
3. Check where the repository lies: on Windows, a short path outside OneDrive, and on every system not in a temporary or Downloads folder (see Troubleshooting).
4. In backend, run uv sync. In frontend, run npm ci.
5. Run the README's Checks except npm run types:check: in backend, uv run ruff check, uv run ruff format --check, uv run mypy and uv run pytest; in frontend, npm run build.
6. Check that nothing listens on ports 8000 and 5173. Start the back end and the page as section 1 says, each in a terminal of its own. Check that http://127.0.0.1:8000/api/view-model and http://localhost:5173/api/view-model answer with JSON, the second through Vite's proxy, and run npm run types:check in frontend. Ask me to open http://localhost:5173 and confirm the notice "Made-up data from the fake controller" and the chips. Then stop both, and check that ports 8000 and 5173 are free again.
7. Explain the rest for me to do in VS Code: open token_viewer.code-workspace with File > Open Workspace from File and answer Yes to the trust question; install the recommended extensions from VS Code's notification, or with @recommended in the Extensions view; start npm run dev in a VS Code terminal in frontend; then start Run and Debug with "Full stack: back end + browser". Tell me where GUIDE.md puts the first breakpoints, in Python and in TypeScript.
8. When something fails, look for it in the README's Troubleshooting table first, and explain the cause before you fix anything.

Finish with a short report: what works, what does not, and what I should ask my instructor. Run git status at the end and show me that no tracked file changed. Remind me to log this conversation in AI_USAGE.md.
````
