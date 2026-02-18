# 플러그인 인터페이스 정의

## 개요
퍼포먼스 마케팅 팀은 **플러그인 아키텍처**로 설계되어 외부 시스템에서 API를 통해 접근할 수 있다.
이 문서는 외부 연동을 위한 입출력 스키마, API 엔드포인트, 인증, 에러 처리를 정의한다.

---

## 아키텍처 개요

```
[External Client]
      │
      ▼
[API Gateway] ← 인증/인가, Rate Limit
      │
      ▼
[Plugin Interface Layer] ← 요청 파싱, 유효성 검증
      │
      ▼
[TEAM_LEAD (Router)] ← 워크플로우 라우팅
      │
      ├── Campaign Service    ← CAMPAIGN_STRATEGIST
      ├── Research Service     ← KEYWORD_RESEARCHER
      ├── Creative Service     ← AD_CREATIVE
      ├── Bid Service          ← BID_OPTIMIZER
      ├── Analytics Service    ← ANALYTICS_AGENT
      └── Channel Service      ← CHANNEL_SPECIALIST
                │
          [Channel Adapters]
          ├── Naver Adapter
          ├── Kakao Adapter
          ├── Meta Adapter
          └── Google Adapter
```

---

## API 엔드포인트

### Base URL
```
https://api.perf-marketing.agentcompany.io/v1
```

### 인증
```
방식: Bearer Token (OAuth 2.0)
헤더: Authorization: Bearer {access_token}

토큰 발급:
POST /auth/token
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "grant_type": "client_credentials"
}

토큰 만료: 3600초 (1시간)
갱신: refresh_token으로 갱신 가능
```

### 엔드포인트 목록

#### 캠페인 관리
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/campaigns` | 새 캠페인 생성 요청 |
| GET | `/campaigns` | 캠페인 목록 조회 |
| GET | `/campaigns/{id}` | 캠페인 상세 조회 |
| PUT | `/campaigns/{id}` | 캠페인 수정 |
| DELETE | `/campaigns/{id}` | 캠페인 삭제 |
| POST | `/campaigns/{id}/launch` | 캠페인 론칭 |
| POST | `/campaigns/{id}/pause` | 캠페인 일시 중지 |
| POST | `/campaigns/{id}/resume` | 캠페인 재개 |

#### 전략
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/strategy/generate` | 캠페인 전략 생성 |
| POST | `/strategy/channel-mix` | 채널 믹스 추천 |
| POST | `/strategy/budget-allocation` | 예산 배분 추천 |

#### 리서치
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/research/keywords` | 키워드 리서치 요청 |
| POST | `/research/audiences` | 오디언스 리서치 요청 |
| POST | `/research/competitors` | 경쟁사 분석 요청 |

#### 크리에이티브
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/creative/generate` | 광고 카피 생성 |
| POST | `/creative/variations` | A/B 변형 생성 |
| POST | `/creative/guide` | 크리에이티브 가이드 생성 |

#### 분석 / 리포트
| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/analytics/dashboard` | 성과 대시보드 조회 |
| GET | `/analytics/reports/weekly` | 주간 리포트 조회 |
| GET | `/analytics/reports/monthly` | 월간 리포트 조회 |
| POST | `/analytics/reports/custom` | 커스텀 리포트 생성 |
| GET | `/analytics/campaigns/{id}/performance` | 캠페인별 성과 |

#### 최적화
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/optimization/analyze` | 최적화 분석 요청 |
| POST | `/optimization/recommend` | 최적화 제안 생성 |
| POST | `/optimization/apply` | 최적화 사항 적용 |

#### A/B 테스트
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/ab-test/create` | A/B 테스트 생성 |
| GET | `/ab-test/{id}/status` | 테스트 상태 조회 |
| GET | `/ab-test/{id}/results` | 테스트 결과 조회 |
| POST | `/ab-test/{id}/apply-winner` | 승자 적용 |

---

## Input Schema (요청 스키마)

### 캠페인 생성 요청

```json
{
  "$schema": "campaign_creation_request",
  "version": "1.0",
  "request": {
    "type": "campaign_creation",
    "priority": "normal | high | urgent",
    "callback_url": "https://your-webhook.com/callback"
  },
  "campaign_brief": {
    "business_name": {
      "type": "string",
      "required": true,
      "description": "사업체명"
    },
    "product_service": {
      "type": "string",
      "required": true,
      "description": "제품/서비스 설명 (상세할수록 좋은 결과)"
    },
    "industry": {
      "type": "string",
      "required": true,
      "enum": ["ecommerce", "ecommerce_fashion", "saas", "local_business", "app", "education", "finance", "healthcare", "travel", "game", "other"],
      "description": "업종"
    },
    "objective": {
      "type": "string",
      "required": true,
      "enum": ["awareness", "consideration", "conversion", "app_install", "lead_generation"],
      "description": "캠페인 목표"
    },
    "target_audience": {
      "type": "object",
      "required": true,
      "properties": {
        "age_range": {
          "type": "string",
          "description": "연령대 (예: 25-44)"
        },
        "gender": {
          "type": "string",
          "enum": ["all", "male", "female"]
        },
        "location": {
          "type": "string",
          "description": "지역 (예: 서울, 전국)"
        },
        "interests": {
          "type": "array",
          "items": "string",
          "description": "관심사 리스트"
        },
        "custom_description": {
          "type": "string",
          "description": "타겟 자유 설명"
        }
      }
    },
    "budget": {
      "type": "object",
      "required": true,
      "properties": {
        "total_amount": {
          "type": "integer",
          "description": "총 예산 (원)"
        },
        "period_days": {
          "type": "integer",
          "description": "캠페인 기간 (일)"
        },
        "daily_cap": {
          "type": "integer",
          "description": "일예산 상한 (원, 선택)"
        },
        "currency": {
          "type": "string",
          "default": "KRW"
        }
      }
    },
    "kpi": {
      "type": "object",
      "required": true,
      "properties": {
        "primary_kpi": {
          "type": "string",
          "description": "주요 KPI (예: CPA 15000)"
        },
        "primary_target": {
          "type": "number",
          "description": "주요 KPI 목표치"
        },
        "secondary_kpi": {
          "type": "string",
          "description": "보조 KPI (선택)"
        },
        "secondary_target": {
          "type": "number",
          "description": "보조 KPI 목표치 (선택)"
        }
      }
    },
    "channels": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["naver", "kakao", "meta", "google"]
      },
      "description": "사용 채널 (비워두면 자동 추천)"
    },
    "landing_page": {
      "type": "string",
      "format": "uri",
      "description": "랜딩 페이지 URL"
    },
    "competitors": {
      "type": "array",
      "items": "string",
      "description": "경쟁사 리스트 (선택)"
    },
    "existing_assets": {
      "type": "boolean",
      "description": "기존 소재 존재 여부"
    },
    "notes": {
      "type": "string",
      "description": "추가 요청사항 (자유)"
    }
  }
}
```

### 성과 분석 요청

```json
{
  "$schema": "analytics_request",
  "version": "1.0",
  "request": {
    "type": "performance_analysis",
    "campaign_id": "campaign_123",
    "period": {
      "start_date": "2026-02-01",
      "end_date": "2026-02-28"
    },
    "channels": ["naver", "meta"],
    "metrics": ["impressions", "clicks", "cost", "conversions", "revenue"],
    "compare_with": "previous_period | previous_year | target",
    "report_format": "summary | detailed | executive"
  }
}
```

### 최적화 요청

```json
{
  "$schema": "optimization_request",
  "version": "1.0",
  "request": {
    "type": "optimization",
    "campaign_id": "campaign_123",
    "issue": "CPA가 목표 대비 150% 초과",
    "scope": "all | keyword | creative | bid | targeting",
    "auto_apply": false,
    "budget_change_limit": 20
  }
}
```

---

## Output Schema (응답 스키마)

### 공통 응답 래퍼

```json
{
  "status": "success | processing | error",
  "request_id": "req_abc123",
  "timestamp": "2026-02-17T09:00:00+09:00",
  "data": { ... },
  "meta": {
    "processing_time_ms": 1500,
    "agent": "TEAM_LEAD",
    "version": "1.0"
  }
}
```

### 캠페인 플랜 응답

```json
{
  "status": "success",
  "data": {
    "campaign_plan": {
      "id": "plan_abc123",
      "campaign_name": "겨울 등산화 캠페인",
      "strategy_summary": "전략 요약 텍스트",
      "channel_mix": [
        {
          "channel": "naver",
          "channel_display_name": "네이버 검색광고",
          "budget_ratio": 40,
          "budget_amount": 4000000,
          "objective": "전환",
          "ad_types": ["파워링크", "쇼핑검색"],
          "targeting_summary": "타겟팅 요약",
          "keywords_count": 150,
          "creatives_count": 5,
          "bid_strategy": "수동 CPC → 전환 최적화",
          "expected_metrics": {
            "impressions": 500000,
            "clicks": 25000,
            "ctr": 5.0,
            "conversions": 500,
            "cpa": 8000,
            "roas": 450
          }
        }
      ],
      "total_budget": 10000000,
      "period": {
        "start_date": "2026-03-01",
        "end_date": "2026-03-31"
      },
      "kpi_targets": {
        "primary": { "kpi": "CPA", "target": 10000, "unit": "원" },
        "secondary": { "kpi": "ROAS", "target": 400, "unit": "%" }
      },
      "risk_assessment": [
        {
          "risk": "경쟁 CPC 상승",
          "probability": "medium",
          "impact": "high",
          "mitigation": "롱테일 키워드 확장, 입찰 전략 다변화"
        }
      ],
      "timeline": [
        { "phase": "세팅", "days": "D1-D3" },
        { "phase": "테스트", "days": "D4-D10" },
        { "phase": "최적화", "days": "D11-D25" },
        { "phase": "마무리", "days": "D26-D31" }
      ]
    }
  }
}
```

### 성과 리포트 응답

```json
{
  "status": "success",
  "data": {
    "performance_report": {
      "period": {
        "start_date": "2026-02-01",
        "end_date": "2026-02-28"
      },
      "executive_summary": "2월 캠페인은 목표 ROAS 400% 대비 450% 달성...",
      "total_metrics": {
        "impressions": 2000000,
        "clicks": 80000,
        "cost": 10000000,
        "conversions": 1200,
        "revenue": 45000000,
        "ctr": 4.0,
        "cpc": 125,
        "cpa": 8333,
        "roas": 450,
        "cvr": 1.5
      },
      "channel_performance": [
        {
          "channel": "naver",
          "metrics": { ... },
          "vs_target": { "cpa": 83, "roas": 112 },
          "top_keywords": [ ... ],
          "insights": "네이버 쇼핑검색에서 전환 집중..."
        }
      ],
      "comparison": {
        "vs_previous_period": {
          "cost": "+5%",
          "conversions": "+12%",
          "roas": "+7%"
        }
      },
      "recommendations": [
        {
          "priority": "high",
          "action": "메타 리타겟팅 예산 20% 증액",
          "expected_impact": "CPA 10% 감소",
          "rationale": "리타겟팅 CVR이 신규 대비 3배 높음"
        }
      ]
    }
  }
}
```

---

## Rate Limits

| 플랜 | 요청/분 | 요청/시간 | 요청/일 |
|------|---------|----------|---------|
| Free | 10 | 100 | 500 |
| Basic | 30 | 500 | 5,000 |
| Pro | 100 | 2,000 | 20,000 |
| Enterprise | 500 | 10,000 | 100,000 |

### Rate Limit 헤더
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1708142400
```

---

## Error Handling

### 에러 응답 형식
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_BUDGET",
    "message": "예산이 최소 기준(100,000원) 미만입니다.",
    "details": {
      "field": "campaign_brief.budget.total_amount",
      "provided": 50000,
      "minimum": 100000
    },
    "suggestion": "최소 100,000원 이상의 예산을 설정해주세요."
  },
  "request_id": "req_abc123",
  "timestamp": "2026-02-17T09:00:00+09:00"
}
```

### 에러 코드

| 코드 | HTTP | 설명 |
|------|------|------|
| AUTH_INVALID | 401 | 인증 실패 |
| AUTH_EXPIRED | 401 | 토큰 만료 |
| FORBIDDEN | 403 | 권한 없음 |
| NOT_FOUND | 404 | 리소스 없음 |
| INVALID_REQUEST | 400 | 요청 형식 오류 |
| INVALID_BUDGET | 400 | 예산 유효성 오류 |
| INVALID_CHANNEL | 400 | 지원하지 않는 채널 |
| INVALID_KPI | 400 | KPI 설정 오류 |
| RATE_LIMITED | 429 | 요청 제한 초과 |
| PROCESSING | 202 | 처리 중 (비동기) |
| CHANNEL_ERROR | 502 | 채널 API 오류 |
| INTERNAL_ERROR | 500 | 내부 서버 오류 |

---

## 웹훅 (Webhook)

### 비동기 작업 완료 알림

캠페인 생성, 리포트 생성 등 시간이 걸리는 작업은 웹훅으로 완료 알림을 보낸다.

```json
// 요청 시 callback_url 지정
POST /campaigns
{
  "request": {
    "callback_url": "https://your-app.com/webhook/perf-marketing"
  },
  ...
}

// 완료 시 웹훅 전송
POST https://your-app.com/webhook/perf-marketing
{
  "event": "campaign.plan.completed",
  "request_id": "req_abc123",
  "timestamp": "2026-02-17T09:30:00+09:00",
  "data": {
    "campaign_id": "campaign_123",
    "status": "completed",
    "result_url": "https://api.perf-marketing.agentcompany.io/v1/campaigns/campaign_123"
  }
}
```

### 웹훅 이벤트 유형

| 이벤트 | 설명 |
|--------|------|
| `campaign.plan.completed` | 캠페인 플랜 생성 완료 |
| `campaign.launched` | 캠페인 론칭 완료 |
| `campaign.paused` | 캠페인 일시 중지 |
| `report.generated` | 리포트 생성 완료 |
| `optimization.recommended` | 최적화 제안 생성 완료 |
| `optimization.applied` | 최적화 적용 완료 |
| `ab_test.completed` | A/B 테스트 완료 |
| `alert.performance` | 성과 이상 감지 알림 |
| `alert.budget` | 예산 이상 알림 |

### 웹훅 보안
```
서명 검증: X-Signature-256 헤더
서명 방식: HMAC-SHA256 (webhook_secret + payload)
재시도: 실패 시 최대 3회 (1분, 5분, 30분 간격)
타임아웃: 10초
```

---

## SDK / 클라이언트 라이브러리

### Python SDK (예정)
```python
from perf_marketing import Client

client = Client(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# 캠페인 생성
plan = client.campaigns.create(
    business_name="나이키 코리아",
    product_service="겨울 등산화",
    industry="ecommerce",
    objective="conversion",
    budget={"total_amount": 10000000, "period_days": 30},
    kpi={"primary_kpi": "ROAS", "primary_target": 400}
)

# 성과 조회
report = client.analytics.get_report(
    campaign_id="campaign_123",
    period={"start": "2026-02-01", "end": "2026-02-28"}
)
```

### REST API (cURL 예시)
```bash
# 캠페인 생성
curl -X POST https://api.perf-marketing.agentcompany.io/v1/campaigns \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "request": { "type": "campaign_creation" },
    "campaign_brief": {
      "business_name": "나이키 코리아",
      "product_service": "겨울 등산화",
      "industry": "ecommerce",
      "objective": "conversion",
      "budget": { "total_amount": 10000000, "period_days": 30 },
      "kpi": { "primary_kpi": "ROAS", "primary_target": 400 }
    }
  }'
```

---

## 버전 관리

| 버전 | 상태 | 날짜 |
|------|------|------|
| v1 | 현재 (Current) | 2026-02-17 |

### 하위 호환성 정책
- Major 버전 변경 시 6개월 이전 공지
- 기존 버전은 최소 12개월 유지
- 신규 필드 추가는 하위 호환 (기존 클라이언트 영향 없음)
- 필드 삭제/변경은 Major 버전 변경

---

## 참고 파일

| 파일 | 용도 |
|------|------|
| `plugin/adapters.md` | 채널 어댑터 패턴 |
| `plugin/integration_guide.md` | 연동 가이드 및 예제 |
| `TEAM.md` | 팀 정의서, 입출력 개요 |
