# OPEN_QUESTIONS.md

## Blockers
- [ ] 질문: visit flow에서 현재 local autosave로 충분한가, 아니면 약한 오프라인 저장까지 필요한가?
  - 왜 중요한가: mobile-first field workflow에서 네트워크 품질이 낮을 수 있다.
  - 기본 가정: v1은 online-first + local autosave로 간다.
  - 미해결 시 영향: visit form state와 storage 전략이 달라진다.

## Non-blockers
- [ ] 질문: report export는 웹 화면만 제공하면 충분한가?
  - 기본 가정: v1은 web report view만 제공한다.
  - 추후 확인 시점: FE-003 이후

- [ ] 질문: partner review는 read-only 공유 링크로 충분한가?
  - 기본 가정: v1은 single-user 중심이다.
  - 추후 확인 시점: staging feedback 이후

## Business questions
- [ ] 질문: 첫 paying ICP는 buyer agent가 맞는가, 아니면 small investor team이 더 맞는가?
  - 기본 가정: 반복 사용성과 보고서 수요를 고려하면 buyer agent와 small investor team이 개인 구매자보다 우선순위가 높다.
  - 확인 방법: 인터뷰와 유료 파일럿 전환율 비교

- [ ] 질문: 첫 유료 offer는 one-time buyer pack이 맞는가, 아니면 monthly solo pro가 맞는가?
  - 기본 가정: 메인 BM은 반복 사용자의 월 구독이고, one-time pack은 검증과 유입용 보조 상품이다.
  - 확인 방법: landing page 실험과 concierge pilot

## Design gaps
- [ ] 항목: checklist taxonomy의 최종 최소 집합
  - 관련 문서: PRD.md, ADR/ADR-001.md
  - owner: planner / architect

## Release gaps
- [x] 항목: attachment upload failure UX
  - 해결 시점: 2026-03-22
  - 반영 내용: visit는 저장된 상태로 유지하고, 실패한 첨부만 재시도할 수 있게 UX를 보강했다.
