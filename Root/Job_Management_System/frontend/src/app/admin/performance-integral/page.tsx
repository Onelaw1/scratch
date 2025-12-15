"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, Avatar, Table, RingProgress
} from "@mantine/core";
import {
    IconChartAreaLine, IconTrophy, IconTrendingUp,
    IconActivity
} from "@tabler/icons-react";
import { api } from "@/lib/api";

// Simple Bar Chart Component for visual representation
const MockAreaChart = ({ data }: { data: any[] }) => {
    const maxVal = 5.0;
    return (
        <div className="h-64 flex items-end justify-between gap-2 mt-4 px-4 bg-gray-50 rounded-lg border border-gray-100 p-4">
            {data.map((d, i) => (
                <div key={i} className="flex flex-col items-center w-full group">
                    {/* Tooltip */}
                    <div className="mb-2 opacity-0 group-hover:opacity-100 transition-opacity bg-black text-white text-xs rounded px-2 py-1">
                        {d.score} ({d.grade})
                    </div>
                    {/* Bar (simulating area point) */}
                    <div
                        className="w-full bg-violet-400 rounded-t-md transition-all hover:bg-violet-600 relative overflow-hidden"
                        style={{ height: `${(d.score / maxVal) * 100}%` }}
                    >
                        <div className="absolute bottom-0 w-full bg-violet-500 opacity-20" style={{ height: `${(d.cumulative / 25) * 100}%` }}></div>
                    </div>
                    <Text size="xs" c="dimmed" mt={1}>{d.year}</Text>
                </div>
            ))}
        </div>
    );
};

export default function PerformanceIntegralPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await api.getPerformanceIntegral("all"); // Get leaderboard
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
    if (!data) return <Container py="xl"><Text c="red">Failed to load performance data.</Text></Container>;

    const topPerformer = data.top_performers[0];

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="xl" color="violet" variant="light">
                        <IconChartAreaLine size={28} />
                    </ThemeIcon>
                    Performance Integral Dashboard
                </Title>
                <Text c="dimmed" size="lg">Scientific Long-term Analysis: Reward Consistency over Recency.</Text>
            </div>

            <Grid>
                {/* Hero Card: The Long-Term Champion */}
                <Grid.Col span={12}>
                    <Paper p="xl" radius="md" withBorder className="bg-gradient-to-r from-violet-50 to-white">
                        <Grid align="center">
                            <Grid.Col span={{ base: 12, md: 8 }}>
                                <Group align="flex-start">
                                    <Avatar size="xl" color="violet" radius="xl">{topPerformer?.name.charAt(0)}</Avatar>
                                    <div>
                                        <Badge color="violet" size="lg" mb="sm">Top Consistent Performer (5y)</Badge>
                                        <Title order={2}>{topPerformer?.name}</Title>
                                        <Text c="dimmed">{topPerformer?.position}</Text>

                                        <Group mt="md" gap="xl">
                                            <div>
                                                <Text size="xs" c="dimmed" fw={700}>TOTAL INTEGRAL</Text>
                                                <Text size="xl" fw={700} c="violet">{topPerformer?.total_integral}</Text>
                                            </div>
                                            <div>
                                                <Text size="xs" c="dimmed" fw={700}>AVG SCORE</Text>
                                                <Text size="xl" fw={700}>{topPerformer?.avg_score}</Text>
                                            </div>
                                            <div>
                                                <Text size="xs" c="dimmed" fw={700}>PERSONA</Text>
                                                <Badge variant="dot" color="teal">{topPerformer?.persona}</Badge>
                                            </div>
                                        </Group>
                                    </div>
                                </Group>
                            </Grid.Col>
                            <Grid.Col span={{ base: 12, md: 4 }}>
                                <Text size="sm" fw={700} ta="center" c="dimmed" mb="xs">5-Year Performance Curve (Area)</Text>
                                <MockAreaChart data={topPerformer.history} />
                            </Grid.Col>
                        </Grid>
                    </Paper>
                </Grid.Col>

                {/* Leaderboard */}
                <Grid.Col span={12}>
                    <Title order={3} mt="xl" mb="md" className="flex items-center gap-2">
                        <IconTrophy color="gold" size={24} />
                        Consistency Leaderboard (Cumulative)
                    </Title>
                    <Paper withBorder radius="md">
                        <Table striped highlightOnHover>
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Rank</Table.Th>
                                    <Table.Th>Employee</Table.Th>
                                    <Table.Th>Position</Table.Th>
                                    <Table.Th>Persona (AI)</Table.Th>
                                    <Table.Th>Avg Score (5y)</Table.Th>
                                    <Table.Th>Total Integral (Value)</Table.Th>
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {data.top_performers.map((user: any, index: number) => (
                                    <Table.Tr key={user.user_id}>
                                        <Table.Td>
                                            <Badge
                                                circle
                                                color={index < 3 ? "yellow" : "gray"}
                                                variant={index < 3 ? "filled" : "light"}
                                            >
                                                {index + 1}
                                            </Badge>
                                        </Table.Td>
                                        <Table.Td fw={500}>{user.name}</Table.Td>
                                        <Table.Td c="dimmed">{user.position}</Table.Td>
                                        <Table.Td>
                                            <Badge
                                                color={user.persona === 'CONSISTENT_HIGH' ? 'teal' : 'blue'}
                                                variant="outline"
                                            >
                                                {user.persona}
                                            </Badge>
                                        </Table.Td>
                                        <Table.Td>{user.avg_score}</Table.Td>
                                        <Table.Td fw={700}>{user.total_integral}</Table.Td>
                                    </Table.Tr>
                                ))}
                            </Table.Tbody>
                        </Table>
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
