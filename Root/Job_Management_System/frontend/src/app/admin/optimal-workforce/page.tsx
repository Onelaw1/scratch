"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Paper, Table, Group, Badge, Button, Loader, Tooltip, SimpleGrid, Card, Progress, RingProgress, Center, ThemeIcon, Alert } from "@mantine/core";
import { IconCalculator, IconUsers, IconAlertTriangle, IconCheck, IconArrowRight, IconChartBar } from "@tabler/icons-react";
import { api } from "@/lib/api";

type DeptAnalysis = {
    department: string;
    current_fte: number;
    required_fte: number;
    gap: number;
    productivity_index: number;
    monthly_volume: number;
    avg_process_time: number;
    status: string;
};

type OptimizationData = {
    generated_at: string;
    formula: string;
    total_hiring_need: number;
    department_analysis: DeptAnalysis[];
};

export default function OptimalWorkforcePage() {
    const [data, setData] = useState<OptimizationData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getWorkforceOptimization()
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Container size="xl" py="xl"><Loader /></Container>;
    if (!data) return <Container size="xl" py="xl"><Text>No data available.</Text></Container>;

    const overworkedDepts = data.department_analysis.filter(d => d.gap > 0);
    const idleDepts = data.department_analysis.filter(d => d.gap < 0);

    return (
        <Container size="xl" py="xl">
            {/* Header */}
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>Optimal Workforce Calculator</Title>
                    <Text c="dimmed">
                        Scientific Headcount Planning based on Standard Time & Volume
                    </Text>
                </div>
                <Badge size="lg" variant="dot" color="blue">Algorithm Active</Badge>
            </Group>

            {/* Formula Alert */}
            <Alert icon={<IconCalculator size={16} />} title="Calculation Logic" color="blue" mb="xl">
                Required FTE = (Monthly Volume × Standard Time) / (160 Hours × 0.85 Utilization)
            </Alert>

            {/* Summary KPI */}
            <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="lg" mb="xl">
                <Card withBorder padding="lg" radius="md">
                    <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Total Hiring Need</Text>
                    <Text fz="xl" fw={700} c="red">+{data.total_hiring_need} FTE</Text>
                    <Progress value={(data.total_hiring_need / 10) * 100} mt="md" color="red" />
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Overworked Depts</Text>
                    <Text fz="xl" fw={700} c="orange">{overworkedDepts.length} Teams</Text>
                    <Progress value={(overworkedDepts.length / data.department_analysis.length) * 100} mt="md" color="orange" />
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Standard Utilization</Text>
                    <Text fz="xl" fw={700} c="blue">85%</Text>
                    <Progress value={85} mt="md" color="blue" />
                </Card>
            </SimpleGrid>

            {/* Main Analysis Table */}
            <Paper withBorder shadow="sm" radius="md" p="md">
                <Group mb="md">
                    <IconChartBar size={20} />
                    <Text fw={600}>Department Workload Analysis</Text>
                </Group>

                <Table striped highlightOnHover>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Department</Table.Th>
                            <Table.Th>Workload (Vol × Time)</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Current FTE</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Required FTE</Table.Th>
                            <Table.Th style={{ textAlign: 'center' }}>Gap</Table.Th>
                            <Table.Th style={{ textAlign: 'center' }}>Load Index</Table.Th>
                            <Table.Th>Actions</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {data.department_analysis.map((dept) => (
                            <Table.Tr key={dept.department}>
                                <Table.Td fw={500}>{dept.department}</Table.Td>
                                <Table.Td>
                                    <Text size="sm">{dept.monthly_volume.toLocaleString()} units</Text>
                                    <Text size="xs" c="dimmed">@ {dept.avg_process_time} min/unit</Text>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'right' }}>{dept.current_fte}</Table.Td>
                                <Table.Td style={{ textAlign: 'right' }} fw={700} c="blue">
                                    {dept.required_fte}
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'center' }}>
                                    <Badge
                                        color={dept.gap > 0 ? "red" : dept.gap < -1 ? "gray" : "green"}
                                        variant="filled"
                                    >
                                        {dept.gap > 0 ? `+${dept.gap}` : dept.gap}
                                    </Badge>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'center' }}>
                                    <Group justify="center" gap={4}>
                                        <RingProgress
                                            size={40}
                                            thickness={4}
                                            roundCaps
                                            sections={[{ value: Math.min(dept.productivity_index, 100), color: dept.productivity_index > 100 ? 'red' : 'blue' }]}
                                        />
                                        <Text size="xs" fw={700}>{dept.productivity_index}%</Text>
                                    </Group>
                                </Table.Td>
                                <Table.Td>
                                    {dept.gap > 1.0 ? (
                                        <Button size="xs" color="red" variant="light" leftSection={<IconUsers size={12} />}>
                                            Hire
                                        </Button>
                                    ) : dept.gap < -2.0 ? (
                                        <Button size="xs" color="gray" variant="light" leftSection={<IconArrowRight size={12} />}>
                                            Redeploy
                                        </Button>
                                    ) : (
                                        <Text size="xs" c="green">Stable</Text>
                                    )}
                                </Table.Td>
                            </Table.Tr>
                        ))}
                    </Table.Tbody>
                </Table>
            </Paper>
        </Container>
    );
}
