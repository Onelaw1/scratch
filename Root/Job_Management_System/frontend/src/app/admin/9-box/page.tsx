"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Group, Badge, Loader, SimpleGrid, Card, ThemeIcon, Avatar, Tooltip } from "@mantine/core";
import { IconStar, IconTrophy, IconAlertTriangle, IconUser } from "@tabler/icons-react";
import { api } from "@/lib/api";

type Employee9Box = {
    id: string;
    name: string;
    dept: string;
    performance: number;
    potential: number;
    box: number; // 1-9
    category: string;
    color: string;
};

type NineBoxData = {
    generated_at: string;
    total_employees: number;
    distribution: Record<string, number>;
    employees: Employee9Box[];
};

export default function NineBoxPage() {
    const [data, setData] = useState<NineBoxData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getNineBoxGrid()
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Container size="xl" py="xl"><Loader /></Container>;
    if (!data) return <Container size="xl" py="xl"><Text>No data available.</Text></Container>;

    // 9 Boxes Configuration (Reverse Order for Y-axis visual: High Pot on Top)
    // Grid:
    // [Pot High]  Box 7 (Enigma) | Box 8 (HiPo) | Box 9 (Star)
    // [Pot Mod ]  Box 4 (Incst)  | Box 5 (Core) | Box 6 (HiPerf)
    // [Pot Low ]  Box 1 (Risk)   | Box 2 (Eff)  | Box 3 (Pro)
    //             [Perf Low]       [Perf Mod]     [Perf High]

    // We render row by row: Row 1 (7,8,9), Row 2 (4,5,6), Row 3 (1,2,3)
    const gridRows = [
        [7, 8, 9],
        [4, 5, 6],
        [1, 2, 3]
    ];

    const getBoxTitle = (boxNum: number) => {
        switch (boxNum) {
            case 9: return "Star (Top Talent)";
            case 8: return "High Potential";
            case 7: return "Enigma (Rough Diamond)";
            case 6: return "High Performer";
            case 5: return "Core Player";
            case 4: return "Inconsistent Player";
            case 3: return "Trusted Professional";
            case 2: return "Effective Employee";
            case 1: return "Underperformer (Risk)";
            default: return "Unknown";
        }
    };

    const getBoxColor = (boxNum: number) => {
        if ([9, 8, 6].includes(boxNum)) return "var(--mantine-color-green-1)"; // Good
        if ([5, 3, 7].includes(boxNum)) return "var(--mantine-color-gray-1)"; // OK
        return "var(--mantine-color-red-1)"; // Bad
    };

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>9-Box Talent Matrix</Title>
                    <Text c="dimmed">
                        Strategic Talent Mapping (Performance vs. Potential)
                    </Text>
                </div>
                <Group>
                    <Badge size="lg" color="blue">Total: {data.total_employees}</Badge>
                    <Badge size="lg" color="green">Stars: {data.distribution.Star}</Badge>
                </Group>
            </Group>

            {/* The Grid */}
            <SimpleGrid cols={3} spacing={0} style={{ border: '1px solid #eee' }}>
                {gridRows.map((row, rowIdx) => (
                    row.map((boxNum) => {
                        const employeesInBox = data.employees.filter(e => e.box === boxNum);

                        return (
                            <Card
                                key={boxNum}
                                padding="sm"
                                radius={0}
                                withBorder
                                style={{
                                    height: '250px',
                                    backgroundColor: getBoxColor(boxNum),
                                    borderColor: '#ddd'
                                }}
                            >
                                <Group justify="space-between" mb="xs">
                                    <Text fw={700} size="sm">{getBoxTitle(boxNum)}</Text>
                                    <Badge variant="light" size="xs">{employeesInBox.length}</Badge>
                                </Group>

                                <div style={{ overflowY: 'auto', height: '100%' }}>
                                    {employeesInBox.map(emp => (
                                        <Card key={emp.id} shadow="xs" padding="xs" radius="sm" mb={4} bg="white">
                                            <Group gap="xs">
                                                <Avatar size="sm" color="blue" radius="xl">{emp.name.charAt(0)}</Avatar>
                                                <div>
                                                    <Text size="xs" fw={500}>{emp.name}</Text>
                                                    <Text size="xs" c="dimmed">{emp.dept}</Text>
                                                </div>
                                            </Group>
                                        </Card>
                                    ))}
                                </div>
                            </Card>
                        );
                    })
                ))}
            </SimpleGrid>

            {/* Axis Labels */}
            <Group justify="space-between" mt="xs">
                <Text size="sm" fw={700}>← Low Performance</Text>
                <Text size="sm" fw={700}>High Performance →</Text>
            </Group>
            <div style={{ position: 'relative', height: 0, top: '-400px', left: '-30px' }}>
                <Text size="sm" fw={700} style={{ transform: 'rotate(-90deg)', width: '150px' }}>Potential ↑</Text>
            </div>
        </Container>
    );
}
