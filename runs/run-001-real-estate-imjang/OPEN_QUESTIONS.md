# OPEN_QUESTIONS.md

## Blockers

- [ ] 질문: v1에서 draft-save는 단순 autosave로 충분한가, 아니면 약한 오프라인 지원까지 필요한가?
  - 왜 중요한가: mobile field visit flow에서 네트워크 품질이 낮을 수 있다.
  - 기본 가정: v1은 online-first + autosave로 간다.
  - 미해결 시 영향: visit form UX와 storage 전략이 크게 달라진다.

## Non-blockers

- [ ] 질문: summary report를 PDF로 내보내야 하는가?
  - 기본 가정: v1은 웹 report view만 제공한다.
  - 추후 확인 시점: comparison/report 기능 안정화 이후

- [ ] 질문: partner share는 read-only link면 충분한가?
  - 기본 가정: v1은 single-user만 지원한다.
  - 추후 확인 시점: v1 adoption 확인 이후

## Design gaps

- [ ] 항목: checklist 항목의 기본 taxonomy
  - 관련 문서: PRD.md, ADR-001.md
  - owner: planner / architect

## Release gaps

- [ ] 항목: attachment upload size and failure UX
  - 위험도: medium
  - 확인 필요 시점: staging smoke 정의 전
