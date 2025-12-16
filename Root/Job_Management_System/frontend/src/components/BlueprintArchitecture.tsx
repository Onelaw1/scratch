"use client";

import { Paper, Text, Group, Box, ScrollArea, Button } from '@mantine/core';
import { IconZoomIn, IconZoomOut, IconMap2 } from '@tabler/icons-react';
import { motion } from 'framer-motion';
import { useState } from 'react';

// --- TYPES ---
interface WireframeNode {
    id: string;
    type: 'screen' | 'database';
    title: string;
    sub: string;
    x: number;
    y: number;
    w: number;
    h: number;
    items: string[]; // UI Components or DB Fields
}

interface WireframeEdge {
    from: string;
    to: string;
    color: string; // 'green' | 'orange' | 'purple' | 'gray'
    label?: string;
}

// --- DATA: THE BLUEPRINT ---
const NODES: WireframeNode[] = [
    // --- ROW 1: FRONTEND PAGES (SCREENS) ---
    {
        id: 'pg_overview', type: 'screen', title: 'System Overview', sub: '/system-overview',
        x: 50, y: 50, w: 220, h: 280,
        items: ['Hero Section', 'Biz Cap (13 Pillars)', 'App Services Map', 'Data Appendices']
    },
    {
        id: 'pg_workforce', type: 'screen', title: 'Workforce Analysis', sub: '/workforce-analysis',
        x: 350, y: 50, w: 220, h: 280,
        items: ['Headcount (TO) Chart', 'Gap Analysis Grid', 'Span of Control Viz', 'Simulate Action']
    },
    {
        id: 'pg_job', type: 'screen', title: 'Job Management', sub: '/job-management',
        x: 650, y: 50, w: 220, h: 280,
        items: ['Job List (Grid)', 'JD Editor (Form)', 'AI Generator (Modal)', 'Task Dictionary']
    },
    {
        id: 'pg_eval', type: 'screen', title: 'Evaluation', sub: '/performance',
        x: 950, y: 50, w: 220, h: 280,
        items: ['KPI Settings', '9-Box Calibration', 'Peer Review Form', 'Result Dashboard']
    },

    // --- ROW 2: BACKEND ENTITIES (DATABASE) ---
    {
        id: 'db_org', type: 'database', title: 'Org Unit', sub: 'public.org_units',
        x: 200, y: 450, w: 180, h: 200,
        items: ['id (PK)', 'name', 'parent_id (FK)', 'head_count']
    },
    {
        id: 'db_work', type: 'database', title: 'Workload', sub: 'public.workloads',
        x: 450, y: 450, w: 180, h: 200,
        items: ['id (PK)', 'user_id (FK)', 'task_id (FK)', 'fte_value']
    },
    {
        id: 'db_job', type: 'database', title: 'Job Position', sub: 'public.job_positions',
        x: 700, y: 450, w: 180, h: 200,
        items: ['id (PK)', 'title', 'ncs_code', 'grade_level']
    },
    {
        id: 'db_review', type: 'database', title: 'Perf Review', sub: 'public.reviews',
        x: 950, y: 450, w: 180, h: 200,
        items: ['id (PK)', 'target_id (FK)', 'score_perf', 'score_pot']
    },
];

const EDGES: WireframeEdge[] = [
    // GREEN: User Nav Flow
    { from: 'pg_overview', to: 'pg_workforce', color: 'green', label: 'Nav' },
    { from: 'pg_workforce', to: 'pg_job', color: 'green', label: 'Drill-down' },
    { from: 'pg_job', to: 'pg_eval', color: 'green', label: 'Linked' },

    // ORANGE: Data Read/Write (Page to DB)
    { from: 'pg_workforce', to: 'db_org', color: 'orange', label: 'Agg' },
    { from: 'pg_workforce', to: 'db_work', color: 'orange', label: 'Sum' },
    { from: 'pg_job', to: 'db_job', color: 'orange', label: 'CRUD' },
    { from: 'pg_eval', to: 'db_review', color: 'orange', label: 'Write' },

    // PURPLE: Entity Relations (DB to DB)
    { from: 'db_org', to: 'db_work', color: 'purple', label: 'Has' },
    { from: 'db_job', to: 'db_work', color: 'purple', label: 'Defines' },
    { from: 'db_job', to: 'db_review', color: 'purple', label: 'Ref' },
];

export function BlueprintArchitecture() {
    const [zoom, setZoom] = useState(1);

    return (
        <Paper p="md" withBorder radius="lg" bg="gray.0" mb="xl" style={{ overflow: 'hidden' }}>
            {/* Toolbar */}
            <Group justify="space-between" mb="md">
                <Group gap="xs">
                    <IconMap2 size={24} className="text-blue-600" />
                    <div>
                        <Text fw={700}>Comprehensive Blueprint Reference</Text>
                        <Text size="xs" c="dimmed">UX Wireflow + Data Schema Mapping</Text>
                    </div>
                </Group>
                <Group>
                    <Button size="xs" variant="default" onClick={() => setZoom(z => Math.max(0.5, z - 0.1))}><IconZoomOut size={14} /></Button>
                    <Text size="xs" fw={700} w={40} ta="center">{Math.round(zoom * 100)}%</Text>
                    <Button size="xs" variant="default" onClick={() => setZoom(z => Math.min(1.5, z + 0.1))}><IconZoomIn size={14} /></Button>
                </Group>
            </Group>

            {/* Canvas */}
            <ScrollArea h={600} bg="#f8f9fa" style={{ border: '1px solid #dee2e6', borderRadius: 8 }}>
                <Box
                    style={{
                        width: 1400,
                        height: 800,
                        position: 'relative',
                        transform: `scale(${zoom})`,
                        transformOrigin: 'top left',
                        // Graph paper background
                        backgroundImage: 'radial-gradient(#ced4da 1px, transparent 1px)',
                        backgroundSize: '20px 20px'
                    }}
                >
                    <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0, overflow: 'visible' }}>
                        <defs>
                            {['green', 'orange', 'purple', 'gray'].map(c => (
                                <marker key={c} id={`arrow-${c}`} markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                                    <polygon points="0 0, 10 3.5, 0 7" fill={getColor(c)} />
                                </marker>
                            ))}
                        </defs>

                        {EDGES.map((edge, i) => {
                            const s = NODES.find(n => n.id === edge.from)!;
                            const t = NODES.find(n => n.id === edge.to)!;

                            // Simple Manhattan routing logic
                            const sx = s.x + s.w / 2;
                            const sy = s.y + s.h; // From bottom
                            const tx = t.x + t.w / 2;
                            const ty = t.y; // To top

                            // If linking sideways (Page to Page)
                            const isSideways = s.y === t.y;

                            let d = "";
                            if (isSideways) {
                                // Right to Left
                                const sRx = s.x + s.w;
                                const sRy = s.y + s.h / 2;
                                const tLx = t.x;
                                const tLy = t.y + t.h / 2;
                                d = `M ${sRx} ${sRy} C ${sRx + 50} ${sRy}, ${tLx - 50} ${tLy}, ${tLx} ${tLy}`;
                            } else {
                                // Top to Bottom
                                const midY = (sy + ty) / 2;
                                d = `M ${sx} ${sy} L ${sx} ${midY} L ${tx} ${midY} L ${tx} ${ty}`;
                            }

                            return (
                                <g key={i}>
                                    <path
                                        d={d}
                                        stroke={getColor(edge.color)}
                                        strokeWidth={3}
                                        fill="none"
                                        markerEnd={`url(#arrow-${edge.color})`}
                                        strokeOpacity={0.7}
                                    />
                                    {edge.label && (
                                        <text x={(sx + tx) / 2} y={(sy + ty) / 2} fill={getColor(edge.color)} fontSize={10} fontWeight={700} textAnchor="middle" dy={-5} bg="white">
                                            {edge.label}
                                        </text>
                                    )}
                                </g>
                            )
                        })}
                    </svg>

                    {NODES.map((node) => (
                        <WireframeNode key={node.id} data={node} />
                    ))}

                </Box>
            </ScrollArea>
        </Paper>
    );
}

function WireframeNode({ data }: { data: WireframeNode }) {
    const isDb = data.type === 'database';
    const borderColor = isDb ? '#fab005' : '#ced4da'; // Orange for DB, Gray for Screen
    const headerBg = isDb ? '#fff9db' : '#fff';

    return (
        <Paper
            shadow="md"
            radius="sm"
            withBorder
            style={{
                position: 'absolute',
                left: data.x,
                top: data.y,
                width: data.w,
                height: data.h,
                borderColor: borderColor,
                borderTop: `4px solid ${isDb ? '#f08c00' : '#868e96'}`,
            }}
        >
            {/* Header */}
            <Box p="xs" bg={headerBg} style={{ borderBottom: '1px solid #eee' }}>
                <Text fw={700} size="sm" tt="uppercase" c={isDb ? 'orange.9' : 'dark'}>{data.title}</Text>
                <Text size="xs" c="dimmed" truncate>{data.sub}</Text>
            </Box>

            {/* Body (Wireframe Representation) */}
            <Box p="xs">
                {/* Mini UI Blocks */}
                {data.type === 'screen' ? (
                    <Group gap={8} style={{ flexDirection: 'column', alignItems: 'stretch' }}>
                        {/* Fake Nav Bar */}
                        <Box h={8} bg="gray.2" style={{ borderRadius: 2 }} w="100%" />
                        <Group>
                            <Box h={40} bg="gray.1" style={{ flex: 1, borderRadius: 4, border: '1px dashed #ced4da' }} />
                            <Box h={40} bg="gray.1" style={{ flex: 1, borderRadius: 4, border: '1px dashed #ced4da' }} />
                        </Group>
                        {/* Content Blocks */}
                        {data.items.map((item, i) => (
                            <Group key={i} gap={4} p={4} bg="gray.0" style={{ border: '1px solid #f1f3f5', borderRadius: 4 }}>
                                <Box w={6} h={6} bg="blue.2" style={{ borderRadius: '50%' }} />
                                <Text size="xs" c="dimmed">{item}</Text>
                            </Group>
                        ))}
                    </Group>
                ) : (
                    // DB Representation
                    <Box>
                        {data.items.map((item, i) => (
                            <Group key={i} justify="space-between" mb={4} p={2} style={{ borderBottom: '1px solid #f8f9fa' }}>
                                <Text size="xs" fw={500} c="dark.6">{item.split(' ')[0]}</Text>
                                <Text size="xs" c="dimmed" style={{ fontSize: 9 }}>{item.split(' ')[1]}</Text>
                            </Group>
                        ))}
                    </Box>
                )}
            </Box>
        </Paper>
    );
}

function getColor(c: string) {
    if (c === 'green') return '#20c997'; // TEAL/GREEN
    if (c === 'orange') return '#fd7e14';
    if (c === 'purple') return '#be4bdb';
    return '#adb5bd';
}
