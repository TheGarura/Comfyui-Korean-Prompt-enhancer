# -*- coding: utf-8 -*-
# 파일명: korean_prompt_enhancer.py

# 외부 라이브러리 import
from googletrans import Translator
# 같은 폴더 내의 llm_integration 모듈에서 LLMIntegration 클래스를 import
from .llm_integration import LLMIntegration 

class KoreanPromptEnhancer:
    """
    ComfyUI 커스텀 노드 클래스입니다.
    한국어 프롬프트를 입력받아 LLM을 통해 창의적으로 확장하는 것을 주 목적으로 합니다.
    만약 LLM API 호출에 실패할 경우, 자체적인 폴백(Fallback) 로직을 통해
    입력된 옵션과 번역된 프롬프트를 조합하여 안정적인 영어 프롬프트를 생성합니다.
    """
    @classmethod
    def INPUT_TYPES(s):
        """ComfyUI 노드의 입력 필드를 정의하는 메소드입니다."""
        return {
            # 필수 입력 필드 정의
            "required": {
                "korean_prompt": ("STRING", {"multiline": True, "default": "노을이 지는 해변을 걷고 있는 백마"}),
                "llm_provider": (["gemini", "chatGPT", "Claude"],),
                "model_name": ("STRING", {"default": "gemini-pro"}),
                "target_language": (["English", "Chinese", "Chinese-Taiwan"],),
                "style": (["photorealistic", "anime", "vintage", "fantasy art", "cyberpunk"],),
                "ethnicity": (["Korean", "Japanese", "Chinese", "Caucasian", "African"],),
                "age": (["10s", "20s", "30s", "40s", "50s+"],),
                "gender": (["Male", "Female", "Person"],),
                "camera_angle": (["eye-level", "front view", "side view", "top view", "bird-eye view"],),
                "lens": (["wide-angle", "standard", "telephoto", "macro"],),
                "lighting": (["natural light", "studio light", "dramatic light", "cinematic lighting"],),
                "negative_prompt": ("STRING", {"multiline": True, "default": "blurry, distortion, cartoon, watermark, text"}),
            },
            # 선택적 입력 필드 정의 (API 키)
            "optional": {
                "gemini_api_key": ("STRING", {"multiline": False, "placeholder": "Enter Gemini API Key"}),
                "openai_api_key": ("STRING", {"multiline": False, "placeholder": "Enter OpenAI API Key"}),
                "anthropic_api_key": ("STRING", {"multiline": False, "placeholder": "Enter Anthropic API Key"}),
            }
        }

    # ComfyUI 노드의 출력 타입을 정의합니다.
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    # ComfyUI 노드의 출력 필드 이름을 정의합니다.
    RETURN_NAMES = ("enhanced_prompt", "final_negative_prompt", "metadata")
    # 실제 로직을 수행할 함수의 이름을 지정합니다.
    FUNCTION = "enhance"
    # ComfyUI 노드 메뉴에서의 카테고리 이름을 지정합니다.
    CATEGORY = "Prompt Enhancement"

    def _translate_korean_to_english(self, text: str) -> str:
        """
        googletrans 라이브러리를 사용하여 한국어 텍스트를 영어로 번역하는 내부 헬퍼 함수입니다.
        번역 실패 시(예: 인터넷 연결 없음), 에러를 발생시키지 않고 원본 텍스트를 그대로 반환하여 안정성을 높입니다.
        """
        # 입력 텍스트가 비어있거나 공백만 있으면 빈 문자열을 반환합니다.
        if not text or not text.strip():
            return ""
        try:
            translator = Translator()
            # 한국어(ko)를 영어(en)로 번역합니다.
            result = translator.translate(text, src='ko', dest='en')
            return result.text
        except Exception as e:
            # 번역 과정에서 예외 발생 시 콘솔에 오류를 출력합니다.
            print(f"[번역 오류] '{text}' 번역 실패. 원본을 반환합니다. 오류: {e}")
            # 번역에 실패했더라도 워크플로우가 중단되지 않도록 원본 텍스트를 반환합니다.
            return text

    def _generate_fallback_prompt(self, korean_prompt, style, ethnicity, age, gender, camera_angle, lens, lighting):
        """
        LLM 호출 실패 시 실행되는 대체 프롬프트 생성기입니다.
        한국어 프롬프트를 기본 번역하고, 사용자가 선택한 옵션들을 기계적으로 조합하여
        안정적이고 표준적인 영어 프롬프트를 생성합니다.
        """
        # 1. 먼저 한국어 핵심 프롬프트를 영어로 번역합니다.
        translated_prompt = self._translate_korean_to_english(korean_prompt)
        
        # 2. 이미지 생성 모델에 효과적인 순서(스타일 -> 주제 -> 세부사항)로 프롬프트 구성요소를 리스트에 담습니다.
        prompt_parts = [
            style,
            f"a portrait of a {ethnicity} {gender} in their {age}", # 예: "a portrait of a Korean Female in their 20s"
            translated_prompt, # 예: "a white horse walking on the beach at sunset"
            f"shot from a {camera_angle}",
            f"using a {lens} lens",
            lighting
        ]
        
        # 3. 리스트의 요소 중 비어있지 않은(None이나 빈 문자열이 아닌) 것들만 ", "로 연결합니다.
        final_prompt = ", ".join(filter(None, prompt_parts))
        print(f"[폴백 모드] 대체 프롬프트 생성: {final_prompt}")
        return final_prompt

    def enhance(self, korean_prompt, llm_provider, model_name, target_language, style, ethnicity, age, gender, camera_angle, lens, lighting, negative_prompt, **kwargs):
        """노드의 메인 실행 함수입니다."""
        enhanced_prompt = None # 최종 프롬프트를 담을 변수 초기화
        metadata = ""          # 처리 결과에 대한 정보를 담을 변수 초기화

        try:
            # 1. LLM 클라이언트 초기화를 시도합니다. API 키가 유효하지 않으면 여기서 에러가 발생할 수 있습니다.
            llm_integration = LLMIntegration(
                model_name=model_name,
                llm_provider=llm_provider,
                gemini_api_key=kwargs.get('gemini_api_key'),
                openai_api_key=kwargs.get('openai_api_key'),
                anthropic_api_key=kwargs.get('anthropic_api_key'),
            )
            
            # 2. LLM에게 전달할 상세한 지시문(Instruction) 프롬프트를 생성합니다.
            instructional_prompt = (
                f"You are a prompt engineer for an image generation AI. "
                f"Translate the following Korean concept into a rich, creative, and descriptive prompt in {target_language}. "
                f"Combine it with the following keywords: Style={style}, Subject={ethnicity} {gender} in {age}, "
                f"Camera={camera_angle} with {lens} lens, Lighting={lighting}. "
                f"Korean Concept: '{korean_prompt}'"
            )

            # 3. LLM API 호출을 시도합니다.
            enhanced_prompt = llm_integration.call_llm(instructional_prompt)

        except Exception as e:
            # LLM 클라이언트 초기화나 호출 준비 과정에서 오류 발생 시 처리
            print(f"[노드 오류] LLM 초기화 또는 호출 준비 실패: {e}")
            enhanced_prompt = None # 명시적으로 실패 처리하여 폴백 로직이 실행되도록 함

        # 4. LLM 호출 결과에 따라 최종 프롬프트를 결정합니다.
        if enhanced_prompt:
            # 성공 시: LLM이 생성한 창의적인 프롬프트를 사용합니다.
            metadata = f"LLM ({llm_provider}/{model_name})에 의해 성공적으로 생성되었습니다."
        else:
            # 실패 시 (enhanced_prompt가 None일 경우): 폴백 로직을 실행합니다.
            metadata = "[경고] LLM 호출에 실패하여 대체 프롬프트가 생성되었습니다."
            enhanced_prompt = self._generate_fallback_prompt(korean_prompt, style, ethnicity, age, gender, camera_angle, lens, lighting)

        # 5. 최종 결과물들을 튜플 형태로 반환합니다.
        return (enhanced_prompt, negative_prompt, metadata)

# ComfyUI에 이 노드를 등록하기 위한 필수 코드입니다.
# 클래스 이름과 실제 노드 클래스를 매핑합니다.
NODE_CLASS_MAPPINGS = {
    "KoreanPromptEnhancer": KoreanPromptEnhancer
}
# ComfyUI 메뉴에 표시될 노드의 이름을 지정합니다.
NODE_DISPLAY_NAME_MAPPINGS = {
    "KoreanPromptEnhancer": "Korean Prompt Enhancer (LLM/Fallback)"
} 
