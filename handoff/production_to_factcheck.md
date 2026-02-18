# 핸드오프: Production Team → AD_FACT_CHECKER

> **Phase**: 3 → 4
> **발신**: CREATIVE_TEAM (COPYWRITER + VISUAL_DIRECTOR + CREATIVE_REVIEWER)
> **수신**: AD_FACT_CHECKER (content-pipeline)
> **목적**: 완성된 크리에이티브를 사실 검증(필수 게이트)에 제출

---

## 캠페인 정보

| 항목 | 내용 |
|------|------|
| 캠페인명 | {campaign_name} |
| 업종 | {industry} |
| 목표 | {objective} |
| 이터레이션 | #{iteration} |
| CREATIVE_REVIEWER 법적 검토 | {PASS / PASS with notes} |

---

## 1. 검증 대상 크리에이티브

### 네이버
| 유형 | 헤드라인 | 설명/본문 | 변형 |
|------|---------|----------|------|
| 파워링크 | "{headline}" | "{description}" | A/B/C |
| 쇼핑 | "{title}" | "{description}" | A/B |
| 브랜드검색 | "{headline}" | "{description}" | - |

### 카카오
| 유형 | 헤드라인 | 설명/본문 | 변형 |
|------|---------|----------|------|
| 비즈보드 | "{headline}" | "{description}" | A/B |
| 디스플레이 | "{headline}" | "{description}" | A/B |
| 메시지 | "{title}" | "{body}" | A/B |

### 메타
| 유형 | 헤드라인 | 본문 | CTA | 변형 |
|------|---------|------|-----|------|
| 피드 | "{headline}" | "{body}" | {cta} | A/B/C |
| 릴스 | "{overlay}" | "{caption}" | {cta} | A/B |
| 스토리 | "{overlay}" | - | {cta} | A/B |

### 구글
| 유형 | 헤드라인(들) | 설명(들) | 변형 |
|------|-------------|----------|------|
| RSA | H1/H2/H3 | D1/D2 | A/B |
| 디스플레이 | "{headline}" | "{description}" | A/B |
| 유튜브 | "{script_summary}" | - | A/B |

---

## 2. 검증 요청 항목

### 자동 플래그 (COPYWRITER 자체 식별)
| # | 카피 원문 | 유형 | 주장 | 출처 (있으면) |
|---|----------|------|------|-------------|
| 1 | "{카피}" | {수치/최상급/비교/etc.} | {무엇을 주장하는가} | {출처 or 없음} |
| 2 | "{카피}" | | | |

> COPYWRITER가 자체적으로 검증 필요 항목을 식별하여 표시합니다.
> AD_FACT_CHECKER는 이 목록 외에도 추가 플래그 항목을 독립적으로 식별해야 합니다.

---

## 3. 참조 자료

### 전략 문서 (검증 맥락용)
- USP: {핵심 USP}
- 타겟: {핵심 타겟}
- 주요 주장 근거: {전략에서 사용된 데이터}

### 리서치 데이터 (출처 확인용)
- 시장 데이터 출처: {DEEP_RESEARCHER 리포트 참조}
- 벤치마크 출처: {config/kpi_definitions.md}
- 경쟁사 데이터 출처: {DEEP_RESEARCHER 리포트 참조}

### CREATIVE_REVIEWER 법적 검토 결과
```
판정: {PASS / PASS with notes}
주의사항: {법적 주의 필요 항목}
필수 고지: {포함되어야 할 고지사항}
```

---

## 4. 업종별 특수 검증 요청

> 해당 업종에 따라 체크

- [ ] **금융**: 투자 위험 고지 포함 여부
- [ ] **건강/의료**: 의료행위 암시 표현 없음 확인
- [ ] **식품**: 건강기능식품 면책 고지 포함
- [ ] **화장품**: 기능성 표시 기준 준수
- [ ] **교육**: 합격률/성과 산정 기준 명시
- [ ] **부동산**: 면적/가격 표시 기준 준수
- [ ] **기타**: {특수 검증 항목}

---

## 5. 일정

| 항목 | 일시 |
|------|------|
| 제출일 | {date} |
| 검증 완료 희망일 | {date} |
| Phase 5 (QA) 예정일 | {date} |

---

## AD_FACT_CHECKER 요청사항

1. COPYWRITER가 식별한 플래그 외에 **추가 플래그 항목을 독립적으로 식별**해주세요
2. 모든 검증 항목에 **출처와 검증 방법을 명시**해주세요
3. **CONDITIONAL PASS 시 수정 제안**을 구체적으로 작성해주세요
4. **Data Accuracy 스코어 ({n}/10)** 를 산출하여 QA_SCORER에 전달해주세요
5. 검증 완료 후 `handoff/factcheck_to_qa.md`로 QA에 전달해주세요
