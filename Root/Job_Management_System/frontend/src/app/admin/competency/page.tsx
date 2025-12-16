"use client";

import React, { useState, useEffect } from "react";
import { Container, Title, Text, Group, Select, Loader, SimpleGrid, Paper, Badge, Stack, ThemeIcon, RingProgress, Center } from "@mantine/core";
import { IconCheck, IconAlertCircle, IconRadar2, IconBook, IconSchool } from "@tabler/icons-react";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip as RechartsTooltip } from "recharts";
import { api } from "@/lib/api";
import { useLanguage } from "@/contexts/LanguageContext";

export default function CompetencyRadarPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const { t } = useLanguage();

    useEffect(() => {
        api.getUsers().then((res: any) => {
            setUsers(res);
            // Default select the first one if available
            if (res.length > 0 && !selectedUserId) {
                // Try to find a user with data if possible, or just first
                setSelectedUserId(res[0].id);
            }
        });
    }, []);

    useEffect(() => {
        if (!selectedUserId) return;
        setLoading(true);
        api.getCompetencyRadar(selectedUserId)
            .then(setData)
            .catch(err => console.error(err))
            .finally(() => setLoading(false));
    }, [selectedUserId]);

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl" align="flex-end">
                <div>
                    <Title order={2} style={{ letterSpacing: '-0.5px' }}>{t('comp.title')}</Title>
                    <Text c="dimmed">{t('comp.subtitle')}</Text>
                </div>
                <Select
                    data={users.map(u => ({ value: u.id, label: `${u.name} (${u.org_unit?.name || 'N/A'})` }))}
                    value={selectedUserId}
                    onChange={setSelectedUserId}
                    placeholder={t('comp.select_user')}
                    searchable
                    style={{ width: 300 }}
                    size="md"
                    radius="md"
                />
            </Group>

            {loading ? (
                <Container h={400} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <Loader size="lg" />
                </Container>
            ) : !selectedUserId ? (
                <Text ta="center" c="dimmed" py="xl">{t('comp.select_user')}</Text>
            ) : data && (
                <SimpleGrid cols={{ base: 1, md: 2 }} spacing="xl">
                    {/* Left: Radar Chart & Score */}
                    <Stack>
                        <Paper shadow="sm" radius="lg" p="xl" withBorder className="bg-white/50 backdrop-blur-sm">
                            <Group justify="center" mb="lg">
                                <RingProgress
                                    size={180}
                                    thickness={16}
                                    roundCaps
                                    sections={[{ value: data.fit_score, color: data.fit_score > 80 ? 'teal' : data.fit_score > 60 ? 'blue' : 'orange' }]}
                                    label={
                                        <Center>
                                            <Stack gap={0} align="center">
                                                <Text fw={700} size="xl">{data.fit_score}%</Text>
                                                <Text size="xs" c="dimmed">{t('comp.fit_score')}</Text>
                                            </Stack>
                                        </Center>
                                    }
                                />
                            </Group>

                            <div style={{ width: '100%', height: 400 }}>
                                <ResponsiveContainer>
                                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data.radar_data}>
                                        <PolarGrid gridType="polygon" />
                                        <PolarAngleAxis dataKey="skill" tick={{ fill: '#666', fontSize: 12 }} />
                                        <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
                                        <Radar
                                            name={t('comp.chart.required')}
                                            dataKey="required"
                                            stroke="#8884d8"
                                            fill="#8884d8"
                                            fillOpacity={0.3}
                                        />
                                        <Radar
                                            name={t('comp.chart.actual')}
                                            dataKey="actual"
                                            stroke="#82ca9d"
                                            fill="#82ca9d"
                                            fillOpacity={0.5}
                                        />
                                        <Legend />
                                        <RechartsTooltip />
                                    </RadarChart>
                                </ResponsiveContainer>
                            </div>
                        </Paper>
                    </Stack>

                    {/* Right: Analysis Details */}
                    <Stack>
                        <Paper shadow="md" radius="lg" p="lg" withBorder className="bg-white">
                            <Group justify="space-between" mb="md">
                                <Group>
                                    <ThemeIcon color="red" variant="light" size="lg" radius="md"><IconAlertCircle /></ThemeIcon>
                                    <Title order={4}>{t('comp.gaps_title')}</Title>
                                </Group>
                                <Badge color="red" variant="light">{data.analysis?.gaps.length || 0} {t('comp.issues_count')}</Badge>
                            </Group>

                            {!data.analysis?.gaps.length ? (
                                <Text c="dimmed" size="sm" py="md" ta="center">{t('comp.no_gaps')}</Text>
                            ) : (
                                <Stack gap="sm">
                                    {data.analysis.gaps.map((gap: any, idx: number) => (
                                        <Paper key={idx} withBorder p="sm" radius="md" bg="red.0" style={{ borderLeft: '4px solid var(--mantine-color-red-5)' }}>
                                            <Group align="flex-start" wrap="nowrap">
                                                <ThemeIcon color="red" variant="transparent" size="sm" mt={2}><IconBook /></ThemeIcon>
                                                <div style={{ flex: 1 }}>
                                                    <Text size="sm" fw={600} c="red.9">{gap.skill}</Text>
                                                    <Group gap="xs" mt={4}>
                                                        <Badge size="sm" color="red" variant="filled">Gap: {gap.gap}</Badge>
                                                        <Text size="xs" c="dimmed">{gap.action}</Text>
                                                    </Group>
                                                </div>
                                            </Group>
                                        </Paper>
                                    ))}
                                </Stack>
                            )}
                        </Paper>

                        <Paper shadow="md" radius="lg" p="lg" withBorder className="bg-white">
                            <Group justify="space-between" mb="md">
                                <Group>
                                    <ThemeIcon color="teal" variant="light" size="lg" radius="md"><IconCheck /></ThemeIcon>
                                    <Title order={4}>{t('comp.strengths_title')}</Title>
                                </Group>
                                <Badge color="teal" variant="light">{data.analysis?.strengths.length || 0} {t('comp.areas_count')}</Badge>
                            </Group>

                            {!data.analysis?.strengths.length ? (
                                <Text c="dimmed" size="sm" py="md" ta="center">{t('comp.no_strengths')}</Text>
                            ) : (
                                <Stack gap="sm">
                                    {data.analysis.strengths.map((str: any, idx: number) => (
                                        <Paper key={idx} withBorder p="sm" radius="md" bg="teal.0" style={{ borderLeft: '4px solid var(--mantine-color-teal-5)' }}>
                                            <Group align="flex-start" wrap="nowrap">
                                                <ThemeIcon color="teal" variant="transparent" size="sm" mt={2}><IconSchool /></ThemeIcon>
                                                <div style={{ flex: 1 }}>
                                                    <Text size="sm" fw={600} c="teal.9">{str.skill}</Text>
                                                    <Group gap="xs" mt={4}>
                                                        <Badge size="sm" color="teal" variant="filled">+{str.surplus}</Badge>
                                                        <Text size="xs" c="dimmed">{str.action}</Text>
                                                    </Group>
                                                </div>
                                            </Group>
                                        </Paper>
                                    ))}
                                </Stack>
                            )}
                        </Paper>
                    </Stack>
                </SimpleGrid>
            )}
        </Container>
    );
}
