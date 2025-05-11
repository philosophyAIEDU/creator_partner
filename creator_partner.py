# 필요한 라이브러리 임포트
import streamlit as st
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
from datetime import datetime

# ============================================================================
# 에이전틱 워크플로우 기반 창작 파트너 시스템
# 3명의 특화된 창작 전문가가 팀을 이루어 사용자를 지원
# ============================================================================

class CreativeTeam:
    """
    AI 기반 창작 파트너 팀을 관리하는 클래스
    각 전문가의 협업을 조율하고 최종 결과를 제공
    """
    
    def __init__(self, api_key):
        """
        창작 파트너 팀 초기화
        Args:
            api_key (str): Google AI API 키
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = GenerativeModel('gemini-2.5-pro-preview-05-06')
        
        # 3명의 특화된 창작 전문가 초기화
        self.content_strategist = ContentStrategist(self.model)  # 콘텐츠 전략 및 기획 전문가
        self.creative_writer = CreativeWriter(self.model)      # 창작 및 스토리텔링 전문가
        self.platform_specialist = PlatformSpecialist(self.model)  # 플랫폼 최적화 및 유통 전문가
        
        # 워크플로우 로그 초기화
        self.workflow_logs = []
    
    def get_creative_advice(self, service_type, input_data):
        """
        사용자 요청에 따라 3명의 전문가가 순차적으로 협업하여 창작 지원 제공
        Args:
            service_type (str): 요청 서비스 유형 (YouTube, 블로그, 인스타그램)
            input_data (dict): 사용자 입력 데이터
        Returns:
            dict: 각 전문가의 조언을 포함한 최종 결과
        """
        # 워크플로우 기록 시작
        workflow_log = {
            "service_type": service_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "experts_involved": ["ContentStrategist", "CreativeWriter", "PlatformSpecialist"],
            "steps": []
        }
        
        # 1단계: 콘텐츠 전략가의 초기 분석 및 기획
        st.markdown("### 1단계: 콘텐츠 전략 및 기획 중...")
        with st.spinner("콘텐츠 전략가가 기획을 수립 중입니다..."):
            initial_strategy = self.content_strategist.analyze(service_type, input_data)
            workflow_log["steps"].append({
                "expert": "ContentStrategist",
                "action": "initial_strategy"
            })
        
        # 2단계: 창작 작가의 콘텐츠 개발 및 스토리텔링
        st.markdown("### 2단계: 콘텐츠 개발 및 스토리텔링 중...")
        with st.spinner("창작 작가가 콘텐츠를 발전시키는 중입니다..."):
            content_enhanced = self.creative_writer.enhance(initial_strategy, service_type, input_data)
            workflow_log["steps"].append({
                "expert": "CreativeWriter",
                "action": "content_enhancement"
            })
        
        # 3단계: 플랫폼 전문가의 최적화 및 배포 전략
        st.markdown("### 3단계: 플랫폼 최적화 및 배포 전략 수립 중...")
        with st.spinner("플랫폼 전문가가 최종 조언을 준비 중입니다..."):
            final_advice = self.platform_specialist.finalize(content_enhanced, service_type, input_data)
            workflow_log["steps"].append({
                "expert": "PlatformSpecialist",
                "action": "finalization"
            })
        
        # 워크플로우 로그 저장
        self.workflow_logs.append(workflow_log)
        
        # 각 전문가별 결과를 모두 반환
        return {
            "strategy": initial_strategy,
            "content": content_enhanced,
            "platform": final_advice
        }


class ContentStrategist:
    """
    콘텐츠 전략 및 기획 전문가
    트렌드 분석, 타겟 오디언스 정의, 콘텐츠 방향성 설정 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "content_strategy"
        self.expert_name = "김지원 콘텐츠 전략가"
        self.expert_intro = """
        안녕하세요, 김지원 콘텐츠 전략가입니다. 
        저는 트렌드 분석, 타겟 오디언스 정의, 콘텐츠 방향성 설정을 전문으로 합니다.
        10년간의 디지털 콘텐츠 전략 경험을 바탕으로 여러분의 창작물이 목표 청중에게 효과적으로 도달할 수 있도록 지원하겠습니다.
        """
    
    def analyze(self, service_type, input_data):
        """
        사용자 요청에 대한 콘텐츠 전략 수립
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "YouTube":
            prompt = self._create_youtube_strategy_prompt(input_data)
        elif service_type == "블로그":
            prompt = self._create_blog_strategy_prompt(input_data)
        elif service_type == "인스타그램":
            prompt = self._create_instagram_strategy_prompt(input_data)
        elif service_type == "통합 콘텐츠":
            prompt = self._create_integrated_strategy_prompt(input_data)
        else:
            prompt = self._create_general_strategy_prompt(input_data, service_type)
        
        # 전문가 정보 추가
        prompt = f"""
        당신은 '{self.expert_name}'이라는 콘텐츠 전략 전문가입니다.
        {self.expert_intro}
        
        {prompt}
        
        분석 결과에 트렌드 분석, 타겟 오디언스 인사이트, 콘텐츠 차별화 전략을 반드시 포함해 주세요.
        전문적이면서도 실용적인 전략을 제시해 주세요.
        """
        
        # AI 모델을 통한 응답 생성
        response = self.model.generate_content(prompt)
        return response.text
    
    def _create_youtube_strategy_prompt(self, input_data):
        return f"""
        다음 YouTube 콘텐츠 아이디어에 대한 전략을 수립해주세요:
        
        주제/아이디어: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 시청자: {input_data.get('target_audience', '')}
        
        다음 항목을 포함하는 YouTube 콘텐츠 전략을 제공해주세요:
        1. 콘텐츠 시장성 및 트렌드 분석
        2. 타겟 시청자 세부 페르소나 및 니즈
        3. 유사 콘텐츠 분석 및 차별화 전략
        4. 핵심 메시지 및 가치 제안
        5. 시리즈/에피소드 구조 제안
        6. 시청자 참여 유도 전략
        """
    
    def _create_blog_strategy_prompt(self, input_data):
        return f"""
        다음 블로그 콘텐츠 아이디어에 대한 전략을 수립해주세요:
        
        주제/분야: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 독자: {input_data.get('target_audience', '')}
        
        다음 항목을 포함하는 블로그 콘텐츠 전략을 작성해주세요:
        1. 블로그 시장/니치 분석
        2. 타겟 독자 페르소나 및 관심사
        3. 주요 경쟁 블로그 분석 및 차별화 포인트
        4. 핵심 주제 클러스터 및 콘텐츠 필러
        5. 타임리스 vs. 시의성 콘텐츠 균형
        6. SEO 및 독자 유입 전략 방향
        """
    
    def _create_instagram_strategy_prompt(self, input_data):
        return f"""
        다음 인스타그램 콘텐츠 아이디어에 대한 전략을 수립해주세요:
        
        계정 주제/성격: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 팔로워: {input_data.get('target_audience', '')}
        
        다음 구조로 인스타그램 콘텐츠 전략을 제시해주세요:
        
        1. 인스타그램 트렌드 및 알고리즘 분석
           - 현재 인기 있는 콘텐츠 유형
           - 최신 인스타그램 알고리즘 고려사항
           - 참여율 높은 콘텐츠 패턴
        
        2. 비주얼 아이덴티티 및 브랜딩 전략
           - 색상 팔레트 및 시각적 일관성
           - 그리드/피드 구성 컨셉
           - 스토리와 릴스 활용 방향
        
        3. 콘텐츠 필러 및 주제 분류
           - 핵심 콘텐츠 카테고리
           - 정기 시리즈 아이디어
           - 참여 유도 콘텐츠 유형
        """
    
    def _create_integrated_strategy_prompt(self, input_data):
        return f"""
        다음 통합 콘텐츠 전략(YouTube, 블로그, 인스타그램)을 수립해주세요:
        
        주제/브랜드: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 오디언스: {input_data.get('target_audience', '')}
        주력 플랫폼: {input_data.get('primary_platform', '')}
        
        다음 구조로 통합 콘텐츠 전략을 제시해주세요:
        
        1. 크로스 플랫폼 브랜드 아이덴티티
           - 일관된 브랜드 메시지 및 톤
           - 플랫폼별 브랜딩 변형
           - 핵심 차별화 포인트
        
        2. 콘텐츠 생태계 설계
           - 플랫폼별 역할 정의
           - 콘텐츠 재활용 전략
           - 플랫폼 간 상호 연결 방법
        
        3. 통합 오디언스 여정 설계
           - 오디언스 유입 및 전환 경로
           - 각 플랫폼별 타겟 오디언스 세그먼트
           - 교차 홍보 전략
        """
    
    def _create_general_strategy_prompt(self, input_data, service_type):
        return f"""
        다음 {service_type} 콘텐츠 요청에 대한 전략을 수립해주세요:
        
        요청 내용: {str(input_data)}
        
        콘텐츠 시장 분석, 타겟 오디언스 정의, 차별화 전략, 핵심 콘텐츠 방향성을 포함한 종합적인 전략을 제공해주세요.
        """


class CreativeWriter:
    """
    창작 및 스토리텔링 전문가
    매력적인 콘텐츠 개발, 스토리 구조, 시각적 요소 기획 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "creative_writing"
        self.expert_name = "이민호 콘텐츠 작가"
        self.expert_intro = """
        안녕하세요, 이민호 콘텐츠 작가입니다.
        저는 매력적인 스토리텔링, 시각적/청각적 콘텐츠 기획, 창의적 표현을 전문으로 합니다.
        8년간의 디지털 콘텐츠 제작 경험을 통해 여러분의 메시지가 청중의 마음을 사로잡을 수 있도록 지원하겠습니다.
        """
    
    def enhance(self, previous_strategy, service_type, input_data):
        """
        전략가의 분석을 바탕으로 창의적 콘텐츠 개발
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "YouTube":
            prompt = self._create_youtube_creative_prompt(input_data)
        elif service_type == "블로그":
            prompt = self._create_blog_creative_prompt(input_data)
        elif service_type == "인스타그램":
            prompt = self._create_instagram_creative_prompt(input_data)
        elif service_type == "통합 콘텐츠":
            prompt = self._create_integrated_creative_prompt(input_data)
        else:
            prompt = self._create_general_creative_prompt(input_data, service_type)
        
        # 전문가 정보 추가
        prompt = f"""
        당신은 '{self.expert_name}'이라는 창작 콘텐츠 전문가입니다.
        {self.expert_intro}
        
        콘텐츠 전략가가 제공한 다음 분석을 검토하고, 창작 관점에서 보완해주세요:
        
        === 콘텐츠 전략가의 분석 ===
        {previous_strategy}
        === 분석 끝 ===
        
        {prompt}
        
        매력적인 스토리 구조, 시각적/청각적 요소, 감정적 연결 전략을 반드시 포함해 주세요.
        """
        
        # AI 모델을 통한 응답 생성
        response = self.model.generate_content(prompt)
        return response.text
    
    def _create_youtube_creative_prompt(self, input_data):
        return f"""
        YouTube 콘텐츠를 위한 창의적 개발 계획을 제안해주세요:
        
        1. 영상 구성 및 스토리보드 아이디어
           - 훅(시작 부분) 디자인
           - 스토리 구조 및 흐름
           - 핵심 시각적 장면 구성
        
        2. 스크립트 및 내레이션 가이드
           - 스크립트 톤과 스타일
           - 핵심 대사 및 표현
           - 청중 참여 기법
        
        3. 시각/청각적 요소 계획
           - 영상 스타일 및 편집 기법
           - 음악 및 사운드 디자인
           - 그래픽 및 애니메이션 요소
        
        4. 썸네일 및 타이틀 기획
           - 클릭을 유도하는 썸네일 컨셉
           - 매력적인 타이틀 구조
           - A/B 테스트 옵션
        
        주제/아이디어: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 시청자: {input_data.get('target_audience', '')}
        채널 스타일: {input_data.get('channel_style', '')}
        """
    
    def _create_blog_creative_prompt(self, input_data):
        return f"""
        블로그 콘텐츠를 위한 창의적 개발 계획을 제안해주세요:
        
        1. 글 구조 및 스토리텔링 전략
           - 주목을 끄는 인트로 접근법
           - 정보 흐름 및 논리 구조
           - 결론 및 행동 유도 전략
        
        2. 콘텐츠 포맷 및 시각적 요소
           - 섹션 구분 및 소제목 전략
           - 이미지/그래픽 활용 방안
           - 인포그래픽 및 시각 자료 아이디어
        
        3. 독자 참여 유도 기법
           - 공감 형성 및 스토리텔링 기법
           - 질문 및 상호작용 요소
           - 공유하고 싶은 인사이트 설계
        
        4. 제목 및 메타 콘텐츠 기획
           - 클릭을 유도하는 헤드라인 구조
           - 서브헤딩 및 메타 설명
           - 내부/외부 링크 전략
        
        주제/분야: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 독자: {input_data.get('target_audience', '')}
        블로그 스타일: {input_data.get('blog_style', '')}
        """
    
    def _create_instagram_creative_prompt(self, input_data):
        return f"""
        인스타그램 콘텐츠를 위한 창의적 개발 계획을 제안해주세요:
        
        1. 피드 포스트 창작 전략
           - 시선을 사로잡는 비주얼 컨셉
           - 캡션 스토리텔링 접근법
           - 감정 연결 및 공감 요소
        
        2. 스토리 및 릴스 컨텐츠 아이디어
           - 릴스 포맷 및 구성 아이디어
           - 스토리 시퀀스 및 상호작용 요소
           - 오디오/음악 활용 전략
        
        3. 비주얼 디자인 가이드
           - 이미지 스타일 및 편집 접근법
           - 색상 및 시각적 요소 활용
           - 텍스트 오버레이 및 그래픽 요소
        
        4. 참여 촉진 콘텐츠 아이디어
           - 질문 및 토론 유도 방식
           - 해시태그 및 커뮤니티 참여 전략
           - 공유 가능성 높은 콘텐츠 유형
        
        계정 주제/성격: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 팔로워: {input_data.get('target_audience', '')}
        시각적 스타일: {input_data.get('visual_style', '')}
        """
    
    def _create_integrated_creative_prompt(self, input_data):
        return f"""
        통합 콘텐츠(YouTube, 블로그, 인스타그램)를 위한 창의적 개발 계획을 제안해주세요:
        
        1. 핵심 스토리/메시지 개발
           - 플랫폼 전반의 일관된 스토리 라인
           - 플랫폼별 변형 접근법
           - 핵심 메시지 및 테마 요소
        
        2. 플랫폼별 창의적 변형 전략
           - 콘텐츠 재구성 및 리퍼포징 방법
           - 플랫폼별 강점 활용 접근법
           - 시각적/텍스트적 변환 가이드
        
        3. 크로스 플랫폼 시각적 아이덴티티
           - 일관된 비주얼 요소 및 브랜딩
           - 플랫폼별 시각적 변형 방법
           - 통합 디자인 에셋 아이디어
        
        4. 콘텐츠 시리즈 및 캠페인 구조
           - 플랫폼 간 상호 보완적 시리즈
           - 시간차 발행 및 연결 전략
           - 통합 스토리텔링 접근법
        
        주제/브랜드: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 오디언스: {input_data.get('target_audience', '')}
        주력 플랫폼: {input_data.get('primary_platform', '')}
        브랜드 스타일: {input_data.get('brand_style', '')}
        """
    
    def _create_general_creative_prompt(self, input_data, service_type):
        return f"""
        다음 {service_type} 콘텐츠 요청에 대한 창의적 개발 계획을 제안해주세요:
        
        요청 내용: {str(input_data)}
        
        매력적인 스토리텔링 구조, 시각적/청각적 요소, 감정적 연결 전략, 참여 유도 방법을 구체적으로 제시해주세요.
        """


class PlatformSpecialist:
    """
    플랫폼 최적화 및 유통 전문가
    플랫폼별 최적화, 성과 측정, 배포 전략 담당
    """
    
    def __init__(self, model):
        self.model = model
        self.expertise = "platform_optimization"
        self.expert_name = "박서연 플랫폼 전문가"
        self.expert_intro = """
        안녕하세요, 박서연 플랫폼 전문가입니다.
        저는 다양한 디지털 플랫폼의 최적화, 알고리즘 이해, 콘텐츠 배포 전략을 전문으로 합니다.
        9년간의 디지털 마케팅 및 콘텐츠 최적화 경험을 통해 여러분의 콘텐츠가 목표 청중에게 효과적으로 도달할 수 있도록 지원하겠습니다.
        """
    
    def finalize(self, previous_content, service_type, input_data):
        """
        전략가와 창작가의 분석을 바탕으로 최종 플랫폼 최적화 및 유통 전략 제공
        """
        # 서비스 유형별 맞춤 프롬프트 생성
        if service_type == "YouTube":
            prompt = self._create_youtube_platform_prompt(input_data)
        elif service_type == "블로그":
            prompt = self._create_blog_platform_prompt(input_data)
        elif service_type == "인스타그램":
            prompt = self._create_instagram_platform_prompt(input_data)
        elif service_type == "통합 콘텐츠":
            prompt = self._create_integrated_platform_prompt(input_data)
        else:
            prompt = self._create_general_platform_prompt(input_data, service_type)
        
        # 전문가 정보 추가
        prompt = f"""
        당신은 '{self.expert_name}'이라는 플랫폼 최적화 전문가입니다.
        {self.expert_intro}
        
        콘텐츠 전략가와 창작 작가가 제공한, 다음 분석을 검토하고 최종적으로 완성해주세요:
        
        === 이전 전문가들의 분석 ===
        {previous_content}
        === 분석 끝 ===
        
        {prompt}
        
        최종 조언에는 다음 세 전문가의 관점이 균형있게 통합되어야 합니다:
        1. 콘텐츠 전략가 (전략 및 방향성)
        2. 창작 작가 (스토리텔링 및 창의적 요소)
        3. 플랫폼 전문가 (최적화 및 유통 전략)
        
        구체적이고 실행 가능한 단계별 콘텐츠 제작 및 배포 가이드를 제공해주세요.
        """
        
        # AI 모델을 통한 응답 생성
        response = self.model.generate_content(prompt)
        return response.text
    
    def _create_youtube_platform_prompt(self, input_data):
        return f"""
        YouTube 콘텐츠를 위한 플랫폼 최적화 및 유통 전략을 제안해주세요:
        
        1. YouTube 알고리즘 최적화 전략
           - 타이틀, 설명, 태그 최적화
           - 시청 지속성 및 참여율 향상 방법
           - 추천 알고리즘 활용 전략
        
        2. 발행 및 프로모션 계획
           - 최적 업로드 타이밍 및 주기
           - 초기 참여 유도 전략
           - 크로스 프로모션 방법
        
        3. 데이터 기반 개선 방법론
           - 핵심 성과 지표(KPI) 설정
           - 분석 모니터링 및 인사이트 발굴
           - A/B 테스트 접근법
        
        4. 커뮤니티 구축 및 확장 전략
           - 댓글 관리 및 시청자 참여 전략
           - 구독자 확보 및 유지 방법
           - 콘텐츠 생태계 확장 방안
        
        주제/아이디어: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 시청자: {input_data.get('target_audience', '')}
        채널 규모: {input_data.get('channel_size', '신규/소규모')}
        """
    
    def _create_blog_platform_prompt(self, input_data):
        return f"""
        블로그 콘텐츠를 위한 플랫폼 최적화 및 유통 전략을 제안해주세요:
        
        1. SEO 최적화 전략
           - 키워드 리서치 및 활용 방법
           - 온페이지 SEO 요소 최적화
           - 내/외부 링크 전략
        
        2. 콘텐츠 발행 및 유통 계획
           - 최적 발행 타이밍 및 주기
           - 소셜 미디어 공유 전략
           - 이메일 마케팅 및 뉴스레터 활용
        
        3. 데이터 분석 및 성과 최적화
           - 트래픽 및 참여 지표 모니터링
           - 전환율 최적화 방법
           - 콘텐츠 업데이트 및 리퍼포징 전략
        
        4. 독자 커뮤니티 구축 방안
           - 댓글 관리 및 독자 참여 전략
           - 충성 독자층 개발 방법
           - 협업 및 게스트 포스팅 활용
        
        주제/분야: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 독자: {input_data.get('target_audience', '')}
        블로그 플랫폼: {input_data.get('blog_platform', '')}
        """
    
    def _create_instagram_platform_prompt(self, input_data):
        return f"""
        인스타그램 콘텐츠를 위한 플랫폼 최적화 및 유통 전략을 제안해주세요:
        
        1. 인스타그램 알고리즘 최적화
           - 해시태그 전략 및 최적화
           - 캡션 및 호출 행동(CTA) 최적화
           - 탐색 페이지 노출 향상 방법
        
        2. 게시 및 참여 전략
           - 최적 포스팅 타이밍 및 빈도
           - 스토리, 릴스, 피드 통합 전략
           - 참여율 증대 전술
        
        3. 성장 및 영향력 확대 방법
           - 팔로워 확보 및 유지 전략
           - 협업 및 인플루언서 활용
           - 크로스 프로모션 기회
        
        4. 분석 및 최적화 프레임워크
           - 주요 성과 지표 모니터링
           - 인사이트 기반 콘텐츠 조정
           - 지속적 실험 및 최적화 접근법
        
        계정 주제/성격: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 팔로워: {input_data.get('target_audience', '')}
        계정 규모: {input_data.get('account_size', '신규/소규모')}
        """
    
    def _create_integrated_platform_prompt(self, input_data):
        return f"""
        통합 콘텐츠(YouTube, 블로그, 인스타그램)를 위한 플랫폼 최적화 및 유통 전략을 제안해주세요:
        
        1. 통합 콘텐츠 발행 전략
           - 플랫폼별 최적 발행 순서 및 타이밍
           - 크로스 플랫폼 프로모션 흐름
           - 콘텐츠 형식별 배포 계획
        
        2. 플랫폼 간 시너지 최대화
           - 트래픽 및 청중 이동 경로 최적화
           - 플랫폼별 강점 극대화 방법
           - 참여 및 전환 경로 설계
        
        3. 통합 데이터 분석 체계
           - 크로스 플랫폼 성과 측정 방법
           - 통합 KPI 설정 및 모니터링
           - 데이터 기반 리소스 배분 전략
        
        4. 장기 성장 및 확장 로드맵
           - 단계별 성장 목표 및 전략
           - 콘텐츠 에코시스템 확장 방법
           - 채널 간 상호 강화 메커니즘
        
        주제/브랜드: {input_data.get('topic', '')}
        목표/목적: {input_data.get('goals', '')}
        타겟 오디언스: {input_data.get('target_audience', '')}
        주력 플랫폼: {input_data.get('primary_platform', '')}
        현재 채널 상태: {input_data.get('current_status', '신규/소규모')}
        """
    
    def _create_general_platform_prompt(self, input_data, service_type):
        return f"""
        다음 {service_type} 콘텐츠 요청에 대한 플랫폼 최적화 및 유통 전략을 제안해주세요:
        
        요청 내용: {str(input_data)}
        
        플랫폼 최적화, 발행 및 유통 전략, 성과 측정 방법, 커뮤니티 구축 접근법을 구체적으로 제시해주세요.
        """


# ============================================================================
# Streamlit 웹 애플리케이션 구현
# ============================================================================

def main():
    """
    메인 함수: Streamlit 웹 애플리케이션의 메인 로직
    """
    # 페이지 기본 설정
    st.set_page_config(
        page_title="AI 창작 파트너 팀",
        page_icon="✨📱📝",
        layout="wide"
    )
    
    # 페이지 제목 및 설명
    st.title("✨ AI 창작 파트너 팀")
    st.markdown("""
    ### 3명의 전문가가 협업하여 맞춤형 콘텐츠 전략과 아이디어를 제공합니다
    
    * **김지원 콘텐츠 전략가**: 트렌드 분석과 콘텐츠 방향성 설정
    * **이민호 콘텐츠 작가**: 매력적인 스토리텔링과 창의적 콘텐츠 개발
    * **박서연 플랫폼 전문가**: 플랫폼별 최적화와 유통 전략
    """)
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🔑 API 설정")
        # API 키 입력 필드 (비밀번호 형식)
        api_key = st.text_input("Google API 키를 입력하세요", type="password")
        
        # API 키가 입력되지 않은 경우 경고 메시지 표시
        if not api_key:
            st.warning("API 키를 입력해주세요.")
            st.stop()
            
        st.markdown("---")
        
        # 전문가 소개
        st.markdown("### 🧠 전문가 소개")
        
        expert_tab = st.selectbox("전문가 정보 보기", 
                                ["김지원 콘텐츠 전략가", "이민호 콘텐츠 작가", "박서연 플랫폼 전문가"])
        
        if expert_tab == "김지원 콘텐츠 전략가":
            st.markdown("""
            **김지원 콘텐츠 전략가**
            
            콘텐츠 전략 전문가로 10년간 디지털 콘텐츠 기획 및 전략 분야에서 활동했습니다.
            시장 트렌드 분석, 타겟 오디언스 정의, 콘텐츠 방향성 설정을 통해 효과적인 콘텐츠 전략을 수립합니다.
            
            * 전문 분야: 콘텐츠 마켓 리서치, 타겟 페르소나 개발, 컨텐츠 차별화 전략
            * 경력: 글로벌 콘텐츠 에이전시, 디지털 마케팅 컨설턴트, 콘텐츠 전략 디렉터
            """)
        
        elif expert_tab == "이민호 콘텐츠 작가":
            st.markdown("""
            **이민호 콘텐츠 작가**
            
            창작 및 스토리텔링 전문가로 8년간 다양한 디지털 콘텐츠 제작 분야에서 활동했습니다.
            매력적인 스토리 구조, 시각적/청각적 요소 기획, 감정적 연결 전략을 전문으로 합니다.
            
            * 전문 분야: 디지털 스토리텔링, 크리에이티브 콘텐츠 제작, 시청각 콘텐츠 설계
            * 경력: 크리에이티브 디렉터, 콘텐츠 프로듀서, 디지털 스토리텔러
            """)
        
        elif expert_tab == "박서연 플랫폼 전문가":
            st.markdown("""
            **박서연 플랫폼 전문가**
            
            플랫폼 최적화 및 유통 전문가로 9년간 디지털 마케팅 및 콘텐츠 최적화 분야에서 활동했습니다.
            다양한 플랫폼의 알고리즘 이해, 최적화 전략, 효과적인 콘텐츠 유통 방법을 제공합니다.
            
            * 전문 분야: 플랫폼 알고리즘 최적화, 콘텐츠 유통 전략, 성과 분석 및 최적화
            * 경력: 디지털 마케팅 전략가, 소셜 미디어 스페셜리스트, 콘텐츠 성과 분석가
            """)
            
        st.markdown("---")
        # 사용 방법 안내
        st.markdown("### ℹ️ 사용 방법")
        st.markdown("""
        1. API 키를 입력하세요
        2. 원하는 플랫폼을 선택하세요
        3. 콘텐츠 정보를 입력하세요
        4. '분석 시작' 버튼을 클릭하면 3명의 전문가가 순차적으로 분석합니다
        5. 최종 창작 가이드를 확인하세요
        """)
    
    # 서비스 선택 드롭다운
    service = st.selectbox(
        "원하는 플랫폼을 선택하세요",
        ["YouTube", "블로그", "인스타그램", "통합 콘텐츠"]
    )
    
    # 카드 스타일 CSS 수정
    st.markdown("""
    <style>
    .expert-card {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        color: #000000;  /* 글자색을 검정색으로 설정 */
    }
    .strategist-card {
        background-color: #E8F4F9;
        border-left: 5px solid #0077B6;
    }
    .creative-card {
        background-color: #E8F9E9;
        border-left: 5px solid #2D6A4F;
    }
    .platform-card {
        background-color: #F9F3E8;
        border-left: 5px solid #D4A017;
    }

    /* 전체 텍스트 색상 설정 */
    .stMarkdown, .stText {
        color: #000000 !important;
    }

    /* 마크다운 텍스트 색상 설정 */
    .stMarkdown p, .stMarkdown li {
        color: #000000 !important;
    }

    /* 결과 텍스트 색상 설정 */
    div[data-testid="stMarkdownContainer"] {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 워크플로우 설명
    with st.expander("에이전틱 워크플로우 프로세스 보기"):
        st.markdown("""
        ### 에이전틱 워크플로우 프로세스
        
        1. **요청 분석**: 사용자 콘텐츠 요청을 분석하여 필요한 전문성 식별
        2. **팀 구성**: 각 요청에 최적화된 AI 창작 전문가 팀 구성
        3. **콘텐츠 전략**: 콘텐츠 전략가가 전체적인 방향성과 타겟 오디언스 분석
        4. **창의적 개발**: 창작 작가가 스토리텔링과 창의적 콘텐츠 요소 개발
        5. **플랫폼 최적화**: 플랫폼 전문가가 배포 전략과 최적화 방안 제시
        6. **통합 가이드**: 세 전문가의 관점을 통합한 최종 맞춤형 콘텐츠 가이드 제공
        """)
    
    # 선택된 서비스에 따른 UI 표시
    if service == "YouTube":
        st.subheader("📹 YouTube 콘텐츠 개발")
        
        topic = st.text_area("주제/아이디어", height=100, placeholder="예: 홈트레이닝 시리즈, 기업가 인터뷰, 제품 리뷰...")
        goals = st.text_area("목표/목적", height=100, placeholder="예: 구독자 증가, 브랜드 인지도 향상, 제품 판매...")
        target_audience = st.text_area("타겟 시청자", height=100, placeholder="예: 20-35세 피트니스 초보자, 신생 스타트업 창업자...")
        
        col1, col2 = st.columns(2)
        with col1:
            channel_style = st.text_input("채널 스타일/톤", placeholder="예: 유머러스, 교육적, 전문적...")
            channel_size = st.selectbox("채널 규모", ["신규 채널", "소규모 (1천-1만)", "중규모 (1만-10만)", "대규모 (10만+)"])
        
        with col2:
            content_format = st.selectbox("콘텐츠 형식", ["튜토리얼/하우투", "Vlog", "인터뷰", "리뷰", "엔터테인먼트", "교육", "기타"])
            video_length = st.selectbox("예상 영상 길이", ["쇼트폼 (1분 미만)", "중간 (1-10분)", "롱폼 (10-30분)", "심층 콘텐츠 (30분+)"])
        
        additional_info = st.text_area("추가 정보 또는 요청사항", height=100)
        
        # 분석 시작 버튼
        if st.button("분석 시작"):
            if topic and goals and target_audience:
                # 전문가 팀 초기화
                creative_team = CreativeTeam(api_key)
                
                # 입력 데이터 구성
                input_data = {
                    "topic": topic,
                    "goals": goals,
                    "target_audience": target_audience,
                    "channel_style": channel_style,
                    "channel_size": channel_size,
                    "content_format": content_format,
                    "video_length": video_length,
                    "additional_info": additional_info
                }
                
                # 결과 처리
                result = creative_team.get_creative_advice("YouTube", input_data)
                
                # 결과 표시
                st.markdown("### 📊 창작 파트너 팀 분석 결과")
                st.markdown(f"""<div class="expert-card strategist-card"><b>김지원 콘텐츠 전략가</b><br><br>{result['strategy']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card creative-card"><b>이민호 콘텐츠 작가</b><br><br>{result['content']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card platform-card"><b>박서연 플랫폼 전문가 (최종 통합 조언)</b><br><br>{result['platform']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("주제, 목표, 타겟 시청자 정보를 모두 입력해주세요.")
                
    elif service == "블로그":
        st.subheader("📝 블로그 콘텐츠 개발")
        
        topic = st.text_area("주제/분야", height=100, placeholder="예: 지속가능한 생활 팁, 프로그래밍 튜토리얼, 여행 가이드...")
        goals = st.text_area("목표/목적", height=100, placeholder="예: 트래픽 증가, 이메일 구독자 확보, 제품 판매...")
        target_audience = st.text_area("타겟 독자", height=100, placeholder="예: 30-45세 환경 의식이 높은 부모, 주니어 개발자...")
        
        col1, col2 = st.columns(2)
        with col1:
            blog_style = st.text_input("블로그 스타일/톤", placeholder="예: 정보 제공형, 스토리텔링, 오피니언...")
            blog_platform = st.selectbox("블로그 플랫폼", ["워드프레스", "미디엄", "브런치", "티스토리", "네이버 블로그", "기타"])
        
        with col2:
            content_format = st.selectbox("콘텐츠 형식", ["How-to 가이드", "리스트형", "사례 연구", "인터뷰", "심층 분석", "개인 에세이", "기타"])
            seo_focus = st.selectbox("SEO 중요도", ["매우 중요", "중요", "보통", "낮음"])
        
        additional_info = st.text_area("추가 정보 또는 요청사항", height=100)
        
        if st.button("분석 시작"):
            if topic and goals and target_audience:
                creative_team = CreativeTeam(api_key)
                input_data = {
                    "topic": topic,
                    "goals": goals, 
                    "target_audience": target_audience,
                    "blog_style": blog_style,
                    "blog_platform": blog_platform,
                    "content_format": content_format,
                    "seo_focus": seo_focus,
                    "additional_info": additional_info
                }
                
                result = creative_team.get_creative_advice("블로그", input_data)
                
                st.markdown("### 📊 창작 파트너 팀 분석 결과")
                st.markdown(f"""<div class="expert-card strategist-card"><b>김지원 콘텐츠 전략가</b><br><br>{result['strategy']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card creative-card"><b>이민호 콘텐츠 작가</b><br><br>{result['content']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card platform-card"><b>박서연 플랫폼 전문가 (최종 통합 조언)</b><br><br>{result['platform']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("주제, 목표, 타겟 독자 정보를 모두 입력해주세요.")
    
    elif service == "인스타그램":
        st.subheader("📱 인스타그램 콘텐츠 개발")
        
        topic = st.text_area("계정 주제/성격", height=100, placeholder="예: 미니멀 라이프스타일, 요가 강사, 수제 쥬얼리 브랜드...")
        goals = st.text_area("목표/목적", height=100, placeholder="예: 팔로워 증가, 제품 판매, 인플루언서 포지셔닝...")
        target_audience = st.text_area("타겟 팔로워", height=100, placeholder="예: 20-35세 패션 관심 여성, 건강 라이프스타일 추구자...")
        
        col1, col2 = st.columns(2)
        with col1:
            visual_style = st.text_input("시각적 스타일", placeholder="예: 밝고 화사한, 모노톤, 자연주의...")
            account_size = st.selectbox("계정 규모", ["신규 계정", "소규모 (1천 미만)", "중규모 (1천-1만)", "대규모 (1만+)"])
        
        with col2:
            content_focus = st.selectbox("콘텐츠 포커스", ["피드 포스트", "릴스", "스토리", "모두 균형있게"])
            posting_frequency = st.selectbox("게시 빈도", ["일 1회 이상", "주 3-5회", "주 1-2회", "월 1-3회"])
        
        additional_info = st.text_area("추가 정보 또는 요청사항", height=100)
        
        if st.button("분석 시작"):
            if topic and goals and target_audience:
                creative_team = CreativeTeam(api_key)
                input_data = {
                    "topic": topic,
                    "goals": goals,
                    "target_audience": target_audience,
                    "visual_style": visual_style,
                    "account_size": account_size,
                    "content_focus": content_focus,
                    "posting_frequency": posting_frequency,
                    "additional_info": additional_info
                }
                
                result = creative_team.get_creative_advice("인스타그램", input_data)
                
                st.markdown("### 📊 창작 파트너 팀 분석 결과")
                st.markdown(f"""<div class="expert-card strategist-card"><b>김지원 콘텐츠 전략가</b><br><br>{result['strategy']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card creative-card"><b>이민호 콘텐츠 작가</b><br><br>{result['content']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card platform-card"><b>박서연 플랫폼 전문가 (최종 통합 조언)</b><br><br>{result['platform']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("주제, 목표, 타겟 팔로워 정보를 모두 입력해주세요.")
    
    elif service == "통합 콘텐츠":
        st.subheader("🔄 통합 콘텐츠 전략 개발")
        
        topic = st.text_area("주제/브랜드", height=100, placeholder="예: 건강식품 브랜드, 디지털 마케팅 전문가, 여행 블로거...")
        goals = st.text_area("목표/목적", height=100, placeholder="예: 브랜드 인지도 향상, 리드 생성, 온라인 커뮤니티 구축...")
        target_audience = st.text_area("타겟 오디언스", height=100, placeholder="예: 25-40세 건강 의식이 높은 전문직, 소규모 비즈니스 오너...")
        
        col1, col2 = st.columns(2)
        with col1:
            primary_platform = st.selectbox("주력 플랫폼", ["YouTube", "블로그", "인스타그램", "모두 동일 비중"])
            brand_style = st.text_input("브랜드 스타일/톤", placeholder="예: 전문적/교육적, 친근한/대화체, 영감을 주는...")
        
        with col2:
            current_status = st.selectbox("현재 채널 상태", ["신규 시작", "초기 단계", "성장 중", "안정된 팔로워십"])
            content_volume = st.selectbox("콘텐츠 생산 역량", ["주 1회 미만", "주 1-2회", "주 3-5회", "주 5회 이상"])
        
        additional_info = st.text_area("추가 정보 또는 요청사항", height=100)
        
        if st.button("분석 시작"):
            if topic and goals and target_audience:
                creative_team = CreativeTeam(api_key)
                input_data = {
                    "topic": topic,
                    "goals": goals,
                    "target_audience": target_audience,
                    "primary_platform": primary_platform,
                    "brand_style": brand_style,
                    "current_status": current_status,
                    "content_volume": content_volume,
                    "additional_info": additional_info
                }
                
                result = creative_team.get_creative_advice("통합 콘텐츠", input_data)
                
                st.markdown("### 📊 창작 파트너 팀 분석 결과")
                st.markdown(f"""<div class="expert-card strategist-card"><b>김지원 콘텐츠 전략가</b><br><br>{result['strategy']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card creative-card"><b>이민호 콘텐츠 작가</b><br><br>{result['content']}</div>""", unsafe_allow_html=True)
                st.markdown(f"""<div class="expert-card platform-card"><b>박서연 플랫폼 전문가 (최종 통합 조언)</b><br><br>{result['platform']}</div>""", unsafe_allow_html=True)
            else:
                st.warning("주제, 목표, 타겟 오디언스 정보를 모두 입력해주세요.")

# 스크립트가 직접 실행될 때만 main() 함수 실행
if __name__ == "__main__":
    main()