"use client";

import { Box, Group, Text, ThemeIcon, Title, Paper, RingProgress, Badge, Tooltip, SimpleGrid, Card, Button } from "@mantine/core";
import {
    IconFileDescription, IconListTree, IconClockHour4, IconSitemap, IconChartBar,
    IconScale, IconArrowRight, IconLock, IconCheck
} from "@tabler/icons-react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion"; // Assuming framer-motion is available? If not, standard CSS.
// I'll use standard CSS animation to be safe, or just Mantine styles.

interface StepNode {
    id: string;
    title: string;
    description: string;
    path: string;
    icon: any;
    status: "completed" | "active" | "locked";
    progress: number;
}

const STEPS: StepNode[] = [
    {
        id: "step1",
        title: "Step 1. 직무 정의",
        description: "직무를 정의하고 필요 역량을 설정합니다.",
        path: "/job-description",
        icon: IconFileDescription,
        status: "completed", // Mock
        progress: 100
    },
    {
        id: "step2",
        title: "Step 2. 업무 분해",
        description: "과업(Task)을 세분화하고 구조를 잡습니다.",
        path: "/job-description", // Merged into JD page functionality effectively
        icon: IconListTree,
        status: "completed",
        progress: 100
    },
    {
        id: "step3",
        title: "Step 3. 업무량 조사",
        description: "시간, 빈도, 난이도를 측정합니다.",
        path: "/job-survey",
        icon: IconClockHour4,
        status: "active",
        progress: 30
    },
    {
        id: "step4",
        title: "Step 4. 직무 분류",
        description: "직무 체계(Group/Series)를 분류합니다.",
        path: "/job-classification",
        icon: IconSitemap,
        status: "active",
        progress: 0
    },
    {
        id: "step5",
        title: "Step 5. 적정 인력",
        description: "FTE 분석 및 적정 인원을 산출합니다.",
        path: "/workload-analysis",
        icon: IconChartBar,
        status: "active",
        progress: 0
    },
    {
        id: "step6",
        title: "Step 6. 보상/평가",
        description: "직무 가치 평가 및 공정성을 검증합니다.",
        path: "/job-evaluation",
        icon: IconScale,
        status: "active",
        progress: 0
    }
];

export function GamifiedWorkflowMap() {
    const router = useRouter();

    return (
        <Box py="xl" px="md">
            <Group justify="center" mb={50}>
                <Box ta="center">
                    <Text size="sm" fw={700} c="blue" tt="uppercase" style={{ letterSpacing: 2 }}>Job Architecture Journey</Text>
                    <Title order={1} style={{ fontSize: '3rem' }}>
                        직무 관리 프로세스
                    </Title>
                    <Text c="dimmed" mt="md" maw={600} mx="auto">
                        아래의 로드맵을 따라 미션을 수행하세요. 모든 단계가 완료되면 최적화된 조직 설계를 얻을 수 있습니다.
                    </Text>
                </Box>
            </Group>

            <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing={40} verticalSpacing={60}>
                {STEPS.map((step, idx) => {
                    const isActive = step.status === "active";
                    const isLocked = step.status === "locked";
                    const isDone = step.status === "completed";

                    return (
                        <div key={step.id} style={{ position: 'relative' }}>
                            {/* Connector Line (Horizontal for Grid?) - Hard to do perfect connectivity in Grid without SVG.
                                Let's stick to Cards style arranged visually.
                            */}

                            <Card
                                shadow={isActive ? "xl" : "sm"}
                                padding="xl"
                                radius="lg"
                                withBorder={!isActive}
                                style={{
                                    border: isActive ? '2px solid var(--mantine-color-blue-5)' : undefined,
                                    opacity: isLocked ? 0.6 : 1,
                                    transform: isActive ? 'scale(1.05)' : 'none',
                                    transition: 'all 0.3s ease',
                                    cursor: isLocked ? 'not-allowed' : 'pointer',
                                    height: '100%'
                                }}
                                onClick={() => !isLocked && router.push(step.path)}
                            >
                                <Group justify="space-between" mb="lg">
                                    <ThemeIcon
                                        size={50}
                                        radius="md"
                                        variant={isActive ? "gradient" : "light"}
                                        gradient={{ from: 'blue', to: 'cyan' }}
                                        color={isLocked ? 'gray' : 'blue'}
                                    >
                                        <step.icon size={26} />
                                    </ThemeIcon>
                                    {isDone && <ThemeIcon color="green" radius="xl"><IconCheck size={16} /></ThemeIcon>}
                                    {isLocked && <ThemeIcon color="gray" variant="transparent"><IconLock size={20} /></ThemeIcon>}
                                    {isActive && <Badge variant="dot" size="lg">진행 중</Badge>}
                                </Group>

                                <Text size="sm" c="dimmed" fw={700} tt="uppercase">Mission {idx + 1}</Text>
                                <Title order={3} mt={4} mb="sm">{step.title}</Title>
                                <Text size="sm" c="dimmed" mb="xl" style={{ minHeight: 40 }}>
                                    {step.description}
                                </Text>

                                <Group align="center" mt="auto">
                                    <RingProgress
                                        size={80}
                                        thickness={8}
                                        roundCaps
                                        sections={[{ value: step.progress, color: isActive ? 'blue' : isDone ? 'green' : 'gray' }]}
                                        label={
                                            <Text ta="center" size="xs" fw={700}>
                                                {step.progress}%
                                            </Text>
                                        }
                                    />
                                    <Button
                                        variant={isActive ? "filled" : "light"}
                                        color={isActive ? "blue" : "gray"}
                                        fullWidth
                                        style={{ flex: 1 }}
                                        disabled={isLocked}
                                        rightSection={!isLocked && <IconArrowRight size={16} />}
                                    >
                                        {isActive ? "계속하기" : isDone ? "다시보기" : "잠김"}
                                    </Button>
                                </Group>
                            </Card>

                            {/* Arrow to next step (Visual Only, simplified) */}
                            {idx < STEPS.length - 1 && (
                                <Box
                                    style={{
                                        position: 'absolute',
                                        right: -25,
                                        top: '50%',
                                        zIndex: 1,
                                        display: 'none' // Hidden for grid layout simplicity, could enable for flex
                                    }}
                                >
                                    <IconArrowRight size={24} color="#adb5bd" />
                                </Box>
                            )}
                        </div>
                    );
                })}
            </SimpleGrid>
        </Box>
    );
}
