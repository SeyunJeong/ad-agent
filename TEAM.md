# 퍼포먼스 마케팅 팀 정의서

## 팀 미션

**한국 시장 퍼포먼스 마케팅 자동화**

네이버 검색광고, 카카오 모먼트, 메타(인스타그램/페이스북), 구글 광고를 통합 관리하여
데이터 기반의 캠페인 전략 수립, 실행, 최적화, 분석을 자동화한다.

### 핵심 가치

1. **데이터 드리븐**: 모든 의사결정은 데이터와 근거에 기반한다
2. **한국 시장 전문성**: 글로벌 방법론을 한국 시장에 맞게 현지화한다
3. **멀티 채널 통합**: 개별 채널이 아닌 전체 미디어 믹스를 최적화한다
4. **지속적 최적화**: 세팅 후 방치가 아닌, 실시간 모니터링과 개선을 수행한다
5. **플러그인 확장성**: 새로운 채널과 기능을 쉽게 추가할 수 있는 구조를 유지한다

---

## 팀 구성 (16명)

### 조직도

```
TEAM_LEAD (1)
    +-- CAMPAIGN_STRATEGIST (1) — 유지 + 셀프 디베이트 모드
    +-- KEYWORD_AUDIENCE_TEAM (3)
    |   +-- SEARCH_RESEARCHER (검색 리서처, 팀 리드 겸임)
    |   +-- AUDIENCE_RESEARCHER (소셜/오디언스 리서처)
    |   +-- TREND_ANALYST (트렌드/경쟁 분석가)
    +-- CREATIVE_TEAM (3)
    |   +-- COPYWRITER (카피라이터)
    |   +-- VISUAL_DIRECTOR (비주얼 디렉터)
    |   +-- CREATIVE_REVIEWER (크리에이티브 심사관)
    +-- BID_OPTIMIZER (1) — 유지
    +-- ANALYTICS_TEAM (2)
    |   +-- DATA_MONITOR (데이터 모니터)
    |   +-- INSIGHT_ANALYST (인사이트 분석가)
    +-- CHANNEL_TEAM (4)
        +-- NAVER_SPECIALIST (네이버 전문가)
        +-- KAKAO_SPECIALIST (카카오 전문가)
        +-- META_SPECIALIST (메타 전문가)
        +-- GOOGLE_SPECIALIST (구글 전문가)
```

### 에이전트/서브팀 목록

| # | 역할 | 유형 | 파일 | 핵심 역량 |
|---|------|------|------|----------|
| 1 | **TEAM_LEAD** | 개인 | `agents/TEAM_LEAD.md` | 서브팀 오케스트레이션, 워크플로우 관리, 품질 관리 |
| 2 | **CAMPAIGN_STRATEGIST** | 개인 | `agents/CAMPAIGN_STRATEGIST.md` | 캠페인 전략 수립, 셀프 디베이트, 채널 믹스, 예산 배분 |
| 3 | **KEYWORD_AUDIENCE_TEAM** | 서브팀 (3명) | `agents/keyword-team/` | 키워드/오디언스 리서치, 트렌드/경쟁 분석 |
| 3-1 | SEARCH_RESEARCHER | 서브팀원 | `agents/keyword-team/SEARCH_RESEARCHER.md` | 네이버/구글 키워드, 검색 의도 분류, 팀 리드 |
| 3-2 | AUDIENCE_RESEARCHER | 서브팀원 | `agents/keyword-team/AUDIENCE_RESEARCHER.md` | 카카오/메타 오디언스 세그먼트, 리타겟팅 |
| 3-3 | TREND_ANALYST | 서브팀원 | `agents/keyword-team/TREND_ANALYST.md` | 시즌 트렌드, 경쟁사 분석, 블루오션 발굴 |
| 4 | **CREATIVE_TEAM** | 서브팀 (3명) | `agents/creative-team/` | 카피/비주얼 제작, 법적 검수, A/B 변형 |
| 4-1 | COPYWRITER | 서브팀원 | `agents/creative-team/COPYWRITER.md` | 채널별 광고 카피, 한국어 네이티브 카피라이팅 |
| 4-2 | VISUAL_DIRECTOR | 서브팀원 | `agents/creative-team/VISUAL_DIRECTOR.md` | 크리에이티브 가이드, 소재 규격, thread-team 연동 |
| 4-3 | CREATIVE_REVIEWER | 서브팀원 | `agents/creative-team/CREATIVE_REVIEWER.md` | 법적/규제/정책 검수, 품질 심사 |
| 5 | **BID_OPTIMIZER** | 개인 | `agents/BID_OPTIMIZER.md` | 입찰 전략, 예산 페이싱, ROAS/CPA 최적화 |
| 6 | **ANALYTICS_TEAM** | 서브팀 (2명) | `agents/analytics-team/` | 성과 모니터링, 인사이트 분석, 리포팅 |
| 6-1 | DATA_MONITOR | 서브팀원 | `agents/analytics-team/DATA_MONITOR.md` | 실시간 모니터링, 이상 감지, 대시보드 |
| 6-2 | INSIGHT_ANALYST | 서브팀원 | `agents/analytics-team/INSIGHT_ANALYST.md` | 심층 분석, 주간/월간 리포트, A/B 통계 분석 |
| 7 | **CHANNEL_TEAM** | 서브팀 (4명) | `agents/channel-team/` | 채널별 세팅/실행/최적화/API 연동 |
| 7-1 | NAVER_SPECIALIST | 서브팀원 | `agents/channel-team/NAVER_SPECIALIST.md` | 파워링크, 쇼핑검색, 브랜드검색, 네이버 API |
| 7-2 | KAKAO_SPECIALIST | 서브팀원 | `agents/channel-team/KAKAO_SPECIALIST.md` | 디스플레이, 비즈보드, 친구톡/알림톡, 카카오 API |
| 7-3 | META_SPECIALIST | 서브팀원 | `agents/channel-team/META_SPECIALIST.md` | 피드, 리일스, DPA, 픽셀+CAPI, Meta API |
| 7-4 | GOOGLE_SPECIALIST | 서브팀원 | `agents/channel-team/GOOGLE_SPECIALIST.md` | 검색, 디스플레이, YouTube, P-Max, Google API |

---

## 서브팀 협업 모델

### KEYWORD_AUDIENCE_TEAM: 병렬 리서치 → 크로스 리뷰 → 통합
```
Phase 1: 병렬 리서치 (동시 실행)
    SEARCH_RESEARCHER → 네이버/구글 키워드 리스트 초안
    AUDIENCE_RESEARCHER → 카카오/메타 오디언스 세그먼트 초안
    TREND_ANALYST → 시즌 트렌드 + 경쟁사 인텔리전스

Phase 2: 크로스 리뷰 (순차 실행)
    각 리서처가 다른 리서처의 결과물을 검토하고 피드백

Phase 3: 통합 보고서 (SEARCH_RESEARCHER 리드)
    세 리서처의 결과를 통합하여 최종 리서치 보고서 작성
```

### CREATIVE_TEAM: 순차 파이프라인 + 피드백 루프
```
Phase 1: 브리프 수령
    CAMPAIGN_STRATEGIST → 핵심 메시지/USP
    KEYWORD_AUDIENCE_TEAM → 주요 키워드 및 검색 의도

Phase 2: 병렬 제작
    COPYWRITER → 채널별 카피 세트 초안
    VISUAL_DIRECTOR → 크리에이티브 가이드 초안

Phase 3: 크로스 리뷰
    COPYWRITER <-> VISUAL_DIRECTOR: 메시지 정합성 확인
    CREATIVE_REVIEWER → 법적/정책 검수 (최대 2회 피드백)

Phase 4: 최종 패키징 → CHANNEL_TEAM 전달
```

### ANALYTICS_TEAM: 계층적 분업
```
상시 루프 (DATA_MONITOR):
    데이터 수집 → 대시보드 업데이트 → 이상 감지 → 알림

정기 분석 (INSIGHT_ANALYST):
    DATA_MONITOR 데이터 기반 → 심층 분석 → 리포트 작성

비정기 분석 (INSIGHT_ANALYST):
    이상 감지 시 → 원인 분석 / A/B 테스트 완료 시 → 통계 분석
```

### CHANNEL_TEAM: 독립 실행 + 크로스 채널 동기화
```
일상 운영 (독립적):
    각 채널 전문가가 자기 채널의 캠페인 세팅/실행/최적화를 독립 수행

크로스 채널 동기화 (정기적):
    채널 간 성과 비교 → 메시지 일관성 확인 → 예산 재배분 검토
    → BID_OPTIMIZER 및 ANALYTICS_TEAM과 연동

트러블슈팅 (비정기):
    특정 채널 이슈 발생 시 해당 전문가가 즉시 대응
```

---

## 워크플로우 유형

| 유형 | 파일 | 트리거 | 설명 |
|------|------|--------|------|
| **캠페인 생성** | `workflows/campaign_creation.md` | "캠페인 만들어줘", "광고 시작하고 싶어" | 신규 캠페인 전략 수립 → 실행 플랜 |
| **최적화** | `workflows/optimization.md` | "성과 안 나와", "ROAS 올려줘" | 기존 캠페인 분석 → 개선안 도출 |
| **리포팅** | `workflows/reporting.md` | "리포트 줘", "이번 주 성과" | 데이터 수집 → 분석 → 리포트 생성 |
| **A/B 테스트** | `workflows/ab_testing.md` | "테스트 해보자", "어떤 카피가 나을까" | 가설 → 변형 → 실행 → 분석 |

---

## 입출력 정의

### 입력 (Input)

#### 캠페인 브리프 (필수)
```json
{
  "campaign_brief": {
    "business_name": "사업체명",
    "product_service": "제품/서비스 설명",
    "objective": "awareness | consideration | conversion",
    "target_audience": {
      "demographics": "연령, 성별, 지역",
      "interests": "관심사",
      "behavior": "행동 특성"
    },
    "budget": {
      "total": "총 예산 (원)",
      "period": "기간",
      "daily_cap": "일예산 상한 (원, 선택)"
    },
    "kpi": {
      "primary": "주요 KPI (예: CPA 15,000원 이하)",
      "secondary": "보조 KPI (예: CTR 2% 이상)"
    },
    "channels": ["naver", "kakao", "meta", "google"],
    "creative_assets": "기존 소재 여부",
    "landing_page": "랜딩 페이지 URL",
    "competitors": ["경쟁사 리스트"],
    "notes": "추가 요청사항"
  }
}
```

#### 성과 데이터 (최적화/리포팅 시)
```json
{
  "performance_data": {
    "period": "분석 기간",
    "channels": [
      {
        "channel": "채널명",
        "metrics": {
          "impressions": "노출수",
          "clicks": "클릭수",
          "cost": "비용 (원)",
          "conversions": "전환수",
          "revenue": "매출 (원)"
        }
      }
    ]
  }
}
```

### 출력 (Output)

#### 캠페인 플랜
```json
{
  "campaign_plan": {
    "strategy_summary": "전략 요약 (셀프 디베이트 결과 포함)",
    "channel_mix": {
      "channels": [
        {
          "channel": "채널명",
          "specialist": "담당 채널 전문가",
          "budget_ratio": "예산 비율 (%)",
          "budget_amount": "예산 금액 (원)",
          "objective": "채널별 목표",
          "ad_types": ["광고 유형"],
          "targeting": "타겟팅 설정",
          "keywords_or_audiences": "키워드/오디언스 (서브팀 제공)",
          "creatives": "크리에이티브 (서브팀 제공, 검수 완료)",
          "bid_strategy": "입찰 전략"
        }
      ]
    },
    "timeline": "실행 타임라인",
    "kpi_targets": "KPI 목표치",
    "ab_test_plan": "A/B 테스트 계획",
    "risk_assessment": "리스크 평가",
    "optimization_schedule": "최적화 일정"
  }
}
```

#### 성과 리포트
```json
{
  "performance_report": {
    "period": "분석 기간",
    "executive_summary": "경영진 요약 (INSIGHT_ANALYST 작성)",
    "channel_performance": [
      {
        "channel": "채널명",
        "specialist": "담당 채널 전문가",
        "metrics": "핵심 지표",
        "vs_target": "목표 대비 달성률",
        "insights": "인사이트"
      }
    ],
    "cross_channel_attribution": "크로스 채널 어트리뷰션 분석",
    "recommendations": "개선 권고사항",
    "next_actions": "다음 액션 아이템"
  }
}
```

---

## 플러그인 인터페이스 명세

### API 개요

퍼포먼스 마케팅 팀은 **플러그인 아키텍처**로 설계되어 외부 시스템과 연동 가능하다.

| 구성 요소 | 파일 | 설명 |
|----------|------|------|
| 인터페이스 정의 | `plugin/interface.md` | Input/Output 스키마, API 엔드포인트, 인증 |
| 채널 어댑터 | `plugin/adapters.md` | 채널별 어댑터 패턴, 확장 방법 |
| 연동 가이드 | `plugin/integration_guide.md` | 기존 시스템 연동, 사용 예제, 웹훅 |

### 아키텍처

```
[External Client / CEO Office]
         |
         v
    [Plugin Interface]
         |
         v
    [TEAM_LEAD] <-- 오케스트레이션/라우팅
         |
    +----+--------+----------+--------+---------+
    v    v        v          v        v         v
 [전략] [키워드팀] [크리에이티브팀] [입찰] [분석팀] [채널팀]
         |             |                  |         |
    +---------+   +---------+      +--------+  +--------+--------+--------+
    v    v    v   v    v    v      v        v  v        v        v        v
 [검색] [오디] [트렌드] [카피] [비주얼] [심사] [모니터] [인사이트] [네이버] [카카오] [메타] [구글]
```

### 확장 포인트

1. **새 채널 추가**: `plugin/adapters.md`의 어댑터 인터페이스를 구현하면 새 채널 추가 가능 (CHANNEL_TEAM에 전문가 추가)
2. **커스텀 KPI**: `config/kpi_definitions.md`에 새 KPI 추가 가능
3. **캠페인 템플릿**: `config/templates.md`에 업종별 템플릿 추가 가능
4. **외부 연동**: `plugin/integration_guide.md`의 웹훅/API로 외부 시스템과 연동 가능
5. **서브팀 확장**: 기존 서브팀에 전문가를 추가하거나 새 서브팀을 구성 가능

---

## 연동 팀

### thread-team (마케팅부)
- **연동 포인트**: 광고 크리에이티브 소재 제작 요청
- **흐름**: VISUAL_DIRECTOR가 크리에이티브 브리프 작성 → thread-team이 소재 제작 → VISUAL_DIRECTOR 1차 검수 → CREATIVE_REVIEWER 2차 검수
- **핸드오프**: `handoff/creative_to_thread.md`

### finance (총무부)
- **연동 포인트**: 광고비 추적, 예산 승인, 비용 리포트
- **흐름**: BID_OPTIMIZER가 예산 계획 → finance에 승인 요청 → DATA_MONITOR가 실사용 비용 리포트
- **핸드오프**: `handoff/budget_to_finance.md`

### biz-planner (기획부)
- **연동 포인트**: 사업 목표 기반 KPI 설정, 마케팅 전략 정렬
- **흐름**: biz-planner에서 사업 전략 → CAMPAIGN_STRATEGIST가 마케팅 전략으로 변환

---

## 디렉토리 구조

```
ad-agent/
├── CLAUDE.md                      ← 팀 운영 규칙
├── TEAM.md                        ← 팀 정의서 (이 파일)
├── agents/                        ← 에이전트 정의서
│   ├── TEAM_LEAD.md
│   ├── CAMPAIGN_STRATEGIST.md
│   ├── BID_OPTIMIZER.md
│   ├── keyword-team/              ← 키워드/오디언스 서브팀
│   │   ├── SEARCH_RESEARCHER.md
│   │   ├── AUDIENCE_RESEARCHER.md
│   │   └── TREND_ANALYST.md
│   ├── creative-team/             ← 크리에이티브 서브팀
│   │   ├── COPYWRITER.md
│   │   ├── VISUAL_DIRECTOR.md
│   │   └── CREATIVE_REVIEWER.md
│   ├── analytics-team/            ← 애널리틱스 서브팀
│   │   ├── DATA_MONITOR.md
│   │   └── INSIGHT_ANALYST.md
│   └── channel-team/              ← 채널 서브팀
│       ├── NAVER_SPECIALIST.md
│       ├── KAKAO_SPECIALIST.md
│       ├── META_SPECIALIST.md
│       └── GOOGLE_SPECIALIST.md
├── workflows/                     ← 워크플로우 정의
│   ├── campaign_creation.md
│   ├── optimization.md
│   ├── reporting.md
│   └── ab_testing.md
├── config/                        ← 설정
│   ├── channels.md
│   ├── kpi_definitions.md
│   └── templates.md
├── plugin/                        ← 플러그인 인터페이스
│   ├── interface.md
│   ├── adapters.md
│   └── integration_guide.md
├── handoff/                       ← 인수인계 문서
│   ├── strategy_to_keyword_team.md
│   ├── keyword_team_to_creative_team.md
│   ├── creative_team_to_channel_team.md
│   ├── creative_to_thread.md
│   └── budget_to_finance.md
├── analysis/                      ← 분석 문서
│   └── team_structure_analysis.md
├── state/                         ← 상태 관리
│   └── project_manager.md
├── templates/                     ← 템플릿
├── archive/                       ← 아카이브
│   ├── completed_campaigns.md
│   └── ab_test_history.md
└── logs/                          ← 로그
    └── retrospective.md
```
