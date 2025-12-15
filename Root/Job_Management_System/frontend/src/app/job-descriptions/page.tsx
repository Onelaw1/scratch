"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, Stack, Badge,
    Textarea, Button, Divider, Loader, ActionIcon, ScrollArea
} from "@mantine/core";
import { useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { IconPrinter, IconDeviceFloppy, IconBriefcase } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function JobDescriptionPage() {
    const [positions, setPositions] = useState<any[]>([]);
    const [selectedPositionId, setSelectedPositionId] = useState<string | null>(null);
    const [jdData, setJdData] = useState<any>(null);
    const [loadingPos, setLoadingPos] = useState(true);
    const [loadingJd, setLoadingJd] = useState(false);
    const [saving, setSaving] = useState(false);

    const form = useForm({
        initialValues: {
            summary: '',
            qualification_requirements: '',
            kpi_indicators: '',
        },
    });

    useEffect(() => {
        loadPositions();
    }, []);

    useEffect(() => {
        if (selectedPositionId) {
            loadJd(selectedPositionId);
        } else {
            setJdData(null);
        }
    }, [selectedPositionId]);

    const loadPositions = async () => {
        try {
            const data = await api.getJobPositions();
            setPositions(data);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load positions', color: 'red' });
        } finally {
            setLoadingPos(false);
        }
    };

    const loadJd = async (id: string) => {
        setLoadingJd(true);
        try {
            const data = await api.getJobDescription(id);
            setJdData(data);
            form.setValues({
                summary: data.description.summary || '',
                qualification_requirements: data.description.qualification_requirements || '',
                kpi_indicators: data.description.kpi_indicators || '',
            });
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load JD', color: 'red' });
        } finally {
            setLoadingJd(false);
        }
    };

    const handleSave = async () => {
        if (!selectedPositionId) return;
        setSaving(true);
        try {
            await api.saveJobDescription(selectedPositionId, form.values);
            notifications.show({ title: 'Saved', message: 'Job Description updated', color: 'green' });
            // Reload to ensure sync
            loadJd(selectedPositionId);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to save', color: 'red' });
        } finally {
            setSaving(false);
        }
    };

    const handlePrint = () => {
        window.print();
    };

    return (
        <Container size="xl" py="xl">
            <style jsx global>{`
                @media print {
                    body * { visibility: hidden; }
                    .print-area, .print-area * { visibility: visible; }
                    .print-area { position: absolute; left: 0; top: 0; width: 100%; }
                    .no-print { display: none !important; }
                    .mantine-AppShell-header, .mantine-AppShell-navbar { display: none !important; }
                }
            `}</style>

            <Group justify="space-between" mb="xl" className="no-print">
                <div>
                    <Title order={2}>Live Job Description</Title>
                    <Text c="dimmed">Auto-generated from Job Analysis & Evaluation data.</Text>
                </div>
                <Button leftSection={<IconPrinter size={18} />} variant="outline" onClick={handlePrint} disabled={!jdData}>
                    Print JD
                </Button>
            </Group>

            <Grid>
                {/* Sidebar: Select Position */}
                <Grid.Col span={{ base: 12, md: 3 }} className="no-print">
                    <Paper withBorder p="md" radius="md" h={800} style={{ display: 'flex', flexDirection: 'column' }}>
                        <Text fw={700} c="dimmed" mb="md" tt="uppercase">Job Lists</Text>
                        <ScrollArea style={{ flex: 1 }}>
                            <Stack gap="xs">
                                {loadingPos ? <Loader size="sm" /> : positions.map((pos) => (
                                    <Paper
                                        key={pos.id}
                                        p="sm"
                                        withBorder={selectedPositionId === pos.id}
                                        onClick={() => setSelectedPositionId(pos.id)}
                                        style={{
                                            cursor: 'pointer',
                                            backgroundColor: selectedPositionId === pos.id ? 'var(--mantine-primary-color-light)' : 'transparent'
                                        }}
                                        className="hover:bg-gray-50 transition-colors"
                                    >
                                        <Text size="sm" fw={600}>{pos.title}</Text>
                                        <Text size="xs" c="dimmed">{pos.series?.name}</Text>
                                    </Paper>
                                ))}
                            </Stack>
                        </ScrollArea>
                    </Paper>
                </Grid.Col>

                {/* Main Content: JD View */}
                <Grid.Col span={{ base: 12, md: 9 }}>
                    {loadingJd ? (
                        <Group justify="center" h={400}><Loader /></Group>
                    ) : jdData ? (
                        <Paper p="xl" withBorder radius="lg" shadow="sm" className="print-area bg-white">
                            {/* Header */}
                            <div className="border-b-2 border-gray-800 pb-4 mb-6">
                                <Group justify="space-between" align="end">
                                    <div>
                                        <Text size="sm" tt="uppercase" c="dimmed" fw={700}>Job Description</Text>
                                        <Title order={1}>{jdData.position.title}</Title>
                                        <Group gap="xs" mt="xs">
                                            <Badge size="lg" radius="sm" variant="filled" color="dark">{jdData.position.group}</Badge>
                                            <Badge size="lg" radius="sm" variant="outline">{jdData.position.series}</Badge>
                                            {jdData.position.grade && <Badge size="lg" radius="sm" color="indigo">{jdData.position.grade}</Badge>}
                                        </Group>
                                    </div>
                                    <div className="text-right">
                                        <Text size="xs" c="dimmed">Last Updated</Text>
                                        <Text fw={500}>{jdData.description.updated_at}</Text>
                                    </div>
                                </Group>
                            </div>

                            <Stack gap="xl">
                                {/* Section 1: Summary */}
                                <div>
                                    <Text fw={700} size="lg" mb="xs" className="border-l-4 border-indigo-500 pl-3">Job Summary</Text>
                                    <Textarea
                                        minRows={3}
                                        autosize
                                        placeholder="Enter job summary..."
                                        variant="unstyled"
                                        className="bg-gray-50 p-2 rounded-md print:bg-transparent print:p-0"
                                        {...form.getInputProps('summary')}
                                    />
                                </div>

                                {/* Section 2: Key Responsibilities (Auto) */}
                                <div>
                                    <Text fw={700} size="lg" mb="md" className="border-l-4 border-indigo-500 pl-3">Key Responsibilities & Tasks</Text>
                                    <Stack gap="sm">
                                        {jdData.responsibilities.map((task: any, idx: number) => (
                                            <div key={task.id} className="flex gap-4 p-2 border-b border-gray-100 last:border-0">
                                                <div className="w-12 pt-1">
                                                    <Badge circle size="lg" variant="light" color="gray">{idx + 1}</Badge>
                                                </div>
                                                <div className="flex-1">
                                                    <Text fw={600}>{task.task_name}</Text>
                                                    <Text size="sm" c="dimmed">{task.action_verb} {task.task_object}</Text>
                                                </div>
                                                <div className="w-24 text-right">
                                                    {task.importance > 0 && (
                                                        <Badge variant="dot" color={task.importance > 20 ? 'red' : 'blue'}>
                                                            {task.importance}% FTE
                                                        </Badge>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                        {jdData.responsibilities.length === 0 && <Text c="dimmed" fs="italic">No tasks assigned yet.</Text>}
                                    </Stack>
                                </div>

                                {/* Section 3: Requirements */}
                                <div>
                                    <Text fw={700} size="lg" mb="xs" className="border-l-4 border-indigo-500 pl-3">Qualification Requirements</Text>
                                    <Textarea
                                        minRows={4}
                                        autosize
                                        placeholder="e.g. Include education, experience, skills..."
                                        variant="unstyled"
                                        className="bg-gray-50 p-2 rounded-md print:bg-transparent print:p-0"
                                        {...form.getInputProps('qualification_requirements')}
                                    />
                                </div>

                                {/* Section 4: KPIs */}
                                <div>
                                    <Text fw={700} size="lg" mb="xs" className="border-l-4 border-indigo-500 pl-3">Key Performance Indicators (KPI)</Text>
                                    <Textarea
                                        minRows={3}
                                        autosize
                                        placeholder="Enter main KPI metrics..."
                                        variant="unstyled"
                                        className="bg-gray-50 p-2 rounded-md print:bg-transparent print:p-0"
                                        {...form.getInputProps('kpi_indicators')}
                                    />
                                </div>
                            </Stack>

                            <Divider my="xl" className="no-print" />

                            <Group justify="end" className="no-print">
                                <Button
                                    size="lg"
                                    leftSection={<IconDeviceFloppy />}
                                    onClick={handleSave}
                                    loading={saving}
                                >
                                    Save Changes
                                </Button>
                            </Group>

                        </Paper>
                    ) : (
                        <div className="flex h-full items-center justify-center text-gray-400">
                            <Stack align="center" gap="xs">
                                <IconBriefcase size={64} stroke={1} />
                                <Text size="lg">Select a job position to view description</Text>
                            </Stack>
                        </div>
                    )}
                </Grid.Col>
            </Grid>
        </Container>
    );
}
