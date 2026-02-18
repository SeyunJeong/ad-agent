# 채널 어댑터 정의

## 개요
퍼포먼스 마케팅 팀은 **어댑터 패턴(Adapter Pattern)**을 사용하여 각 광고 채널과 통신한다.
채널 어댑터는 통일된 인터페이스를 제공하여, 내부 에이전트들이 채널 차이를 의식하지 않고 작업할 수 있게 한다.
새 채널을 추가할 때는 어댑터만 구현하면 기존 로직 변경 없이 확장 가능하다.

---

## 어댑터 아키텍처

```
[에이전트 Layer]
├── CAMPAIGN_STRATEGIST
├── KEYWORD_RESEARCHER
├── AD_CREATIVE
├── BID_OPTIMIZER
├── ANALYTICS_AGENT
└── CHANNEL_SPECIALIST
        │
        ▼
[Adapter Interface] ← 통일된 인터페이스
        │
   ┌────┼────┬────────┬──────────┐
   ▼    ▼    ▼        ▼          ▼
[Naver] [Kakao] [Meta] [Google]  [New Channel]
Adapter Adapter Adapter Adapter   Adapter
   │      │      │       │         │
   ▼      ▼      ▼       ▼         ▼
[네이버  [카카오  [Meta   [Google   [New
 API]    API]    API]    API]      API]
```

---

## 어댑터 인터페이스 (공통)

### IChannelAdapter

모든 채널 어댑터가 구현해야 하는 공통 인터페이스.

```
interface IChannelAdapter {

  // === 기본 정보 ===
  getChannelInfo(): ChannelInfo
  getCapabilities(): Capabilities
  getSupportedAdTypes(): AdType[]
  getConstraints(): Constraints

  // === 캠페인 관리 ===
  createCampaign(config: CampaignConfig): Campaign
  updateCampaign(id: string, updates: Partial<CampaignConfig>): Campaign
  pauseCampaign(id: string): void
  resumeCampaign(id: string): void
  deleteCampaign(id: string): void
  getCampaign(id: string): Campaign
  listCampaigns(filters?: CampaignFilters): Campaign[]

  // === 광고 그룹 관리 ===
  createAdGroup(campaignId: string, config: AdGroupConfig): AdGroup
  updateAdGroup(id: string, updates: Partial<AdGroupConfig>): AdGroup
  listAdGroups(campaignId: string): AdGroup[]

  // === 광고/소재 관리 ===
  createAd(adGroupId: string, creative: CreativeConfig): Ad
  updateAd(id: string, updates: Partial<CreativeConfig>): Ad
  listAds(adGroupId: string): Ad[]

  // === 키워드/타겟팅 ===
  addKeywords(adGroupId: string, keywords: Keyword[]): void
  removeKeywords(adGroupId: string, keywordIds: string[]): void
  setTargeting(adGroupId: string, targeting: TargetingConfig): void

  // === 입찰/예산 ===
  setBidStrategy(campaignId: string, strategy: BidStrategy): void
  setBudget(campaignId: string, budget: BudgetConfig): void
  adjustBid(entityId: string, bidAmount: number): void

  // === 성과 데이터 ===
  getPerformance(params: PerformanceQuery): PerformanceData
  getDailyStats(campaignId: string, dateRange: DateRange): DailyStats[]

  // === 유틸리티 ===
  validateCreative(creative: CreativeConfig): ValidationResult
  estimateReach(targeting: TargetingConfig): ReachEstimate
  checkApprovalStatus(adId: string): ApprovalStatus
}
```

### 공통 데이터 타입

```
// 채널 정보
ChannelInfo {
  id: string              // "naver" | "kakao" | "meta" | "google"
  name: string            // "네이버 검색광고"
  currency: string        // "KRW"
  timezone: string        // "Asia/Seoul"
  api_version: string     // 현재 API 버전
  status: string          // "active" | "maintenance"
}

// 채널 능력
Capabilities {
  search_ads: boolean
  display_ads: boolean
  video_ads: boolean
  shopping_ads: boolean
  message_ads: boolean
  app_install: boolean
  retargeting: boolean
  lookalike_audience: boolean
  automated_bidding: boolean
  conversion_tracking: boolean
}

// 제약 조건
Constraints {
  title_max_length: number
  description_max_length: number
  image_specs: ImageSpec[]
  video_specs: VideoSpec[]
  min_bid: number
  min_daily_budget: number
  max_keywords_per_group: number
  approval_time_hours: number
}

// 성과 데이터
PerformanceData {
  period: DateRange
  metrics: {
    impressions: number
    clicks: number
    cost: number
    conversions: number
    revenue: number
    ctr: number
    cpc: number
    cpa: number
    roas: number
    cvr: number
  }
  breakdown: {       // 선택적 세분화
    by_campaign?: MetricsByEntity[]
    by_adgroup?: MetricsByEntity[]
    by_keyword?: MetricsByEntity[]
    by_creative?: MetricsByEntity[]
    by_device?: MetricsByEntity[]
    by_hour?: MetricsByEntity[]
  }
}
```

---

## 채널별 어댑터 스펙

### 1. NaverAdapter

```
class NaverAdapter implements IChannelAdapter {

  // 인증
  auth: {
    type: "hmac_sha256"
    credentials: {
      customer_id: string
      api_key: string
      secret_key: string
    }
  }

  // 채널 특수 기능
  naverSpecific: {
    // 네이버 전용 광고 유형
    createPowerLink(config): PowerLinkAd
    createShoppingAd(config): ShoppingAd
    createBrandSearch(config): BrandSearchAd
    createPowerContent(config): PowerContentAd

    // 키워드 도구
    getKeywordStats(keywords: string[]): KeywordStats[]
    getRelatedKeywords(keyword: string): RelatedKeyword[]
    getSeasonalTrend(keyword: string): SeasonalData

    // 네이버 전용 리포트
    getQualityIndex(keywordId: string): QualityIndex
    getSearchVolume(keywords: string[]): SearchVolume[]
  }

  // 제약 조건
  constraints: {
    title_max_length: 15       // 파워링크 제목
    description_max_length: 45 // 파워링크 설명
    min_bid: 70                // 최소 CPC (원)
    shopping_title_max: 50     // 쇼핑 상품명
    max_keywords_per_group: 1000
    approval_time_hours: 24~72
  }

  // 매핑
  objectiveMapping: {
    "conversion" → "WEBSITE_CONVERSION"
    "traffic" → "WEBSITE_TRAFFIC"
    "awareness" → "BRAND_AWARENESS"
  }
}
```

### 2. KakaoAdapter

```
class KakaoAdapter implements IChannelAdapter {

  // 인증
  auth: {
    type: "oauth2"
    credentials: {
      client_id: string
      client_secret: string
      refresh_token: string
    }
  }

  // 채널 특수 기능
  kakaoSpecific: {
    // 카카오 전용 광고 유형
    createBizBoard(config): BizBoardAd
    createFriendTalk(config): FriendTalkMessage
    createAlimTalk(template): AlimTalkTemplate

    // 카카오 오디언스
    createCustomAudience(data): CustomAudience
    createLookalikeAudience(source, percent): LookalikeAudience
    getAudienceEstimate(targeting): AudienceSize

    // 카카오톡 채널
    getChannelFriends(): FriendStats
    getBlockRate(): number

    // 카카오 픽셀
    getPixelEvents(): PixelEvent[]
  }

  // 제약 조건
  constraints: {
    display_title_max: 25
    display_description_max: 34
    bizboard_title_max: 18
    bizboard_description_max: 27
    bizboard_image: "1029x258px"
    min_daily_budget: 10000       // 최소 일예산 (원)
    min_cpm: 1000                 // 최소 CPM (원)
    friend_talk_cost: "15~30원/건"
    approval_time_hours: 24~48
  }

  // 매핑
  objectiveMapping: {
    "conversion" → "CONVERSION"
    "traffic" → "VISITING"
    "awareness" → "REACH"
    "app_install" → "APP_INSTALL"
  }
}
```

### 3. MetaAdapter

```
class MetaAdapter implements IChannelAdapter {

  // 인증
  auth: {
    type: "oauth2"
    credentials: {
      app_id: string
      app_secret: string
      access_token: string
      ad_account_id: string
    }
  }

  // 채널 특수 기능
  metaSpecific: {
    // 메타 전용 기능
    createDPA(catalog, targeting): DynamicProductAd
    createLeadAd(form): LeadGenerationAd
    createCollectionAd(config): CollectionAd
    createReelsAd(video): ReelsAd

    // 오디언스
    createCustomAudience(source): CustomAudience
    createLookalikeAudience(source, country, percent): LookalikeAudience
    getAudienceOverlap(audiences): OverlapData

    // 카탈로그
    uploadCatalog(feed): Catalog
    syncCatalog(catalogId): SyncStatus

    // 픽셀 + CAPI
    getPixelEvents(): PixelEvent[]
    sendServerEvent(event): void
    checkAEMConfig(): AEMConfig

    // 크리에이티브 인사이트
    getCreativeInsights(adId): CreativeMetrics
    getAdLibrary(query): CompetitorAds[]
  }

  // 제약 조건
  constraints: {
    primary_text_recommended: 125    // 주요 텍스트 (권장)
    headline_recommended: 27         // 제목 (권장)
    description_recommended: 27      // 설명 (권장)
    image_feed: "1080x1080 or 1080x1350"
    image_story: "1080x1920"
    video_feed: "1080x1080, max 240min"
    video_reels: "1080x1920, 15~90sec"
    min_daily_budget: 1000           // ~$1
    learning_phase_conversions: 50   // 광고세트당 주 50전환
    approval_time_hours: 24
  }

  // 매핑
  objectiveMapping: {
    "awareness" → "OUTCOME_AWARENESS"
    "traffic" → "OUTCOME_TRAFFIC"
    "conversion" → "OUTCOME_SALES"
    "lead_generation" → "OUTCOME_LEADS"
    "app_install" → "OUTCOME_APP_PROMOTION"
  }
}
```

### 4. GoogleAdapter

```
class GoogleAdapter implements IChannelAdapter {

  // 인증
  auth: {
    type: "oauth2"
    credentials: {
      developer_token: string
      client_id: string
      client_secret: string
      refresh_token: string
      customer_id: string
    }
  }

  // 채널 특수 기능
  googleSpecific: {
    // 구글 전용 캠페인 유형
    createSearchCampaign(config): SearchCampaign
    createDisplayCampaign(config): DisplayCampaign
    createYouTubeCampaign(config): YouTubeCampaign
    createShoppingCampaign(config): ShoppingCampaign
    createPMaxCampaign(config): PMaxCampaign

    // 키워드 플래너
    getKeywordIdeas(seeds): KeywordIdea[]
    getKeywordForecast(keywords): Forecast

    // Merchant Center
    syncMerchantCenter(): SyncStatus
    getProductStatus(): ProductStatus[]

    // 전환 추적
    getConversionActions(): ConversionAction[]
    createEnhancedConversion(config): void

    // 리포트 (GAQL)
    executeQuery(gaql: string): QueryResult

    // 추천
    getRecommendations(campaignId): Recommendation[]
    applyRecommendation(recommendationId): void
  }

  // 제약 조건
  constraints: {
    rsa_headline_max: 30             // RSA 제목 (30자 x 15개)
    rsa_description_max: 90          // RSA 설명 (90자 x 4개)
    rsa_min_headlines: 3
    rsa_min_descriptions: 2
    display_headline_max: 30
    display_long_headline_max: 90
    display_description_max: 90
    video_bumper_max: 6              // 범퍼 광고 최대 6초
    min_daily_budget: 0              // 제한 없음
    pmax_min_daily: "목표 CPA의 3~5배"
    target_cpa_min_conversions: 30   // 월 30전환 이상
    approval_time_hours: 24
  }

  // 매핑
  objectiveMapping: {
    "awareness" → "BRAND_AWARENESS_AND_REACH"
    "consideration" → "PRODUCT_AND_BRAND_CONSIDERATION"
    "traffic" → "WEBSITE_TRAFFIC"
    "conversion" → "SALES"
    "lead_generation" → "LEADS"
    "app_install" → "APP_PROMOTION"
  }
}
```

---

## 새 채널 추가 방법

### Step 1: 어댑터 정의서 작성
```
파일: plugin/adapters/{channel_name}_adapter.md

필수 포함 항목:
1. 채널 개요 (ChannelInfo)
2. 인증 방식 (auth)
3. IChannelAdapter 인터페이스 구현 매핑
4. 채널 특수 기능 (channelSpecific)
5. 제약 조건 (constraints)
6. 목표 매핑 (objectiveMapping)
7. API 엔드포인트 매핑
```

### Step 2: config/channels.md 업데이트
```
채널 세팅 정보, API 스펙, 정책 추가
```

### Step 3: config/kpi_definitions.md 업데이트
```
해당 채널의 벤치마크 데이터 추가
```

### Step 4: 에이전트 가이드 업데이트
```
각 에이전트의 채널별 가이드에 새 채널 추가:
├── CAMPAIGN_STRATEGIST: 채널 믹스에 포함
├── KEYWORD_RESEARCHER: 해당 채널 키워드/오디언스 리서치
├── AD_CREATIVE: 해당 채널 카피 가이드
├── BID_OPTIMIZER: 해당 채널 입찰 전략
├── ANALYTICS_AGENT: 해당 채널 데이터 수집/분석
└── CHANNEL_SPECIALIST: 해당 채널 세팅 가이드
```

### Step 5: 테스트 및 검증
```
1. 어댑터 인터페이스 완성도 확인
2. 기존 워크플로우와의 호환성 확인
3. 데이터 정합성 확인
4. TEAM_LEAD 검수
```

---

## 어댑터 간 데이터 변환

### 통합 메트릭 표준

각 채널의 메트릭 명칭이 다르므로, 어댑터가 내부 표준으로 변환한다.

| 내부 표준 | 네이버 | 카카오 | 메타 | 구글 |
|----------|--------|--------|------|------|
| impressions | impCnt | impression | impressions | metrics.impressions |
| clicks | clkCnt | click | clicks | metrics.clicks |
| cost | salesAmt | cost | spend | metrics.cost_micros/1000000 |
| conversions | ccCnt | conversion | actions[purchase] | metrics.conversions |
| revenue | - | - | action_values[purchase] | metrics.conversions_value |

---

## 참고 파일

| 파일 | 용도 |
|------|------|
| `config/channels.md` | 채널별 상세 API 스펙 |
| `plugin/interface.md` | 플러그인 인터페이스 전체 |
| `plugin/integration_guide.md` | 연동 가이드 |
