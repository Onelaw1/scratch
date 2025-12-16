"use client";

import { useEffect, useState } from 'react';
import { Container, Grid, Paper, Title, Text, Button, Tabs, Slider, Stack, Group, ThemeIcon, Badge, Textarea, LoadingOverlay, Divider, Box, ScrollArea } from '@mantine/core';
import { IconClipboardCheck, IconInfoCircle, IconBrain, IconTool, IconUser, IconDeviceFloppy } from '@tabler/icons-react';
import { useParams, useRouter } from 'next/navigation';
import { evaluationApi, EvaluationCriteria } from '@/lib/api';

export default function JobEvaluationPage() {
    const params = useParams();
    const router = useRouter();
    const [activeTab, setActiveTab] = useState<string | null>('context');
    const [criteria, setCriteria] = useState<EvaluationCriteria[]>([]);
    const [scores, setScores] = useState<Record<string, number>>({});
    const [comments, setComments] = useState("");
    const [loading, setLoading] = useState(false); // Assume loaded for demo

    // Mock Data for Demo (Real app would fetch via API)
    const JOB_CONTEXT = {
        title: "Senior Backend Engineer",
        dept: "R&D Platform Team",
        summary: "Responsible for designing and implementing scalable backend services using Python and FastAPI. Mentors junior developers and ensures code quality.",
        tasks: [
            { name: "System Architecture Design", difficulty: "High", freq: "Weekly" },
            { name: "API Development", difficulty: "Medium", freq: "Daily" },
            { name: "Code Review", difficulty: "High", freq: "Daily" },
            { name: "Production Support", difficulty: "High", freq: "Irregular" },
        ],
        requirements: {
            education: "Master's Degree in CS",
            experience: "7+ Years",
            skills: "Python, AWS, System Design"
        }
    };

    useEffect(() => {
        // Mock Criteria Fetch
        const mockCriteria: EvaluationCriteria[] = [
            { id: 'c1', name: 'Professional Knowledge', category: 'Input', weight: 0.3 },
            { id: 'c2', name: 'Problem Solving', category: 'Process', weight: 0.3 },
            { id: 'c3', name: 'Accountability / Impact', category: 'Output', weight: 0.2 },
            { id: 'c4', name: 'Leadership / Interaction', category: 'Relational', weight: 0.2 },
        ];
        setCriteria(mockCriteria);

        // Init scores
        const initialScores: Record<string, number> = {};
        mockCriteria.forEach(c => initialScores[c.id] = 50); // Default 50
        setScores(initialScores);
    }, []);

    const handleScoreChange = (id: string, val: number) => {
        setScores(prev => ({ ...prev, [id]: val }));
    };

    const calculateWeightedScore = () => {
        let total = 0;
        criteria.forEach(c => {
            total += (scores[c.id] || 0) * c.weight;
        });
        return total;
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // Real API call would go here
            // await evaluationApi.submitRating({ ... });
            setTimeout(() => {
                alert("Evaluation Submitted!");
                router.push('/evaluation/dashboard'); // Or back
            }, 1000);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="xl" py="xl" h="90vh">
            <Group justify="space-between" mb="lg">
                <Group>
                    <ThemeIcon size="xl" color="grape" variant="filled" radius="md">
                        <IconClipboardCheck size={28} />
                    </ThemeIcon>
                    <div>
                        <Title order={2}>Job Valuation Session</Title>
                        <Text c="dimmed">Multi-Rater Factor Comparison Method</Text>
                    </div>
                </Group>
                <Group>
                    <Text fw={700} size="xl" c="blue">{calculateWeightedScore().toFixed(1)} Pts</Text>
                    <Button leftSection={<IconDeviceFloppy size={18} />} onClick={handleSubmit} loading={loading}>
                        Submit Assessment
                    </Button>
                </Group>
            </Group>

            <Grid h="100%">
                {/* LEFT PANEL: CONTEXT (Job Info) */}
                <Grid.Col span={5} h="100%">
                    <Paper withBorder h="100%" radius="md" p={0} style={{ display: 'flex', flexDirection: 'column' }}>
                        <Box p="md" bg="gray.0">
                            <Title order={4}>{JOB_CONTEXT.title}</Title>
                            <Text size="sm" c="dimmed">{JOB_CONTEXT.dept}</Text>
                        </Box>
                        <Divider />
                        <ScrollArea style={{ flex: 1 }}>
                            <Box p="md">
                                <Stack gap="lg">
                                    <div>
                                        <Text fw={700} size="sm" mb={4}><IconInfoCircle size={14} style={{ display: 'inline' }} /> Job Summary</Text>
                                        <Text size="sm">{JOB_CONTEXT.summary}</Text>
                                    </div>

                                    <div>
                                        <Text fw={700} size="sm" mb={4}><IconTool size={14} style={{ display: 'inline' }} /> Key Tasks</Text>
                                        <Stack gap="xs">
                                            {JOB_CONTEXT.tasks.map((t, i) => (
                                                <Paper key={i} withBorder p="xs" bg="white">
                                                    <Group justify="space-between">
                                                        <Text size="sm" fw={500}>{t.name}</Text>
                                                        <Badge size="sm" color={t.difficulty === 'High' ? 'red' : 'blue'}>{t.difficulty}</Badge>
                                                    </Group>
                                                </Paper>
                                            ))}
                                        </Stack>
                                    </div>

                                    <div>
                                        <Text fw={700} size="sm" mb={4}><IconBrain size={14} style={{ display: 'inline' }} /> Competency Requirements</Text>
                                        <Paper withBorder p="xs" bg="white">
                                            <Text size="sm"><strong>Edu:</strong> {JOB_CONTEXT.requirements.education}</Text>
                                            <Text size="sm"><strong>Exp:</strong> {JOB_CONTEXT.requirements.experience}</Text>
                                            <Text size="sm"><strong>Skills:</strong> {JOB_CONTEXT.requirements.skills}</Text>
                                        </Paper>
                                    </div>
                                </Stack>
                            </Box>
                        </ScrollArea>
                    </Paper>
                </Grid.Col>

                {/* RIGHT PANEL: EVALUATION FORM */}
                <Grid.Col span={7} h="100%">
                    <Paper withBorder h="100%" radius="md" p="md" style={{ overflowY: 'auto' }}>
                        <Title order={4} mb="md">Assessment Factors</Title>

                        <Stack gap="xl">
                            {criteria.map(c => (
                                <Box key={c.id}>
                                    <Group justify="space-between" mb={8}>
                                        <div>
                                            <Text fw={600}>{c.name}</Text>
                                            <Text size="xs" c="dimmed">{c.category} (Weight: {c.weight})</Text>
                                        </div>
                                        <Badge size="lg" variant="outline" color="blue">{scores[c.id]}</Badge>
                                    </Group>
                                    <Slider
                                        value={scores[c.id]}
                                        onChange={(v) => handleScoreChange(c.id, v)}
                                        min={0} max={100} step={5}
                                        marks={[
                                            { value: 20, label: 'Low' },
                                            { value: 50, label: 'Avg' },
                                            { value: 80, label: 'High' },
                                        ]}
                                        mb="md"
                                    />
                                    <Divider />
                                </Box>
                            ))}

                            <Textarea
                                label="Rationale / Comments"
                                placeholder="Explain your scoring logic..."
                                minRows={3}
                                value={comments}
                                onChange={(e) => setComments(e.target.value)}
                            />
                        </Stack>
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
