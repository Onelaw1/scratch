"use client";

import React, { useState, useEffect } from "react";
import { Paper, Title, ScrollArea, Group, Text, Stack, ThemeIcon, Badge, Loader } from "@mantine/core";
import { IconChevronRight, IconFolder, IconFileText, IconListCheck, IconBriefcase, IconChecklist } from "@tabler/icons-react";
import { api, JobHierarchyNode } from "../lib/api";

export default function CascadingJobView() {
    const [hierarchy, setHierarchy] = useState<JobHierarchyNode[]>([]);
    const [selectedPath, setSelectedPath] = useState<JobHierarchyNode[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setLoading(true);
        api.getJobHierarchy()
            .then(setHierarchy)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    const handleSelect = (node: JobHierarchyNode, depth: number) => {
        const newPath = selectedPath.slice(0, depth);
        newPath.push(node);
        setSelectedPath(newPath);
    };

    // Columns: Root (Groups) -> Series -> Positions -> Tasks -> Work Items
    const columns = [];

    // col 0: Groups (Root)
    columns.push({ nodes: hierarchy, depth: 0, title: "직무군" });

    // col 1..N: Children of selected nodes
    for (let i = 0; i < selectedPath.length; i++) {
        const node = selectedPath[i];
        if (node.children && node.children.length > 0) {
            let title = "Items";
            if (node.type === "GROUP") title = "직무열";
            if (node.type === "SERIES") title = "직무";
            if (node.type === "POSITION") title = "책무";
            if (node.type === "TASK") title = "세부 과업";
            columns.push({ nodes: node.children, depth: i + 1, title });
        }
    }

    const getIcon = (type: string) => {
        switch (type) {
            case "GROUP": return <IconBriefcase size={16} />;
            case "SERIES": return <IconFolder size={16} />;
            case "POSITION": return <IconFileText size={16} />;
            case "TASK": return <IconListCheck size={16} />;
            default: return <IconChecklist size={16} />;
        }
    }

    return (
        <Paper p="lg" radius="xl" shadow="md" h={800} style={{ display: 'flex', flexDirection: 'column' }}>
            <Title order={3} mb="lg">직무 분류 계층도</Title>
            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                    <Loader size="lg" />
                </div>
            ) : (
                <div style={{ display: 'flex', overflowX: 'auto', gap: '1rem', height: '100%' }} className="no-scrollbar">
                    {columns[0].nodes.length === 0 && (
                        <div style={{ padding: '2rem', textAlign: 'center', width: '100%' }}>
                            <Text c="dimmed">등록된 직무 데이터가 없습니다.</Text>
                            <Text c="blue" style={{ cursor: 'pointer' }} onClick={() => document.querySelector<HTMLElement>('button[role="tab"][value="matrix"]')?.click()}>
                                '매트릭스 뷰' 탭에서 데이터를 입력하세요.
                            </Text>
                        </div>
                    )}
                    {columns.map((col, idx) => (
                        <Paper key={idx} withBorder w={320} radius="lg" style={{ display: 'flex', flexDirection: 'column', flexShrink: 0, backgroundColor: 'rgba(255,255,255,0.5)' }}>
                            <div style={{ padding: '1rem', borderBottom: '1px solid var(--mantine-color-gray-3)', backgroundColor: 'rgba(255,255,255,0.8)', borderTopLeftRadius: 'var(--mantine-radius-lg)', borderTopRightRadius: 'var(--mantine-radius-lg)' }}>
                                <Text fw={700} size="sm" c="dimmed" tt="uppercase" style={{ letterSpacing: '1px' }}>{col.title}</Text>
                            </div>
                            <ScrollArea style={{ flex: 1 }}>
                                <Stack gap={4} p="xs">
                                    {col.nodes.map((node) => {
                                        const isSelected = selectedPath[col.depth]?.id === node.id;
                                        return (
                                            <div
                                                key={node.id}
                                                onClick={() => handleSelect(node, col.depth)}
                                                style={{
                                                    padding: '0.75rem',
                                                    borderRadius: 'var(--mantine-radius-md)',
                                                    cursor: 'pointer',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'space-between',
                                                    backgroundColor: isSelected ? 'var(--mantine-primary-color-filled)' : 'transparent',
                                                    color: isSelected ? 'var(--mantine-color-white)' : 'var(--mantine-color-text)',
                                                    transition: 'all 0.2s ease',
                                                }}
                                                className={isSelected ? 'shadow-md transform scale-[1.02]' : 'hover:bg-black/5'}
                                            >
                                                <Group gap="xs">
                                                    <ThemeIcon
                                                        size="sm"
                                                        variant="transparent"
                                                        c={isSelected ? "white" : "dimmed"}
                                                    >
                                                        {getIcon(node.type)}
                                                    </ThemeIcon>
                                                    <Text span size="sm" fw={isSelected ? 600 : 500}>{node.name}</Text>
                                                    {node.grade && (
                                                        <Badge size="xs" variant={isSelected ? "white" : "light"} color={isSelected ? "dark" : "gray"}>
                                                            {node.grade}
                                                        </Badge>
                                                    )}
                                                </Group>
                                                {node.children && node.children.length > 0 && (
                                                    <IconChevronRight size={14} style={{ opacity: isSelected ? 1 : 0.4 }} />
                                                )}
                                            </div>
                                        );
                                    })}
                                </Stack>
                            </ScrollArea>
                        </Paper>
                    ))}
                </div>
            )}
        </Paper>
    );
}
