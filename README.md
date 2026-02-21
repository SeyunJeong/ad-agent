# AdAgent

한국 시장 퍼포먼스 마케팅을 자동화하는 AI 플랫폼.

네이버 검색광고, 카카오 모먼트, 메타, 구글 — 4개 채널의 캠페인 전략 수립부터 소재 제작, 집행, 최적화까지를 AI 에이전트가 처리한다.

## 왜 만들었나

한국 디지털 광고 시장은 연 10조 원 규모인데, 중소사업자 대부분이 광고 대행사에 15% 수수료를 내면서도 제대로 된 전략을 못 받고 있다. AdAgent는 대행사가 하는 일(리서치 → 전략 → 소재 → 집행 → 분석)을 AI 파이프라인으로 대체한다.

## 핵심 구조: 8단계 콘텐츠 파이프라인

캠페인 하나가 만들어지기까지 8단계를 거친다. 각 단계는 전담 AI 에이전트가 처리하고, 중간에 품질 게이트가 있어서 기준 미달이면 자동으로 되돌린다.

```
Phase 0  시장 조사        DEEP_RESEARCHER — 시장/경쟁사/타겟 분석
   ↓
Phase 1  전략 수립        CAMPAIGN_STRATEGIST — 셀프 디베이트 방식
   ↓                     (Blue Team 제안 → Red Team 비판 → 최종 정리)
Phase 2  컨셉 기획        CONCEPT_PLANNER — Safe / Bold / Wild Card 3안
   ↓
Phase 3  소재 제작        COPYWRITER + KEYWORD_TEAM + VISUAL_DIRECTOR
   ↓
Phase 4  팩트 체크  ████  AD_FACT_CHECKER — 통과 못하면 진행 불가
   ↓
Phase 5  QA 스코어  ████  QA_SCORER — 50점 만점, 35점 미만 자동 반려
   ↓
Phase 6  채널 셋업        CHANNEL_TEAM + BID_OPTIMIZER — 4채널 동시 세팅
   ↓
Phase 7  분석/피드백      ANALYTICS_TEAM — 성과 분석 후 Phase 0/2/3 재진입
```

**Phase 4, 5는 필수 게이트**로, TEAM_LEAD도 우회할 수 없다. 허위 광고나 품질 미달 소재가 집행되는 걸 구조적으로 막는다.

## 셀프 디베이트 전략 생성

전략을 한 번에 뽑지 않는다. 3단계 토론을 거친다:

1. **Blue Team** — 공격적인 초안 전략 제시
2. **Red Team** — 8가지 체크리스트로 약점 지적 (예산 효율성, 법적 리스크, 경쟁사 대비 등)
3. **Defense** — 유효한 비판은 수용, 과잉 비판은 반박 → 최종 전략 확정

단발성 LLM 호출보다 훨씬 균형 잡힌 전략이 나온다.

## 멀티채널 어댑터 아키텍처

4개 광고 채널을 하나의 인터페이스로 추상화했다.

```python
class ChannelAdapter(ABC):
    async def create_campaign(config) -> dict
    async def pause_campaign(campaign_id) -> None
    async def add_keywords(ad_group_id, keywords) -> list
    async def set_bid_strategy(campaign_id, strategy) -> None
    async def get_performance(campaign_id, start, end) -> MetricSet
    # ... 총 32개 메서드
```

구현체:

| 채널 | 어댑터 | API |
|------|--------|-----|
| 네이버 | `NaverSearchAdsAdapter` | Naver Search Ads API |
| 카카오 | `KakaoMomentAdapter` | Kakao Moment API |
| 메타 | `MetaAdsAdapter` | Meta Marketing API |
| 구글 | `GoogleAdsAdapter` | Google Ads API |

새 채널을 추가하려면 `ChannelAdapter`를 구현하고 레지스트리에 등록하면 된다. 기존 코드를 건드릴 필요 없음.

## 비주얼 생성 파이프라인

광고 이미지도 AI가 만든다:

1. **Claude** — 영문 프롬프트 생성 (이미지 설명)
2. **Flux 2.0** (FAL.ai) — 이미지 생성
3. **Creatomate** — 한글 텍스트 오버레이 합성

이미지 생성 모델이 한글을 잘 못 그리기 때문에, 이미지는 영문으로 생성하고 텍스트는 별도 레이어로 합성하는 방식을 택했다. 덕분에 카피만 바꿔서 A/B 테스트하기도 쉽다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| AI | Anthropic Claude API (전략/카피/QA) |
| 비주얼 | FAL.ai (Flux 2.0), Creatomate |
| 채널 API | Naver Search Ads, Google Ads, Meta Marketing, Kakao Moment |
| DB | SQLite (aiosqlite, async) |
| 스케줄링 | APScheduler (입찰 최적화, 데이터 수집) |
| 로깅 | structlog |

## 프로젝트 구조

```
ad-agent/
├── src/
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── agents/
│   │   └── orchestrator.py     # 8단계 파이프라인 오케스트레이터
│   ├── api/                    # REST API 엔드포인트
│   │   ├── campaigns.py        # 캠페인 CRUD + 실행/일시정지
│   │   ├── strategy.py         # 전략 생성
│   │   ├── creative.py         # 소재 생성
│   │   ├── analytics.py        # 성과 분석
│   │   └── visuals.py          # 비주얼 생성
│   ├── channels/               # 채널 어댑터 (Adapter Pattern)
│   │   ├── base.py             # ChannelAdapter ABC
│   │   ├── naver.py
│   │   ├── google.py
│   │   ├── meta.py
│   │   ├── kakao.py
│   │   └── registry.py         # 채널 팩토리
│   ├── models/                 # Pydantic 도메인 모델
│   ├── services/               # 비주얼 생성, 에셋 저장
│   └── storage/                # SQLite 비동기 저장소
├── agents/                     # 에이전트 정의 문서 (20명)
├── config/                     # KPI 정의, 품질 스코어링 기준
├── workflows/                  # 워크플로우 정의
└── pyproject.toml
```

## 에이전트 팀 (20명)

```
TEAM_LEAD
├── CAMPAIGN_STRATEGIST          전략 + 셀프 디베이트
├── KEYWORD_AUDIENCE_TEAM (3)    키워드/오디언스 리서치
├── CREATIVE_TEAM (3)            카피 + 비주얼 + 심사
├── BID_OPTIMIZER                입찰 최적화
├── ANALYTICS_TEAM (2)           데이터 모니터링 + 인사이트
├── CHANNEL_TEAM (4)             채널별 전문가
└── CONTENT_PIPELINE_TEAM (4)    리서치 + 컨셉 + 팩트체크 + QA
```

## 실행

```bash
# 의존성 설치
poetry install

# 환경 변수 설정
cp .env.example .env
# ANTHROPIC_API_KEY, 각 채널 API 키 설정

# 서버 실행
poetry run ad-agent
# http://localhost:8000/docs 에서 API 문서 확인
```

## API 예시

```bash
# 캠페인 전략 생성
POST /api/v1/strategy/generate
{
  "business_name": "우리카페",
  "industry": "F&B",
  "monthly_budget": 3000000,
  "channels": ["naver", "meta"],
  "goal": "신규 고객 유입"
}

# 캠페인 실행
POST /api/v1/campaigns/{id}/launch

# 성과 조회
GET /api/v1/analytics/{campaign_id}/performance?period=7d
```
