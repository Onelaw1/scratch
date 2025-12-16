import { Paper, Text, Group, Badge, SimpleGrid, Card, ThemeIcon, Stack, Divider, Box, Center, RingProgress } from '@mantine/core';
import { IconUser, IconUserShield, IconBriefcase, IconBuildingSkyscraper, IconKey, IconEye, IconEdit, IconCheck } from '@tabler/icons-react';

export function UserRoleSpace3D() {
    return (
        <Paper p="xl" radius="lg" withBorder bg="gray.1" mb="xl">
            <Group mb="xl">
                <ThemeIcon color="violet" size="lg" radius="xl" variant="filled"><IconUserShield size={20} /></ThemeIcon>
                <div>
                    <Text fw={700} size="lg">Appendix A: User Role & Permission Space</Text>
                    <Text c="dimmed" size="xs">Multi-Dimensional Access Control Architecture</Text>
                </div>
            </Group>

            <SimpleGrid cols={{ base: 1, md: 4 }} spacing="lg">
                <RoleCard
                    role="EXECUTIVE"
                    icon={IconBuildingSkyscraper}
                    color="red"
                    desc="Strategic Decision Maker"
                    access={["Dashboard", "Simulation", "Audit"]}
                    perms={["VIEW_ALL", "EXEC_SIM", "READ_AUDIT"]}
                />
                <RoleCard
                    role="HR MANAGER"
                    icon={IconUserShield}
                    color="teal"
                    desc="System Operator & Auditor"
                    access={["User Mgmt", "Job Matrix", "Calibration"]}
                    perms={["MANAGE_USER", "EDIT_JOB", "RUN_CALIB"]}
                />
                <RoleCard
                    role="TEAM LEAD"
                    icon={IconBriefcase}
                    color="cyan"
                    desc="Unit Performance Owner"
                    access={["Team Eval", "KPI Setup", "Work Allocation"]}
                    perms={["VIEW_TEAM", "WRITE_EVAL", "ASSIGN_WORK"]}
                />
                <RoleCard
                    role="EMPLOYEE"
                    icon={IconUser}
                    color="indigo"
                    desc="Individual Contributor"
                    access={["My Profile", "Workload", "Task R&R"]}
                    perms={["VIEW_SELF", "LOG_WORK", "VIEW_RNR"]}
                />
            </SimpleGrid>
        </Paper>
    )
}

function RoleCard({ role, icon: Icon, color, desc, access, perms }: any) {
    return (
        <Card radius="md" p={0} withBorder style={{ overflow: 'visible' }}>
            {/* Header Layer */}
            <Paper p="md" bg={`${color}.1`} radius="md" style={{ borderBottomLeftRadius: 0, borderBottomRightRadius: 0 }}>
                <Center>
                    <ThemeIcon color={color} size={48} radius="50%" variant="filled" mb="sm" style={{ border: `4px solid white`, boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}>
                        <Icon size={24} />
                    </ThemeIcon>
                </Center>
                <Text fw={800} size="lg" ta="center" c={`${color}.9`}>{role}</Text>
                <Text size="xs" ta="center" c={`${color}.7`} mb="xs">{desc}</Text>
            </Paper>

            {/* Content Layer */}
            <Stack gap="xs" p="md" bg="white" style={{ minHeight: 200 }}>

                {/* Access Zone (Spatial) */}
                <Box>
                    <Group gap="xs" mb={4}>
                        <IconEye size={14} color="gray" />
                        <Text size="xs" fw={700} tt="uppercase" c="dimmed">Access Scope</Text>
                    </Group>
                    <Box p="xs" bg="gray.0" style={{ borderRadius: 8, border: '1px dashed #ced4da' }}>
                        <SimpleGrid cols={1} spacing={4}>
                            {access.map((a: string) => (
                                <Group key={a} gap={6}>
                                    <ThemeIcon color={color} size={6} radius="xl"><IconCheck size={4} /></ThemeIcon>
                                    <Text size="xs" fw={600}>{a}</Text>
                                </Group>
                            ))}
                        </SimpleGrid>
                    </Box>
                </Box>

                <Divider variant="dotted" />

                {/* Permission Keys (Functional) */}
                <Box>
                    <Group gap="xs" mb={4}>
                        <IconKey size={14} color="gray" />
                        <Text size="xs" fw={700} tt="uppercase" c="dimmed">Permission Keys</Text>
                    </Group>
                    <Group gap={4}>
                        {perms.map((p: string) => (
                            <Badge key={p} size="xs" variant="outline" color={color} style={{ textTransform: 'none' }}>{p}</Badge>
                        ))}
                    </Group>
                </Box>
            </Stack>

            {/* Footer Layer */}
            <Paper p="xs" bg="gray.1" style={{ borderTop: '1px solid #eee' }}>
                <Group justify="center" gap="xs">
                    <Badge size="xs" color="dark" variant="filled">ACL Level {role === 'EXECUTIVE' || role === 'HR MANAGER' ? '1 (Admin)' : '2 (User)'}</Badge>
                </Group>
            </Paper>
        </Card>
    );
}
