"use client";

import React, { useState } from "react";
import {
    Container, Title, Text, Button, Group, Paper, Stack,
    ThemeIcon, Grid, RingProgress, Badge, Table, Alert
} from "@mantine/core";
import {
    IconChartPie, IconBrain, IconArrowRight, IconAlertTriangle, IconCheck, IconBulb
} from "@tabler/icons-react";
import { api } from "@/lib/api";

const MOCK_TASKS = [
    { task_name: "Respond to client emails", fte: 0.2, action_verb: "respond" },
    { task_name: "Schedule team meetings", fte: 0.1, action_verb: "schedule" },
    { task_name: "Prepare weekly reports", fte: 0.3, action_verb: "prepare" },
    { task_name: "File expense reports", fte: 0.1, action_verb: "file" },
    { task_name: "Coordinate office supplies", fte: 0.1, action_verb: "coordinate" },

    { task_name: "Develop strategic roadmap", fte: 0.4, action_verb: "develop" },
    { task_name: "Present vision to board", fte: 0.2, action_verb: "present" },
    { task_name: "Lead quarterly planning", fte: 0.3, action_verb: "lead" },

    { task_name: "Debug server api", fte: 0.4, action_verb: "debug" },
    { task_name: "Fix login bug", fte: 0.2, action_verb: "fix" }
];

export default function GapAnalysisPage() {
    const [analysis, setAnalysis] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        setLoading(true);
        try {
            const result = await api.analyzeWorkload(MOCK_TASKS);
            setAnalysis(result);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="lg" py="xl">
            {/* Header */}
            <div className="text-center mb-10">
                <ThemeIcon size={64} radius="xl" variant="light" color="orange" className="mb-4">
                    <IconChartPie size={32} />
                </ThemeIcon>
                <Title order={1}>Smart Workload & Gap Analysis</Title>
                <Text c="dimmed">
                    AI automatically clusters scattered tasks into "Duties" and identifies staffing gaps.
                </Text>
            </div>

            {/* Control Panel */}
            <Paper p="xl" radius="md" withBorder className="mb-8 bg-gray-50">
                <Group justify="space-between">
                    <div>
                        <Title order={4}>Data Source</Title>
                        <Text size="sm" c="dimmed">Loaded 10 raw tasks from Survey (Simulated)</Text>
                    </div>
                    <Button
                        size="md"
                        color="orange"
                        leftSection={<IconBrain size={18} />}
                        onClick={handleAnalyze}
                        loading={loading}
                    >
                        Run AI Clustering
                    </Button>
                </Group>
            </Paper>

            {/* Results Grid */}
            <Grid gutter="lg">
                {analysis.map((cluster, idx) => (
                    <Grid.Col key={idx} span={{ base: 12, md: 6 }}>
                        <Paper radius="md" withBorder p="lg" className="h-full border-t-4 border-t-orange-400 hover:shadow-md transition-shadow">
                            <Group justify="space-between" mb="md">
                                <div>
                                    <Badge color="orange" size="lg" mb="xs">{cluster.duty_name}</Badge>
                                    <Text fw={700} size="xl">{cluster.fte_sum} FTE</Text>
                                </div>
                                <RingProgress
                                    size={80}
                                    thickness={8}
                                    sections={[{ value: Math.min(cluster.fte_sum * 100, 100), color: 'orange' }]}
                                    label={
                                        <Text c="dimmed" fw={700} ta="center" size="xs">
                                            {Math.round(cluster.fte_sum * 100)}%
                                        </Text>
                                    }
                                />
                            </Group>

                            {/* Recommendation Alert */}
                            <Alert
                                title="AI Recommendation"
                                color={cluster.fte_sum > 1.0 ? 'red' : 'blue'}
                                icon={<IconBulb size={16} />}
                                className="mb-4"
                            >
                                {cluster.recommendation}
                            </Alert>

                            {/* Task Breakdown */}
                            <Text size="sm" fw={700} c="dimmed" mb="xs">CLUSTERED TASKS:</Text>
                            <Table withTableBorder withRowBorders={false} horizontalSpacing="xs">
                                <Table.Tbody>
                                    {cluster.tasks.map((t: any, i: number) => (
                                        <Table.Tr key={i}>
                                            <Table.Td><IconCheck size={14} className="text-gray-400" /></Table.Td>
                                            <Table.Td>{t.task_name}</Table.Td>
                                            <Table.Td align="right" c="dimmed">{t.fte} FTE</Table.Td>
                                        </Table.Tr>
                                    ))}
                                </Table.Tbody>
                            </Table>
                        </Paper>
                    </Grid.Col>
                ))}
            </Grid>

            {!loading && analysis.length === 0 && (
                <div className="text-center py-20 text-gray-400">
                    <IconBrain size={48} className="mb-4 text-gray-300 mx-auto" />
                    <Text>Click "Run AI Clustering" to analyze workload patterns.</Text>
                </div>
            )}
        </Container>
    );
}
