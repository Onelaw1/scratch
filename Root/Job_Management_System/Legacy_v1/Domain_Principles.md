# 직무관리시스템 13대 도메인 설계 원칙 (Structured Domain Principles)

본 문서는 13개 핵심 구성요소의 설계 원칙을 **4단계 계층 구조(Layered Architecture)**로 구조화한 문서입니다.
**정부 가이드라인** 준수 및 **유사 기관 벤치마킹(HCROI/HCVA)**을 통한 객관적 생산성 분석을 포함합니다.

## 1. 원칙 구조도 (Principle Architecture)

```mermaid
graph TD
    %% Layer 1: Foundation
    subgraph L1 [Layer 1: Data Foundation (데이터 기틀)]
        P1[1. Atomic Task Unit<br/>(과업 원자성)]
        P2[2. Cascading Hierarchy<br/>(조직-직무 캐스케이딩)]
        P13[13. Behavioral Indicator<br/>(행동 지표)]
    end

    %% Layer 2: Logic Engine
    subgraph L2 [Layer 2: Quantification Engine (정량화 엔진)]
        P3[3. Top-Down & Comparative Productivity<br/>(탑다운 & 비교 생산성)]
        P6[6. Parametric Scoring<br/>(파라미터 채점)]
        P5[5. Org Design & Headcount<br/>(조직설계 및 정원)]
    end

    %% Layer 3: Application
    subgraph L3 [Layer 3: Dynamic Application (동적 활용)]
        P4[4. Future Job Design<br/>(미래 직무 설계)]
        P7[7. Live View<br/>(JD 라이브뷰)]
        P8[8. Data-Linked Appraisal<br/>(데이터 연동 평가)]
        P11[11. Algorithmic Ranking<br/>(알고리즘 랭킹)]
        P12[12. Competency-Gap Matching<br/>(역량 갭 매칭)]
    end

    %% Layer 4: Integration
    subgraph L4 [Layer 4: Holistic Management (통합 관리)]
        P9[9. Holistic Dashboard<br/>(통합 대시보드)]
        P10[10. Dual Proficiency Tracking<br/>(이원화 숙련도 관리)]
    end

    %% Dependencies
    P1 --> P3
    P2 --> P1
    P2 --> P5
    
    P3 --> P5
    P3 --> P4
    P5 --> P4
    
    P6 --> P11
    P13 --> P6
    P13 --> P12
    
    P8 --> P11
    P8 --> P12
    
    P7 --> P9
    P5 --> P9
    P11 --> P9
    
    P9 --> P10

    style L1 fill:#f0f9ff,stroke:#0ea5e9,stroke-width:2px
    style L2 fill:#f0fdf4,stroke:#22c55e,stroke-width:2px
    style L3 fill:#fff7ed,stroke:#f97316,stroke-width:2px
    style L4 fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px
```

---

## 2. 계층별 상세 원칙 (Detailed Principles by Layer)

### Layer 1. Data Foundation (데이터 기틀)
*   **1. 직무조사**: **Atomic Task Unit Principle (과업 단위 원자성)**
    *   모든 데이터의 근원은 '과업'이며, 쪼개질 수 없는 최소 단위로 관리한다.
*   **2. 직무분류**: **Cascading Hierarchy Principle (조직-직무 캐스케이딩)**
    *   **Org Structure**: `본부(HQ) -> 실(Office) -> 팀(Team) -> 주무(R&R)` 위계 구조.
    *   **Cascading**: 상위 조직 미션 -> 하위 조직 R&R -> 개인 과업으로 연결 (Past-Based).
    *   **Constraints**: 1 직무 ≤ 20 과업, 1 과업 ≤ 5 단위업무, 단위업무 ≥ 10시간.
*   **13. 역량모델링**: **Behavioral Indicator Principle (행동 지표)**
    *   역량은 추상적 개념이 아닌, 과업과 연결된 구체적 행동으로 정의한다.

### Layer 2. Quantification Engine (정량화 엔진)
*   **3. 업무량조사**: **Top-Down & Comparative Productivity Principle (탑다운 & 비교 생산성)**
    *   **Top-Down**: 부서장 부여 업무량 조사 병행 및 AHP 보정.
    *   **External Benchmarking**: 단순 사내 비교를 넘어, **유사 기관(규모, 예산, 정원)** 그룹과 생산성을 비교한다.
    *   **Key Metrics**:
        *   **HCROI (Human Capital ROI)**: `(매출 - (영업비용 - 인건비)) / 인건비`
        *   **HCVA (Human Capital Value Added)**: `(매출 - (영업비용 - 인건비)) / FTE`
    *   **Legal**: 주 52시간 한도 검증.
*   **6. 직무평가**: **Parametric Scoring Principle (파라미터 기반 채점)**
    *   평가 점수는 사전에 정의된 로직과 가중치에 의해 자동 계산된다.
*   **5. 정원산정**: **Org Design & Zero-Base Justification (조직설계 및 제로베이스 검증)**
    *   적정 인력(Required) vs 정원(Authorized) vs 현원(Current) 3중 Gap 분석 및 조직 개편 근거 마련.

### Layer 3. Dynamic Application (동적 활용)
*   **4. 직무재설계**: **Future Job Design Principle (미래 직무 설계)**
    *   과거 데이터(Past)와 미래 전략(To-Be) 직무 모델 병행 관리.
*   **7. 직무기술서**: **Live View Principle (라이브 뷰)**
    *   JD는 정적 문서가 아닌, DB 데이터를 실시간으로 조합한 뷰(View)이다.
*   **8. 인사평가**: **Data-Linked Appraisal Principle (데이터 연동 평가)**
    *   평가는 기억이 아닌, 축적된 업무 기록과 KPI 데이터에 기반한다.
*   **11. 승진관리**: **Algorithmic Ranking Principle (알고리즘 랭킹)**
    *   승진 서열은 투명한 수식에 의해 자동 산정된다.
*   **12. 교육관리**: **Competency-Gap Matching Principle (역량 갭 매칭)**
    *   요구 역량과 보유 역량의 차이(Gap)를 기반으로 교육을 추천한다.

### Layer 4. Holistic Management (통합 관리)
*   **9. 직무관리카드**: **Holistic Dashboard Principle (통합 대시보드)**
    *   직무의 모든 속성(분석, 평가, 인원 등)을 한 화면에서 통합 조회한다.
*   **10. 인사기록카드**: **Dual Proficiency Tracking Principle (이원화 숙련도 관리)**
    *   **Absolute Tenure**: 입사일 기준 절대 근속 연수.
    *   **Job Tenure**: 해당 직무 수행 기간(직무 전문성).
