# Grand Principles: System Entity Relationship Diagram (ERD)

This document serves as the **Constitution** of the Job Management System. It defines the Data Architecture, UX/UI Philosophy, and Technical Standards.

## 1. UX/UI Design Principles (The "Intuitive" Standard)
> "Users should never have to guess. The interface must be self-explanatory."

1.  **Zero Learning Curve**: No manuals required. Use familiar metaphors (e.g., Excel-like grids, Shopping Cart style selection).
2.  **Visual Feedback**: Every action (save, delete, calculate) must have an immediate visual response (toast, color change, animation).
3.  **Error Prevention**: Validate data *before* submission. Use sliders and dropdowns instead of free text where possible.
4.  **Contextual Help**: AI-driven tooltips appear only when needed, explaining *why* a task is important, not just *how* to do it.
5.  **Information Hierarchy**: Most important data (e.g., Total Score, Grade) is biggest and boldest. Secondary data is accessible on demand.

## 2. Data Architecture (ERD)
This diagram represents the **12-Module Architecture** of the Public Institution Job Management System.

```mermaid
erDiagram
    %% --- Core Domain ---
    Institution ||--|{ OrgUnit : "has"
    Institution ||--|{ User : "employs"
    OrgUnit ||--|{ User : "contains"
    OrgUnit ||--o| OrgUnit : "parent"

    %% --- Job Architecture ---
    JobGroup ||--|{ JobSeries : "contains"
    JobSeries ||--|{ JobPosition : "defines"
    JobPosition ||--|{ JobTask : "composed_of"
    JobPosition ||--|{ User : "assigned_to"
    
    %% --- Workload Analysis ---
    SurveyPeriod ||--|{ WorkloadEntry : "collects"
    User ||--|{ WorkloadEntry : "submits"
    JobTask ||--|{ WorkloadEntry : "measured_in"

    %% --- Job Evaluation (Phase 3) ---
    JobPosition ||--o| JobEvaluation : "evaluated"
    JobEvaluation ||--|{ JobEvaluationScore : "has_scores"
    User ||--o| JobEvaluationScore : "rated_by (Self/Peer/Boss)"
    
    %% --- HR Management (Phase 4) ---
    User ||--|{ PerformanceReview : "reviewed"
    User ||--|{ PromotionList : "listed_in"
    JobPosition ||--|{ JobDescription : "described_by"
    
    %% --- Training (Phase 4) ---
    JobSeries ||--|{ TrainingProgram : "requires"

    %% --- Entities ---
    Institution {
        string id PK
        string name
        enum category
    }
    OrgUnit {
        string id PK
        string name
        enum unit_type
        string mission
    }
    User {
        string id PK
        string name
        string email
    }
    JobGroup {
        string id PK
        string name "직군 (예: 행정직)"
    }
    JobSeries {
        string id PK
        string name "직렬 (예: 일반행정)"
    }
    JobPosition {
        string id PK
        string title "직무 (예: 예산담당)"
        enum grade
    }
    JobTask {
        string id PK
        string name "과업 (Atomic Task)"
        float ai_substitution "AI 대체율"
        float ai_augmentation "AI 보완율"
    }
    WorkloadEntry {
        string id PK
        float volume "빈도"
        float standard_time "시간"
        float fte "FTE"
    }
    JobEvaluation {
        string id PK
        float total_score
        enum grade "직무등급"
    }
    JobEvaluationScore {
        string id PK
        enum rater_type "본인/동료/상사/외부"
        float z_score "표준화 점수"
    }
    JobDescription {
        string id PK
        text summary
        text kpi_indicators
    }
    PerformanceReview {
        string id PK
        float total_score
        string grade "S/A/B/C/D"
    }
    PromotionList {
        string id PK
        int rank "서열"
        float total_points
    }
    TrainingProgram {
        string id PK
        string name
        string required_competency
    }
```
