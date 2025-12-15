"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, RingProgress,
    Table, Badge, ActionIcon, NumberInput, Button, Modal, Stack
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { IconEdit, IconUsers, IconChartBar } from "@tabler/icons-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from "recharts";
import { api } from "@/lib/api";

export default function WorkforcePlanningPage() {
    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedUnit, setSelectedUnit] = useState<any>(null);
    const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false);
    const [newAuthorized, setNewAuthorized] = useState<number | ''>('');
    const [saving, setSaving] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const res = await api.getGapAnalysis();
            setData(res);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load gap analysis', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleEditClick = (unit: any) => {
        setSelectedUnit(unit);
        setNewAuthorized(unit.authorized_count);
        openEdit();
    };

    const handleSave = async () => {
        if (!selectedUnit || newAuthorized === '') return;

        setSaving(true);
        try {
            await api.saveHeadcountPlan({
                institution_id: "default-institution-id", // MVP Hack: Should come from context
                org_unit_id: selectedUnit.id,
                year: 2025,
                authorized_count: Number(newAuthorized)
            });
            notifications.show({ title: 'Success', message: 'Authorized headcount updated', color: 'green' });
            closeEdit();
            loadData(); // Refresh
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to save', color: 'red' });
        } finally {
            setSaving(false);
        }
    };

    const totalGap = data.reduce((acc, curr) => acc + curr.gap, 0);
    const understaffedCount = data.filter(d => d.gap < 0).length;
    const overstaffedCount = data.filter(d => d.gap > 0).length;

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2}>Workforce Planning & Gap Analysis</Title>
                    <Text c="dimmed">Analyze the gap between Authorized (TO) and Required (FTE) headcount.</Text>
                </div>
            </Group>

            {/* Summary Cards */}
            <Grid mb="xl">
                <Grid.Col span={{ base: 12, sm: 4 }}>
                    <Paper p="md" radius="md" withBorder>
                        <Group>
                            <RingProgress
                                size={80}
                                roundCaps
                                thickness={8}
                                sections={[{ value: 100, color: totalGap < 0 ? 'red' : 'blue' }]}
                                label={<IconUsers size={20} style={{ display: 'block', margin: 'auto' }} />}
                            />
                            <div>
                                <Text c="dimmed" size="xs" tt="uppercase" fw={700}>Total Gap</Text>
                                <Title order={2} c={totalGap < 0 ? 'red' : 'blue'}>
                                    {totalGap > 0 ? '+' : ''}{totalGap.toFixed(1)}
                                </Title>
                            </div>
                        </Group>
                    </Paper>
                </Grid.Col>
                <Grid.Col span={{ base: 12, sm: 4 }}>
                    <Paper p="md" radius="md" withBorder>
                        <Group>
                            <RingProgress
                                size={80}
                                roundCaps
                                thickness={8}
                                sections={[{ value: (understaffedCount / data.length) * 100, color: 'red' }]}
                                label={<Text ta="center" size="sm" fw={700}>{understaffedCount}</Text>}
                            />
                            <div>
                                <Text c="dimmed" size="xs" tt="uppercase" fw={700}>Understaffed Units</Text>
                                <Text size="sm" c="dimmed">Requiring reinforcement</Text>
                            </div>
                        </Group>
                    </Paper>
                </Grid.Col>
                <Grid.Col span={{ base: 12, sm: 4 }}>
                    <Paper p="md" radius="md" withBorder>
                        <Group>
                            <RingProgress
                                size={80}
                                roundCaps
                                thickness={8}
                                sections={[{ value: (overstaffedCount / data.length) * 100, color: 'blue' }]}
                                label={<Text ta="center" size="sm" fw={700}>{overstaffedCount}</Text>}
                            />
                            <div>
                                <Text c="dimmed" size="xs" tt="uppercase" fw={700}>Overstaffed Units</Text>
                                <Text size="sm" c="dimmed">Potential redeployment</Text>
                            </div>
                        </Group>
                    </Paper>
                </Grid.Col>
            </Grid>

            <Grid>
                {/* Chart */}
                <Grid.Col span={{ base: 12, lg: 8 }}>
                    <Paper p="md" radius="md" withBorder mb="md">
                        <Title order={4} mb="md">Gap Analysis by Unit</Title>
                        <ResponsiveContainer width="100%" height={350}>
                            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="unit_name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <ReferenceLine y={0} stroke="#000" />
                                <Bar dataKey="authorized_count" name="Authorized (TO)" fill="#8884d8" />
                                <Bar dataKey="required_count" name="Required (FTE)" fill="#82ca9d" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid.Col>

                {/* Detailed Table */}
                <Grid.Col span={{ base: 12, lg: 4 }}>
                    <Paper p="md" radius="md" withBorder h="100%">
                        <Title order={4} mb="md">Detailed Status</Title>
                        <Table striped highlightOnHover>
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Unit</Table.Th>
                                    <Table.Th>Auth</Table.Th>
                                    <Table.Th>Req</Table.Th>
                                    <Table.Th>Gap</Table.Th>
                                    <Table.Th></Table.Th>
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {data.map((row) => (
                                    <Table.Tr key={row.id}>
                                        <Table.Td>{row.unit_name}</Table.Td>
                                        <Table.Td>{row.authorized_count}</Table.Td>
                                        <Table.Td>{row.required_count}</Table.Td>
                                        <Table.Td>
                                            <Badge color={row.gap < 0 ? 'red' : 'blue'} variant="light">
                                                {row.gap > 0 ? '+' : ''}{row.gap}
                                            </Badge>
                                        </Table.Td>
                                        <Table.Td>
                                            <ActionIcon variant="subtle" size="sm" onClick={() => handleEditClick(row)}>
                                                <IconEdit size={14} />
                                            </ActionIcon>
                                        </Table.Td>
                                    </Table.Tr>
                                ))}
                            </Table.Tbody>
                        </Table>
                    </Paper>
                </Grid.Col>
            </Grid>

            <Modal opened={editOpened} onClose={closeEdit} title="Update Authorized Headcount (TO)">
                <Stack>
                    <Text size="sm">Set the authorized headcount for <b>{selectedUnit?.unit_name}</b>.</Text>
                    <NumberInput
                        label="Authorized Count"
                        value={newAuthorized}
                        onChange={(val) => setNewAuthorized(Number(val))}
                        min={0}
                        step={1}
                    />
                    <Button onClick={handleSave} loading={saving}>Save Changes</Button>
                </Stack>
            </Modal>
        </Container>
    );
}
