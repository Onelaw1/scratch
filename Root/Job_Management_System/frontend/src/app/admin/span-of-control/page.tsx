"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Group, Badge, Loader, SimpleGrid, Card, Alert, Progress, RingProgress, Table, Stack, ThemeIcon, Paper, Avatar, Button } from "@mantine/core";
import { IconAlertTriangle, IconSitemap, IconUser, IconHierarchy, IconCheck } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { useLanguage } from "@/contexts/LanguageContext";

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
    const { t } = useLanguage();

    useEffect(() => {
        api.getSpanOfControlAnalysis()
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return (
        <Container size="xl" py="xl" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
            <Loader size="lg" />
        </Container>
    );

    const handleSeedData = async () => {
        setLoading(true);
        try {
            await api.seedDemoData();
            // Reload page to fetch new data
            window.location.reload();
        } catch (error) {
            console.error(error);
            setLoading(false);
        }
    };

    if (!data || data.nodes.length === 0) return (
        <Container size="xl" py="xl">
            <Paper p="xl" withBorder radius="lg" style={{ textAlign: 'center', minHeight: 400, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <ThemeIcon size={80} radius="xl" variant="light" color="blue" mb="xl">
                    <IconSitemap size={40} />
                </ThemeIcon>
                <Title order={2} mb="md">{t('span.title')}</Title>
                <Text c="dimmed" mb="xl" maw={500}>
                    조직 데이터가 없습니다. 시연을 위해 가상의 조직 구조(CEO, 이사, 매니저, 팀원)를 생성하시겠습니까?
                </Text>
                <Button size="lg" onClick={handleSeedData} loading={loading}>
                    가상 데이터 생성 (Generate Demo Data)
                </Button>
            </Paper>
        </Container>
    );

    // Helper to translate status
    const getStatusLabel = (status: string) => {
        if (status.includes("Wide")) return t('span.status.wide');
        if (status.includes("Narrow")) return t('span.status.narrow');
        if (status === "Optimal") return t('span.status.optimal');
        return t('span.status.ic');
    };

    return (
        <Container size="xl" py="xl">
            {/* Header */}
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2} style={{ letterSpacing: '-0.5px' }}>{t('span.title')}</Title>
                    <Text c="dimmed">{t('span.subtitle')}</Text>
                </div>
                <Badge size="xl" variant="gradient" gradient={{ from: 'indigo', to: 'violet' }}>
                    {data.analyzed_at}
                </Badge>
            </Group>

            {/* Metrics Cards */}
            <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="lg" mb="xl">
                <Paper shadow="sm" radius="lg" p="xl" withBorder className="bg-white/50 backdrop-blur-sm">
                    <Group align="flex-start" justify="space-between">
                        <Stack gap="xs">
                            <Text size="xs" c="dimmed" tt="uppercase" fw={700}>{t('span.metric.avg_span')}</Text>
                            <Text fw={700} size="3rem" style={{ lineHeight: 1 }} c="blue">{data.metrics.average_span}</Text>
                            <Badge size="sm" variant="light" color="blue">{t('span.target')}: 7-10</Badge>
                        </Stack>
                        <ThemeIcon size={48} radius="md" variant="light" color="blue">
                            <IconUser size={28} />
                        </ThemeIcon>
                    </Group>
                    <Progress value={(data.metrics.average_span / 15) * 100} mt="lg" size="sm" radius="xl" />
                </Paper>

                <Paper shadow="sm" radius="lg" p="xl" withBorder className="bg-white/50 backdrop-blur-sm">
                    <Group align="flex-start" justify="space-between">
                        <Stack gap="xs">
                            <Text size="xs" c="dimmed" tt="uppercase" fw={700}>{t('span.metric.max_layers')}</Text>
                            <Text fw={700} size="3rem" style={{ lineHeight: 1 }} c="violet">{data.metrics.max_layers}</Text>
                            <Badge size="sm" variant="light" color="violet">{t('span.target')}: 3-5</Badge>
                        </Stack>
                        <ThemeIcon size={48} radius="md" variant="light" color="violet">
                            <IconHierarchy size={28} />
                        </ThemeIcon>
                    </Group>
                    <Progress value={(data.metrics.max_layers / 8) * 100} mt="lg" size="sm" radius="xl" color="violet" />
                </Paper>

                <Paper shadow="sm" radius="lg" p="xl" withBorder className="bg-white/50 backdrop-blur-sm">
                    <Group align="flex-start" justify="space-between">
                        <Stack gap="xs">
                            <Text size="xs" c="dimmed" tt="uppercase" fw={700}>{t('span.metric.bottlenecks')}</Text>
                            <Text fw={700} size="3rem" style={{ lineHeight: 1 }} c={data.alerts.length > 0 ? "orange" : "green"}>
                                {data.alerts.length}
                            </Text>
                            <Text size="xs" c="dimmed">{t('span.unit.managers')}</Text>
                        </Stack>
                        <ThemeIcon size={48} radius="md" variant="light" color={data.alerts.length > 0 ? "orange" : "green"}>
                            {data.alerts.length > 0 ? <IconAlertTriangle size={28} /> : <IconCheck size={28} />}
                        </ThemeIcon>
                    </Group>
                    <Progress value={(data.alerts.length / 5) * 100} mt="lg" size="sm" radius="xl" color="orange" />
                </Paper>
            </SimpleGrid>

            {/* Alerts Section */}
            {data.alerts.length > 0 && (
                <Paper withBorder p="lg" radius="lg" mb="xl" style={{ borderColor: 'var(--mantine-color-orange-3)', background: 'var(--mantine-color-orange-0)' }}>
                    <Group mb="md">
                        <IconAlertTriangle color="orange" />
                        <Title order={4}>{t('span.alerts_title')}</Title>
                    </Group>
                    <SimpleGrid cols={{ base: 1, sm: 2 }}>
                        {data.alerts.map((alert, idx) => (
                            <Alert key={idx} color={alert.severity === "High" ? "red" : "orange"} variant="light" title={alert.name} radius="md">
                                {alert.issue}
                            </Alert>
                        ))}
                    </SimpleGrid>
                </Paper>
            )}

            {/* Detailed Table */}
            <Paper shadow="sm" radius="lg" p="md" withBorder className="bg-white">
                <Group mb="md" px="xs">
                    <IconSitemap size={20} color="gray" />
                    <Title order={4}>{t('span.table.title')}</Title>
                </Group>
                <Table horizontalSpacing="md" verticalSpacing="sm" highlightOnHover>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>{t('span.table.name')}</Table.Th>
                            <Table.Th>{t('span.table.role')}</Table.Th>
                            <Table.Th>{t('span.table.depth')}</Table.Th>
                            <Table.Th>{t('span.table.span')}</Table.Th>
                            <Table.Th>{t('span.table.status')}</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {data.nodes.map(node => (
                            <Table.Tr key={node.id}>
                                <Table.Td>
                                    <Group gap="sm">
                                        <Avatar size="sm" radius="xl" color="blue" name={node.name}>{node.name.charAt(0)}</Avatar>
                                        <Text size="sm" fw={500}>{node.name}</Text>
                                    </Group>
                                </Table.Td>
                                <Table.Td><Badge variant="dot" color="gray">{node.role}</Badge></Table.Td>
                                <Table.Td><Text size="sm">{node.depth}</Text></Table.Td>
                                <Table.Td><Text fw={700}>{node.span}</Text></Table.Td>
                                <Table.Td>
                                    <Badge
                                        variant="light"
                                        color={
                                            node.status.includes("Wide") ? "red" :
                                                node.status.includes("Narrow") ? "orange" :
                                                    node.status === "Optimal" ? "green" : "gray"
                                        }
                                    >
                                        {getStatusLabel(node.status)}
                                    </Badge>
                                </Table.Td>
                            </Table.Tr>
                        ))}
                    </Table.Tbody>
                </Table>
            </Paper>
        </Container>
    );
}
