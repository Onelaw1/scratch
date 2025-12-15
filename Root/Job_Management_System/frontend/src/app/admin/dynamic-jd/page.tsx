"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Paper, Table, Group, Badge, Button, Loader, Tooltip, SimpleGrid, Card, Progress, RingProgress, Center, ThemeIcon, Alert, ActionIcon, Grid } from "@mantine/core";
import { IconBriefcase, IconRefresh, IconCheck, IconTrash, IconArrowRight, IconAlertTriangle, IconPlus, IconMinus } from "@tabler/icons-react";
import { api } from "@/lib/api";

type TaskSuggestion = {
    task_name: string;
    task_id?: string;
    reason: string;
    confidence: number;
};

type DynamicJDData = {
    job_id: string;
    job_title: string;
    analyzed_at: string;
    drift_score: number;
    status: string;
    current_jd_summary: string[];
    suggestions: {
        add: TaskSuggestion[];
        remove: TaskSuggestion[];
    };
};

export default function DynamicJDPage() {
    // For demo, we hardcode a job ID
    const JOB_ID = "job-marketing-01";
    const [data, setData] = useState<DynamicJDData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getDynamicJDAnalysis(JOB_ID)
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Container size="xl" py="xl"><Loader /></Container>;
    if (!data) return <Container size="xl" py="xl"><Text>No data available.</Text></Container>;

    return (
        <Container size="xl" py="xl">
            {/* Header */}
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>Dynamic JD Generator</Title>
                    <Text c="dimmed">
                        Analyzing Workload Logs to keep Job Descriptions alive.
                    </Text>
                </div>
                <Group>
                    <Badge size="lg" variant={data.status === "high_drift" ? "filled" : "outline"} color={data.status === "high_drift" ? "red" : "green"}>
                        {data.status === "high_drift" ? "High Drift Detected" : "Stable"}
                    </Badge>
                    <Button leftSection={<IconRefresh size={16} />} variant="light">Re-Analyze</Button>
                </Group>
            </Group>

            {/* Alert */}
            {data.drift_score > 0 && (
                <Alert icon={<IconAlertTriangle size={16} />} title="Action Required" color="red" mb="xl">
                    We found {data.drift_score} discrepancies between the official JD and actual work logs. Review suggestions below.
                </Alert>
            )}

            <Grid gutter="xl">
                {/* Left: Current JD (Theory) */}
                <Grid.Col span={5}>
                    <Paper withBorder p="md" radius="md" h="100%">
                        <Group mb="md">
                            <ThemeIcon size="lg" radius="md" variant="light" color="gray">
                                <IconBriefcase size={20} />
                            </ThemeIcon>
                            <Text fw={700}>Current Official JD</Text>
                        </Group>
                        <Text size="sm" c="dimmed" mb="md">As defined in the system.</Text>

                        {data.current_jd_summary.map((task, idx) => {
                            const isObsolete = data.suggestions.remove.some(r => r.task_name === task);
                            return (
                                <Paper key={idx} withBorder p="sm" mb="sm" style={{ opacity: isObsolete ? 0.5 : 1, borderColor: isObsolete ? 'red' : undefined }}>
                                    <Group justify="space-between">
                                        <Text size="sm" td={isObsolete ? 'line-through' : undefined}>{task}</Text>
                                        {isObsolete && <Badge color="red" size="xs">Obsolete</Badge>}
                                    </Group>
                                </Paper>
                            );
                        })}
                    </Paper>
                </Grid.Col>

                {/* Middle: Drift Analysis */}
                <Grid.Col span={2}>
                    <Center h="100%">
                        <Group justify="center" align="center" style={{ flexDirection: 'column' }}>
                            <IconArrowRight size={32} color="gray" />
                            <Badge size="lg" circle>{data.drift_score}</Badge>
                            <Text size="xs" c="dimmed">Changes</Text>
                        </Group>
                    </Center>
                </Grid.Col>

                {/* Right: Suggested Changes (Reality) */}
                <Grid.Col span={5}>
                    <Paper withBorder p="md" radius="md" h="100%" style={{ borderColor: data.drift_score > 0 ? '#fa5252' : undefined }}>
                        <Group mb="md">
                            <ThemeIcon size="lg" radius="md" variant="light" color="blue">
                                <IconRefresh size={20} />
                            </ThemeIcon>
                            <Text fw={700}>System Suggestions</Text>
                        </Group>
                        <Text size="sm" c="dimmed" mb="md">Based on 90-day Workload Logs.</Text>

                        {/* Add Suggestions */}
                        {data.suggestions.add.map((item, idx) => (
                            <Card key={`add-${idx}`} withBorder shadow="sm" radius="md" mb="sm" padding="sm" style={{ borderColor: 'green' }}>
                                <Group justify="space-between" mb="xs">
                                    <Badge color="green" leftSection={<IconPlus size={12} />}>New Task Found</Badge>
                                    <Badge variant="outline" color="gray">{item.confidence}% Conf.</Badge>
                                </Group>
                                <Text fw={600} size="sm" mb={4}>{item.task_name}</Text>
                                <Text size="xs" c="dimmed" mb="sm">{item.reason}</Text>
                                <Button fullWidth size="xs" color="green" variant="light" leftSection={<IconCheck size={14} />}>
                                    Add to JD
                                </Button>
                            </Card>
                        ))}

                        {/* Remove Suggestions */}
                        {data.suggestions.remove.map((item, idx) => (
                            <Card key={`rem-${idx}`} withBorder shadow="sm" radius="md" mb="sm" padding="sm" style={{ borderColor: 'red' }}>
                                <Group justify="space-between" mb="xs">
                                    <Badge color="red" leftSection={<IconMinus size={12} />}>Obsolete Task</Badge>
                                    <Badge variant="outline" color="gray">{item.confidence}% Conf.</Badge>
                                </Group>
                                <Text fw={600} size="sm" mb={4}>{item.task_name}</Text>
                                <Text size="xs" c="dimmed" mb="sm">{item.reason}</Text>
                                <Button fullWidth size="xs" color="red" variant="light" leftSection={<IconTrash size={14} />}>
                                    Remove from JD
                                </Button>
                            </Card>
                        ))}

                        {data.suggestions.add.length === 0 && data.suggestions.remove.length === 0 && (
                            <Alert color="green" icon={<IconCheck size={16} />}>
                                JD is perfectly synced with reality.
                            </Alert>
                        )}
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
