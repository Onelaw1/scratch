const API_BASE_URL = "http://localhost:8000";

export interface JobHierarchyNode {
    id: string;
    name: string;
    type: "GROUP" | "SERIES" | "POSITION" | "TASK" | "WORK_ITEM";
    children?: JobHierarchyNode[];
    [key: string]: any;
}

export interface JobMatrixItem {
    group_name: string;
    series_name: string;
    position_title: string;
    position_grade?: string;
    task_name: string;
    work_item_name?: string;
    frequency?: string;
    workload?: number;
}

export interface FinancialPerformance {
    year: number;
    revenue: number;
    operating_expenses: number;
    personnel_costs: number;
    net_income: number;
    institution_id: string;
}

export interface ProductivityMetric {
    year: number;
    revenue: number;
    operating_expenses: number;
    personnel_costs: number;
    net_income: number;
    fte: number;
    hcroi: number;
    hcva: number;
}

export const api = {
    // --- Job Tasks (Auto-Complete) ---
    getJobTasks: async () => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/job-tasks/`);
        if (!res.ok) throw new Error("Failed to fetch job tasks");
        return res.json();
    },

    createJobTask: async (data: { task_name: string; position_id: string; action_verb?: string }) => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/job-tasks/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to create job task");
        return res.json();
    },

    // --- Job Positions ---
    getJobPositions: async () => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/job-positions/`);
        if (!res.ok) throw new Error("Failed to fetch job positions");
        return res.json();
    },

    // --- Users ---
    getUsers: async () => {
        const res = await fetch(`${API_BASE_URL}/users/`);
        if (!res.ok) throw new Error("Failed to fetch users");
        return res.json();
    },

    // --- Workload Entries (Grid Data) ---
    getWorkloadEntries: async () => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/workload-entries/`);
        if (!res.ok) throw new Error("Failed to fetch workload entries");
        return res.json();
    },

    saveWorkloadEntry: async (data: {
        user_id: string;
        task_id: string;
        volume: number;
        standard_time: number;
    }) => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/workload-entries/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to save workload entry");
        return res.json();
    },

    // --- Job Classification ---
    getJobHierarchy: async (): Promise<JobHierarchyNode[]> => {
        const res = await fetch(`${API_BASE_URL}/classification/hierarchy`);
        if (!res.ok) throw new Error("Failed to fetch job hierarchy");
        return res.json();
    },

    getJobMatrix: async (): Promise<JobMatrixItem[]> => {
        const res = await fetch(`${API_BASE_URL}/classification/matrix`);
        if (!res.ok) throw new Error("Failed to fetch job matrix");
        return res.json();
    },

    saveJobMatrix: async (items: JobMatrixItem[]) => {
        const res = await fetch(`${API_BASE_URL}/classification/matrix`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(items),
        });
        if (!res.ok) throw new Error("Failed to save job matrix");
        return res.json();
    },

    // --- Analysis ---
    getFteByOrg: async (): Promise<{ name: string, fte: number }[]> => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/analysis/fte-by-org`);
        if (!res.ok) throw new Error("Failed to fetch FTE by Org");
        return res.json();
    },

    getFteByPosition: async (): Promise<{ name: string, fte: number }[]> => {
        const res = await fetch(`${API_BASE_URL}/job-analysis/analysis/fte-by-position`);
        if (!res.ok) throw new Error("Failed to fetch FTE by Position");
        return res.json();
    },

    // --- Institutions ---
    getInstitutions: async () => {
        const res = await fetch(`${API_BASE_URL}/institutions/`);
        if (!res.ok) throw new Error("Failed to fetch institutions");
        return res.json();
    },

    // --- Productivity ---
    saveFinancialPerformance: async (data: Omit<FinancialPerformance, 'net_income'>) => {
        const res = await fetch(`${API_BASE_URL}/productivity/financial-performance`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to save financial performance");
        return res.json();
    },

    getFinancialPerformance: async (institution_id: string): Promise<FinancialPerformance[]> => {
        const res = await fetch(`${API_BASE_URL}/productivity/financial-performance/${institution_id}`);
        if (!res.ok) throw new Error("Failed to fetch financial performance");
        return res.json();
    },

    getProductivityMetrics: async (institution_id: string): Promise<ProductivityMetric[]> => {
        const res = await fetch(`${API_BASE_URL}/productivity/metrics/${institution_id}`);
        if (!res.ok) throw new Error("Failed to fetch productivity metrics");
        return res.json();
    },
    // --- Job Evaluation ---
    getEvaluationPositions: async (): Promise<any[]> => {
        const res = await fetch(`${API_BASE_URL}/evaluations/positions/status`);
        if (!res.ok) throw new Error("Failed to fetch evaluation positions");
        return res.json();
    },

    createEvaluation: async (positionId: string) => {
        const res = await fetch(`${API_BASE_URL}/evaluations/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_position_id: positionId }),
        });
        if (!res.ok) throw new Error("Failed to create evaluation");
        return res.json();
    },

    saveEvaluationScore: async (data: {
        evaluation_id: string;
        rater_type: string;
        score_expertise: number;
        score_responsibility: number;
        score_complexity: number;
        rater_user_id?: string;
    }) => {
        const res = await fetch(`${API_BASE_URL}/evaluations/${data.evaluation_id}/scores`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to save evaluation score");
        return res.json();
    },

    calculateEvaluationResult: async (evaluationId: string) => {
        const res = await fetch(`${API_BASE_URL}/evaluations/${evaluationId}/calculate`, {
            method: "POST",
        });
        if (!res.ok) throw new Error("Failed to calculate evaluation");
        return res.json();
    },
    // --- Simulation ---
    getScenarios: async (): Promise<any[]> => {
        const res = await fetch(`${API_BASE_URL}/scenarios/`);
        if (!res.ok) throw new Error("Failed to fetch scenarios");
        return res.json();
    },

    createScenario: async (name: string, description?: string) => {
        const res = await fetch(`${API_BASE_URL}/scenarios/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description }),
        });
        if (!res.ok) throw new Error("Failed to create scenario");
        return res.json();
    },

    cloneScenario: async (scenarioId: string) => {
        const res = await fetch(`${API_BASE_URL}/scenarios/${scenarioId}/clone`, {
            method: "POST",
        });
        if (!res.ok) throw new Error("Failed to clone scenario");
        return res.json();
    },

    getScenarioPositions: async (scenarioId: string): Promise<any[]> => {
        const res = await fetch(`${API_BASE_URL}/scenarios/${scenarioId}/positions`);
        if (!res.ok) throw new Error("Failed to fetch scenario positions");
        return res.json();
    },

    moveTask: async (taskId: string, targetPositionId: string) => {
        const res = await fetch(`${API_BASE_URL}/scenarios/move-task`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task_id: taskId, target_position_id: targetPositionId }),
        });
        if (!res.ok) throw new Error("Failed to move task");
        return res.json();
    },
    // --- Workforce Gap Analysis ---
    getGapAnalysis: async (): Promise<any[]> => {
        const res = await fetch(`${API_BASE_URL}/workforce/gap-analysis`);
        if (!res.ok) throw new Error("Failed to fetch gap analysis");
        return res.json();
    },

    saveHeadcountPlan: async (data: { institution_id: string; org_unit_id: string; year: number; authorized_count: number }) => {
        const res = await fetch(`${API_BASE_URL}/workforce/headcount-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to save headcount plan");
        return res.json();
    },
    // --- Job Description ---
    getJobDescription: async (positionId: string) => {
        const res = await fetch(`${API_BASE_URL}/descriptions/${positionId}`);
        if (!res.ok) throw new Error("Failed to fetch job description");
        return res.json();
    },

    saveJobDescription: async (positionId: string, data: { summary: string; qualification_requirements: string; kpi_indicators: string }) => {
        const res = await fetch(`${API_BASE_URL}/descriptions/${positionId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error("Failed to save job description");
        return res.json();
    },
    // --- Performance Management ---
    createReview: async (userId: string, year: number) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/reviews`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, year }),
        });
        if (!res.ok) throw new Error("Failed to create review");
        return res.json();
    },

    getReview: async (userId: string, year: number) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/reviews/${userId}/${year}`);
        if (!res.ok && res.status !== 404) throw new Error("Failed to fetch review");
        return res.ok ? res.json() : null;
    },

    addGoal: async (reviewId: string, goal: any) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/reviews/${reviewId}/goals`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(goal),
        });
        if (!res.ok) throw new Error("Failed to add goal");
        return res.json();
    },

    updateGoal: async (goalId: string, update: any) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/goals/${goalId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(update),
        });
        if (!res.ok) throw new Error("Failed to update goal");
        return res.json();
    },

    calculateReview: async (reviewId: string) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/reviews/${reviewId}/calculate`, {
            method: "POST",
        });
        if (!res.ok) throw new Error("Failed to calculate review");
        return res.json();
    },

    getGoalSuggestions: async (positionId: string) => {
        const res = await fetch(`${API_BASE_URL}/api/performance/suggestions/${positionId}`);
        if (!res.ok) throw new Error("Failed to fetch suggestions");
        return res.json();
    },
    // --- Reporting (Job Management Card) ---
    getJobManagementCard: async (userId: string) => {
        const res = await fetch(`${API_BASE_URL}/reporting/job-card/${userId}`);
        if (!res.ok) throw new Error("Failed to fetch job card");
        return res.json();
    },
    // --- Personnel Record (Dual Tenure) ---
    getPersonnelTenure: async (userId: string) => {
        const res = await fetch(`${API_BASE_URL}/personnel/${userId}/tenure`);
        if (!res.ok) throw new Error("Failed to fetch tenure info");
        return res.json();
    },

    assignJobDate: async (userId: string, dateStr: string) => {
        const res = await fetch(`${API_BASE_URL}/personnel/${userId}/assign-job?date_str=${dateStr}`, {
            method: "POST",
        });
        if (!res.ok) throw new Error("Failed to assign job date");
        return res.json();
    },

    getDualTenureAnalysis: async (orgUnitId?: string): Promise<any[]> => {
        const query = orgUnitId ? `?org_unit_id=${orgUnitId}` : '';
        const res = await fetch(`${API_BASE_URL}/workforce/dual-tenure${query}`);
        if (!res.ok) throw new Error("Failed to fetch dual tenure analysis");
        return res.json();
    },

    // --- Career Development (Promotion, Training, Competency) ---
    getPromotionCandidates: async () => {
        const res = await fetch(`${API_BASE_URL}/career/promotion-candidates`);
        if (!res.ok) throw new Error("Failed to fetch promotion candidates");
        return res.json();
    },

    getTrainingRecommendations: async (userId: string) => {
        const res = await fetch(`${API_BASE_URL}/career/training-recommendations/${userId}`);
        if (!res.ok) throw new Error("Failed to fetch training recommendations");
        return res.json();
    },

    getCompetencyModel: async (seriesId: string) => {
        const res = await fetch(`${API_BASE_URL}/career/competency-model/${seriesId}`);
        if (!res.ok) throw new Error("Failed to fetch competency model");
        return res.json();
    },

    // --- AI Intelligence ---
    getAiSearchResults: async (query: string, type?: string) => {
        const res = await fetch(`${API_BASE_URL}/ai/search?query=${encodeURIComponent(query)}&type=${type || ""}`);
        if (!res.ok) throw new Error("Search failed");
        return res.json();
    },

    generateJobDescription: async (positionId: string, taskIds: string[]) => {
        const res = await fetch(`${API_BASE_URL}/ai/generate-jd`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ position_id: positionId, task_ids: taskIds })
        });
        if (!res.ok) throw new Error("Generation failed");
        return res.json();
    },

    analyzeWorkload: async (tasks: any[]) => {
        const res = await fetch(`${API_BASE_URL}/ai/analyze-workload`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tasks: tasks })
        });
        if (!res.ok) throw new Error("Analysis failed");
        return res.json();
    },

    // --- Employee Experience (My Job) ---
    getMyJobDashboard: async () => {
        const res = await fetch(`${API_BASE_URL}/users/me/dashboard`);
        if (!res.ok) throw new Error("Failed to fetch dashboard");
        return res.json();
    },

    submitPulseCheck: async (data: { mood: number, workload: string, note?: string }) => {
        const res = await fetch(`${API_BASE_URL}/surveys/pulse`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error("Pulse submission failed");
        return res.json();
    },

    // --- Enterprise Integration (ERP) ---
    previewERPSync: async () => {
        const res = await fetch(`${API_BASE_URL}/erp/preview`);
        if (!res.ok) throw new Error("Failed to fetch ERP preview");
        return res.json();
    },

    executeERPSync: async () => {
        const res = await fetch(`${API_BASE_URL}/erp/sync`, { method: "POST" });
        if (!res.ok) throw new Error("Sync failed");
        return res.json();
    },

    // --- Phase 4: Wage Simulation ---
    runWageSimulation: async (spread: number, base_increase: number) => {
        const res = await fetch(`${API_BASE_URL}/wage/simulate`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ spread, base_increase })
        });
        if (!res.ok) throw new Error("Simulation failed");
        return res.json();
    },

    // --- Phase 4: NCS Compliance ---
    runNCSAudit: async (job_id: string, ncs_code?: string) => {
        const res = await fetch(`${API_BASE_URL}/compliance/audit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_id, ncs_code })
        });
        if (!res.ok) throw new Error("Audit failed");
        return res.json();
    },

    // --- Descriptions ---
    getJobDescriptions: async () => {
        const res = await fetch(`${API_BASE_URL}/descriptions/`);
        if (!res.ok) throw new Error("Failed to fetch job descriptions");
        return res.json();
    },

    // --- Phase 4: Fairness Analysis ---
    getFairnessAnalysis: async () => {
        const res = await fetch(`${API_BASE_URL}/fairness/analysis`);
        if (!res.ok) throw new Error("Failed to fetch fairness analysis");
        return res.json();
    },

    // --- Phase 5: Prediction ---
    getAttritionPrediction: async () => {
        const res = await fetch(`${API_BASE_URL}/prediction/attrition`);
        if (!res.ok) throw new Error("Failed to fetch attrition prediction");
        return res.json();
    },

    // --- Phase 5: Global Settings ---
    getGlobalSettings: async () => {
        const res = await fetch(`${API_BASE_URL}/global/settings`);
        if (!res.ok) throw new Error("Failed to fetch global settings");
        return res.json();
    },

    // --- Phase 5: Blockchain ---
    issueBlockchainCertificate: async (userId: string) => {
        const res = await fetch(`${API_BASE_URL}/blockchain/issue/${userId}`, {
            method: 'POST'
        });
        if (!res.ok) throw new Error("Failed to issue blockchain certificate");
        return res.json();
    },

    // --- Phase 6: Scientific HR ---
    getCalibrationSuggestions: async () => {
        const res = await fetch(`${API_BASE_URL}/scientific/calibration/suggestions`);
        if (!res.ok) throw new Error("Failed to fetch calibration suggestions");
        return res.json();
    },

    getPerformanceIntegral: async (userId: string = "all") => {
        const endpoint = userId === "all" ? "integral/all" : `integral/${userId}`;
        const res = await fetch(`${API_BASE_URL}/scientific/performance/${endpoint}`);
        if (!res.ok) throw new Error("Failed to fetch performance integral");
        return res.json();
    },

    simulatePromotion: async () => {
        const res = await fetch(`${API_BASE_URL}/scientific/promotion/simulate`);
        if (!res.ok) throw new Error("Failed to fetch promotion simulation");
        return res.json();
    },
    // Phase 7: Scientific Promotion Rank
    getPromotionRankList: async () => {
        const response = await fetch(`${API_BASE_URL}/scientific/rank/list`);
        return response.json();
    },

    // Phase 7: Optimal Workforce Calculator
    getWorkforceOptimization: async () => {
        const response = await fetch(`${API_BASE_URL}/scientific/workforce/optimization`);
        return response.json();
    },

    // Phase 8: Dynamic JD
    getDynamicJDAnalysis: async (jobId: string) => {
        const response = await fetch(`${API_BASE_URL}/job-architecture/dynamic-jd/${jobId}`);
        return response.json();
    },



    // Phase 8: R&R Conflict Map
    getRAndRAnalysis: async () => {
        const response = await fetch(`${API_BASE_URL}/job-architecture/r-and-r/conflict-map`);
        return response.json();
    },

    // Phase 8.5: RACI Generator
    getRACIChart: async (processId: string) => {
        const response = await fetch(`${API_BASE_URL}/scientific/raci/matrix/${processId}`);
        return response.json();
    },

    // Phase 8.5: 9-Box Grid
    getNineBoxGrid: async () => {
        const response = await fetch(`${API_BASE_URL}/scientific/talent/9-box`);
        return response.json();
    },

    // Phase 8.5: Span of Control
    getSpanOfControlAnalysis: async () => {
        const response = await fetch(`${API_BASE_URL}/scientific/org/span-of-control`);
        return response.json();
    },

    // Phase 8.6: Competency Fit Radar
    getCompetencyRadar: async (userId: string) => {
        const response = await fetch(`${API_BASE_URL}/scientific/competency/radar/${userId}`);
        return response.json();
    },

    // Phase 9: Predictive HR
    trainTurnoverModel: async () => {
        const response = await fetch(`${API_BASE_URL}/scientific/prediction/turnover/train`, { method: 'POST' });
        return response.json();
    },
    getTurnoverRisk: async (userId: string) => {
        const response = await fetch(`${API_BASE_URL}/scientific/prediction/turnover/${userId}`);
        return response.json();
    },
    getCareerRecommendations: async (userId: string) => {
        const response = await fetch(`${API_BASE_URL}/scientific/prediction/career/${userId}`);
        return response.json();
    },
};
