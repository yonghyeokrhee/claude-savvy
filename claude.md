# GitBook 프로젝트 — Claude 컨텍스트

> 이 파일은 SUMMARY.md 또는 .md 파일 변경 시 자동으로 갱신됩니다.
> 마지막 갱신: 2026-03-05 21:41:41

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

## 강의

* [Skills](skills.md)
* [Sub-Agent](sub-agent.md)
* [Workflow](workflow.md)
* [MCP](mcp.md)

## 실습

* [CLAUDE.md 실습](practice/CLAUDE.md)
* [2월 성과 데이터](practice/data/feb-2026.csv)
```

## 루트 페이지 파일

agent.md agents.md best-practices.md core-concepts.md getting-started.md introduction.md mcp.md README.md skills.md sub-agent.md SUMMARY.md workflow.md 

## practice/ 실습 파일

practice/CLAUDE.md 

## 주요 명령

```bash
# 변경사항 푸시 (GitBook 자동 반영)
git push origin main

# 로컬 상태 확인
git status
```
