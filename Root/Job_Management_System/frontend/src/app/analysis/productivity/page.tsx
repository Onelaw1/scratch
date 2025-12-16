
'use client';

import { useState, useEffect } from 'react';
import { Container, Title, Paper, Group, Text, Grid, Card, RingProgress, Center, Loader, Alert } from '@mantine/core';
import { IconCoin, IconUsers, IconChartBar, IconAlertCircle } from '@tabler/icons-react';

// Types
interface ProductivityMetric {
    year: number;
    revenue: number;
    operating_expenses: number;
    personnel_costs: number;
    net_income: number;
    hcroi: number;
    hcva: number;
}

export default function ProductivityPage() {
    const [metrics, setMetrics] = useState<ProductivityMetric[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Fetch data from backend
        // Assuming backend is running on localhost:8000 and we have a proxy or direct call
        // For demo simplicity, hardcoding institution ID 'inst_1' which we seeded.
        fetch('http://localhost:8000/productivity/metrics/inst_1')
            .then(res => {
                if (!res.ok) throw new Error('Failed to fetch data');
                return res.json();
            })
            .then(data => {
                setMetrics(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setError('Failed to load productivity metrics. Ensure backend is running.');
                setLoading(false);
            });
    }, []);

    if (loading) {
        return (
            <Center h={400}>
                <Loader size="xl" />
            </Center>
        );
    }

    if (error) {
        return (
            <Container size="xl" py="xl">
                <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
                    {error}
                </Alert>
            </Container>
        )
    }

    // Get latest year
    const latest = metrics[0];

    return (
        <Container size="xl" py="xl">
            <Title order={2} mb="lg">Productivity Metrics (HCROI/HCVA)</Title>

            {latest ? (
                <Grid>
                    <Grid.Col span={6}>
                        <Card shadow="sm" p="lg" radius="md" withBorder>
                            <Group justify="space-between" mb="xs">
                                <Text fw={500} c="dimmed">HCROI (Human Capital ROI)</Text>
                                <IconCoin size={20} stroke={1.5} />
                            </Group>
                            <Group align="flex-end" gap="xs">
                                <Text fz="xl" fw={700}>{latest.hcroi.toFixed(2)}</Text>
                                <Text fz="sm" c="teal" fw={500}>
                                    Return on every $1 invested
                                </Text>
                            </Group>
                            <Text fz="xs" c="dimmed" mt="md">
                                (Revenue - OpEx) / Total Personnel Costs
                            </Text>
                        </Card>
                    </Grid.Col>

                    <Grid.Col span={6}>
                        <Card shadow="sm" p="lg" radius="md" withBorder>
                            <Group justify="space-between" mb="xs">
                                <Text fw={500} c="dimmed">HCVA (Human Capital Value Added)</Text>
                                <IconUsers size={20} stroke={1.5} />
                            </Group>
                            <Group align="flex-end" gap="xs">
                                <Text fz="xl" fw={700}>${latest.hcva.toLocaleString()}</Text>
                                <Text fz="sm" c="blue" fw={500}>
                                    Value added per FTE
                                </Text>
                            </Group>
                            <Text fz="xs" c="dimmed" mt="md">
                                (Revenue - OpEx) / FTE Count
                            </Text>
                        </Card>
                    </Grid.Col>

                    <Grid.Col span={12}>
                        <Card shadow="sm" p="lg" radius="md" withBorder>
                            <Title order={4} mb="md">Financial Overview ({latest.year})</Title>
                            <Grid>
                                <Grid.Col span={3}>
                                    <Text c="dimmed" size="sm">Revenue</Text>
                                    <Text fw={500}>${latest.revenue.toLocaleString()}</Text>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <Text c="dimmed" size="sm">Operating Expenses</Text>
                                    <Text fw={500}>${latest.operating_expenses.toLocaleString()}</Text>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <Text c="dimmed" size="sm">Personnel Costs</Text>
                                    <Text fw={500}>${latest.personnel_costs.toLocaleString()}</Text>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <Text c="dimmed" size="sm">Net Income</Text>
                                    <Text fw={500} c="green">${latest.net_income.toLocaleString()}</Text>
                                </Grid.Col>
                            </Grid>
                        </Card>
                    </Grid.Col>
                </Grid>
            ) : (
                <Text>No data available.</Text>
            )}
        </Container>
    );
}
