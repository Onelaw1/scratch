"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, RingProgress, Progress, Card
} from "@mantine/core";
import {
    IconScale, IconGenderFemale, IconGenderMale,
    IconChartBar, IconAlertTriangle, IconUserCancel
} from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function FairnessDashboardPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAnalysis = async () => {
            try {
                const res = await api.getFairnessAnalysis();
                setData(res);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        loadAnalysis();
    }, []);

    // Helper for Pay Gap Badge
    const getGapBadge = (gap: number) => {
        if (Math.abs(gap) < 5) return <Badge color="teal">Balanced ({gap}%)</Badge>;
        if (Math.abs(gap) < 15) return <Badge color="yellow">Moderate ({gap}%)</Badge>;
        return <Badge color="red">Significant Gap ({gap}%)</Badge>;
    };

    if (loading) {
        return (
            <Container size="xl" py="xl" className="flex justify-center h-[50vh] items-center">
                <Loader size="xl" type="dots" />
            </Container>
        );
    }

    if (!data) return <Container><Text color="red">Failed to load data.</Text></Container>;

    const m = data.metrics;

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="md" color="grape" variant="light">
                        <IconScale size={28} />
                    </ThemeIcon>
                    Fairness & DEI Dashboard
                </Title>
                <Text c="dimmed" size="lg">Monitor Pay Equity and Demographic Balance.</Text>
            </div>

            <Grid>
                {/* Top Metrics */}
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder>
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="dimmed" fw={700}>GENDER PAY GAP</Text>
                            <ThemeIcon color={m.gender_pay_gap_pct > 0 ? "blue" : "pink"} variant="light" radius="xl">
                                {m.gender_pay_gap_pct > 0 ? <IconGenderMale size={16} /> : <IconGenderFemale size={16} />}
                            </ThemeIcon>
                        </Group>
                        <Title order={2}>{m.gender_pay_gap_pct.toFixed(2)}%</Title>
                        <Text size="xs" c="dimmed" mb="md">
                            Difference between Median Male vs Female Salary
                        </Text>
                        {getGapBadge(m.gender_pay_gap_pct)}
                    </Paper>
                </Grid.Col>

                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder>
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="dimmed" fw={700}>AVG SALARY (M vs F)</Text>
                            <IconChartBar size={20} className="text-gray-400" />
                        </Group>
                        <Stack gap="xs">
                            <div>
                                <Group justify="space-between">
                                    <Text size="sm">Male</Text>
                                    <Text size="sm" fw={700}>{(m.avg_salary_male / 1000000).toFixed(1)}M</Text>
                                </Group>
                                <Progress value={100} color="blue" size="sm" />
                            </div>
                            <div>
                                <Group justify="space-between">
                                    <Text size="sm">Female</Text>
                                    <Text size="sm" fw={700}>{(m.avg_salary_female / 1000000).toFixed(1)}M</Text>
                                </Group>
                                <Progress value={(m.avg_salary_female / m.avg_salary_male) * 100} color="pink" size="sm" />
                            </div>
                        </Stack>
                    </Paper>
                </Grid.Col>

                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="lg" radius="md" withBorder>
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" c="dimmed" fw={700}>AGE CORRELATION</Text>
                            <ThemeIcon color="orange" variant="light"><IconAlertTriangle size={16} /></ThemeIcon>
                        </Group>
                        <Group align="flex-end" gap="xs">
                            <Title order={2}>{m.age_pay_correlation}</Title>
                            <Text size="sm" mb={4} c="dimmed">(Pearson R)</Text>
                        </Group>
                        <Text size="xs" c="dimmed" mt="xs">
                            Low correlation ({'<'}0.3) indicates success in moving away from Seniority-based pay.
                        </Text>
                    </Paper>
                </Grid.Col>

                {/* Outliers Section */}
                <Grid.Col span={12}>
                    <Title order={3} mb="md" mt="xl">Risk Detection (Outliers)</Title>
                    {data.outliers.length > 0 ? (
                        <Grid>
                            {data.outliers.map((o: any, i: number) => (
                                <Grid.Col span={{ base: 12, md: 6, lg: 4 }} key={i}>
                                    <Card shadow="sm" padding="lg" radius="md" withBorder>
                                        <Group justify="space-between" mb="xs">
                                            <Badge color="red" variant="light">Flight Risk</Badge>
                                            <IconUserCancel size={20} color="gray" />
                                        </Group>
                                        <Text fw={500}>{o.name}</Text>
                                        <Text size="sm" c="dimmed" mb="sm">{o.issue}</Text>
                                        <Paper p="xs" bg="gray.1">
                                            <Text size="xs" color="dimmed" style={{ fontFamily: 'monospace' }}>
                                                {o.details}
                                            </Text>
                                        </Paper>
                                    </Card>
                                </Grid.Col>
                            ))}
                        </Grid>
                    ) : (
                        <Paper p="xl" withBorder className="bg-gray-50 text-center">
                            <Text c="dimmed">No significant outliers detected.</Text>
                        </Paper>
                    )}
                </Grid.Col>
            </Grid>
        </Container>
    );
}
