"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, Stack, Badge,
    Tabs, Table, Button, Select, Loader, SimpleGrid, ThemeIcon
} from "@mantine/core";
import {
    IconTrophy, IconSchool, IconChartRadar, IconUser, IconCheck
} from "@tabler/icons-react";
import { api } from "@/lib/api";
import { Radar } from 'recharts'; // Mantine doesn't have built-in Radar yet, using a placeholder or need access to recharts direct?
// Actually we can use Recharts directly if installed, or just simulate with Progress bars for MVP stability.
// Let's use simple Progress bars for Competency to avoid dependency hell if Recharts not perfectly setup for Radar.
import { Progress } from "@mantine/core";

export default function CareerDevelopmentPage() {
    const [activeTab, setActiveTab] = useState<string | null>('promotion');

    // Promotion State
    const [candidates, setCandidates] = useState<any[]>([]);
    const [loadingCandidates, setLoadingCandidates] = useState(false);

    // Training State
    const [users, setUsers] = useState<any[]>([]);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [trainingRecs, setTrainingRecs] = useState<any[]>([]);

    // Competency State
    const [seriesList, setSeriesList] = useState<any[]>([]);
    const [selectedSeries, setSelectedSeries] = useState<string | null>(null);
    const [competencyModel, setCompetencyModel] = useState<any>(null);

    useEffect(() => {
        loadCandidates();
        loadUsersAndSeries();
    }, []);

    useEffect(() => {
        if (selectedUser) loadTraining(selectedUser);
    }, [selectedUser]);

    useEffect(() => {
        if (selectedSeries) loadCompetency(selectedSeries);
    }, [selectedSeries]);

    const loadCandidates = async () => {
        setLoadingCandidates(true);
        try {
            const data = await api.getPromotionCandidates();
            setCandidates(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoadingCandidates(false);
        }
    };

    const loadUsersAndSeries = async () => {
        try {
            // Users
            const posData = await api.getEvaluationPositions();
            const usersWithPos = posData.filter((p: any) => p.user_id).map((p: any) => ({
                value: p.user_id,
                label: `${p.user?.name || 'Unknown'} (${p.title})`
            }));
            setUsers(Array.from(new Map(usersWithPos.map((item: any) => [item.value, item])).values()));

            // Series (from same data for MVP)
            const seriesMap = new Map();
            posData.forEach((p: any) => {
                if (p.series) seriesMap.set(p.series.id, p.series.name);
            });
            setSeriesList(Array.from(seriesMap.entries()).map(([id, name]) => ({ value: id, label: name })));

        } catch (error) { console.error(error); }
    };

    const loadTraining = async (uid: string) => {
        try {
            const data = await api.getTrainingRecommendations(uid);
            setTrainingRecs(data);
        } catch (error) { console.error(error); }
    };

    const loadCompetency = async (sid: string) => {
        try {
            const data = await api.getCompetencyModel(sid);
            setCompetencyModel(data);
        } catch (error) { console.error(error); }
    };

    return (
        <Container size="xl" py="xl">
            <Group mb="xl">
                <div>
                    <Title order={2}>Career Development</Title>
                    <Text c="dimmed">Integrated Talent Management (Promotion, Competency, Training)</Text>
                </div>
            </Group>

            <Tabs value={activeTab} onChange={setActiveTab} radius="md">
                <Tabs.List>
                    <Tabs.Tab value="promotion" leftSection={<IconTrophy size={16} />}>Promotion Management</Tabs.Tab>
                    <Tabs.Tab value="competency" leftSection={<IconChartRadar size={16} />}>Competency Modeling</Tabs.Tab>
                    <Tabs.Tab value="training" leftSection={<IconSchool size={16} />}>Training Plan</Tabs.Tab>
                </Tabs.List>

                {/* Tab 1: Promotion */}
                <Tabs.Panel value="promotion" p="md">
                    <Grid>
                        <Grid.Col span={12}>
                            <Paper withBorder p="md" radius="md">
                                <Title order={4} mb="md">Promotion Candidates</Title>
                                <Text size="sm" c="dimmed" mb="lg">
                                    Employees with excellent performance (S/A) eligible for the next grade.
                                </Text>

                                {loadingCandidates ? <Loader /> : (
                                    <Table verticalSpacing="sm">
                                        <Table.Thead>
                                            <Table.Tr>
                                                <Table.Th>Name</Table.Th>
                                                <Table.Th>Current Position</Table.Th>
                                                <Table.Th>Current Grade</Table.Th>
                                                <Table.Th>Performance</Table.Th>
                                                <Table.Th>Action</Table.Th>
                                            </Table.Tr>
                                        </Table.Thead>
                                        <Table.Tbody>
                                            {candidates.map((c, idx) => (
                                                <Table.Tr key={idx}>
                                                    <Table.Td>
                                                        <Group gap="xs">
                                                            <ThemeIcon color="blue" variant="light" size="sm"><IconUser size={12} /></ThemeIcon>
                                                            <Text fw={500}>{c.name}</Text>
                                                        </Group>
                                                    </Table.Td>
                                                    <Table.Td>{c.current_title}</Table.Td>
                                                    <Table.Td><Badge variant="outline">{c.current_grade}</Badge></Table.Td>
                                                    <Table.Td>
                                                        <Badge color="teal" variant="filled">{c.performance_grade} ({c.performance_year})</Badge>
                                                    </Table.Td>
                                                    <Table.Td>
                                                        <Button size="xs" variant="light" color="indigo" leftSection={<IconCheck size={14} />}>
                                                            Promote
                                                        </Button>
                                                    </Table.Td>
                                                </Table.Tr>
                                            ))}
                                            {candidates.length === 0 && (
                                                <Table.Tr><Table.Td colSpan={5}><Text ta="center" c="dimmed">No eligible candidates found.</Text></Table.Td></Table.Tr>
                                            )}
                                        </Table.Tbody>
                                    </Table>
                                )}
                            </Paper>
                        </Grid.Col>
                    </Grid>
                </Tabs.Panel>

                {/* Tab 2: Competency */}
                <Tabs.Panel value="competency" p="md">
                    <Grid>
                        <Grid.Col span={12}>
                            <Select
                                label="Select Job Series"
                                placeholder="Choose..."
                                data={seriesList}
                                value={selectedSeries}
                                onChange={setSelectedSeries}
                                className="mb-4 w-64"
                            />

                            {competencyModel ? (
                                <Paper p="xl" withBorder radius="md">
                                    <Group mb="xl" justify="space-between">
                                        <Title order={3}>{competencyModel.series_name} Model</Title>
                                        <Badge>KSA Structured</Badge>
                                    </Group>

                                    <SimpleGrid cols={{ base: 1, md: 2 }} spacing="xl">
                                        {competencyModel.competencies.map((c: any, idx: number) => (
                                            <div key={idx}>
                                                <Group justify="space-between" mb={4}>
                                                    <Text fw={600}>{c.name}</Text>
                                                    <Text size="sm" c="dimmed">{c.type} ({c.score}/5.0)</Text>
                                                </Group>
                                                <Progress
                                                    value={(c.score / 5) * 100}
                                                    size="lg"
                                                    radius="md"
                                                    color={c.type === 'Knowledge' ? 'blue' : c.type === 'Skill' ? 'cyan' : 'grape'}
                                                />
                                            </div>
                                        ))}
                                    </SimpleGrid>
                                </Paper>
                            ) : (
                                <Text c="dimmed">Select a Job Series to view its Competency Model.</Text>
                            )}
                        </Grid.Col>
                    </Grid>
                </Tabs.Panel>

                {/* Tab 3: Training */}
                <Tabs.Panel value="training" p="md">
                    <Grid>
                        <Grid.Col span={12}>
                            <Select
                                label="Select Employee"
                                placeholder="Search..."
                                data={users}
                                value={selectedUser}
                                onChange={setSelectedUser}
                                className="mb-4 w-64"
                                searchable
                            />

                            {selectedUser && trainingRecs.length > 0 ? (
                                <Grid>
                                    {trainingRecs.map((t, idx) => (
                                        <Grid.Col key={idx} span={{ base: 12, md: 6 }}>
                                            <Paper p="md" withBorder className="border-l-4 border-l-orange-400">
                                                <Group justify="space-between" mb="xs">
                                                    <Badge color="orange" variant="light">{t.type}</Badge>
                                                    <Button size="xs" variant="subtle">Enroll</Button>
                                                </Group>
                                                <Text fw={700} size="lg">{t.title}</Text>
                                                <Text c="dimmed" size="sm" mt="sm">Reason: {t.reason}</Text>
                                            </Paper>
                                        </Grid.Col>
                                    ))}
                                </Grid>
                            ) : selectedUser ? (
                                <Text c="dimmed">No specific training recommendations found.</Text>
                            ) : (
                                <Text c="dimmed">Select an employee to view training plan.</Text>
                            )}
                        </Grid.Col>
                    </Grid>
                </Tabs.Panel>
            </Tabs>
        </Container>
    );
}
