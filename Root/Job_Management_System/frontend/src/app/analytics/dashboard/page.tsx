"use client";

import { useEffect, useState } from 'react';
import { Container, Title, Grid, Paper, Text, Group, Badge, RingProgress, Center, Stack, ThemeIcon } from '@mantine/core';
import { IconUsers, IconHierarchy, IconChartBar, IconAlertTriangle, IconCheck, IconArrowUpRight } from '@tabler/icons-react';
import { analyticsApi } from '@/lib/api';

// --- Types ---
interface FillRateData {
    org_unit: string;
    authorized: number;
    actual: number;
    fill_rate: number;
}

interface SpanData {
    manager_name: string;
    job_title: string;
    grade: string;
    span: number;
}

export default function WorkforceAnalyticsDashboard() {
    const [fillRates, setFillRates] = useState<FillRateData[]>([]);
    const [spanData, setSpanData] = useState<SpanData[]>([]);
    const [loading, setLoading] = useState(true);

    // Hardcoded Institution ID for demo
    const INSTITUTION_ID = "INST-001";

    useEffect(() => {
        async function fetchData() {
            try {
                const [fill, span] = await Promise.all([
                    // Mocking the call if backend returns empty/error for now or real call
                    // analyticsApi.getHeadcountFillRate(INSTITUTION_ID, 2024),
                    // analyticsApi.getSpanOfControl(INSTITUTION_ID)

                    // For Demo UI immediately without waiting for DB seed:
                    Promise.resolve([
                        { org_unit: 'Management Support', authorized: 10, actual: 9, fill_rate: 90.0 },
                        { org_unit: 'R&D Division', authorized: 50, actual: 42, fill_rate: 84.0 },
                        { org_unit: 'Sales Dept', authorized: 30, actual: 30, fill_rate: 100.0 },
                        { org_unit: 'Customer Service', authorized: 20, actual: 15, fill_rate: 75.0 },
                    ]),
                    Promise.resolve([
                        { manager_name: 'David Kim', job_title: 'Head of R&D', grade: 'G1', span: 12 },
                        { manager_name: 'Sarah Lee', job_title: 'Sales Director', grade: 'G1', span: 8 },
                        { manager_name: 'Michael Chen', job_title: 'Support Clean', grade: 'G2', span: 15 }, // High!
                        { manager_name: 'Jessica Park', job_title: 'HR Manager', grade: 'G2', span: 4 },
                    ])
                ]);

                setFillRates(fill as FillRateData[]);
                setSpanData(span as SpanData[]);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    // --- Calculations ---
    const avgFillRate = fillRates.reduce((acc, curr) => acc + curr.fill_rate, 0) / (fillRates.length || 1);
    const avgSpan = spanData.reduce((acc, curr) => acc + curr.span, 0) / (spanData.length || 1);

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2}>Strategic Workforce Analytics</Title>
                    <Text c="dimmed">Optimization Dashboard: Headcount & Org Efficiency</Text>
                </div>
                <Badge size="lg" color="dark" variant="filled">2025 Plan</Badge>
            </Group>

            {/* KPI Cards */}
            <Grid mb="xl">
                <Grid.Col span={4}>
                    <Paper withBorder p="md" radius="md">
                        <Group justify="space-between">
                            <Text size="xs" c="dimmed" fw={700} tt="uppercase">Avg Fill Rate</Text>
                            <ThemeIcon color="blue" variant="light"><IconUsers size={16} /></ThemeIcon>
                        </Group>
                        <Group align="flex-end" gap="xs" mt="sm">
                            <Text fz="2rem" fw={700}>{avgFillRate.toFixed(1)}%</Text>
                            <Badge color={avgFillRate < 90 ? 'yellow' : 'teal'} variant="light">
                                {avgFillRate < 90 ? 'Understaffed' : 'Healthy'}
                            </Badge>
                        </Group>
                    </Paper>
                </Grid.Col>
                <Grid.Col span={4}>
                    <Paper withBorder p="md" radius="md">
                        <Group justify="space-between">
                            <Text size="xs" c="dimmed" fw={700} tt="uppercase">Avg Span of Control</Text>
                            <ThemeIcon color="grape" variant="light"><IconHierarchy size={16} /></ThemeIcon>
                        </Group>
                        <Group align="flex-end" gap="xs" mt="sm">
                            <Text fz="2rem" fw={700}>{avgSpan.toFixed(1)}</Text>
                            <Text size="sm" c="dimmed" pb={4}>reports / manager</Text>
                        </Group>
                    </Paper>
                </Grid.Col>
                <Grid.Col span={4}>
                    <Paper withBorder p="md" radius="md">
                        <Group justify="space-between">
                            <Text size="xs" c="dimmed" fw={700} tt="uppercase">Org Efficiency</Text>
                            <ThemeIcon color="orange" variant="light"><IconChartBar size={16} /></ThemeIcon>
                        </Group>
                        <Group align="flex-end" gap="xs" mt="sm">
                            <Text fz="2rem" fw={700}>B+</Text>
                            <Text size="sm" c="dimmed" pb={4}>System Score</Text>
                        </Group>
                    </Paper>
                </Grid.Col>
            </Grid>

            <Grid>
                {/* 1. Headcount Fill Rate (Bar Chart Visual) */}
                <Grid.Col span={6}>
                    <Paper withBorder p="md" radius="md" h="100%">
                        <Title order={4} mb="md">Headcount Fill Rate by Unit</Title>
                        <Stack gap="md">
                            {fillRates.map(item => (
                                <div key={item.org_unit}>
                                    <Group justify="space-between" mb={4}>
                                        <Text size="sm" fw={500}>{item.org_unit}</Text>
                                        <Text size="sm">{item.fill_rate}% ({item.actual}/{item.authorized})</Text>
                                    </Group>
                                    <div style={{ height: 8, background: '#f1f3f5', borderRadius: 4, overflow: 'hidden' }}>
                                        <div style={{ height: '100%', width: `${Math.min(item.fill_rate, 100)}%`, background: item.fill_rate < 80 ? '#fab005' : '#20c997' }} />
                                    </div>
                                </div>
                            ))}
                        </Stack>
                    </Paper>
                </Grid.Col>

                {/* 2. Span of Control Analysis */}
                <Grid.Col span={6}>
                    <Paper withBorder p="md" radius="md" h="100%">
                        <Group justify="space-between" mb="md">
                            <Title order={4}>Span of Control Analysis</Title>
                            <Badge color="red" variant="dot">High Risk: {'>'} 12</Badge>
                        </Group>

                        <Stack gap="xs">
                            {spanData.map((mgr, idx) => (
                                <Paper key={idx} withBorder p="xs" bg={mgr.span > 12 ? 'red.0' : 'gray.0'}>
                                    <Group justify="space-between">
                                        <Group gap="sm">
                                            <ThemeIcon color={mgr.span > 12 ? 'red' : 'gray'} variant="transparent">
                                                {mgr.span > 12 ? <IconAlertTriangle size={18} /> : <IconCheck size={18} />}
                                            </ThemeIcon>
                                            <div>
                                                <Text size="sm" fw={600}>{mgr.manager_name}</Text>
                                                <Text size="xs" c="dimmed">{mgr.job_title} ({mgr.grade})</Text>
                                            </div>
                                        </Group>
                                        <Group gap="xs">
                                            <Text fw={700} c={mgr.span > 12 ? 'red.7' : 'dark'}>{mgr.span}</Text>
                                            <Text size="xs" c="dimmed">reports</Text>
                                        </Group>
                                    </Group>
                                </Paper>
                            ))}
                        </Stack>
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
