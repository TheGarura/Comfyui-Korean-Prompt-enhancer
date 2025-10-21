# -*- coding: utf-8 -*-
# 외부 LLM 연동을 처리하는 LLMIntegration 클래스를 가져옵니다.
from .llm_integration import LLMIntegration
# 메타데이터 생성을 위해 json 라이브러리를 가져옵니다.
import json

# ComfyUI 커스텀 노드의 메인 클래스입니다.
class KoreanPromptEnhancer:
    @classmethod
    def INPUT_TYPES(s):
        # 노드의 UI를 정의하는 부분입니다.
        # 여기에 정의된 순서는 아래 execute 함수의 파라미터 순서와 반드시 일치해야 합니다.
        return {
            "required": {
                # 1. 핵심 프롬프트 정보
                "korean_prompt": ("STRING", {"multiline": True, "default": ""}), # 주체 1에 대한 한국어 설명
                "target_language": (["English", "Chinese", "Chinese-Taiwan"],), # 번역 목표 언어
                "llm_provider": (["gemini", "chatGPT", "Claude"],), # 사용할 LLM 서비스
                "model_name": ("STRING", {"multiline": False, "default": "gemini-1.5-flash-latest"}), # 사용할 LLM의 상세 모델명

                # 2. 복합 장면 구성 (선택 사항)
                "subject_2_prompt": ("STRING", {"multiline": True, "default": ""}), # 장면에 추가할 주체 2에 대한 한국어 설명
                "composition_description": ("STRING", {"multiline": True, "default": "Subject 1 is the main focus."} ), # 주체 1과 2의 관계 및 장면 구성 설명

                # 3. 스타일 관련 옵션
                "style": (["auto", "photorealistic", "hyperrealistic", "cinematic", "film noir", "anime (90s style)", "manga", "ghibli style", "vintage photography", "fantasy art", "sci-fi concept art", "cyberpunk", "steampunk", "watercolor", "oil painting", "impressionism", "pop art", "minimalist"],), # 전체적인 이미지 스타일
                "artist_style_keywords": ("STRING", {"multiline": False, "default": ""}), # 참고할 특정 아티스트나 화풍

                # 4. 주체 상세 정보 (단일 주체일 경우 주로 사용)
                "ethnicity": (["auto", "African", "Afro-American", "Arab", "Caucasian", "Chinese", "Hispanic", "Indian", "Japanese", "Korean", "Native American", "Southeast Asian"],), # 인종
                "age": (["10s", "20s", "30s", "40s", "50s+"],), # 연령대
                "gender": (["Male", "Female"],), # 성별

                # 5. 시네마틱(촬영) 관련 옵션
                "camera_angle": (["auto", "eye-level shot", "low-angle shot", "high-angle shot", "dutch angle", "over-the-shoulder shot", "point-of-view (POV)", "close-up", "medium shot", "long shot", "crane shot", "drone shot", "bird-eye view"],), # 카메라 각도
                "lens": (["auto", "wide-angle", "ultra-wide-angle", "standard (50mm)", "telephoto", "super-telephoto", "macro", "prime lens", "zoom lens", "fisheye", "tilt-shift"],), # 카메라 렌즈
                "lighting": (["auto", "natural light", "golden hour", "blue hour", "midday sun", "overcast", "studio light", "softbox", "ring light", "rim light", "backlight", "dramatic light", "chiaroscuro", "neon lights", "candlelight"],), # 조명
                
                # 6. 생성 방식 제어
                "num_variations": ("INT", {"default": 1, "min": 1, "max": 10}), # 생성할 프롬프트 변형 개수
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1}), # LLM의 창의성 (0.0~2.0)
                "generate_intelligent_negative": ("BOOLEAN", {"default": False}), # 지능형 네거티브 프롬프트 생성 여부

                # 7. API 키 및 기본 네거티브 프롬프트
                "gemini_api_key": ("STRING", {"multiline": False, "default": ""}),
                "openai_api_key": ("STRING", {"multiline": False, "default": ""}),
                "anthropic_api_key": ("STRING", {"multiline": False, "default": ""}),
                "negative_prompt": ("STRING", {"multiline": True, "default": "blurry, distortion, cartoon"}),
            }
        }

    # 노드의 출력 타입을 정의합니다.
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    # 노드의 출력 이름을 정의합니다. UI에 표시됩니다.
    RETURN_NAMES = ("enhanced_prompts_batch", "final_negative_prompt", "metadata")
    # 노드가 실행할 실제 함수(메소드)의 이름을 지정합니다.
    FUNCTION = "execute"
    # ComfyUI 메뉴에서 노드가 나타날 카테고리를 지정합니다.
    CATEGORY = "Korean Prompt Enhancer"

    # 노드의 핵심 로직을 수행하는 메소드입니다.
    # 파라미터의 순서는 위의 INPUT_TYPES에 정의된 순서와 완벽하게 일치해야 오류가 발생하지 않습니다.
    def execute(self, korean_prompt, target_language, llm_provider, model_name, subject_2_prompt, composition_description, style, artist_style_keywords, ethnicity, age, gender, camera_angle, lens, lighting, num_variations, temperature, generate_intelligent_negative, gemini_api_key, openai_api_key, anthropic_api_key, negative_prompt):
        
        # LLM 연동을 위한 클래스를 초기화합니다. 모든 관련 정보를 전달합니다.
        llm = LLMIntegration(model_name=model_name, gemini_api_key=gemini_api_key, openai_api_key=openai_api_key, anthropic_api_key=anthropic_api_key, llm_provider=llm_provider, temperature=temperature)

        generated_prompts = [] # 생성된 긍정 프롬프트들을 저장할 리스트
        intelligent_negatives = [] # 생성된 지능형 네거티브 프롬프트들을 저장할 리스트

        # 사용자가 요청한 `num_variations` 만큼 프롬프트 생성을 반복합니다.
        for i in range(num_variations):
            # --- 1. 긍정 프롬프트 생성을 위한 LLM 지시문 구성 ---
            
            # `subject_2_prompt`가 비어있는지에 따라 단일 장면인지 복합 장면인지 판단합니다.
            is_complex_scene = subject_2_prompt.strip()
            if not is_complex_scene:
                # 단일 주체(인물/사물)에 대한 프롬프트 템플릿
                base_prompt = f"""Generate a rich, descriptive image prompt about a single subject.\nTranslate the following Korean description of the subject into {target_language}:\n`{korean_prompt}`\n\nCreatively combine it with these characteristics:\n"""
            else:
                # 두 주체가 등장하는 복합 장면에 대한 프롬프트 템플릿
                base_prompt = f"""Generate a rich, descriptive image prompt for a complex scene with two subjects.\n\n- Subject 1 (in Korean): `{korean_prompt}`\n- Subject 2 (in Korean): `{subject_2_prompt}`\n\nTranslate both subjects into {target_language} and place them in a scene based on the following composition description:\n`{composition_description}`\n\nAlso, creatively combine the scene with these characteristics:\n"""

            # LLM에게 전달할 세부 특성(characteristics)을 동적으로 구성합니다.
            characteristics = []
            if style != "auto": characteristics.append(f"- Overall Style: {style}")
            else: characteristics.append("- Overall Style: [Choose a creative and fitting style]") # 'auto'일 경우 LLM에게 선택 위임

            if artist_style_keywords:
                # 아티스트 키워드가 있을 경우, 단순히 이름을 나열하는 대신 화풍을 모방하도록 더 구체적으로 지시합니다.
                characteristics.append(f"- Art Style Influence: Emulate the distinct artistic style of {artist_style_keywords}, paying attention to their characteristic techniques (e.g., brushstrokes, color palette, mood).")

            # 단일 주체 장면일 경우에만 인물/피사체에 대한 상세 정보를 추가합니다.
            if not is_complex_scene:
                if ethnicity != "auto": characteristics.append(f"- Subject Details: A {age} {ethnicity} {gender}")
                else: characteristics.append(f"- Subject Details: A {age} [Choose a fitting ethnicity] {gender}")

            # 촬영 관련 상세 정보를 구성합니다.
            shot_details = []
            if camera_angle != "auto": shot_details.append(camera_angle)
            else: shot_details.append("[Choose a dynamic camera angle]")
            if lens != "auto": shot_details.append(f"{lens} lens")
            else: shot_details.append("[Choose a suitable lens]")
            if lighting != "auto": shot_details.append(f"with {lighting}")
            else: shot_details.append("with [Choose impactful lighting]")
            characteristics.append(f"- Cinematic Details: {', '.join(shot_details)}")

            # 최종적으로 LLM에게 전달할 긍정 프롬프트 지시문을 조립합니다.
            positive_prompt_template = base_prompt + "\n".join(characteristics)
            positive_prompt_template += f"\n\nThe final output should be a single, coherent, and detailed paragraph in {target_language} for an image generation model."

            # 두 번째 변형부터는 이전과 다른 결과물을 생성하도록 명시적으로 요청합니다.
            if i > 0: positive_prompt_template += "\n\nIMPORTANT: Generate a new, different variation of the prompt based on the same core request."

            # LLM을 호출하여 강화된 긍정 프롬프트를 생성합니다.
            enhanced_prompt = llm.call_llm(positive_prompt_template)
            generated_prompts.append(enhanced_prompt)

            # --- 2. 지능형 네거티브 프롬프트 생성 (사용자가 옵션을 켰을 경우) ---
            if generate_intelligent_negative:
                # 생성된 긍정 프롬프트를 기반으로, 관련 네거티브 키워드를 생성하도록 LLM에게 요청합니다.
                negative_prompt_template = f'''Based on the image prompt: "{enhanced_prompt}"\nList comma-separated negative keywords to prevent common image artifacts, deformities, or unwanted elements. Only output the keywords in a single line.'''
                generated_negative = llm.call_llm(negative_prompt_template)
                intelligent_negatives.append(generated_negative)

        # --- 3. 최종 결과물 조합 ---
        # 생성된 모든 긍정 프롬프트 변형들을 두 줄의 공백으로 구분하여 하나의 텍스트로 합칩니다.
        final_batch_prompt = "\n\n".join(generated_prompts)

        # 네거티브 프롬프트를 조합합니다.
        default_negatives = "low quality, watermark, blurry, distortion, cartoon" # 기본 네거티브
        # 생성된 모든 지능형 네거티브들을 중복 제거하여 합칩니다.
        intelligent_negative_str = ", ".join(sorted(list(set(intelligent_negatives))))
        # 사용자가 입력한 네거티브, 기본 네거티브, 지능형 네거티브를 모두 합칩니다. (빈 값은 제외)
        final_negative_prompt = ", ".join(filter(None, [negative_prompt, default_negatives, intelligent_negative_str]))

        # 재현 및 분석을 위해 사용된 모든 설정값을 JSON 형식의 메타데이터로 저장합니다.
        metadata = json.dumps({
            "korean_prompt": korean_prompt,
            "target_language": target_language,
            "llm_provider": llm_provider,
            "model_name": model_name,
            "subject_2_prompt": subject_2_prompt,
            "composition_description": composition_description,
            "style": style,
            "artist_style_keywords": artist_style_keywords,
            "ethnicity": ethnicity,
            "age": age,
            "gender": gender,
            "camera_angle": camera_angle,
            "lens": lens,
            "lighting": lighting,
            "num_variations": num_variations,
            "temperature": temperature,
            "generate_intelligent_negative": generate_intelligent_negative,
        }, indent=4, ensure_ascii=False)

        # 최종 결과물들을 튜플 형태로 ComfyUI에 반환합니다.
        return (final_batch_prompt, final_negative_prompt, metadata)

# ComfyUI가 이 파일을 커스텀 노드로 인식하게 하는 필수 설정입니다.
NODE_CLASS_MAPPINGS = {
    "KoreanPromptEnhancer": KoreanPromptEnhancer
}

# ComfyUI 메뉴에 표시될 노드의 이름을 지정합니다.
NODE_DISPLAY_NAME_MAPPINGS = {
    "KoreanPromptEnhancer": "Korean Prompt Enhancer"
}