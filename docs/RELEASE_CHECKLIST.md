# RELEASE_CHECKLIST.md

## Pre-merge
- [ ] PRD / ADR / acceptance 문서가 최신이다.
- [ ] 관련 task packet의 `write_scope`와 실제 변경 범위가 일치한다.
- [ ] `npm run web:lint` 통과
- [ ] `npm run api:check` 통과
- [ ] reviewer must-fix 0건

## Pre-staging
- [ ] release notes 초안 작성
- [ ] smoke 대상 flow 확정
- [ ] env/secrets 차이 확인
- [ ] staging deploy command contract 검증
- [ ] attachment upload path 확인
- [ ] rollback draft 작성

## Post-staging
- [ ] staging deploy 성공
- [ ] create project 흐름 통과
- [ ] add property 흐름 통과
- [ ] complete visit 흐름 통과
- [ ] comparison/report 흐름 통과

## Pre-production
- [ ] human approval 완료
- [ ] production release tag 또는 image tag 확정
- [ ] production deploy command contract 검증
- [ ] final staging smoke 재실행
- [ ] rollback procedure 확정
- [ ] reviewer high severity 0건
- [ ] observability entrypoints 준비
- [ ] 승인자와 승인 시각 기록
