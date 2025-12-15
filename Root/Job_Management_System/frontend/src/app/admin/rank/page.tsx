"use client";

import { useState, useEffect } from "react";
import { Container, Title, Text, Paper, Table, Group, Badge, Button, Loader, Tooltip, HoverCard, ThemeIcon, Progress, Card, SimpleGrid, Accordion } from "@mantine/core";
import { IconTrophy, IconChartArrowsVertical, IconHistory, IconTrendingUp, IconFileDownload, IconInfoCircle, IconCheck, IconHelp, IconAlertCircle } from "@tabler/icons-react";
import { api } from "@/lib/api";

type RankItem = {
    rank: number;
    user_id: number;
    name: string;
    department: string;
    current_grade: string;
    tenure_years: number;
    integral_score: number;
    growth_slope: number;
    score_tenure: number;
    score_integral: number;
    score_slope: number;
    total_score: number;
    tier: string;
    tier_color: string;
};

type RankData = {
    generated_at: string;
    total_candidates: number;
    rank_list: RankItem[];
};

export default function PromotionRankPage() {
    const [data, setData] = useState<RankData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getPromotionRankList()
            .then(setData)
            .catch((err) => console.error(err))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <Container size="xl" py="xl"><Loader /></Container>;
    if (!data) return <Container size="xl" py="xl"><Text>No data available.</Text></Container>;

    // Calculate Tiers counts for summary
    const certainCount = data.rank_list.filter(i => i.tier.includes("Certain")).length;
    const probableCount = data.rank_list.filter(i => i.tier.includes("Probable")).length;
    const holdCount = data.rank_list.filter(i => i.tier.includes("Hold")).length;

    return (
        <Container size="xl" py="xl">
            {/* Header */}
            <Group justify="space-between" mb="lg">
                <div>
                    <Title order={1}>Scientific Promotion Rank Register</Title>
                    <Text c="dimmed">
                        Official Ranking based on SPS (Scientific Promotion Score) • Generated: {data.generated_at}
                    </Text>
                </div>
                <Button leftSection={<IconFileDownload size={16} />} variant="outline" color="gray">
                    Export Formal PDF
                </Button>
            </Group>

            {/* Summary Cards */}
            <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="lg" mb="xl">
                <Card withBorder padding="lg" radius="md">
                    <Group justify="space-between">
                        <div>
                            <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Certain (확정)</Text>
                            <Text fz="xl" fw={700} c="teal">{certainCount} Candidates</Text>
                        </div>
                        <ThemeIcon color="teal" variant="light" size="lg">
                            <IconCheck size={20} />
                        </ThemeIcon>
                    </Group>
                    <Progress value={(certainCount / data.total_candidates) * 100} mt="md" color="teal" />
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Group justify="space-between">
                        <div>
                            <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Probable (유력)</Text>
                            <Text fz="xl" fw={700} c="blue">{probableCount} Candidates</Text>
                        </div>
                        <ThemeIcon color="blue" variant="light" size="lg">
                            <IconHelp size={20} />
                        </ThemeIcon>
                    </Group>
                    <Progress value={(probableCount / data.total_candidates) * 100} mt="md" color="blue" />
                </Card>
                <Card withBorder padding="lg" radius="md">
                    <Group justify="space-between">
                        <div>
                            <Text fz="xs" tt="uppercase" fw={700} c="dimmed">Hold (보류)</Text>
                            <Text fz="xl" fw={700} c="gray">{holdCount} Candidates</Text>
                        </div>
                        <ThemeIcon color="gray" variant="light" size="lg">
                            <IconAlertCircle size={20} />
                        </ThemeIcon>
                    </Group>
                    <Progress value={(holdCount / data.total_candidates) * 100} mt="md" color="gray" />
                </Card>
            </SimpleGrid>

            {/* Formula Explanation Accordion */}
            <Accordion variant="separated" mb="xl">
                <Accordion.Item value="formula">
                    <Accordion.Control icon={<IconInfoCircle size={20} />}>
                        <Text fw={500}>How is SPS Calculated?</Text>
                    </Accordion.Control>
                    <Accordion.Panel>
                        <Group align="flex-start">
                            <div>
                                <Text fw={700} mb={5}>Total SPS =</Text>
                                <Text size="sm">
                                    (Tenure × 10) + (Integral × 0.6) + (Slope × 30)
                                </Text>
                            </div>
                            <div style={{ flex: 1 }}>
                                <Text size="sm" c="dimmed">
                                    • <b>Tenure (10%)</b>: Rewards loyalty but has the lowest weight.<br />
                                    • <b>Integral (40%)</b>: Rewards long-term consistent performance (Area under curve).<br />
                                    • <b>Slope (50%)</b>: Rewards recent growth velocity and future potential. High impact.
                                </Text>
                            </div>
                        </Group>
                    </Accordion.Panel>
                </Accordion.Item>
            </Accordion>

            {/* Ranking Table */}
            <Paper withBorder shadow="sm" radius="md" p="md">
                <Table striped highlightOnHover>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Rank</Table.Th>
                            <Table.Th>Name</Table.Th>
                            <Table.Th>Dept / Current</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Tenure</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Integral (Area)</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Growth Slope</Table.Th>
                            <Table.Th style={{ textAlign: 'right' }}>Total SPS</Table.Th>
                            <Table.Th style={{ textAlign: 'center' }}>Status</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {data.rank_list.map((item) => (
                            <Table.Tr key={item.user_id}>
                                <Table.Td>
                                    <Text fw={700}>#{item.rank}</Text>
                                </Table.Td>
                                <Table.Td>
                                    <Text fw={500}>{item.name}</Text>
                                    <Text size="xs" c="dimmed">ID: {item.user_id}</Text>
                                </Table.Td>
                                <Table.Td>
                                    <Text size="sm">{item.department}</Text>
                                    <Badge size="xs" variant="outline">{item.current_grade}</Badge>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'right' }}>
                                    <Tooltip label={`Score: ${item.score_tenure} pts`}>
                                        <Text size="sm">{item.tenure_years} yr</Text>
                                    </Tooltip>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'right' }}>
                                    <Tooltip label={`Score: ${item.score_integral} pts`}>
                                        <Text size="sm" c="blue">{item.integral_score}</Text>
                                    </Tooltip>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'right' }}>
                                    <Tooltip label={`Score: ${item.score_slope} pts`}>
                                        <Group gap={4} justify="flex-end">
                                            {item.growth_slope > 1.0 && <IconTrendingUp size={14} color="green" />}
                                            <Text size="sm" fw={item.growth_slope > 1.0 ? 700 : 400} c={item.growth_slope > 0 ? 'dark' : 'red'}>
                                                {item.growth_slope}
                                            </Text>
                                        </Group>
                                    </Tooltip>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'right' }}>
                                    <Text fw={700} size="lg">{item.total_score}</Text>
                                </Table.Td>
                                <Table.Td style={{ textAlign: 'center' }}>
                                    <Badge color={item.tier_color} variant="filled" size="lg">
                                        {item.tier}
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
