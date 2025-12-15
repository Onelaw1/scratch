"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, Stack, Badge,
    Avatar, Timeline, RingProgress, Select, Loader, SimpleGrid, ThemeIcon
} from "@mantine/core";
import { IconBriefcase, IconAward, IconSchool, IconHistory, IconUser } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function JobCardPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [cardData, setCardData] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadUsers();
    }, []);

    useEffect(() => {
        if (selectedUser) {
            loadCard(selectedUser);
        } else {
            setCardData(null);
        }
    }, [selectedUser]);

    const loadUsers = async () => {
        try {
            // Reusing the logic to fetch users via positions
            const res = await api.getEvaluationPositions();
            const usersWithPos = res.filter((p: any) => p.user_id).map((p: any) => ({
                value: p.user_id,
                label: `${p.user?.name || 'Unknown'} (${p.title})`
            }));
            // Remove duplicates if user has multiple positions ? 
            // Ideally uniq by user_id
            const uniqueUsers = Array.from(new Map(usersWithPos.map((item: any) => [item.value, item])).values());
            setUsers(uniqueUsers);
            if (uniqueUsers.length > 0) setSelectedUser((uniqueUsers[0] as any).value);
        } catch (error) {
            console.error(error);
        }
    };

    const loadCard = async (userId: string) => {
        setLoading(true);
        try {
            const data = await api.getJobManagementCard(userId);
            setCardData(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2}>Job Management Card</Title>
                    <Text c="dimmed">Comprehensive One-Page Report for Employee/Job</Text>
                </div>
                <Select
                    placeholder="Search Employee"
                    data={users}
                    value={selectedUser}
                    onChange={setSelectedUser}
                    searchable
                    className="w-72"
                />
            </Group>

            {loading ? (
                <Grid>
                    <Grid.Col span={12}><Loader /></Grid.Col>
                </Grid>
            ) : cardData ? (
                <Stack gap="lg">
                    {/* Header: Profile */}
                    <Paper p="xl" radius="md" withBorder bg="var(--mantine-color-blue-0)">
                        <Group>
                            <Avatar size={80} radius="xl" color="blue">
                                <IconUser size={40} />
                            </Avatar>
                            <div style={{ flex: 1 }}>
                                <Group align="center" gap="xs">
                                    <Title order={3}>{cardData.profile.name}</Title>
                                    <Badge size="lg" variant="filled" color="indigo">{cardData.position.grade || 'N/A'}</Badge>
                                </Group>
                                <Text size="lg" c="dimmed" mb={4}>{cardData.position.title}</Text>
                                <Group gap="md">
                                    <Text size="sm"><span className="font-semibold">Department:</span> {cardData.profile.department}</Text>
                                    <Text size="sm"><span className="font-semibold">Series:</span> {cardData.position.series}</Text>
                                    <Text size="sm"><span className="font-semibold">Email:</span> {cardData.profile.email || '-'}</Text>
                                </Group>
                            </div>
                        </Group>
                    </Paper>

                    <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
                        {/* 1. Job Evaluation Status */}
                        <Paper p="md" withBorder radius="md">
                            <Group mb="md">
                                <ThemeIcon size="lg" color="violet" variant="light"><IconBriefcase /></ThemeIcon>
                                <Text fw={700}>Job Value</Text>
                            </Group>
                            <Stack align="center" gap={0}>
                                <Text size="xs" tt="uppercase" c="dimmed" fw={700}>Job Grade</Text>
                                <Text size="3rem" fw={900} variant="gradient" gradient={{ from: 'violet', to: 'blue', deg: 45 }}>
                                    {cardData.position.grade || '-'}
                                </Text>
                                <Text size="sm" c="dimmed">{cardData.position.group}</Text>
                            </Stack>
                        </Paper>

                        {/* 2. Performance Status */}
                        <Paper p="md" withBorder radius="md">
                            <Group mb="md">
                                <ThemeIcon size="lg" color="green" variant="light"><IconAward /></ThemeIcon>
                                <Text fw={700}>Performance</Text>
                            </Group>
                            <Group justify="center" gap="xl">
                                <Stack align="center" gap={0}>
                                    <Text size="xs" tt="uppercase" c="dimmed" fw={700}>Appraisal</Text>
                                    <Text size="3rem" fw={900} c={getPerformanceColor(cardData.performance.grade)}>
                                        {cardData.performance.grade || '-'}
                                    </Text>
                                    <Text size="xs" c="dimmed">{cardData.performance.year || 'No Data'}</Text>
                                </Stack>
                            </Group>
                        </Paper>

                        {/* 3. Training & Competency */}
                        <Paper p="md" withBorder radius="md">
                            <Group mb="md">
                                <ThemeIcon size="lg" color="orange" variant="light"><IconSchool /></ThemeIcon>
                                <Text fw={700}>Development</Text>
                            </Group>
                            <Stack gap="xs">
                                {cardData.trainings.length === 0 && <Text c="dimmed" size="sm">No training history.</Text>}
                                {cardData.trainings.map((t: any, idx: number) => (
                                    <Group key={idx} justify="space-between">
                                        <Text size="sm" lineClamp={1}>{t.program}</Text>
                                        <Badge size="xs" variant="outline" color={t.status === 'COMPLETED' ? 'green' : 'gray'}>
                                            {t.status}
                                        </Badge>
                                    </Group>
                                ))}
                            </Stack>
                        </Paper>
                    </SimpleGrid>

                    {/* Timeline: History */}
                    <Grid>
                        <Grid.Col span={12}>
                            <Paper p="md" withBorder radius="md">
                                <Group mb="lg">
                                    <ThemeIcon size="lg" color="gray" variant="light"><IconHistory /></ThemeIcon>
                                    <Text fw={700}>Job Profile History</Text>
                                </Group>
                                <Timeline active={0} bulletSize={24} lineWidth={2}>
                                    {cardData.history.map((h: any, idx: number) => (
                                        <Timeline.Item key={idx} title={h.title}>
                                            <Text c="dimmed" size="sm">{h.period} • {h.series}</Text>
                                        </Timeline.Item>
                                    ))}
                                </Timeline>
                            </Paper>
                        </Grid.Col>
                    </Grid>
                </Stack>
            ) : (
                <Text c="dimmed">Select an employee to view their Job Management Card.</Text>
            )}
        </Container>
    );
}

function getPerformanceColor(grade: string) {
    if (['S', 'A'].includes(grade)) return 'blue';
    if (['B'].includes(grade)) return 'green';
    if (['C'].includes(grade)) return 'yellow';
    return 'red';
}
