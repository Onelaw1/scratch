const API_BASE_URL = "http://localhost:8000";

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
};
