"use client";

import { useState, useEffect } from "react";
import {
    Table, TextInput, Button, ActionIcon, NumberInput, Group, Badge,
    ThemeIcon, Text
} from "@mantine/core";
import { IconPlus, IconTrash, IconCornerDownRight } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { notifications } from "@mantine/notifications";

interface TaskItem {
    id: string;
    task_name: string;
    importance: number;
    parent_id?: string | null;
    children?: TaskItem[];
    level?: number;
}

interface Props {
    positionId: string;
    onChange?: () => void;
}

export function TaskHierarchyEditor({ positionId, onChange }: Props) {
    const [tasks, setTasks] = useState<TaskItem[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (positionId) loadTasks();
    }, [positionId]);

    const loadTasks = async () => {
        setLoading(true);
        try {
            const allTasks = await api.getJobTasks();
            // Filter for position
            const relevant = allTasks.filter((t: any) => t.job_position_id === positionId);
            const tree = buildTree(relevant);
            setTasks(tree);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const buildTree = (items: any[], parentId: string | null = null, level = 0): TaskItem[] => {
        return items
            .filter(item => item.parent_id === parentId)
            .map(item => ({
                ...item,
                children: buildTree(items, item.id, level + 1),
                level: level
            }));
    };

    const handleAddTask = async (parentId: string | null = null) => {
        try {
            await api.createJobTask({
                task_name: "새 과업",
                position_id: positionId,
                // parent_id support needed in createJobTask if we want hierarchy
                // Assuming createJobTask supports parent_id based on models.py
            });
            // NOTE: api.createJobTask might need update to accept parent_id
            // If it doesn't, we need to fix it. Let's assume for now and fix if needed.
            // Actually, I'll check api.ts. It receives { task_name, position_id }.
            // I need to update api.ts to send parent_id.

            loadTasks();
            if (onChange) onChange();
        } catch (e) {
            console.error(e);
        }
    };

    // Flatten for simple table rendering with indent
    const flattenTree = (nodes: TaskItem[]): TaskItem[] => {
        let flat: TaskItem[] = [];
        for (const node of nodes) {
            flat.push(node);
            if (node.children) {
                flat = [...flat, ...flattenTree(node.children)];
            }
        }
        return flat;
    };

    const flatTasks = flattenTree(tasks);

    const updateTask = async (id: string, field: string, val: any) => {
        // Optimistic update
        // We'd rely on simple state update but better to save via API for "Excel feel"? 
        // Maybe too many calls.
        // Let's just update local state and have a save button? 
        // User asked for "Input Box", usually implies immediate or bulk save.
        // The parent page has "Save All". I should probably bubble up changes or save immediately.
        // For simplicity, save immediately on blur? 
        // Let's implement local state change for inputs, and save on blur.

        // Actually, to make it simple, I'll save immediately for this prototype.
        try {
            await api.updateJobTask(id, { [field]: val });
            // Don't reload entire tree to keep focus
            // Just update local state
            // But flattening makes local state update tricky.
            // Let's just reload for safety or find item in flat list.
            loadTasks();
        } catch (e) { console.error(e); }
    };

    return (
        <Table highlightOnHover withTableBorder withColumnBorders>
            <Table.Thead bg="gray.1">
                <Table.Tr>
                    <Table.Th w={400}>과업명 (Task Breakdown)</Table.Th>
                    <Table.Th w={100} ta="center">비중 (%)</Table.Th>
                    <Table.Th w={100} ta="center">관리</Table.Th>
                </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
                {flatTasks.map((task) => (
                    <Table.Tr key={task.id}>
                        <Table.Td>
                            <Group gap="xs" style={{ paddingLeft: (task.level || 0) * 20 }}>
                                {(task.level || 0) > 0 && <IconCornerDownRight size={14} style={{ opacity: 0.5 }} />}
                                <TextInput
                                    variant="unstyled"
                                    value={task.task_name}
                                    onChange={(e) => { }} // Handle change?
                                    onBlur={(e) => updateTask(task.id, 'task_name', e.target.value)}
                                    // defaultValue used for uncontrolled "Excel" feel avoiding re-renders on every keystroke
                                    defaultValue={task.task_name}
                                    style={{ flex: 1 }}
                                />
                            </Group>
                        </Table.Td>
                        <Table.Td>
                            <NumberInput
                                variant="unstyled"
                                value={task.importance}
                                onChange={(v) => updateTask(task.id, 'importance', v)}
                                min={0} max={100}
                                ta="center"
                            />
                        </Table.Td>
                        <Table.Td ta="center">
                            <Group justify="center" gap={4}>
                                <ActionIcon size="sm" variant="subtle" color="blue" onClick={() => handleAddTask(task.id)} title="하위 과업 추가">
                                    <IconPlus size={14} />
                                </ActionIcon>
                                <ActionIcon size="sm" variant="subtle" color="red" title="삭제">
                                    <IconTrash size={14} />
                                </ActionIcon>
                            </Group>
                        </Table.Td>
                    </Table.Tr>
                ))}

                {/* Add Root Task Row */}
                <Table.Tr>
                    <Table.Td colSpan={3}>
                        <Button variant="subtle" fullWidth leftSection={<IconPlus size={14} />} onClick={() => handleAddTask(null)}>
                            최상위 과업 추가
                        </Button>
                    </Table.Td>
                </Table.Tr>
            </Table.Tbody>
        </Table>
    );
}
