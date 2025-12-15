"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Button, Group, Select,
    Checkbox, Paper, Stack, Textarea, Stepper, Divider,
    ThemeIcon, Loader, Badge, ActionIcon
} from "@mantine/core";
import {
    IconWand, IconBriefcase, IconDownload, IconArrowRight, IconCheck, IconBulb, IconRefresh
} from "@tabler/icons-react";
import { notifications } from "@mantine/notifications";
import { api } from "@/lib/api";

export default function JdGeneratorPage() {
    const [activeStep, setActiveStep] = useState(0);
    const [positions, setPositions] = useState<any[]>([]);
    const [tasks, setTasks] = useState<any[]>([]);

    // Selections
    const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
    const [selectedTasks, setSelectedTasks] = useState<string[]>([]);

    // Result
    const [generatedJd, setGeneratedJd] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [posData, taskData] = await Promise.all([
                api.getJobPositions(),
                api.getJobTasks()
            ]);
            setPositions(posData.map((p: any) => ({ value: p.id, label: p.title })));
            setTasks(taskData);
        } catch (e) {
            console.error(e);
        }
    };

    const handleGenerate = async () => {
        if (!selectedPosition || selectedTasks.length === 0) return;

        setLoading(true);
        try {
            const result = await api.generateJobDescription(selectedPosition, selectedTasks);
            setGeneratedJd(result);
            setActiveStep(2);
        } catch (e) {
            notifications.show({ title: 'Error', message: 'Failed to generate JD', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleSave = () => {
        // Mock save for now
        notifications.show({ title: 'Saved', message: 'Job Description saved to database.', color: 'green' });
    };

    return (
        <Container size="md" py="xl">
            <div className="text-center mb-10">
                <ThemeIcon size={64} radius="xl" variant="filled" color="violet" className="mb-4">
                    <IconWand size={32} />
                </ThemeIcon>
                <Title order={1}>AI Job Description Generator</Title>
                <Text c="dimmed">Auto-draft professional JDs using task composition.</Text>
            </div>

            <Stepper active={activeStep} onStepClick={setActiveStep} color="violet">
                <Stepper.Step label="Target" description="Select Position">
                    <Paper p="xl" radius="md" withBorder mt="xl">
                        <Title order={3} mb="md">Choose Target Position</Title>
                        <Select
                            label="Job Position"
                            placeholder="Select a position"
                            data={positions}
                            value={selectedPosition}
                            onChange={setSelectedPosition}
                            size="md"
                            searchable
                        />
                        <Group justify="flex-end" mt="xl">
                            <Button onClick={() => setActiveStep(1)} disabled={!selectedPosition}>Next: Select Tasks</Button>
                        </Group>
                    </Paper>
                </Stepper.Step>

                <Stepper.Step label="Tasks" description="Select Core Tasks">
                    <Paper p="xl" radius="md" withBorder mt="xl">
                        <Title order={3} mb="sm">What does this role do?</Title>
                        <Text c="dimmed" mb="lg">Select the key tasks responsible for this position.</Text>

                        <Stack gap="xs" h={400} className="overflow-y-auto border border-gray-100 rounded-md p-2">
                            {tasks.map((t) => (
                                <Checkbox
                                    key={t.id}
                                    value={t.id}
                                    label={t.task_name}
                                    description={t.action_verb}
                                    checked={selectedTasks.includes(t.id)}
                                    onChange={(event) => {
                                        if (event.currentTarget.checked) setSelectedTasks([...selectedTasks, t.id]);
                                        else setSelectedTasks(selectedTasks.filter((id) => id !== t.id));
                                    }}
                                    p="sm"
                                    className={`rounded-md transition-colors ${selectedTasks.includes(t.id) ? 'bg-violet-50' : 'hover:bg-gray-50'}`}
                                />
                            ))}
                        </Stack>

                        <Group justify="space-between" mt="xl">
                            <Button variant="default" onClick={() => setActiveStep(0)}>Back</Button>
                            <Button color="violet" onClick={handleGenerate} loading={loading} leftSection={<IconWand size={16} />}>
                                Generate Draft
                            </Button>
                        </Group>
                    </Paper>
                </Stepper.Step>

                <Stepper.Step label="Review" description="Polish Draft">
                    {generatedJd && (
                        <Paper p="xl" radius="md" withBorder mt="xl" className="border-t-4 border-t-violet-500">
                            <Group justify="space-between" mb="lg">
                                <div>
                                    <Badge size="lg" color="violet">{generatedJd.grade}</Badge>
                                    <Title order={2}>{generatedJd.title}</Title>
                                </div>
                                <ActionIcon variant="light" onClick={handleGenerate} loading={loading}><IconRefresh size={16} /></ActionIcon>
                            </Group>

                            <Stack gap="md">
                                <div>
                                    <Text fw={700} size="sm" c="dimmed">JOB OVERVIEW</Text>
                                    <Textarea minRows={4} autosize defaultValue={generatedJd.overview} />
                                </div>

                                <div>
                                    <Text fw={700} size="sm" c="dimmed">KEY RESPONSIBILITIES</Text>
                                    <Textarea minRows={6} autosize defaultValue={generatedJd.responsibilities} />
                                </div>

                                <div>
                                    <Text fw={700} size="sm" c="dimmed">QUALIFICATIONS</Text>
                                    <Textarea minRows={3} autosize defaultValue={generatedJd.qualifications} />
                                </div>
                            </Stack>

                            <Group justify="flex-end" mt="xl">
                                <Button variant="default" onClick={() => setActiveStep(1)}>Back</Button>
                                <Button color="green" onClick={handleSave} leftSection={<IconCheck size={16} />}>Finalize & Save</Button>
                            </Group>
                        </Paper>
                    )}
                </Stepper.Step>
            </Stepper>
        </Container>
    );
}
