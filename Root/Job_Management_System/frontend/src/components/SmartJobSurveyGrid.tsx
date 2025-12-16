"use client";

import React, { useState, useEffect } from "react";
import {
    Button, Select, Group, Text, Title, Paper, TextInput, Slider,
    Stack, Badge, ActionIcon, ScrollArea, Tooltip, Transition, Kbd, Progress, Card, ThemeIcon,
    Modal, LoadingOverlay, Checkbox, Divider
} from "@mantine/core";
import {
    IconPlus, IconTrash, IconWand, IconSparkles, IconClock, IconRepeat, IconCheck, IconListCheck,
    IconRobot, IconRefresh
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
    "daily": 240, "every day": 240, "매일": 240,
    "weekly": 48, "every week": 48, "매주": 48, "주간": 48,
    "monthly": 12, "every month": 12, "매월": 12, "월간": 12,
    "quarterly": 4, "분기": 4, "분기별": 4,
    "annually": 1, "yearly": 1, "매년": 1, "연간": 1
};

// ... (Previous imports remain, ensure IconChevronRight, IconChevronDown are imported if needed)
import { IconChevronRight, IconChevronDown, IconCornerDownRight } from "@tabler/icons-react";

interface JobSurveyRow {
    id?: string;
    taskId?: string;
    taskName: string;
    actionVerb: string;
    volume: number;
    standardTime: number;
    fte: number;
    isNew?: boolean;
    parentId?: string; // For hierarchy
    children?: JobSurveyRow[]; // For UI tree structure
    expanded?: boolean; // UI state
}

// ... (FREQ_MAP remains same)

export default function SmartJobSurveyGrid({ totalHours = 2080 }: { totalHours?: number }) {
    const [rowData, setRowData] = useState<JobSurveyRow[]>([]);
    const [loading, setLoading] = useState(false);

    // AI Discovery State
    const [aiModalOpen, setAiModalOpen] = useState(false);
    const [aiJobTitle, setAiJobTitle] = useState("");
    const [aiSuggestions, setAiSuggestions] = useState<any[]>([]);
    const [selectedSuggestions, setSelectedSuggestions] = useState<string[]>([]);
    const [aiLoading, setAiLoading] = useState(false);

    // Flattened list for calculations, Tree for display
    // Actually simpler to manage flat list with parentId and build tree on render or memo

    // ... (State hooks remain)

    // Helper to build tree
    const buildTree = (rows: JobSurveyRow[]) => {
        const map: Record<string, JobSurveyRow> = {};
        const roots: JobSurveyRow[] = [];
        const rowsWithChildren = rows.map(r => ({ ...r, children: [] })); // Deep copy for UI

        rowsWithChildren.forEach(r => { map[r.taskId || r.taskName] = r; }); // Use taskId or name as key

        rowsWithChildren.forEach(r => {
            if (r.parentId && map[r.parentId]) {
                map[r.parentId].children?.push(r);
            } else {
                roots.push(r);
            }
        });
        return roots;
    };

    // ... (useEffect for Parsing & Loading remain mostly same)

    // Load Data: needs to fetch parent_id too
    const loadData = async () => {
        setLoading(true);
        try {
            const entries = await api.getWorkloadEntries();
            const tasks = await api.getJobTasks(); // Need tasks to get hierarchies

            const taskMap = new Map(tasks.map((t: any) => [t.id, t]));

            const formatted = entries.map((e: any) => ({
                id: e.id,
                taskId: e.task_id,
                taskName: e.task?.task_name || "Unknown",
                parentId: (taskMap.get(e.task_id) as any)?.parent_id, // Get parent from task def
                actionVerb: e.task?.action_verb || "",
                volume: e.volume,
                standardTime: e.standard_time,
                fte: e.fte,
                expanded: true
            }));
            setRowData(formatted);
        } catch (err) { console.error(err); }
        finally { setLoading(false); }
    };

    const handleAdd = (parentTask?: JobSurveyRow) => {
        // If adding subtask, check if parsed or manual
        // Logic to add row with parentId
    };

    // Recursive Row Component
    const TaskRow = ({ row, level = 0, onDelete, onUpdate, onAddSub, parentTotalHours = 0, totalBudgetHours }: any) => {
        const totalMinutes = row.volume * row.standardTime;
        const totalHours = totalMinutes / 60;

        // Calculate Children Totals
        const childrenSumMinutes = row.children?.reduce((acc: number, c: any) => acc + (c.volume * c.standardTime), 0) || 0;
        const childrenSumHours = childrenSumMinutes / 60;

        // If has children, display SUM. If leaf, display OWN.
        const effectiveHours = (row.children && row.children.length > 0) ? childrenSumHours : totalHours;
        const globalPercentage = (effectiveHours / totalBudgetHours * 100).toFixed(1);

        // Local percentage (share of parent)
        const localPercentage = parentTotalHours > 0 ? (effectiveHours / parentTotalHours * 100).toFixed(1) : globalPercentage;

        return (
            <div className="mb-3">
                <Paper p="sm" radius="md" withBorder className={`transition-all hover:shadow-md ${level > 0 ? 'ml-8 border-l-4 border-l-indigo-100' : 'border-l-4 border-l-indigo-500'} bg-white`}>
                    <Group align="center" justify="space-between" mb="xs">
                        <Group gap="sm" style={{ flex: 1 }}>
                            {level > 0 && <IconCornerDownRight size={16} className="text-gray-400" />}
                            <Stack gap={0} style={{ flex: 1 }}>
                                <TextInput
                                    variant="unstyled"
                                    size={level === 0 ? "lg" : "md"}
                                    fw={level === 0 ? 700 : 500}
                                    value={row.taskName}
                                    placeholder="업무명을 입력하세요..."
                                    onChange={(e) => onUpdate(row, 'taskName', e.target.value)}
                                    classNames={{ input: 'p-0 m-0 h-auto' }}
                                />
                                {/* Percentage Bar Under Name */}
                                <Group gap="xs" align="center" mt={4}>
                                    <Progress
                                        value={parseFloat(localPercentage)}
                                        size="xs"
                                        color={level === 0 ? "indigo" : "cyan"}
                                        w={100}
                                        radius="xl"
                                    />
                                    <Text size="xs" c="dimmed" fw={600}>
                                        {effectiveHours.toLocaleString()}h <span className="text-gray-300">|</span> <span className="text-indigo-600">{globalPercentage}%</span> of Total
                                    </Text>
                                </Group>
                            </Stack>
                        </Group>

                        <Group>
                            <ActionIcon variant="light" color="blue" onClick={() => onAddSub(row)} title="하위 업무 추가">
                                <IconPlus size={16} />
                            </ActionIcon>
                            <ActionIcon variant="light" color="red" onClick={() => onDelete(row)}>
                                <IconTrash size={16} />
                            </ActionIcon>
                        </Group>
                    </Group>

                    {/* Controls (Only for Leaf Nodes) */}
                    {(!row.children || row.children.length === 0) && (
                        <Card bg="gray.0" p="xs" radius="md" mt="sm">
                            <Group grow align="start">
                                {/* Frequency Control */}
                                <Stack gap={4}>
                                    <Group justify="space-between">
                                        <Text size="xs" fw={600} c="dimmed">빈도</Text>
                                        <Badge variant="white" color="blue" size="sm">{row.volume}회 / 년</Badge>
                                    </Group>
                                    <Slider
                                        value={row.volume} onChange={(v) => onUpdate(row, 'volume', v)}
                                        min={1} max={260}
                                        color="blue" size="sm" thumbSize={14}
                                    />
                                    <Group gap={4}>
                                        {[
                                            { label: '매일', val: 240 }, { label: '매주', val: 52 },
                                            { label: '매월', val: 12 }, { label: '매년', val: 1 }
                                        ].map(preset => (
                                            <Badge
                                                key={preset.label}
                                                variant="outline" color="gray"
                                                className="cursor-pointer hover:bg-gray-100"
                                                onClick={() => onUpdate(row, 'volume', preset.val)}
                                            >
                                                {preset.label}
                                            </Badge>
                                        ))}
                                    </Group>
                                </Stack>

                                {/* Duration Control */}
                                <Stack gap={4}>
                                    <Group justify="space-between">
                                        <Text size="xs" fw={600} c="dimmed">소요 시간</Text>
                                        <Badge variant="white" color="orange" size="sm">{row.standardTime}분</Badge>
                                    </Group>
                                    <Slider
                                        value={row.standardTime} onChange={(v) => onUpdate(row, 'standardTime', v)}
                                        min={10} max={480} step={10}
                                        color="orange" size="sm" thumbSize={14}
                                    />
                                    <Group gap={4}>
                                        {[
                                            { label: '30분', val: 30 }, { label: '1시간', val: 60 },
                                            { label: '2시간', val: 120 }, { label: '4시간', val: 240 }
                                        ].map(preset => (
                                            <Badge
                                                key={preset.label}
                                                variant="outline" color="gray"
                                                className="cursor-pointer hover:bg-gray-100"
                                                onClick={() => onUpdate(row, 'standardTime', preset.val)}
                                            >
                                                {preset.label}
                                            </Badge>
                                        ))}
                                    </Group>
                                </Stack>
                            </Group>
                        </Card>
                    )}
                </Paper>

                {/* Render Children */}
                {row.children?.map((child: any) => (
                    <TaskRow
                        key={child.taskId || child.taskName}
                        row={child}
                        level={level + 1}
                        onDelete={onDelete}
                        onUpdate={onUpdate}
                        onAddSub={onAddSub}
                        parentTotalHours={effectiveHours} // Pass parent's hours for % calc
                        totalBudgetHours={totalBudgetHours}
                    />
                ))}
            </div>
        );
    };

    const treeData = React.useMemo(() => buildTree(rowData), [rowData]);

    // ... (Rest of render)
    // Replace the flat list mapping with:
    // {treeData.map((node) => <TaskRow key={node.taskId} row={node} ... />)}

    // --- Handlers ---
    const handleUpdate = (row: JobSurveyRow, key: string, val: any) => {
        setRowData(prev => prev.map(r => {
            if (r.taskId === row.taskId || (r.taskName === row.taskName && r.isNew)) {
                return { ...r, [key]: val };
            }
            return r;
        }));
    };

    const handleDelete = (row: JobSurveyRow) => {
        setRowData(prev => prev.filter(r => r !== row));
    };

    const handleSaveAll = async () => {
        setLoading(true);
        try {
            // Flatten and save
            // Note: For new tasks, we might need to create them first or backend handles it.
            // Current API expects task_id. If isNew, we need 'createJobTask' first?
            // For MVP Demo: Assume we only update Volumes for existing tasks or skip new ones for now unless robust logic added.

            // We will loop and save individually (inefficient but safe) or bulk. 
            // API has 'saveWorkloadEntry'.

            let savedCount = 0;
            for (const row of rowData) {
                if (!row.taskId) continue; // Skip if no ID (should allow creating new tasks in Phase 2)

                // Calculate Volume/Time
                // volume = occurrences/year
                // standard_time = mins/occurrence

                await api.saveWorkloadEntry({
                    user_id: "user_test", // Mock User
                    task_id: row.taskId,
                    volume: row.volume,
                    standard_time: row.standardTime
                });
                savedCount++;
            }
            notifications.show({ title: '저장 완료', message: `${savedCount}개 항목이 저장되었습니다.`, color: 'green' });
        } catch (e) {
            console.error(e);
            notifications.show({ title: '저장 실패', message: '데이터 저장 중 오류가 발생했습니다.', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    // --- AI Discovery Handlers ---
    const handleDiscover = async () => {
        if (!aiJobTitle) {
            notifications.show({ message: "직무명을 입력해주세요.", color: 'red' });
            return;
        }
        setAiLoading(true);
        try {
            const results = await api.discoverTasks(aiJobTitle);
            setAiSuggestions(results);
            setSelectedSuggestions([]); // Reset selection
        } catch (e) {
            notifications.show({ title: 'AI 검색 실패', message: '추천 작업을 가져오지 못했습니다.', color: 'red' });
        } finally {
            setAiLoading(false);
        }
    };

    const handleAddSuggestions = () => {
        const toAdd = aiSuggestions.filter(s => selectedSuggestions.includes(s.task_name));

        const newRows: JobSurveyRow[] = toAdd.map(s => ({
            id: `new_${Date.now()}_${Math.random()}`, // Temp ID
            taskName: s.task_name,
            actionVerb: s.action_verb,
            volume: 12, // Default
            standardTime: s.avg_time || 60,
            fte: 0,
            isNew: true,
            expanded: true
        }));

        setRowData(prev => [...prev, ...newRows]);
        setAiModalOpen(false);
        notifications.show({ title: '추가 완료', message: `${newRows.length}개의 업무가 추가되었습니다.`, color: 'blue' });
    };

    return (
        <Stack gap="md" className="h-full">
            {/* AI Modal */}
            <Modal
                opened={aiModalOpen}
                onClose={() => setAiModalOpen(false)}
                title={<Group><IconRobot size={24} color="#4F46E5" /><Text fw={700}>AI 업무 자동 발굴</Text></Group>}
                size="lg"
            >
                <Stack>
                    <Text size="sm" c="dimmed">
                        직무명을 입력하면 AI가 수행해야 할 핵심 과업을 자동으로 제안합니다.
                    </Text>
                    <Group align="end">
                        <TextInput
                            label="직무명 (Job Title)"
                            placeholder="예: HR Manager, SW Engineer, Sales"
                            style={{ flex: 1 }}
                            value={aiJobTitle}
                            onChange={(e) => setAiJobTitle(e.target.value)}
                            onKeyDown={(e) => { if (e.key === 'Enter') handleDiscover(); }}
                        />
                        <Button
                            color="indigo"
                            variant="filled"
                            leftSection={<IconSparkles size={16} />}
                            onClick={handleDiscover}
                            loading={aiLoading}
                        >
                            AI 검색
                        </Button>
                    </Group>

                    <Divider my="xs" label="AI 제안 결과" labelPosition="center" />

                    <div className="min-h-[200px] relative">
                        <LoadingOverlay visible={aiLoading} />
                        {aiSuggestions.length > 0 ? (
                            <Stack gap="xs">
                                <Group justify="space-between" mb="xs">
                                    <Text size="xs" fw={700}>{aiSuggestions.length}개의 제안 발견</Text>
                                    <Button variant="subtle" size="xs" onClick={() => setSelectedSuggestions(aiSuggestions.map(s => s.task_name))}>모두 선택</Button>
                                </Group>
                                <ScrollArea h={250}>
                                    {aiSuggestions.map((item, idx) => (
                                        <Paper key={idx} withBorder p="sm" mb="xs" bg="gray.0">
                                            <Checkbox
                                                label={
                                                    <Group justify="space-between" w="100%">
                                                        <Text size="sm" fw={500}>{item.task_name}</Text>
                                                        <Badge size="sm" color="gray">{item.action_verb}</Badge>
                                                    </Group>
                                                }
                                                checked={selectedSuggestions.includes(item.task_name)}
                                                onChange={(event) => {
                                                    if (event.currentTarget.checked) {
                                                        setSelectedSuggestions([...selectedSuggestions, item.task_name]);
                                                    } else {
                                                        setSelectedSuggestions(selectedSuggestions.filter(t => t !== item.task_name));
                                                    }
                                                }}
                                            />
                                        </Paper>
                                    ))}
                                </ScrollArea>
                                <Button fullWidth mt="md" onClick={handleAddSuggestions} disabled={selectedSuggestions.length === 0}>
                                    선택한 {selectedSuggestions.length}개 업무 추가하기
                                </Button>
                            </Stack>
                        ) : (
                            !aiLoading && <Text c="dimmed" ta="center" mt="xl">검색 결과가 여기에 표시됩니다.</Text>
                        )}
                    </div>
                </Stack>
            </Modal>

            {/* Control Bar */}
            <Paper p="sm" withBorder shadow="sm" className="sticky top-0 z-10 bg-white">
                <Group justify="space-between">
                    <Group>
                        <ThemeIcon variant="light" size="lg" color="indigo"><IconListCheck /></ThemeIcon>
                        <div>
                            <Text fw={700}>직무 조사 (Job Survey)</Text>
                            <Text size="xs" c="dimmed">목표: {totalHours}시간 / 분석</Text>
                        </div>
                    </Group>
                    <Group>
                        <Button
                            variant="light"
                            color="teal"
                            leftSection={<IconWand size={16} />}
                            onClick={loadData}
                            loading={loading}
                        >
                            초기화
                        </Button>
                        <Button
                            variant="gradient"
                            gradient={{ from: 'indigo', to: 'cyan' }}
                            leftSection={<IconSparkles size={16} />}
                            onClick={() => setAiModalOpen(true)}
                        >
                            AI 추천
                        </Button>
                        <Button
                            variant="filled"
                            color="indigo"
                            leftSection={<IconCheck size={16} />}
                            onClick={handleSaveAll}
                            loading={loading}
                        >
                            저장하기
                        </Button>
                    </Group>
                </Group>
            </Paper>

            <ScrollArea className="flex-1 -mx-4 px-4">
                {treeData.length === 0 && !loading && (
                    <Paper p="xl" withBorder className="border-dashed border-2 bg-slate-50">
                        <Stack align="center" gap="md">
                            <IconSparkles size={48} className="text-gray-300" />
                            <Title order={3} c="dimmed">분석 준비 완료</Title>
                            <Button size="md" variant="white" onClick={loadData}>JD 데이터 가져오기</Button>
                        </Stack>
                    </Paper>
                )}

                <Stack gap="xs" pb="xl">
                    {treeData.map((node, idx) => (
                        <TaskRow
                            key={node.taskId || idx}
                            row={node}
                            onDelete={handleDelete}
                            onUpdate={handleUpdate}
                            onAddSub={(parent: any) => {
                                notifications.show({ message: "하위 업무 추가는 아직 지원되지 않습니다.", color: 'orange' });
                            }}
                            parentTotalHours={0}
                            totalBudgetHours={totalHours}
                        />
                    ))}
                </Stack>
            </ScrollArea>
        </Stack>
    );
}
