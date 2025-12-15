"use client";

import { useState, useEffect } from "react";
import { Container, Grid, Paper, Title, Text, Group, Button, Badge, ScrollArea, Slider, Stack, Divider, Loader, RingProgress, Center } from "@mantine/core";
import { useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { IconCalculator, IconCheck, IconTrophy } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function JobEvaluationPage() {
    const [positions, setPositions] = useState<any[]>([]);
    const [selectedPosition, setSelectedPosition] = useState<any>(null);
    const [evaluation, setEvaluation] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [calculating, setCalculating] = useState(false);

    const form = useForm({
        initialValues: {
            score_expertise: 0,
            score_responsibility: 0,
            score_complexity: 0,
        },
    });

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const data = await api.getEvaluationPositions();
            setPositions(data);
            setLoading(false);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load positions', color: 'red' });
            setLoading(false);
        }
    };

    const handleSelectPosition = async (pos: any) => {
        setSelectedPosition(pos);
        // Reset form or load existing scores if needed
        // For MVP, we assume a fresh evaluation session or overwrite
        if (pos.evaluation) {
            setEvaluation(pos.evaluation);
            // We could load scores here if we fetched them
        } else {
            setEvaluation(null);
            // Create a draft evaluation if needed, or wait until save
        }
    };

    const handleCalculate = async () => {
        if (!selectedPosition) return;

        setCalculating(true);
        try {
            // 1. Create Evaluation Context if not exists
            let evalId = evaluation?.id;
            if (!evalId) {
                const newEval = await api.createEvaluation(selectedPosition.id);
                evalId = newEval.id;
                setEvaluation(newEval);
            }

            // 2. Save Scores (Simulating "Self" or "Admin" rater for now)
            await api.saveEvaluationScore({
                evaluation_id: evalId,
                rater_type: "EXTERNAL", // Admin/Committee mode
                ...form.values
            });

            // 3. Trigger Calculation
            const result = await api.calculateEvaluationResult(evalId);
            setEvaluation(result);

            // 4. Update local list
            const updatedPositions = positions.map(p =>
                p.id === selectedPosition.id ? { ...p, evaluation: result } : p
            );
            setPositions(updatedPositions);

            notifications.show({ title: 'Success', message: `Graded as ${result.grade}`, color: 'green' });
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Evaluation failed', color: 'red' });
        } finally {
            setCalculating(false);
        }
    };

    const getGradeColor = (grade: string) => {
        switch (grade) {
            case 'G1': return 'violet';
            case 'G2': return 'indigo';
            case 'G3': return 'blue';
            case 'G4': return 'cyan';
            default: return 'gray';
        }
    };

    return (
        <Container size="xl" py="xl">
            <Title order={2} mb="xl">Job Evaluation & Grading</Title>

            <Grid>
                {/* Sidebar: Job List */}
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="md" withBorder radius="lg" h={700} style={{ display: 'flex', flexDirection: 'column' }}>
                        <Text fw={700} c="dimmed" mb="md" tt="uppercase">Evaluation Targets</Text>
                        <ScrollArea style={{ flex: 1 }}>
                            <Stack gap="xs">
                                {loading ? <Loader size="sm" /> : positions.map((pos) => (
                                    <Paper
                                        key={pos.id}
                                        p="sm"
                                        radius="md"
                                        withBorder={selectedPosition?.id === pos.id}
                                        onClick={() => handleSelectPosition(pos)}
                                        style={{
                                            cursor: 'pointer',
                                            backgroundColor: selectedPosition?.id === pos.id ? 'var(--mantine-primary-color-light)' : 'transparent',
                                            transition: 'all 0.2s',
                                        }}
                                        className="hover:bg-gray-50"
                                    >
                                        <Group justify="space-between">
                                            <div>
                                                <Text fw={600} size="sm">{pos.title}</Text>
                                                <Text size="xs" c="dimmed">{pos.series?.name}</Text>
                                            </div>
                                            {pos.evaluation?.grade ? (
                                                <Badge color={getGradeColor(pos.evaluation.grade)} variant="filled">
                                                    {pos.evaluation.grade}
                                                </Badge>
                                            ) : (
                                                <Badge color="gray" variant="light">Pending</Badge>
                                            )}
                                        </Group>
                                    </Paper>
                                ))}
                            </Stack>
                        </ScrollArea>
                    </Paper>
                </Grid.Col>

                {/* Main: Scoring Form */}
                <Grid.Col span={{ base: 12, md: 8 }}>
                    {selectedPosition ? (
                        <Paper p="xl" withBorder radius="lg" shadow="sm" h={700} style={{ display: 'flex', flexDirection: 'column' }}>
                            <Group justify="space-between" mb="lg">
                                <div>
                                    <Text size="sm" c="dimmed" tt="uppercase" fw={700}>Scoring for</Text>
                                    <Title order={3}>{selectedPosition.title}</Title>
                                </div>
                                {evaluation?.grade && (
                                    <Badge size="xl" radius="md" gradient={{ from: 'indigo', to: 'cyan' }} variant="gradient">
                                        Current Grade: {evaluation.grade}
                                    </Badge>
                                )}
                            </Group>

                            <Divider mb="xl" />

                            <ScrollArea style={{ flex: 1 }}>
                                <Stack gap="xl" px="sm">
                                    {/* Factor 1: Expertise */}
                                    <div>
                                        <Group justify="space-between" mb="xs">
                                            <Text fw={600}>1. Expertise & Knowledge (Max 100)</Text>
                                            <Badge size="lg" color="blue">{form.values.score_expertise}</Badge>
                                        </Group>
                                        <Text size="sm" c="dimmed" mb="md">
                                            Depth of technical knowledge and breadth of skills required.
                                        </Text>
                                        <Slider
                                            max={100}
                                            step={5}
                                            marks={[
                                                { value: 20, label: 'Basic' },
                                                { value: 50, label: 'Proficient' },
                                                { value: 80, label: 'Expert' },
                                            ]}
                                            {...form.getInputProps('score_expertise')}
                                        />
                                    </div>

                                    {/* Factor 2: Responsibility */}
                                    <div>
                                        <Group justify="space-between" mb="xs">
                                            <Text fw={600}>2. Responsibility & Impact (Max 100)</Text>
                                            <Badge size="lg" color="teal">{form.values.score_responsibility}</Badge>
                                        </Group>
                                        <Text size="sm" c="dimmed" mb="md">
                                            Impact on organizational results and degree of accountability.
                                        </Text>
                                        <Slider
                                            max={100}
                                            step={5}
                                            color="teal"
                                            marks={[
                                                { value: 20, label: 'Task' },
                                                { value: 50, label: 'Team' },
                                                { value: 80, label: 'Strategic' },
                                            ]}
                                            {...form.getInputProps('score_responsibility')}
                                        />
                                    </div>

                                    {/* Factor 3: Complexity */}
                                    <div>
                                        <Group justify="space-between" mb="xs">
                                            <Text fw={600}>3. Problem Solving & Complexity (Max 100)</Text>
                                            <Badge size="lg" color="grape">{form.values.score_complexity}</Badge>
                                        </Group>
                                        <Text size="sm" c="dimmed" mb="md">
                                            Complexity of problems faced and creativity required.
                                        </Text>
                                        <Slider
                                            max={100}
                                            step={5}
                                            color="grape"
                                            marks={[
                                                { value: 20, label: 'Routine' },
                                                { value: 50, label: 'Adaptive' },
                                                { value: 80, label: 'Innovative' },
                                            ]}
                                            {...form.getInputProps('score_complexity')}
                                        />
                                    </div>

                                    <Divider my="md" />

                                    {/* Total Simulation */}
                                    <Center>
                                        <RingProgress
                                            size={180}
                                            thickness={16}
                                            roundCaps
                                            sections={[
                                                { value: (form.values.score_expertise / 300) * 100, color: 'blue', tooltip: 'Expertise' },
                                                { value: (form.values.score_responsibility / 300) * 100, color: 'teal', tooltip: 'Responsibility' },
                                                { value: (form.values.score_complexity / 300) * 100, color: 'grape', tooltip: 'Complexity' },
                                            ]}
                                            label={
                                                <Center>
                                                    <Stack gap={0} align="center">
                                                        <Text fw={700} size="xl">
                                                            {form.values.score_expertise + form.values.score_responsibility + form.values.score_complexity}
                                                        </Text>
                                                        <Text size="xs" c="dimmed">Total / 300</Text>
                                                    </Stack>
                                                </Center>
                                            }
                                        />
                                    </Center>

                                </Stack>
                            </ScrollArea>

                            <Divider my="md" />

                            <Button
                                size="lg"
                                leftSection={<IconCalculator />}
                                onClick={handleCalculate}
                                loading={calculating}
                                fullWidth
                                variant="gradient"
                                gradient={{ from: 'indigo', to: 'cyan' }}
                            >
                                Calculate Grade
                            </Button>

                        </Paper>
                    ) : (
                        <Paper p="xl" withBorder radius="lg" h={700} className="flex flex-col items-center justify-center bg-gray-50">
                            <IconTrophy size={64} className="text-gray-300 mb-4" />
                            <Text size="lg" c="dimmed" fw={500}>Select a job position to start evaluation</Text>
                        </Paper>
                    )}
                </Grid.Col>
            </Grid>
        </Container>
    );
}
