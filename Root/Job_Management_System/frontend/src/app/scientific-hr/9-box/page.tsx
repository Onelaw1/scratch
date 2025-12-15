'use client';

import React, { useEffect, useState } from 'react';
import {
    Container, Title, Text, SimpleGrid, Paper, Group, Badge,
    Loader, Stack, ThemeIcon, Avatar, Tooltip, HoverCard
} from '@mantine/core';
import { IconUser, IconInfoCircle } from '@tabler/icons-react';
import { api } from '@/lib/api';

export default function NineBoxPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await api.getNineBoxGrid();
                setData(result);
            } catch (error) {
                console.error("Failed to load 9-box data", error);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) {
        return (
            <Container size="xl" py="xl" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <Loader size="lg" />
            </Container>
        );
    }

    // Define the grid structure (3x3)
    // Rows: High Pot, Mod Pot, Low Pot
    // Cols: Low Perf, Mod Perf, High Perf
    // Box IDs:
    // [7 (Enigma), 8 (High Pot), 9 (Star)]
    // [4 (Inconsistent), 5 (Core), 6 (High Performer)]
    // [1 (Risk), 2 (Effective), 3 (Trusted Pro)]

    const gridCells = [
        { id: 7, label: "Enigma (7)", color: "yellow", desc: "High Potential, Low Performance" },
        { id: 8, label: "High Potential (8)", color: "cyan", desc: "High Potential, Mod Performance" },
        { id: 9, label: "Star (9)", color: "blue", desc: "High Potential, High Performance" },
        { id: 4, label: "Inconsistent (4)", color: "orange", desc: "Mod Potential, Low Performance" },
        { id: 5, label: "Core Player (5)", color: "gray", desc: "Mod Potential, Mod Performance" },
        { id: 6, label: "High Performer (6)", color: "green", desc: "Mod Potential, High Performance" },
        { id: 1, label: "Risk (1)", color: "red", desc: "Low Potential, Low Performance" },
        { id: 2, label: "Effective (2)", color: "gray", desc: "Low Potential, Mod Performance" },
        { id: 3, label: "Trusted Pro (3)", color: "teal", desc: "Low Potential, High Performance" },
    ];

    const getEmployeesInBox = (boxId: number) => {
        return data?.employees.filter((e: any) => e.box === boxId) || [];
    };

    return (
        <Container size="xl" py="xl">
            <Stack gap="lg">
                <Group justify="space-between" align="center">
                    <div>
                        <Title order={2}>9-Box Talent Matrix</Title>
                        <Text c="dimmed">Scientific Talent Mapping based on Performance & Potential</Text>
                    </div>
                    <Badge size="lg" variant="light" color="blue">
                        Total: {data?.total_employees || 0}
                    </Badge>
                </Group>

                <SimpleGrid cols={3} spacing="md" verticalSpacing="md">
                    {gridCells.map((cell) => {
                        const employees = getEmployeesInBox(cell.id);

                        return (
                            <Paper
                                key={cell.id}
                                shadow="sm"
                                p="md"
                                radius="md"
                                withBorder
                                style={{ minHeight: '250px', display: 'flex', flexDirection: 'column' }}
                            >
                                <Group justify="space-between" mb="xs">
                                    <Text fw={700} size="sm" c="dimmed">{cell.label}</Text>
                                    <Badge variant="filled" color={cell.color} size="sm" circle>
                                        {employees.length}
                                    </Badge>
                                </Group>
                                <Text size="xs" c="dimmed" mb="md" lineClamp={2}>
                                    {cell.desc}
                                </Text>

                                <Stack gap="xs" style={{ flex: 1, overflowY: 'auto' }}>
                                    {employees.map((emp: any) => (
                                        <HoverCard key={emp.id} width={280} shadow="md">
                                            <HoverCard.Target>
                                                <Paper key={emp.id} withBorder p="xs" radius="sm" style={{ cursor: 'pointer' }}>
                                                    <Group gap="sm">
                                                        <Avatar size="sm" radius="xl" color="blue" name={emp.name}>
                                                            {emp.name.charAt(0)}
                                                        </Avatar>
                                                        <div style={{ flex: 1 }}>
                                                            <Text size="sm" fw={500} lineClamp={1}>{emp.name}</Text>
                                                            <Text size="xs" c="dimmed" lineClamp={1}>{emp.dept}</Text>
                                                        </div>
                                                    </Group>
                                                </Paper>
                                            </HoverCard.Target>
                                            <HoverCard.Dropdown>
                                                <Text size="sm" fw={700}>{emp.name}</Text>
                                                <Text size="xs" c="dimmed" mb="xs">{emp.dept}</Text>
                                                <Group gap="xs">
                                                    <Badge size="xs" variant="outline">Perf: {emp.performance}</Badge>
                                                    <Badge size="xs" variant="outline">Pot: {emp.potential}</Badge>
                                                </Group>
                                            </HoverCard.Dropdown>
                                        </HoverCard>
                                    ))}
                                </Stack>
                            </Paper>
                        );
                    })}
                </SimpleGrid>

                <Paper withBorder p="md" radius="md">
                    <Title order={5} mb="sm">Matrix Interpretation</Title>
                    <SimpleGrid cols={3}>
                        <Group>
                            <ThemeIcon color="blue" variant="light"><IconUser size={16} /></ThemeIcon>
                            <Text size="sm">Star: Priority for Promotion</Text>
                        </Group>
                        <Group>
                            <ThemeIcon color="yellow" variant="light"><IconUser size={16} /></ThemeIcon>
                            <Text size="sm">Enigma: Assess Fit / Coaching</Text>
                        </Group>
                        <Group>
                            <ThemeIcon color="teal" variant="light"><IconUser size={16} /></ThemeIcon>
                            <Text size="sm">Trusted: Retention Critical</Text>
                        </Group>
                    </SimpleGrid>
                </Paper>
            </Stack>
        </Container>
    );
}
