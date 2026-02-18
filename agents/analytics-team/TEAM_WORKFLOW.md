# Analytics Team - 팀 워크플로우

## 팀 개요

분석 팀(Analytics Team)은 퍼포먼스 마케팅 팀의 **데이터 두뇌** 역할을 한다.
모든 의사결정의 기반이 되는 정확한 데이터를 제공하고,
그 데이터에서 실행 가능한 인사이트를 도출한다.

### 팀 구성

| 역할 | 에이전트 | 핵심 업무 | 작업 패턴 |
|------|---------|----------|----------|
| 데이터 모니터 | DATA_MONITOR | 데이터 수집, 대시보드, 이상 감지, 알림 | 상시 반복 (일 1-2회) |
| 인사이트 분석가 | INSIGHT_ANALYST | 심층 분석, 리포트, 전략 제안, A/B 분석 | 정기 + 비정기 |

### 역할 분담 원칙
```
DATA_MONITOR: "무엇이 일어나고 있는가" (What)
├── 데이터 수집/정리 → 팩트 제공
├── 이상 감지 → 빠른 알림
└── 대시보드 → 현황 시각화

INSIGHT_ANALYST: "왜 일어났고, 무엇을 해야 하는가" (Why + How)
├── 원인 분석 → 근본 원인 파악
├── 인사이트 도출 → 비즈니스 의미 해석
└── 전략 제안 → 실행 방안 제시
```

---

## 협업 모델: 계층적 분업

### 기본 원칙

```
1. 데이터 흐름 원칙
   - DATA_MONITOR가 정리한 데이터만 INSIGHT_ANALYST가 분석한다
   - INSIGHT_ANALYST는 원본 데이터에 직접 접근하지 않는다 (일관성 유지)
   - 단, 긴급 분석 시 직접 접근 허용 (사후 DATA_MONITOR에 공유)

2. 분석 요청 원칙
   - TEAM_LEAD 또는 CAMPAIGN_STRATEGIST의 분석 요청은
     DATA_MONITOR가 데이터를 준비하고, INSIGHT_ANALYST가 분석한다
   - 이상 감지 시 DATA_MONITOR가 감지하고, INSIGHT_ANALYST에게 원인 분석을 요청한다

3. 리포트 품질 원칙
   - DATA_MONITOR: 데이터 정확성 책임
   - INSIGHT_ANALYST: 인사이트 깊이/실행 가능성 책임
```

---

## 워크플로우 1: 상시 모니터링 루프 (DATA_MONITOR 주도)

```
[일일 루틴]

AM 09:00 - 데이터 수집
    DATA_MONITOR:
    ├── 4개 채널 API에서 전일 성과 데이터 수집
    ├── GA4 전환 데이터 수집
    ├── 자사 시스템 매출 데이터 매칭
    └── 데이터 정규화 + 정합성 1차 체크

AM 09:30 - 일일 스냅샷 생성 + 건강 상태 판정
    DATA_MONITOR:
    ├── 일일 성과 스냅샷 생성 (state/daily_snapshot)
    ├── KPI 건강 상태 판정 (정상/주의/위험)
    ├── 이상 감지 규칙 실행
    ├── [정상] → 대시보드 업데이트, 스냅샷 저장
    ├── [주의] → INSIGHT_ANALYST에게 원인 분석 요청
    └── [위험] → 즉시 TEAM_LEAD 알림 + INSIGHT_ANALYST 긴급 분석

PM 15:00 - 중간 체크
    DATA_MONITOR:
    ├── 당일 예산 소진 속도 확인
    ├── 이상 지표 2차 확인
    └── AM 이상 건 후속 확인

매주 월요일 AM - 주간 데이터 패키지 전달
    DATA_MONITOR → INSIGHT_ANALYST:
    ├── 지난 주 일별 스냅샷 7건
    ├── 주간 채널별 요약 데이터
    ├── 이상 감지 이력
    └── 특이사항 메모

매월 1일 AM - 월간 데이터 패키지 전달
    DATA_MONITOR → INSIGHT_ANALYST:
    ├── 지난 달 일별 스냅샷 전체
    ├── 월간 채널별 요약 데이터
    ├── 월간 이상 감지 이력
    ├── finance 전달 광고비 데이터
    └── 전월 대비 변화 데이터
```

---

## 워크플로우 2: 정기 분석 (INSIGHT_ANALYST 주도)

```
[주간 분석 사이클]

매주 월요일 AM - 주간 리포트 작성
    INSIGHT_ANALYST:
    ├── DATA_MONITOR의 주간 데이터 패키지 수령
    ├── 주간 성과 분석
    │   ├── 채널별 성과 비교 + 전주 대비 변화
    │   ├── Top/Bottom 캠페인/키워드/소재 분석
    │   ├── 인사이트 3~5개 도출 (관찰-원인-시사점-액션)
    │   └── 다음 주 권고 액션 도출
    ├── 주간 리포트 초안 작성
    └── TEAM_LEAD에게 제출

매월 첫째 주 - 월간 리포트 작성
    INSIGHT_ANALYST:
    ├── DATA_MONITOR의 월간 데이터 패키지 수령
    ├── 월간 심층 분석
    │   ├── 월간 트렌드 분석 (주별 추이)
    │   ├── 채널별 심층 분석
    │   ├── 크로스 채널 어트리뷰션 분석
    │   ├── 업종 벤치마크 대비 분석
    │   ├── 예산 집행 효율 분석
    │   ├── 인사이트 5~7개 도출
    │   └── 다음 달 전략 권고
    ├── 월간 리포트 작성
    └── TEAM_LEAD + CAMPAIGN_STRATEGIST에게 제출
```

---

## 워크플로우 3: 비정기 분석 (트리거 기반)

```
[트리거 1: 이상 감지 → 원인 분석]

DATA_MONITOR 이상 감지
    │
    ▼
INSIGHT_ANALYST 원인 분석 요청 수신
    │
    ▼
[분석 프로세스]
    ├── 현상 파악: 어떤 지표가, 얼마나, 언제 변했는가
    ├── 분해 분석: 채널/캠페인/키워드/소재/기기/시간대별 분해
    ├── 가설 수립: 가능한 원인 가설 3~5개
    ├── 가설 검증: 데이터로 각 가설 검증
    ├── 근본 원인 특정: 가장 유력한 원인
    └── 대응 방안 제시: 구체적 액션 + 담당 에이전트
    │
    ▼
원인 분석 보고서 → TEAM_LEAD + 관련 에이전트
    │
    ▼
대응 시한: 긴급(위험) 4시간 이내, 일반(주의) 24시간 이내


[트리거 2: A/B 테스트 완료 → 결과 분석]

A/B 테스트 데이터 축적 완료
    │
    ▼
INSIGHT_ANALYST 분석
    ├── 데이터 품질 확인 (샘플 사이즈, 외부 변수)
    ├── 통계적 유의성 검증 (p값, 신뢰구간)
    ├── 효과 크기 산출
    ├── 결론 도출 (채택/기각/추가 테스트)
    └── 다음 테스트 제안
    │
    ▼
A/B 테스트 보고서 → TEAM_LEAD + AD_CREATIVE + 관련 채널 전문가


[트리거 3: 전략 의사결정 지원 요청]

TEAM_LEAD/CAMPAIGN_STRATEGIST 분석 요청
    │
    ▼
INSIGHT_ANALYST:
    ├── 요청 이해 및 분석 범위 확인
    ├── DATA_MONITOR에 필요 데이터 요청
    ├── 분석 수행
    └── 데이터 기반 전략 제안서 작성
    │
    ▼
전략 제안서 → 요청자에게 제출
```

---

## 데이터 파이프라인 설계

```
[데이터 흐름도]

채널 API (4개)  ─┐
GA4             ─┤
자사 시스템      ─┘
                  │
                  ▼
        [DATA_MONITOR]
        ├── 수집/정규화
        ├── 정합성 체크
        ├── 대시보드 업데이트
        ├── 이상 감지
        └── 일일 스냅샷 생성
                  │
            ┌─────┼──────────────┐
            │     │              │
            ▼     ▼              ▼
        [알림]  [INSIGHT     [finance]
                ANALYST]
                ├── 원인 분석
                ├── 인사이트 도출
                ├── 리포트 작성
                └── 전략 제안
                      │
            ┌─────────┼──────────┐
            │         │          │
            ▼         ▼          ▼
        [TEAM    [CAMPAIGN   [BID
         LEAD]   STRATEGIST] OPTIMIZER]
```

### 데이터 저장 구조
```
state/
├── daily_snapshot_{YYYY-MM-DD}.json  ← DATA_MONITOR 생성
├── weekly_report_{YYYY-WNN}.md       ← INSIGHT_ANALYST 생성
├── monthly_report_{YYYY-MM}.md       ← INSIGHT_ANALYST 생성
└── project_manager.md                ← 진행 중 캠페인 상태

archive/
├── completed_campaigns.md            ← 완료된 캠페인 성과
└── ab_test_results/                  ← A/B 테스트 결과 아카이브
```

---

## 팀 내부 커뮤니케이션 프로토콜

### DATA_MONITOR → INSIGHT_ANALYST 요청
```json
{
  "request_type": "anomaly_analysis|regular_data|ad_hoc_data",
  "priority": "urgent|normal",
  "data_package": {
    "snapshots": "object[] (관련 스냅샷)",
    "anomaly_details": "object (이상 감지 상세, 해당 시)",
    "context": "string (배경 정보)"
  },
  "expected_output": "string (원인 분석|주간 리포트|특별 분석)",
  "deadline": "string (기한)"
}
```

### INSIGHT_ANALYST → DATA_MONITOR 데이터 추가 요청
```json
{
  "request_type": "additional_data",
  "data_needed": {
    "channel": "string",
    "metrics": "string[]",
    "dimensions": "string[] (키워드별, 소재별, 시간대별 등)",
    "period": "string",
    "granularity": "daily|hourly"
  },
  "reason": "string (왜 이 데이터가 필요한지)",
  "urgency": "urgent|normal"
}
```

---

## 팀 품질 기준

### 팀 차원 품질 지표

| 항목 | 기준 | 담당 |
|------|------|------|
| 데이터 수집 완전성 | 4개 채널 100% 수집 | DATA_MONITOR |
| 스냅샷 적시성 | AM 09:30까지 생성 | DATA_MONITOR |
| 이상 감지 속도 | 1시간 이내 감지 | DATA_MONITOR |
| 주간 리포트 적시성 | 매주 월요일 AM 제출 | INSIGHT_ANALYST |
| 월간 리포트 적시성 | 익월 3영업일 이내 | INSIGHT_ANALYST |
| 인사이트 실행 가능성 | 모든 인사이트에 구체적 액션 | INSIGHT_ANALYST |
| 원인 분석 속도 | 긴급 4시간, 일반 24시간 | INSIGHT_ANALYST |
| 데이터 정합성 | 채널 간 오차 20% 이내 | DATA_MONITOR |
| finance 리포트 기한 | 100% 기한 준수 | DATA_MONITOR |

### 지속적 개선
```
월간 회고:
├── 이번 달 분석 정확도 검토
│   └── 제안한 전략이 실제로 효과가 있었는가?
├── 이상 감지 정확도 검토
│   └── 오탐(false positive) 비율은 얼마인가?
├── 리포트 피드백 수집
│   └── TEAM_LEAD/CAMPAIGN_STRATEGIST로부터 리포트 개선 피드백
└── 분석 도구/방법론 업데이트
    └── 새로운 분석 기법, 벤치마크 데이터 업데이트
```

---

## 외부 팀 연동

| 대상 | 연동 내용 | 주기 | 담당 |
|------|----------|------|------|
| TEAM_LEAD | 일일 브리핑, 이상 알림, 주간/월간 리포트 | 일일+주간+월간 | 양쪽 |
| CAMPAIGN_STRATEGIST | 전략 제안, 성과 근거 데이터 | 주간+수시 | INSIGHT |
| BID_OPTIMIZER | 실시간 성과 데이터, 입찰 조정 트리거 | 일일 | MONITOR |
| Channel Team (4명) | 채널별 성과 데이터 교환, 이상 원인 협업 | 일일+수시 | 양쪽 |
| AD_CREATIVE | 소재별 성과, A/B 결과, 소재 피로도 | 주간+수시 | INSIGHT |
| KEYWORD_RESEARCHER | 키워드별 성과, 고/저성과 키워드 | 주간 | INSIGHT |
| finance | 광고비 리포트, 예산 집행 현황 | 일일+주간+월간 | MONITOR |

---

## 참고 파일

| 파일 | 용도 |
|------|------|
| `agents/analytics-team/DATA_MONITOR.md` | 데이터 모니터 정의서 |
| `agents/analytics-team/INSIGHT_ANALYST.md` | 인사이트 분석가 정의서 |
| `config/kpi_definitions.md` | KPI 정의 및 벤치마크 |
| `config/channels.md` | 채널별 데이터 소스 |
| `handoff/budget_to_finance.md` | finance 전달 양식 |
| `archive/completed_campaigns.md` | 과거 캠페인 아카이브 |
