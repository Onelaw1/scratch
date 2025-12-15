"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Button, Paper, Group, SimpleGrid, ThemeIcon, Badge, Stack } from "@mantine/core";
import { IconPlus, IconBriefcase, IconTrendingUp, IconCoin } from "@tabler/icons-react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Notifications } from "@mantine/notifications";
import {
    ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { useLanguage } from "@/contexts/LanguageContext";

export default function SimulationDashboard() {
    const router = useRouter();
    const [scenarios, setScenarios] = useState<any[]>([]);
    const [metrics, setMetrics] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const { t } = useLanguage();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [scenariosRes, institutionsRes] = await Promise.all([
                api.getScenarios(),
                api.getInstitutions()
            ]);
            setScenarios(scenariosRes);

            // Fetch metrics for the first institution for demo purposes
            if (institutionsRes.length > 0) {
                const metricsRes = await api.getProductivityMetrics(institutionsRes[0].id);
                setMetrics(metricsRes);
            }
        } catch (error) {
            console.error(error);
            Notifications.show({ title: 'Error', message: 'Failed to load dashboard data', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleCreateScenario = async () => {
        const name = prompt("Enter scenario name:");
        if (!name) return;
        try {
            await api.createScenario({ name, description: "New simulation" });
            loadData();
        } catch (error) {
            console.error(error);
            Notifications.show({ title: 'Error', message: 'Failed to create scenario', color: 'red' });
        }
    };

    // Helper to get latest metrics
    const latest = metrics.length > 0 ? metrics[metrics.length - 1] : null;

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2} style={{ letterSpacing: '-0.5px' }}>{t('prod.title')}</Title>
                    <Text c="dimmed">{t('prod.subtitle')}</Text>
                </div>
                <Button leftSection={<IconPlus size={16} />} onClick={handleCreateScenario} variant="gradient" gradient={{ from: 'blue', to: 'cyan' }}>
                    {t('prod.new_scenario')}
                </Button>
            </Group>

            <Paper
                p="xl"
                radius="lg"
                mb="xl"
                style={{
                    background: 'rgba(255, 255, 255, 0.9)', // More opaque for readability
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255,255,255,0.7)',
                    boxShadow: '0 8px 30px rgba(0,0,0,0.05)'
                }}
            >
                <Group mb="lg" align="center">
                    <ThemeIcon size={40} radius="md" color="green" variant="light">
                        <IconTrendingUp size={24} />
                    </ThemeIcon>
                    <div>
                        <Text size="lg" fw={700}>{t('prod.overview_title')}</Text>
                        <Text size="sm" c="dimmed">{t('prod.overview_desc')}</Text>
                    </div>
                </Group>

                <SimpleGrid cols={{ base: 1, md: 3 }} spacing="xl">
                    {/* KPI 1: HCROI */}
                    <Paper p="md" radius="md" bg="gray.0">
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" fw={700} c="dimmed" tt="uppercase">{t('prod.hcroi_label')}</Text>
                            <IconTrendingUp size={16} className="text-green-600" />
                        </Group>
                        <Group align="flex-end" gap="xs">
                            <Text size="2rem" fw={800} lh={1}>{latest ? latest.hcroi.toFixed(2) : '0.00'}</Text>
                            {latest && latest.hcroi < 2.5 && <Badge color="red" variant="light">Loss Warning</Badge>}
                        </Group>
                        <Text size="xs" c="dimmed" mt="sm">{t('prod.hcroi_desc')}</Text>
                    </Paper>

                    {/* KPI 2: HCVA */}
                    <Paper p="md" radius="md" bg="gray.0">
                        <Group justify="space-between" mb="xs">
                            <Text size="xs" fw={700} c="dimmed" tt="uppercase">{t('prod.hcva_label')}</Text>
                            <ThemeIcon size={16} radius="xl" color="blue" variant="transparent"><IconCoin size={14} /></ThemeIcon>
                        </Group>
                        <Group align="flex-end" gap="xs">
                            <Text size="2rem" fw={800} lh={1}>${latest ? (latest.hcva / 1000).toFixed(1) : '0.0'}k</Text>
                            <Text size="sm" fw={600} c="dimmed" mb={4}>per FTE</Text>
                        </Group>
                        <Text size="xs" c="dimmed" mt="sm">{t('prod.hcva_desc')}</Text>
                    </Paper>

                    {/* Chart Area */}
                    <Paper p="xs" radius="md" bg="transparent" style={{ gridColumn: 'span 1' }}>
                        {/* Placeholder used to align grid, content is below */}
                    </Paper>
                </SimpleGrid>

                {/* Main Trends Chart */}
                <Paper mt="xl" p="md" radius="md" withBorder>
                    <Text fw={600} mb="md">{t('prod.trends')}</Text>
                    <div style={{ width: '100%', height: 300 }}>
                        <ResponsiveContainer>
                            <ComposedChart data={metrics}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="year" />
                                <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
                                <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
                                <Tooltip
                                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                                />
                                <Legend />
                                <Bar yAxisId="left" dataKey="personnel_costs" name="Personnel Costs" fill="#e0e0e0" radius={[4, 4, 0, 0]} />
                                <Line yAxisId="left" type="monotone" dataKey="revenue" name="Revenue" stroke="#8884d8" strokeWidth={2} dot={{ r: 4 }} />
                                <Line yAxisId="right" type="monotone" dataKey="hcroi" name="HCROI" stroke="#00c49f" strokeWidth={2} dot={{ r: 4 }} />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                </Paper>
            </Paper>

            <Title order={3} mb="md">{t('prod.scenarios')}</Title>
            {scenarios.length === 0 ? (
                <Paper p="xl" withBorder radius="md" bg="gray.0">
                    <Text c="dimmed" ta="center">{t('prod.no_scenarios')}</Text>
                </Paper>
            ) : (
                <Stack>
                    {scenarios.map((s) => (
                        <Paper key={s.id} p="md" radius="md" withBorder className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => router.push(`/simulation/${s.id}`)}>
                            <Group justify="space-between">
                                <Group>
                                    <ThemeIcon size="lg" radius="md" variant="light" color="blue">
                                        <IconBriefcase size={20} />
                                    </ThemeIcon>
                                    <div>
                                        <Text fw={600}>{s.name}</Text>
                                        <Text size="sm" c="dimmed">Last updated: {new Date().toLocaleDateString()}</Text>
                                    </div>
                                </Group>
                                <Badge variant="light">Draft</Badge>
                            </Group>
                        </Paper>
                    ))}
                </Stack>
            )}
        </Container>
    );
}
