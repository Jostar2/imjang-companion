# OPEN_QUESTIONS.md

## Blockers
- 없음. `offline_support_decision`은 2026-03-23 기준으로 닫는다.
  - 결정: v1은 `online-first + browser-local autosave/restore`만 지원한다.
  - 범위 밖: partial offline queueing, offline attachment upload, cross-device draft recovery.
  - 남는 위험: 저품질 네트워크에서는 draft 복구는 가능해도 서버 저장과 업로드는 막힐 수 있다.

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

## Resolved decisions
- [x] 질문: visit flow에서 local autosave만으로 충분한가, 아니면 partial offline support가 필요한가?
  - 결정: v1은 online-first로 유지하고, 같은 device/browser에서만 browser-local autosave draft restore를 제공한다.
  - 이유: current mobile web MVP 범위 안에서 draft loss를 줄이되, sync/storage/conflict/attachment semantics를 확장하지 않기 위해서다.
  - 재검토 조건: staging 또는 첫 pilot field sessions에서 low-connectivity로 visit completion이 반복적으로 막히면 재검토한다.

## Release gaps
- [ ] 항목: autosave restore를 local walkthrough에서 실제 검증
  - 위험도: medium
  - 확인 필요 시점: 첫 local demo rehearsal 전

- [ ] 항목: launch artifact 초안을 실제 파일럿용 내용으로 채우기
  - 필요한 산출물: landing page copy, onboarding path, analytics event map, support runbook, paid pilot contact list
  - 확인 필요 시점: paid pilot outreach 시작 전

- [ ] 항목: hosted staging은 파일럿 수요가 확인된 뒤로 미룰지, 아니면 그 전에 꼭 필요한지
  - 기본 가정: 지금은 local-first로 검증하고, 반복 데모나 외부 접근이 필요해질 때 staging을 다시 연다.
  - 확인 필요 시점: 첫 3건의 인터뷰 또는 첫 live pilot 일정이 잡힐 때

- [x] 항목: attachment upload failure UX
  - 해결 시점: 2026-03-22
  - 반영 내용: visit는 저장된 상태로 유지하고, 실패한 첨부만 재시도할 수 있게 UX를 보강했다.
