---
name: BashScriptMaster
description: Advanced shell scripting best practices and automation logic.
triggers: [bash, shell, script, loop, variable, pipe, sed, awk, grep, automation]
---
# ASSERTIVE CONTEXT: PROFESSIONAL BASH SCRIPTING
- **Strict Mode:** Every script suggested must start with `set -euo pipefail` to ensure immediate failure on errors or undefined variables.
- **Portability:** Use `#!/usr/bin/env bash` for the shebang to ensure the script finds the bash binary in the user's PATH.
- **Syntax:** - Always use `[[ ]]` for tests instead of `[ ]`.
  - Prefer `$(...)` over backticks for command substitution.
  - Quote all variables (e.g., `"$VAR"`) to prevent word splitting and globbing.
- **Functionality:** Group logic into functions. Use `local` for all function-scoped variables to avoid namespace pollution.
- **Performance:** For large file processing, prefer `awk` or `sed` over pure bash loops to maintain efficiency.