# OPEN_QUESTIONS.md

## Blockers

- 없음. `offline_support_decision`은 2026-03-23 기준으로 닫는다.
  - 결정: v1은 `online-first + browser-local autosave/restore`만 지원한다.
  - 범위 밖: partial offline queueing, offline attachment upload, cross-device draft recovery.
  - 남는 위험: 저품질 네트워크에서는 draft 복구는 가능해도 서버 저장과 업로드는 막힐 수 있다.

## Non-blockers

- [ ] 질문: summary report를 PDF로 내보내야 하는가?
  - 기본 가정: v1은 웹 report view만 제공한다.
  - 추후 확인 시점: comparison/report 기능 안정화 이후

- [ ] 질문: partner share는 read-only link면 충분한가?
  - 기본 가정: v1은 single-user만 지원한다.
  - 추후 확인 시점: v1 adoption 확인 이후

## Resolved decisions
- [x] 질문: v1에서 autosave-only로 충분한가, 아니면 partial offline support가 필요한가?
  - 결정: v1은 online-first로 유지하고, 같은 device/browser에서만 browser-local autosave draft restore를 제공한다.
  - 이유: 현재 MVP 범위 안에서 draft loss를 줄이되, sync/storage/conflict/attachment semantics를 늘리지 않기 위해서다.
  - 재검토 조건: staging 또는 첫 pilot field sessions에서 low-connectivity로 visit completion이 반복적으로 막히면 재검토한다.
- [x] 질문: 첫 paying ICP는 누구인가?
  - 결정: 첫 paying ICP는 `independent buyer agent`로 잠근다.
  - 이유: single-operator onboarding이 가장 단순하고, same-day report ROI가 명확하며, v1의 single-user workflow와 가장 잘 맞는다.
  - 재검토 조건: 5건의 buyer-agent workflow review 후 반응이 약하면 small investor team을 다시 올린다.
- [x] 질문: 첫 working offer는 무엇인가?
  - 결정: `2-week founder-led paid pilot`
  - 구성: 1 operator, 최대 2개 active routes, founder onboarding, same-day support, wrap-up retro
  - 내부 working ask: `KRW 149,000`
- [x] 항목: checklist taxonomy 최소 집합
  - 결정: v1 required sections는 `property`, `building`, `neighborhood`이고 `redflags`는 optional narrative capture로 유지한다.
  - 관련 문서: PRD.md, ADR-001.md

## Release gaps

- [ ] 항목: autosave restore를 local walkthrough에서 실제 검증
  - 위험도: medium
  - 확인 필요 시점: 첫 local demo rehearsal 전

- [ ] 항목: attachment upload size limit and retry UX를 local walkthrough에서 검증
  - 위험도: medium
  - 확인 필요 시점: 첫 local demo rehearsal 전

- [x] 항목: first payer / first offer / seeded lead list를 founder handoff 수준으로 채우기
  - 해결 시점: 2026-03-23
  - 반영 내용: buyer-agent-first 가정, 2주 pilot offer, and 5 seeded outreach slots를 문서에 반영했다.

- [ ] 항목: hosted staging은 파일럿 수요가 확인된 뒤로 미룰지, 아니면 그 전에 꼭 필요한지
  - 기본 가정: 지금은 local-first로 검증하고, 반복 데모나 외부 접근이 필요해질 때 staging을 다시 연다.
  - 확인 필요 시점: 첫 3건의 인터뷰 또는 첫 live pilot 일정이 잡힐 때
