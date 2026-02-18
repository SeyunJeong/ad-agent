# Performance Marketing Agent SaaS 사업계획서

**작성일**: 2026-02-17
**작성팀**: biz-planner (기획부)
**버전**: v1.0
**상태**: 초안 (오너 검토 대기)

---

## 목차

1. [시장 분석](#1-시장-분석)
2. [제품 정의](#2-제품-정의)
3. [타겟 고객](#3-타겟-고객)
4. [차별점 & 경쟁 우위](#4-차별점--경쟁-우위)
5. [수익 모델](#5-수익-모델)
6. [플러그인 API 스펙 초안](#6-플러그인-api-스펙-초안)
7. [로드맵](#7-로드맵)

---

## 1. 시장 분석

### 1.1 한국 디지털 광고 시장 규모 및 성장률

#### 전체 광고 시장

| 구분 | 수치 | 출처 |
|------|------|------|
| 2024년 방송통신 광고비 총액 | **17조 1,263억 원** (전년 대비 +3.5%) | [매드타임스, 방송통신광고비 조사](https://www.madtimes.co.kr/news/articleView.html?idxno=22798) |
| 2024년 온라인 광고비 | **10조 1,011억 원** (전년 대비 +7.9%) | [서울경제](https://www.sedaily.com/NewsView/2K781GQN0I) |
| 2025년 온라인 광고비 전망 | **10조 7,204억 원** (+6.1%) | [전자신문](https://www.etnews.com/20250109000246) |
| 2025년 디지털 광고 시장 (USD) | **USD 117억** | [Statista](https://www.statista.com/outlook/dmo/digital-advertising/south-korea) |
| 2025-2033 전체 광고 시장 CAGR | **5.93%** (2033년 229억 달러 전망) | [IMARC Group](https://www.globalresearch.kr/markets/advertising-market-imarc/) |
| 2025-2030 디지털 광고 CAGR | **4.91% ~ 18.1%** (조사기관별 상이) | [Grand View Research](https://www.grandviewresearch.com/horizon/outlook/digital-advertising-market/south-korea) |

#### 온라인 광고 세부 구성 (2024년)

| 구분 | 금액 | 비중 |
|------|------|------|
| 모바일 광고 | 7조 7,899억 원 | 77.1% |
| PC 광고 | 2조 3,112억 원 | 22.9% |
| **합계** | **10조 1,011억 원** | 전체 광고비의 **59%** |

> **핵심 시사점**: 한국 온라인 광고 시장은 2024년 사상 최초 10조 원을 돌파했으며, 전체 광고 시장의 60%에 육박한다. 특히 모바일 광고가 77%를 차지하여, 모바일 퍼스트 전략이 필수적이다.

---

### 1.2 퍼포먼스 마케팅 에이전시 시장 현황

#### 시장 구조

한국 퍼포먼스 마케팅 에이전시 시장은 크게 세 층으로 나뉜다:

| 계층 | 대표 기업 | 특징 |
|------|-----------|------|
| **대형 종합 대행사** | 이노션, 제일기획, HS애드 | 대기업 중심, 풀서비스 |
| **중형 퍼포먼스 전문** | 에코마케팅, 플레이디, 이엠넷, 모비데이즈 | 성과 기반 과금, 기술 중심 |
| **소형/1인 에이전시** | 다수 (수천 개 추정) | 프리랜서 및 소규모 팀 |

**에코마케팅**은 2024년 매출 4,000억 원을 돌파하며 퍼포먼스 마케팅 전문 대행사의 대표격으로 자리잡았다.

#### 시장 변화 동향

- **수수료 구조 붕괴**: 전통적 15~20% 대행 수수료가 경쟁 심화로 10%, 7%, 5%까지 하락하는 추세 ([아이보스](https://www.i-boss.co.kr/ab-2110-14887))
- **대행사 → SaaS 전환**: 인건비 대비 마진 하락으로 에이전시 모델의 한계가 드러나며, 기술 기반 SaaS 모델로의 전환 시도가 증가
- **AI 도입 가속화**: 머신러닝 기반 입찰 최적화가 CPA를 평균 34% 절감하는 효과를 입증 ([디플러스](https://www.dplus.kr/2025-performance-marketing/))

> **핵심 시사점**: 대행사 수수료 하락과 인건비 상승이 동시에 일어나며, "사람이 아닌 기술로 마케팅하는" SaaS 모델에 대한 수요가 급증하고 있다.

---

### 1.3 주요 광고 채널별 특성

#### 네이버 검색광고

| 항목 | 내용 |
|------|------|
| **시장 점유율** | 검색 시장 약 40% (2025년 기준, 구글에 1위 양보) |
| **광고 상품** | 검색광고 (파워링크, 쇼핑검색), 디스플레이 (GFA), 브랜드검색 |
| **과금 방식** | CPC (클릭당 과금) 중심 |
| **API 지원** | 네이버 검색광고 API (캠페인/키워드 관리, 보고서 조회) |
| **특이사항** | 한국 특화 검색 생태계 (스마트스토어, 블로그, 카페 연동), AI 입찰 시스템 도입 |
| **월 최소 집행액** | 제한 없음 (일 최소 70원/CPC) |

**출처**: [koreatraffic.com](https://www.koreatraffic.com/kr/news/search-engine-market-share-korea-2025), [naver/searchad-apidoc](https://github.com/naver/searchad-apidoc)

#### 카카오모먼트 (카카오 비즈보드)

| 항목 | 내용 |
|------|------|
| **플랫폼 커버리지** | 카카오톡, 다음, 카카오스토리, 카카오페이지 등 |
| **광고 상품** | 디스플레이, 동영상, 카탈로그, 메시지(친구톡/알림톡) |
| **과금 방식** | CPM, CPC, CPA 다양 |
| **API 지원** | 카카오모먼트 API (캠페인/광고그룹/소재 관리, ON/OFF, 입찰금액 변경) |
| **특이사항** | **공식 대행사만 API 접근 가능** (권한 신청 필수) |
| **강점** | 카카오톡 4,700만 MAU 기반 높은 도달률 |

**출처**: [Kakao Developers](https://developers.kakao.com/docs/latest/ko/kakaomoment/reference)

#### 메타 (Instagram / Facebook)

| 항목 | 내용 |
|------|------|
| **시장 위치** | 인스타그램 — 한국인 사용 1위 SNS 앱 (2025년) |
| **광고 상품** | 피드, 스토리, 릴스, 카루셀, 다이내믹 광고 |
| **과금 방식** | CPM, CPC, CPA, ROAS 기반 최적화 |
| **API 지원** | Meta Marketing API (캠페인 CRUD, 자동 규칙, 크리에이티브 관리) |
| **특이사항** | AI 기반 Advantage+ 캠페인으로 전 과정 자동화 추진 (2026년 완성 목표) |
| **강점** | 강력한 타겟팅 (관심사, 유사 오디언스), 글로벌 연동 |

**출처**: [openads.co.kr](https://openads.co.kr/content/contentDetail?contsId=16397), [적정마케팅연구소](https://segama.co.kr/blog/25149/)

#### 구글 광고 (Google Ads)

| 항목 | 내용 |
|------|------|
| **시장 점유율** | 검색 시장 50% 돌파 (2025년 최초 1위) |
| **광고 상품** | 검색, 디스플레이, 유튜브, 쇼핑, Performance Max |
| **과금 방식** | CPC, CPV, CPM, 전환 최적화 입찰 |
| **API 지원** | Google Ads API (캠페인 관리, 자동 입찰, 커스텀 리포팅, 인벤토리 연동) |
| **특이사항** | Performance Max — 1,200개 이상 변수를 ML로 분석하여 자동 최적화 |
| **강점** | 글로벌 최대 광고 플랫폼, 유튜브 연동, 검색 점유율 상승 중 |

**출처**: [Google Ads API](https://developers.google.com/google-ads/api/docs/get-started/introduction), [gyeongsang.kr](https://gyeongsang.kr/entry/%E2%80%9C2025-%EA%B2%80%EC%83%89%EC%8B%9C%EC%9E%A5-%EC%A0%90%EC%9C%A0%EC%9C%A8-%EC%99%84%EC%A0%84-%EC%A0%95%EB%A6%AC-%EB%84%A4%EC%9D%B4%EB%B2%84-vs-%EA%B5%AC%EA%B8%80-10%EB%85%84-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A1%9C-%EB%B3%B8-%EC%8A%B9%EC%9E%90%E2%80%9D)

---

### 1.4 AI 기반 광고 최적화 트렌드

#### 2026년 AI 마케팅 투자 우선순위

| 분야 | 투자 비중 |
|------|----------|
| 콘텐츠 최적화 | 23% |
| 마케팅 자동화 | 21% |
| AI 엔진 최적화 (AEO) | 16% |
| 이미지 제작 | 17% |
| 숏폼 동영상 제작 | 15% |
| 광고 제작 | 13% |

**출처**: [디지털마케팅연구회, 2026년 AI 마케팅 트렌드 7대 핵심 키워드](https://www.madtimes.co.kr/news/articleView.html?idxno=25860)

#### 주요 트렌드

1. **AI가 마케팅 운영체제의 기반 레이어로 진화**: 개별 도구가 아닌 전체 마케팅 워크플로우를 AI가 관장 ([openads.co.kr](https://openads.co.kr/content/contentDetail?contsId=17722))
2. **플랫폼 자체 AI 고도화**: 구글 Performance Max, 메타 Advantage+, 네이버 AI 입찰이 표준화
3. **생성형 AI 활용 폭발**: 광고 카피, 이미지, 영상까지 자동 생성 → 제작 비용 90% 절감 가능
4. **실증 사례**: 삼성전자 갤럭시 S25 — AI 솔루션으로 예산 2배 투입에도 ROAS 안정적 유지 ([리멤버](https://market.rememberapp.co.kr/blog/insights/ai-%EB%A7%88%EC%BC%80%ED%8C%85-%ED%8A%B8%EB%A0%8C%EB%93%9C-2026-%EC%83%9D%EC%84%B1%ED%98%95-ai-%EC%8B%9C%EB%8C%80%EC%9D%98-%EC%A0%84%EB%9E%B5%EA%B3%BC-%EC%84%B1%EA%B3%B5-%EC%82%AC%EB%A1%80))

> **핵심 시사점**: AI는 이미 선택이 아닌 필수가 되었다. 그러나 대부분의 한국 중소기업은 AI 도구를 직접 활용할 역량이 없다. 이 간극이 바로 우리 제품의 기회다.

---

## 2. 제품 정의

### 2.1 제품명 및 개요

**제품명**: **AdAgent** (가칭)
**한글명**: 애드에이전트
**태그라인**: "AI가 대행사를 대체합니다"

AdAgent는 AI 에이전트 기반 퍼포먼스 마케팅 자동화 SaaS로, 한국 시장에 특화된 멀티채널 광고 운영 플랫폼이다. 네이버, 카카오, 메타, 구글 4대 채널을 하나의 대시보드에서 관리하며, AI가 전략 수립부터 크리에이티브 생성, 입찰 최적화, 성과 분석까지 전 과정을 자동화한다.

---

### 2.2 핵심 기능 목록 및 상세 스펙

#### F1. 캠페인 전략 수립 (Strategy Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 비즈니스 목표, 예산, 업종을 입력하면 AI가 최적 채널 믹스 및 캠페인 구조를 자동 설계 |
| **입력** | 업종, 월 예산, KPI (전환/인지도/트래픽), 타겟 지역, 경쟁사 URL |
| **출력** | 채널별 예산 배분, 캠페인 구조도, 예상 KPI, 실행 타임라인 |
| **AI 활용** | LLM 기반 전략 추론 + 업종별 벤치마크 데이터 참조 |
| **차별점** | 한국 시장 특화 벤치마크 DB (네이버/카카오 포함) |

#### F2. 키워드 리서치 (Keyword Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 업종/제품 키워드에서 확장 키워드를 자동 발굴하고, 검색량/경쟁도/예상 CPC를 분석 |
| **지원 채널** | 네이버 검색광고, 구글 검색광고 |
| **데이터 소스** | 네이버 키워드 도구 API, 구글 Keyword Planner API, 자체 크롤링 데이터 |
| **출력** | 키워드 목록 (검색량, 경쟁도, 예상 CPC, 추천 입찰가), 롱테일 키워드 제안, 네거티브 키워드 제안 |
| **AI 활용** | 의미론적 키워드 확장 (LLM), 시즌/트렌드 기반 키워드 예측 |

#### F3. 크리에이티브 생성 (Creative Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 광고 카피 (제목/설명문), 배너 이미지, 숏폼 영상 스크립트를 AI로 자동 생성 |
| **지원 유형** | 검색광고 카피, SNS 피드 이미지, 카루셀, 스토리/릴스 스크립트 |
| **입력** | 제품/서비스 정보, 브랜드 톤앤매너, 참고 이미지/URL |
| **출력** | 채널별 규격에 맞는 광고 소재 (텍스트 + 이미지 + 영상 스크립트) |
| **AI 활용** | 텍스트 — LLM (한국어 특화), 이미지 — 생성형 AI, 영상 — 스크립트 + 스토리보드 |
| **차별점** | 한국어 광고 카피 전문 모델 (존칭/반말/이모지 톤 조절), 네이버 광고 규정 자동 준수 |

#### F4. 입찰 최적화 (Bidding Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 실시간 성과 데이터를 기반으로 입찰가를 자동 조정하여 ROAS/CPA 최적화 |
| **지원 채널** | 네이버 (CPC 입찰), 카카오 (CPM/CPC), 메타 (자동입찰 연동), 구글 (스마트입찰 보완) |
| **최적화 기준** | 목표 CPA, 목표 ROAS, 최대 전환 수, 예산 소진율 |
| **작동 방식** | 15분 간격 성과 수집 → ML 모델 예측 → 입찰가 자동 조정 → 이상 감지 알림 |
| **AI 활용** | 시계열 예측 모델 (전환율 예측), 강화학습 기반 입찰 최적화 |
| **안전장치** | 일예산 상한, 급격한 입찰가 변동 제한 (전일 대비 +-30%), 이상치 감지 시 자동 중단 + 알림 |

#### F5. 성과 분석 (Analytics Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 전 채널 성과를 통합 대시보드에서 실시간 모니터링하고, AI가 인사이트를 자동 생성 |
| **주요 지표** | 노출, 클릭, CTR, CPC, 전환, CPA, ROAS, LTV |
| **통합 범위** | 네이버 + 카카오 + 메타 + 구글 성과를 단일 뷰로 통합 |
| **AI 인사이트** | "지난주 대비 네이버 CPC가 15% 상승 — 경쟁 키워드 증가 추정. 롱테일 키워드 확대 제안" 형태의 자연어 분석 리포트 |
| **리포팅** | 일간/주간/월간 자동 리포트 생성, PDF/Excel 내보내기, 슬랙/이메일 자동 발송 |
| **차별점** | 채널 간 어트리뷰션 분석 (네이버 검색 → 메타 리타겟팅 → 전환 경로 추적) |

#### F6. A/B 테스트 (Testing Agent)

| 항목 | 상세 |
|------|------|
| **기능** | 광고 소재, 타겟 오디언스, 랜딩 페이지 등 변수를 자동으로 A/B 테스트하고 통계적 유의미성을 판단 |
| **테스트 대상** | 광고 카피, 이미지/영상, 타겟 오디언스, 입찰 전략, 랜딩 페이지 |
| **작동 방식** | 변수 설정 → 트래픽 자동 분배 → 통계적 유의성 도달 시 승자 자동 선택 → 패자 자동 중단 |
| **통계 기법** | 베이지안 A/B 테스트 (빠른 결론), 다중 비교 보정 (Bonferroni) |
| **AI 활용** | 테스트 변수 자동 제안 ("이 광고의 CTA를 변경하면 CTR +12% 예상"), 결과 해석 자연어 제공 |

---

### 2.3 채널별 지원 범위 매트릭스

| 기능 | 네이버 | 카카오 | 메타 | 구글 |
|------|--------|--------|------|------|
| 캠페인 자동 생성 | O | O | O | O |
| 키워드 리서치 | O | - | - | O |
| 크리에이티브 생성 | O | O | O | O |
| 입찰 최적화 | O | O | O | O |
| 성과 대시보드 | O | O | O | O |
| A/B 테스트 | O | O | O | O |
| 자동 규칙 (ON/OFF) | O | O | O | O |
| 오디언스 관리 | - | O | O | O |
| 카탈로그/쇼핑 | O (스마트스토어) | O | O | O |

---

## 3. 타겟 고객

### 3.1 1차 타겟: 한국 중소기업 / 스타트업

#### 시장 규모

- 한국 중소기업 수: **804.3만 개** (2022년 기준, [중소벤처기업부](https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=1057029&parentSeq=1057029))
- 연간 신규 창업: **118.3만 개** (2024년)
- 스타트업 신규 창업: **21.5만 개** (2024년, [유니콘팩토리](https://www.unicornfactory.co.kr/article/2025022717011043195))

#### 페인 포인트

| 문제 | 현재 해결책 | 한계 |
|------|------------|------|
| 마케팅 인력 부재 | 대행사 위탁 | 월 수백만 원 수수료, 성과 불투명 |
| 광고 운영 전문성 부족 | 직접 운영 시도 | 비효율적 예산 집행, 학습 비용 높음 |
| 멀티채널 관리 어려움 | 채널별 각각 로그인 | 시간 낭비, 통합 분석 불가 |
| 크리에이티브 제작 비용 | 외주 디자이너 | 속도 느림, 반복 비용 |

#### 예상 고객 프로필

- 월 광고 예산: 100만 ~ 3,000만 원
- 마케팅 전담 인원: 0 ~ 1명
- 업종: 이커머스, F&B, 교육, 뷰티, 앱 서비스
- 의사결정자: 대표, COO, 마케팅 담당자 (1인 겸업)

#### TAM/SAM/SOM 추정

| 구분 | 산출 근거 | 규모 |
|------|----------|------|
| **TAM** (전체 시장) | 한국 디지털 광고 시장 | **10.7조 원** (2025년) |
| **SAM** (접근 가능 시장) | 중소기업 디지털 광고비 (전체의 ~30%) | **약 3.2조 원** |
| **SOM** (확보 가능 시장) | SAM의 1% (SaaS 도구 구독 + 수수료) | **약 320억 원** |

---

### 3.2 2차 타겟: 마케팅 에이전시

#### 페인 포인트

| 문제 | 현재 해결책 | 한계 |
|------|------------|------|
| 대행사 수수료 하락 (15% → 5%) | 인원 감축, 저가 경쟁 | 품질 저하, 인재 유출 |
| 반복 업무 (리포팅, 입찰 조정) | 수작업 + 엑셀 | 인건비 증가, 실수 발생 |
| 클라이언트 다수 관리 | 담당자별 운영 | 스케일 불가 |

#### 예상 고객 프로필

- 운영 광고주 수: 10 ~ 100개
- 팀 규모: 5 ~ 30명
- 니즈: 1인당 관리 광고주 수 증가 (현재 3~5개 → 목표 10~15개)
- 의사결정자: 대표, 운영팀장

#### 가치 제안

"AdAgent로 리포팅 80%, 입찰 조정 90%를 자동화하면, 같은 인원으로 3배의 광고주를 관리할 수 있습니다."

---

### 3.3 3차 타겟: 인하우스 마케터

#### 페인 포인트

- 1인 마케팅 팀으로 4개 채널 동시 운영 부담
- 크리에이티브 제작에 시간의 60% 소요
- 경영진에게 보고할 통합 대시보드 부재

#### 예상 고객 프로필

- 기업 규모: 중견기업 (매출 100억 ~ 1,000억)
- 마케팅 팀: 1 ~ 3명
- 월 광고 예산: 1,000만 ~ 1억 원
- 의사결정자: CMO, 마케팅 팀장

---

## 4. 차별점 & 경쟁 우위

### 4.1 경쟁 환경 분석

| 경쟁사 | 유형 | 강점 | 약점 |
|--------|------|------|------|
| **아드리엘 (Adriel)** | 대시보드 SaaS | 650개 채널 통합, 글로벌 확장, Series B 투자 ($13M) | 광고 운영 자동화 약함, 크리에이티브 생성 없음 |
| **레버 (LEVER)** | 자동화 SaaS | 매체 데이터 자동 수집, 리포팅 자동화 | 한국 특화 부족, AI 에이전트 기능 없음 |
| **비즈스프링 (BizSpring)** | 애널리틱스 | 고객 행동 분석, 개인화 엔진 | 광고 운영 기능 없음, 분석에 한정 |
| **애드이피션시** | 대행사+SaaS | 퍼포먼스 마케팅 실행력 | SaaS 제품화 미흡 |
| **구글 Performance Max** | 플랫폼 내장 | 구글 생태계 최적화 | 구글만 지원, 멀티채널 불가 |
| **메타 Advantage+** | 플랫폼 내장 | 메타 생태계 최적화 | 메타만 지원, 멀티채널 불가 |

**출처**: [브랜드브리프 - 아드리엘](https://www.brandbrief.co.kr/news/articleView.html?idxno=6726), [레버](https://lever.me/), [비즈스프링](https://bizspring.co.kr/solution.php)

---

### 4.2 AdAgent의 핵심 차별점

#### 차별점 1: AI 에이전트 기반 "풀스택" 자동화

```
기존 SaaS:  데이터 수집 → [사람] → 분석 → [사람] → 의사결정 → [사람] → 실행
AdAgent:   데이터 수집 → [AI] → 분석 → [AI] → 의사결정 → [AI] → 실행 → [사람 승인]
```

- 아드리엘/레버: **데이터 시각화**에 집중 (Observe)
- AdAgent: **전략 → 실행 → 최적화 → 보고** 전 과정 자동화 (Observe + Decide + Act)
- 사람은 최종 승인만 담당 → "AI 대행사" 경험 제공

#### 차별점 2: 한국 4대 채널 네이티브 지원

- **네이버 검색광고** + **카카오모먼트**: 한국 특화 채널을 1등 시민으로 지원
- 글로벌 SaaS (HubSpot, Smartly.io 등)는 네이버/카카오 미지원
- 한국어 광고 카피 전문 생성 (존칭, 이모지, 맞춤법 규정 준수)

#### 차별점 3: 크리에이티브 생성 내장

- 대부분 경쟁사: 성과 분석/대시보드만 제공
- AdAgent: **광고 소재까지 AI가 생성** (카피 + 이미지 + 영상 스크립트)
- 소재 제작 → 업로드 → 테스트 → 최적화가 하나의 워크플로우로 연결

#### 차별점 4: 에이전트 회사 시너지

- 자사 마케팅부(thread-team)의 콘텐츠 제작 노하우 내재화
- 자사 총무부(finance)의 비용 추적 로직 연동
- 자사 기획부(biz-planner)의 전략 프레임워크 탑재
- 다른 SaaS 대비 **실전 검증된 에이전트 아키텍처** 보유

---

## 5. 수익 모델

### 5.1 구독 플랜

| 플랜 | **Free** | **Pro** | **Enterprise** |
|------|----------|---------|----------------|
| **월 가격** | 0원 | 29만 원/월 | 99만 원~/월 (협의) |
| **연간 결제** | - | 24만 원/월 (17% 할인) | 별도 협의 |
| **광고 계정 수** | 1개 | 5개 | 무제한 |
| **지원 채널** | 1개 | 4개 (네이버+카카오+메타+구글) | 4개 + 커스텀 |
| **월 광고비 한도** | 300만 원 | 5,000만 원 | 무제한 |
| **AI 크리에이티브** | 월 10건 | 월 200건 | 무제한 |
| **AI 전략 리포트** | 기본 (주 1회) | 고급 (일 1회) | 실시간 + 커스텀 |
| **A/B 테스트** | 수동만 | 자동 | 자동 + 멀티변수 |
| **입찰 최적화** | 제안만 | 자동 실행 | 자동 + 커스텀 룰 |
| **데이터 보존** | 30일 | 1년 | 무제한 |
| **지원** | 셀프서비스 | 이메일 + 챗 | 전담 매니저 |

### 5.2 광고비 연동 수수료 (Add-on)

Pro/Enterprise 고객 중 **월 5,000만 원 이상 광고비 집행** 고객 대상:

| 월 광고비 | 수수료율 | 설명 |
|----------|---------|------|
| 5,000만 ~ 1억 원 | 3% | 기존 대행사 대비 1/3 수준 |
| 1억 ~ 5억 원 | 2% | 볼륨 디스카운트 |
| 5억 원 이상 | 1.5% | 대형 광고주 유치 |

> **가격 설정 근거**: 기존 대행사 수수료 5~15% 대비 **1/3 ~ 1/5 수준**으로 설정. SaaS의 한계 비용이 거의 0이므로 낮은 수수료율에서도 높은 마진 확보 가능.

### 5.3 수익 시나리오 (12개월 후)

| 구분 | 보수적 | 기본 | 공격적 |
|------|--------|------|--------|
| Free 사용자 | 500 | 1,000 | 2,000 |
| Pro 구독자 | 50 | 100 | 200 |
| Enterprise | 3 | 5 | 10 |
| 월 구독 매출 | 1,747만 원 | 3,890만 원 | 8,780만 원 |
| 월 수수료 매출 | 500만 원 | 1,500만 원 | 3,000만 원 |
| **월 총매출** | **2,247만 원** | **5,390만 원** | **1.18억 원** |
| **연 매출** | **2.7억 원** | **6.5억 원** | **14.1억 원** |

> **손익분기점**: Pro 구독 80명 + 수수료 매출 월 1,000만 원 = 약 서비스 출시 6~9개월 후 예상

---

## 6. 플러그인 API 스펙 초안

### 6.1 아키텍처 개요

```
┌─────────────────────────────────────────────────────────┐
│                    AdAgent SaaS Platform                 │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Strategy │  │ Keyword  │  │ Creative │  │Bidding │  │
│  │  Agent   │  │  Agent   │  │  Agent   │  │ Agent  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       │              │              │             │       │
│  ┌────┴──────────────┴──────────────┴─────────────┴──┐   │
│  │              Orchestration Layer                   │   │
│  │         (Agent Coordinator + Task Queue)           │   │
│  └────────────────────┬──────────────────────────────┘   │
│                       │                                  │
│  ┌────────────────────┴──────────────────────────────┐   │
│  │              Channel Adapter Layer                 │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐ │   │
│  │  │ Naver  │ │ Kakao  │ │  Meta  │ │   Google   │ │   │
│  │  │Adapter │ │Adapter │ │Adapter │ │  Adapter   │ │   │
│  │  └───┬────┘ └───┬────┘ └───┬────┘ └─────┬──────┘ │   │
│  └──────┼──────────┼──────────┼─────────────┼────────┘   │
│         │          │          │             │            │
└─────────┼──────────┼──────────┼─────────────┼────────────┘
          │          │          │             │
    ┌─────┴──┐ ┌────┴───┐ ┌───┴────┐ ┌──────┴─────┐
    │ Naver  │ │ Kakao  │ │  Meta  │ │  Google    │
    │  Ads   │ │Moment  │ │Marketing│ │  Ads      │
    │  API   │ │  API   │ │  API   │ │  API      │
    └────────┘ └────────┘ └────────┘ └────────────┘
```

### 6.2 외부 연동 API (Plugin API)

AdAgent를 외부 시스템에 플러그인으로 연결하기 위한 REST API:

#### 인증

```
POST /api/v1/auth/token
Content-Type: application/json

{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

모든 API 호출은 `Authorization: Bearer {access_token}` 헤더 필요.

---

#### 핵심 API 엔드포인트

##### 캠페인 관리

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/campaigns` | 새 캠페인 생성 (AI 전략 자동 수립) |
| `GET` | `/api/v1/campaigns` | 캠페인 목록 조회 |
| `GET` | `/api/v1/campaigns/{id}` | 캠페인 상세 조회 |
| `PATCH` | `/api/v1/campaigns/{id}` | 캠페인 수정 |
| `DELETE` | `/api/v1/campaigns/{id}` | 캠페인 삭제 |
| `POST` | `/api/v1/campaigns/{id}/launch` | 캠페인 집행 시작 |
| `POST` | `/api/v1/campaigns/{id}/pause` | 캠페인 일시 중지 |

**캠페인 생성 요청 예시:**

```json
POST /api/v1/campaigns
{
  "name": "봄 시즌 프로모션",
  "objective": "conversions",
  "budget": {
    "monthly_total": 5000000,
    "currency": "KRW"
  },
  "channels": ["naver", "meta", "google"],
  "targeting": {
    "locations": ["서울", "경기"],
    "age_range": { "min": 25, "max": 45 },
    "gender": "all",
    "interests": ["패션", "뷰티"]
  },
  "product": {
    "name": "스프링 컬렉션",
    "url": "https://example.com/spring",
    "description": "2026 봄 신상품 컬렉션"
  },
  "ai_strategy": true
}
```

**응답 예시:**

```json
{
  "id": "camp_abc123",
  "status": "draft",
  "strategy": {
    "channel_allocation": {
      "naver": { "budget": 2000000, "type": "search" },
      "meta": { "budget": 2000000, "type": "feed+stories" },
      "google": { "budget": 1000000, "type": "pmax" }
    },
    "estimated_kpi": {
      "impressions": 500000,
      "clicks": 15000,
      "conversions": 300,
      "estimated_cpa": 16667
    }
  },
  "created_at": "2026-02-17T09:00:00+09:00"
}
```

##### 키워드 리서치

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/keywords/research` | 키워드 리서치 실행 |
| `GET` | `/api/v1/keywords/suggestions` | AI 키워드 추천 |

```json
POST /api/v1/keywords/research
{
  "seed_keywords": ["여성 봄 자켓", "스프링 코트"],
  "channels": ["naver", "google"],
  "include_longtail": true,
  "include_negatives": true
}
```

##### 크리에이티브 생성

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/creatives/generate` | AI 광고 소재 생성 |
| `GET` | `/api/v1/creatives/{id}` | 생성된 소재 조회 |
| `POST` | `/api/v1/creatives/{id}/variations` | 소재 변형 생성 (A/B 테스트용) |

```json
POST /api/v1/creatives/generate
{
  "campaign_id": "camp_abc123",
  "type": "search_ad",
  "channel": "naver",
  "product_info": {
    "name": "스프링 코트",
    "price": 89000,
    "features": ["울 혼방", "오버핏", "5가지 컬러"]
  },
  "tone": "casual_friendly",
  "count": 5
}
```

##### 성과 분석

| Method | Endpoint | 설명 |
|--------|----------|------|
| `GET` | `/api/v1/analytics/dashboard` | 통합 대시보드 데이터 |
| `GET` | `/api/v1/analytics/campaigns/{id}` | 캠페인별 성과 |
| `GET` | `/api/v1/analytics/channels` | 채널별 성과 비교 |
| `POST` | `/api/v1/analytics/reports` | 커스텀 리포트 생성 |
| `GET` | `/api/v1/analytics/insights` | AI 인사이트 조회 |

```json
GET /api/v1/analytics/dashboard?period=last_7d

Response:
{
  "period": "2026-02-10 ~ 2026-02-17",
  "summary": {
    "total_spend": 3500000,
    "impressions": 450000,
    "clicks": 12500,
    "ctr": 2.78,
    "conversions": 280,
    "cpa": 12500,
    "roas": 3.2
  },
  "by_channel": {
    "naver": { "spend": 1500000, "conversions": 120, "cpa": 12500 },
    "meta": { "spend": 1200000, "conversions": 100, "cpa": 12000 },
    "google": { "spend": 800000, "conversions": 60, "cpa": 13333 }
  },
  "ai_insights": [
    {
      "type": "optimization",
      "message": "네이버 '봄 자켓' 키워드의 CPC가 전주 대비 20% 상승했습니다. 롱테일 키워드 '여성 봄 자켓 오버핏'으로 확장하면 CPC를 30% 절감할 수 있습니다.",
      "action": "keyword_expansion",
      "confidence": 0.85
    }
  ]
}
```

##### A/B 테스트

| Method | Endpoint | 설명 |
|--------|----------|------|
| `POST` | `/api/v1/tests` | A/B 테스트 생성 |
| `GET` | `/api/v1/tests/{id}` | 테스트 결과 조회 |
| `POST` | `/api/v1/tests/{id}/apply-winner` | 승자 소재 적용 |

##### Webhook (이벤트 알림)

| Event | 설명 |
|-------|------|
| `campaign.budget_depleted` | 예산 소진 임박 |
| `campaign.performance_alert` | 성과 이상 감지 |
| `test.completed` | A/B 테스트 통계적 유의성 도달 |
| `creative.generated` | 크리에이티브 생성 완료 |
| `report.ready` | 리포트 생성 완료 |
| `bidding.anomaly` | 입찰 이상 감지 |

```json
POST /api/v1/webhooks
{
  "url": "https://your-system.com/webhook",
  "events": ["campaign.performance_alert", "test.completed"],
  "secret": "your_webhook_secret"
}
```

---

### 6.3 채널 어댑터 구조

각 광고 채널은 통일된 인터페이스(Adapter Pattern)로 추상화된다:

```python
# 채널 어댑터 인터페이스 (Python pseudocode)
class ChannelAdapter(ABC):
    """모든 채널 어댑터가 구현해야 하는 인터페이스"""

    @abstractmethod
    async def create_campaign(self, config: CampaignConfig) -> CampaignResult:
        """채널에 캠페인 생성"""
        pass

    @abstractmethod
    async def update_bid(self, campaign_id: str, bid: BidConfig) -> BidResult:
        """입찰가 업데이트"""
        pass

    @abstractmethod
    async def get_performance(self, campaign_id: str, period: DateRange) -> PerformanceData:
        """성과 데이터 조회"""
        pass

    @abstractmethod
    async def create_creative(self, campaign_id: str, creative: CreativeConfig) -> CreativeResult:
        """광고 소재 업로드"""
        pass

    @abstractmethod
    async def toggle_status(self, campaign_id: str, status: str) -> StatusResult:
        """캠페인 ON/OFF"""
        pass

    @abstractmethod
    async def get_keywords(self, query: str) -> KeywordData:
        """키워드 데이터 조회 (검색 채널만)"""
        pass


# 채널별 구현
class NaverAdapter(ChannelAdapter):
    """네이버 검색광고 API 연동"""
    BASE_URL = "https://api.searchad.naver.com"
    # 네이버 API 키 인증 (액세스 라이선스 + 비밀키)

class KakaoAdapter(ChannelAdapter):
    """카카오모먼트 API 연동"""
    BASE_URL = "https://kapi.kakao.com/v2/moment"
    # OAuth 2.0 인증 (공식 대행사 권한 필요)

class MetaAdapter(ChannelAdapter):
    """Meta Marketing API 연동"""
    BASE_URL = "https://graph.facebook.com/v19.0"
    # OAuth 2.0 + 시스템 유저 토큰

class GoogleAdapter(ChannelAdapter):
    """Google Ads API 연동"""
    # google-ads Python 라이브러리 사용
    # OAuth 2.0 + 개발자 토큰
```

#### 어댑터별 주의사항

| 채널 | 인증 방식 | 제약 사항 | Rate Limit |
|------|----------|----------|------------|
| 네이버 | API 키 (라이선스 + 시크릿) | 일부 기능 대행사 전용 | 명시 없음 (보수적 운용 권장) |
| 카카오 | OAuth 2.0 | **공식 대행사만 API 접근 가능** | 초당 10회 (추정) |
| 메타 | OAuth 2.0 + 시스템 유저 | 비즈니스 검증 필요 | 계정당 시간당 호출 제한 |
| 구글 | OAuth 2.0 + 개발자 토큰 | 개발자 토큰 승인 필요 (약 2주) | 분당 15,000 요청 |

> **중요**: 카카오모먼트 API는 공식 대행사에만 권한이 부여된다. 따라서 **카카오 광고 공식 대행사 등록**이 사업의 전제조건이다.

---

### 6.4 연동 가능한 외부 시스템

| 시스템 | 연동 방식 | 활용 |
|--------|----------|------|
| **Slack** | Webhook + Bot | 실시간 알림, 성과 리포트 발송 |
| **카카오톡** | 알림톡 API | 한국 사용자 친화적 알림 |
| **텔레그램** | Bot API | 자사 인프라 활용 (infra/telegram) |
| **Google Sheets** | Sheets API | 리포트 자동 내보내기 |
| **Notion** | Notion API | 마케팅 캘린더, 대시보드 |
| **Shopify/Cafe24** | 각 API | 이커머스 전환 추적, 상품 카탈로그 동기화 |
| **GA4** | Google Analytics API | 웹사이트 전환 데이터 연동 |
| **에어브릿지/앱스플라이어** | MMP API | 앱 어트리뷰션 데이터 |

---

## 7. 로드맵

### Phase 1: MVP (1개월)

**목표**: 핵심 가치를 증명할 수 있는 최소 제품

| 주차 | 작업 | 산출물 |
|------|------|--------|
| Week 1 | 아키텍처 설계 + 인프라 셋업 | 시스템 설계 문서, DB 스키마, CI/CD 파이프라인 |
| Week 1 | 네이버 검색광고 어댑터 개발 | NaverAdapter (캠페인 CRUD, 키워드 조회, 성과 조회) |
| Week 2 | 구글 Ads 어댑터 개발 | GoogleAdapter (캠페인 CRUD, 키워드 조회, 성과 조회) |
| Week 2 | AI 크리에이티브 생성 (텍스트) | 검색광고 카피 자동 생성 (제목+설명문) |
| Week 3 | 통합 대시보드 (기본) | 웹 UI - 네이버+구글 성과 통합 뷰 |
| Week 3 | AI 전략 수립 기본 기능 | 업종+예산 입력 → 채널 배분+키워드 추천 |
| Week 4 | 내부 알파 테스트 | 자사 링크노트 앱 광고에 적용하여 검증 |
| Week 4 | 피드백 반영 + 버그 수정 | 안정화 |

**MVP 핵심 기능**:
- [x] 네이버 + 구글 2개 채널 지원
- [x] AI 검색광고 카피 생성
- [x] AI 키워드 리서치
- [x] 통합 성과 대시보드 (기본)
- [x] AI 전략 제안 (기본)

**MVP 제외 기능**: 카카오, 메타, 입찰 자동화, A/B 테스트, 이미지 생성

---

### Phase 2: V1 (3개월 / MVP 이후)

**목표**: 전체 4개 채널 지원 + 핵심 자동화 기능 완성

| 월 | 작업 | 산출물 |
|------|------|--------|
| Month 2 | 메타 어댑터 개발 | MetaAdapter (캠페인 관리, 오디언스, 크리에이티브) |
| Month 2 | 카카오 어댑터 개발 | KakaoAdapter (대행사 등록 후) |
| Month 2 | AI 이미지 생성 | 배너/피드 이미지 자동 생성 |
| Month 3 | 입찰 최적화 엔진 | ML 기반 자동 입찰 (네이버+구글 우선) |
| Month 3 | A/B 테스트 엔진 | 자동 소재 테스트 + 통계적 유의성 판단 |
| Month 3 | Plugin API v1 | 외부 연동 REST API 공개 |
| Month 4 | 클로즈드 베타 | 20~50개 기업 대상 베타 테스트 |
| Month 4 | 결제 시스템 | 구독 + 수수료 과금 체계 구현 |

**V1 추가 기능**:
- [x] 4개 채널 완전 지원 (네이버+카카오+메타+구글)
- [x] AI 입찰 최적화
- [x] AI 이미지 크리에이티브 생성
- [x] A/B 테스트 자동화
- [x] Plugin API v1 공개
- [x] 구독 결제 시스템

---

### Phase 3: V2 (6개월 / V1 이후)

**목표**: 외부 판매 시작 + 에이전시 모드 추가

| 월 | 작업 | 산출물 |
|------|------|--------|
| Month 5 | 에이전시 모드 (멀티 클라이언트) | 대행사가 고객별 광고 관리 가능 |
| Month 5 | 고급 어트리뷰션 | 크로스채널 전환 경로 분석 |
| Month 6 | 숏폼 영상 스크립트 생성 | 릴스/쇼츠 광고 대응 |
| Month 6 | 공식 출시 + 마케팅 | 프로덕트헌트, 론치, PR |
| Month 7-8 | 이커머스 딥 연동 | 카페24, 스마트스토어, 쿠팡 상품 연동 |
| Month 7-8 | 글로벌 확장 준비 | 영어 UI, 일본 시장 어댑터 (Yahoo! Japan) |

**V2 추가 기능**:
- [x] 에이전시 모드 (화이트라벨)
- [x] 크로스채널 어트리뷰션
- [x] 영상 크리에이티브 지원
- [x] 이커머스 플랫폼 연동
- [x] 글로벌 확장 (일본 우선)

---

### 마일스톤 요약

```
2026.03  ─── MVP 완성 (네이버+구글, AI 카피, 대시보드)
              └── 자사 링크노트 광고로 검증
2026.06  ─── V1 완성 (4채널, 입찰 최적화, A/B 테스트)
              └── 클로즈드 베타 50개사
2026.09  ─── V2 / 공식 출시
              └── 유료 구독 시작
              └── 에이전시 모드
2026.12  ─── 글로벌 확장 시작
              └── 일본 시장 진출
              └── 월 매출 1억 원 목표
```

---

## 부록 A: 리스크 분석

| 리스크 | 영향도 | 발생 확률 | 대응 방안 |
|--------|--------|----------|----------|
| 카카오 API 대행사 등록 지연 | 높음 | 중 | MVP에서 카카오 제외, 나머지 3채널 우선 |
| 네이버/구글 API 정책 변경 | 높음 | 낮음 | 어댑터 패턴으로 격리, 빠른 대응 체계 |
| 플랫폼 자체 AI 강화 (PMax, Advantage+) | 중 | 높음 | 멀티채널 통합이라는 차별점 유지, 플랫폼 AI 위에 메타 최적화 레이어 |
| 경쟁사 유사 제품 출시 | 중 | 중 | 한국 특화 (네이버/카카오) + 에이전트 기술력으로 선점 |
| AI 생성 광고 품질 이슈 | 중 | 중 | 사람 검수 단계 필수 포함, 품질 피드백 루프 |
| 초기 고객 확보 어려움 | 중 | 중 | Free 플랜으로 진입장벽 제거, 자사 마케팅부 활용 |

---

## 부록 B: 기술 스택 (권장)

| 영역 | 기술 | 근거 |
|------|------|------|
| **백엔드** | Python (FastAPI) | AI/ML 생태계, 자사 에이전트 기술 호환 |
| **프론트엔드** | Next.js (React) | 대시보드 UI, SSR 지원 |
| **데이터베이스** | PostgreSQL + Redis | 안정성 + 캐싱/실시간 |
| **큐/워커** | Celery + Redis | 비동기 작업 (입찰 조정, 리포트 생성) |
| **AI/LLM** | Claude API (자사 인프라) | 전략 수립, 카피 생성, 인사이트 |
| **이미지 생성** | DALL-E 3 / Stable Diffusion | 배너/피드 이미지 |
| **ML (입찰)** | scikit-learn / PyTorch | 전환 예측, 입찰 최적화 |
| **인프라** | AWS / Railway | 자사 기존 인프라 활용 |
| **모니터링** | Grafana + Prometheus | 시스템 + 비즈니스 메트릭 |

---

## 부록 C: 필요 리소스

### 팀 구성 (최소)

| 역할 | 인원 | 담당 |
|------|------|------|
| PM / 팀장 | 1명 | 제품 전략, 로드맵, 고객 소통 |
| 백엔드 개발 | 2명 | API, 어댑터, 입찰 엔진 |
| 프론트엔드 개발 | 1명 | 대시보드 UI |
| AI/ML 엔지니어 | 1명 | LLM 연동, 입찰 ML 모델 |
| 마케팅/세일즈 | 1명 (자사 마케팅부 겸업) | GTM, 고객 확보 |

> **에이전트 회사 이점**: AI/ML 엔지니어와 마케팅은 기존 팀 역량을 활용하여 초기 인건비를 절감할 수 있다.

---

## 부록 D: 참고 자료 및 출처

| # | 출처 | 링크 |
|---|------|------|
| 1 | 매드타임스, 2024년 방송통신광고비 조사 | [링크](https://www.madtimes.co.kr/news/articleView.html?idxno=22798) |
| 2 | 서울경제, 국내 온라인 광고비 10조 돌파 | [링크](https://www.sedaily.com/NewsView/2K781GQN0I) |
| 3 | 전자신문, 2025년 온라인 광고 시장 전망 | [링크](https://www.etnews.com/20250109000246) |
| 4 | Statista, Digital Advertising South Korea | [링크](https://www.statista.com/outlook/dmo/digital-advertising/south-korea) |
| 5 | IMARC Group, 한국 광고 시장 규모 2025-2033 | [링크](https://www.globalresearch.kr/markets/advertising-market-imarc/) |
| 6 | Grand View Research, South Korea Digital Advertising | [링크](https://www.grandviewresearch.com/horizon/outlook/digital-advertising-market/south-korea) |
| 7 | 디플러스, 2025년 퍼포먼스 마케팅 혁신 | [링크](https://www.dplus.kr/2025-performance-marketing/) |
| 8 | koreatraffic.com, 2025 검색엔진 시장 점유율 | [링크](https://www.koreatraffic.com/kr/news/search-engine-market-share-korea-2025) |
| 9 | 적정마케팅연구소, 4대 광고 플랫폼 업데이트 | [링크](https://segama.co.kr/blog/25149/) |
| 10 | 디지털마케팅연구회, 2026년 AI 마케팅 7대 키워드 | [링크](https://www.madtimes.co.kr/news/articleView.html?idxno=25860) |
| 11 | 브랜드브리프, 아드리엘 SaaS 전략 | [링크](https://www.brandbrief.co.kr/news/articleView.html?idxno=6726) |
| 12 | Kakao Developers, 카카오모먼트 API | [링크](https://developers.kakao.com/docs/latest/ko/kakaomoment/reference) |
| 13 | Google Ads API Documentation | [링크](https://developers.google.com/google-ads/api/docs/get-started/introduction) |
| 14 | 네이버 검색광고 API 문서 (GitHub) | [링크](https://github.com/naver/searchad-apidoc) |
| 15 | 유니콘팩토리, 2024 스타트업 창업 통계 | [링크](https://www.unicornfactory.co.kr/article/2025022717011043195) |
| 16 | 중소벤처기업부, 창업기업실태조사 | [링크](https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=1057029&parentSeq=1057029) |

---

*본 사업계획서는 biz-planner (기획부)에서 작성하였으며, 오너의 검토 및 승인 후 team-builder (HR)를 통해 팀 빌드를 진행합니다.*
