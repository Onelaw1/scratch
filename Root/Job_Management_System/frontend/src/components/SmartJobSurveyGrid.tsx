"use client";

import React, { useState, useEffect, useCallback } from "react";
import { AgGridReact } from "ag-grid-react";
import {
    ColDef,
    GridReadyEvent,
    ICellEditorParams,
    CellValueChangedEvent,
} from "ag-grid-community";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { motion } from "framer-motion";
import { Plus, Save, Wand2, Loader2 } from "lucide-react";
import { api } from "../lib/api";

// --- Types ---
interface JobSurveyRow {
    id?: string;
    taskName: string;
    actionVerb: string;
    volume: number;
    standardTime: number;
    fte: number;
    isNew?: boolean;
}

// --- Custom Cell Editor ---
const AutoCompleteEditor = (params: ICellEditorParams) => {
    const [value, setValue] = useState(params.value);
    const [options, setOptions] = useState<string[]>([]);

    useEffect(() => {
        // Fetch options from API (Mocked for now, but ready for real API)
        api.getJobTasks().then((tasks: any[]) => {
            setOptions(tasks.map((t) => t.task_name));
        });
    }, []);

    return (
        <div className="w-full h-full">
            <input
                value={value}
                onChange={(e) => setValue(e.target.value)}
                list={`list-${params.colDef.field}`}
                className="w-full h-full px-2 outline-none"
            />
            <datalist id={`list-${params.colDef.field}`}>
                {options.map((opt, idx) => (
                    <option key={idx} value={opt} />
                ))}
            </datalist>
        </div>
    );
};

export default function SmartJobSurveyGrid() {
    const [rowData, setRowData] = useState<JobSurveyRow[]>([]);
    const [loading, setLoading] = useState(false);

    // Fetch initial data
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const entries = await api.getWorkloadEntries();
            // Transform API data to Grid format
            const formatted = entries.map((e: any) => ({
                id: e.id,
                taskName: e.task?.task_name || "Unknown",
                actionVerb: e.task?.action_verb || "",
                volume: e.volume,
                standardTime: e.standard_time,
                fte: e.fte,
            }));
            setRowData(formatted);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const [columnDefs] = useState<ColDef<JobSurveyRow>[]>([
        {
            field: "taskName",
            headerName: "과업명 (Task)",
            editable: true,
            cellEditor: AutoCompleteEditor,
            flex: 2,
        },
        {
            field: "actionVerb",
            headerName: "행동동사",
            editable: true,
            cellClass: "bg-blue-50 text-blue-600 font-medium",
        },
        {
            field: "volume",
            headerName: "물량 (Volume)",
            editable: true,
            type: "numericColumn",
            valueParser: (params) => Number(params.newValue),
        },
        {
            field: "standardTime",
            headerName: "표준시간 (ST)",
            editable: true,
            type: "numericColumn",
            valueParser: (params) => Number(params.newValue),
        },
        {
            field: "fte",
            headerName: "FTE (자동계산)",
            editable: false,
            valueGetter: (params) => {
                const vol = params.data?.volume || 0;
                const st = params.data?.standardTime || 0;
                return ((vol * st) / 1920).toFixed(3);
            },
            cellClass: "font-bold text-slate-700 bg-slate-50",
        },
    ]);

    const onCellValueChanged = useCallback((event: CellValueChangedEvent) => {
        // Real-time FTE calculation is handled by valueGetter
        // Here we could trigger auto-save or validation
        console.log("Cell changed:", event.data);
    }, []);

    const addNewRow = () => {
        const newRow: JobSurveyRow = {
            taskName: "",
            actionVerb: "",
            volume: 0,
            standardTime: 0,
            fte: 0,
            isNew: true,
        };
        setRowData([...rowData, newRow]);
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            // Mock User ID and Task ID for demo
            const userId = "user-uuid-123";
            const taskId = "task-uuid-123";

            for (const row of rowData) {
                if (row.isNew || true) { // Save all for simplicity in this phase
                    await api.saveWorkloadEntry({
                        user_id: userId,
                        task_id: taskId, // In real app, find task ID by name or create new
                        volume: row.volume,
                        standard_time: row.standardTime,
                    });
                }
            }
            alert("저장되었습니다!");
            loadData(); // Refresh
        } catch (err) {
            alert("저장 실패: " + err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 h-[800px] flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-2xl font-bold text-slate-900">직무 조사표 (Job Survey)</h2>
                    <p className="text-slate-500 mt-1">
                        엑셀처럼 입력하면 FTE가 자동 계산됩니다.
                    </p>
                </div>
                <div className="flex gap-3">
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={addNewRow}
                        className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors"
                    >
                        <Plus size={18} />
                        행 추가
                    </motion.button>
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleSave}
                        disabled={loading}
                        className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition-colors shadow-lg shadow-slate-900/20 disabled:opacity-50"
                    >
                        {loading ? <Loader2 className="animate-spin" size={18} /> : <Save size={18} />}
                        저장하기
                    </motion.button>
                </div>
            </div>

            <div className="flex-1 ag-theme-quartz">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columnDefs}
                    defaultColDef={{
                        flex: 1,
                        minWidth: 100,
                        resizable: true,
                    }}
                    onCellValueChanged={onCellValueChanged}
                    className="h-full"
                />
            </div>
        </div>
    );
}
