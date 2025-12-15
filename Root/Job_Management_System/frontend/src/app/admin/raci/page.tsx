"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Group, Badge, Loader, Card, Table, Select, Button, ThemeIcon, Alert } from "@mantine/core";
import { IconCheck, IconRefresh, IconUser, IconSitemap, IconInfoCircle } from "@tabler/icons-react";
import { api } from "@/lib/api";

type RACIMatrix = {
    process_id: string;
    process_name: string;
    generated_at: string;
    stakeholders: string[];
    matrix: Array<{
        step: string;
        roles: Record<string, string>; // "R", "A", "C", "I", ""
    }>;
};

export default function RACIPage() {
    const [processId, setProcessId] = useState<string>("hiring");
    const [data, setData] = useState<RACIMatrix | null>(null);
    const [loading, setLoading] = useState(false);

    const fetchRACI = (pid: string) => {
        setLoading(true);
        api.getRACIChart(pid)
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        fetchRACI(processId);
    }, [processId]);

    const getRoleBadge = (role: string) => {
        switch (role) {
            case "R": return <Badge color="blue" variant="filled">R</Badge>; // Responsible
            case "A": return <Badge color="red" variant="filled">A</Badge>; // Accountable
            case "C": return <Badge color="orange" variant="light">C</Badge>; // Consulted
            case "I": return <Badge color="gray" variant="light">I</Badge>; // Informed
            default: return null;
        }
    };

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>RACI Chart Generator</Title>
                    <Text c="dimmed">
                        Auto-generating Role & Responsibility Matrix based on workload and hierarchy.
                    </Text>
                </div>
                <Group>
                    <Select
                        data={[
                            { value: 'hiring', label: 'Recruiting Process' },
                            { value: 'budget', label: 'Budget Planning' }
                        ]}
                        value={processId}
                        onChange={(v) => v && setProcessId(v)}
                        allowDeselect={false}
                    />
                    <Button leftSection={<IconRefresh size={16} />} onClick={() => fetchRACI(processId)} variant="light">
                        Regenerate
                    </Button>
                </Group>
            </Group>

            {loading ? (
                <Container py="xl"><Loader /></Container>
            ) : data ? (
                <>
                    <Alert icon={<IconInfoCircle size={16} />} title="RACI Definitions" color="blue" mb="xl">
                        <Group gap="xl">
                            <Group gap={5}><Badge color="blue" variant="filled">R</Badge> <Text size="sm">Responsible (Doer)</Text></Group>
                            <Group gap={5}><Badge color="red" variant="filled">A</Badge> <Text size="sm">Accountable (Approver)</Text></Group>
                            <Group gap={5}><Badge color="orange" variant="light">C</Badge> <Text size="sm">Consulted (Advisor)</Text></Group>
                            <Group gap={5}><Badge color="gray" variant="light">I</Badge> <Text size="sm">Informed (Notify)</Text></Group>
                        </Group>
                    </Alert>

                    <Card withBorder padding="lg" radius="md">
                        <Title order={3} mb="md">{data.process_name} Matrix</Title>
                        <Table striped highlightOnHover withTableBorder verticalSpacing="md">
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Process Step</Table.Th>
                                    {data.stakeholders.map(s => (
                                        <Table.Th key={s} style={{ textAlign: 'center' }}>{s}</Table.Th>
                                    ))}
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {data.matrix.map((row, idx) => (
                                    <Table.Tr key={idx}>
                                        <Table.Td fw={600}>{row.step}</Table.Td>
                                        {data.stakeholders.map(s => (
                                            <Table.Td key={`${idx}-${s}`} style={{ textAlign: 'center' }}>
                                                {getRoleBadge(row.roles[s] || "")}
                                            </Table.Td>
                                        ))}
                                    </Table.Tr>
                                ))}
                            </Table.Tbody>
                        </Table>
                    </Card>
                </>
            ) : (
                <Text>No data loaded.</Text>
            )}
        </Container>
    );
}
