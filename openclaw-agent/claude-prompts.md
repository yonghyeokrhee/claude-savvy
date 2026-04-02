# Claude Code Prompts for claude-savvy

## 1) Improve a page
```text
You are editing a GitBook documentation repository.
Project root: /Users/yong/claude-savvy

Task:
- Improve the target page for clarity, structure, and consistency
- Preserve technical meaning
- Keep style practical and concise
- Update related links or SUMMARY.md only if needed

Before finishing:
- Summarize changed files
- Mention any follow-up suggestions
```

## 2) Restructure a section
```text
You are maintaining a GitBook repo.
Reorganize the target section so navigation is clearer and duplication is reduced.

Requirements:
- Keep SUMMARY.md consistent
- Preserve existing meaning
- Avoid unnecessary rewrites
- Keep headings and filenames intuitive

Before finishing:
- Report the new structure
- List any moved/renamed files
```

## 3) Release/publish prep
```text
Prepare this GitBook repo for publish.

Do:
- inspect changed docs
- fix broken headings/links if found
- ensure SUMMARY.md matches navigation
- propose a clean commit summary

Do not push.
Only prepare the repo and summarize readiness.
```
