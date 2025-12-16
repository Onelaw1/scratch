import { Paper, Text, Group, ThemeIcon, SimpleGrid, Card, Divider, Code, Badge, Stack, Box } from '@mantine/core';
import { IconLock, IconDatabase, IconFileCode, IconArrowRight, IconShieldCheck, IconUserCheck, IconServer } from '@tabler/icons-react';

export function SecurityArchitectureDiagram() {
    return (
        <Paper p="xl" radius="lg" withBorder bg="gray.0" mb="xl">
            <Group justify="space-between" mb="lg">
                <Group>
                    <ThemeIcon size={48} radius="md" color="teal" variant="filled">
                        <IconShieldCheck size={28} />
                    </ThemeIcon>
                    <div>
                        <Text size="xl" fw={700}>보안 아키텍처 및 권한 제어 흐름</Text>
                        <Text c="dimmed">Security Architecture & Permission Enforcement Flow</Text>
                    </div>
                </Group>
                <Badge size="lg" color="red" variant="outline">Strict RBAC Enforced</Badge>
            </Group>

            {/* Diagram Container */}
            <SimpleGrid cols={{ base: 1, md: 4 }} spacing="lg" style={{ alignItems: 'stretch' }}>

                {/* 1. Definition Layer */}
                <DiagramCard
                    title="1. 권한 정의 (Definition)"
                    icon={IconFileCode}
                    color="blue"
                    description="권한은 코드가 아닌 설정 파일에서 독립적으로 관리됩니다."
                >
                    <Code block color="blue.1" c="blue.9" style={{ fontSize: '0.75rem' }}>
                        {`HR_MANAGER:
  personnel: all
  jobs: write_all

TEAM_LEAD:
  personnel: read_own`}
                    </Code>
                    <Badge mt="xs" variant="dot">permissions.yaml</Badge>
                </DiagramCard>

                {/* Arrow */}
                <FlowArrow label="Login & JWT" />

                {/* 2. Enforcement Layer */}
                <DiagramCard
                    title="2. 보안 가드 (Enforcement)"
                    icon={IconLock}
                    color="red"
                    description="모든 API 요청은 미들웨어 레벨에서 교차 검증됩니다."
                >
                    <Stack gap="xs" mt="xs">
                        <Paper withBorder p="xs" radius="sm" bg="white">
                            <Group gap="xs">
                                <IconUserCheck size={14} color="gray" />
                                <Text size="xs" fw={700}>Role Extraction</Text>
                            </Group>
                        </Paper>
                        <Paper withBorder p="xs" radius="sm" bg="white">
                            <Group gap="xs">
                                <IconShieldCheck size={14} color="red" />
                                <Text size="xs" fw={700}>Permission Match</Text>
                            </Group>
                        </Paper>
                    </Stack>
                    <Badge mt="xs" color="red">dependencies.py</Badge>
                </DiagramCard>

                {/* Arrow */}
                <FlowArrow label="Access Granted" />

                {/* 3. Data Data Layer */}
                <DiagramCard
                    title="3. 데이터 접근 (Access)"
                    icon={IconDatabase}
                    color="grape"
                    description="검증된 요청만이 실제 DB 모델에 접근하여 데이터를 처리합니다."
                >
                    <Stack gap="xs" mt="xs">
                        <Paper withBorder p="xs" radius="sm" bg="white">
                            <Group gap="xs">
                                <IconServer size={14} color="grape" />
                                <Text size="xs">User Model (ORM)</Text>
                            </Group>
                        </Paper>
                        <Paper withBorder p="xs" radius="sm" bg="white">
                            <Group gap="xs">
                                <IconDatabase size={14} color="grape" />
                                <Text size="xs">PostgreSQL DB</Text>
                            </Group>
                        </Paper>
                    </Stack>
                </DiagramCard>

            </SimpleGrid>

            <Divider my="lg" style={{ borderStyle: 'dashed' }} />

            <Group justify="center" gap="xl">
                <Text size="sm" c="dimmed">Architecture Verification:</Text>
                <Group gap="xs">
                    <IconCheckCircle label="JWT Standard" />
                    <IconCheckCircle label="YAML Configurable" />
                    <IconCheckCircle label="Middleware Guard" />
                </Group>
            </Group>
        </Paper>
    );
}

function DiagramCard({ title, icon: Icon, color, description, children }: any) {
    return (
        <Card withBorder radius="md" padding="lg" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Group mb="md">
                <ThemeIcon variant="light" color={color} size="lg" radius="md">
                    <Icon size={20} />
                </ThemeIcon>
                <Text fw={700} size="sm">{title}</Text>
            </Group>
            <Text size="xs" c="dimmed" mb="md" style={{ flexGrow: 1 }}>
                {description}
            </Text>
            {children}
        </Card>
    );
}

function FlowArrow({ label }: { label: string }) {
    return (
        <Box className="hidden md:flex" style={{ flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <Text size="xs" c="dimmed" mb={4} fw={600}>{label}</Text>
            <ThemeIcon variant="transparent" color="gray" size="xl">
                <IconArrowRight size={32} />
            </ThemeIcon>
        </Box>
    );
}

function IconCheckCircle({ label }: { label: string }) {
    return (
        <Group gap={6}>
            <ThemeIcon color="teal" size="sm" radius="xl" variant="filled">
                <IconShieldCheck size={10} />
            </ThemeIcon>
            <Text size="sm" fw={500}>{label}</Text>
        </Group>
    )
}
