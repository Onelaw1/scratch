import { Paper, Text, Group, Badge, Table, ThemeIcon, List } from '@mantine/core';
import { IconCheck, IconUserCheck } from '@tabler/icons-react';

export function RolePermissionsMatrix() {
    return (
        <Paper p="xl" radius="md" withBorder bg="gray.0" mb="xl">
            <Group mb="lg">
                <ThemeIcon color="dark" size="lg" radius="xl"><IconUserCheck size={20} /></ThemeIcon>
                <div>
                    <Text fw={700} size="lg">Appendix A: Role-Based User Permissions</Text>
                    <Text c="dimmed" size="xs">Granular Access Control List (ACL) Definition</Text>
                </div>
            </Group>
            <Table striped withTableBorder withColumnBorders bg="white">
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th style={{ width: '20%' }}>Target Role (Actor)</Table.Th>
                        <Table.Th style={{ width: '40%' }}>Core Pain Points (Human Needs)</Table.Th>
                        <Table.Th>System Resolution & Permissions</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                    <Table.Tr>
                        <Table.Td><Badge color="red" variant="filled" size="md">EXECUTIVE</Badge></Table.Td>
                        <Table.Td>
                            <List size="xs" spacing={2} icon={<IconCheck size={10} color="red" />}>
                                <List.Item>Organizational Efficiency Audit</List.Item>
                                <List.Item>Workforce Risk Prediction</List.Item>
                            </List>
                        </Table.Td>
                        <Table.Td>
                            <Badge variant="outline" color="red" mr={5}>VIEW_ALL_STATS</Badge>
                            <Badge variant="outline" color="red">EXECUTE_SIMULATION</Badge>
                        </Table.Td>
                    </Table.Tr>
                    <Table.Tr>
                        <Table.Td><Badge color="teal" variant="filled" size="md">HR MANAGER</Badge></Table.Td>
                        <Table.Td>
                            <List size="xs" spacing={2} icon={<IconCheck size={10} color="teal" />}>
                                <List.Item>Fairness Calibration</List.Item>
                                <List.Item>JD Standardization</List.Item>
                            </List>
                        </Table.Td>
                        <Table.Td>
                            <Badge variant="outline" color="teal" mr={5}>MANAGE_USERS</Badge>
                            <Badge variant="outline" color="teal">EDIT_JOB_MATRIX</Badge>
                        </Table.Td>
                    </Table.Tr>
                    <Table.Tr>
                        <Table.Td><Badge color="pink" variant="filled" size="md">TEAM LEAD</Badge></Table.Td>
                        <Table.Td>
                            <List size="xs" spacing={2} icon={<IconCheck size={10} color="pink" />}>
                                <List.Item>Team Resource Allocation</List.Item>
                                <List.Item>Performance Review (Rater)</List.Item>
                            </List>
                        </Table.Td>
                        <Table.Td>
                            <Badge variant="outline" color="pink" mr={5}>VIEW_TEAM_DASHBOARD</Badge>
                            <Badge variant="outline" color="pink">WRITE_EVALUATION</Badge>
                        </Table.Td>
                    </Table.Tr>
                    <Table.Tr>
                        <Table.Td><Badge color="indigo" variant="filled" size="md">EMPLOYEE</Badge></Table.Td>
                        <Table.Td>
                            <List size="xs" spacing={2} icon={<IconCheck size={10} color="indigo" />}>
                                <List.Item>Role Clarity (R&R)</List.Item>
                                <List.Item>Fair Evaluation Record</List.Item>
                            </List>
                        </Table.Td>
                        <Table.Td>
                            <Badge variant="outline" color="indigo" mr={5}>VIEW_OWN_PROFILE</Badge>
                            <Badge variant="outline" color="indigo">SUBMIT_APPEAL</Badge>
                        </Table.Td>
                    </Table.Tr>
                </Table.Tbody>
            </Table>
        </Paper>
    )
}
