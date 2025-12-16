import { Paper, Text, Group, ThemeIcon, SimpleGrid, Card, Code, Badge, Stack, Tabs, ScrollArea, RingProgress } from '@mantine/core';
import { IconServer, IconCpu, IconCode, IconBrain, IconCheck, IconBrandPython } from '@tabler/icons-react';

export function BackendEngineVisualizer() {
    return (
        <Paper p="xl" radius="lg" withBorder bg="gray.9" c="white" mb="xl">
            <Group justify="space-between" mb="xl">
                <Group>
                    <ThemeIcon size={56} radius="md" color="blue" variant="filled">
                        <IconCpu size={32} />
                    </ThemeIcon>
                    <div>
                        <Text size="xl" fw={700} c="white">핵심 백엔드 엔진 (Backend Core Engines)</Text>
                        <Text c="dimmed">Python FastAPI & Scientific HR Algorithms</Text>
                    </div>
                </Group>
                <Badge size="lg" color="yellow" variant="outline" leftSection={<IconBrandPython size={14} />}>100% Python Native</Badge>
            </Group>

            <SimpleGrid cols={{ base: 1, md: 3 }} spacing="lg">
                <EngineCard
                    name="Talent Intelligence Engine"
                    service="nine_box_service.py"
                    description="성과(Performance)와 잠재력(Potential)을 2차원 매트릭스로 분석하여 핵심 인재군을 자동 식별합니다."
                    techs={["Numpy", "Genetic Alg", "Matrix"]}
                    color="grape"
                />
                <EngineCard
                    name="Fairness Guard System"
                    service="fairness_service.py"
                    description="다면 평가 데이터의 편향성(Bias)을 탐지하고, 이상치(Outlier)를 제거하여 평가 공정성을 보장합니다."
                    techs={["Z-Score", "Anomaly Detect", "Stats"]}
                    color="teal"
                />
                <EngineCard
                    name="Org Efficiency Analyzer"
                    service="span_service.py"
                    description="관리자 1인당 적정 통솔 범위(Span of Control)를 산출하고 조직 비효율 구간을 시각화합니다."
                    techs={["Graph Theory", "Tree Traversal"]}
                    color="orange"
                />
                <EngineCard
                    name="Dynamic JD Generator"
                    service="jd_generator.py"
                    description="LLM을 활용하여 최신 트렌드와 내부 직무 데이터를 결합, 실시간으로 직무 기술서를 생성합니다."
                    techs={["LangChain", "Vector DB", "RAG"]}
                    color="pink"
                />
                <EngineCard
                    name="Dual Tenure Tracker"
                    service="workforce_service.py"
                    description="조직 근속(Loyalty)과 직무 근속(Expertise)을 분리 계산하여 전문 인력 양성 지표를 제공합니다."
                    techs={["Time-Series", "SQLAlchemy"]}
                    color="cyan"
                />
                <EngineCard
                    name="Predictive HR Model"
                    service="prediction_service.py"
                    description="과거 인사 데이터를 학습하여 핵심 인재의 이직 확률과 승진 적합도를 예측합니다."
                    techs={["Scikit-Learn", "Regression"]}
                    color="red"
                />
            </SimpleGrid>
        </Paper>
    );
}

function EngineCard({ name, service, description, techs, color }: any) {
    return (
        <Card withBorder radius="md" padding="lg" bg="dark.7" style={{ borderColor: '#373A40' }}>
            <Group justify="space-between" mb="xs">
                <Badge variant="filled" color={color}>{name}</Badge>
                <IconServer size={18} color="gray" />
            </Group>
            <Code block color="dark" c="yellow.4" mb="md" style={{ fontSize: '0.8rem' }}>
                {`>> import ${service}`}
            </Code>
            <Text size="sm" c="gray.3" mb="lg" style={{ lineHeight: 1.6, minHeight: 45 }}>
                {description}
            </Text>

            <Group gap="xs">
                {techs.map((t: string) => (
                    <Badge key={t} size="xs" variant="outline" color="gray">{t}</Badge>
                ))}
            </Group>
        </Card>
    );
}
