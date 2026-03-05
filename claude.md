# GitBook 프로젝트 — Claude 컨텍스트

> 이 파일은 SUMMARY.md 또는 .md 파일 변경 시 자동으로 갱신됩니다.
> 마지막 갱신: 2026-03-05 22:17:38

## 프로젝트 개요

GitHub 연동 GitBook 기반 **Claude Code 한글 강의 교재** 프로젝트.
- 저장소: github.com/yonghyeokrhee/claude-savvy
- GitBook과 GitHub main 브랜치가 실시간 동기화됨

## 작성 규칙

- 모든 문서는 **한글**로 작성
- 새 페이지 추가 시 반드시 `SUMMARY.md`에 등록
- 파일명은 kebab-case 사용 (예: `core-concepts.md`)
- `claude.md`는 자동 생성 파일 — 직접 수정 금지
- `agents.md`는 `claude.md`의 symlink

## 현재 목차 (SUMMARY.md)

```
# Summary

* [Claude Code 소개](introduction.md)
* [시작하기](getting-started.md)
* [핵심 개념](core-concepts.md)
* [팁 & 모범 사례](best-practices.md)

## 강의

* [Skills](skills.md)
  * [Skill 직접 만들기](skills-practice.md)
* [Sub-Agent](sub-agent.md)
  * [Sub-Agent 실습](practice/sub-agent.md)
  * [Sub-Agent + Skill 활용](practice/sub-agent-skill.md)
  * [Sub-Agent 직접 만들기](practice/sub-agent-create.md)
* [Workflow](workflow.md)
* [MCP](mcp.md)

## 실습

* [CLAUDE.md 만들기](practice/claude-md.md)
```

## 루트 페이지 파일

agents.md best-practices.md core-concepts.md getting-started.md introduction.md mcp.md README.md skills-practice.md skills.md sub-agent.md SUMMARY.md workflow.md 

## practice/ 실습 파일

practice/.claude/agents/campaign-analyzer.md practice/.claude/skills/mop-report/SKILL.md practice/.claude/skills/support-explorer/SKILL.md practice/claude-md.md practice/CLAUDE.md practice/data/budget-usage.md practice/data/campaign-search.md practice/data/campaign-shopping.md practice/data/report-feb-2026.md practice/sub-agent-create.md practice/sub-agent-skill.md practice/sub-agent.md 

## 주요 명령

```bash
# 변경사항 푸시 (GitBook 자동 반영)
git push origin main

# 로컬 상태 확인
git status
```
