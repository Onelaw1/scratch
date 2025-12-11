# 직무관리시스템 고도화 기획안 (Job Management System Renewal Plan)

## 1. 개요 (Overview)
본 기획안은 **정부의 직무중심 인사관리 가이드라인**을 준수하며, **13대 핵심 구성요소**를 완벽하게 구현하기 위한 설계 문서입니다.
"나노바나나" 구조도를 대체하여, 데이터베이스 중심의 견고한 아키텍처를 제안합니다.

## 2. 13대 핵심 구성요소별 설계 (Component Design)

### 1. 직무조사 (Job Analysis)
*   **핵심 원칙**: **"Atomic Task Unit & Bottom-Up"**
    *   현장의 데이터를 있는 그대로 수집하되, 표준 행동 동사(Action Verb)를 강제하여 정제된 데이터를 확보한다.
*   **DB 설계**:
    *   `JobSurvey`: 조사표 메타데이터 (기간, 대상).
    *   `SurveyResponse`: 개별 직원의 응답 (Raw Data).
    *   `TaskDictionary`: 표준화된 과업 사전 (Reference).

### 2. 직무분류 (Job Classification)
*   **핵심 원칙**: **"Cascading Hierarchy & Future Design"**
    *   **Cascading**: `본부(HQ) -> 실(Office) -> 팀(Team) -> 주무(R&R)`로 이어지는 미션 캐스케이딩 체계를 구축한다.
    *   **Future Design**: 과거 데이터 기반(Past-Based) 분류뿐만 아니라, 미래 전략에 따른 **To-Be 직무 모델**을 별도로 설계한다.
*   **DB 설계**:
    *   `OrgUnit`: `type` (HQ, Office, Team).
    *   `JobPosition`: `is_future_model` (Boolean) 플래그 추가.
    *   `CascadingLink`: 상위 조직 미션 <-> 하위 조직 R&R 매핑.

### 3. 업무량조사 (Workload Analysis)
*   **핵심 원칙**: **"Top-Down & Comparative Productivity"**
    *   **Top-Down**: 부서장 부여 업무량과 개인 입력 업무량을 교차 검증한다.
    *   **External Benchmarking**: 유사 기관(규모, 예산, 정원)과의 **HCROI**, **HCVA** 비교를 통해 객관적 생산성을 분석한다.
        *   **HCROI** = `(매출 - (영업비용 - 인건비)) / 인건비`
        *   **HCVA** = `(매출 - (영업비용 - 인건비)) / FTE`
*   **DB 설계**:
    *   `WorkloadEntry`: `User` + `Task` + `Volume` + `StandardTime` = `FTE`.
    *   `TeamBudget`: 팀별 연간 예산 및 매출 목표.
    *   `ExternalBenchmarkData`:
        *   `institution_type` (유형), `headcount_range` (정원규모), `budget_range` (예산규모).
        *   `avg_hcroi` (평균 HCROI), `avg_hcva` (평균 HCVA).

### 4. 직무재설계 (Job Redesign)
*   **핵심 원칙**: **"Dynamic Simulation"**
    *   FTE 분석 결과에 따라 과소/과다 업무를 재분배하고, 유사 중복 업무를 통폐합한다.
*   **DB 설계**:
    *   `JobChangeLog`: 직무 변경 이력 (Before/After).
    *   `RedesignSimulation`: 가상 조직도 및 업무 분장 시뮬레이션 결과.

### 5. 조직설계 및 정원 (Org Design & Headcount)
*   **핵심 원칙**: **"Appropriate Workforce & Zero-Base"**
    *   **Appropriate Workforce**: 적정 인력(Required) vs 정원(Authorized) vs 현원(Current)의 3중 Gap을 분석한다.
    *   **Org Design**: 분석된 적정 인력을 기반으로 팀 신설/통폐합 등 조직 개편안을 도출한다.
*   **DB 설계**:
    *   `HeadcountPlan`: 부서/직무별 `Required` / `Authorized` / `Current` 수치 관리.
    *   `OrgDesignProposal`: 조직 개편 시뮬레이션 안.

### 6. 직무평가 (Job Evaluation)
*   **핵심 원칙**: **"Parametric Scoring"**
    *   사전에 정의된 평가 요소(Factor)와 가중치(Weight)에 따라 시스템이 점수를 자동 계산한다.
*   **DB 설계**:
    *   `EvaluationFactor`: 평가 요소 (숙련도, 책임, 노력 등).
    *   `PointTable`: 요소별 레벨 점수표.
    *   `JobScore`: 직무별 평가 점수 및 등급(Grade).

### 7. 직무기술서작성 (Job Description Creation)
*   **핵심 원칙**: **"Live View"**
    *   직무조사 및 분석 데이터를 바탕으로 직무기술서(JD)를 실시간 뷰(View)로 제공한다.
*   **DB 설계**:
    *   `JobDescriptionTemplate`: JD 양식 템플릿.
    *   `GeneratedJD`: 버전 관리되는 JD 스냅샷.

### 8. 인사평가 (Performance Evaluation)
*   **핵심 원칙**: **"Data-Linked Appraisal"**
    *   직무별 핵심성과지표(KPI)와 필요 역량(Competency)을 기반으로 평가한다.
*   **DB 설계**:
    *   `KPI`: 직무별 성과 지표 라이브러리.
    *   `AppraisalResult`: 개인별 평가 결과.

### 9. 직무관리카드 (Job Management Card)
*   **핵심 원칙**: **"Holistic Dashboard"**
    *   해당 직무의 모든 속성(정의, 요건, 평가결과, 업무량 등)을 한눈에 보여주는 대시보드.
*   **DB 설계**:
    *   View(뷰) 형태로 구현: `Job` 테이블을 중심으로 관련 정보 Aggregation.

### 10. 인사기록카드 (Personnel Record Card)
*   **핵심 원칙**: **"Dual Proficiency Tracking"**
    *   **Absolute Tenure**: 입사일 기준 절대 근속 연수.
    *   **Job Tenure**: 해당 직무 수행 기간 (직무 전문성 지표).
*   **DB 설계**:
    *   `EmployeeHistory`: 부서 이동, 직무 변경 이력.
    *   `ProficiencyStats`: 개인별 `TotalYears` vs `JobYears` 집계.

### 11. 승진서열명부 (Promotion List)
*   **핵심 원칙**: **"Algorithmic Ranking"**
    *   근무평정, 경력, 가점 등을 합산하여 승진 서열을 투명하게 산정한다.
*   **DB 설계**:
    *   `PromotionCandidate`: 승진 대상자 풀.
    *   `PromotionScore`: 항목별 점수 및 총점, 순위.

### 12. 교육관리 설계 (Education Management)
*   **핵심 원칙**: **"Competency-Gap Matching"**
    *   직무 요구 역량과 개인 보유 역량의 차이(Gap)를 해소하기 위한 교육 과정을 매칭한다.
*   **DB 설계**:
    *   `TrainingCourse`: 교육 과정 정보.
    *   `IDP`: 개인별 역량 개발 계획.

### 13. 역량모델링 (Competency Modeling)
*   **핵심 원칙**: **"Behavioral Indicator"**
    *   역량은 추상적 개념이 아닌, 과업과 연결된 구체적 행동 지표로 정의한다.
*   **DB 설계**:
    *   `CompetencyDictionary`: 역량 사전.
    *   `BehaviorIndicator`: 역량별 행동 지표 (Task와 매핑).

## 3. 시스템 구조도 (System Structure Diagram)
*(별첨 `System_Architecture_Master.md` 참조)*

## 4. 추진 전략 (Implementation Strategy)
1.  **Phase 1 (Foundation)**: 직무조사, 분류(Cascading), 업무량(HCROI/HCVA), 직무평가.
2.  **Phase 2 (Expansion)**: 조직설계/정원, JD 자동화, 인사평가 연동.
3.  **Phase 3 (Integration)**: 승진, 교육, 이원화 숙련도 관리, 통합 대시보드.
