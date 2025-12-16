"use client";

import { useState, useEffect, useMemo } from 'react';
import { Title, Card, Table, NumberInput, Group, Button, Badge, Text, ScrollArea, LoadingOverlay, Select, Alert, Stack, Slider, Modal } from '@mantine/core';
import { IconCheck, IconAlertCircle, IconDeviceFloppy, IconTestPipe } from '@tabler/icons-react';
import { api } from '@/lib/api';
import { notifications } from '@mantine/notifications';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function MatrixEvaluationPage() {
    const [loading, setLoading] = useState(true);
    const [jobs, setJobs] = useState<any[]>([]);
    const [criteria, setCriteria] = useState<any[]>([]);
    const [sessionId, setSessionId] = useState<string>('');
    const [sessions, setSessions] = useState<any[]>([]);

    // Ratings: { jobId: { criteriaId: score } }
    const [ratings, setRatings] = useState<Record<string, Record<string, number>>>({});

    // TARGET AVERAGE (Hardcoded for "Anti-Leniency" Demo)
    const TARGET_AVG = 5.0;
    const TOLERANCE = 0.5; // 4.5 ~ 5.5 is OK

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const institutions = await api.getInstitutions();
            const instId = institutions[0]?.id || 'inst-001';

            const [posData, sessionList] = await Promise.all([
                api.getJobPositions(),
                api.getSessions(instId)
            ]);

            if (sessionList && sessionList.length > 0) {
                setSessionId(sessionList[0].id);
                setSessions(sessionList);
                const critData = await api.getSessionCriteria(sessionList[0].id);
                setCriteria(critData);
            } else {
                setSessions([{ id: 'demo-session', name: '2024년 정기 평가' }]);
                setSessionId('demo-session');
                setCriteria([
                    { id: 'c1', name: '전문 지식', weight: 0.2 },
                    { id: 'c2', name: '문제 해결', weight: 0.3 },
                    { id: 'c3', name: '영향력', weight: 0.3 },
                    { id: 'c4', name: '의사소통', weight: 0.2 },
                ]);
            }

            if (posData && Array.isArray(posData)) {
                setJobs(posData);
                const initialRatings: any = {};
                posData.forEach((j: any) => {
                    initialRatings[j.id] = {};
                });
                setRatings(initialRatings);
            }

        } catch (error) {
            console.error(error);
            notifications.show({ title: '오류', message: '평가 데이터를 불러오지 못했습니다.', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleRatingChange = (jobId: string, criteriaId: string, val: number) => {
        setRatings(prev => ({
            ...prev,
            [jobId]: {
                ...prev[jobId],
                [criteriaId]: val
            }
        }));
    };

    // Calculate Column Averages
    const columnStats = useMemo(() => {
        const stats: Record<string, { sum: number, avg: number, valid: boolean }> = {};
        criteria.forEach(c => {
            let sum = 0;
            let count = 0;
            jobs.forEach(j => {
                const score = ratings[j.id]?.[c.id] || 0;
                if (score > 0) {
                    sum += score;
                    count++;
                }
            });
            const avg = count > 0 ? sum / count : 0;
            const valid = Math.abs(avg - TARGET_AVG) <= TOLERANCE || count === 0;
            stats[c.id] = { sum, avg, valid };
        });
        return stats;
    }, [ratings, jobs, criteria]);

    const canSubmit = useMemo(() => {
        if (jobs.length === 0) return false;
        const allColsValid = criteria.every(c => columnStats[c.id]?.valid);
        return allColsValid;
    }, [columnStats, criteria, jobs]);


    const handleSubmit = async () => {
        if (!canSubmit) {
            notifications.show({ title: '제출 불가', message: '항목별 평균 점수 기준을 맞춰주세요.', color: 'red' });
            return;
        }

        const payload = {
            session_id: sessionId,
            rater_type: 'SUPERVISOR_1',
            ratings: jobs.map(j => ({
                job_position_id: j.id,
                factor_scores: ratings[j.id] || {}
            })).filter(r => Object.keys(r.factor_scores).length > 0)
        };

        try {
            await api.submitMatrixEvaluation(sessionId, payload);
            notifications.show({ title: '완료', message: '평가가 성공적으로 제출되었습니다!', color: 'green' });
        } catch (e) {
            notifications.show({ title: '오류', message: '제출에 실패했습니다.', color: 'red' });
        }
    };

    const getRowTotal = (jobId: string) => {
        const r = ratings[jobId];
        if (!r) return 0;
        return Object.values(r).reduce((a, b) => a + b, 0);
    };

    // --- Report State ---
    const [reportOpen, setReportOpen] = useState(false);
    const [analysisData, setAnalysisData] = useState<any>(null);

    const handleAnalyze = async () => {
        const payload = {
            session_id: sessionId,
            rater_type: 'SUPERVISOR_1', // Should be dynamic based on User login
            rater_user_id: 'user-001', // Mock User ID
            ratings: jobs.map(j => ({
                job_position_id: j.id,
                factor_scores: ratings[j.id] || {}
            })).filter(r => Object.keys(r.factor_scores).length > 0)
        };

        try {
            const res = await api.submitMatrixEvaluation(sessionId, payload, true); // dryRun=true
            if (res.analysis) {
                setAnalysisData(res.analysis);
                setReportOpen(true);
            }
        } catch (e) {
            notifications.show({ title: 'Error', message: 'Failed to generate report', color: 'red' });
        }
    };

    const handleConfirmSubmit = async () => {
        setReportOpen(false);
        await handleSubmit();
    };

    return (
        <Stack gap="lg" p="md">
            <Group justify="space-between">
                <div>
                    <Title order={2}>Job Evaluation Matrix</Title>
                    <Text c="dimmed">Relative Evaluation (Anti-Leniency)</Text>
                </div>
                <Group>
                    <Select
                        data={sessions.map(s => ({ value: s.id, label: s.name }))}
                        value={sessionId}
                        onChange={(v) => setSessionId(v || '')}
                        disabled
                    />
                    <Button
                        variant="light"
                        color="blue"
                        leftSection={<IconTestPipe size={18} />}
                        onClick={handleAnalyze}
                        disabled={Object.keys(ratings).length === 0}
                    >
                        Analyze Impact
                    </Button>
                    <Button
                        leftSection={<IconDeviceFloppy size={18} />}
                        onClick={handleSubmit}
                        disabled={!canSubmit}
                        color={canSubmit ? 'teal' : 'gray'}
                    >
                        Submit Evaluation
                    </Button>
                </Group>
            </Group>

            <Alert icon={<IconAlertCircle size={16} />} title="Evaluation Guide" color="blue">
                Evaluate each job per criteria.
                <Text span fw={700}> Target Avg: {TARGET_AVG.toFixed(1)} (±{TOLERANCE}).</Text>
            </Alert>

            <Card withBorder radius="md">
                <ScrollArea>
                    <Table striped highlightOnHover withTableBorder>
                        <Table.Thead bg="gray.1">
                            <Table.Tr>
                                <Table.Th style={{ minWidth: 200 }}>Job Position</Table.Th>
                                {criteria.map(c => (
                                    <Table.Th key={c.id} style={{ textAlign: 'center', minWidth: 160 }}>
                                        <Stack gap={0} align="center">
                                            <Text size="sm">{c.name}</Text>
                                            <Text size="xs" fw={400} c="dimmed">(Max 10 / W: {c.weight})</Text>
                                        </Stack>
                                    </Table.Th>
                                ))}
                                <Table.Th style={{ textAlign: 'center', minWidth: 80 }}>Total</Table.Th>
                            </Table.Tr>
                        </Table.Thead>
                        <Table.Tbody>
                            {jobs.map(job => (
                                <Table.Tr key={job.id}>
                                    <Table.Td>
                                        <Text fw={500}>{job.title}</Text>
                                        <Text size="xs" c="dimmed">{job.grade || 'No Grade'}</Text>
                                    </Table.Td>
                                    {criteria.map(c => (
                                        <Table.Td key={c.id}>
                                            <Stack gap={2} align="center">
                                                <Text fw={700} size="sm" c="blue">
                                                    {(ratings[job.id]?.[c.id] || 0).toFixed(1)}
                                                </Text>
                                                <Slider
                                                    w="100%"
                                                    min={0} max={10} step={0.1}
                                                    label={null}
                                                    value={ratings[job.id]?.[c.id] || 0}
                                                    onChange={(v) => handleRatingChange(job.id, c.id, Number(v))}
                                                    color="blue"
                                                    size="sm"
                                                    styles={{ thumb: { borderWidth: 1 } }}
                                                />
                                            </Stack>
                                        </Table.Td>
                                    ))}
                                    <Table.Td style={{ textAlign: 'center' }}>
                                        <Text fw={700}>{getRowTotal(job.id).toFixed(1)}</Text>
                                    </Table.Td>
                                </Table.Tr>
                            ))}
                        </Table.Tbody>
                        <Table.Tfoot bg="gray.0" style={{ position: 'sticky', bottom: 0, zIndex: 1 }}>
                            <Table.Tr>
                                <Table.Th>
                                    <Stack gap={0}>
                                        <Text size="sm" fw={700}>Average</Text>
                                        <Text size="xs" c="dimmed">(Goal: 5.0)</Text>
                                    </Stack>
                                </Table.Th>
                                {criteria.map(c => {
                                    const stats = columnStats[c.id];
                                    if (!stats) return <Table.Th key={c.id} />;
                                    return (
                                        <Table.Th key={c.id} style={{ textAlign: 'center' }}>
                                            <Group gap={4} justify="center">
                                                <Text fw={700} c={stats.valid ? 'teal' : 'red'}>
                                                    {stats.avg.toFixed(2)}
                                                </Text>
                                                {stats.valid ? <IconCheck size={16} color="green" /> : <IconAlertCircle size={16} color="red" />}
                                            </Group>
                                        </Table.Th>
                                    );
                                })}
                                <Table.Th />
                            </Table.Tr>
                        </Table.Tfoot>
                    </Table>
                </ScrollArea>
            </Card>

            {/* Pre-Submission Report Modal */}
            <Modal opened={reportOpen} onClose={() => setReportOpen(false)} title="Evaluation Impact Analysis" size="lg">
                {analysisData && (
                    <Stack>
                        <Alert
                            color={analysisData.bias_warning === 'Balanced' ? 'green' : 'orange'}
                            title="Bias Check"
                            icon={analysisData.bias_warning === 'Balanced' ? <IconCheck /> : <IconAlertCircle />}
                        >
                            <Text>Your rating tendency is: <Text span fw={700}>{analysisData.bias_warning}</Text></Text>
                            <Text size="sm">Average Score: {analysisData.average} (Target: ~5.0)</Text>
                        </Alert>

                        <Card withBorder>
                            <Text fw={700} mb="md">Rating Distribution</Text>
                            <div style={{ height: 300, width: '100%' }}>
                                <ResponsiveContainer>
                                    <BarChart data={Object.entries(analysisData.distribution).map(([range, count]) => ({ range, count }))}>
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="range" />
                                        <YAxis allowDecimals={false} />
                                        <Tooltip />
                                        <Bar dataKey="count" fill="#228be6" name="Job Count" />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </Card>

                        <Group justify="flex-end" mt="md">
                            <Button variant="default" onClick={() => setReportOpen(false)}>Edit Ratings</Button>
                            <Button color="teal" onClick={handleConfirmSubmit}>Confirm & Submit</Button>
                        </Group>
                    </Stack>
                )}
            </Modal>
        </Stack>
    );
}
