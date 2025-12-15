"use client";

import React, { useEffect, useState } from "react";
import {
    Container, Title, Text, Paper, Group, Stack, RingProgress,
    Button, ThemeIcon, Avatar, SimpleGrid, Badge, ActionIcon, Loader
} from "@mantine/core";
import {
    IconTarget, IconBook, IconMoodSmile, IconBell, IconBriefcase, IconChevronRight
} from "@tabler/icons-react";
import { api } from "@/lib/api";
import Link from "next/link";

export default function MyJobPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await api.getMyJobDashboard();
                setData(res);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    if (loading) return <Container className="py-20 text-center"><Loader /></Container>;
    if (!data) return <Container className="py-20 text-center">Failed to load dashboard.</Container>;

    return (
        <Container size="xs" p="md" className="bg-gray-50 min-h-screen">
            {/* Top Bar */}
            <Group justify="space-between" mb="xl">
                <div>
                    <Text size="xs" c="dimmed" fw={700}>GOOD MORNING</Text>
                    <Title order={2}>{data.user.name}</Title>
                </div>
                <div className="relative">
                    <ActionIcon variant="light" radius="xl" size="lg">
                        <IconBell size={20} />
                    </ActionIcon>
                    {data.notifications.length > 0 && (
                        <Badge
                            circle
                            size="xs"
                            color="red"
                            className="absolute -top-1 -right-1"
                        >
                            {data.notifications.length}
                        </Badge>
                    )}
                </div>
            </Group>

            {/* My Role Card */}
            <Paper radius="lg" p="lg" className="bg-white shadow-sm mb-6">
                <Group>
                    <ThemeIcon size={48} radius="md" variant="gradient" gradient={{ from: 'blue', to: 'indigo' }}>
                        <IconBriefcase size={28} />
                    </ThemeIcon>
                    <div style={{ flex: 1 }}>
                        <Text size="xs" c="dimmed" fw={700}>CURRENT ROLE</Text>
                        <Text fw={700} size="lg">{data.user.title}</Text>
                        <Text size="sm" c="dimmed">{data.user.department}</Text>
                    </div>
                </Group>
            </Paper>

            {/* Pulse Check-In (Hero Action) */}
            <Paper
                radius="lg"
                p="xl"
                className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-lg mb-8 relative overflow-hidden"
                component={Link}
                href="/my-job/pulse"
            >
                <div className="relative z-10">
                    <Text size="xs" fw={700} className="mb-1 opacity-80">DAILY CHECK-IN</Text>
                    <Title order={3} className="mb-4">How is your energy today?</Title>
                    <Button variant="white" color="indigo" radius="xl">
                        Log Mood & Workload
                    </Button>
                </div>
                <IconMoodSmile
                    size={120}
                    className="absolute -bottom-4 -right-4 opacity-20 text-white rotate-12"
                />
            </Paper>

            {/* Quick Stats Grid */}
            <SimpleGrid cols={2} spacing="md" mb="xl">
                <Paper radius="lg" p="md" className="bg-white shadow-sm">
                    <Group align="flex-start" justify="space-between">
                        <ThemeIcon color="teal" variant="light" size="lg" radius="md"><IconTarget size={20} /></ThemeIcon>
                        <Text fw={700} size="xl">{data.stats.goals_completed}</Text>
                    </Group>
                    <Text size="sm" c="dimmed" mt="xs">Goals Met</Text>
                </Paper>
                <Paper radius="lg" p="md" className="bg-white shadow-sm">
                    <Group align="flex-start" justify="space-between">
                        <ThemeIcon color="orange" variant="light" size="lg" radius="md"><IconBook size={20} /></ThemeIcon>
                        <Text fw={700} size="xl">{data.stats.training_hours}h</Text>
                    </Group>
                    <Text size="sm" c="dimmed" mt="xs">Training</Text>
                </Paper>
            </SimpleGrid>

            {/* Key Tasks List */}
            <Text size="sm" fw={700} c="dimmed" mb="sm">CORE RESPONSIBILITIES</Text>
            <Stack gap="sm">
                {data.key_tasks.map((task: string, i: number) => (
                    <Paper key={i} radius="md" p="md" className="bg-white shadow-sm hover:bg-gray-50 cursor-pointer transition-colors">
                        <Group justify="space-between">
                            <Text size="sm" fw={500}>{task}</Text>
                            <IconChevronRight size={16} className="text-gray-300" />
                        </Group>
                    </Paper>
                ))}
            </Stack>
        </Container>
    );
}
