https://gemini.google.com/app/ef702d7b7d7b75b1



this is not what I wanted, I want a python script that from a prompt and using context .md files and, progressive disclose, builds assertive context for specific and specialised AI responses, like  OpenClaw seems to do

# ######################

```



uv pip install PyYAML requests



```





This is a great pivot. You’re looking for the **In-Context Learning (ICL) orchestration** logic. In systems like OpenClaw or Anthropic’s "Agent Skills," the goal isn't just to dump files into a prompt—it's to prevent "context pollution" by only feeding the AI what it actually needs to execute the current task.

The pattern is often called the **"Metadata Hook"** approach. It works in three distinct layers:

1. **Layer 1 (The Registry):** The AI sees a list of *names* and *one-sentence descriptions* of available knowledge/skills.
2. **Layer 2 (The Instruction Set):** Only if the AI decides a skill is relevant does it "disclose" (read) the full `.md` file.
3. **Layer 3 (The Deep Context):** If the `.md` file references specialized technical docs or huge data tables, those are read only on an "as-needed" basis.

Below is a complete, standalone Python script that implements this **Progressive Disclosure Context Engine**.

Python

```
# context_engine.py
import os
import re
import yaml
import json
from typing import List, Dict, Optional

class ProgressiveDisclosureEngine:
    """
    A context orchestrator that mimics the OpenClaw/Claude Skills mechanism.
    It manages a multi-layered disclosure of Markdown-based knowledge.
    """
    
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = knowledge_dir
        self.registry: Dict[str, Dict] = {}
        self._initialize_registry()

    def _initialize_registry(self):
        """
        LAYER 1: The 'Metadata Hook'. 
        Scans all .md files and extracts only the YAML frontmatter.
        """
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir)
            return

        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(".md"):
                path = os.path.join(self.knowledge_dir, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract YAML frontmatter between --- tags
                    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                    if match:
                        metadata = yaml.safe_load(match.group(1))
                        metadata['filename'] = filename
                        # Use name or filename as key
                        key = metadata.get('name', filename)
                        self.registry[key] = metadata

    def get_layer_1_context(self) -> str:
        """Returns the lightweight 'Registry' for the AI to choose from."""
        context = "AVAILABLE SPECIALIZED SKILLS:\n"
        for name, meta in self.registry.items():
            context += f"- {name}: {meta.get('description', 'No description available.')}\n"
        return context

    def disclose_layer_2(self, skill_name: str) -> str:
        """
        LAYER 2: The 'Instruction Set'. 
        Loads the full content of a specific .md file once selected.
        """
        meta = self.registry.get(skill_name)
        if not meta:
            return f"Error: Skill '{skill_name}' not found."
        
        path = os.path.join(self.knowledge_dir, meta['filename'])
        with open(path, 'r', encoding='utf-8') as f:
            # We return everything EXCEPT the frontmatter to keep it clean
            content = f.read()
            return re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    def build_assertive_prompt(self, user_prompt: str, selected_skills: List[str]) -> str:
        """
        Assembles the final specialized context for the AI.
        'Assertive' context means it is stripped of noise and highly focused.
        """
        specialized_context = ""
        for skill in selected_skills:
            specialized_context += f"\n--- START SPECIALIZED CONTEXT: {skill} ---\n"
            specialized_context += self.disclose_layer_2(skill)
            specialized_context += f"\n--- END SPECIALIZED CONTEXT: {skill} ---\n"

        final_payload = f"""
SYSTEM INSTRUCTIONS:
You are a highly specialized AI. Use the provided context below to answer the user request.
If the context contains specific formatting rules or technical constraints, adhere to them strictly.

{specialized_context}

USER REQUEST:
{user_prompt}
"""
        return final_payload.strip()

# --- DEMONSTRATION LOGIC ---

def setup_demo_environment():
    """Creates dummy .md files to demonstrate the mechanism."""
    os.makedirs("knowledge_base", exist_ok=True)
    
    # Skill 1: Financial Expert
    with open("knowledge_base/finance.md", "w") as f:
        f.write("""---
name: FinanceExpert
description: Use this for calculating tax, interest rates, and loan risks.
---
# Financial Logic
- Always apply a 15% buffer to risk assessments.
- Interest calculation formula: (Principal * Rate * Time) / 100.
- Never give direct investment advice; only provide data analysis.
""")

    # Skill 2: Tech Support
    with open("knowledge_base/tech.md", "w") as f:
        f.write("""---
name: DebugAssistant
description: Use this for diagnosing Python errors and system logs.
---
# Debugging Guidelines
- Check for 'NoneType' errors first.
- If the error is 'ModuleNotFoundError', suggest a pip install.
- Always provide a minimal code fix.
""")

if __name__ == "__main__":
    # 1. Setup the dummy files
    setup_demo_environment()

    # 2. Initialize the Engine (This happens at app startup)
    engine = ProgressiveDisclosureEngine("knowledge_base")

    # 3. Layer 1 Disclosure: The AI "sees" what it can do
    # In a real app, you'd send this to the LLM first or use it for routing.
    print(">>> LAYER 1: AVAILABLE SKILLS")
    print(engine.get_layer_1_context())

    # 4. Simulate an Intent: The User asks about a loan
    user_query = "What is the risk for a $5000 loan at 5% for 2 years?"
    
    # Simple logic to 'auto-disclose' based on keywords 
    # (In OpenClaw, the AI itself would call a 'get_skill' tool here)
    relevant_skills = []
    if "loan" in user_query.lower() or "risk" in user_query.lower():
        relevant_skills.append("FinanceExpert")

    # 5. Layer 2 Disclosure: Build the 'Assertive Context'
    print(f"\n>>> BUILDING CONTEXT FOR SKILLS: {relevant_skills}")
    final_prompt = engine.build_assertive_prompt(user_query, relevant_skills)

    print("\n>>> FINAL ASSERTIVE PROMPT (Sent to LLM):")
    print(final_prompt)
```

------

### Why this creates "Assertive Context"

- **Dynamic Intent Matching:** Instead of providing the `DebugAssistant` instructions when the user is asking about money, the script filters it out entirely.
- **Token Efficiency:** By using **Layer 1** (YAML Metadata) for the initial "check," you save thousands of tokens that would otherwise be wasted on implementation details of irrelevant skills.
- **Modular Knowledge:** You can add 100 new `.md` files to the `knowledge_base` folder, and the script will automatically register them. The AI's "brain" only expands when it identifies a relevant trigger.

### Key Logic in the Code:

- **The Regex (`re.search`):** It targets the standard `---` YAML block. This is the exact mechanism used by OpenClaw to separate "what this is" from "how to do it."
- **The `disclose_layer_2` method:** It acts as the "Tool" an agent would call. In a full agentic loop, the AI would receive the output of `get_layer_1_context` and then emit a command: `USE_SKILL("FinanceExpert")`.

Would you like me to extend this to include a **Layer 3**, where the script can recursively search and "disclose" sub-files referenced inside the `.md` content?
