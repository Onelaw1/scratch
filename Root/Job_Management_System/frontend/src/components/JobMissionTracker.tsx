"use client";

import { Paper, Group, Stack, Text, ThemeIcon, Progress, RingProgress, Button, Tooltip, Collapse, Checkbox, Box } from "@mantine/core";
import { IconFileText, IconSitemap, IconClock, IconAward, IconCheck, IconArrowRight, IconListDetails, IconChevronDown, IconChevronUp } from "@tabler/icons-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

interface JobMissionTrackerProps {
    currentStep: 1 | 2 | 3 | 4;
}

export function JobMissionTracker({ currentStep }: JobMissionTrackerProps) {
    const router = useRouter();
    const [detailsOpen, setDetailsOpen] = useState(true);

    const steps = [
        { step: 1, label: "직무 정의", eng: "Job Definition", desc: "직무 기술서", icon: IconFileText, path: "/job-description" },
        { step: 2, label: "업무 분해", eng: "Task Breakdown", desc: "세부 과업 구조화", icon: IconSitemap, path: "/job-survey" },
        { step: 3, label: "업무량 측정", eng: "Workload Measurement", desc: "빈도/시간 입력", icon: IconClock, path: "/job-survey" },
        { step: 4, label: "직무 분류", eng: "Classification", desc: "등급 및 계열 산정", icon: IconAward, path: "/job-classification" },
    ];

    // Mock sub-checklist for current step gamification
    const getChecklist = (step: number) => {
        if (step === 1) return [
            { label: "직무 개요(Summary) 작성", done: true },
            { label: "주요 역할(Role) 및 중요도 설정", done: false }, // Logic to check actual state would be ideal
            { label: "자격 요건(Requirements) 정의", done: false }
        ];
        if (step === 2) return [
            { label: "JD 기반 과업(Task) 불러오기", done: false },
            { label: "세부 과업(Sub-task) 쪼개기", done: false }
        ];
        return [];
    };

    const activeStepInfo = steps.find(s => s.step === currentStep);
    const progress = (currentStep - 1) / 4 * 100; // Adjusted calculation for 4 steps completion logic
    // Actually currentStep 1 means step 1 is IN PROGRESS. So 0% done of step 1? 
    // Let's say (Step-1) * 25%.

    const checklist = getChecklist(currentStep);

    return (
        <Paper p="md" radius="md" withBorder bg="var(--mantine-color-gray-0)" mb="lg">
            <Group justify="space-between" align="start">
                <Stack gap="xs" style={{ flex: 1 }}>
                    {/* Header */}
                    <Group gap="apart" justify="space-between">
                        <Group gap="xs">
                            <ThemeIcon size={42} radius="md" color="violet" variant="gradient" gradient={{ from: 'violet', to: 'indigo' }}>
                                {activeStepInfo?.icon && <activeStepInfo.icon size={24} />}
                            </ThemeIcon>
                            <div>
                                <Text size="xs" tt="uppercase" fw={700} c="dimmed">현재 미션</Text>
                                <Tooltip label={activeStepInfo?.eng} position="right" withArrow>
                                    <Text fw={900} size="xl" variant="gradient" gradient={{ from: 'violet', to: 'blue' }} style={{ cursor: 'help' }}>
                                        Step {currentStep}. {activeStepInfo?.label}
                                    </Text>
                                </Tooltip>
                            </div>
                        </Group>

                        <Button
                            variant="subtle" size="xs"
                            rightSection={detailsOpen ? <IconChevronUp size={14} /> : <IconChevronDown size={14} />}
                            onClick={() => setDetailsOpen(!detailsOpen)}
                        >
                            체크리스트 {detailsOpen ? "접기" : "보기"}
                        </Button>
                    </Group>

                    {/* Collapsible Checklist */}
                    <Collapse in={detailsOpen}>
                        <Paper withBorder p="sm" bg="white" shadow="xs" radius="md" mt="xs">
                            <Stack gap="xs">
                                <Text size="xs" fw={700} c="dimmed">해야 할 일</Text>
                                {checklist.length > 0 ? checklist.map((item, idx) => (
                                    <Group key={idx} gap="xs">
                                        <ThemeIcon variant="light" color={item.done ? "green" : "gray"} size="xs" radius="xl">
                                            <IconCheck size={10} />
                                        </ThemeIcon>
                                        <Text size="sm" c={item.done ? "dimmed" : "dark"} td={item.done ? "line-through" : ""}>
                                            {item.label}
                                        </Text>
                                    </Group>
                                )) : <Text size="sm" c="dimmed">이 단계의 추가 체크리스트가 없습니다.</Text>}
                            </Stack>
                        </Paper>
                    </Collapse>
                </Stack>

                {/* Global Progress */}
                <Stack align="flex-end" gap={0} ml="xl">
                    <Text size="xs" fw={700} c="dimmed">전체 진행률</Text>
                    <Group align="flex-end" gap="xs">
                        <Text fw={900} size="h2" c="blue" lts={-1}>{Math.round(progress)}%</Text>
                        <Text size="sm" c="dimmed" mb={4}>완료</Text>
                    </Group>
                    <Stack gap={4} mt="xs">
                        {steps.map((s) => (
                            <Group key={s.step} gap={8} align="center">
                                <ThemeIcon size={8} radius="xl" color={s.step <= currentStep ? "blue" : "gray"} variant="filled" />
                                <Tooltip label={s.eng} position="left">
                                    <Text size="xs" fw={s.step === currentStep ? 700 : 500} c={s.step === currentStep ? "blue" : "dimmed"}>
                                        {s.label}
                                    </Text>
                                </Tooltip>
                            </Group>
                        ))}
                    </Stack>
                </Stack>
            </Group>
        </Paper>
    );
}

// Map helper to determine next route based on current step
export const getNextStepPath = (currentStep: number) => {
    if (currentStep === 1) return "/job-survey"; // To Breakdown
    if (currentStep === 2) return "/job-survey"; // Stay for workload? Or simplify: 2&3 same page
    if (currentStep === 3) return "/job-classification";
    return "/";
};
