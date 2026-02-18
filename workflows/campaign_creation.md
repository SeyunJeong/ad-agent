# 캠페인 생성 워크플로우 (Type A) — 8단계 콘텐츠 파이프라인

## 개요

새로운 캠페인을 처음부터 설계하여 실행 가능한 캠페인 플랜을 만드는 워크플로우.
**심층 리서치 → 전략 수립 (셀프 디베이트) → 컨셉 기획 → 제작 → 팩트체크 (필수 게이트) → QA 스코어링 → 채널 세팅 → 분석/피드백** 8단계 전 과정을 커버한다.

```
Phase 0: Deep Research        → DEEP_RESEARCHER
Phase 1: Strategy (Self-Debate) → CAMPAIGN_STRATEGIST
Phase 2: Concept / Ideation   → CONCEPT_PLANNER
Phase 3: Production            → COPYWRITER + VISUAL_DIRECTOR + KEYWORD_AUDIENCE_TEAM
Phase 4: Fact Check ██ 필수 ██ → AD_FACT_CHECKER
Phase 5: QA Scoring            → QA_SCORER + CREATIVE_REVIEWER
Phase 6: Channel Setup         → CHANNEL_TEAM + BID_OPTIMIZER
Phase 7: Analysis + Feedback   → ANALYTICS_TEAM → (다음 이터레이션)
```

---

## 트리거

| 조건 | 예시 | 판단 기준 |
|------|------|----------|
| 신규 캠페인 요청 | "캠페인 만들어줘", "광고 시작하고 싶어" | 처음 시작하는 새 캠페인 |
| 신규 채널 진출 | "네이버 광고 해보고 싶어" | 기존에 없던 채널 추가 |
| 신규 제품/서비스 론칭 | "신제품 광고 플랜 짜줘" | 새 제품의 마케팅 |
| 프로모션/이벤트 캠페인 | "블프 세일 캠페인 짜줘" | 시즌/이벤트 캠페인 |
| 풀 파이프라인 요청 | "캠페인 플랜 만들어줘" | 리서치부터 채널 세팅까지 |

---

## 전체 프로세스 플로우

```
[오너: 캠페인 요청]
         ↓
[TEAM_LEAD] 접수 + 브리프 작성/확인
         ↓
[Phase 0: 심층 리서치] ─── DEEP_RESEARCHER
  → 사전 검증 5개 게이트 통과
  → 시장/경쟁사/타겟/채널 리서치
  → 벤치마크 최신화
  → handoff: research_to_strategist.md
         ↓
[Phase 1: 전략 수립] ─── CAMPAIGN_STRATEGIST
  → 리서치 데이터 기반 전략 설계
  → 셀프 디베이트 (Blue → Red → Defense)
  → handoff: strategy_to_concept.md
         ↓
[Phase 2: 컨셉 기획] ─── CONCEPT_PLANNER
  → 전략 USP → 크리에이티브 컨셉 2-3안
  → 채널별 변주 + A/B 테스트 설계
  → 자체 검증 (7개 체크)
  → handoff: concept_to_production.md
         ↓
[Phase 3: 제작] ─── CREATIVE_TEAM + KEYWORD_AUDIENCE_TEAM
  → 병렬: COPYWRITER(카피) + VISUAL_DIRECTOR(비주얼)
  → KEYWORD_AUDIENCE_TEAM 키워드 리서치 병렬
  → 크로스 리뷰 + CREATIVE_REVIEWER 법적 검수
  → handoff: production_to_factcheck.md
         ↓
[Phase 4: 팩트체크] ██ 필수 게이트 ██ ─── AD_FACT_CHECKER
  → 모든 수치/주장/비교 표현 검증
  → 법규/채널정책 검증
  → PASS → 다음 / FAIL → Phase 3 리턴
  → handoff: factcheck_to_qa.md
         ↓
[Phase 5: QA 스코어링] ─── QA_SCORER + CREATIVE_REVIEWER
  → 5개 지표 × 10점 = 50점 만점 평가
  → PASS (≥35) → Phase 6
  → REVISE (≥30 or 개별<5) → Phase 3 리턴
  → REJECT (<30 or 개별<3) → Phase 2 리턴
         ↓
[Phase 6: 채널 세팅 + 입찰] ─── CHANNEL_TEAM + BID_OPTIMIZER
  → 각 채널 독립 세팅 + 크로스 채널 동기화
  → 입찰/예산 설계
  → 론칭 체크리스트 + 최종 검수
         ↓
[Phase 7: 분석 + 피드백] ─── ANALYTICS_TEAM
  → 성과 모니터링 + 분석 리포트
  → 피드백 루프 → Phase 0/2/3 재진입
         ↓
[TEAM_LEAD] 오너에게 최종 보고 / 이터레이션 관리
```

---

## 단계별 상세

### Step 0: 브리프 확인 (TEAM_LEAD)

**입력**: 오너의 요청
**처리**:
- 캠페인 브리프 필수 항목 확인
- 누락 항목 오너에게 질문
- 브리프 구조화

**필수 확인 항목**:
```
[ ] 비즈니스/제품/서비스 설명
[ ] 캠페인 목표 (인지도/트래픽/전환)
[ ] 타겟 오디언스
[ ] 총 예산 및 기간
[ ] 선호 채널 (있을 경우)
[ ] 경쟁사 정보 (있을 경우)
[ ] 랜딩 페이지 URL
[ ] 기존 소재 존재 여부
[ ] 특별 요청사항
```

---

### Phase 0: 심층 리서치 (DEEP_RESEARCHER)

**입력**: 구조화된 캠페인 브리프
**에이전트**: `agents/content-pipeline/DEEP_RESEARCHER.md`
**처리**:
```
Step 0: 사전 검증 (config/researcher_prechecklist.md)
  → 5개 게이트 통과 확인 (GO / CONDITIONAL GO / NO-GO)

Step 1: 기존 데이터 확인
  → archive/, config/templates.md, config/kpi_definitions.md

Step 2-6: 시장/경쟁사/타겟/채널/벤치마크 리서치
  → 웹 서치 필수
  → 출처 A/B 등급 70% 이상
```
**출력**: Deep Research Report
**핸드오프**: `handoff/research_to_strategist.md`
**TEAM_LEAD 검수**: 리서치 범위/깊이 적정성, 출처 신뢰도

---

### Phase 1: 전략 수립 (CAMPAIGN_STRATEGIST)

**입력**: Deep Research Report + 캠페인 브리프 (`handoff/research_to_strategist.md`)
**에이전트**: `agents/CAMPAIGN_STRATEGIST.md`
**처리**:
```
Step 1: 리서치 데이터 기반 비즈니스 분석
Step 2: 채널 믹스 설계 (리서치 벤치마크 반영)
Step 3: 예산 배분 전략
Step 4: KPI 목표 설정
Step 5: 셀프 디베이트 (Blue → Red → Defense)
  → Red Team은 리서치 데이터의 한계도 공격 포인트로 활용
Step 6: 최종 전략 확정
```
**출력**: 캠페인 전략서 (디베이트 로그 + 리서치 참조 포함)
**핸드오프**: `handoff/strategy_to_concept.md`
**TEAM_LEAD 검수**: 전략 8대 요소 완결성, 리서치 데이터 활용도

**전략서 필수 포함 항목**:
```
[ ] 캠페인 목표 및 KPI (리서치 벤치마크 기반)
[ ] 타겟 오디언스 프로파일 (리서치 인사이트 반영)
[ ] 채널 믹스 및 채널별 역할 (리서치 채널 트렌드 반영)
[ ] 예산 배분 (채널별/기간별)
[ ] 핵심 메시지 및 USP
[ ] 퍼널 전략
[ ] 경쟁 분석 요약 (리서치 경쟁사 분석 기반)
[ ] 리스크 평가 (Red Team 검증 결과)
[ ] 셀프 디베이트 로그
```

---

### Phase 2: 컨셉 기획 (CONCEPT_PLANNER)

**입력**: 캠페인 전략서 (`handoff/strategy_to_concept.md`)
**에이전트**: `agents/content-pipeline/CONCEPT_PLANNER.md`
**처리**:
```
Step 1: 입력 데이터 분석 (전략 USP + 리서치 인사이트)
Step 2: 크리에이티브 앵글 도출 (감정적 트리거 매핑)
Step 3: 컨셉 2-3안 개발 (Safe / Bold / Wild Card)
Step 4: 자체 검증 (7개 체크리스트)
Step 5: 컨셉 브리프 완성
```
**출력**: Creative Concept Brief (2-3안 + 채널별 변주 + A/B 설계)
**핸드오프**: `handoff/concept_to_production.md`
**TEAM_LEAD 검수**: 전략 정합성, 컨셉 차별화, 제작 가능성

---

### Phase 3: 제작 (CREATIVE_TEAM + KEYWORD_AUDIENCE_TEAM)

**입력**: Creative Concept Brief (`handoff/concept_to_production.md`)
**에이전트**: COPYWRITER, VISUAL_DIRECTOR, CREATIVE_REVIEWER + KEYWORD_AUDIENCE_TEAM
**처리**:
```
병렬 실행 1:
├── COPYWRITER → 채널별 카피 세트 + A/B 변형
├── VISUAL_DIRECTOR → 크리에이티브 가이드 + thread-team 소재 요청
└── KEYWORD_AUDIENCE_TEAM → 키워드/오디언스 리서치
    ├── SEARCH_RESEARCHER → 네이버/구글 키워드
    ├── AUDIENCE_RESEARCHER → 카카오/메타 오디언스
    └── TREND_ANALYST → 시즌/경쟁 트렌드

크로스 리뷰:
└── COPYWRITER ↔ VISUAL_DIRECTOR: 메시지/비주얼 정합성

법적 검수:
└── CREATIVE_REVIEWER → PASS/REVISE/REJECT (최대 2회 피드백)

최종 패키징:
└── 검수 완료 소재 패키지 + 자체 플래그 식별
```
**출력**: 검수 완료된 카피 세트 + 크리에이티브 가이드 + 키워드 리서치
**핸드오프**: `handoff/production_to_factcheck.md`
**TEAM_LEAD 검수**: 컨셉 충실도, 채널 규격 준수, 법적 검수 통과

**thread-team 연동 판단**:
```
이미지/영상 소재 필요 → VISUAL_DIRECTOR가 thread-team에 요청
  → handoff/creative_to_thread.md 양식으로 전달
카피만 필요 → COPYWRITER 자체 처리
```

---

### Phase 4: 팩트체크 ██ 필수 게이트 ██ (AD_FACT_CHECKER)

**입력**: 크리에이티브 패키지 (`handoff/production_to_factcheck.md`)
**에이전트**: `agents/content-pipeline/AD_FACT_CHECKER.md`
**처리**:
```
Step 1: 검증 대상 추출 (수치/최상급/효능/비교/할인/인증/통계)
Step 2: 각 항목 검증 (VERIFIED / UNVERIFIED / FALSE)
Step 3: 법규 검증 (표시광고법 + 업종별 + 채널 정책)
Step 4: 종합 판정 + Data Accuracy 스코어 산출
```

**판정**:
| 결과 | 조건 | 액션 |
|------|------|------|
| **PASS** | 전항 VERIFIED + 법규 통과 | → Phase 5 |
| **CONDITIONAL PASS** | UNVERIFIED 1-2건 (사소) | → Phase 5 (감점 반영) |
| **FAIL** | FALSE 1건 이상 또는 법규 위반 | → **Phase 3 리턴** |

> **이 게이트는 TEAM_LEAD도 override 불가. FAIL 시 반드시 Phase 3로 리턴.**

**출력**: Fact Check Report + Data Accuracy 스코어 ({n}/10)
**핸드오프**: `handoff/factcheck_to_qa.md` (PASS/CONDITIONAL PASS 시)

---

### Phase 5: QA 스코어링 (QA_SCORER + CREATIVE_REVIEWER)

**입력**: 팩트체크 완료 크리에이티브 (`handoff/factcheck_to_qa.md`)
**에이전트**: `agents/content-pipeline/QA_SCORER.md` + CREATIVE_REVIEWER
**처리**:
```
QA_SCORER 자체 평가 (3개 지표):
├── Strategy Alignment: {n}/10
├── Creative Impact: {n}/10
└── Channel Optimization: {n}/10

외부 수신 (2개 지표):
├── Data Accuracy: {n}/10 (AD_FACT_CHECKER)
└── Legal Compliance: {n}/10 (CREATIVE_REVIEWER)

종합: 50점 만점 스코어카드
```

**판정** (`config/ad_quality_scoring.md` 기준):
| 판정 | 조건 | 액션 |
|------|------|------|
| **PASS** | 총점 >= 35 AND 모든 개별 >= 5 | → Phase 6 진행 |
| **REVISE** | 총점 >= 30 OR 개별 하나라도 < 5 | → **Phase 3 리턴** |
| **REJECT** | 총점 < 30 OR 개별 하나라도 < 3 | → **Phase 2 리턴** |

**특별 규칙**:
- Data Accuracy FAIL → 총점 무관 REJECT
- Legal Compliance < 3 → 총점 무관 REJECT
- 3회 연속 REVISE → TEAM_LEAD 에스컬레이션

**출력**: QA Score Card (50점 만점)
**리턴 시 전달**: 스코어카드 + 구체적 수정 지시 + 원본 전략/리서치 참조

---

### Phase 6: 채널 세팅 + 입찰/예산 (CHANNEL_TEAM + BID_OPTIMIZER)

**입력**: QA PASS된 크리에이티브 + 키워드/오디언스 리서치
**에이전트**: CHANNEL_TEAM (4명) + BID_OPTIMIZER
**처리**:
```
병렬 실행:
├── BID_OPTIMIZER → 채널별 입찰 전략 + 예산 페이싱
└── CHANNEL_TEAM 독립 세팅:
    ├── NAVER_SPECIALIST → 파워링크/쇼핑/브랜드검색
    ├── KAKAO_SPECIALIST → 카카오 모먼트/메시지
    ├── META_SPECIALIST → 메타 캠페인 + 픽셀/CAPI
    └── GOOGLE_SPECIALIST → 구글 캠페인 + GA4

크로스 채널 동기화:
├── UTM 파라미터 규칙 통일
├── 트래킹 코드 충돌 확인
├── 론칭 시간 동기화
└── 채널 간 메시지 일관성 확인

최종 검수 (TEAM_LEAD + ANALYTICS_TEAM):
├── TEAM_LEAD → 전체 정합성 확인
├── DATA_MONITOR → 트래킹 정상 작동 + 대시보드 설정
└── INSIGHT_ANALYST → KPI 모니터링 기준 설정
```

**finance 연동 판단**:
```
월 예산 500만원 이상 → finance 팀 승인 필요
  → handoff/budget_to_finance.md
월 예산 500만원 미만 → TEAM_LEAD 승인으로 진행
```

**출력**: 채널별 세팅 완료 + 입찰 전략 + 론칭 체크리스트

---

### Phase 7: 분석 + 피드백 루프 (ANALYTICS_TEAM)

**입력**: 캠페인 실행 데이터
**에이전트**: DATA_MONITOR + INSIGHT_ANALYST
**처리**:
```
지속 모니터링 (DATA_MONITOR):
├── 일일 성과 스냅샷
├── 이상 감지 (KPI 급변, 비용 이상 등)
└── 이상 시 즉시 TEAM_LEAD 알림

정기 분석 (INSIGHT_ANALYST):
├── 주간 성과 리포트
├── 채널별/크리에이티브별 상세 분석
├── A/B 테스트 결과 분석
└── 최적화 제안

피드백 루프 판단 (config/feedback_loop.md 기준):
├── KPI 달성률 < 50% → Phase 0 재진입 (전략 재검토)
├── CTR/CVR 벤치마크 하회 + 전략 유효 → Phase 2 재진입 (컨셉 변경)
├── 미세 조정만 필요 → Phase 3 재진입 (카피 수정)
└── 성과 양호 → 유지 + 지속 최적화
```

**핸드오프**: `handoff/analysis_to_planning.md` (재진입 시)
**출력**: 성과 리포트 + 피드백 데이터 + 다음 이터레이션 권고

---

## 리턴 루프 관리

### QA 리턴 (Phase 5 → Phase 2/3)

```
리턴 횟수 제한: 최대 3회
동일 지적 반복: 2회 시 TEAM_LEAD 개입
리턴 시 전달: 스코어카드 + 수정 지시 + 원본 참조

REVISE (Phase 3 리턴):
  → COPYWRITER/VISUAL_DIRECTOR에 수정 지시
  → 컨셉 유지, 카피/비주얼만 수정
  → Phase 4 (팩트체크)부터 재실행

REJECT (Phase 2 리턴):
  → CONCEPT_PLANNER에 재기획 요청
  → 전략 유지, 컨셉 변경
  → Phase 3 (제작)부터 재실행
```

### 성과 피드백 (Phase 7 → Phase 0/2/3)

```
Phase 0 재진입: 전략 수준 재검토 필요 시
  → DEEP_RESEARCHER가 Delta 리서치 (전체 재수행 X)

Phase 2 재진입: 컨셉 수준 변경 필요 시
  → CONCEPT_PLANNER가 이전 성과 기반 신규 컨셉

Phase 3 재진입: 미세 조정만 필요 시
  → COPYWRITER가 A/B 테스트 기반 카피 최적화
```

---

## 에러 처리

### 브리프 정보 부족
```
캠페인 설계를 위해 추가 정보가 필요합니다:
1. {누락 항목 1}
2. {누락 항목 2}
이 정보가 있으면 더 정확한 전략을 세울 수 있어요.
```

### 리서치 사전 검증 실패 (NO-GO)
```
리서치 사전 검증에서 다음 게이트가 차단되었습니다:
- {BLOCK 게이트}: {사유}
해결 방법: {필요한 조치}
```

### 예산-목표 불일치
```
요청하신 목표({목표})를 달성하기 위한 최소 예산은 {금액}원입니다.
현재 예산({금액}원)으로 가능한 옵션:
1. 목표 하향 조정: {조정된 목표}
2. 채널 축소: {N}개 채널로 집중
3. 기간 단축: {N}주로 테스트 먼저
```

### 팩트체크 FAIL
```
AD_FACT_CHECKER가 다음 항목에서 FAIL 판정했습니다:
- 항목: {검증 실패 항목}
- 사유: {구체적 사유}
- 수정 필요: {수정 방향}
→ Phase 3 (Production)으로 리턴합니다.
```

### QA 스코어 미달
```
QA 스코어: {total}/50 (기준: 35점)
미달 지표: {지표명} {score}/10
판정: {REVISE/REJECT}
→ Phase {2/3}으로 리턴합니다.
수정 지시: {구체적 수정 사항}
```

---

## 산출물 템플릿

### 최종 캠페인 플랜 (오너 보고용)
```
# 캠페인 플랜: {캠페인명}

## 1. 캠페인 개요
- 목표: {목표}
- 기간: {시작일} ~ {종료일}
- 총 예산: {금액}원

## 2. 리서치 요약 (Phase 0)
- 시장 규모: {TAM/SAM/SOM}
- 핵심 경쟁사: {top 3}
- 타겟 인사이트: {핵심 발견}

## 3. 전략 요약 (Phase 1, 셀프 디베이트 결과 반영)
- 핵심 메시지 (USP): {메시지}
- 타겟: {타겟 요약}
- 채널 구성: {채널 목록}
- Red Team 검증 결과: {주요 리스크 + 보완 내용}

## 4. 크리에이티브 컨셉 (Phase 2)
- 채택 컨셉: {컨셉명} ({유형})
- 핵심 아이디어: {한 줄}
- A/B 테스트 설계: {테스트 변수}

## 5. 채널별 실행 계획 (Phase 3+6)
| 채널 | 담당 | 광고 유형 | 예산 | KPI |
|------|------|----------|------|-----|
{채널별 상세}

## 6. 예산 배분
{채널별/기간별 예산 표}

## 7. KPI 목표
{채널별 KPI 목표 표}

## 8. 크리에이티브 미리보기 (Phase 3)
{채널별 주요 카피/소재 미리보기}

## 9. 품질 검증 결과 (Phase 4+5)
- 팩트체크: {PASS/CONDITIONAL PASS}
- QA 스코어: {total}/50
- 법적 검수: {PASS}

## 10. 일정
{론칭까지 타임라인}

## 11. 리스크 및 대응
{Red Team 검증 결과 + 리서치 기반 리스크}

## 12. 모니터링 + 피드백 루프 (Phase 7)
- DATA_MONITOR: 일일 스냅샷 + 이상 감지
- INSIGHT_ANALYST: 주간 리포트
- 피드백 루프: 성과 기반 자동 재진입 판단

## 13. 다음 단계
- 오너 승인 후 론칭
- 론칭 후 {N}일 뒤 첫 성과 리포트
- 피드백 루프 기반 이터레이션 관리
```

---

## 모듈별 호출 (부분 실행)

| 오너 명령 | 실행 범위 | 시작 Phase |
|----------|----------|-----------|
| "캠페인 플랜 만들어줘" | 풀 파이프라인 (Phase 0-6) | Phase 0 |
| "시장 리서치해줘" | Phase 0만 | Phase 0 |
| "광고 전략 수립해줘" | Phase 0+1 | Phase 0 |
| "크리에이티브 컨셉 잡아줘" | Phase 2만 | Phase 2 |
| "광고 카피 만들어줘" | Phase 3만 | Phase 3 |
| "팩트체크해줘" | Phase 4만 | Phase 4 |
| "캠페인 분석해줘" | Phase 7 | Phase 7 |

---

## 참고 파일

| 파일 | 용도 |
|------|------|
| `TEAM.md` | 팀 구성, 입출력 정의 |
| `config/channels.md` | 채널별 세팅 가이드 |
| `config/kpi_definitions.md` | KPI 정의 및 벤치마크 |
| `config/templates.md` | 업종별 캠페인 템플릿 |
| `config/ad_quality_scoring.md` | 5점 스코어링 루브릭 |
| `config/researcher_prechecklist.md` | 리서치 사전 검증 5개 게이트 |
| `config/feedback_loop.md` | 피드백 루프 메커니즘 |
| `agents/content-pipeline/DEEP_RESEARCHER.md` | 심층 리서치 에이전트 |
| `agents/content-pipeline/CONCEPT_PLANNER.md` | 컨셉 기획 에이전트 |
| `agents/content-pipeline/AD_FACT_CHECKER.md` | 팩트 체커 에이전트 |
| `agents/content-pipeline/QA_SCORER.md` | 품질 스코어러 에이전트 |
| `handoff/research_to_strategist.md` | Phase 0→1 핸드오프 |
| `handoff/strategy_to_concept.md` | Phase 1→2 핸드오프 |
| `handoff/concept_to_production.md` | Phase 2→3 핸드오프 |
| `handoff/production_to_factcheck.md` | Phase 3→4 핸드오프 |
| `handoff/factcheck_to_qa.md` | Phase 4→5 핸드오프 |
| `handoff/analysis_to_planning.md` | Phase 7→0/2 피드백 루프 |
| `handoff/strategy_to_keyword_team.md` | 전략→키워드팀 (기존) |
| `handoff/keyword_team_to_creative_team.md` | 키워드팀→크리에이티브팀 (기존) |
| `handoff/creative_team_to_channel_team.md` | 크리에이티브팀→채널팀 (기존) |
