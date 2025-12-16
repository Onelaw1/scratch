import { Paper, Text, Group, Badge, SimpleGrid, Card, Table, Tabs, ThemeIcon } from '@mantine/core';
import { IconDatabase, IconSchema, IconUsers, IconBolt, IconChartBar } from '@tabler/icons-react';

export function DataSchemaSpec() {
    return (
        <Paper p="xl" radius="lg" withBorder bg="gray.1" mb="xl">
            <Group justify="space-between" mb="xl" align="center">
                <Group>
                    <ThemeIcon size={48} radius="md" color="blue" variant="filled">
                        <IconSchema size={28} />
                    </ThemeIcon>
                    <div>
                        <Text component="h2" size="lg" fw={700} m={0}>Appendix B: Entity Relationship Data Model</Text>
                        <Text c="dimmed" size="xs">PostgreSQL / SQLAlchemy Logic Schema Reference</Text>
                    </div>
                </Group>
                <Badge size="lg" color="blue">3NF Normalized</Badge>
            </Group>

            <Tabs defaultValue="core" variant="outline" radius="md" bg="white">
                <Tabs.List mb="md">
                    <Tabs.Tab value="core" leftSection={<IconUsers size={16} />}>Master Data (Core)</Tabs.Tab>
                    <Tabs.Tab value="work" leftSection={<IconBolt size={16} />}>Work & Jobs</Tabs.Tab>
                    <Tabs.Tab value="perf" leftSection={<IconChartBar size={16} />}>Evaluation</Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="core" p="md">
                    <SimpleGrid cols={{ base: 1, md: 2 }} spacing="lg">
                        <SchemaTable
                            name="User (Employee)"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "org_unit_id", type: "FK", desc: "-> OrgUnit" },
                                { name: "reports_to_id", type: "FK", desc: "Recursive" },
                                { name: "job_assignment_date", type: "Date", desc: "Job Tenure" },
                            ]}
                        />
                        <SchemaTable
                            name="OrgUnit"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "name", type: "String", desc: "Unit Name" },
                                { name: "parent_id", type: "FK", desc: "Tree Structure" },
                                { name: "unit_type", type: "Enum", desc: "HQ/Team" }
                            ]}
                        />
                    </SimpleGrid>
                </Tabs.Panel>
                <Tabs.Panel value="work" p="md">
                    <SimpleGrid cols={{ base: 1, md: 2 }} spacing="lg">
                        <SchemaTable
                            name="JobPosition"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "title", type: "String", desc: "Position Title" },
                                { name: "grade", type: "String", desc: "Compensation Grade" },
                                { name: "ncs_code", type: "String", desc: "National Std Code" }
                            ]}
                        />
                        <SchemaTable
                            name="JobTask (Dictionary)"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "task_name", type: "String", desc: "Action Verb + Object" },
                                { name: "difficulty", type: "Int", desc: "1-5 Scale" },
                                { name: "is_ai_replaceable", type: "Bool", desc: "AI Impact" }
                            ]}
                        />
                    </SimpleGrid>
                </Tabs.Panel>
                <Tabs.Panel value="perf" p="md">
                    <SimpleGrid cols={{ base: 1, md: 2 }} spacing="lg">
                        <SchemaTable
                            name="PerformanceReview"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "user_id", type: "FK", desc: "-> User" },
                                { name: "total_score", type: "Float", desc: "Performance Axis" },
                                { name: "score_potential", type: "Float", desc: "Potential Axis" },
                                { name: "final_grade", type: "Enum", desc: "S/A/B/C/D" }
                            ]}
                        />
                        <SchemaTable
                            name="CompetencyScore"
                            fields={[
                                { name: "id", type: "UUID", desc: "PK" },
                                { name: "review_id", type: "FK", desc: "-> Review" },
                                { name: "competency_id", type: "FK", desc: "-> Competency" },
                                { name: "score", type: "Float", desc: "1-5 Rating" }
                            ]}
                        />
                    </SimpleGrid>
                </Tabs.Panel>
            </Tabs>
        </Paper>
    )
}

function SchemaTable({ name, fields }: { name: string, fields: any[] }) {
    return (
        <Card withBorder radius="md" p="md" bg="gray.0">
            <Group mb="md">
                <IconDatabase size={16} className="text-blue-600" />
                <Text fw={700} size="sm">{name}</Text>
            </Group>
            <Table striped withTableBorder withColumnBorders>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th style={{ fontSize: '10px' }}>Field</Table.Th>
                        <Table.Th style={{ fontSize: '10px' }}>Type</Table.Th>
                        <Table.Th style={{ fontSize: '10px' }}>Desc</Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                    {fields.map((f) => (
                        <Table.Tr key={f.name}>
                            <Table.Td fw={500} style={{ fontSize: '10px' }}>{f.name}</Table.Td>
                            <Table.Td><Badge size="xs" variant="outline" style={{ fontSize: '8px' }}>{f.type}</Badge></Table.Td>
                            <Table.Td c="dimmed" style={{ fontSize: '10px' }}>{f.desc}</Table.Td>
                        </Table.Tr>
                    ))}
                </Table.Tbody>
            </Table>
        </Card>
    );
}
