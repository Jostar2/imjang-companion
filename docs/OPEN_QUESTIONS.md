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
- [ ] 질문: buyer agent first 가정이 실제 인터뷰와 파일럿 반응에서도 유지되는가?
  - 기본 가정: independent buyer agent가 첫 paying ICP이고, small investor team은 두 번째 세그먼트다.
  - 확인 방법: 5건의 buyer-agent workflow review와 첫 1건의 유료 pilot 반응 확인

## Resolved decisions
- [x] 질문: visit flow에서 local autosave만으로 충분한가, 아니면 partial offline support가 필요한가?
  - 결정: v1은 online-first로 유지하고, 같은 device/browser에서만 browser-local autosave draft restore를 제공한다.
  - 이유: current mobile web MVP 범위 안에서 draft loss를 줄이되, sync/storage/conflict/attachment semantics를 확장하지 않기 위해서다.
  - 재검토 조건: staging 또는 첫 pilot field sessions에서 low-connectivity로 visit completion이 반복적으로 막히면 재검토한다.

- [x] 질문: 첫 paying ICP는 buyer agent가 맞는가, 아니면 small investor team이 더 맞는가?
  - 결정: 첫 paying ICP는 independent buyer agent로 잠근다.
  - 이유: single-operator onboarding이 가장 단순하고, same-day report ROI가 명확하며, v1의 single-user workflow와 가장 잘 맞는다.
  - 재검토 조건: 5건의 buyer-agent workflow review 후 반응이 약하면 small investor team을 다시 올린다.

- [x] 질문: 첫 working offer는 무엇인가?
  - 결정: 첫 working offer는 `2-week founder-led paid pilot`이다.
  - 구성: 1 operator, 최대 2개 active routes, local walkthrough onboarding, same-day support, wrap-up retro.
  - 내부 working ask: `KRW 149,000`
  - 재검토 조건: 첫 3건의 workflow review에서 가격 저항이 반복되면 pilot ask를 다시 조정한다.

## Release gaps
- [ ] 항목: autosave restore를 local walkthrough에서 실제 검증
  - 위험도: medium
  - 확인 필요 시점: 첫 local demo rehearsal 전

- [x] 항목: launch artifact 초안을 실제 파일럿용 내용으로 채우기
  - 해결 시점: 2026-03-23
  - 반영 내용: buyer-agent-first 메시지, founder-led pilot offer, seeded outreach list, and local demo script를 문서에 반영했다.

- [ ] 항목: hosted staging은 파일럿 수요가 확인된 뒤로 미룰지, 아니면 그 전에 꼭 필요한지
  - 기본 가정: 지금은 local-first로 검증하고, 반복 데모나 외부 접근이 필요해질 때 staging을 다시 연다.
  - 확인 필요 시점: 첫 3건의 인터뷰 또는 첫 live pilot 일정이 잡힐 때

- [x] 항목: attachment upload failure UX
  - 해결 시점: 2026-03-22
  - 반영 내용: visit는 저장된 상태로 유지하고, 실패한 첨부만 재시도할 수 있게 UX를 보강했다.
