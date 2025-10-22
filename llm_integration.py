# -*- coding: utf-8 -*-
# 파일명: llm_integration.py

import google.generativeai as genai
from openai import OpenAI
import anthropic

class LLMIntegration:
    """
    다양한 LLM 공급자(Gemini, OpenAI, Anthropic)와의 API 통신을 관리하는 클래스입니다.
    주요 설계 목표는 API 호출 실패 시 에러를 발생시키는 대신 None을 반환하여,
    이 클래스를 호출한 상위 로직(메인 노드)에서 안정적인 폴백(Fallback) 처리를 할 수 있도록 하는 것입니다.
    """
    # 초기화 메소드: 각 API 클라이언트를 설정하고, 사용자가 지정한 모델 이름과 temperature를 저장합니다.
    def __init__(self, model_name, gemini_api_key=None, openai_api_key=None, anthropic_api_key=None, llm_provider="gemini", temperature=0.7):
        # 인스턴스 변수 설정
        self.llm_provider = llm_provider  # 사용할 LLM 서비스 제공자 (e.g., "gemini")
        self.temperature = temperature    # 생성 결과의 창의성 조절 (0.0 ~ 1.0)
        self.model_name = model_name      # 사용할 특정 모델의 이름 (e.g., "gemini-pro")

        # LLM 공급자에 따라 필요한 API 키를 확인하고 클라이언트를 초기화합니다.
        if self.llm_provider == "gemini":
            if not gemini_api_key: raise ValueError("Gemini API 키가 필요합니다.")
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.generation_config = genai.types.GenerationConfig(temperature=self.temperature)

        elif self.llm_provider == "chatGPT":
            if not openai_api_key: raise ValueError("OpenAI API 키가 필요합니다.")
            self.client = OpenAI(api_key=openai_api_key)

        elif self.llm_provider == "Claude":
            if not anthropic_api_key: raise ValueError("Anthropic API 키가 필요합니다.")
            self.client = anthropic.Anthropic(api_key=anthropic_api_key)

    def call_llm(self, prompt):
        """
        LLM 공급자에 따라 적절한 API 호출 메소드를 실행하는 라우터(분배기) 역할을 합니다.
        딕셔너리를 사용하여 코드를 간결하고 확장 가능하게 만듭니다.
        """
        route = {
            "gemini": self.call_gemini,
            "chatGPT": self.call_chatgpt,
            "Claude": self.call_claude
        }
        call_function = route.get(self.llm_provider) # 공급자에 맞는 함수를 가져옴
        if call_function:
            return call_function(prompt) # 해당 함수를 실행하고 결과를 반환
        else:
            # 지원하지 않는 공급자일 경우 에러 발생
            raise ValueError(f"지원하지 않는 LLM 공급자입니다: {self.llm_provider}")

    def call_gemini(self, prompt):
        """Gemini API를 호출하여 프롬프트 결과를 생성합니다."""
        try:
            # API를 통해 콘텐츠 생성을 요청합니다.
            response = self.model.generate_content(prompt, generation_config=self.generation_config)
            return response.text
        except Exception as e:
            # 네트워크 오류, API 키 오류 등 모든 예외 상황을 처리합니다.
            print(f"[LLMIntegration 오류] Gemini API 호출 실패: {e}") # 디버깅을 위해 콘솔에 오류 기록
            return None # 실패 신호로 None을 반환하여 폴백 로직을 트리거

    def call_chatgpt(self, prompt):
        """OpenAI (ChatGPT) API를 호출하여 프롬프트 결과를 생성합니다."""
        try:
            # API를 통해 채팅 완성(completion)을 요청합니다.
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[LLMIntegration 오류] OpenAI API 호출 실패: {e}")
            return None # 실패 신호로 None을 반환

    def call_claude(self, prompt):
        """Anthropic (Claude) API를 호출하여 프롬프트 결과를 생성합니다."""
        try:
            # API를 통해 메시지 생성을 요청합니다.
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2048, # 최대 생성 토큰 수 설정
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"[LLMIntegration 오류] Anthropic API 호출 실패: {e}")
            return None # 실패 신호로 None을 반환
        