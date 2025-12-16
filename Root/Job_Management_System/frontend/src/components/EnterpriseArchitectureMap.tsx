import { Paper, Text, Group, Box, SimpleGrid, Badge, Stack, Divider, ThemeIcon, Code, Grid, Center } from '@mantine/core';
import {
    IconTarget, IconSettingsAutomation, IconDatabase, IconServer, IconBuildingArch,
    IconUsers, IconChartDots, IconBrain, IconLock, IconArrowsExchange, IconDeviceDesktopAnalytics
} from '@tabler/icons-react';

export function EnterpriseArchitectureMap() {
    return (
        <Stack gap={2} bg="gray.1" p="xs" style={{ border: '1px solid #dee2e6' }}>
            {/* Header / Title Block */}
            <Paper p="md" radius={0} bg="dark.9" c="white" mb="xs">
                <Group justify="space-between">
                    <div>
                        <Text fw={900} size="xl" tt="uppercase" style={{ letterSpacing: '1px' }}>To-Be Enterprise Architecture</Text>
                        <Text size="xs" c="gray.5">Integrated Human Capital Management System (L3-L5 Granularity)</Text>
                    </div>
                    <Group gap="xs">
                        <Badge variant="filled" color="blue" radius="sm">ISP Final</Badge>
                        <Badge variant="outline" color="gray" radius="sm">Confidential</Badge>
                    </Group>
                </Group>
            </Paper>

            <Grid gutter={4}>
                {/* LEFT PILLAR: Channels and UX */}
                <Grid.Col span={1}>
                    <VerticalPillar title="Channels" color="indigo" icon={IconDeviceDesktopAnalytics} />
                </Grid.Col>

                {/* CENTER: Main Stack */}
                <Grid.Col span={10}>
                    <Stack gap={4}>

                        {/* LAYER 1: BUSINESS STRATEGY (Value Chain) */}
                        <ArchitectureLayer title="L1. Business Strategy & Value Drivers" color="red" icon={IconTarget}>
                            <SimpleGrid cols={4} spacing={4}>
                                <BizBox title="Organizational Agility" kpi="Span of Control" modules={["strategy.py", "workforce_optimization.py"]} />
                                <BizBox title="Talent Density" kpi="Perf/Pot Ratio" modules={["nine_box.py", "calibration.py"]} />
                                <BizBox title="Fairness Equity" kpi="Bias Index" modules={["fairness.py", "compliance.py"]} />
                                <BizBox title="Operational Cost" kpi="FTE Efficiency" modules={["wage.py", "productivity.py"]} />
                            </SimpleGrid>
                        </ArchitectureLayer>

                        {/* LAYER 2: BUSINESS APPLICATIONS (The 13 Pillars) */}
                        <ArchitectureLayer title="L2. Business Application Services (Core Domains)" color="blue" icon={IconSettingsAutomation}>
                            <Grid gutter={4}>
                                <Grid.Col span={3}>
                                    <DomainGroup title="Job Architecture" color="cyan">
                                        <ModuleItem name="job_centric.py" desc="Dynamic JD Manage" />
                                        <ModuleItem name="classification.py" desc="Auto Job Classify" />
                                        <ModuleItem name="raci.py" desc="R&R Matrix" />
                                        <ModuleItem name="tasks.py" desc="Task Dictionary" />
                                    </DomainGroup>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <DomainGroup title="Workforce Planning" color="teal">
                                        <ModuleItem name="workforce.py" desc="Headcount/TO Plan" />
                                        <ModuleItem name="gap_analysis.py" desc="Supply/Demand Gap" />
                                        <ModuleItem name="span_of_control.py" desc="Org Structure Sim" />
                                        <ModuleItem name="simulation.py" desc="Scenario Modeling" />
                                    </DomainGroup>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <DomainGroup title="Talent Mgmt" color="grape">
                                        <ModuleItem name="performance.py" desc="Goal & KPI Review" />
                                        <ModuleItem name="evaluation.py" desc="Multi-Rater Eval" />
                                        <ModuleItem name="promotion.py" desc="Career Path Sim" />
                                        <ModuleItem name="recruitment.py" desc="JD-CV Matching" />
                                    </DomainGroup>
                                </Grid.Col>
                                <Grid.Col span={3}>
                                    <DomainGroup title="Comp & Benefits" color="yellow">
                                        <ModuleItem name="wage.py" desc="Payroll Simulation" />
                                        <ModuleItem name="grade.py" desc="Job Grading Logic" />
                                        <ModuleItem name="reward.py" desc="Total Reward Calc" />
                                        <ModuleItem name="welfare.py" desc="Benefit Alloc" />
                                    </DomainGroup>
                                </Grid.Col>
                            </Grid>
                        </ArchitectureLayer>

                        {/* LAYER 3: INTELLIGENCE ENGINE (AI/ML) */}
                        <ArchitectureLayer title="L3. Intelligence & Analytics Engine" color="violet" icon={IconBrain}>
                            <SimpleGrid cols={5} spacing={4}>
                                <TechBox title="Generative AI" sub="LangChain / RAG" modules={["jd_generator.py", "ai_impact.py"]} />
                                <TechBox title="Predictive ML" sub="Scikit-Learn" modules={["prediction.py", "turnover_model.py"]} />
                                <TechBox title="Search Engine" sub="TF-IDF / Vector" modules={["search_engine.py", "embeddings.py"]} />
                                <TechBox title="Optimization" sub="Genetic Alg" modules={["genetic_solver.py", "opt_scheduler.py"]} />
                                <TechBox title="Text Analytics" sub="NLP / NLU" modules={["nlp_parser.py", "sentiment.py"]} />
                            </SimpleGrid>
                        </ArchitectureLayer>

                        {/* LAYER 4: DATA PERSISTENCE */}
                        <ArchitectureLayer title="L4. Data Foundation & Persistence" color="dark" icon={IconDatabase}>
                            <SimpleGrid cols={3} spacing={4}>
                                <DataBox title="Master Data" content="User, OrgUnit, JobPosition, Competency" />
                                <DataBox title="Transaction Data" content="Workload, PerformanceReview, AuditLog" />
                                <DataBox title="Mart / Warehouse" content="Snapshot, StatsCube, VectorStore" />
                            </SimpleGrid>
                        </ArchitectureLayer>

                    </Stack>
                </Grid.Col>

                {/* RIGHT PILLAR: Governance */}
                <Grid.Col span={1}>
                    <VerticalPillar title="Security & Governance" color="red" icon={IconLock} />
                </Grid.Col>
            </Grid>

            {/* FOOTER: Infrastructure */}
            <Paper p="xs" radius={0} bg="gray.3" withBorder>
                <Group justify="center" gap="xl">
                    <InfraItem label="Infrastructure" val="AWS / Hybrid Cloud" />
                    <Divider orientation="vertical" />
                    <InfraItem label="Database" val="PostgreSQL 14" />
                    <Divider orientation="vertical" />
                    <InfraItem label="Container" val="Docker / K8s" />
                    <Divider orientation="vertical" />
                    <InfraItem label="Security" val="OAuth2 / JWT" />
                    <Divider orientation="vertical" />
                    <InfraItem label="Integration" val="REST API / ERP Interface" />
                </Group>
            </Paper>

        </Stack>
    );
}

// --- Sub-components (Atomic Design) ---

function ArchitectureLayer({ title, children, color, icon: Icon }: any) {
    return (
        <Paper withBorder radius={0} p={0} style={{ borderTop: `3px solid var(--mantine-color-${color}-6)` }}>
            <Group bg={`${color}.0`} px="xs" py={4} gap="xs" style={{ borderBottom: '1px solid #eee' }}>
                <ThemeIcon size="xs" color={color} variant="transparent"><Icon size={12} /></ThemeIcon>
                <Text size="xs" fw={700} c={`${color}.9`} tt="uppercase">{title}</Text>
            </Group>
            <Box p={4} bg="white">
                {children}
            </Box>
        </Paper>
    );
}

function BizBox({ title, kpi, modules }: any) {
    return (
        <Paper withBorder p={4} radius={0} bg="red.0">
            <Text size="xs" fw={700} ta="center" mb={2}>{title}</Text>
            <Text size="9px" c="dimmed" ta="center" mb={4}>KPI: {kpi}</Text>
            <Group justify="center" gap={2}>
                {modules.map((m: string) => <Code key={m} color="red" style={{ fontSize: '8px' }}>{m}</Code>)}
            </Group>
        </Paper>
    );
}

function DomainGroup({ title, children, color }: any) {
    return (
        <Stack gap={2} bg={`${color}.0`} p={4} style={{ border: `1px solid var(--mantine-color-${color}-2)` }}>
            <Text size="xs" fw={700} ta="center" c={`${color}.9`}>{title}</Text>
            {children}
        </Stack>
    );
}

function ModuleItem({ name, desc }: any) {
    return (
        <Paper withBorder p={3} radius={0} bg="white">
            <Group justify="space-between">
                <Text size="9px" fw={700}>{name}</Text>
                <Text size="8px" c="dimmed">{desc}</Text>
            </Group>
        </Paper>
    );
}

function TechBox({ title, sub, modules }: any) {
    return (
        <Paper withBorder p={4} radius={0} bg="violet.0">
            <Text size="xs" fw={700} ta="center">{title}</Text>
            <Text size="8px" c="dimmed" ta="center" mb={2}>{sub}</Text>
            <Divider variant="dashed" my={2} />
            <Stack gap={1} align="center">
                {modules.map((m: string) => <Text key={m} size="8px" c="violet.9">{m}</Text>)}
            </Stack>
        </Paper>
    )
}

function DataBox({ title, content }: any) {
    return (
        <Paper withBorder p={4} radius={0} bg="dark.0">
            <Group gap={4} mb={2}>
                <IconDatabase size={10} color="gray" />
                <Text size="xs" fw={700}>{title}</Text>
            </Group>
            <Text size="9px" c="dimmed" style={{ lineHeight: 1.2 }}>{content}</Text>
        </Paper>
    )
}

function VerticalPillar({ title, color, icon: Icon }: any) {
    return (
        <Paper bg={`${color}.1`} h="100%" withBorder radius={0} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <ThemeIcon color={color} variant="transparent" mb="xs"><Icon size={24} style={{ transform: 'rotate(-90deg)' }} /></ThemeIcon>
            <Text
                fw={900}
                size="xs"
                tt="uppercase"
                c={`${color}.9`}
                style={{
                    writingMode: 'vertical-rl',
                    textOrientation: 'mixed',
                    transform: 'rotate(180deg)'
                }}
            >
                {title}
            </Text>
        </Paper>
    )
}

function InfraItem({ label, val }: any) {
    return (
        <Group gap={4}>
            <Text size="xs" fw={700} c="dimmed">{label}:</Text>
            <Text size="xs" fw={700}>{val}</Text>
        </Group>
    )
}
