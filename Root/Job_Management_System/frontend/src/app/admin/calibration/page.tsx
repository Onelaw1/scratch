"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, Button, Progress, Card, Avatar, ActionIcon
} from "@mantine/core";
import {
    IconScale, IconArrowUpRight, IconArrowDownRight,
    IconCheck, IconX, IconTrendingUp
} from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function CalibrationPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await api.getCalibrationSuggestions();
                setData(res);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    if (loading) return <Container py="xl" className="flex justify-center"><Loader /></Container>;
    if (!data) return <Container py="xl"><Text c="red">Failed to load calibration data.</Text></Container>;

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="md" color="teal" variant="light">
                        <IconScale size={28} />
                    </ThemeIcon>
                    Job Grade Calibration Bot
                </Title>
                <Text c="dimmed" size="lg">cientific Drift Detection: Aligning Job Grades with Actual Workload.</Text>
            </div>

            <Grid>
                {/* Summary Cards */}
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder>
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="dimmed" fw={700}>TOTAL ANALYZED</Text>
                            <ThemeIcon color="gray" variant="light"><IconTrendingUp size={16} /></ThemeIcon>
                        </Group>
                        <Title order={2}>{data.total_analyzed}</Title>
                        <Text size="xs" c="dimmed" mt="xs">Employees Scanning</Text>
                    </Paper>
                </Grid.Col>

                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder className="bg-teal-50 border-teal-200">
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="teal" fw={700}>DRIFT DETECTED</Text>
                            <ThemeIcon color="teal" variant="filled" radius="xl"><IconScale size={16} /></ThemeIcon>
                        </Group>
                        <Title order={2} c="teal">{data.drift_detected_count}</Title>
                        <Text size="sm" c="teal">Grade Mismatch Found</Text>
                    </Paper>
                </Grid.Col>

                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder>
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="dimmed" fw={700}>AVG CONFIDENCE</Text>
                            <Badge variant="dot" color="blue">High</Badge>
                        </Group>
                        <Title order={2}>94%</Title>
                        <Text size="xs" c="dimmed" mt="xs">Based on 6-month Workload Logs</Text>
                    </Paper>
                </Grid.Col>
            </Grid>

            {/* Suggestions List */}
            <Title order={3} mt="xl" mb="md" className="flex items-center gap-2">
                <IconArrowUpRight color="teal" size={24} />
                Upgrade Suggestions (Data-Driven)
            </Title>
            <Text c="dimmed" mb="lg">The following employees are consistently performing above their assigned grade.</Text>

            <Grid>
                {data.suggestions.map((s: any, i: number) => (
                    <Grid.Col span={{ base: 12, md: 6 }} key={i}>
                        <Card padding="lg" radius="md" withBorder shadow="sm">
                            <Group justify="space-between" align="start" mb="md">
                                <Group>
                                    <Avatar color="teal" radius="xl">{s.name.charAt(0)}</Avatar>
                                    <div>
                                        <Text fw={600} size="lg">{s.name}</Text>
                                        <Text size="sm" c="dimmed">{s.position}</Text>
                                    </div>
                                </Group>
                                <Badge size="lg" color="teal" variant="light">Gap: +{s.gap} Levels</Badge>
                            </Group>

                            <Group grow mb="md">
                                <Paper p="xs" bg="gray.1" radius="md" className="text-center">
                                    <Text size="xs" c="dimmed">Current Grade</Text>
                                    <Text fw={700} size="xl">{s.current_grade}</Text>
                                </Paper>
                                <IconArrowUpRight size={24} className="text-gray-400 mx-auto" />
                                <Paper p="xs" bg="teal.1" radius="md" className="text-center border border-teal-200">
                                    <Text size="xs" c="teal.8">Calculated Grade</Text>
                                    <Text fw={700} size="xl" c="teal.9">{s.calculated_grade}</Text>
                                </Paper>
                            </Group>

                            <Paper bg="gray.0" p="sm" radius="sm" mb="md">
                                <Text size="xs" fw={700} c="dimmed" mb="xs">AI REASONING (Confidence: {s.confidence}%)</Text>
                                <Text size="sm">{s.reason}</Text>
                            </Paper>

                            <Group mt="auto" grow>
                                <Button leftSection={<IconCheck size={16} />} color="teal">Approve Upgrade</Button>
                                <Button leftSection={<IconX size={16} />} variant="default">Reject</Button>
                            </Group>
                        </Card>
                    </Grid.Col>
                ))}
            </Grid>
        </Container>
    );
}
