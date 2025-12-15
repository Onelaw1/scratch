"use client";

import React, { useState, useEffect } from "react";
import { Container, Title, Text, Group, Select, Loader, SimpleGrid, Paper, Badge, Stack, ThemeIcon } from "@mantine/core";
import { IconCheck, IconAlertCircle } from "@tabler/icons-react";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from "recharts";
import { api } from "@/lib/api";

export default function CompetencyRadarPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        api.getUsers().then((res: any) => {
            setUsers(res);
            if (res.length > 0) setSelectedUserId(res[0].id);
        });
    }, []);

    useEffect(() => {
        if (!selectedUserId) return;
        setLoading(true);
        api.getCompetencyRadar(selectedUserId)
            .then(setData)
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [selectedUserId]);

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={2}>Competency Fit Radar</Title>
                    <Text c="dimmed">Job-Person Fit Analysis</Text>
                </div>
                <Select
                    data={users.map(u => ({ value: u.id, label: u.name }))}
                    value={selectedUserId}
                    onChange={setSelectedUserId}
                    placeholder="Select Employee"
                    searchable
                />
            </Group>

            {loading ? <Loader /> : !selectedUserId ? <Text>Please select a user.</Text> : data && (
                <SimpleGrid cols={2} spacing="lg">
                    {/* Charts */}
                    <Paper withBorder p="md" radius="md">
                        <Title order={4} mb="md" ta="center">Fit Score: {data.fit_score}%</Title>
                        <div style={{ width: '100%', height: 400 }}>
                            <ResponsiveContainer>
                                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data.radar_data}>
                                    <PolarGrid />
                                    <PolarAngleAxis dataKey="skill" />
                                    <PolarRadiusAxis angle={30} domain={[0, 5]} />
                                    <Radar name="Required" dataKey="required" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
                                    <Radar name="Actual" dataKey="actual" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.5} />
                                    <Legend />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </Paper>

                    {/* Analysis */}
                    <Stack>
                        <Paper withBorder p="md" radius="md">
                            <Group justify="space-between" mb="sm">
                                <Title order={4}>Gaps & Training Needs</Title>
                                <Badge color="red">{data.analysis?.gaps.length || 0} Issues</Badge>
                            </Group>
                            {!data.analysis?.gaps.length ? <Text c="dimmed">No significant gaps found.</Text> :
                                <Stack gap="xs">
                                    {data.analysis.gaps.map((gap: any, idx: number) => (
                                        <Paper key={idx} withBorder p="xs" bg="var(--mantine-color-red-0)">
                                            <Group>
                                                <ThemeIcon color="red" variant="light"><IconAlertCircle size={16} /></ThemeIcon>
                                                <div style={{ flex: 1 }}>
                                                    <Text size="sm" fw={500}>{gap.skill}</Text>
                                                    <Text size="xs" c="red">{gap.action} (Gap: {gap.gap})</Text>
                                                </div>
                                            </Group>
                                        </Paper>
                                    ))}
                                </Stack>
                            }
                        </Paper>

                        <Paper withBorder p="md" radius="md">
                            <Group justify="space-between" mb="sm">
                                <Title order={4}>Strengths</Title>
                                <Badge color="teal">{data.analysis?.strengths.length || 0} Areas</Badge>
                            </Group>
                            {!data.analysis?.strengths.length ? <Text c="dimmed">No specific strengths identified.</Text> :
                                <Stack gap="xs">
                                    {data.analysis.strengths.map((str: any, idx: number) => (
                                        <Paper key={idx} withBorder p="xs" bg="var(--mantine-color-teal-0)">
                                            <Group>
                                                <ThemeIcon color="teal" variant="light"><IconCheck size={16} /></ThemeIcon>
                                                <div style={{ flex: 1 }}>
                                                    <Text size="sm" fw={500}>{str.skill}</Text>
                                                    <Text size="xs" c="teal">{str.action} (+{str.surplus})</Text>
                                                </div>
                                            </Group>
                                        </Paper>
                                    ))}
                                </Stack>
                            }
                        </Paper>
                    </Stack>
                </SimpleGrid>
            )}
        </Container>
    );
}
