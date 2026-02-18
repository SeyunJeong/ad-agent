# 연동 가이드

## 개요
이 문서는 퍼포먼스 마케팅 팀의 플러그인 인터페이스를 외부 시스템과 연동하는 방법을 설명한다.
기존 에이전트 회사 내부 팀, 외부 SaaS 클라이언트, 자사 시스템 모두에 적용 가능하다.

---

## 1. 내부 팀 연동

### CEO Office 연동

CEO Office(CHIEF_OF_STAFF)가 퍼포먼스 마케팅 팀에 태스크를 전달하는 흐름.

```
[오너 메시지]
      ↓
[CHIEF_OF_STAFF] 의도 파악 + 트리아지
      ↓
[태스크 생성]
  → tasks/perf-marketing/TASK-{날짜}-{순번}.json
  → 캠페인 브리프 포함
      ↓
[TEAM_LEAD] 태스크 접수
      ↓
[워크플로우 실행]
      ↓
[결과] tasks/completed/ 이동
      ↓
[CHIEF_OF_STAFF] 결과 수집 → 오너 보고
```

### 태스크 JSON 형식
```json
{
  "task_id": "TASK-20260217-001",
  "from": "ceo-office",
  "to": "perf-marketing",
  "type": "campaign_creation",
  "priority": "normal",
  "created_at": "2026-02-17T09:00:00+09:00",
  "original_message": "네이버 검색광고로 우리 신제품 캠페인 만들어줘. 월 500만원 예산.",
  "structured_brief": {
    "product_service": "AI 생산성 도구",
    "objective": "conversion",
    "budget": {
      "total_amount": 5000000,
      "period_days": 30
    },
    "channels": ["naver"],
    "kpi": {
      "primary_kpi": "CPA",
      "primary_target": 20000
    }
  },
  "status": "pending",
  "assignee": "TEAM_LEAD",
  "deadline": "2026-02-19T18:00:00+09:00"
}
```

### thread-team 연동

AD_CREATIVE가 크리에이티브 소재를 thread-team에 요청하는 흐름.

```
[AD_CREATIVE] 크리에이티브 브리프 작성
      ↓
[handoff/creative_to_thread.md] 양식으로 전달
      ↓
[thread-team TEAM_LEAD] 접수
      ↓
[thread-team Writer/Editor] 소재 제작
      ↓
[결과물] AD_CREATIVE에게 전달
      ↓
[AD_CREATIVE] 검수 (채널 규격, 브랜드 가이드라인)
      ↓
[승인] → CHANNEL_SPECIALIST에게 전달
[반려] → thread-team에 수정 요청
```

#### 크리에이티브 요청 양식
```json
{
  "request_id": "CR-20260217-001",
  "from": "perf-marketing/AD_CREATIVE",
  "to": "thread-team",
  "type": "creative_production",
  "campaign": "겨울 등산화 캠페인",
  "deliverables": [
    {
      "type": "image",
      "channel": "meta",
      "spec": "1080x1080px",
      "quantity": 3,
      "message": "겨울 등산에 최적화된 방수 등산화",
      "tone": "활동적, 아웃도어, 자연"
    },
    {
      "type": "image",
      "channel": "kakao",
      "spec": "1200x628px",
      "quantity": 2,
      "message": "오늘만 50% 할인",
      "tone": "긴급함, 혜택 강조"
    }
  ],
  "brand_guideline": "브랜드 컬러: 네이비, 폰트: 맑은고딕",
  "references": ["참고 이미지 URL"],
  "deadline": "2026-02-19T12:00:00+09:00"
}
```

### finance 팀 연동

BID_OPTIMIZER/ANALYTICS_AGENT가 예산 관련 정보를 finance 팀과 주고받는 흐름.

```
[예산 승인 요청 흐름]
BID_OPTIMIZER → handoff/budget_to_finance.md → finance
  포함: 월 예산 계획, 채널별 배분, 예산 근거

[비용 리포트 전달 흐름]
ANALYTICS_AGENT → handoff/budget_to_finance.md → finance
  포함: 실제 집행 금액, 채널별 내역, 잔액, 다음 달 예산 요청
```

#### 예산 요청 양식
```json
{
  "request_id": "BUD-20260217-001",
  "from": "perf-marketing",
  "to": "finance",
  "type": "budget_request",
  "period": "2026-03",
  "budget_plan": {
    "total": 10000000,
    "breakdown": {
      "naver": 4000000,
      "meta": 3000000,
      "google": 2000000,
      "kakao": 1000000
    }
  },
  "justification": "2월 ROAS 450% 달성, 3월 스케일업 근거",
  "vs_previous": "+20%",
  "expected_return": {
    "roas": 400,
    "revenue": 40000000
  }
}
```

---

## 2. 외부 시스템 연동 (SaaS)

### Quick Start

#### Step 1: API 키 발급
```
1. https://console.perf-marketing.agentcompany.io 접속
2. 프로젝트 생성
3. API Credentials 발급 (client_id, client_secret)
4. 웹훅 URL 등록 (선택)
```

#### Step 2: 인증 토큰 발급
```bash
curl -X POST https://api.perf-marketing.agentcompany.io/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "grant_type": "client_credentials"
  }'

# 응답
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "ref_..."
}
```

#### Step 3: 첫 번째 API 호출
```bash
# 캠페인 전략 생성
curl -X POST https://api.perf-marketing.agentcompany.io/v1/strategy/generate \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "request": {
      "type": "campaign_creation",
      "callback_url": "https://your-app.com/webhook"
    },
    "campaign_brief": {
      "business_name": "테스트 쇼핑몰",
      "product_service": "여성 의류 온라인 쇼핑몰",
      "industry": "ecommerce_fashion",
      "objective": "conversion",
      "target_audience": {
        "age_range": "25-44",
        "gender": "female",
        "location": "서울, 수도권",
        "interests": ["패션", "쇼핑", "뷰티"]
      },
      "budget": {
        "total_amount": 5000000,
        "period_days": 30,
        "currency": "KRW"
      },
      "kpi": {
        "primary_kpi": "ROAS",
        "primary_target": 300
      },
      "channels": ["meta", "naver"],
      "landing_page": "https://example-shop.com"
    }
  }'
```

### API 사용 예제

#### 예제 1: 캠페인 전체 생성 (End-to-End)
```
1. POST /campaigns
   → 캠페인 브리프 제출
   → 응답: { "status": "processing", "request_id": "req_001" }

2. (웹훅 수신 대기)
   → "campaign.plan.completed" 이벤트

3. GET /campaigns/{campaign_id}
   → 완성된 캠페인 플랜 확인

4. POST /campaigns/{campaign_id}/launch
   → 캠페인 론칭 (오너 승인 후)

5. GET /analytics/campaigns/{campaign_id}/performance
   → 성과 확인
```

#### 예제 2: 키워드 리서치만 요청
```bash
curl -X POST https://api.perf-marketing.agentcompany.io/v1/research/keywords \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "seed_keywords": ["등산화", "트레킹화", "등산 장비"],
    "channels": ["naver", "google"],
    "industry": "ecommerce",
    "include_competitors": true,
    "competitors": ["K2", "노스페이스", "블랙야크"]
  }'

# 응답 (비동기, 웹훅으로 완료 알림)
{
  "status": "processing",
  "request_id": "req_kw_001",
  "estimated_time_seconds": 120
}
```

#### 예제 3: 성과 리포트 조회
```bash
curl -X GET "https://api.perf-marketing.agentcompany.io/v1/analytics/reports/weekly?campaign_id=camp_001&week=2026-W07" \
  -H "Authorization: Bearer {token}"

# 응답 (동기)
{
  "status": "success",
  "data": {
    "performance_report": {
      "period": { "start": "2026-02-10", "end": "2026-02-16" },
      "executive_summary": "이번 주 ROAS 420%로 목표 초과 달성...",
      "total_metrics": {
        "impressions": 500000,
        "clicks": 20000,
        "cost": 2500000,
        "conversions": 300,
        "revenue": 10500000,
        "roas": 420
      },
      ...
    }
  }
}
```

#### 예제 4: 실시간 최적화 제안 받기
```bash
curl -X POST https://api.perf-marketing.agentcompany.io/v1/optimization/recommend \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "camp_001",
    "issue": "CPA가 전주 대비 40% 상승",
    "scope": "all",
    "auto_apply": false
  }'
```

---

## 3. 웹훅 설정

### 웹훅 등록
```bash
curl -X POST https://api.perf-marketing.agentcompany.io/v1/webhooks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhook/perf-marketing",
    "events": [
      "campaign.plan.completed",
      "report.generated",
      "alert.performance",
      "alert.budget"
    ],
    "secret": "your_webhook_secret"
  }'
```

### 웹훅 수신 처리 (Python 예시)
```python
import hmac
import hashlib
import json
from flask import Flask, request

app = Flask(__name__)
WEBHOOK_SECRET = "your_webhook_secret"

@app.route('/webhook/perf-marketing', methods=['POST'])
def handle_webhook():
    # 서명 검증
    signature = request.headers.get('X-Signature-256')
    payload = request.get_data()
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, f"sha256={expected}"):
        return "Invalid signature", 403

    # 이벤트 처리
    event = json.loads(payload)
    event_type = event['event']

    if event_type == 'campaign.plan.completed':
        handle_campaign_completed(event['data'])
    elif event_type == 'alert.performance':
        handle_performance_alert(event['data'])
    elif event_type == 'report.generated':
        handle_report_ready(event['data'])

    return "OK", 200

def handle_campaign_completed(data):
    campaign_id = data['campaign_id']
    # 캠페인 플랜 확인 후 론칭 여부 결정
    print(f"캠페인 {campaign_id} 플랜 완성됨")

def handle_performance_alert(data):
    # 성과 이상 알림 처리
    print(f"성과 이상: {data['alert_type']} - {data['message']}")

def handle_report_ready(data):
    # 리포트 다운로드
    print(f"리포트 준비됨: {data['report_url']}")
```

---

## 4. 텔레그램 봇 연동

에이전트 회사의 텔레그램 인프라(`infra/telegram`)와 연동하여 오너에게 알림을 보낸다.

### 알림 유형

| 알림 | 트리거 | 메시지 예시 |
|------|--------|-----------|
| 캠페인 플랜 완성 | 캠페인 생성 워크플로우 완료 | "[퍼포먼스 마케팅] 겨울 등산화 캠페인 플랜이 완성되었습니다. 확인해주세요." |
| 주간 리포트 | 매주 월요일 | "[주간 리포트] ROAS 420%, CPA 8,500원. 목표 대비 105% 달성." |
| 성과 이상 | CPA 급등/CTR 급락 | "[긴급] 네이버 캠페인 CPA가 50% 급등했습니다. 원인: 경쟁 입찰 심화." |
| 예산 알림 | 일예산 150% 초과 | "[예산 주의] 메타 캠페인 일예산 150% 소진. 상한 적용 중." |

### 연동 방법
```
infra/telegram 봇이 perf-marketing 팀의 state/project_manager.md를 읽어서
스케줄에 따라 알림을 전송한다.

또는 웹훅으로 텔레그램 봇에 직접 알림:
POST {telegram_bot_webhook_url}
{
  "team": "perf-marketing",
  "type": "alert",
  "message": "알림 메시지",
  "priority": "high"
}
```

---

## 5. 보안 가이드라인

### API 키 관리
```
- API 키를 코드에 하드코딩하지 않는다
- 환경 변수 또는 시크릿 매니저 사용
- 키 로테이션: 90일 주기 권장
- 불필요한 키는 즉시 비활성화
```

### 데이터 보안
```
- 전송: TLS 1.2+ 필수 (HTTPS only)
- 저장: 민감 데이터(고객 리스트 등) 암호화 저장
- 접근: 최소 권한 원칙 (필요한 엔드포인트만 허용)
- 로깅: 접근 로그 90일 보관
```

### 개인정보 처리
```
- 한국 개인정보보호법 준수 필수
- 고객 데이터(전화번호, 이메일 등) 전송 시 해싱 권장
- 오디언스 데이터 보관 기간 정책 준수
- 수집/이용 동의 근거 확보
```

---

## 6. 트러블슈팅

### 자주 발생하는 이슈

| 이슈 | 원인 | 해결 |
|------|------|------|
| 401 Unauthorized | 토큰 만료 | refresh_token으로 갱신 |
| 429 Rate Limited | 요청 제한 초과 | 요청 간격 늘리기, 플랜 업그레이드 |
| 502 Channel Error | 채널 API 일시 오류 | 자동 재시도 (최대 3회) |
| 데이터 불일치 | 채널 간 어트리뷰션 차이 | 통합 분석 도구(GA4) 기준 사용 |
| 웹훅 미수신 | URL 접근 불가 또는 타임아웃 | 웹훅 URL 확인, 10초 내 응답 |

### 지원 채널
```
- 기술 문의: tech@agentcompany.io
- API 이슈: api-support@agentcompany.io
- 긴급 이슈: 텔레그램 봇으로 TEAM_LEAD에게 직접 에스컬레이션
```

---

## 참고 파일

| 파일 | 용도 |
|------|------|
| `plugin/interface.md` | API 스키마 상세 |
| `plugin/adapters.md` | 채널 어댑터 패턴 |
| `TEAM.md` | 팀 정의서 |
| `config/channels.md` | 채널 API 스펙 |
