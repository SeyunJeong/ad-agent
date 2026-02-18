# 채널 설정 및 API 연동 스펙

## 개요
퍼포먼스 마케팅 팀이 운영하는 4개 광고 채널(네이버, 카카오, 메타, 구글)의 설정 정보 및 API 연동 사양을 정의한다.

---

## 1. 네이버 검색광고 (Naver Search Ads)

### 채널 개요
| 항목 | 내용 |
|------|------|
| 플랫폼 | 네이버 검색광고 (searchad.naver.com) |
| 한국 시장 점유율 | 검색 광고 시장 약 60~70% |
| 주요 광고 유형 | 파워링크, 쇼핑검색, 브랜드검색, 파워콘텐츠 |
| 과금 방식 | CPC (파워링크, 쇼핑), CPT (브랜드검색) |
| 최소 입찰가 | CPC 70원 (2024년 기준) |
| 최소 일예산 | 없음 (단, 실효성 있는 최소 권장: 1만원/일) |

### 광고 유형 상세

#### 파워링크 (검색 광고)
```
위치: 네이버 검색 결과 상단/하단
포맷: 제목(15자) + 설명(45자) + URL
확장 소재: 전화번호, 위치, 가격표, 부가 설명
입찰: CPC (키워드별 개별 입찰)
노출 순위: 입찰가 x 품질지수
```

#### 쇼핑검색광고
```
위치: 네이버 쇼핑 검색 결과
포맷: 상품 이미지 + 상품명(50자) + 가격 + 리뷰수
입찰: CPC (상품/카테고리별)
연동: 스마트스토어 또는 EP(상품정보파일)
```

#### 브랜드검색
```
위치: 네이버 검색 결과 최상단 (프리미엄)
포맷: 타이틀(18자) + 서브타이틀(25자) + 설명(45자x2) + 이미지/영상
입찰: CPT (기간당 과금, 월 단위)
자격: 상표권 보유 브랜드
심사: 3~5영업일
```

#### 파워콘텐츠
```
위치: 네이버 검색 결과 내 콘텐츠 영역
포맷: 블로그/포스트 형식의 콘텐츠형 광고
입찰: CPC
적합: 정보 탐색형 키워드, 교육 콘텐츠
```

### API 연동 스펙

#### 네이버 검색광고 API
```
Base URL: https://api.searchad.naver.com
인증: API Key + Secret Key (Customer ID 기반)
인증 방식: HMAC-SHA256 서명

주요 엔드포인트:
├── GET /ncc/campaigns          - 캠페인 목록 조회
├── POST /ncc/campaigns         - 캠페인 생성
├── PUT /ncc/campaigns/{id}     - 캠페인 수정
├── GET /ncc/adgroups           - 광고 그룹 조회
├── POST /ncc/adgroups          - 광고 그룹 생성
├── GET /ncc/keywords           - 키워드 조회
├── POST /ncc/keywords          - 키워드 추가
├── GET /ncc/ads                - 광고 소재 조회
├── POST /ncc/ads               - 광고 소재 생성
├── GET /stat-reports           - 성과 리포트 조회
└── POST /keywordstool          - 키워드 도구 (검색량 등)

Rate Limit: 1,000 requests / 10초
데이터 지연: 실시간 ~ 최대 3시간

응답 형식: JSON
페이지네이션: offset + limit
```

#### 키워드 도구 API
```
POST /keywordstool
Request:
{
  "hintKeywords": ["키워드1", "키워드2"],
  "showDetail": 1
}

Response:
{
  "keywordList": [
    {
      "relKeyword": "키워드",
      "monthlyPcQcCnt": 1000,      // PC 월간 검색량
      "monthlyMobileQcCnt": 5000,  // 모바일 월간 검색량
      "monthlyAvePcClkCnt": 100,   // PC 월간 평균 클릭수
      "monthlyAveMobileClkCnt": 400, // 모바일 월간 평균 클릭수
      "monthlyAvePcCtr": 10.0,     // PC 월간 평균 CTR
      "monthlyAveMobileCtr": 8.0,  // 모바일 월간 평균 CTR
      "plAvgDepth": 15,            // 월평균 노출광고수
      "compIdx": "높음"             // 경쟁 정도
    }
  ]
}
```

---

## 2. 카카오 모먼트 (Kakao Moment)

### 채널 개요
| 항목 | 내용 |
|------|------|
| 플랫폼 | 카카오 모먼트 (moment.kakao.com) |
| 도달 규모 | 카카오톡 MAU 약 4,700만명 (한국 인구의 90%+) |
| 주요 광고 유형 | 디스플레이, 비즈보드, 메시지(친구톡/알림톡), 동영상 |
| 과금 방식 | CPM, CPC, CPA, oCPM |
| 최소 입찰가 | CPM 1,000원~, CPC 50원~ (유형별 상이) |
| 최소 일예산 | 10,000원 |

### 광고 유형 상세

#### 디스플레이 광고
```
게재지면: 카카오톡, 다음, 카카오스토리, 카카오 네트워크
포맷:
├── 네이티브 배너: 500x500px
├── 배너: 1200x628px
├── 와이드 배너: 1200x480px
└── 카드형: 500x500px
과금: CPM, CPC
타겟팅: 데모그래픽, 관심사, 행동, 커스텀, 룩어라이크
```

#### 비즈보드
```
게재지면: 카카오톡 채팅 탭 상단 (프리미엄)
포맷: 1029x258px (이미지) + 제목(18자) + 설명(27자)
과금: CPM (프리미엄 단가)
특징: 높은 도달률, 높은 CPM, 브랜드 인지도에 적합
```

#### 메시지 광고
```
친구톡:
├── 대상: 카카오톡 채널 친구
├── 유형: 텍스트/이미지/와이드/캐러셀
├── 비용: 15~30원/건
└── 제약: 수신 동의 필수, 차단율 관리

알림톡:
├── 대상: 전화번호 기반 (비친구 가능)
├── 유형: 텍스트 + 버튼
├── 비용: 7~15원/건
├── 제약: 사전 심사 필수 (템플릿 승인)
└── 용도: 정보성 메시지만 (광고 메시지 제한)
```

### API 연동 스펙

#### 카카오 모먼트 API
```
Base URL: https://apis.moment.kakao.com
인증: OAuth 2.0 (카카오 비즈니스 계정)

주요 엔드포인트:
├── GET /openapi/v4/campaigns         - 캠페인 조회
├── POST /openapi/v4/campaigns        - 캠페인 생성
├── GET /openapi/v4/adGroups          - 광고 그룹 조회
├── POST /openapi/v4/adGroups         - 광고 그룹 생성
├── GET /openapi/v4/creatives         - 소재 조회
├── POST /openapi/v4/creatives        - 소재 생성
├── GET /openapi/v4/reports/campaigns - 캠페인 리포트
├── GET /openapi/v4/reports/adGroups  - 광고 그룹 리포트
└── GET /openapi/v4/demographics      - 오디언스 데이터

Rate Limit: 100 requests / 분
데이터 지연: 최대 6시간

응답 형식: JSON
```

#### 카카오 픽셀
```
설치 방법:
├── JavaScript SDK: 웹사이트 <head> 태그에 삽입
├── 서버 API: 서버사이드 이벤트 전송
└── GTM: Google Tag Manager 템플릿

표준 이벤트:
├── pageView: 페이지 조회
├── viewContent: 콘텐츠 조회
├── addToCart: 장바구니 추가
├── purchase: 구매 완료
├── signUp: 회원가입
└── completeRegistration: 등록 완료
```

---

## 3. 메타 (Meta - Instagram / Facebook)

### 채널 개요
| 항목 | 내용 |
|------|------|
| 플랫폼 | Meta Ads Manager (business.facebook.com) |
| 한국 도달 규모 | 인스타그램 ~1,800만, 페이스북 ~1,500만 |
| 주요 광고 유형 | 피드, 스토리, 리일스, 메신저, DPA, 컬렉션 |
| 과금 방식 | CPM, CPC, CPA, oCPM, ROAS 기반 |
| 최소 일예산 | 약 $1/일 (캠페인 목표에 따라 다름) |
| 통화 | USD 또는 KRW (계정 설정) |

### 광고 유형 상세

#### 피드 광고 (인스타그램/페이스북)
```
포맷:
├── 단일 이미지: 1080x1080 (정사각), 1080x1350 (세로)
├── 캐러셀: 최대 10장 이미지/영상
├── 영상: 1080x1080 또는 1080x1920, 최대 240분
└── 컬렉션: 커버 이미지/영상 + 상품 카탈로그
텍스트: 주요텍스트(125자 권장) + 제목(27자) + 설명(27자)
CTA: 미리 정의된 버튼 옵션
```

#### 스토리/리일스
```
포맷: 1080x1920 (9:16, 풀스크린)
스토리: 최대 15초 (자동 분할)
리일스: 15~90초
특징: 사운드 온 환경, 몰입형
```

#### 다이나믹 광고 (DPA)
```
요구사항:
├── 상품 카탈로그 (CSV/XML/API)
├── Meta 픽셀 (웹) 또는 SDK (앱)
├── 이벤트: ViewContent, AddToCart, Purchase
└── 리타겟팅 오디언스 자동 생성
```

### API 연동 스펙

#### Meta Marketing API
```
Base URL: https://graph.facebook.com/v18.0
인증: OAuth 2.0 (System User Token 또는 User Token)

주요 엔드포인트:
├── GET /{ad_account_id}/campaigns         - 캠페인 조회
├── POST /{ad_account_id}/campaigns        - 캠페인 생성
├── GET /{ad_account_id}/adsets            - 광고 세트 조회
├── POST /{ad_account_id}/adsets           - 광고 세트 생성
├── GET /{ad_account_id}/ads               - 광고 조회
├── POST /{ad_account_id}/ads              - 광고 생성
├── GET /{ad_account_id}/insights          - 인사이트 (성과 데이터)
├── GET /{ad_account_id}/customaudiences   - 커스텀 오디언스
├── POST /{ad_account_id}/customaudiences  - 커스텀 오디언스 생성
└── GET /act_{id}/delivery_estimate        - 예상 도달 규모

Rate Limit:
├── Marketing API: 앱별 시간당 제한 (Business Use Case Rate)
├── 일반: 200 calls / 시간 / 광고 계정
└── 인사이트: 별도 rate limit

데이터 지연: 최대 48시간 (attribution window에 따라)
응답 형식: JSON
```

#### Meta 픽셀 + Conversions API (CAPI)
```
픽셀 (클라이언트 사이드):
├── JavaScript 코드 <head> 삽입
├── 표준 이벤트: PageView, ViewContent, AddToCart, Purchase 등
└── 커스텀 이벤트: 자유 정의

CAPI (서버 사이드):
├── POST /{pixel_id}/events
├── iOS14+ ATT 대응 필수
├── 중복 제거: event_id로 픽셀과 CAPI 이벤트 매칭
└── 데이터 파라미터: user_data (hashed), custom_data

Aggregated Event Measurement (AEM):
├── iOS14+ 환경 대응
├── 도메인당 최대 8개 전환 이벤트 설정
└── 이벤트 우선순위 설정 필요
```

---

## 4. 구글 광고 (Google Ads)

### 채널 개요
| 항목 | 내용 |
|------|------|
| 플랫폼 | Google Ads (ads.google.com) |
| 한국 시장 점유율 | 검색 약 30~35%, 디스플레이/유튜브 높은 점유 |
| 주요 광고 유형 | 검색, 디스플레이, YouTube, 쇼핑, P-Max |
| 과금 방식 | CPC, CPM, CPV, CPA, ROAS 기반 |
| 최소 일예산 | 제한 없음 (실효성 최소 권장: 1만원/일) |
| 통화 | KRW |

### 광고 유형 상세

#### 검색 광고 (RSA)
```
포맷: 반응형 검색 광고 (RSA)
├── 제목: 최대 15개 (각 30자, 최소 3개)
├── 설명: 최대 4개 (각 90자, 최소 2개)
├── 표시 경로: /15자/15자
└── 구글이 자동으로 최적 조합 선택
입찰: CPC, 타겟 CPA, 타겟 ROAS, 전환수 극대화
```

#### 디스플레이 광고
```
포맷: 반응형 디스플레이 광고
├── 이미지: 최대 15개 (1200x628, 1200x1200 등)
├── 로고: 최대 5개 (1200x1200, 1200x300)
├── 제목: 최대 5개 (각 30자)
├── 긴 제목: 최대 5개 (각 90자)
└── 설명: 최대 5개 (각 90자)
게재 네트워크: 300만+ 웹사이트/앱
```

#### YouTube 광고
```
유형:
├── 인스트림 (스킵 가능): 5초 후 스킵 가능, CPV
├── 인스트림 (스킵 불가): 15~20초, CPM
├── 범퍼: 6초, CPM
├── 인피드: YouTube 검색/추천 내, CPC
└── 쇼츠: YouTube Shorts 내, CPV/CPM
```

#### 쇼핑 광고 / P-Max
```
쇼핑:
├── 연동: Google Merchant Center
├── 상품 피드: 한국어 상품 정보 필수
├── 포맷: 상품 이미지 + 이름 + 가격 + 스토어명
└── 입찰: 타겟 ROAS 권장

P-Max:
├── 모든 구글 인벤토리 자동 게재
├── 에셋: 텍스트 + 이미지 + 영상 + 오디언스 시그널
├── AI 기반 최적화 (블랙박스)
└── 입찰: 전환수 극대화 / 타겟 CPA / 타겟 ROAS
```

### API 연동 스펙

#### Google Ads API
```
Base URL: https://googleads.googleapis.com/v15
인증: OAuth 2.0 (Developer Token + OAuth Client)

주요 리소스:
├── customers/{id}/campaigns         - 캠페인
├── customers/{id}/adGroups          - 광고 그룹
├── customers/{id}/ads               - 광고
├── customers/{id}/keywords          - 키워드
├── customers/{id}/biddingStrategies - 입찰 전략
├── customers/{id}/conversionActions - 전환 액션
└── customers/{id}/reports           - 리포트 (GAQL)

리포트 쿼리 (GAQL):
SELECT campaign.name, metrics.clicks, metrics.cost_micros
FROM campaign
WHERE segments.date DURING LAST_7_DAYS

Rate Limit:
├── 기본: 10,000 operations / 일
├── 리포트: 별도 quota
└── mutate: 5,000 operations / request

데이터 지연: 실시간 ~ 최대 3시간
응답 형식: JSON (Protocol Buffers 기반)
```

#### Google Ads 전환 추적
```
방법 1: Google Ads 전환 태그
├── Global site tag (gtag.js)
├── 이벤트 스니펫 (전환 페이지)
└── 향상된 전환 (Enhanced Conversions)

방법 2: GA4 연동
├── GA4 전환 이벤트 → Google Ads 가져오기
├── 자동 태깅 (gclid)
└── 오프라인 전환 가져오기

방법 3: Google Tag Manager
├── Google Ads 전환 추적 태그
├── 트리거 설정
└── 데이터 레이어 변수 매핑
```

---

## 채널 간 통합 관리

### UTM 파라미터 규칙

```
utm_source: {채널} (naver, kakao, meta, google)
utm_medium: {광고유형} (cpc, display, social, video)
utm_campaign: {캠페인명} (영문_소문자_하이픈)
utm_content: {소재ID} (ad_variant_001)
utm_term: {키워드} (검색광고 시)

예시:
?utm_source=naver&utm_medium=cpc&utm_campaign=winter-shoes-2026&utm_content=ad_a_benefit&utm_term=겨울등산화
```

### 채널 간 어트리뷰션 설정

| 채널 | 어트리뷰션 윈도우 | 전환 카운트 |
|------|-----------------|-----------|
| 네이버 | 클릭 후 30일 | 마지막 클릭 |
| 카카오 | 클릭 후 7일 / 노출 후 1일 | 마지막 터치 |
| 메타 | 클릭 후 7일 / 노출 후 1일 (기본) | 1일 노출 + 7일 클릭 |
| 구글 | 클릭 후 30일 (기본, 조정 가능) | 마지막 클릭 (검색) / 데이터 기반 |

> **주의**: 채널별 어트리뷰션 윈도우가 다르므로, 단순 합산 시 전환 중복 발생.
> GA4 등 통합 분석 도구로 중복 제거 후 비교해야 정확.

---

## 참고 자료

| 자료 | URL |
|------|-----|
| 네이버 광고 API 문서 | https://naver.github.io/searchad-apidoc/ |
| 카카오 모먼트 API 문서 | https://developers.kakao.com/docs/latest/ko/moment |
| Meta Marketing API 문서 | https://developers.facebook.com/docs/marketing-apis |
| Google Ads API 문서 | https://developers.google.com/google-ads/api/docs |
