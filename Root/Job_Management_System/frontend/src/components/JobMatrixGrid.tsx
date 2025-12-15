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
        } catch (error) {
            console.error(error);
            setNotification({ title: "Error", message: "Failed to load matrix data", color: "red" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    const [columnDefs] = useState<ColDef<JobMatrixItem>[]>([
        { field: "group_name", headerName: "Job Group", editable: true, rowGroupIndex: 0, hide: true },
        { field: "series_name", headerName: "Job Series", editable: true, rowGroupIndex: 1, hide: true },
        { field: "position_title", headerName: "Position", editable: true, width: 220, pinned: 'left' },
        { field: "position_grade", headerName: "Grade", editable: true, width: 100 },
        { field: "task_name", headerName: "Task Name", editable: true, flex: 2, wrapText: true, autoHeight: true },
        { field: "work_item_name", headerName: "Work Item", editable: true, flex: 2, wrapText: true, autoHeight: true },
        { field: "frequency", headerName: "Frequency", editable: true, width: 120 },
    ]);

    const addNewRow = () => {
        const newRow: JobMatrixItem = {
            group_name: "New Group",
            series_name: "New Series",
            position_title: "New Position",
            task_name: "New Task"
        };
        setRowData([newRow, ...rowData]); // Add to top for visibility
    };

    const handleSave = async () => {
        setLoading(true);
        try {
            // In a real application, you'd only send changed rows or use a transaction API.
            // Here we send the whole snapshot as per the simplified backend implementation.
            await api.saveJobMatrix(rowData);
            setNotification({ title: "Success", message: "Job Matrix Saved Successfully!", color: "green" });

            // Reload to ensure consistency
            // Note: Delay slightly to allow backend transaction to complete if async database
            setTimeout(loadData, 500);
        } catch (error) {
            setNotification({ title: "Error", message: "Failed to save: " + error, color: "red" });
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
                    <Title order={3}>Job Matrix (Edit Mode)</Title>
                    <Text size="sm" c="dimmed">Edit classification data in bulk. Changes are local until saved.</Text>
                </div>
                <Group>
                    <Button variant="default" leftSection={<IconPlus size={16} />} onClick={addNewRow}>Add Row</Button>
                    <Button color="blue" leftSection={<IconDeviceFloppy size={16} />} onClick={handleSave}>Save Changes</Button>
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
