"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Group, Badge, Loader, SimpleGrid, Card, Alert, Table, ThemeIcon, Tooltip, HoverCard } from "@mantine/core";
import { IconAlertTriangle, IconRefresh, IconExclamationCircle, IconCheck, IconBuildingCommunity, IconBriefcase } from "@tabler/icons-react";
import { api } from "@/lib/api";

type RAndRData = {
    analyzed_at: string;
    departments: string[];
    categories: string[];
    matrix: Record<string, Record<string, number>>;
    alerts: {
        duplications: Array<{
            category: string;
            involved_depts: string[];
            reason: string;
            severity: string;
        }>;
        gaps: Array<{
            category: string;
            reason: string;
            severity: string;
        }>;
    };
};

export default function RAndRPage() {
    const [data, setData] = useState<RAndRData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getRAndRAnalysis()
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
                    <Title order={1}>R&R Conflict Map</Title>
                    <Text c="dimmed">
                        Visualizing Role & Responsibility overlaps and gaps across organization.
                    </Text>
                </div>
                <Badge size="lg" variant="light" color="gray">
                    {data.analyzed_at}
                </Badge>
            </Group>

            {/* Alerts Section */}
            <SimpleGrid cols={2} spacing="lg" mb="xl">
                <Card withBorder padding="md" radius="md" style={{ borderColor: data.alerts.duplications.length > 0 ? 'red' : undefined }}>
                    <Group mb="sm">
                        <ThemeIcon color="red" variant="light" size="lg"><IconAlertTriangle /></ThemeIcon>
                        <Text fw={700}>Duplication Alerts (Efficiency Loss)</Text>
                    </Group>
                    {data.alerts.duplications.length === 0 ? (
                        <Text c="dimmed" size="sm">No conflicts detected.</Text>
                    ) : (
                        data.alerts.duplications.map((alert, idx) => (
                            <Alert key={idx} color="red" variant="light" mb="xs" title={alert.category} icon={<IconExclamationCircle size={16} />}>
                                <Text size="xs">{alert.reason}</Text>
                                <Group gap={5} mt={5}>
                                    {alert.involved_depts.map(d => <Badge key={d} size="xs" color="red" variant="outline">{d}</Badge>)}
                                </Group>
                            </Alert>
                        ))
                    )}
                </Card>

                <Card withBorder padding="md" radius="md" style={{ borderColor: data.alerts.gaps.length > 0 ? 'orange' : undefined }}>
                    <Group mb="sm">
                        <ThemeIcon color="orange" variant="light" size="lg"><IconExclamationCircle /></ThemeIcon>
                        <Text fw={700}>Gap Alerts (Risk)</Text>
                    </Group>
                    {data.alerts.gaps.length === 0 ? (
                        <Text c="dimmed" size="sm">No gaps detected.</Text>
                    ) : (
                        data.alerts.gaps.map((alert, idx) => (
                            <Alert key={idx} color="orange" variant="light" mb="xs" title={alert.category}>
                                <Text size="xs">{alert.reason}</Text>
                            </Alert>
                        ))
                    )}
                </Card>
            </SimpleGrid>

            {/* Matrix View */}
            <Card withBorder padding="lg" radius="md">
                <Title order={3} mb="md">Organization Workload Matrix</Title>
                <Table striped highlightOnHover withTableBorder>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Task Category / Dept</Table.Th>
                            {data.departments.map(dept => (
                                <Table.Th key={dept} style={{ textAlign: 'center' }}>{dept}</Table.Th>
                            ))}
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {data.categories.map(category => {
                            const isDuplicated = data.alerts.duplications.some(d => d.category === category);
                            const isGap = data.alerts.gaps.some(g => g.category === category);

                            return (
                                <Table.Tr key={category} bg={isDuplicated ? 'var(--mantine-color-red-0)' : isGap ? 'var(--mantine-color-orange-0)' : undefined}>
                                    <Table.Td fw={600}>
                                        <Group gap="xs">
                                            {category}
                                            {isDuplicated && <Badge color="red" size="xs">Conflict</Badge>}
                                            {isGap && <Badge color="orange" size="xs">Gap</Badge>}
                                        </Group>
                                    </Table.Td>
                                    {data.departments.map(dept => {
                                        const value = data.matrix[category]?.[dept] || 0;
                                        return (
                                            <Table.Td key={`${category}-${dept}`} style={{ textAlign: 'center' }}>
                                                {value > 0 ? (
                                                    <Badge
                                                        variant={value > 50 ? "filled" : "light"}
                                                        color={value > 50 ? "blue" : "gray"}
                                                    >
                                                        {value}%
                                                    </Badge>
                                                ) : (
                                                    <Text c="dimmed" size="xs">-</Text>
                                                )}
                                            </Table.Td>
                                        );
                                    })}
                                </Table.Tr>
                            );
                        })}
                    </Table.Tbody>
                </Table>
            </Card>
        </Container>
    );
}
