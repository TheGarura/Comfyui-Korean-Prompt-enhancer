# ComfyUI Korean Prompt Enhancer

<div align="center">

**이제 한국어로 편하게 상상력을 표현하고, 나머지는 AI에게 맡기세요.**  
**Express your imagination in Korean, and let AI handle the rest.**

</div>

[**한국어**](#-korean-prompt-enhancer) | [**English**](#-korean-prompt-enhancer-english-version)

---

## 🇰🇷 Korean Prompt Enhancer

`Korean Prompt Enhancer`는 ComfyUI 사용자를 위한 궁극의 프롬프트 자동화 도구입니다. 이 커스텀 노드는 간단한 한국어 아이디어를 입력받아, Gemini, ChatGPT, Claude와 같은 강력한 LLM(거대 언어 모델)을 통해 예술적이고 풍부한 이미지 생성 프롬프트로 자동 확장 및 번역해 줍니다.

LLM 연결에 실패하더라도 걱정하지 마세요. 안정적인 폴백(Fallback) 기능이 내장되어 있어, 어떤 상황에서도 워크플로우가 중단되지 않고 안정적인 결과물을 생성합니다.

### ✨ 주요 기능

- **🤖 LLM 기반 프롬프트 확장**: Gemini, ChatGPT, Claude를 지원하여, 단순한 키워드를 넘어 창의적이고 상세한 프롬프트를 자동으로 생성합니다.
- **🛡️ 안정적인 폴백 기능**: LLM API 호출에 실패하거나 API 키가 없어도, 내장된 번역기와 옵션 조합을 통해 즉시 안정적인 대체 프롬프트를 생성합니다. 워크플로우는 절대 멈추지 않습니다.
- **⚡ UI 멈춤 현상 완벽 해결**: 모든 네트워크 통신(LLM, 번역)을 비동기(Asynchronous)로 처리하여, 노드가 실행되는 동안 ComfyUI 캔버스가 멈추는 현상을 완전히 해결했습니다.
- **📑 구조화된 JSON 출력**: 고급 워크플로우 연동 및 데이터 분석을 위해, 모든 결과물을 체계적으로 정리된 JSON 형식으로 출력할 수 있습니다.
- **🔍 상세/요약 미리보기**: UI 멈춤을 유발할 수 있는 긴 프롬프트는 요약된 정보로 미리보고, 필요할 때만 전체 내용을 확인할 수 있는 `detailed_preview` 옵션을 제공하여 쾌적한 사용 환경을 보장합니다.
- **🌐 다국어 지원**: 영어뿐만 아니라 중국어(간체/번체)로도 프롬프트를 생성할 수 있습니다.
- **✍️ 상세한 로그**: 실행 시마다 최종 생성된 긍정/부정 프롬프트를 터미널에 출력하여, 디버깅 및 결과 확인이 매우 용이합니다.

### 📦 설치 방법

1.  터미널을 열고 ComfyUI의 `custom_nodes` 폴더로 이동합니다.
    ```bash
    cd path/to/your/ComfyUI/custom_nodes/
    ```
2.  이 저장소를 `git clone` 명령어로 복제합니다.
    ```bash
    git clone https://github.com/your-username/ComfyUI-Korean-Prompt-Enhancer.git
    ```
3.  **(매우 중요)** ComfyUI의 가상환경을 활성화합니다.
    ```bash
    # ComfyUI 설치 경로에 따라 다를 수 있습니다.
    source path/to/your/ComfyUI/.venv/bin/activate
    ```
4.  새로 복제된 폴더로 이동하여, 필요한 모든 라이브러리를 설치합니다.
    ```bash
    cd ComfyUI-Korean-Prompt-Enhancer/
    pip install -r requirements.txt
    ```
5.  ComfyUI를 완전히 재시작합니다.

### 🚀 사용 방법 (기본 워크플로우)

1.  ComfyUI 캔버스에서 마우스 우클릭 > `Add Node` > `Prompt Enhancement` > `Korean Prompt Enhancer (Final)`를 선택하여 노드를 추가합니다.
2.  필요한 노드들(`Load Checkpoint`, `KSampler` 등)을 배치합니다.
3.  아래와 같이 노드들을 연결합니다.
    - `enhanced_prompt` (첫 번째 출력) → `KSampler`의 `positive` 입력
    - `final_negative_prompt` (두 번째 출력) → `KSampler`의 `negative` 입력
4.  (선택 사항, 강력 추천) 디버깅 및 결과 확인을 위해 `Show Text` 노드를 추가하고, `preview_string` (네 번째 출력)을 `Show Text`의 `text` 입력에 연결합니다.

_(워크플로우 예시 이미지 링크)_

### 🔧 노드 입력 (Inputs)

| 이름                    | 타입    | 설명                                                                                                                                     |
| ----------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `korean_prompt`         | STRING  | 이미지로 만들고 싶은 아이디어를 한국어로 자유롭게 입력합니다.                                                                            |
| `detailed_preview`      | BOOLEAN | `True`로 설정하면 미리보기(네 번째 출력)에 전체 프롬프트/JSON을 표시합니다. (UI가 느려질 수 있음) **기본값(`False`) 사용을 권장합니다.** |
| `output_format`         | COMBO   | 출력 형식을 `JSON` 또는 `STRING`으로 선택합니다. 고급 워크플로우에는 JSON을 추천합니다.                                                  |
| `llm_provider`          | COMBO   | 사용할 LLM 서비스를 선택합니다. (Gemini, ChatGPT, Claude)                                                                                |
| `model_name`            | STRING  | 선택한 LLM 서비스에서 사용할 특정 모델의 이름을 입력합니다. (예: `gemini-pro`, `gpt-4-turbo`)                                            |
| `target_language`       | COMBO   | 프롬프트가 번역될 목표 언어를 선택합니다.                                                                                                |
| `style`, `ethnicity` 등 | COMBO   | 이미지의 스타일, 인물, 카메라, 조명 등 세부 요소를 선택합니다. 이 값들은 LLM 프롬프트 생성 시 핵심 키워드로 활용됩니다.                  |
| `negative_prompt`       | STRING  | 이미지에 나타나지 않았으면 하는 요소를 입력합니다.                                                                                       |
| `..._api_key`           | STRING  | 선택한 LLM 서비스의 API 키를 입력합니다. 비워두면 폴백 기능이 자동으로 활성화됩니다.                                                     |

### 📤 노드 출력 (Outputs)

| 이름                    | 타입   | 설명                                                                                                                                                                    |
| ----------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enhanced_prompt`       | STRING | **STRING 모드**: 최종 생성된 긍정 프롬프트 문자열입니다.<br>**JSON 모드**: 모든 정보(긍정/부정/메타데이터)가 포함된 전체 JSON 문자열입니다.                             |
| `final_negative_prompt` | STRING | **모든 모드에서 항상** 최종적으로 사용될 부정 프롬프트 문자열을 출력합니다.                                                                                             |
| `metadata`              | STRING | **STRING 모드**: 처리 상태(LLM 성공/폴백) 메시지입니다.<br>**JSON 모드**: 전체 JSON에서 `metadata` 객체 부분만 추출하여 포맷팅된 JSON 문자열입니다.                     |
| `preview_string`        | STRING | **`detailed_preview`가 `False`일 때**: UI 멈춤 방지를 위한 요약 정보입니다.<br>**`detailed_preview`가 `True`일 때**: `enhanced_prompt`와 동일한 전체 내용을 표시합니다. |

### 🤔 문제 해결 (Troubleshooting)

- **노드가 보이지 않거나 로딩에 실패하는 경우:**

  1.  ComfyUI를 실행한 터미널에 `ImportError`와 같은 오류가 있는지 확인하세요.
  2.  `custom_nodes` 폴더 내에 노드 폴더가 올바르게 위치해 있는지 확인하세요.
  3.  터미널에서 ComfyUI의 가상환경을 활성화하고, `pip install -r requirements.txt --upgrade --force-reinstall` 명령을 실행하여 모든 라이브러리를 강제로 재설치한 후 ComfyUI를 재시작하세요.

- **LLM이 이상한 답변을 하는 경우:**
  - API 키가 올바른지 확인하세요.
  - `model_name`이 정확한지 확인하세요.
  - LLM 서비스 자체의 일시적인 문제일 수 있습니다. 잠시 후 다시 시도해보세요.

---

## 🇬🇧 Korean Prompt Enhancer (English Version)

The `Korean Prompt Enhancer` is the ultimate prompt automation tool for ComfyUI users. This custom node takes your simple ideas in Korean and automatically translates and expands them into artistic, rich, and detailed image generation prompts using powerful LLMs like Gemini, ChatGPT, and Claude.

Don't worry about LLM connection failures. A stable fallback mechanism is built-in, ensuring your workflow never stops and consistently produces reliable results under any circumstances.

### ✨ Key Features

- **🤖 LLM-Powered Prompt Expansion**: Supports Gemini, ChatGPT, and Claude to automatically generate creative and detailed prompts that go beyond simple keywords.
- **🛡️ Stable Fallback Mechanism**: Even if the LLM API call fails or you don't have an API key, it instantly generates a stable alternative prompt using its built-in translator and option combiner. Your workflow will never be interrupted.
- **⚡ UI Freeze Completely Resolved**: All network communications (LLM, translation) are handled asynchronously, completely eliminating the UI freezing issue while the node is executing.
- **📑 Structured JSON Output**: For advanced workflows and data analysis, all results can be output in a systematically structured JSON format.
- **🔍 Detailed/Summary Preview**: A `detailed_preview` option is provided to prevent UI lag by showing a lightweight summary for long prompts, allowing you to view the full content only when needed.
- **🌐 Multi-language Support**: Prompts can be generated not only in English but also in Chinese (Simplified/Traditional).
- **✍️ Detailed Logging**: The final positive and negative prompts are printed to the terminal upon each execution, making debugging and result verification extremely easy.

### 📦 Installation

1.  Open a terminal and navigate to your ComfyUI `custom_nodes` directory.
    ```bash
    cd path/to/your/ComfyUI/custom_nodes/
    ```
2.  Clone this repository using `git clone`.
    ```bash
    git clone https://github.com/your-username/ComfyUI-Korean-Prompt-Enhancer.git
    ```
3.  **(VERY IMPORTANT)** Activate ComfyUI's virtual environment.
    ```bash
    # This may vary depending on your ComfyUI installation path.
    source path/to/your/ComfyUI/.venv/bin/activate
    ```
4.  Navigate into the newly cloned folder and install all required libraries.
    ```bash
    cd ComfyUI-Korean-Prompt-Enhancer/
    pip install -r requirements.txt
    ```
5.  Restart ComfyUI completely.

### 🚀 How to Use (Basic Workflow)

1.  On the ComfyUI canvas, right-click > `Add Node` > `Prompt Enhancement` > `Korean Prompt Enhancer (Final)` to add the node.
2.  Place other necessary nodes (e.g., `Load Checkpoint`, `KSampler`).
3.  Connect the nodes as follows:
    - `enhanced_prompt` (first output) → `KSampler`'s `positive` input
    - `final_negative_prompt` (second output) → `KSampler`'s `negative` input
4.  (Optional but highly recommended) For debugging and verification, add a `Show Text` node and connect the `preview_string` (fourth output) to the `Show Text` node's `text` input.

_(Link to workflow example image)_

### 🔧 Node Inputs

| Name                       | Type    | Description                                                                                                                              |
| -------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `korean_prompt`            | STRING  | Freely enter your idea for the image in Korean.                                                                                          |
| `detailed_preview`         | BOOLEAN | If `True`, the preview output will display the full prompt/JSON. (May cause UI lag) **Using the default (`False`) is recommended.**      |
| `output_format`            | COMBO   | Choose the output format as `JSON` or `STRING`. JSON is recommended for advanced workflows.                                              |
| `llm_provider`             | COMBO   | Select the LLM service to use (Gemini, ChatGPT, Claude).                                                                                 |
| `model_name`               | STRING  | Enter the specific model name for the selected LLM service (e.g., `gemini-pro`, `gpt-4-turbo`).                                          |
| `target_language`          | COMBO   | Select the target language for the prompt translation.                                                                                   |
| `style`, `ethnicity`, etc. | COMBO   | Select detailed elements like image style, subject, camera, and lighting. These values are used as key inputs for LLM prompt generation. |
| `negative_prompt`          | STRING  | Enter elements you do not want to appear in the image.                                                                                   |
| `..._api_key`              | STRING  | Enter the API key for the selected LLM service. If left blank, the fallback mechanism will be automatically activated.                   |

### 📤 Node Outputs

| Name                    | Type   | Description                                                                                                                                                                        |
| ----------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `enhanced_prompt`       | STRING | **STRING Mode**: The final generated positive prompt string.<br>**JSON Mode**: The full JSON string containing all information (positive/negative/metadata).                       |
| `final_negative_prompt` | STRING | **Always outputs** the final negative prompt string in all modes.                                                                                                                  |
| `metadata`              | STRING | **STRING Mode**: A status message (LLM success/fallback).<br>**JSON Mode**: A formatted JSON string containing only the `metadata` object extracted from the full JSON.            |
| `preview_string`        | STRING | **When `detailed_preview` is `False`**: A lightweight summary to prevent UI freeze.<br>**When `detailed_preview` is `True`**: Displays the same full content as `enhanced_prompt`. |

### 🤔 Troubleshooting

- **Node doesn't appear or fails to load:**

  1.  Check the ComfyUI terminal for any errors like `ImportError`.
  2.  Ensure the node folder is correctly placed inside the `custom_nodes` directory.
  3.  Activate the venv in your terminal, then run `pip install -r requirements.txt --upgrade --force-reinstall` to forcibly reinstall all libraries, and then restart ComfyUI.

- **The LLM gives a strange response:**
  - Verify that your API key is correct.
  - Check if the `model_name` is accurate.
  - It might be a temporary issue with the LLM service itself. Try again after a short while.
