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
            notifications.show({ title: '오류', message: 'JD 생성 실패', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        if (!generatedJd || !selectedPosition) return;

        try {
            await api.saveGeneratedJD({
                position_id: selectedPosition,
                overview: generatedJd.overview,
                responsibilities: generatedJd.responsibilities,
                qualifications: generatedJd.qualifications
            });
            notifications.show({ title: '저장 완료', message: '직무 기술서가 저장되었습니다.', color: 'green' });
        } catch (e) {
            notifications.show({ title: '오류', message: '저장 중 문제가 발생했습니다.', color: 'red' });
        }
    };

    return (
        <Container size="md" py="xl">
            <div className="text-center mb-10">
                <ThemeIcon size={64} radius="xl" variant="filled" color="violet" className="mb-4">
                    <IconWand size={32} />
                </ThemeIcon>
                <Title order={1}>AI 직무 기술서 생성기</Title>
                <Text c="dimmed">과업(Task) 조합을 기반으로 전문적인 JD 초안을 자동 생성합니다.</Text>
            </div>

            <Stepper active={activeStep} onStepClick={setActiveStep} color="violet">
                <Stepper.Step label="대상 선정" description="직무 선택">
                    <Paper p="xl" radius="md" withBorder mt="xl">
                        <Title order={3} mb="md">대상 직무 선택</Title>
                        <Select
                            label="직무 포지션"
                            placeholder="포지션을 선택하세요"
                            data={positions}
                            value={selectedPosition}
                            onChange={setSelectedPosition}
                            size="md"
                            searchable
                        />
                        <Group justify="flex-end" mt="xl">
                            <Button onClick={() => setActiveStep(1)} disabled={!selectedPosition}>다음: 과업 선택</Button>
                        </Group>
                    </Paper>
                </Stepper.Step>

                <Stepper.Step label="과업 구성" description="핵심 과업 선택">
                    <Paper p="xl" radius="md" withBorder mt="xl">
                        <Title order={3} mb="sm">이 직무는 어떤 일을 합니까?</Title>
                        <Text c="dimmed" mb="lg">AI가 문맥을 이해할 수 있도록 핵심 과업(Task)을 체크하세요.</Text>

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
                            <Button variant="default" onClick={() => setActiveStep(0)}>이전</Button>
                            <Button color="violet" onClick={handleGenerate} loading={loading} leftSection={<IconWand size={16} />}>
                                초안 생성
                            </Button>
                        </Group>
                    </Paper>
                </Stepper.Step>

                <Stepper.Step label="검토 및 완성" description="최종 다듬기">
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
                                    <Text fw={700} size="sm" c="dimmed">직무 개요</Text>
                                    <Textarea minRows={4} autosize defaultValue={generatedJd.overview} />
                                </div>

                                <div>
                                    <Text fw={700} size="sm" c="dimmed">주요 책임 및 과업</Text>
                                    <Textarea minRows={6} autosize defaultValue={generatedJd.responsibilities} />
                                </div>

                                <div>
                                    <Text fw={700} size="sm" c="dimmed">자격 요건</Text>
                                    <Textarea minRows={3} autosize defaultValue={generatedJd.qualifications} />
                                </div>
                            </Stack>

                            <Group justify="flex-end" mt="xl">
                                <Button variant="default" onClick={() => setActiveStep(1)}>이전</Button>
                                <Button color="green" onClick={handleSave} leftSection={<IconCheck size={16} />}>최종 확정 및 저장</Button>
                            </Group>
                        </Paper>
                    )}
                </Stepper.Step>
            </Stepper>
        </Container>
    );
}
