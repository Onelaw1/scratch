# 프로젝트 인사이트 및 대원칙 (System 2.0 헌법)

이 문서는 직무관리시스템의 이전 개발 과정에서 얻은 핵심 교훈과 "대원칙"을 통합한 문서입니다. 이는 "System 2.0" 재구축을 위한 불변의 기틀(Constitution) 역할을 합니다.

## 1. UX/UI 및 미학 원칙 ("애플 스탠다드")
*   **Visual First (시각화 우선)**: "설명하지 말고 보여주라." 텍스트보다는 스크린샷, 다이어그램, 라이브 데모를 우선한다.
*   **Premium Aesthetics (프리미엄 미학)**: 글래스모피즘(Glassmorphism), 정제된 HSL 컬러 팔레트, 현대적인 타이포그래피(Inter/Roboto)를 사용한다. "기본 부트스트랩" 느낌을 지양한다.
*   **Zero Learning Curve (학습 곡선 제로)**: 인터페이스는 설명서 없이도 이해되어야 한다. 익숙한 메타포(엑셀 그리드, 쇼핑카트 등)를 활용한다.
*   **Live Feedback (즉각적 피드백)**: 모든 사용자의 행동에는 즉각적인 시각적 확인(토스트 메시지, 애니메이션, 상태 변화)이 따라야 한다.

## 2. 기술 아키텍처 원칙
*   **MCP-First (MCP 우선)**: 모든 데이터 검증 및 외부 도구 제어는 MCP(Model Context Protocol)를 통해 수행한다. 추측을 배제한다.
*   **Lightning Backend (초고속 백엔드)**: FastAPI와 비동기(Async) 처리는 필수다. 불필요한 레이어를 제거한 "린(Lean) 아키텍처"를 지향한다.
*   **Continuous Intelligence (연속적 지능)**: 세션 간 맥락을 보존하며, 사용자의 피드백을 즉시 학습하여 시스템에 반영한다.
*   **Korean Native (한국어 네이티브)**: 모든 비즈니스 로직 주석과 사용자 인터페이스 텍스트는 자연스럽고 전문적인 한국어로 작성한다.

## 3. 핵심 도메인 원칙 (13대 기둥)
### Layer 1: 데이터 파운데이션 (Data Foundation)
*   **Atomic Task Unit (과업의 원자성)**: "과업(Task)"은 더 이상 쪼갤 수 없는 데이터의 최소 단위이다.
*   **Cascading Hierarchy (위계적 연결)**: 미션 -> R&R -> 과업으로 이어지는 논리적 흐름이 있어야 한다.
*   **Behavioral Indicators (행동 지표)**: 역량은 추상적 용어가 아닌, 관찰 가능한 행동으로 정의되어야 한다.

### Layer 2: 정량화 엔진 (Quantification Engine)
*   **Objective Workload (객관적 업무량)**: `표준시간 x 물량 = FTE`. 주관적인 "바쁨"의 느낌이 아닌 데이터로 산출한다.
*   **Comparative Analysis (비교 분석)**: 단순히 내부 과거 데이터가 아닌, 유사 규모/예산/미션을 가진 외부 기관과 비교한다.
*   **Parametric Scoring (파라미터 채점)**: 직무 평가 점수는 수기 입력이 아닌 검증된 알고리즘에 의해 계산된다.

### Layer 3: 동적 애플리케이션 (Dynamic Application)
*   **Live JD (살아있는 직무기술서)**: JD는 정적 파일이 아닌, 현재 DB 상태를 보여주는 동적 뷰(View)이다.
*   **Data-Linked Appraisal (데이터 연동 평가)**: 인사평가는 구체적인 과업 데이터와 KPI 기록을 근거로 해야 한다.

### Layer 4: 통합 관리 (Holistic Management)
*   **Dual Proficiency (이원화된 숙련도)**: "절대 근속(입사 기간)"과 "직무 근속(해당 직무 수행 기간)"을 분리하여 관리한다.
*   **Holistic Dashboard (통합 대시보드)**: 9-Box, 업무량, 역량을 단일 화면에서 통합적으로 조망한다.

## 4. 운영 대원칙 (Operational Principles)
*   **Evidence-Based Dialectic (증거 기반 정반합)**: 정(계획) -> 반(비평) -> 합(해결책)의 과정을 거친다.
*   **Systematic Breakdown (체계적 분해)**: 문제는 증상(Symptom)에서 근본 원인(Root Cause)으로 파고든다.
*   **Tool Efficiency (도구 효율성)**: `grep`, `find`, `multi_replace` 등을 사용하여 토큰을 절약하고 정밀하게 작업한다.

## 5. 심층 회고 및 피드백 분석 (Deep Feedback Analysis)
*> 사용자의 불만족 사항(Pain Points)을 철저히 분석하여 도출한 '행동 교정 강령'입니다.*

### A. "코드 블라인드" 현상 타파 (No More Code Blindness)
*   **지적사항**: "파일을 확인해보세요"라는 말은 무책임하다. 사용자는 에이전트가 무슨 짓을 했는지 모른 채 결과를 떠안아야 했다.
*   **교정 강령**: **Visual Evidence Mandatory (시각적 증거 필수).** 코드를 수정했다면, 무엇이 바뀌었는지 `diff`나 결과를 반드시 출력하여 보여준다. 사용자가 "확인"하게 하지 말고, 내가 "증명"한다.

### B. "한국어 패치"가 아닌 "한국어 네이티브" (Embedded Localization)
*   **지적사항**: UI는 한국어인데 에러 메시지나 로직 설명이 영어로 나오거나, 번역투의 어색한 표현이 몰입을 깸.
*   **교정 강령**: **Korean Context (한국어 맥락화).** 단순 번역이 아니라, 한국의 조직 문화(직군, 직렬, 호봉 등)를 이해하고 그에 맞는 용어를 코드 레벨에서부터 사용한다.

### C. "유령 의존성" 제거 (Eliminate Ghost Dependencies)
*   **지적사항**: `import` 에러. "내 컴퓨터에선 되는데" 식의 코드는 사용자의 신뢰를 가장 크게 깎아먹는 요인.
*   **교정 강령**: **Self-Contained Execution (자체 완결적 실행).** 스크립트는 실행 시 자신의 위치를 스스로 파악(`pathlib` 활용)하고, `sys.path`를 동적으로 연결해야 한다. 루트 디렉토리에 대한 가정을 코드에 하드코딩하지 않는다.

### D. "심미적 완성도"는 기능의 일부다 (Aesthetics IS Function)
*   **지적사항**: "대충 플레이스홀더로 채우지 마라." 디자인이 조악하면 기능이 아무리 좋아도 사용해보고 싶지 않다.
*   **교정 강령**: **No Placeholder (빈칸 금지).** 이미지가 필요하면 생성하고, 텍스트가 필요하면 그럴드한 더미 데이터를 채워 넣는다. 미완성된 느낌을 사용자에게 전달하지 않는다.

### E. "맥락 단절" 거부 (Reject Context Loss)
*   **지적사항**: 이전 대화에서 지적한 내용을 까먹고 똑같은 실수를 반복함.
*   **교정 강령**: **Persistent Memory (영속적 기억).** 작업을 시작하기 전에 반드시 이 문서를 다시 읽고(Review), 이전 실수를 반복하지 않겠다는 다짐(Commitment)을 한 뒤 코드를 짠다.
