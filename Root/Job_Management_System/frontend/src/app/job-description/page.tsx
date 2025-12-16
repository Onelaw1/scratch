"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Group, Paper, Select, TextInput, Textarea, Button,
    Stack, Grid, ThemeIcon, Alert, Stepper, Progress, Badge, Slider, ActionIcon, Card, Tabs, rem, Tooltip, Modal
} from "@mantine/core";
import {
    IconFileText, IconDeviceFloppy, IconArrowRight, IconInfoCircle, IconCheck,
    IconTarget, IconPlus, IconTrash, IconChartPie, IconList
} from "@tabler/icons-react";
import { notifications } from "@mantine/notifications";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { JobMissionTracker } from "@/components/JobMissionTracker";
import { TaskHierarchyEditor } from "@/components/TaskHierarchyEditor";

export default function JobDescriptionPage() {
    const router = useRouter();
    const [positions, setPositions] = useState<any[]>([]);
    const [selectedPosition, setSelectedPosition] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    // Create Job State
    const [createModalOpen, setCreateModalOpen] = useState(false);
    const [newJobTitle, setNewJobTitle] = useState("");
    const [newJobGrade, setNewJobGrade] = useState("");

    // JD Form State (Split for UI, Combined for API)
    const [jd, setJd] = useState({
        summary: "",
        kpi_indicators: ""
    });

    // Detailed Qualification Fields (Stored as JSON in qualification_requirements)
    const [qualifications, setQualifications] = useState<any>({
        skills: "",
        values: "",
        attitudes: "",
        knowledge: "",
        previous_experience: "",
        required_training: "",
        proficiency_min: "",
        proficiency_max: ""
    });

    // Duties (Job Tasks L1)
    const [duties, setDuties] = useState<any[]>([]);

    useEffect(() => {
        loadPositions();
    }, []);

    useEffect(() => {
        if (selectedPosition) {
            loadJd(selectedPosition);
            loadDuties(selectedPosition);
        } else {
            setJd({ summary: "", kpi_indicators: "" });
            setQualifications({ skills: "", values: "", attitudes: "", knowledge: "", previous_experience: "", required_training: "" });
            setDuties([]);
        }
    }, [selectedPosition]);

    const handleCreatePosition = async () => {
        if (!newJobTitle) return;
        try {
            const newPos = await api.createJobPosition({ title: newJobTitle, grade: newJobGrade });
            notifications.show({ title: 'Success', message: '직무가 생성되었습니다.', color: 'green' });
            setNewJobTitle("");
            setNewJobGrade("");
            setCreateModalOpen(false);

            const data = await api.getJobPositions();
            const options = data.map((p: any) => ({
                value: p.id,
                label: `${p.title} (${p.grade || 'No Grade'})`
            }));
            setPositions(options);
            setSelectedPosition(newPos.id);

        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Error', message: '직무 생성 실패', color: 'red' });
        }
    };

    const loadPositions = async () => {
        try {
            const data = await api.getJobPositions();
            const options = data.map((p: any) => ({
                value: p.id,
                label: `${p.title} (${p.grade || 'No Grade'})`
            }));
            setPositions(options);
            if (!selectedPosition && options.length > 0) setSelectedPosition(options[0].value);
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load positions', color: 'red' });
        }
    };

    const loadJd = async (posId: string) => {
        setLoading(true);
        try {
            const data = await api.getJobDescription(posId);
            if (data) {
                setJd({
                    summary: data.summary || "",
                    kpi_indicators: data.kpi_indicators || ""
                });

                // Parse Qualifications
                if (data.qualification_requirements) {
                    try {
                        const parsed = JSON.parse(data.qualification_requirements);
                        setQualifications(parsed);
                    } catch (e) {
                        // Legacy text data
                        setQualifications({
                            skills: "",
                            values: "",
                            attitudes: "",
                            knowledge: "",
                            previous_experience: data.qualification_requirements,
                            required_training: ""
                        });
                    }
                } else {
                    setQualifications({ skills: "", values: "", attitudes: "", knowledge: "", previous_experience: "", required_training: "" });
                }
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const loadDuties = async (posId: string) => {
        try {
            const allTasks = await api.getJobTasks();
            const posTasks = allTasks.filter((t: any) => t.job_position_id === posId && !t.parent_id);
            setDuties(posTasks.map((t: any) => ({ ...t, importance: t.importance || 0 })));
        } catch (e) { console.error(e); }
    };

    const handleSaveJD = async (showNotif = true) => {
        if (!selectedPosition) return;
        setLoading(true);
        try {
            // Pack qualifications into JSON
            const packedQual = JSON.stringify(qualifications);
            await api.saveJobDescription(selectedPosition, {
                summary: jd.summary,
                kpi_indicators: jd.kpi_indicators,
                qualification_requirements: packedQual
            });
            if (showNotif) notifications.show({ title: 'Saved', message: 'Job Description updated', color: 'green' });
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to save JD', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleSaveDuties = async () => {
        try {
            const proms = duties.map(d => {
                return api.updateJobTask(d.id, { importance: d.importance });
            });
            await Promise.all(proms);
            notifications.show({ title: 'Saved', message: 'Duties & Weights updated', color: 'green' });
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Error', message: 'Failed to save duties', color: 'red' });
        }
    };

    const totalImportance = duties.reduce((acc, d) => acc + (d.importance || 0), 0);

    const onDutyChange = (idx: number, field: string, val: any) => {
        const newDuties = [...duties];
        newDuties[idx] = { ...newDuties[idx], [field]: val };
        setDuties(newDuties);
    };

    const addNewDuty = async () => {
        if (!selectedPosition) {
            notifications.show({ title: 'Error', message: '먼저 직무를 선택해주세요.', color: 'red' });
            return;
        }
        try {
            const newTask = await api.createJobTask({
                task_name: "새 역할 (New Duty)",
                position_id: selectedPosition
            });
            setDuties([...duties, { ...newTask, importance: 0 }]);
        } catch (e) { console.error(e); }
    };

    return (
        <Container size="xl" py="xl">
            <JobMissionTracker currentStep={1} />

            <Title order={2} mb="xs">Step 1: 직무 기술서</Title>
            <Text c="dimmed" mb="xl">
                직무의 정의, 요구 역량(Skill, Value, Attitude, Knowledge), 그리고 역할 구성을 한 페이지에서 관리합니다.
            </Text>

            <Group align="flex-start" mb="lg">
                <Paper p="md" withBorder radius="md" flex={1}>
                    <Stack gap="xs">
                        <Text size="sm" fw={700} c="dimmed">대상 직무 (Target Position)</Text>
                        <Group>
                            <Select
                                style={{ flex: 1 }}
                                placeholder="직무 선택"
                                data={positions}
                                value={selectedPosition}
                                onChange={setSelectedPosition}
                                searchable
                            />
                            <ActionIcon
                                size="lg" variant="default"
                                onClick={() => setCreateModalOpen(true)}
                                title="새 직무 생성"
                            >
                                <IconPlus size={20} />
                            </ActionIcon>
                        </Group>
                    </Stack>
                </Paper>
                <Button
                    size="lg" h={76} color="blue"
                    onClick={() => { handleSaveJD(); handleSaveDuties(); }}
                    leftSection={<IconDeviceFloppy size={24} />}
                >
                    전체 저장 (Save All)
                </Button>
            </Group>

            <Modal opened={createModalOpen} onClose={() => setCreateModalOpen(false)} title="새 직무 생성 (Create New Position)">
                <Stack>
                    <TextInput
                        label="직무명 (Job Title)"
                        placeholder="예: 클라우드 아키텍트"
                        value={newJobTitle}
                        onChange={(e) => setNewJobTitle(e.target.value)}
                    />
                    <TextInput
                        label="직급/등급"
                        placeholder="예: 4급"
                        value={newJobGrade}
                        onChange={(e) => setNewJobGrade(e.target.value)}
                    />
                    <Button onClick={handleCreatePosition} fullWidth mt="md">생성</Button>
                </Stack>
            </Modal>

            {/* Single Scroll Layout */}
            <Stack gap="xl">

                {/* 1. Job Summary */}
                <Paper p="xl" withBorder radius="md" shadow="sm">
                    <Title order={4} mb="md" c="blue.7">1. 직무 개요 (Job Summary)</Title>
                    <Textarea
                        minRows={3}
                        placeholder="이 직무의 존재 목적과 미션을 기술하세요."
                        value={jd.summary}
                        onChange={(e) => setJd({ ...jd, summary: e.target.value })}
                    />
                </Paper>

                {/* 2. Competency Model (SKVA) */}
                <Paper p="xl" withBorder radius="md" shadow="sm">
                    <Title order={4} mb="md" c="violet.7">2. 필요 역량 (Competency Requirements)</Title>
                    <Grid>
                        <Grid.Col span={6}>
                            <Textarea
                                label="Skill (기술)"
                                minRows={4}
                                placeholder="직무 수행에 필요한 구체적 기술"
                                value={qualifications.skills}
                                onChange={(e) => setQualifications({ ...qualifications, skills: e.target.value })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <Textarea
                                label="Knowledge (지식)"
                                minRows={4}
                                placeholder="업무 수행의 기반이 되는 지식"
                                value={qualifications.knowledge}
                                onChange={(e) => setQualifications({ ...qualifications, knowledge: e.target.value })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <Textarea
                                label="Attitude (태도)"
                                minRows={4}
                                placeholder="직무 수행자에게 요구되는 태도"
                                value={qualifications.attitudes}
                                onChange={(e) => setQualifications({ ...qualifications, attitudes: e.target.value })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <Textarea
                                label="Value (가치)"
                                minRows={4}
                                placeholder="직무가 지향해야 할 가치 (Core Values)"
                                value={qualifications.values}
                                onChange={(e) => setQualifications({ ...qualifications, values: e.target.value })}
                            />
                        </Grid.Col>
                    </Grid>
                </Paper>

                {/* 3. Prerequisites */}
                <Paper p="xl" withBorder radius="md" shadow="sm">
                    <Title order={4} mb="md" c="orange.7">3. 자격 및 숙련 요건 (Prerequisites & Proficiency)</Title>
                    <Grid>
                        <Grid.Col span={6}>
                            <Textarea
                                label="이전 경험 직무 (Previous Experience)"
                                minRows={3}
                                placeholder="이 직무 수행 전 경험해야 할 직무"
                                value={qualifications.previous_experience}
                                onChange={(e) => setQualifications({ ...qualifications, previous_experience: e.target.value })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <Textarea
                                label="요구 교육훈련 (Required Training)"
                                minRows={3}
                                placeholder="필수 이수 교육 과정"
                                value={qualifications.required_training}
                                onChange={(e) => setQualifications({ ...qualifications, required_training: e.target.value })}
                            />
                        </Grid.Col>

                        {/* Proficiency Time */}
                        <Grid.Col span={6}>
                            <TextInput
                                label="숙련 소요 기간 (하한)"
                                placeholder="예: 6개월"
                                value={qualifications.proficiency_min || ""}
                                onChange={(e) => setQualifications({ ...qualifications, proficiency_min: e.target.value })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <TextInput
                                label="숙련 완성 기간 (상한/적정)"
                                placeholder="예: 24개월"
                                value={qualifications.proficiency_max || ""}
                                onChange={(e) => setQualifications({ ...qualifications, proficiency_max: e.target.value })}
                            />
                        </Grid.Col>
                    </Grid>
                </Paper>

                {/* 4. Role Composition (Hierarchy Grid) */}
                <Paper p="xl" withBorder radius="md" shadow="sm" bg="gray.0">
                    <Title order={4} mb="md" c="teal.7">4. 직무 구성 과업 (Hierarchy Breakdown)</Title>
                    <Text size="sm" c="dimmed" mb="md">
                        직무를 구성하는 과업(Task)을 엑셀처럼 계층적으로 입력하세요.
                    </Text>

                    {selectedPosition ? (
                        <TaskHierarchyEditor positionId={selectedPosition} />
                    ) : (
                        <Text c="dimmed">직무를 선택하면 입력 테이블이 표시됩니다.</Text>
                    )}
                </Paper>

                <Group justify="flex-end" mt="xl">
                    <Button
                        size="xl"
                        rightSection={<IconArrowRight size={20} />}
                        onClick={() => router.push('/job-survey')}
                    >
                        다음 단계: 업무 분해 (Next Step)
                    </Button>
                </Group>

            </Stack>
        </Container>
    );
}
