"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Group, Badge, Loader, SimpleGrid, Card, Alert, Progress, RingProgress, Table, Stack } from "@mantine/core";
import { IconAlertTriangle, IconSitemap, IconUser } from "@tabler/icons-react";
import { api } from "@/lib/api";

type OrgNode = {
    id: string;
    name: string;
    role: string;
    span: number;
    depth: number;
    status: string;
};

type SpanData = {
    analyzed_at: string;
    metrics: {
        average_span: number;
        max_layers: number;
        total_managers: number;
    };
    nodes: OrgNode[];
    alerts: Array<{
        name: string;
        issue: string;
        severity: string;
    }>;
};

export default function SpanOfControlPage() {
    const [data, setData] = useState<SpanData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getSpanOfControlAnalysis()
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Container size="xl" py="xl"><Loader /></Container>;
    if (!data) return <Container size="xl" py="xl"><Text>No data available.</Text></Container>;

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>Span of Control Analyzer</Title>
                    <Text c="dimmed">
                        Organizational Efficiency & Hierarchy Depth Analysis
                    </Text>
                </div>
                <Badge size="lg" variant="outline">{data.analyzed_at}</Badge>
            </Group>

            {/* Metrics Cards */}
            <SimpleGrid cols={3} spacing="lg" mb="xl">
                <Card withBorder padding="lg" radius="md">
                    <Stack align="center" gap={0}>
                        <IconUser size={30} color="var(--mantine-color-blue-6)" />
                        <Text size="xs" c="dimmed" mt="xs">Avg. Span of Control</Text>
                        <Text fw={700} size="xl">{data.metrics.average_span}</Text>
                        <Text size="xs" c="green">Target: 7-10</Text>
                    </Stack>
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Stack align="center" gap={0}>
                        <IconSitemap size={30} color="var(--mantine-color-violet-6)" />
                        <Text size="xs" c="dimmed" mt="xs">Max Org Layers</Text>
                        <Text fw={700} size="xl">{data.metrics.max_layers}</Text>
                        <Text size="xs" c="green">Target: 3-5</Text>
                    </Stack>
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Stack align="center" gap={0}>
                        <IconAlertTriangle size={30} color="var(--mantine-color-orange-6)" />
                        <Text size="xs" c="dimmed" mt="xs">Bottleneck Alerts</Text>
                        <Text fw={700} size="xl">{data.alerts.length}</Text>
                        <Text size="xs" c="dimmed">Managers with issues</Text>
                    </Stack>
                </Card>
            </SimpleGrid>

            {/* Alerts Section */}
            {data.alerts.length > 0 && (
                <Card withBorder padding="lg" radius="md" mb="xl" style={{ borderColor: 'orange' }}>
                    <Title order={3} mb="sm">Structural Alerts</Title>
                    <SimpleGrid cols={2}>
                        {data.alerts.map((alert, idx) => (
                            <Alert key={idx} color={alert.severity === "High" ? "red" : "orange"} variant="light" title={alert.name}>
                                {alert.issue}
                            </Alert>
                        ))}
                    </SimpleGrid>
                </Card>
            )}

            {/* Detailed Table */}
            <Card withBorder padding="lg" radius="md">
                <Title order={3} mb="md">Manager Report</Title>
                <Table striped highlightOnHover>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Name</Table.Th>
                            <Table.Th>Role</Table.Th>
                            <Table.Th>Org Depth</Table.Th>
                            <Table.Th>Span (Reports)</Table.Th>
                            <Table.Th>Status</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {data.nodes.map(node => (
                            <Table.Tr key={node.id}>
                                <Table.Td fw={500}>{node.name}</Table.Td>
                                <Table.Td>{node.role}</Table.Td>
                                <Table.Td>{node.depth}</Table.Td>
                                <Table.Td>{node.span}</Table.Td>
                                <Table.Td>
                                    <Badge
                                        color={
                                            node.status.includes("Wide") ? "red" :
                                                node.status.includes("Inefficiency") ? "orange" :
                                                    node.status === "Narrow" ? "yellow" : "green"
                                        }
                                    >
                                        {node.status}
                                    </Badge>
                                </Table.Td>
                            </Table.Tr>
                        ))}
                    </Table.Tbody>
                </Table>
            </Card>
        </Container>
    );
}
