import { Paper, Text, Group, Box, SimpleGrid, Badge, Stack, Divider, ThemeIcon, Code } from '@mantine/core';
import { IconTarget, IconSettingsAutomation, IconDatabase, IconServer, IconArrowDown } from '@tabler/icons-react';

export function FrameworkArchitectureDiagram() {
    return (
        <Stack gap="xs">
            {/* Header */}
            <Group justify="space-between" align="flex-end" mb="md">
                <div>
                    <Text size="xs" fw={700} c="dimmed" tt="uppercase">To-Be System Architecture</Text>
                    <Text size="h2" fw={900} style={{ letterSpacing: '-0.5px', lineHeight: 1 }}>
                        Strategic HR Information System (HRIS)
                    </Text>
                    <Text size="sm" c="dimmed">Target Operating Model for Scientific Job Management</Text>
                </div>
                <Badge size="lg" color="dark" radius="sm" variant="filled">CONFIDENTIAL / INTERNAL</Badge>
            </Group>

            {/* Level 1: Strategic Drivers (Business Value) */}
            <SectionHeader title="1. Strategic Drivers (Business Value)" icon={IconTarget} color="red" />
            <SimpleGrid cols={3} spacing="md">
                <StrategyBox
                    title="Organizational Efficiency"
                    desc="Optimal Workforce Sizing & Cost Control"
                    kpi="Span of Control > 8"
                />
                <StrategyBox
                    title="Fairness & Transparency"
                    desc="Data-Driven Evaluation & Comps"
                    kpi="Bias Score < 0.05"
                />
                <StrategyBox
                    title="Talent Retention"
                    desc="Proactive Career Pathing & Growth"
                    kpi="Turnover < 5%"
                />
            </SimpleGrid>

            <CenterArrow />

            {/* Level 2: Business Capabilities (Functional Architecture) */}
            <SectionHeader title="2. Business Capabilities (13 Pillars)" icon={IconSettingsAutomation} color="blue" />
            <Paper p="md" radius={0} withBorder bg="gray.0">
                <SimpleGrid cols={4} spacing="xs">
                    <CapabilityColumn
                        title="Job Foundation"
                        items={["Job Classification", "Job Evaluation (Matrix)", "R&R / RACI Definition", "Job Description (JD)"]}
                    />
                    <CapabilityColumn
                        title="Workforce Planning"
                        items={["Workload Analysis (FTE)", "Headcount Plan (TO)", "Gap Analysis", "Span of Control"]}
                    />
                    <CapabilityColumn
                        title="Talent Management"
                        items={["Performance Review", "9-Box Grid Calibration", "Succession Planning", "Competency Model"]}
                    />
                    <CapabilityColumn
                        title="Compensation & Growth"
                        items={["Wage Simulation", "Promotion Simulation", "Dual Tenure Track", "Reward Optimization"]}
                    />
                </SimpleGrid>
            </Paper>

            <CenterArrow />

            {/* Level 3: Application Services (System Architecture) - The CORE */}
            <SectionHeader title="3. Application Services (Python Backend Engine)" icon={IconServer} color="grape" />
            <Box style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
                {/* Micro-service style cards */}
                <ServiceCard name="job_centric.py" desc="Dynamic JD Generation & Versioning" type="Core" />
                <ServiceCard name="workforce.py" desc="FTE Calculation & TO/PO Gap Logic" type="Analytics" />
                <ServiceCard name="nine_box.py" desc="Performance-Potential Matrix Algo" type="Algorithmic" />
                <ServiceCard name="wage.py" desc="Total Labor Cost Simulation Engine" type="Simulation" />

                <ServiceCard name="classification.py" desc="ML-based Job Classification (NCS)" type="AI" />
                <ServiceCard name="span_of_control.py" desc="Graph-Theory Org Structure Analysis" type="Graph" />
                <ServiceCard name="fairness.py" desc="Z-Score Bias Detection & Calibration" type="Stats" />
                <ServiceCard name="prediction.py" desc="Retention & Promotion Prediction" type="ML" />

                <ServiceCard name="raci.py" desc="Responsibility Matrix Validation" type="Logic" />
                <ServiceCard name="job_analysis.py" desc="Time-Study Data Processing" type="Data" />
                <ServiceCard name="competency.py" desc="Skill Gap Vector Matching" type="AI" />
                <ServiceCard name="erp_sync.py" desc="Legacy System Integration (Audit)" type="Integrator" />
            </Box>

            <CenterArrow />

            {/* Level 4: Data Foundation (Information Architecture) */}
            <SectionHeader title="4. Data Foundation (Single Source of Truth)" icon={IconDatabase} color="dark" />
            <Paper p="md" radius={0} withBorder bg="dark.9" c="white">
                <SimpleGrid cols={3} spacing="xl">
                    <DataGroup title="Master Data" items={["User (Employee)", "Org Unit (Dept)", "Job Position", "Competency Library"]} />
                    <DataGroup title="Transaction Data" items={["Workload Entry", "Performance Review", "Scenario (Sim)", "Audit Log"]} />
                    <DataGroup title="Analytical Mart" items={["Snapshot (Monthly)", "Vector Index (FAISS)", "Training Set", "Metrics Cube"]} />
                </SimpleGrid>
            </Paper>
        </Stack>
    );
}

// --- Sub-components for strict layout ---

function SectionHeader({ title, icon: Icon, color }: any) {
    return (
        <Group gap="xs" mt="sm">
            <ThemeIcon color={color} size="sm" variant="transparent"><Icon size={16} /></ThemeIcon>
            <Text fw={700} uppercase size="xs" c={color}>{title}</Text>
            <Divider style={{ flexGrow: 1 }} color={color} />
        </Group>
    );
}

function StrategyBox({ title, desc, kpi }: any) {
    return (
        <Paper withBorder p="sm" radius={0} style={{ borderTop: '3px solid #e03131' }} bg="white">
            <Text fw={700} size="sm" mb={4}>{title}</Text>
            <Text size="xs" c="dimmed" mb="xs" style={{ minHeight: '32px' }}>{desc}</Text>
            <Group gap={4} bg="gray.1" p={4}>
                <Text size="xs" fw={700} c="dark">KPI:</Text>
                <Code color="red.1" c="red.9" style={{ fontSize: '10px' }}>{kpi}</Code>
            </Group>
        </Paper>
    );
}

function CapabilityColumn({ title, items }: any) {
    return (
        <Box>
            <Paper py={4} px={8} bg="blue.1" mb={4} radius={0}>
                <Text fw={700} size="xs" c="blue.9" ta="center">{title}</Text>
            </Paper>
            <Stack gap={4}>
                {items.map((item: string) => (
                    <Paper key={item} withBorder p={6} radius={0} bg="white">
                        <Text size="xs" fw={500}>{item}</Text>
                    </Paper>
                ))}
            </Stack>
        </Box>
    );
}

function ServiceCard({ name, desc, type }: any) {
    const colorMap: any = { Core: 'blue', Analytics: 'cyan', AI: 'grape', ML: 'red', Stats: 'orange', Graph: 'teal', Simulation: 'pink', Integrator: 'gray', Logic: 'violet', Data: 'lime', Algorithmic: 'indigo' };
    const c = colorMap[type] || 'gray';

    return (
        <Paper withBorder p="xs" radius={0} style={{ borderLeft: `3px solid var(--mantine-color-${c}-5)` }}>
            <Group justify="space-between" mb={4}>
                <Code color="dark" c="white" style={{ fontSize: '10px', fontWeight: 700 }}>{name}</Code>
                <Badge size="xs" variant="outline" color={c} radius={0}>{type}</Badge>
            </Group>
            <Text size="xs" c="dimmed" style={{ lineHeight: 1.2, fontSize: '10px' }}>{desc}</Text>
        </Paper>
    );
}

function DataGroup({ title, items }: any) {
    return (
        <Box>
            <Text fw={700} size="sm" c="gray.3" mb="xs" ta="center" style={{ borderBottom: '1px solid #555' }} pb={4}>{title}</Text>
            <Group gap={6} justify="center">
                {items.map((item: string) => (
                    <Badge key={item} variant="filled" color="dark.6" radius="sm" size="sm" style={{ textTransform: 'none' }}>
                        {item}
                    </Badge>
                ))}
            </Group>
        </Box>
    );
}

function CenterArrow() {
    return (
        <Group justify="center" my={-4}>
            <IconArrowDown size={14} color="#adb5bd" />
        </Group>
    )
}
