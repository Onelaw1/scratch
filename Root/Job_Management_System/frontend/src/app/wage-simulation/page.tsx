"use client";

import React, { useState } from "react";
import {
    Container, Title, Text, Paper, Group, Grid, Slider,
    RingProgress, Stack, Badge, ThemeIcon, Button, Loader,
    Alert
} from "@mantine/core";
import {
    IconChartDots, IconCurrencyDollar, IconArrowUpRight,
    IconAlertTriangle, IconRefresh, IconAdjustments
} from "@tabler/icons-react";
import { api } from "@/lib/api";
// Custom SVG implementation used for Scatter Plot to avoid external dependencies.

export default function WageSimulationPage() {
    const [spread, setSpread] = useState(0.3); // 30%
    const [baseIncrease, setBaseIncrease] = useState(2.0); // 2%

    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const handleSimulate = async () => {
        setLoading(true);
        try {
            const data = await api.runWageSimulation(spread, baseIncrease / 100);
            setResult(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    // Helper to visualize bands vs scatter
    const renderScatter = () => {
        if (!result) return null;
        // Simple SVG implementation for "Scatter + Band" visualization
        // X-Axis: Grades (0 to 4), Y-Axis: Salary
        const height = 400;
        const width = 600;
        const padding = 40;

        // Find Max Salary for scaling
        const maxSal = 120000000;
        const grades = ["G1", "G2", "G3", "G4", "G5"];

        const yScale = (val: number) => height - padding - ((val / maxSal) * (height - 2 * padding));
        const xScale = (idx: number) => padding + (idx * ((width - 2 * padding) / 4));

        return (
            <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} className="overflow-visible">
                {/* Axes */}
                <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#ccc" />
                <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#ccc" />

                {/* Bands */}
                {grades.map((g, i) => {
                    const band = result.bands[g];
                    if (!band) return null;
                    const x = xScale(i) - 30;
                    const w = 60;
                    const yTop = yScale(band.max);
                    const yBot = yScale(band.min);
                    const h = yBot - yTop;

                    return (
                        <g key={g}>
                            <rect x={x} y={yTop} width={w} height={h} fill="rgba(130, 201, 30, 0.2)" stroke="rgba(130, 201, 30, 0.5)" rx={4} />
                            <line x1={x} y1={yScale(band.mid)} x2={x + w} y2={yScale(band.mid)} stroke="rgba(130, 201, 30, 1)" strokeDasharray="4" />
                            <text x={x + 30} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">{g}</text>
                        </g>
                    );
                })}

                {/* Scatter Points */}
                {result.scatter_data.map((pt: any, i: number) => {
                    const gIdx = grades.indexOf(pt.grade);
                    if (gIdx === -1) return null;

                    // Add some jitter
                    const jitter = (i % 10) - 5;
                    const x = xScale(gIdx) + jitter;
                    const y = yScale(pt.new_salary);

                    let color = "#228be6"; // Blue (In Band)
                    if (pt.status === "BELOW_MIN") color = "#fa5252"; // Red (Raised)
                    if (pt.status === "ABOVE_MAX") color = "#fab005"; // Yellow (Capped)

                    return (
                        <circle key={i} cx={x} cy={y} r={4} fill={color} opacity={0.7}>
                            <title>{`${pt.name}: ${pt.status} (${(pt.new_salary / 10000).toFixed(0)}만원)`}</title>
                        </circle>
                    );
                })}
            </svg>
        );
    };

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="md" color="lime" variant="light">
                        <IconChartDots size={28} />
                    </ThemeIcon>
                    Wage Transition Simulator
                </Title>
                <Text c="dimmed" size="lg">Analyze the financial impact of shifting to a Job-Based Wage System.</Text>
            </div>

            <Grid>
                {/* Control Panel */}
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="xl" radius="md" withBorder className="bg-gray-50 h-full">
                        <Stack gap="xl">
                            <Title order={3}>Simulation Parameters</Title>

                            <div>
                                <Text fw={500} mb="xs">Pay Band Spread (Width)</Text>
                                <Text size="sm" c="dimmed" mb="md">Wider bands allow more flexibility but cost less to adjust.</Text>
                                <Group>
                                    <Slider
                                        value={spread} onChange={setSpread}
                                        min={0.1} max={0.6} step={0.05}
                                        label={(val) => `${(val * 100).toFixed(0)}%`}
                                        className="flex-1" color="lime"
                                    />
                                    <Badge size="lg" color="lime" variant="light">{(spread * 100).toFixed(0)}%</Badge>
                                </Group>
                            </div>

                            <div>
                                <Text fw={500} mb="xs">Base Pay Increase</Text>
                                <Text size="sm" c="dimmed" mb="md">General increase applied before band adjustment.</Text>
                                <Group>
                                    <Slider
                                        value={baseIncrease} onChange={setBaseIncrease}
                                        min={0.0} max={10.0} step={0.5}
                                        label={(val) => `${val}%`}
                                        className="flex-1" color="blue"
                                    />
                                    <Badge size="lg" color="blue" variant="light">{baseIncrease}%</Badge>
                                </Group>
                            </div>

                            <Button
                                size="lg" color="lime"
                                leftSection={<IconAdjustments size={20} />}
                                onClick={handleSimulate}
                                loading={loading}
                            >
                                Run Simulation
                            </Button>

                            {result && (
                                <Alert color="gray" title="Scenarios" icon={<IconAlertTriangle size={16} />}>
                                    Adjusting options creates a new "To-Be" scenario.
                                </Alert>
                            )}
                        </Stack>
                    </Paper>
                </Grid.Col>

                {/* Visualization Panel */}
                <Grid.Col span={{ base: 12, md: 8 }}>
                    <Stack>
                        {/* Summary Cards */}
                        {result && (
                            <Grid>
                                <Grid.Col span={4}>
                                    <Paper p="md" radius="md" withBorder>
                                        <Text size="xs" c="dimmed" fw={700}>TOTAL COST INCREASE</Text>
                                        <Group align="flex-end" gap="xs">
                                            <Title order={2} c={result.summary.increase_pct > 5 ? "red" : "teal"}>
                                                +{result.summary.increase_pct.toFixed(2)}%
                                            </Title>
                                            <Text size="sm" mb={4} c="dimmed">
                                                ({(result.summary.increase_amount / 1000000).toFixed(1)}M KRW)
                                            </Text>
                                        </Group>
                                    </Paper>
                                </Grid.Col>
                                <Grid.Col span={4}>
                                    <Paper p="md" radius="md" withBorder>
                                        <Text size="xs" c="dimmed" fw={700}>BELOW BAND (RAISED)</Text>
                                        <Group align="flex-end" gap="xs">
                                            <Title order={2} c="orange">
                                                {result.summary.impacted_below_count}
                                            </Title>
                                            <Text size="sm" mb={4} c="dimmed">Employees</Text>
                                        </Group>
                                    </Paper>
                                </Grid.Col>
                                <Grid.Col span={4}>
                                    <Paper p="md" radius="md" withBorder>
                                        <Text size="xs" c="dimmed" fw={700}>AVG INCREASE</Text>
                                        <Group align="flex-end" gap="xs">
                                            <Title order={2} c="blue">
                                                {((result.summary.total_new_cost / result.summary.total_current_cost - 1) * 100).toFixed(1)}%
                                            </Title>
                                        </Group>
                                    </Paper>
                                </Grid.Col>
                            </Grid>
                        )}

                        {/* Chart */}
                        <Paper p="lg" radius="md" withBorder h={500} className="relative flex items-center justify-center bg-white">
                            {loading ? (
                                <Loader size="xl" type="dots" />
                            ) : result ? (
                                <div className="w-full h-full">
                                    <Text ta="center" size="sm" c="dimmed" mb="md">Job Grade vs. Salary Scatter Plot</Text>
                                    {renderScatter()}
                                    <Group justify="center" gap="xl" mt="xs">
                                        <Group gap={4}><Badge size="dot" color="blue">In Band</Badge></Group>
                                        <Group gap={4}><Badge size="dot" color="red">Raised (Below Min)</Badge></Group>
                                        <Group gap={4}><Badge size="dot" color="yellow">Capped (Above Max)</Badge></Group>
                                    </Group>
                                </div>
                            ) : (
                                <div className="text-center text-gray-400">
                                    <IconChartDots size={64} className="mx-auto mb-4 opacity-50" />
                                    <Text>Run simulation to view analysis</Text>
                                </div>
                            )}
                        </Paper>
                    </Stack>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
