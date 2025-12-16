"use client";

import { useState, useEffect } from 'react';
import { Title, Card, Tabs, Text, Group, Button, TextInput, NumberInput, Stack, Box, Select, MultiSelect, LoadingOverlay, Container, Table, ActionIcon } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { api, EvaluationCriteria } from '@/lib/api';
import { IconSettings, IconUsers, IconTestPipe, IconPlus, IconEdit, IconChartDots } from '@tabler/icons-react';
import { RelationshipMap } from './RelationshipMap';

export default function EvaluationConfigPage() {
    const [activeTab, setActiveTab] = useState<string | null>('criteria');
    const [loading, setLoading] = useState(false);
    const [sessions, setSessions] = useState<any[]>([]);
    const [currentSessionId, setCurrentSessionId] = useState<string>('');
    const [criteria, setCriteria] = useState<any[]>([]);

    // Assignment State
    const [users, setUsers] = useState<any[]>([]);
    const [jobs, setJobs] = useState<any[]>([]);
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [selectedTargetJobs, setSelectedTargetJobs] = useState<string[]>([]);
    const [raterRole, setRaterRole] = useState('PEER');

    useEffect(() => {
        loadInitialData();
    }, []);

    const loadInitialData = async () => {
        try {
            const insts = await api.getInstitutions();
            const instId = insts[0]?.id || 'inst-001';
            const [sessList, userList, jobList] = await Promise.all([
                api.getSessions(instId),
                api.getUsers(),
                api.getJobPositions()
            ]);

            setSessions(sessList);
            if (sessList.length > 0) {
                setCurrentSessionId(sessList[0].id);
                loadCriteria(sessList[0].id);
            }

            setUsers(userList);
            setJobs(jobList);
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Error', message: 'Failed to load data', color: 'red' });
        }
    };

    const loadCriteria = async (sessId: string) => {
        setLoading(true);
        try {
            const res = await api.getSessionCriteria(sessId);
            setCriteria(res);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateCriteria = async (id: string, field: string, value: any) => {
        // Optimistic update
        setCriteria(prev => prev.map(c => c.id === id ? { ...c, [field]: value } : c));

        try {
            await api.updateCriteria(id, { [field]: value });
            notifications.show({ title: 'Updated', message: 'Criteria updated successfully', color: 'green' });
        } catch (e) {
            notifications.show({ title: 'Error', message: 'Failed to save criteria', color: 'red' });
        }
    };

    const handleAssign = async () => {
        if (!selectedUser || !currentSessionId || selectedTargetJobs.length === 0) return;

        const payload = selectedTargetJobs.map(jobId => ({
            session_id: currentSessionId,
            rater_user_id: selectedUser,
            target_job_position_id: jobId,
            rater_role: raterRole
        }));

        try {
            setLoading(true);
            await api.createAssignments(payload);
            notifications.show({ title: 'Assigned', message: `${payload.length} assignments created.`, color: 'teal' });
            setSelectedTargetJobs([]);
        } catch (e) {
            notifications.show({ title: 'Error', message: 'Assignment failed', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Stack gap="lg" p="md">
            <Group justify="space-between">
                <div>
                    <Title order={2}>Evaluation Configuration</Title>
                    <Text c="dimmed">Manage Criteria, Weights, and Rater Assignments</Text>
                </div>
                <Select
                    label="Current Session"
                    data={sessions.map(s => ({ value: s.id, label: s.name }))}
                    value={currentSessionId}
                    onChange={(v) => {
                        setCurrentSessionId(v || '');
                        if (v) loadCriteria(v);
                    }}
                />
            </Group>

            <Tabs value={activeTab} onChange={setActiveTab} variant="outline" radius="md">
                <Tabs.List>
                    <Tabs.Tab value="criteria" leftSection={<IconSettings size={14} />}>
                        Criteria & Weights
                    </Tabs.Tab>
                    <Tabs.Tab value="assignments" leftSection={<IconUsers size={14} />}>
                        Evaluator Assignments
                    </Tabs.Tab>
                    <Tabs.Tab value="relationships" leftSection={<IconChartDots size={14} />}>
                        Relationship Map
                    </Tabs.Tab>
                    <Tabs.Tab value="simulation" leftSection={<IconTestPipe size={14} />}>
                        Simulation
                    </Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="criteria" p="md">
                    <Stack>
                        {criteria.map(c => (
                            <Card key={c.id} withBorder>
                                <Group align="flex-end">
                                    <TextInput
                                        label="Criteria Name"
                                        value={c.name}
                                        onChange={(e) => handleUpdateCriteria(c.id, 'name', e.target.value)}
                                        style={{ flex: 1 }}
                                    />
                                    <NumberInput
                                        label="Weight (Ratio)"
                                        value={c.weight}
                                        onChange={(v) => handleUpdateCriteria(c.id, 'weight', Number(v))}
                                        step={0.1}
                                        min={0}
                                        max={1}
                                        style={{ width: 120 }}
                                    />
                                    <TextInput
                                        label="Description"
                                        value={c.description || ''}
                                        onChange={(e) => handleUpdateCriteria(c.id, 'description', e.target.value)}
                                        style={{ flex: 2 }}
                                    />
                                </Group>
                            </Card>
                        ))}
                        {criteria.length === 0 && <Text c="dimmed">No criteria found for this session.</Text>}
                    </Stack>
                </Tabs.Panel>

                <Tabs.Panel value="assignments" p="md">
                    <Card withBorder>
                        <Title order={4} mb="md">Assign Evaluators</Title>
                        <Stack>
                            <Group>
                                <Select
                                    label="Select User (Rater)"
                                    data={users.map(u => ({ value: u.id, label: u.name }))}
                                    value={selectedUser}
                                    onChange={setSelectedUser}
                                    searchable
                                    style={{ flex: 1 }}
                                />
                                <Select
                                    label="Rater Role"
                                    data={['SELF', 'PEER', 'SUPERVISOR_1', 'SUPERVISOR_2', 'EXTERNAL']}
                                    value={raterRole}
                                    onChange={(v) => setRaterRole(v || 'PEER')}
                                    style={{ width: 200 }}
                                />
                            </Group>

                            <MultiSelect
                                label="Target Jobs to Evaluate"
                                data={jobs.map(j => ({ value: j.id, label: j.title }))}
                                value={selectedTargetJobs}
                                onChange={setSelectedTargetJobs}
                                searchable
                                clearable
                                style={{ flex: 1 }}
                            />

                            <Button onClick={handleAssign} disabled={!selectedUser || selectedTargetJobs.length === 0}>
                                Assign Selected Jobs
                            </Button>
                        </Stack>
                    </Card>
                </Tabs.Panel>

                <Tabs.Panel value="relationships" p="md">
                    {currentSessionId ? (
                        <RelationshipMap sessionId={currentSessionId} />
                    ) : (
                        <Text c="dimmed">Please select a session first.</Text>
                    )}
                </Tabs.Panel>

                <Tabs.Panel value="simulation" p="md">
                    <Text>Simulation features coming soon.</Text>
                </Tabs.Panel>
            </Tabs>
        </Stack>
    );
}
