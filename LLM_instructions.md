# LLM Instructions

## 1. Adherence to the Plan
* Follow `plan.md` document step-by-step without deviating
* Complete tasks in small, incremental steps
* Validate completion of each task before proceeding

## 2. Behavioral Guidelines
* Avoid unnecessary changes to existing code unless instructed
* Make additive changes only; do not improve what isn't broken
* Do not modify dependency versions unless explicitly directed

## 3. Incremental Problem-Solving
* Break large tasks into smaller, manageable sub-tasks
* Always aim for reversible actions (e.g., create backups, avoid destructive edits)

## 4. Best Practices for Code
* Do not add caches, retry loops, or small delays unnecessarily
* Avoid monkey-patching or other risky programming practices

## 5. Error Handling
* Assume that issues are likely user-related, not system-related
* Handle errors gracefully and escalate to the user when stuck

## 6. General Philosophy
* Treat existing working code as sacred
* Isolate and document new features clearly
* Write verbose, detailed Git commit messages to ensure all changes are traceable