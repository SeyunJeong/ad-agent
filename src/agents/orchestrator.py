"""Agent orchestrator — TEAM_LEAD that routes to sub-agents.

Uses Anthropic API to run AI agents for the 8-phase content pipeline:
- Phase 0: Deep research (market/competitor/target)
- Phase 1: Campaign strategy (with self-debate)
- Phase 2: Concept/ideation (creative concepts)
- Phase 3: Production (copywriting + keyword research)
- Phase 4: Fact check (mandatory gate)
- Phase 5: QA scoring (50-point quality gate)
- Phase 6: Channel setup + bid optimization
- Phase 7: Analysis + feedback loop
"""

import json
import time
from typing import Any, Optional

import anthropic
import structlog

from src.config.settings import Settings
from src.models.campaign import CampaignBrief
from src.storage.repositories import AgentLogRepository

logger = structlog.get_logger()


class AgentOrchestrator:
    """TEAM_LEAD — 캠페인 워크플로우 오케스트레이터.

    각 단계별 에이전트를 호출하고 결과를 조합.
    """

    def __init__(
        self,
        settings: Settings,
        log_repo: Optional[AgentLogRepository] = None,
    ) -> None:
        self._settings = settings
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.ai_model
        self._log_repo = log_repo

    async def _call_agent(
        self,
        agent_name: str,
        system_prompt: str,
        user_message: str,
        campaign_id: Optional[str] = None,
    ) -> str:
        """단일 에이전트 호출."""
        start = time.time()
        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        duration_ms = int((time.time() - start) * 1000)
        result = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens

        logger.info(
            "agent_called",
            agent=agent_name,
            tokens=tokens,
            duration_ms=duration_ms,
        )

        if self._log_repo:
            await self._log_repo.log(
                agent_name=agent_name,
                action="generate",
                campaign_id=campaign_id,
                input_data={"system": system_prompt[:200], "user": user_message[:500]},
                output_data={"result": result[:1000]},
                tokens_used=tokens,
                duration_ms=duration_ms,
            )

        return result

    # === Phase 0: 심층 리서치 (DEEP_RESEARCHER) ===

    async def deep_research(
        self, brief: CampaignBrief, campaign_id: Optional[str] = None
    ) -> str:
        """Phase 0 — 시장/경쟁사/타겟/채널 심층 리서치."""
        return await self._call_agent(
            agent_name="deep_researcher",
            system_prompt=DEEP_RESEARCHER_PROMPT,
            user_message=(
                f"캠페인 브리프:\n{brief.model_dump_json(indent=2)}\n\n"
                "심층 리서치를 수행해줘. 시장 규모, 경쟁사 분석, 타겟 인사이트, "
                "채널 트렌드, 벤치마크 데이터를 포함해줘."
            ),
            campaign_id=campaign_id,
        )

    # === Phase 1: 전략 수립 (Self-Debate) ===

    async def generate_strategy(
        self,
        brief: CampaignBrief,
        research_data: Optional[str] = None,
        campaign_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """전략 수립 — Blue Team → Red Team → Defense → Final."""

        brief_text = brief.model_dump_json(indent=2)
        research_context = (
            f"\n\n리서치 데이터:\n{research_data}" if research_data else ""
        )

        # Step 1: Blue Team — 초안 전략
        blue_result = await self._call_agent(
            agent_name="strategist_blue",
            system_prompt=STRATEGIST_BLUE_PROMPT,
            user_message=(
                f"다음 캠페인 브리프에 대한 전략을 수립해줘:\n\n{brief_text}"
                f"{research_context}"
            ),
            campaign_id=campaign_id,
        )

        # Step 2: Red Team — 비판 및 약점 분석
        red_result = await self._call_agent(
            agent_name="strategist_red",
            system_prompt=STRATEGIST_RED_PROMPT,
            user_message=f"다음 전략의 약점을 분석해줘:\n\n브리프:\n{brief_text}\n\n전략:\n{blue_result}",
            campaign_id=campaign_id,
        )

        # Step 3: Defense — 반박 및 보완
        defense_result = await self._call_agent(
            agent_name="strategist_defense",
            system_prompt=STRATEGIST_DEFENSE_PROMPT,
            user_message=(
                f"Blue Team 전략:\n{blue_result}\n\n"
                f"Red Team 비판:\n{red_result}\n\n"
                "비판을 반영하여 최종 전략을 완성해줘."
            ),
            campaign_id=campaign_id,
        )

        return {
            "strategy": defense_result,
            "blue_team": blue_result,
            "red_team": red_result,
            "process": "self_debate",
        }

    # === Phase 2: 컨셉 기획 (CONCEPT_PLANNER) ===

    async def generate_concept(
        self,
        brief: CampaignBrief,
        strategy: str,
        research_data: Optional[str] = None,
        campaign_id: Optional[str] = None,
    ) -> str:
        """Phase 2 — 전략 USP를 크리에이티브 컨셉 2-3안으로 변환."""
        return await self._call_agent(
            agent_name="concept_planner",
            system_prompt=CONCEPT_PLANNER_PROMPT,
            user_message=(
                f"캠페인 브리프:\n{brief.model_dump_json(indent=2)}\n\n"
                f"전략 (Self-Debate 결과):\n{strategy}\n\n"
                + (f"리서치 데이터:\n{research_data}\n\n" if research_data else "")
                + "크리에이티브 컨셉 2-3안을 기획해줘. "
                "Safe/Bold/Wild Card 유형으로, 채널별 변주와 A/B 테스트 설계를 포함해줘."
            ),
            campaign_id=campaign_id,
        )

    # === Phase 3-1: 키워드 리서치 ===

    async def research_keywords(
        self,
        brief: CampaignBrief,
        channels: list[str],
        campaign_id: Optional[str] = None,
    ) -> str:
        return await self._call_agent(
            agent_name="researcher",
            system_prompt=RESEARCHER_PROMPT,
            user_message=(
                f"캠페인 브리프:\n{brief.model_dump_json(indent=2)}\n\n"
                f"채널: {', '.join(channels)}\n\n"
                "키워드 리서치를 수행해줘. 채널별 추천 키워드, 검색량 예측, "
                "타겟 오디언스 분석을 포함해줘."
            ),
            campaign_id=campaign_id,
        )

    # === 크리에이티브 생성 ===

    async def generate_creatives(
        self,
        brief: CampaignBrief,
        channels: list[str],
        strategy: str,
        campaign_id: Optional[str] = None,
    ) -> str:
        return await self._call_agent(
            agent_name="creative",
            system_prompt=CREATIVE_PROMPT,
            user_message=(
                f"캠페인 브리프:\n{brief.model_dump_json(indent=2)}\n\n"
                f"전략:\n{strategy}\n\n"
                f"채널: {', '.join(channels)}\n\n"
                "각 채널별 광고 카피를 생성해줘. 제목, 설명, CTA를 포함하고 "
                "채널별 글자수 제한을 지켜줘.\n"
                "JSON 배열로 출력해줘: "
                '[{"channel": "...", "headline": "...", "description": "...", "cta": "..."}]'
            ),
            campaign_id=campaign_id,
        )

    # === Phase 4: 팩트체크 (AD_FACT_CHECKER) — 필수 게이트 ===

    async def fact_check(
        self,
        creatives: str,
        strategy: str,
        campaign_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Phase 4 — 광고 카피 사실 검증. 필수 게이트."""
        result = await self._call_agent(
            agent_name="fact_checker",
            system_prompt=FACT_CHECKER_PROMPT,
            user_message=(
                f"전략 맥락:\n{strategy[:1000]}\n\n"
                f"검증 대상 크리에이티브:\n{creatives}\n\n"
                "모든 수치, 주장, 비교 표현을 사실 검증해줘. "
                "PASS/CONDITIONAL_PASS/FAIL 판정과 Data Accuracy 스코어를 포함해줘."
            ),
            campaign_id=campaign_id,
        )
        return {"report": result, "agent": "AD_FACT_CHECKER"}

    # === Phase 5: QA 스코어링 (QA_SCORER) ===

    async def score_quality(
        self,
        creatives: str,
        strategy: str,
        fact_check_report: str,
        concept: str,
        campaign_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Phase 5 — 50점 만점 품질 스코어링."""
        result = await self._call_agent(
            agent_name="qa_scorer",
            system_prompt=QA_SCORER_PROMPT,
            user_message=(
                f"전략:\n{strategy[:1000]}\n\n"
                f"컨셉:\n{concept[:1000]}\n\n"
                f"크리에이티브:\n{creatives}\n\n"
                f"팩트체크 리포트:\n{fact_check_report}\n\n"
                "5개 지표(Strategy Alignment, Data Accuracy, Creative Impact, "
                "Channel Optimization, Legal Compliance)를 각 10점씩 채점하고 "
                "총점 50점 기준으로 PASS(≥35)/REVISE(≥30)/REJECT(<30) 판정해줘."
            ),
            campaign_id=campaign_id,
        )
        return {"scorecard": result, "agent": "QA_SCORER"}

    # === Phase 6: 입찰/예산 최적화 ===

    async def optimize_bids(
        self,
        campaign_id: str,
        performance_data: dict,
        current_config: dict,
    ) -> str:
        return await self._call_agent(
            agent_name="bid_optimizer",
            system_prompt=BID_OPTIMIZER_PROMPT,
            user_message=(
                f"캠페인 ID: {campaign_id}\n"
                f"현재 성과:\n{json.dumps(performance_data, ensure_ascii=False, indent=2)}\n\n"
                f"현재 설정:\n{json.dumps(current_config, ensure_ascii=False, indent=2)}\n\n"
                "입찰가와 예산 최적화 제안을 해줘."
            ),
            campaign_id=campaign_id,
        )

    # === 성과 분석 ===

    async def analyze_performance(
        self,
        campaign_id: str,
        performance_data: dict,
        report_type: str = "weekly",
    ) -> str:
        return await self._call_agent(
            agent_name="analyst",
            system_prompt=ANALYST_PROMPT,
            user_message=(
                f"캠페인 ID: {campaign_id}\n"
                f"리포트 유형: {report_type}\n"
                f"성과 데이터:\n{json.dumps(performance_data, ensure_ascii=False, indent=2)}\n\n"
                "성과 분석 리포트를 작성해줘. 핵심 인사이트와 개선 제안을 포함해."
            ),
            campaign_id=campaign_id,
        )

    # === Full 8-Phase Campaign Creation Pipeline ===

    async def create_campaign_plan(
        self, brief: CampaignBrief, campaign_id: Optional[str] = None
    ) -> dict[str, Any]:
        """8단계 콘텐츠 파이프라인 전체 실행.

        Phase 0: Deep Research (DEEP_RESEARCHER)
        Phase 1: Strategy - Self-Debate (CAMPAIGN_STRATEGIST)
        Phase 2: Concept/Ideation (CONCEPT_PLANNER)
        Phase 3: Production (COPYWRITER + KEYWORD_TEAM)
        Phase 4: Fact Check — 필수 게이트 (AD_FACT_CHECKER)
        Phase 5: QA Scoring (QA_SCORER)
        Phase 6: Channel Setup + Bid/Budget
        """
        channels = brief.channels or ["naver", "meta", "google", "kakao"]

        # Phase 0: Deep Research
        logger.info("pipeline_phase", phase="0_deep_research", campaign_id=campaign_id)
        research_result = await self.deep_research(brief, campaign_id)

        # Phase 1: Strategy (Self-Debate with research data)
        logger.info("pipeline_phase", phase="1_strategy", campaign_id=campaign_id)
        strategy_result = await self.generate_strategy(
            brief, research_data=research_result, campaign_id=campaign_id
        )

        # Phase 2: Concept/Ideation
        logger.info("pipeline_phase", phase="2_concept", campaign_id=campaign_id)
        concept_result = await self.generate_concept(
            brief,
            strategy_result["strategy"],
            research_data=research_result,
            campaign_id=campaign_id,
        )

        # Phase 3: Production (keywords + creatives)
        logger.info("pipeline_phase", phase="3_production", campaign_id=campaign_id)
        keyword_result = await self.research_keywords(brief, channels, campaign_id)
        creative_result = await self.generate_creatives(
            brief, channels, strategy_result["strategy"], campaign_id
        )

        # Phase 4: Fact Check (mandatory gate)
        logger.info("pipeline_phase", phase="4_fact_check", campaign_id=campaign_id)
        fact_check_result = await self.fact_check(
            creative_result, strategy_result["strategy"], campaign_id
        )

        # Phase 5: QA Scoring
        logger.info("pipeline_phase", phase="5_qa_scoring", campaign_id=campaign_id)
        qa_result = await self.score_quality(
            creative_result,
            strategy_result["strategy"],
            fact_check_result["report"],
            concept_result,
            campaign_id,
        )

        # Phase 6: Bid/Budget
        logger.info("pipeline_phase", phase="6_bid_budget", campaign_id=campaign_id)
        bid_result = await self._call_agent(
            agent_name="bid_optimizer",
            system_prompt=BID_OPTIMIZER_PROMPT,
            user_message=(
                f"캠페인 브리프:\n{brief.model_dump_json(indent=2)}\n\n"
                f"전략:\n{strategy_result['strategy']}\n\n"
                f"채널: {', '.join(channels)}\n\n"
                "채널별 예산 배분과 입찰 전략을 수립해줘. "
                "JSON으로 출력: "
                '[{"channel": "...", "budget_ratio": N, "bid_strategy": "...", "expected_cpi": N}]'
            ),
            campaign_id=campaign_id,
        )

        return {
            "research": research_result,
            "strategy": strategy_result,
            "concept": concept_result,
            "keywords": keyword_result,
            "creatives": creative_result,
            "fact_check": fact_check_result,
            "qa_score": qa_result,
            "bid_budget": bid_result,
            "channels": channels,
            "pipeline": "8_phase_content_pipeline",
        }


# ====== Agent System Prompts ======

STRATEGIST_BLUE_PROMPT = """너는 한국 퍼포먼스 마케팅 전문 전략가야. (Blue Team)

역할: 캠페인 브리프를 분석하고 최적의 전략을 수립한다.

출력 형식:
1. 전략 요약 (3-5줄)
2. 채널 믹스 추천 (채널별 비중, 근거)
3. 핵심 타겟팅 전략
4. 예상 KPI 및 달성 경로
5. 리스크 및 대응 방안

한국 시장 특성을 고려해:
- 네이버 검색광고: 한국 검색 시장 60-70% 점유. 의도 기반 키워드 타겟팅
- 카카오: 2030 여성 강세. 카카오톡 채널 연계
- 메타: 관심사 기반 타겟팅, 리타겟팅 강력
- 구글: 앱 설치 캠페인 우수, YouTube 포함

반드시 구체적인 숫자와 근거를 제시해."""

STRATEGIST_RED_PROMPT = """너는 광고 전략 비평가야. (Red Team)

역할: 제시된 전략의 약점, 리스크, 비현실적 가정을 찾아서 비판한다.

체크리스트:
1. KPI 목표가 예산 대비 현실적인가?
2. 채널 배분의 근거가 충분한가?
3. 타겟팅이 너무 넓거나 좁지 않은가?
4. 경쟁사 대비 차별점이 있는가?
5. 시즌/타이밍 요소를 고려했는가?
6. 학습 기간(러닝 타임)을 반영했는가?
7. 측정/추적 방안이 구체적인가?
8. 최악의 시나리오에 대한 대비가 있는가?

약점당 구체적인 개선 방향을 함께 제시해."""

STRATEGIST_DEFENSE_PROMPT = """너는 캠페인 전략 최종 정리자야.

Blue Team의 초안 전략과 Red Team의 비판을 모두 검토하고,
비판이 타당한 부분은 수정하고, 과도한 비판은 근거를 들어 방어하여
최종 전략을 완성해.

출력 형식 (JSON):
{
  "strategy_summary": "전략 요약",
  "channel_mix": [
    {"channel": "naver", "ratio": 30, "reason": "..."},
    {"channel": "meta", "ratio": 35, "reason": "..."},
    ...
  ],
  "targeting": {"primary": "...", "secondary": "..."},
  "kpi_targets": {"primary": "CPI 3000원", "secondary": "..."},
  "timeline": [{"phase": "...", "days": "...", "action": "..."}],
  "risks": [{"risk": "...", "mitigation": "..."}],
  "red_team_responses": [{"criticism": "...", "response": "accepted/defended", "action": "..."}]
}"""

RESEARCHER_PROMPT = """너는 한국 디지털 광고 키워드/오디언스 리서처야.

역할: 캠페인 브리프를 분석하고 채널별 키워드 및 오디언스 전략을 수립한다.

출력:
1. 핵심 키워드 (채널별 20-30개)
   - 키워드, 예상 검색량, 예상 CPC, 경쟁도, 매치 타입
2. 롱테일 키워드 (10-20개)
3. 네거티브 키워드 (5-10개)
4. 오디언스 세그먼트 (메타/카카오용)
   - 관심사, 행동, 맞춤 타겟 제안
5. 경쟁사 분석 (키워드 겹침, 차별화 포인트)

한국 시장 특성:
- 네이버: 검색량은 네이버 키워드 도구 기준
- 구글: 글로벌 검색 + 한국 로컬
- 메타/카카오: 관심사 + 행동 타겟팅"""

CREATIVE_PROMPT = """너는 한국 퍼포먼스 마케팅 광고 카피라이터야.

역할: 채널별 광고 소재(카피)를 생성한다.

채널별 규격:
- 네이버 파워링크: 제목 15자, 설명 45자
- 카카오: 제목 25자, 설명 45자
- 메타: 제목 25자, 설명 125자
- 구글 RSA: 제목 30자 x 최소 3개, 설명 90자 x 최소 2개

원칙:
1. USP(고유 가치 제안)를 명확히
2. CTA(행동 유도)를 포함
3. 한국어 자연스럽게 (번역체 금지)
4. 숫자/구체적 혜택 우선
5. 경쟁사와 차별화

각 채널별 최소 3개 변형(A/B/C)을 생성해."""

BID_OPTIMIZER_PROMPT = """너는 퍼포먼스 마케팅 입찰/예산 최적화 전문가야.

역할: 채널별 예산 배분과 입찰 전략을 수립한다.

고려 사항:
1. 채널별 평균 CPC/CPI (한국 시장 2024-2026 기준)
   - 네이버 검색광고: CPC 200-1500원 (업종별 상이)
   - 카카오 모먼트: CPC 100-500원
   - 메타: CPC 200-800원, CPM 3000-15000원
   - 구글: CPC 150-1000원, CPI 2000-5000원
2. 학습 기간 (최소 7일, 50회 이상 전환)
3. 일예산 = 목표 CPA x 예상 일전환수 x 1.5 (여유분)
4. 초기: 균등 배분 → 3-5일 후 성과 기반 재배분

출력: 채널별 구체적인 예산 금액, 입찰 전략, 예상 성과."""

DEEP_RESEARCHER_PROMPT = """너는 한국 시장 전문 심층 리서치 에이전트야. (DEEP_RESEARCHER)

역할: 캠페인 시작 전 시장, 경쟁사, 타겟, 채널을 심층 리서치하여 전략 수립의 데이터 기반을 제공한다.

출력 형식:
1. Executive Summary (핵심 발견 3-5개)
2. 시장 개요 (시장 규모 TAM/SAM/SOM, 성장률, 트렌드)
3. 경쟁사 분석 (직접 3-5개: 채널/USP/추정 광고비/강점/약점)
4. 타겟 인사이트 (페르소나, 디지털 행동, 구매 여정, 페인 포인트)
5. 채널별 인사이트 (최신 동향, 기회, 리스크)
6. 벤치마크 데이터 (업종별 CTR/CPC/CVR/CPA by 채널)
7. 전략 제언 (Must-Do / Should-Do / Watch-Out)

한국 시장 특성:
- 네이버: 검색 60-70% 점유, 쇼핑 검색 강력
- 카카오: 47M MAU, 메시지 광고 고효율
- 메타: 인스타그램 18M, 비주얼/리타겟팅 강점
- 구글: 검색 30-35%, YouTube/앱 설치 강점

모든 데이터에 출처를 명시하고, A/B급 출처를 70% 이상 사용해."""

CONCEPT_PLANNER_PROMPT = """너는 크리에이티브 컨셉 기획 전문가야. (CONCEPT_PLANNER)

역할: 캠페인 전략의 USP를 구체적인 크리에이티브 컨셉 2-3안으로 변환한다.

각 컨셉에 포함할 요소:
1. 컨셉명 + 유형 (Safe/Bold/Wild Card)
2. 핵심 아이디어 (한 줄)
3. 감정적 트리거 (공포/호기심/사회적증명/긴급성/자아표현/편의/소속감)
4. 타겟 공감 구조: 페인 포인트 → 해결 제안 → 증거 → CTA
5. 채널별 변주 (네이버/카카오/메타/구글)
6. A/B 테스트 포인트 + 가설
7. Production 팀 지시사항 (COPYWRITER/VISUAL_DIRECTOR)

컨셉 유형 가이드:
- 컨셉 1 (Safe): 검증된 접근, 업종 관례 따름
- 컨셉 2 (Bold): 차별화된 접근, 경쟁사와 다른 앵글
- 컨셉 3 (Wild Card): 파격적 접근, 높은 바이럴 잠재력

모든 컨셉에 전략 USP가 반드시 반영되어야 한다.
추천 컨셉과 이유를 명시해."""

FACT_CHECKER_PROMPT = """너는 광고 팩트 체커야. (AD_FACT_CHECKER) ██ 필수 게이트 ██

역할: 광고 크리에이티브의 모든 수치, 주장, 비교 표현을 사실 검증한다.
이 검증을 통과하지 않으면 광고를 집행할 수 없다.

검증 대상 (자동 플래그):
- 수치: "30% 절감", "100만 명 사용" 등
- 최상급: "1위", "최고", "유일", "최초" 등
- 효능/효과: "확실한 효과", "즉각적 개선" 등
- 비교: "A보다 좋은", "업계 최저가" 등
- 할인/가격, 인증/수상, 후기/추천, 통계

각 항목 판정:
- VERIFIED: 신뢰 출처로 확인됨
- UNVERIFIED: 확인 불가, 출처 없음 → 표현 수정 필요
- FALSE: 사실과 다름, 과장/왜곡 → 즉시 삭제/수정

법규 체크:
- 표시광고법 (허위/기만/부당비교/비방)
- 업종별 규제 (금융/건강/식품/화장품/교육)
- 채널별 광고정책 (네이버/카카오/메타/구글)

출력:
1. 종합 판정: PASS / CONDITIONAL_PASS / FAIL
2. Data Accuracy 스코어: {n}/10
3. 검증 항목별 상세 (원문, 유형, 판정, 출처, 수정 제안)
4. 법규 검증 결과
5. FAIL 시 수정 필요 항목 목록

FALSE 항목 1개라도 발견되면 반드시 FAIL 판정해."""

QA_SCORER_PROMPT = """너는 광고 품질 스코어러야. (QA_SCORER)

역할: 광고 크리에이티브의 총체적 품질을 50점 만점으로 정량 평가한다.

5개 평가 지표 (각 10점):

1. Strategy Alignment (전략 정합성):
   - 전략 USP가 크리에이티브에 반영되었는가?
   - Red Team 지적 사항이 보완되었는가?
   - 채널별 메시지 일관성

2. Data Accuracy (데이터 정확성):
   - AD_FACT_CHECKER 리포트 결과를 반영
   - 모든 수치/주장 검증 여부

3. Creative Impact (크리에이티브 임팩트):
   - 3초 내 핵심 메시지 전달
   - 감정적 훅 작동 여부
   - CTA 명확성 + 행동 유도

4. Channel Optimization (채널 최적화):
   - 네이버 파워링크 15/45자, 카카오 25/45자, 메타 25/125자, 구글 RSA 30×3/90×2
   - 채널 네이티브 톤 반영
   - 플랫폼 행동 패턴 반영

5. Legal Compliance (법적 준수):
   - CREATIVE_REVIEWER 관점에서 평가
   - 표시광고법/업종규제/채널정책

판정 기준:
- PASS: 총점 ≥ 35 AND 모든 개별 ≥ 5
- REVISE: 총점 ≥ 30 OR 개별 하나라도 < 5 → Phase 3 리턴
- REJECT: 총점 < 30 OR 개별 하나라도 < 3 → Phase 2 리턴

출력: QA Score Card 형식으로 5개 지표 점수 + 총점 + 판정 + 상세 피드백.
REVISE/REJECT 시 구체적인 수정 지시를 포함해."""

ANALYST_PROMPT = """너는 퍼포먼스 마케팅 데이터 분석가야.

역할: 캠페인 성과 데이터를 분석하고 인사이트를 도출한다.

분석 프레임워크:
1. Executive Summary (3줄 핵심 요약)
2. KPI 달성률 (목표 vs 실적)
3. 채널별 성과 비교
4. Top/Bottom 키워드/소재 분석
5. 이상 감지 (갑작스런 변화)
6. 최적화 제안 (우선순위별)

인사이트 도출 시:
- WHY에 집중 (왜 이 수치인가)
- SO WHAT 제시 (그래서 뭘 해야 하는가)
- 구체적인 액션 아이템으로 마무리"""
