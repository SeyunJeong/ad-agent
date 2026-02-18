# 핸드오프: AD_FACT_CHECKER → QA_SCORER

> **Phase**: 4 → 5
> **발신**: AD_FACT_CHECKER (content-pipeline)
> **수신**: QA_SCORER (content-pipeline) + CREATIVE_REVIEWER (creative-team)
> **목적**: 팩트체크 통과한 크리에이티브를 종합 품질 평가에 전달

---

## 캠페인 정보

| 항목 | 내용 |
|------|------|
| 캠페인명 | {campaign_name} |
| 업종 | {industry} |
| 이터레이션 | #{iteration} |
| 팩트체크 판정 | {PASS / CONDITIONAL PASS} |

> **참고**: FAIL 판정 시 이 핸드오프는 생성되지 않습니다 (Phase 3 리턴).

---

## 1. 팩트체크 리포트 요약

### 종합 판정: {PASS / CONDITIONAL PASS}
### Data Accuracy 스코어: {n}/10

### 검증 결과 요약
| # | 카피 원문 | 유형 | 판정 | 비고 |
|---|----------|------|------|------|
| 1 | "{카피}" | {유형} | VERIFIED | 출처: {source} |
| 2 | "{카피}" | {유형} | VERIFIED | 출처: {source} |
| {n} | "{카피}" | {유형} | {UNVERIFIED} | 수정 제안: {대안} |

### 법규 검증 요약
| 항목 | 판정 |
|------|------|
| 표시광고법 | {PASS} |
| 업종 규제 | {PASS} |
| 네이버 정책 | {PASS} |
| 카카오 정책 | {PASS} |
| 메타 정책 | {PASS} |
| 구글 정책 | {PASS} |

### CONDITIONAL PASS 시 수정 필요 사항
| # | 원문 | 수정 제안 | 심각도 |
|---|------|----------|--------|
| 1 | "{원문}" | "{수정안}" | {보통} |

> CONDITIONAL PASS 항목은 QA_SCORER가 종합 판단 시 감점 반영

---

## 2. 크리에이티브 전문 (검증 완료본)

### 네이버
| 유형 | 헤드라인 | 설명/본문 | 변형 | 팩트체크 |
|------|---------|----------|------|---------|
| 파워링크 | "{headline}" | "{description}" | A | PASS |
| 파워링크 | "{headline}" | "{description}" | B | PASS |
| 쇼핑 | "{title}" | "{description}" | A | PASS |

### 카카오
| 유형 | 헤드라인 | 설명/본문 | 변형 | 팩트체크 |
|------|---------|----------|------|---------|
| 비즈보드 | "{headline}" | "{description}" | A | PASS |
| 메시지 | "{title}" | "{body}" | A | PASS |

### 메타
| 유형 | 헤드라인 | 본문 | CTA | 변형 | 팩트체크 |
|------|---------|------|-----|------|---------|
| 피드 | "{headline}" | "{body}" | {cta} | A | PASS |
| 릴스 | "{overlay}" | "{caption}" | {cta} | A | PASS |

### 구글
| 유형 | 헤드라인 | 설명 | 변형 | 팩트체크 |
|------|---------|------|------|---------|
| RSA | H1/H2/H3 | D1/D2 | A | PASS |
| 디스플레이 | "{headline}" | "{description}" | A | PASS |

---

## 3. 참조 자료 (QA 평가용)

### 전략 문서 요약
- **USP**: {핵심 USP}
- **타겟**: {핵심 타겟}
- **Self-Debate 결론**: {최종 전략 방향}
- **Red Team 반영 사항**: {크리에이티브에 반영되어야 할 항목}

### 컨셉 브리프 요약
- **채택 컨셉**: {컨셉명 + 유형}
- **핵심 아이디어**: {한 줄}
- **감정적 트리거**: {트리거 유형}
- **톤 앤 매너**: {톤}

### 채널 규격 참조
{config/channels.md 주요 내용 요약}

---

## 4. QA_SCORER 평가 요청

### 평가 필요 지표

| # | 지표 | 평가자 | 입력 |
|---|------|--------|------|
| 1 | Strategy Alignment | **QA_SCORER** | 전략 문서 + 크리에이티브 |
| 2 | Data Accuracy | AD_FACT_CHECKER (이미 완료) | **{n}/10** |
| 3 | Creative Impact | **QA_SCORER** | 크리에이티브 전문 |
| 4 | Channel Optimization | **QA_SCORER** | 크리에이티브 + 채널 규격 |
| 5 | Legal Compliance | **CREATIVE_REVIEWER** | 크리에이티브 + 법적 검토 |

### CREATIVE_REVIEWER 요청
- Legal Compliance 스코어 ({n}/10) 산출 필요
- 기존 법적 검토 결과 업데이트 필요 시 재검토

---

## 5. 이전 리턴 이력 (해당 시)

| # | 이터레이션 | QA 총점 | 판정 | 주요 수정 |
|---|----------|---------|------|----------|
| 1 | #{prev} | {score}/50 | {REVISE/REJECT} | {수정 사항} |

> 이전 리턴이 있는 경우, QA_SCORER는 동일 문제가 개선되었는지 중점 확인

---

## QA_SCORER 요청사항

1. `config/ad_quality_scoring.md` 루브릭에 따라 **5개 지표 채점**해주세요
2. **총점 + 개별 점수** 기준으로 PASS/REVISE/REJECT 판정해주세요
3. REVISE/REJECT 시 **구체적 수정 지시**를 포함해주세요
4. PASS 시 Phase 6 (Channel Setup) 진행을 TEAM_LEAD에 보고해주세요
5. 스코어카드를 `config/ad_quality_scoring.md` 형식으로 작성해주세요
