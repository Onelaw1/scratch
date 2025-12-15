"use client";

import { useEffect, useState } from "react";
import { Container, Grid, Paper, Title, Text, Loader, Button, Group, Modal, NumberInput, Stack, Divider } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { IconPlus } from "@tabler/icons-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, ReferenceLine } from "recharts";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { Drawer } from "@mantine/core";

export default function WorkloadAnalysisPage() {
    const router = useRouter();
    const [fteByOrg, setFteByOrg] = useState<{ name: string, fte: number }[]>([]);
    const [fteByPos, setFteByPos] = useState<{ name: string, fte: number }[]>([]);
    const [metrics, setMetrics] = useState<{ year: number, hcroi: number, hcva: number, revenue: number }[]>([]);
    const [institutions, setInstitutions] = useState<any[]>([]);
    const [selectedInstitutionId, setSelectedInstitutionId] = useState<string>("");

    const [loading, setLoading] = useState(true);
    const [opened, { open, close }] = useDisclosure(false);

    // Form for Financial Data
    const form = useForm({
        initialValues: {
            year: new Date().getFullYear(),
            revenue: 0,
            operating_expenses: 0,
            personnel_costs: 0,
        },
    });

    useEffect(() => {
        const load = async () => {
            try {
                const [orgData, posData, instData] = await Promise.all([
                    api.getFteByOrg(),
                    api.getFteByPosition(),
                    api.getInstitutions()
                ]);
                setFteByOrg(orgData);
                setFteByPos(posData);
                setInstitutions(instData);
                if (instData.length > 0) {
                    setSelectedInstitutionId(instData[0].id);
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    useEffect(() => {
        if (!selectedInstitutionId) return;
        api.getProductivityMetrics(selectedInstitutionId).then(setMetrics).catch(console.error);
    }, [selectedInstitutionId]);

    const handleSubmit = async (values: typeof form.values) => {
        if (!selectedInstitutionId) return;
        try {
            await api.saveFinancialPerformance({
                ...values,
                institution_id: selectedInstitutionId
            });
            // Refresh metrics
            const res = await api.getProductivityMetrics(selectedInstitutionId);
            setMetrics(res);
            close();
            notifications.show({ title: 'Success', message: 'Financial data saved', color: 'green' });
        } catch (error) {
            notifications.show({ title: 'Error', message: 'Failed to save data', color: 'red' });
        }
    };

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <Title order={2}>Workload & Productivity Analysis</Title>
                <Button onClick={open} leftSection={<IconPlus size={16} />}>Input Financial Data</Button>
            </Group>

            {/* Financial Input Drawer (UX Improvement: Context is kept) */}
            <Drawer opened={opened} onClose={close} title={<Title order={4}>Financial Performance Input</Title>} position="right" padding="xl">
                <Text size="sm" c="dimmed" mb="lg">
                    Enter financial data to calculate HCROI and HCVA metrics.
                    Changes are reflected immediately after saving.
                </Text>
                <form onSubmit={form.onSubmit(handleSubmit)}>
                    <NumberInput label="Year" {...form.getInputProps('year')} mb="sm" />
                    <NumberInput label="Revenue (Total)" description="Total annual revenue" {...form.getInputProps('revenue')} mb="sm" />
                    <NumberInput label="Operating Expenses" description="Excluding personnel costs" {...form.getInputProps('operating_expenses')} mb="sm" />
                    <NumberInput label="Personnel Costs" description="Total labor costs" {...form.getInputProps('personnel_costs')} mb="sm" />

                    <Divider my="md" />

                    <Group grow>
                        <Button variant="light" color="gray" onClick={close}>Cancel</Button>
                        <Button type="submit">Save Data</Button>
                    </Group>
                </form>
            </Drawer>

            {loading ? <Loader /> : (
                <Stack gap="lg">
                    {/* Key Indicators Upgrade */}
                    <Grid>
                        <Grid.Col span={{ base: 12, sm: 6, lg: 3 }}>
                            <Paper withBorder p="md" radius="md" style={{ borderLeft: '4px solid #4dabf7' }}>
                                <Text size="xs" c="dimmed" tt="uppercase" fw={700}>Total FTE</Text>
                                <Title order={2}>{fteByOrg.reduce((acc, curr) => acc + curr.fte, 0).toFixed(1)}</Title>
                                <Text size="xs" c="green" fw={500} mt="xs">Across {fteByOrg.length} Units</Text>
                            </Paper>
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, sm: 6, lg: 3 }}>
                            <Paper withBorder p="md" radius="md" style={{ borderLeft: '4px solid #82ca9d' }}>
                                <Text size="xs" c="dimmed" tt="uppercase" fw={700}>Latest HCROI</Text>
                                <Title order={2}>{metrics.length > 0 ? metrics[metrics.length - 1].hcroi.toFixed(2) : '-'}</Title>
                                <Text size="xs" c="dimmed" mt="xs">Return on $1 Invested</Text>
                            </Paper>
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, sm: 6, lg: 3 }}>
                            <Paper withBorder p="md" radius="md" style={{ borderLeft: '4px solid #ff7043' }}>
                                <Text size="xs" c="dimmed" tt="uppercase" fw={700}>Latest HCVA</Text>
                                <Title order={2}>{metrics.length > 0 ? `${(metrics[metrics.length - 1].hcva / 1000000).toFixed(1)}M` : '-'}</Title>
                                <Text size="xs" c="dimmed" mt="xs">Value Added per FTE</Text>
                            </Paper>
                        </Grid.Col>
                        <Grid.Col span={{ base: 12, sm: 6, lg: 3 }}>
                            <Paper withBorder p="md" radius="md" style={{ borderLeft: '4px solid #ffd43b' }}>
                                <Text size="xs" c="dimmed" tt="uppercase" fw={700}>Revenue</Text>
                                <Title order={2}>{metrics.length > 0 ? `${(metrics[metrics.length - 1].revenue / 100000000).toFixed(1)}억` : '-'}</Title>
                                <Text size="xs" c="dimmed" mt="xs">Total Annual</Text>
                            </Paper>
                        </Grid.Col>
                    </Grid>

                    <Grid>
                        <Grid.Col span={{ base: 12, md: 6 }}>
                            <Paper p="md" withBorder radius="md" shadow="sm">
                                <Title order={4} mb="md" c="dimmed">FTE by Team (Org Unit)</Title>
                                <div style={{ height: 300 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={fteByOrg}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="name" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Bar dataKey="fte" fill="#4dabf7" name="Total FTE" radius={[4, 4, 0, 0]} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </Paper>
                        </Grid.Col>

                        <Grid.Col span={{ base: 12, md: 6 }}>
                            <Paper p="md" withBorder radius="md" shadow="sm">
                                <Title order={4} mb="md" c="dimmed">FTE by Job Position</Title>
                                <div style={{ height: 300 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <PieChart>
                                            <Pie
                                                data={fteByPos}
                                                cx="50%"
                                                cy="50%"
                                                labelLine={true}
                                                outerRadius={100}
                                                fill="#8884d8"
                                                dataKey="fte"
                                                nameKey="name"
                                                label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                                                onClick={(e) => {
                                                    // Contextual Navigation
                                                    router.push('/job-classification');
                                                }}
                                                className="cursor-pointer"
                                            >
                                                {fteByPos.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                ))}
                                            </Pie>
                                            <Tooltip />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </div>
                            </Paper>
                        </Grid.Col>
                    </Grid>

                    <Divider my="md" label="Productivity Metrics (HCROI / HCVA)" labelPosition="center" />

                    <Grid>
                        <Grid.Col span={{ base: 12, md: 6 }}>
                            <Paper p="md" withBorder radius="md" shadow="sm">
                                <Title order={4} mb="md" c="dimmed">HCROI (Human Capital ROI)</Title>
                                <Text size="sm" c="dimmed" mb="sm">Revenue - OpEx / Personnel Costs</Text>
                                <div style={{ height: 300 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={metrics}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="year" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Line type="monotone" dataKey="hcroi" stroke="#8884d8" name="HCROI" strokeWidth={2} />
                                            {/* Benchmark Visualization */}
                                            <ReferenceLine y={1.5} label="Industry Avg (1.5)" stroke="red" strokeDasharray="3 3" />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </Paper>
                        </Grid.Col>

                        <Grid.Col span={{ base: 12, md: 6 }}>
                            <Paper p="md" withBorder radius="md" shadow="sm">
                                <Title order={4} mb="md" c="dimmed">HCVA (Human Capital Value Added)</Title>
                                <Text size="sm" c="dimmed" mb="sm">Value Added / FTE</Text>
                                <div style={{ height: 300 }}>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={metrics}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="year" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Bar dataKey="hcva" fill="#82ca9d" name="HCVA (per FTE)" radius={[4, 4, 0, 0]} />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </Paper>
                        </Grid.Col>
                    </Grid>
                </Stack>
            )}
        </Container>
    );
}
