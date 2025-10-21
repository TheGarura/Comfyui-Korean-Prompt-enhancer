# -*- coding: utf-8 -*-
import google.generativeai as genai
from openai import OpenAI
import anthropic

class LLMIntegration:
    # 초기화 메소드: 각 API 클라이언트를 설정하고, 사용자가 지정한 모델 이름과 temperature를 저장합니다.
    def __init__(self, model_name, gemini_api_key, openai_api_key, anthropic_api_key, llm_provider="gemini", temperature=0.7):
        self.llm_provider = llm_provider
        self.temperature = temperature
        self.model_name = model_name # 사용자가 입력한 모델 이름을 저장

        if self.llm_provider == "gemini":
            if not gemini_api_key:
                raise ValueError("Gemini API key is required.")
            genai.configure(api_key=gemini_api_key)
            # 사용자가 지정한 모델 이름으로 Gemini 모델을 설정합니다.
            self.model = genai.GenerativeModel(self.model_name)
            self.generation_config = genai.types.GenerationConfig(temperature=self.temperature)

        elif self.llm_provider == "chatGPT":
            if not openai_api_key:
                raise ValueError("OpenAI API key is required.")
            self.client = OpenAI(api_key=openai_api_key)
            # self.model_name은 이미 상단에서 사용자가 지정한 값으로 설정되었습니다.

        elif self.llm_provider == "Claude":
            if not anthropic_api_key:
                raise ValueError("Anthropic API key is required.")
            self.client = anthropic.Anthropic(api_key=anthropic_api_key)
            # self.model_name은 이미 상단에서 사용자가 지정한 값으로 설정되었습니다.

    # LLM 공급자에 따라 적절한 API 호출 메소드를 실행하는 라우터입니다.
    def call_llm(self, prompt):
        if self.llm_provider == "gemini":
            return self.call_gemini(prompt)
        elif self.llm_provider == "chatGPT":
            return self.call_chatgpt(prompt)
        elif self.llm_provider == "Claude":
            return self.call_claude(prompt)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

    def call_gemini(self, prompt):
        try:
            response = self.model.generate_content(prompt, generation_config=self.generation_config)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {e}"

    def call_chatgpt(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name, # 사용자가 지정한 모델 사용
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {e}"

    def call_claude(self, prompt):
        try:
            message = self.client.messages.create(
                model=self.model_name, # 사용자가 지정한 모델 사용
                max_tokens=2048,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error calling Anthropic API: {e}"
