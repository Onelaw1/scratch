# 직무관리시스템 설계 15대 대원칙 (15 Design Principles of Job Management System)

본 문서는 프로젝트 가이드라인(`project_guidelines.md`)과 시스템 소스코드(`Job_Management_System`)에 분산되어 있던 설계 원칙을 통합하여 복원한 것입니다.

## A. 핵심 대원칙 (The 5 Pillars)
*프로젝트의 기술적, 미학적 기반이 되는 5가지 절대 원칙*

1.  **MCP-First Architecture (MCP 활용 극대화)**
    *   모든 외부 도구 및 라이브러리 사용은 `context7`과 `memory` 서버를 통해 검증되고 관리되어야 한다.
    *   추측이 아닌 검증된 데이터(Verified Data)만을 사용한다.

2.  **Apple-Style Aesthetics (애플 스타일 미학)**
    *   단순한 기능 구현을 넘어, 사용자에게 시각적 감동을 주는 디자인을 추구한다.
    *   Glassmorphism, San Francisco Typography, Diffuse Shadows를 표준으로 한다.

3.  **Lightning Fast Backend (빠르고 간결한 백엔드)**
    *   FastAPI의 비동기(Async) 처리를 통해 즉각적인 응답 속도를 보장한다.
    *   불필요한 레이어를 제거한 Lean Architecture를 지향한다.

4.  **Advanced Prompting Engineering (고급 프롬프팅 기법)**
    *   상황에 맞는 동적 페르소나(Dynamic Persona)를 스위칭하여 최적의 해답을 도출한다.
    *   복잡한 문제는 CoT(Chain of Thought)를 통해 논리적 오류를 방지한다.

5.  **Continuous Intelligence (연속적 지능)**
    *   세션이 종료되어도 프로젝트의 맥락(Context)은 영구적으로 보존된다.
    *   사용자의 피드백을 즉시 학습하여 시스템을 진화시킨다.

## B. 도메인 설계 원칙 (Domain Design Principles)
*직무관리시스템의 논리적 구조와 데이터 무결성을 보장하는 4가지 원칙*

6.  **직무 분석 고도화 (Job Analysis Enhancement)**
    *   **Rule of 30**: 하나의 직무는 30개 이상의 과업(Task)을 가질 수 없다. (입도 관리)
    *   **Action Verb**: 모든 과업은 표준화된 행동 동사로 정의되어야 한다.

7.  **직무 분류 체계화 (Job Classification Enhancement)**
    *   **NCS Mapping**: 모든 직무는 국가직무능력표준(NCS)과 1:1 또는 1:N으로 매핑되어야 한다.
    *   표준화된 분류 체계를 통해 데이터의 호환성을 확보한다.

8.  **적정 업무량 분석 (Workload Analysis Enhancement)**
    *   **FTE Calculation**: 주관적 설문이 아닌, `표준시간(Standard Time) x 물량(Volume)` 공식을 통해 객관적인 FTE를 산출한다.
    *   데이터 기반의 인력 산정 근거를 마련한다.

9.  **직무 평가 객관화 (Job Evaluation Enhancement)**
    *   **Point Table**: 사전에 정의된 점수표(Point Table)에 의거하여 직무 가치를 정량적으로 평가한다.
    *   평가 결과는 보상 및 승진 체계와 연동될 수 있어야 한다.

## C. 수행 및 운영 원칙 (Operational Principles)
*성공적인 프로젝트 수행과 품질 보증을 위한 6가지 행동 강령*

10. **시각적 검증 우선 (Visual Verification First)**
    *   사용자에게 "파일을 확인해보세요"라고 말하지 않는다.
    *   반드시 스크린샷, 인용구, 다이어그램 등을 통해 결과물을 **직접 보여준다.**

11. **MCP 도구 효율성 (Tool Efficiency)**
    *   대규모 파일 조작 시 `multi_replace`, `grep_search` 등을 활용하여 토큰을 절약한다.
    *   무작위적인 파일 읽기를 지양하고, 검색을 통해 필요한 정보만 취득한다.

12. **코딩 표준 준수 (Coding Standards)**
    *   Backend는 Python(PEP 8), Frontend는 JS/HTML(Prettier) 표준을 준수한다.
    *   복잡한 비즈니스 로직에는 반드시 **한글 주석**을 작성하여 유지보수성을 높인다.

13. **지속적 혁신 (Continuous Innovation)**
    *   단순한 차트(Chart)를 넘어, 구조화된 다이어그램과 시각화 도구를 통해 **"컨설팅 장표의 본질"**을 구현한다.
    *   매일 새로운 시각화 기술을 탐색하고 적용한다.

14. **체계적 문제 해결 (Systematic Breakdown)**
    *   문제 발생 시 증상(Symptom)에서 원인(Root Cause)으로 논리적으로 접근한다.
    *   문제를 최소 단위로 분해(Breakdown)하여 하나씩 검증하고 해결한다.

15. **증거 기반 정반합 (Evidence-Based Dialectic)**
    *   **Thesis(계획) -> Antithesis(비평) -> Synthesis(검증된 전략)**의 루프를 통해 의사결정의 품질을 높인다.
    *   단순한 주장이 아닌, 데이터와 규정에 근거한 전략만을 채택한다.
