# ComfyUI Korean Prompt Enhancer

This document is also available in [Korean](#--korean).

## 1. Introduction

The `Korean Prompt Enhancer` is a ComfyUI custom node that uses a Large Language Model (LLM) to generate creative and detailed image prompts from Korean language input. Its goal is to create rich, descriptive final prompts by combining an initial idea with various options, going beyond simple translation.

## 2. Key Features

- **Multi-LLM Support**: Choose from major LLM providers like Gemini, OpenAI (ChatGPT), and Anthropic (Claude).
- **Custom Model Name**: Specify the exact model name you want to use for each provider (e.g., `gpt-4o-mini`, `claude-3-haiku-20240307`).
- **Detailed Prompt Options**: Enhance prompts with over 30 granular options for characters, style, camera, lighting, and more.
- **"Auto" Mode**: Set key options like style, character, and cinematography to `auto` to let the LLM creatively choose the best keywords.
- **Complex Scene Composition**: Describe complex scenes by defining up to two subjects and their relationship or placement.
- **Intelligent Negative Prompt**: Automatically generate context-aware negative keywords to prevent common artifacts (e.g., malformed hands, duplicate heads) based on the positive prompt.
- **Multiple Prompt Variations**: Generate several versions of a prompt in a single run to explore different creative directions.

## 3. Installation

1.  **Download Node**: Place the `comfyui-korean-prompt-enhancer` folder inside your `ComfyUI/custom_nodes/` directory.
    ```
    ComfyUI/custom_nodes/comfyui-korean-prompt-enhancer/
    ```

2.  **Install Dependencies**: Run the following command in your terminal to install all required libraries from the `requirements.txt` file.

    ```bash
    # You must use the pip from your ComfyUI's .venv folder.
    /Users/garura/Documents/ComfyUI/.venv/bin/pip install -r /Users/garura/Documents/ComfyUI/custom_nodes/comfyui-korean-prompt-enhancer/requirements.txt
    ```

3.  **Restart ComfyUI**: Completely restart the ComfyUI server after installation.

## 4. Inputs

| Name                          | Description                                                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `korean_prompt`               | Enter the core description of Subject 1 in Korean (e.g., `a beautiful woman in a hanbok`).                                                 |
| `target_language`             | Select the final language for the prompt.                                                                                                  |
| `llm_provider`                | Select the LLM provider to use (gemini, chatGPT, Claude).                                                                                  |
| `model_name`                  | Enter the specific model name for the chosen provider (e.g., `gemini-1.5-flash-latest`, `gpt-4o`, `claude-3-sonnet-20240229`).      |
| `subject_2_prompt`            | (Optional) Enter a description for a second subject in Korean. Filling this enables complex scene mode.                                    |
| `composition_description`     | (Optional) Describe the relationship between the two subjects or the overall scene composition.                                            |
| `style`                       | Select the overall style of the image. Set to `auto` for the LLM to recommend one.                                                       |
| `artist_style_keywords`       | Enter specific artists or styles to emulate (e.g., `by Hayao Miyazaki`).                                                                 |
| `ethnicity`, `age`, `gender`  | (Single Subject Mode) Set the ethnicity, age, and gender of the subject. `ethnicity` can be set to `auto`.                                 |
| `camera_angle`, `lens`, `lighting` | Select the shot composition, lens, and lighting effects. All can be set to `auto`.                                                       |
| `num_variations`              | Set the number of prompt variations to generate.                                                                                           |
| `temperature`                 | Adjust the creativity of the LLM (0.0-2.0). Lower values are more consistent; higher values are more creative.                             |
| `generate_intelligent_negative` | If set to `True`, the LLM will automatically generate a negative prompt based on the positive prompt.                                      |
| `*_api_key`                   | Enter the appropriate API key for each LLM provider.                                                                                       |
| `negative_prompt`             | Enter any basic negative prompts you want to add yourself.                                                                               |

## 5. Outputs

| Name                      | Description                                                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `enhanced_prompts_batch`  | The final batch of generated positive prompts. If `num_variations` > 1, multiple prompts will be included.                                   |
| `final_negative_prompt`   | The final combined negative prompt, including user input, default negatives, and (optionally) the intelligent negative prompt.             |
| `metadata`                | A JSON text containing all the settings used to generate the prompt. Useful for reproducibility and analysis.                                |

---

## (Korean)

## 1. 소개

`Korean Prompt Enhancer`는 한국어 프롬프트를 입력받아 LLM(대규모 언어 모델)을 통해 창의적이고 상세한 이미지 생성용 프롬프트를 만들어주는 ComfyUI 커스텀 노드입니다. 단순히 번역만 하는 것을 넘어, 다양한 옵션과 결합하여 풍부한 묘사가 담긴 최종 프롬프트를 생성하는 것을 목표로 합니다.

## 2. 주요 기능

- **다양한 LLM 지원**: Gemini, OpenAI(ChatGPT), Anthropic(Claude) 등 주요 LLM 공급자를 선택하여 사용할 수 있습니다.
- **사용자 지정 모델명**: 각 LLM 공급자 내에서 사용하고 싶은 특정 모델 이름(예: `gpt-4o-mini`, `claude-3-haiku-20240307`)을 직접 지정할 수 있습니다.
- **상세한 프롬프트 옵션**: 인물, 스타일, 카메라, 조명 등 30가지가 넘는 세분화된 옵션을 제공하여 프롬프트의 완성도를 높입니다.
- **`auto` 모드**: 스타일, 인물, 촬영 기법 등 주요 옵션을 `auto`로 설정하면, LLM이 문맥에 가장 어울리는 키워드를 창의적으로 선택합니다.
- **복합적인 장면 구성**: 최대 2개의 주체(인물/사물)와 그들의 관계 및 배치를 자유롭게 서술하여 복잡한 장면을 연출할 수 있습니다.
- **지능형 네거티브 프롬프트**: 생성된 긍정 프롬프트를 기반으로, 이미지의 완성도를 해칠 수 있는 요소(예: 깨진 손가락, 중복된 머리)를 방지하기 위한 네거티브 키워드를 LLM이 자동으로 추천합니다.
- **다중 프롬프트 변형(Variation)**: 한 번의 실행으로 여러 버전의 프롬프트를 생성하여, 가장 마음에 드는 결과물을 선택할 수 있습니다.

## 3. 설치 방법

1.  **노드 다운로드**: `comfyui-korean-prompt-enhancer` 폴더를 ComfyUI의 `custom_nodes` 디렉토리 내에 위치시킵니다.
    ```
    ComfyUI/custom_nodes/comfyui-korean-prompt-enhancer/
    ```

2.  **필요 라이브러리 설치**: ComfyUI 가상 환경에서 아래의 명령어를 실행하여 `requirements.txt` 파일에 명시된 모든 라이브러리를 설치합니다.

    ```bash
    # ComfyUI가 설치된 폴더의 .venv/bin/pip를 사용해야 합니다.
    /Users/garura/Documents/ComfyUI/.venv/bin/pip install -r /Users/garura/Documents/ComfyUI/custom_nodes/comfyui-korean-prompt-enhancer/requirements.txt
    ```

3.  **ComfyUI 재시작**: 라이브러리 설치 후, ComfyUI 서버를 완전히 재시작합니다.

## 4. 입력(Inputs) 설명

| 이름                          | 설명                                                                                                                                |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `korean_prompt`               | 주체 1에 대한 핵심 설명을 한국어로 입력합니다. (예: `한복을 입은 아름다운 여성`)                                                        |
| `target_language`             | 프롬프트가 번역될 최종 언어를 선택합니다.                                                                                           |
| `llm_provider`                | 사용할 LLM 공급자를 선택합니다. (gemini, chatGPT, Claude)                                                                           |
| `model_name`                  | `llm_provider`에서 사용할 상세 모델명을 입력합니다. (예: `gemini-1.5-flash-latest`, `gpt-4o`, `claude-3-sonnet-20240229`)         |
| `subject_2_prompt`            | (선택) 장면에 추가할 두 번째 주체를 한국어로 입력합니다. 이 필드를 채우면 복합 장면 구성 모드로 작동합니다.                      |
| `composition_description`     | (선택) 두 주체의 관계나 장면 전체의 구성을 서술합니다. (예: `1번 주체가 2번 주체의 어깨에 기대어 있다`)                       |
| `style`                       | 이미지의 전체적인 스타일을 선택합니다. `auto`로 설정 시 LLM이 추천합니다.                                                         |
| `artist_style_keywords`       | 참고하고 싶은 특정 아티스트나 화풍을 텍스트로 입력합니다. (예: `by Hayao Miyazaki`)                                                 |
| `ethnicity`, `age`, `gender`  | (단일 주체 모드) 주체의 인종, 나이, 성별을 설정합니다. `ethnicity`는 `auto` 설정이 가능합니다.                                   |
| `camera_angle`, `lens`, `lighting` | 촬영 구도, 렌즈, 조명 효과를 선택합니다. 모두 `auto` 설정이 가능합니다.                                                          |
| `num_variations`              | 생성할 프롬프트 변형의 개수를 정합니다.                                                                                             |
| `temperature`                 | LLM의 창의성을 조절합니다. (0.0~2.0, 낮을수록 일관적, 높을수록 창의적)                                                              |
| `generate_intelligent_negative` | `True`로 설정 시, 생성된 긍정 프롬프트에 맞춰 LLM이 네거티브 프롬프트를 자동으로 생성합니다.                                        |
| `*_api_key`                   | 각 LLM 공급자에 맞는 API 키를 입력합니다.                                                                                           |
| `negative_prompt`             | 사용자가 직접 추가하고 싶은 기본 네거티브 프롬프트를 입력합니다.                                                                    |

## 5. 출력(Outputs) 설명

| 이름                      | 설명                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| `enhanced_prompts_batch`  | 최종적으로 생성된 긍정 프롬프트 묶음입니다. (`num_variations` > 1일 경우, 여러 프롬프트가 포함됩니다.) |
| `final_negative_prompt`   | 사용자가 입력한 네거티브, 기본 네거티브, 그리고 (옵션에 따라) 지능형 네거티브가 모두 조합된 최종 결과물입니다. |
| `metadata`                | 프롬프트 생성에 사용된 모든 설정값이 JSON 형식으로 저장된 텍스트입니다. 재현 및 분석에 유용합니다.      |