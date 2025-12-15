"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, Avatar, Table, Button, RingProgress, Divider
} from "@mantine/core";
import {
    IconTrophy, IconTrendingUp, IconUserCheck, IconRocket, IconRefresh
} from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function PromotionSimPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const loadData = async () => {
        setLoading(true);
        try {
            const res = await api.simulatePromotion();
            setData(res);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadData();
    }, []);

    if (loading) return <Container py="xl" className="flex justify-center"><Loader /></Container>;
    if (!data) return <Container py="xl"><Text c="red">Failed to load simulation data.</Text></Container>;

    const renderCandidateList = (scenario: any, color: string, icon: any) => (
        <Paper p="md" radius="md" withBorder className="h-full">
            <Group justify="space-between" mb="lg">
                <Group>
                    <ThemeIcon color={color} variant="light" size="lg">{icon}</ThemeIcon>
                    <div>
                        <Text fw={700} size="sm" tt="uppercase" c="dimmed">Strategy</Text>
                        <Title order={4}>{scenario.strategy}</Title>
                    </div>
                </Group>
                <div className="text-right">
                    <Text size="xs" fw={700} c="dimmed">Talent Density (Avg Slope)</Text>
                    <Text fw={700} size="xl" c={color}>+{scenario.avg_growth_slope}</Text>
                </div>
            </Group>

            <Divider my="sm" />

            <Stack gap="sm">
                {scenario.candidates.map((c: any, i: number) => (
                    <Paper key={c.user_id} p="sm" bg="gray.0" className="flex justify-between items-center">
                        <Group>
                            <Avatar color={color} radius="xl">{c.name.charAt(0)}</Avatar>
                            <div>
                                <Text fw={500} size="sm">{c.name}</Text>
                                <Text size="xs" c="dimmed">{c.position} • {c.tenure}y</Text>
                            </div>
                        </Group>
                        <div className="text-right">
                            <Badge variant="light" color={color} size="sm">Score: {c.current_score}</Badge>
                            <Text size="xs" c={color} fw={700} mt={2}>↗ {c.growth_slope}</Text>
                        </div>
                    </Paper>
                ))}
            </Stack>
        </Paper>
    );

    return (
        <Container size="xl" py="xl">
            <div className="mb-8 flex justify-between items-end">
                <div>
                    <Title order={1} className="flex items-center gap-3">
                        <ThemeIcon size={48} radius="xl" color="orange" variant="light">
                            <IconTrophy size={28} />
                        </ThemeIcon>
                        Promotion Simulation Game
                    </Title>
                    <Text c="dimmed" size="lg">What-If Analysis: Tenure (Traditional) vs Growth Slope (Scientific).</Text>
                </div>
                <Button leftSection={<IconRefresh size={16} />} onClick={loadData} variant="default">Re-Simulate</Button>
            </div>

            <Grid gutter="xl">
                {/* Scenario A: Traditional */}
                <Grid.Col span={{ base: 12, md: 6 }}>
                    {renderCandidateList(data.scenario_a, "gray", <IconUserCheck size={20} />)}
                </Grid.Col>

                {/* Scenario B: Scientific */}
                <Grid.Col span={{ base: 12, md: 6 }}>
                    {renderCandidateList(data.scenario_b, "orange", <IconTrendingUp size={20} />)}
                </Grid.Col>

                {/* Insight: Hidden Gems */}
                <Grid.Col span={12}>
                    <Paper p="xl" radius="md" withBorder className="bg-orange-50 border-orange-200">
                        <Group mb="md">
                            <ThemeIcon size={40} radius="xl" color="orange" variant="filled">
                                <IconRocket size={24} />
                            </ThemeIcon>
                            <div>
                                <Title order={3} c="orange.9">Hidden Gems Detected</Title>
                                <Text c="orange.8">High-Potential talent missed by Tenure-based strategy.</Text>
                            </div>
                        </Group>

                        {data.hidden_gems.length > 0 ? (
                            <Grid>
                                {data.hidden_gems.map((gem: any) => (
                                    <Grid.Col span={{ base: 12, md: 4 }} key={gem.user_id}>
                                        <Paper p="md" shadow="sm" radius="md" className="bg-white">
                                            <Group mb="xs">
                                                <Avatar size="md" color="orange">{gem.name.charAt(0)}</Avatar>
                                                <div>
                                                    <Text fw={600}>{gem.name}</Text>
                                                    <Text size="xs" c="dimmed">{gem.position} (Tenure: {gem.tenure}y)</Text>
                                                </div>
                                            </Group>
                                            <Group grow>
                                                <div className="text-center p-2 bg-gray-50 rounded">
                                                    <Text size="xs" c="dimmed">Current</Text>
                                                    <Text fw={700}>{gem.current_score}</Text>
                                                </div>
                                                <div className="text-center p-2 bg-orange-100 rounded">
                                                    <Text size="xs" c="orange.9">Slope</Text>
                                                    <Text fw={700} c="orange.9">+{gem.growth_slope}</Text>
                                                </div>
                                            </Group>
                                        </Paper>
                                    </Grid.Col>
                                ))}
                            </Grid>
                        ) : (
                            <Text c="dimmed" fs="italic">No hidden gems found in this simulation run. Both strategies aligned.</Text>
                        )}
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
