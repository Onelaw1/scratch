"use client";

import React, { useState, useEffect, useCallback } from "react";
import { AgGridReact } from "ag-grid-react";
import {
    ColDef,
    CellValueChangedEvent,
} from "ag-grid-community";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import { Button, Group, Paper, Title, Text, LoadingOverlay, Notification } from "@mantine/core";
import { IconDeviceFloppy, IconPlus } from "@tabler/icons-react";
import { api, JobMatrixItem } from "../lib/api";

export default function JobMatrixGrid() {
    const [rowData, setRowData] = useState<JobMatrixItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [notification, setNotification] = useState<{ title: string, message: string, color: string } | null>(null);

    const loadData = async () => {
        setLoading(true);
        try {
            const data = await api.getJobMatrix();
            setRowData(data);
        } catch (error: any) {
            console.error(error);
            setNotification({
                title: "오류",
                message: error.message || "매트릭스 데이터를 불러오는데 실패했습니다.",
                color: "red"
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const [columnDefs] = useState<ColDef<JobMatrixItem>[]>([
        { field: "group_name", headerName: "직무군", editable: true, rowGroupIndex: 0, hide: true },
        { field: "series_name", headerName: "직무열", editable: true, rowGroupIndex: 1, hide: true },
        { field: "position_title", headerName: "직무 (Position)", editable: true, width: 220, pinned: 'left' },
        { field: "position_grade", headerName: "직급", editable: true, width: 100 },
        { field: "task_name", headerName: "책무/과업", editable: true, flex: 2, wrapText: true, autoHeight: true },
        { field: "work_item_name", headerName: "세부 활동", editable: true, flex: 2, wrapText: true, autoHeight: true },
        { field: "frequency", headerName: "수행 빈도", editable: true, width: 120 },
    ]);

    const [gridApi, setGridApi] = useState<any>(null);

    const onGridReady = (params: any) => {
        setGridApi(params.api);
    };

    const addNewRow = () => {
        const newRow: JobMatrixItem = {
            group_name: "새 직무군",
            series_name: "새 직무열",
            position_title: "새 직무",
            task_name: "새 책무"
        };
        // Use Transaction for immediate update
        if (gridApi) {
            gridApi.applyTransaction({ add: [newRow], addIndex: 0 });
            // Also update rowData state if we want to keep it somewhat in sync, 
            // but for saving we will extract from grid.
        }
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            // Extract data directly from Grid to ensure we capture all edits and new rows
            const allData: JobMatrixItem[] = [];
            if (gridApi) {
                gridApi.forEachNode((node: any) => {
                    // Only push leaf nodes or data nodes
                    if (node.data) {
                        allData.push(node.data);
                    }
                });
            }

            // Fallback if gridApi not ready (unlikely)
            const dataToSave = gridApi ? allData : rowData;

            await api.saveJobMatrix(dataToSave);
            setNotification({ title: "성공", message: "직무 매트릭스가 저장되었습니다!", color: "green" });

            // Reload to ensure consistency
            setTimeout(loadData, 500);
        } catch (error) {
            setNotification({ title: "오류", message: "저장 실패: " + error, color: "red" });
        } finally {
            setLoading(false);
        }
    };

    // Keep rowData in sync. AgGrid modifies the objects in place, so rowData ref technically has the changes,
    // but the state setter needs to be called if we were doing immutable updates. 
    // Since we pass `rowData` directly to `saveJobMatrix` and AgGrid mutates it, it 'works' but isn't pure React.
    // For this prototype level, it is acceptable.
    const onCellValueChanged = useCallback((event: CellValueChangedEvent) => {
        console.log("Cell changed", event.data);
    }, []);

    return (
        <Paper p="md" radius="lg" shadow="sm" h={800} pos="relative" className="flex flex-col">
            <LoadingOverlay visible={loading} zIndex={100} overlayProps={{ radius: "sm", blur: 2 }} />

            <Group justify="space-between" mb="md">
                <div>
                    <Title order={3}>직무 매트릭스</Title>
                    <Text size="sm" c="dimmed">직무 분류 데이터를 일괄 편집합니다. '변경사항 저장'을 눌러야 반영됩니다.</Text>
                </div>
                <Group>
                    <Button variant="default" leftSection={<IconPlus size={16} />} onClick={addNewRow}>행 추가</Button>
                    <Button color="blue" leftSection={<IconDeviceFloppy size={16} />} onClick={handleSave}>변경사항 저장</Button>
                </Group>
            </Group>

            {notification && (
                <Notification
                    title={notification.title}
                    color={notification.color}
                    onClose={() => setNotification(null)}
                    mb="md"
                >
                    {notification.message}
                </Notification>
            )}

            <div className="flex-1 ag-theme-quartz">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columnDefs}
                    onGridReady={onGridReady}
                    defaultColDef={{
                        sortable: true,
                        filter: true,
                        resizable: true,
                    }}
                    onCellValueChanged={onCellValueChanged}
                    groupDefaultExpanded={-1} // Expand all groups by default
                    className="h-full"
                />
            </div>
        </Paper>
    );
}
