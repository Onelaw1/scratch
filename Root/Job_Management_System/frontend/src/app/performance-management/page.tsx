"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, Stack, Badge,
    Button, Loader, Select, Modal, TextInput, NumberInput, RingProgress, Divider,
    Progress, Slider, Card, ActionIcon
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { IconCheck, IconPlus, IconBulb, IconTarget } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function PerformanceManagementPage() {
    // State
    const [users, setUsers] = useState<any[]>([]);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [review, setReview] = useState<any>(null);
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [loadingUsers, setLoadingUsers] = useState(true);
    const [loadingReview, setLoadingReview] = useState(false);

    // Modal State
    const [goalModalOpened, { open: openGoalModal, close: closeGoalModal }] = useDisclosure(false);
    const [suggestionModalOpened, { open: openSuggestionModal, close: closeSuggestionModal }] = useDisclosure(false);

    // Form State
    const [newGoal, setNewGoal] = useState({ category: 'MBO', goal_text: '', weight: 0, target: '' });

    useEffect(() => {
        loadUsers();
    }, []);

    useEffect(() => {
        if (selectedUser) {
            loadReview(selectedUser);
        } else {
            setReview(null);
        }
    }, [selectedUser]);

    const loadUsers = async () => {
        try {
            // For MVP, just treating all users as "My Team" or similar
            // Ideally fetch from /users
            // Using a dummy list or fetching actual users if API exists
            // Let's assume we can fetch users who have positions
            // Reusing getEvaluationPositions to get positions which have users? No, specific user endpoint needed.
            // For now, let's look for a basic user list or just mock one active user for demo
            // Trying to use a known user ID or fetch first available
            const res = await api.getEvaluationPositions(); // Get positions, they have user_id
            const usersWithPos = res.filter((p: any) => p.user_id).map((p: any) => ({
                value: p.user_id,
                label: `${p.user?.name || 'Unknown'} (${p.title})`,
                positionId: p.id
            }));
            setUsers(usersWithPos);
            if (usersWithPos.length > 0) setSelectedUser(usersWithPos[0].value);
        } catch (error) {
            console.error(error);
        } finally {
            setLoadingUsers(false);
        }
    };

    const loadReview = async (userId: string) => {
        setLoadingReview(true);
        try {
            // Try to get 2025 review
            let data = await api.getReview(userId, 2025);
            if (!data) {
                // If not exists, create one
                data = await api.createReview(userId, 2025);
            }
            setReview(data);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load review', color: 'red' });
        } finally {
            setLoadingReview(false);
        }
    };

    const loadSuggestions = async () => {
        if (!selectedUser) return;
        const userObj = users.find(u => u.value === selectedUser);
        if (!userObj) return;

        try {
            const data = await api.getGoalSuggestions(userObj.positionId);
            setSuggestions(data);
            openSuggestionModal();
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load suggestions', color: 'red' });
        }
    };

    const handleAddGoal = async () => {
        if (!review) return;
        try {
            await api.addGoal(review.id, newGoal);
            notifications.show({ title: 'Success', message: 'Goal added', color: 'green' });
            closeGoalModal();
            loadReview(selectedUser!); // Refresh
            setNewGoal({ category: 'MBO', goal_text: '', weight: 0, target: '' }); // Reset
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to add goal', color: 'red' });
        }
    };

    const handleImportSuggestion = async (suggestion: any) => {
        // Pre-fill goal form with suggestion
        setNewGoal({
            category: suggestion.category,
            goal_text: suggestion.goal_text,
            weight: 20, // Default
            target: ''
        });
        closeSuggestionModal();
        openGoalModal();
    };

    const handleCalculate = async () => {
        if (!review) return;
        try {
            await api.calculateReview(review.id);
            loadReview(selectedUser!);
            notifications.show({ title: 'Calculated', message: 'Score updated', color: 'blue' });
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Calculation failed', color: 'red' });
        }
    };

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2}>Performance Management</Title>
                    <Text c="dimmed">Goal Setting (MBO) & Performance Appraisal</Text>
                </div>
                <Select
                    placeholder="Select Employee"
                    data={users}
                    value={selectedUser}
                    onChange={setSelectedUser}
                    searchable
                    className="w-64"
                />
            </Group>

            {loadingReview ? (
                <Loader />
            ) : review ? (
                <Grid>
                    {/* Left: Goals */}
                    <Grid.Col span={{ base: 12, md: 8 }}>
                        <Paper p="md" withBorder radius="md">
                            <Group justify="space-between" mb="md">
                                <Title order={4}>2025 Performance Goals</Title>
                                <Group>
                                    <Button variant="light" leftSection={<IconBulb size={16} />} onClick={loadSuggestions} color="grape">
                                        AI Suggestions
                                    </Button>
                                    <Button leftSection={<IconPlus size={16} />} onClick={openGoalModal}>
                                        Add Goal
                                    </Button>
                                </Group>
                            </Group>

                            <EmptyState visible={review.goals.length === 0} />

                            {review.goals.length > 0 && (
                                <Stack gap="xs">
                                    {/* Smart Weight Budget Bar */}
                                    <Paper p="sm" bg="blue.0" className="border border-blue-200">
                                        <Group justify="space-between" mb={4}>
                                            <Group gap={4}>
                                                <IconTarget size={16} className="text-blue-600" />
                                                <Text fw={700} size="sm" c="blue.9">Total Weight Allocation</Text>
                                            </Group>
                                            <Text fw={700} size="sm" c={
                                                review.goals.reduce((acc: any, g: any) => acc + g.weight, 0) === 100 ? 'teal' :
                                                    review.goals.reduce((acc: any, g: any) => acc + g.weight, 0) > 100 ? 'red' : 'orange'
                                            }>
                                                {review.goals.reduce((acc: any, g: any) => acc + g.weight, 0)}% / 100%
                                            </Text>
                                        </Group>
                                        <Progress
                                            value={review.goals.reduce((acc: any, g: any) => acc + g.weight, 0)}
                                            size="xl"
                                            radius="xl"
                                            color={
                                                review.goals.reduce((acc: any, g: any) => acc + g.weight, 0) > 100 ? 'red' : 'blue'
                                            }
                                            striped animated
                                        />
                                    </Paper>

                                    {/* Interactive Goal List */}
                                    {review.goals.map((goal: any, idx: number) => (
                                        <Paper key={goal.id} p="sm" withBorder bg="white">
                                            <Group justify="space-between" mb="xs" align="start">
                                                <div style={{ flex: 1 }}>
                                                    <Group gap="xs" mb={4}>
                                                        <Badge variant="dot" size="sm">{goal.category}</Badge>
                                                        <Text fw={600} size="sm">{goal.goal_text}</Text>
                                                    </Group>
                                                    {goal.target && <Text size="xs" c="dimmed">Target: {goal.target}</Text>}
                                                </div>
                                                <ActionIcon color="red" variant="subtle" size="sm" onClick={async () => {
                                                    // Delete logic here (assuming API exists or just hide for demo)
                                                    // Ideally api.deleteGoal(goal.id)
                                                    if (confirm('Delete goal?')) {
                                                        await api.deleteGoal(goal.id); // Assuming this is added or handle via review update
                                                        loadReview(selectedUser!);
                                                    }
                                                }}>
                                                    <IconPlus size={16} style={{ transform: 'rotate(45deg)' }} />
                                                </ActionIcon>
                                            </Group>

                                            {/* Weight Slider */}
                                            <Card bg="gray.0" p="xs" radius="md">
                                                <Stack gap={2}>
                                                    <Group justify="space-between">
                                                        <Text size="xs" fw={600} c="dimmed">Weight</Text>
                                                        <Badge variant="filled" color="blue" size="sm">{goal.weight}%</Badge>
                                                    </Group>
                                                    <Slider
                                                        value={goal.weight}
                                                        onChangeEnd={async (val) => {
                                                            // Optimistic update locally first? Or direct API call
                                                            // Direct API call for now to keep sync
                                                            try {
                                                                await api.updateGoal(goal.id, { weight: val });
                                                                loadReview(selectedUser!); // Refresh full state
                                                            } catch (e) { console.error(e); }
                                                        }}
                                                        // Optimistic UX: Bind to local state change if we lifted state up
                                                        // For now simplified: onChangeEnd triggers save
                                                        min={0} max={100} step={5}
                                                        color="blue" size="sm"
                                                        marks={[
                                                            { value: 10, label: '10' },
                                                            { value: 20, label: '20' },
                                                            { value: 30, label: '30' },
                                                            { value: 50, label: '50' },
                                                        ]}
                                                    />
                                                </Stack>
                                            </Card>
                                        </Paper>
                                    ))}
                                </Stack>
                            )}
                        </Paper>
                    </Grid.Col>

                    {/* Right: Score Card */}
                    <Grid.Col span={{ base: 12, md: 4 }}>
                        <Paper p="md" withBorder radius="md" h="100%">
                            <Title order={4} mb="lg">Appraisal Summary</Title>

                            <Stack align="center" mb="xl">
                                <RingProgress
                                    size={140}
                                    thickness={12}
                                    roundCaps
                                    sections={[{ value: review.total_score, color: getGradeColor(review.grade) }]}
                                    label={
                                        <Text ta="center" size="xl" fw={700}>
                                            {review.grade || '-'}
                                        </Text>
                                    }
                                />
                                <Text size="sm" c="dimmed">Total Score: {review.total_score?.toFixed(1)}</Text>
                            </Stack>

                            <Divider my="md" />

                            <Button fullWidth onClick={handleCalculate} variant="light" mb="md">
                                Calculate Score
                            </Button>

                            <Text size="xs" c="dimmed" ta="center">
                                Status: {review.status}
                            </Text>
                        </Paper>
                    </Grid.Col>
                </Grid>
            ) : (
                <Text c="dimmed">Select a user to view performance review.</Text>
            )}

            {/* Modal: New Goal */}
            <Modal opened={goalModalOpened} onClose={closeGoalModal} title="Add Performance Goal">
                <Stack>
                    <Select
                        label="Category"
                        data={['MBO', 'BSC_FINANCIAL', 'COMPETENCY', 'JD_KPI', 'JOB_TASK']}
                        value={newGoal.category}
                        onChange={(v) => setNewGoal({ ...newGoal, category: v || 'MBO' })}
                    />
                    <TextInput
                        label="Goal Description"
                        required
                        value={newGoal.goal_text}
                        onChange={(e) => setNewGoal({ ...newGoal, goal_text: e.target.value })}
                    />
                    <TextInput
                        label="Target (Optional)"
                        placeholder="e.g. Achieve 10% growth"
                        value={newGoal.target}
                        onChange={(e) => setNewGoal({ ...newGoal, target: e.target.value })}
                    />
                    <NumberInput
                        label="Weight (%)"
                        min={0} max={100}
                        value={newGoal.weight}
                        onChange={(v) => setNewGoal({ ...newGoal, weight: Number(v) })}
                    />
                    <Button onClick={handleAddGoal}>Save Goal</Button>
                </Stack>
            </Modal>

            {/* Modal: Suggestions */}
            <Modal opened={suggestionModalOpened} onClose={closeSuggestionModal} title="Suggested Goals from Job Description">
                <Stack>
                    {suggestions.length === 0 && <Text c="dimmed">No suggestions found for this job position.</Text>}
                    {suggestions.map((s, idx) => (
                        <Paper key={idx} p="sm" withBorder className="hover:bg-gray-50 cursor-pointer" onClick={() => handleImportSuggestion(s)}>
                            <Group justify="space-between">
                                <div>
                                    <Badge size="xs" mb={4}>{s.category}</Badge>
                                    <Text size="sm">{s.goal_text}</Text>
                                </div>
                                <IconPlus size={16} color="gray" />
                            </Group>
                        </Paper>
                    ))}
                </Stack>
            </Modal>
        </Container>
    );
}

function EmptyState({ visible }: { visible: boolean }) {
    if (!visible) return null;
    return (
        <Stack align="center" gap="xs" py="xl" c="dimmed">
            <IconTarget size={40} stroke={1.5} />
            <Text size="sm">No goals set yet.</Text>
        </Stack>
    );
}

function getGradeColor(grade: string) {
    switch (grade) {
        case 'S': return 'teal';
        case 'A': return 'blue';
        case 'B': return 'green';
        case 'C': return 'yellow';
        case 'D': return 'red';
        default: return 'gray';
    }
}
