"use client";

import React, { useState, useEffect } from "react";
import {
    Button, Select, Group, Text, Title, Paper, TextInput, Slider,
    Stack, Badge, ActionIcon, ScrollArea, Tooltip, Transition, Kbd
} from "@mantine/core";
import {
    IconPlus, IconTrash, IconWand, IconSparkles, IconClock, IconRepeat, IconCheck
} from "@tabler/icons-react";
import { useInputState } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { api } from "../lib/api";

interface JobSurveyRow {
    id?: string;
    taskId?: string;
    taskName: string;
    actionVerb: string;
    volume: number; // occurrences per year
    standardTime: number; // minutes per occurrence
    fte: number;
    isNew?: boolean;
}

// Frequency helpers
const FREQ_MAP: Record<string, number> = {
    "daily": 240,
    "weekly": 48,
    "monthly": 12,
    "quarterly": 4,
    "annually": 1,
    "yearly": 1,
    "every day": 240,
    "every week": 48,
    "every month": 12,
};

export default function SmartJobSurveyGrid() {
    const [rowData, setRowData] = useState<JobSurveyRow[]>([]);
    const [loading, setLoading] = useState(false);

    // Smart Input
    const [inputValue, setInputValue] = useInputState("");
    const [parsedPreview, setParsedPreview] = useState<Partial<JobSurveyRow> | null>(null);

    // Context
    const [positions, setPositions] = useState<any[]>([]);
    const [users, setUsers] = useState<any[]>([]);
    const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);

    useEffect(() => {
        loadContext();
    }, []);

    useEffect(() => {
        if (selectedUser) loadData();
    }, [selectedUser]);

    // Parse Input in Real-time
    useEffect(() => {
        if (!inputValue.trim()) {
            setParsedPreview(null);
            return;
        }

        // Simple Heuristic Regex
        // Pattern: [Task Name] [Frequency] [Duration]
        // e.g. "Write Report weekly for 2 hours"
        const freqPattern = /(daily|weekly|monthly|quarterly|annually|yearly|every day|every week|every month)/i;
        const durationPattern = /(\d+)\s*(min|hour|h|m)/i;

        const freqMatch = inputValue.match(freqPattern);
        const durMatch = inputValue.match(durationPattern);

        let vol = 0;
        let st = 0;
        let name = inputValue;

        if (freqMatch) {
            vol = FREQ_MAP[freqMatch[0].toLowerCase()] || 0;
            name = name.replace(freqMatch[0], "").trim();
        }

        if (durMatch) {
            const val = parseInt(durMatch[1]);
            const unit = durMatch[2].toLowerCase();
            if (unit.startsWith('h')) st = val * 60;
            else st = val;
            name = name.replace(durMatch[0], "").trim();
        }

        // Clean up prepositions
        name = name.replace(/\s+(for|at|during|every)\s*$/, "").trim();

        if (name && (vol > 0 || st > 0)) {
            setParsedPreview({
                taskName: name,
                volume: vol,
                standardTime: st,
                fte: ((vol * st) / (2080 * 60)) // approximate
            });
        } else {
            setParsedPreview(null);
        }

    }, [inputValue]);

    const loadContext = async () => {
        try {
            const [posData, userData] = await Promise.all([api.getJobPositions(), api.getUsers()]);
            setPositions(posData.map((p: any) => ({ value: p.id, label: p.title })));
            setUsers(userData.map((u: any) => ({ value: u.id, label: u.name || u.email })));
            if (posData.length) setSelectedPosition(posData[0].id);
            if (userData.length) setSelectedUser(userData[0].id);
        } catch (e) { console.error(e); }
    };

    const loadData = async () => {
        setLoading(true);
        try {
            const entries = await api.getWorkloadEntries();
            const formatted = entries.map((e: any) => ({
                id: e.id,
                taskId: e.task_id,
                taskName: e.task?.task_name || "Unknown",
                actionVerb: e.task?.action_verb || "",
                volume: e.volume,
                standardTime: e.standard_time,
                fte: e.fte,
            }));
            setRowData(formatted);
        } catch (err) { console.error(err); }
        finally { setLoading(false); }
    };

    const handleSmartAdd = async () => {
        if (!parsedPreview || !selectedUser || !selectedPosition) return;

        const newRow: JobSurveyRow = {
            taskName: parsedPreview.taskName!,
            actionVerb: "",
            volume: parsedPreview.volume || 1, // default to once
            standardTime: parsedPreview.standardTime || 60, // default to 1hr
            fte: 0,
            isNew: true
        };

        // Optimistic Add
        setRowData([newRow, ...rowData]);
        setInputValue("");
        setParsedPreview(null);
        notifications.show({ title: 'Added', message: 'Task added to list. Remember to Save.', color: 'blue' });
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && parsedPreview) {
            handleSmartAdd();
        }
    };

    const updateRow = (index: number, field: keyof JobSurveyRow, val: any) => {
        const newRows = [...rowData];
        newRows[index] = { ...newRows[index], [field]: val };
        setRowData(newRows);
    };

    const saveAll = async () => {
        if (!selectedUser || !selectedPosition) return;
        setLoading(true);
        try {
            // Simplified save logic reusing previous Logic
            const tasks = await api.getJobTasks();
            for (const row of rowData) {
                if (!row.isNew && !row.id) continue; // Skip partials

                let taskId = row.taskId;
                if (!taskId) {
                    const existing = tasks.find((t: any) => t.task_name === row.taskName);
                    if (existing) taskId = existing.id;
                    else {
                        const newTask = await api.createJobTask({
                            task_name: row.taskName,
                            action_verb: row.actionVerb,
                            position_id: selectedPosition
                        });
                        taskId = newTask.id;
                    }
                }

                await api.saveWorkloadEntry({
                    user_id: selectedUser,
                    task_id: taskId!,
                    volume: row.volume,
                    standard_time: row.standardTime
                });
            }
            notifications.show({ title: 'Saved', message: 'Workload saved successfully', color: 'green' });
            loadData();
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Error', message: 'Failed to save', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const deleteRow = (index: number) => {
        const newRows = [...rowData];
        newRows.splice(index, 1);
        setRowData(newRows);
    };

    return (
        <div className="h-full flex flex-col gap-6">
            {/* Context Header */}
            <Group justify="space-between">
                <div>
                    <Title order={2}>Workload Survey</Title>
                    <Text c="dimmed">Use natural language to add tasks (e.g., "Weekly meeting for 1 hour")</Text>
                </div>
                <Group>
                    <Select data={users} value={selectedUser} onChange={setSelectedUser} placeholder="User" searchable />
                    <Select data={positions} value={selectedPosition} onChange={setSelectedPosition} placeholder="Position" searchable />
                    <Button onClick={saveAll} loading={loading} leftSection={<IconCheck size={16} />}>Save Changes</Button>
                </Group>
            </Group>

            {/* Smart Input Bar */}
            <Paper p="lg" radius="lg" withBorder className="shadow-sm relative overflow-visible bg-white z-10">
                <TextInput
                    size="xl"
                    placeholder="Type task... e.g., 'Daily Standup for 30 mins'"
                    value={inputValue}
                    onChange={setInputValue}
                    onKeyDown={handleKeyDown}
                    leftSection={<IconWand size={24} className="text-indigo-500" />}
                    rightSection={
                        inputValue && (
                            <ActionIcon variant="filled" color="indigo" size="lg" radius="xl" onClick={handleSmartAdd}>
                                <IconPlus size={20} />
                            </ActionIcon>
                        )
                    }
                    classNames={{ input: 'border-none focus:ring-0 text-lg' }}
                />

                {/* Preview Badge */}
                <Transition mounted={!!parsedPreview} transition="pop-bottom-left" duration={200} timingFunction="ease">
                    {(styles) => (
                        <div style={styles} className="absolute -bottom-4 left-6">
                            <Badge
                                size="lg"
                                variant="gradient"
                                gradient={{ from: 'indigo', to: 'cyan' }}
                                leftSection={<IconSparkles size={14} />}
                                className="shadow-md"
                            >
                                {parsedPreview?.taskName} • {Math.round(parsedPreview?.volume || 0)}x/yr • {Math.round(parsedPreview?.standardTime || 0)}m
                            </Badge>
                        </div>
                    )}
                </Transition>

                {/* Helper Hints */}
                {!parsedPreview && !inputValue && (
                    <Group className="absolute -bottom-3 left-6" gap="xs">
                        <Badge variant="outline" size="sm" color="gray" leftSection={<IconRepeat size={10} />}>Try: "Monthly Repo Audit for 3h"</Badge>
                        <Badge variant="outline" size="sm" color="gray" leftSection={<IconClock size={10} />}>Try: "Daily Email Check for 30m"</Badge>
                    </Group>
                )}
            </Paper>

            {/* Card List */}
            <ScrollArea className="flex-1 -mx-4 px-4">
                <Stack>
                    {rowData.map((row, idx) => (
                        <Paper key={idx} p="md" radius="md" withBorder className="hover:border-indigo-300 transition-colors">
                            <Group align="start" justify="space-between" mb="xs">
                                <div className="flex-1">
                                    <TextInput
                                        variant="unstyled"
                                        size="lg"
                                        fw={600}
                                        value={row.taskName}
                                        onChange={(e) => updateRow(idx, 'taskName', e.target.value)}
                                        className="p-0 m-0 h-auto"
                                    />
                                    <Text c="dimmed" size="xs">
                                        FTE: {((row.volume * row.standardTime) / (2080 * 60)).toFixed(3)}
                                    </Text>
                                </div>
                                <ActionIcon variant="subtle" color="red" onClick={() => deleteRow(idx)}><IconTrash size={16} /></ActionIcon>
                            </Group>

                            <Group grow align="center">
                                {/* Volume Slider */}
                                <Stack gap={2}>
                                    <Group justify="space-between">
                                        <Text size="xs" fw={500} c="dimmed">Frequency (Times/Year)</Text>
                                        <Badge variant="light" color="blue">{row.volume}</Badge>
                                    </Group>
                                    <Slider
                                        value={row.volume}
                                        onChange={(v) => updateRow(idx, 'volume', v)}
                                        min={1} max={300}
                                        label={null}
                                        color="blue"
                                        size="sm"
                                    />
                                    <Group justify="space-between">
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'volume', 12)} className="cursor-pointer hover:text-blue-500">Monthly</Text>
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'volume', 52)} className="cursor-pointer hover:text-blue-500">Weekly</Text>
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'volume', 240)} className="cursor-pointer hover:text-blue-500">Daily</Text>
                                    </Group>
                                </Stack>

                                {/* Time Slider */}
                                <Stack gap={2}>
                                    <Group justify="space-between">
                                        <Text size="xs" fw={500} c="dimmed">Duration (Mins)</Text>
                                        <Badge variant="light" color="orange">{row.standardTime}m</Badge>
                                    </Group>
                                    <Slider
                                        value={row.standardTime}
                                        onChange={(v) => updateRow(idx, 'standardTime', v)}
                                        min={5} max={480} step={5}
                                        label={null}
                                        color="orange"
                                        size="sm"
                                    />
                                    <Group justify="space-between">
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'standardTime', 30)} className="cursor-pointer hover:text-orange-500">30m</Text>
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'standardTime', 60)} className="cursor-pointer hover:text-orange-500">1h</Text>
                                        <Text size="xs" c="dimmed" onClick={() => updateRow(idx, 'standardTime', 120)} className="cursor-pointer hover:text-orange-500">2h</Text>
                                    </Group>
                                </Stack>
                            </Group>
                        </Paper>
                    ))}
                    {rowData.length === 0 && (
                        <div className="text-center py-12 text-gray-400">
                            <IconSparkles size={48} className="mx-auto mb-4 opacity-50" />
                            <Text>No tasks yet. Try typing above!</Text>
                        </div>
                    )}
                </Stack>
            </ScrollArea>
        </div>
    );
}
