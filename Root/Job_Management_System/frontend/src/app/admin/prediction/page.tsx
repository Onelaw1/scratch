"use client";

import React, { useState, useEffect } from "react";
import { Container, Title, Text, Group, Button, Loader, SimpleGrid, Paper, Badge, Stack, ThemeIcon, Progress, Table } from "@mantine/core";
import { IconBrain, IconAlertTriangle, IconBriefcase, IconTrendingUp } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function PredictionDashboard() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [predictions, setPredictions] = useState<Record<string, any>>({});
    const [recommendations, setRecommendations] = useState<Record<string, any[]>>({});

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const userList = await api.getUsers();
            setUsers(userList);

            // Fetch predictions for all users (Demo purpose)
            // In real app, only fetch for visible or selected
            const preds: Record<string, any> = {};
            const recs: Record<string, any[]> = {};

            for (const u of userList) {
                try {
                    const p = await api.getTurnoverRisk(u.id);
                    preds[u.id] = p;

                    const r = await api.getCareerRecommendations(u.id);
                    recs[u.id] = r;
                } catch (e) {
                    console.error(`Error fetching for ${u.name}`, e);
                }
            }
            setPredictions(preds);
            setRecommendations(recs);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleTrain = async () => {
        setLoading(true);
        try {
            await api.trainTurnoverModel();
            alert("Model retrained successfully!");
            loadData(); // Reload
        } catch (e) {
            alert("Training failed");
        } finally {
            setLoading(false);
        }
    };

    // Filter High Risk
    const highRiskUsers = users.filter(u => predictions[u.id]?.risk_level === "High");

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={2}>Predictive HR Analytics</Title>
                    <Text c="dimmed">AI-Driven Insights for Retention & Career Growth</Text>
                </div>
                <Button leftSection={<IconBrain size={16} />} onClick={handleTrain} loading={loading}>
                    Retrain Model
                </Button>
            </Group>

            {loading && users.length === 0 ? <Loader /> : (
                <SimpleGrid cols={2} spacing="lg">
                    {/* Retention Risk */}
                    <Paper withBorder p="md" radius="md">
                        <Group justify="space-between" mb="md">
                            <Title order={4}>Turnover Risk Monitor</Title>
                            <Badge color="red" size="lg">{highRiskUsers.length} High Risk</Badge>
                        </Group>

                        {highRiskUsers.length === 0 ? <Text c="dimmed">No high risk employees detected.</Text> :
                            <Table striped highlightOnHover>
                                <Table.Thead>
                                    <Table.Tr>
                                        <Table.Th>Name</Table.Th>
                                        <Table.Th>Risk Score</Table.Th>
                                        <Table.Th>Top Factor</Table.Th>
                                    </Table.Tr>
                                </Table.Thead>
                                <Table.Tbody>
                                    {highRiskUsers.map(u => {
                                        const pred = predictions[u.id];
                                        return (
                                            <Table.Tr key={u.id}>
                                                <Table.Td>{u.name}</Table.Td>
                                                <Table.Td>
                                                    <Badge color="red">{(pred.risk_score * 100).toFixed(0)}%</Badge>
                                                </Table.Td>
                                                <Table.Td>
                                                    <Text size="xs">
                                                        Rating: {pred.factors.rating}, OT: {pred.factors.overtime}h
                                                    </Text>
                                                </Table.Td>
                                            </Table.Tr>
                                        );
                                    })}
                                </Table.Tbody>
                            </Table>
                        }
                    </Paper>

                    {/* Career Recommendations */}
                    <Paper withBorder p="md" radius="md">
                        <Title order={4} mb="md">AI Career Recommendations</Title>
                        <ScrollArea h={300}>
                            <Stack>
                                {users.slice(0, 5).map(u => (
                                    <Paper key={u.id} p="xs" withBorder>
                                        <Text fw={500} size="sm" mb="xs">{u.name}</Text>
                                        {recommendations[u.id]?.length > 0 ? (
                                            <Stack gap="xs">
                                                {recommendations[u.id].map((req, idx) => (
                                                    <Group key={idx} justify="space-between">
                                                        <Group gap="xs">
                                                            <IconTrendingUp size={14} color="blue" />
                                                            <Text size="xs">{req.job_title}</Text>
                                                        </Group>
                                                        <Badge size="sm" variant="outline">{req.match_score}% Match</Badge>
                                                    </Group>
                                                ))}
                                            </Stack>
                                        ) : <Text size="xs" c="dimmed">No specific path found.</Text>}
                                    </Paper>
                                ))}
                            </Stack>
                        </ScrollArea>
                    </Paper>

                    {/* Feature Importance (Static for Demo) */}
                    <Paper withBorder p="md" radius="md" mt="md">
                        <Title order={4} mb="sm">Risk Factors Analysis</Title>
                        <Stack gap="xs">
                            <Group justify="space-between">
                                <Text size="sm">Low Compensation Ratio</Text>
                                <Progress value={80} color="red" size="sm" w={200} />
                            </Group>
                            <Group justify="space-between">
                                <Text size="sm">Consistent Overtime (&gt;10h)</Text>
                                <Progress value={65} color="orange" size="sm" w={200} />
                            </Group>
                            <Group justify="space-between">
                                <Text size="sm">Low Performance Rating</Text>
                                <Progress value={40} color="yellow" size="sm" w={200} />
                            </Group>
                        </Stack>
                    </Paper>
                </SimpleGrid>
            )}
        </Container>
    );
}

// Helper for ScrollArea
import { ScrollArea } from "@mantine/core";
