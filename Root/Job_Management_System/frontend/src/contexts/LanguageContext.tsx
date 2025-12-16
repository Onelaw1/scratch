"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Language = 'ko' | 'en';

interface LanguageContextType {
    language: Language;
    toggleLanguage: () => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

// Simple dictionary for immediate needs
const dictionary: Record<string, Record<Language, string>> = {
    // Navigation
    'nav.dashboard': { ko: '대시보드', en: 'Dashboard' },
    'nav.org_jobs': { ko: '조직 & 직무', en: 'Organization & Jobs' },
    'nav.workforce': { ko: '인력 & 분석', en: 'Workforce & Analysis' },
    'nav.personnel': { ko: '인사 & 경력', en: 'Personnel & Career' },
    'nav.ai_brain': { ko: 'AI 인텔리전스', en: 'AI Intelligence (Brain)' },
    'nav.emp_exp': { ko: '직원 경험', en: 'Employee Experience' },
    'nav.admin': { ko: '엔터프라이즈 관리', en: 'Enterprise Admin' },
    'nav.overview': { ko: '시스템 개요', en: 'System Overview' },
    'nav.workflow': { ko: '직무 관리 흐름', en: 'Job Management Workflow' },
    'nav.workload': { ko: '적정 인력', en: 'Workload Analysis' },
    'nav.analytics': { ko: '분석 및 최적화', en: 'Analytics & Optimization' },
    'nav.strat_dash': { ko: '전략 대시보드', en: 'Strategy Dashboard' },
    'nav.pred': { ko: '예측 분석', en: 'Predictive Analytics' },
    'nav.permissions': { ko: '사용자 권한 관리', en: 'User Permissions' },

    // 9-Box Grid
    'ninebox.title': { ko: '9-Box 인재 매트릭스', en: '9-Box Talent Matrix' },
    'ninebox.subtitle': { ko: '성과와 잠재력 기반의 과학적 인재 매핑', en: 'Scientific Talent Mapping based on Performance & Potential' },
    'ninebox.total': { ko: '총 인원', en: 'Total Employees' },
    'ninebox.box.star': { ko: '스타 (핵심인재)', en: 'Star' },
    'ninebox.box.high_pot': { ko: '고잠재력자', en: 'High Potential' },
    'ninebox.box.enigma': { ko: '물음표 (잠재력)', en: 'Enigma' },
    'ninebox.box.high_perf': { ko: '고성과자', en: 'High Performer' },
    'ninebox.box.core': { ko: '핵심 플레이어', en: 'Core Player' },
    'ninebox.box.inconsistent': { ko: '불규칙 성과', en: 'Inconsistent' },
    'ninebox.box.trusted': { ko: '숙련 전문가', en: 'Trusted Pro' },
    'ninebox.box.effective': { ko: '유효 인력', en: 'Effective' },
    'ninebox.box.risk': { ko: '관리 대상 (리스크)', en: 'Risk / Exit' },
    'ninebox.legend.star': { ko: '스타: 승진 최우선 대상', en: 'Star: Priority for Promotion' },
    'ninebox.legend.enigma': { ko: '물음표: 직무 적합도 재검토/코칭', en: 'Enigma: Assess Fit / Coaching' },
    'ninebox.legend.trusted': { ko: '숙련자: 유지 관리 필수', en: 'Trusted: Retention Critical' },

    // Span of Control
    'span.title': { ko: '통솔범위(Span of Control) 분석', en: 'Span of Control Analyzer' },
    'span.subtitle': { ko: '조직 효율성 및 보고 계층(Layer) 심층 분석', en: 'Organizational Efficiency & Hierarchy Depth Analysis' },
    'span.metric.avg_span': { ko: '평균 통솔범위', en: 'Avg. Span of Control' },
    'span.metric.max_layers': { ko: '최대 조직 계층', en: 'Max Org Layers' },
    'span.metric.bottlenecks': { ko: '병목 구간 경고', en: 'Bottleneck Alerts' },
    'span.target': { ko: '목표', en: 'Target' },
    'span.unit.managers': { ko: '명 (문제 관리자)', en: 'Managers with issues' },
    'span.alerts_title': { ko: '구조적 문제 감지', en: 'Structural Alerts' },
    'span.table.title': { ko: '관리자 리포트', en: 'Manager Report' },
    'span.table.name': { ko: '이름', en: 'Name' },
    'span.table.role': { ko: '역할', en: 'Role' },
    'span.table.depth': { ko: '계층(Depth)', en: 'Org Depth' },
    'span.table.span': { ko: '직속 보고', en: 'Span (Reports)' },
    'span.table.status': { ko: '상태', en: 'Status' },
    'span.status.wide': { ko: '과부하', en: 'Wide (Bottleneck)' },
    'span.status.narrow': { ko: '비효율', en: 'Narrow (Micro-mgmt)' },
    'span.status.optimal': { ko: '최적', en: 'Optimal' },
    'span.status.ic': { ko: '실무자', en: 'Individual Contributor' },

    // Competency Radar
    'comp.title': { ko: '역량 적합도(Competency Fit) 분석', en: 'Competency Fit Radar' },
    'comp.subtitle': { ko: '직무 요구 역량 vs 개인 보유 역량 비교 분석 (NCS 기반)', en: 'Job-Person Fit Analysis (NCS Based)' },
    'comp.fit_score': { ko: '적합도 점수', en: 'Fit Score' },
    'comp.select_user': { ko: '분석 대상 직원 선택', en: 'Select Employee' },
    'comp.gaps_title': { ko: '역량 Gap (교육 훈련 필요)', en: 'Gaps & Training Needs' },
    'comp.strengths_title': { ko: '강점 (멘토링 활용)', en: 'Strengths' },
    'comp.no_gaps': { ko: '주요 역량 Gap이 발견되지 않았습니다.', en: 'No significant gaps found.' },
    'comp.no_strengths': { ko: '특이 강점이 식별되지 않았습니다.', en: 'No specific strengths identified.' },
    'comp.issues_count': { ko: '건 (보완 필요)', en: 'Issues' },
    'comp.areas_count': { ko: '개 영역', en: 'Areas' },
    'comp.chart.required': { ko: '요구 수준', en: 'Required' },
    'comp.chart.actual': { ko: '보유 수준', en: 'Actual' },

    // Navigation - Submenus
    'nav.job_class': { ko: '직무 분류', en: 'Job Classification' },
    'nav.job_desc': { ko: '직무 기술서', en: 'Job Descriptions' },
    'nav.job_eval': { ko: '직무 평가', en: 'Job Evaluation' },
    'nav.span': { ko: '조직도 (통솔범위)', en: 'Org Chart (Span)' },
    'nav.wf_planning': { ko: '인력 계획', en: 'Workforce Planning' },
    'nav.wl_analysis': { ko: '업무량 분석', en: 'Workload Analysis' },
    'nav.sim_board': { ko: '시뮬레이션 보드', en: 'Simulation Board' },
    'nav.personnel_rec': { ko: '인사 기록', en: 'Personnel Records' },
    'nav.perf_mgmt': { ko: '성과 관리', en: 'Performance Mgmt' },
    'nav.career_dev': { ko: '경력 개발', en: 'Career Development' },
    'nav.talent_map': { ko: '인재 매핑 (9-Box)', en: 'Talent Mapping (9-Box)' },
    'nav.comp_radar': { ko: '역량 레이더', en: 'Competency Radar' },
    'nav.ai_search': { ko: 'AI 의미 기반 검색', en: 'AI Semantic Search' },
    'nav.jd_gen': { ko: 'JD 생성기', en: 'JD Generator' },
    'nav.gap_analysis': { ko: '스마트 갭 분석', en: 'Smart Gap Analysis' },
    'nav.pred_analytics': { ko: '예측 분석', en: 'Predictive Analytics' },
    'nav.my_job': { ko: '내 직무 (모바일)', en: 'My Job (Mobile)' },
    'nav.job_survey': { ko: '직무 조사 (입력)', en: 'Job Survey (Input)' },
    'nav.erp_sync': { ko: 'ERP 동기화', en: 'ERP Sync' },

    // Productivity Dashboard
    'prod.title': { ko: '전략적 HR 시뮬레이션', en: 'Strategic HR Simulation' },
    'prod.subtitle': { ko: '생산성 분석 및 직무 재설계', en: 'Analyze Productivity & Redesign Job Architecture' },
    'prod.new_scenario': { ko: '새 시뮬레이션', en: 'New Scenario' },
    'prod.overview_title': { ko: '생산성 개요 (HCROI & HCVA)', en: 'Productivity Overview (HCROI & HCVA)' },
    'prod.overview_desc': { ko: '인적 자본 투자 대비 재무 성과', en: 'Financial performance relative to human capital investment.' },
    'prod.hcroi_label': { ko: 'HCROI (인적자본 ROI)', en: 'HCROI (RETURN ON INVESTMENT)' },
    'prod.hcroi_desc': { ko: '인건비 $1 투자 창출 가치', en: 'Value created per $1 spent on workforce.' },
    'prod.hcva_label': { ko: 'HCVA (인적자본 부가가치)', en: 'HCVA (VALUE ADDED)' },
    'prod.hcva_desc': { ko: 'FTE 1인당 순부가가치', en: 'Net value added per full-time employee.' },
    'prod.trends': { ko: '생산성 추세', en: 'Productivity Trends' },
    'prod.scenarios': { ko: '시뮬레이션 시나리오', en: 'Simulation Scenarios' },
    'prod.no_scenarios': { ko: '시나리오가 없습니다. 새로운 시나리오를 생성하여 설계를 시작하세요.', en: 'No scenarios yet. Create one to start designing.' },

    // Personnel Record
    'personnel.title': { ko: '인사 기록', en: 'Personnel Record' },
    'personnel.subtitle': { ko: '이원화된 근속연수 관리 (직무 vs 조직)', en: 'Dual Tenure Management (Job vs Organization)' },
    'personnel.search_placeholder': { ko: '직원 검색', en: 'Search Employee' },
    'personnel.org_tenure': { ko: '조직 근속연수 (로열티)', en: 'Organization Tenure (Loyalty)' },
    'personnel.job_tenure': { ko: '직무 근속연수 (전문성)', en: 'Job Tenure (Expertise)' },
    'personnel.set_date': { ko: '직무 배치일 설정', en: 'Set Assignment Date' },
    'personnel.spec_ratio': { ko: '전문성 비율', en: 'Specialization Ratio' },
    'personnel.high_spec': { ko: '높은 전문성. 일관된 경력 경로.', en: 'High specialization. Consistent career path.' },
    'personnel.low_spec': { ko: '낮은 전문성. 잦은 순환 근무 감지.', en: 'Low specialization. Frequent rotations detected.' },
    'personnel.sme_candidate': { ko: 'SME (직무 전문가) 후보', en: 'Subject Matter Expert (SME)' },
    'personnel.full_time': { ko: '정규직', en: 'Full Time' },
};

export function LanguageProvider({ children }: { children: ReactNode }) {
    const [language, setLanguage] = useState<Language>('ko'); // Default to Korean

    const toggleLanguage = () => {
        setLanguage(prev => prev === 'ko' ? 'en' : 'ko');
    };

    const t = (key: string) => {
        const item = dictionary[key];
        if (!item) return key;
        return item[language];
    };

    return (
        <LanguageContext.Provider value={{ language, toggleLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
}

export function useLanguage() {
    const context = useContext(LanguageContext);
    if (!context) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
}
