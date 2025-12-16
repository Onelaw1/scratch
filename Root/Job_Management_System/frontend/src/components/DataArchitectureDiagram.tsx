"use client";

import { Paper, Title, Grid, Stack, Text, Group, ThemeIcon, Badge, SimpleGrid, Card, RingProgress, Box } from '@mantine/core';
import {
    IconDatabase, IconServer, IconAssembly, IconCpu, IconDeviceAnalytics, IconArrowRight, IconCloudDownload, IconRefresh,
    IconTable, IconCode, IconApi, IconRobot, IconStack2
} from '@tabler/icons-react';

export function DataArchitectureDiagram() {
    return (
        <Card p="xl" radius="lg" withBorder bg="gray.1" mb="xl">
            <Group justify="space-between" mb="lg">
                <Group>
                    <ThemeIcon size="xl" radius="md" color="indigo" variant="filled">
                        <IconAssembly size={28} />
                    </ThemeIcon>
                    <div>
                        <Title order={2}>Deep-Dive Data Intelligence Architecture</Title>
                        <Text c="dimmed">Detailed Technical Flow: Sources → Ingestion (CDC/Batch) → Lakehouse (Medallion) → AI Ops → Deployment</Text>
                    </div>
                </Group>
                <Badge size="lg" color="indigo" variant="light">Technical View</Badge>
            </Group>

            <Grid gutter="md">
                {/* 1. SOURCES LAYER */}
                <Grid.Col span={2}>
                    <LayerHeader label="1. DATA SOURCES" color="cyan" />
                    <Stack gap="sm">
                        <DetailBox icon={IconDatabase} title="Legacy HRIS" sub="Oracle DB" details={['Employee Master', 'Org Structure']} color="cyan" />
                        <DetailBox icon={IconServer} title="Financial ERP" sub="SAP/Netsuite" details={['GL Data', 'Budget Codes']} color="blue" />
                        <DetailBox icon={IconDeviceAnalytics} title="User Interactions" sub="Web Events" details={['Clickstream', 'Survey Response']} color="violet" />
                    </Stack>
                </Grid.Col>

                <ArrowCol />

                {/* 2. PLATFORM CORE */}
                <Grid.Col span={7}>
                    <Paper p="md" shadow="sm" radius="md" withBorder style={{ height: '100%', borderColor: '#4c6ef5', borderWidth: 2 }} bg="white">
                        <Badge color="indigo" size="lg" mb="md" fullWidth>Unified Data Intelligence Platform</Badge>

                        <Grid>
                            {/* INGESTION */}
                            <Grid.Col span={4}>
                                <SubLayerHeader label="2. INGESTION" color="orange" />
                                <Stack gap="xs" h="100%">
                                    <TechBox icon={IconRefresh} title="Batch ETL" tech="Apache Airflow" desc="Nightly Sync" color="orange" />
                                    <TechBox icon={IconCloudDownload} title="CDC Stream" tech="Debezium / Kafka" desc="Real-time Change Event" color="orange" />
                                    <TechBox icon={IconApi} title="API Gateway" tech="FastAPI Ingress" desc="Direct Payload" color="orange" />
                                </Stack>
                            </Grid.Col>

                            {/* STORAGE & PROCESSING */}
                            <Grid.Col span={8}>
                                <SubLayerHeader label="3. LAKEHOUSE & PROCESSING" color="blue" />

                                {/* Medallion Architecture */}
                                <SimpleGrid cols={3} spacing="xs" mb="md">
                                    <StoreBox title="Bronze (Raw)" desc="JSON/Parquet Landing" color="gray" />
                                    <StoreBox title="Silver (Clean)" desc="Deduplicated/Schema" color="blue" />
                                    <StoreBox title="Gold (Mart)" desc="Aggregated Facts" color="indigo" />
                                </SimpleGrid>

                                <Divider my="sm" label="4. AI & COMPUTE ENGINE" />

                                <Grid gutter="xs">
                                    <Grid.Col span={6}>
                                        <TechBox icon={IconCode} title="Analytical Engine" tech="Pandas / Polars" desc="Statistical Processing" color="grape" />
                                    </Grid.Col>
                                    <Grid.Col span={6}>
                                        <TechBox icon={IconRobot} title="AI / LLM Ops" tech="LangChain + Gemini" desc="RAG & Vector Search" color="grape" />
                                    </Grid.Col>
                                </Grid>
                            </Grid.Col>
                        </Grid>
                    </Paper>
                </Grid.Col>

                <ArrowCol />

                {/* 3. APPLICATIONS */}
                <Grid.Col span={2}>
                    <LayerHeader label="5. APPLICATION" color="teal" />
                    <Stack gap="sm">
                        <DetailBox icon={IconApi} title="Service Layer" sub="FastAPI / Pydantic" details={['Rest Interfaces', 'Auth Middlewares']} color="teal" />
                        <DetailBox icon={IconDeviceAnalytics} title="Frontend" sub="Next.js / Mantine" details={['SSR Rendering', 'Interactive Dash']} color="green" />
                        <DetailBox icon={IconCpu} title="Strategic HR" sub="Eval & Analytics" details={['Job Valuation', 'Span of Control']} color="grape" />
                        <DetailBox icon={IconStack2} title="BI Connectors" sub="Superset / Tableau" details={['Executive View', 'Ad-hoc Query']} color="teal" />
                    </Stack>
                </Grid.Col>
            </Grid>
        </Card>
    );
}

function ArrowCol() {
    return (
        <Grid.Col span={0.5} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <IconArrowRight size={24} className="text-gray-400" />
        </Grid.Col>
    )
}

function LayerHeader({ label, color }: any) {
    return (
        <Text c={color + ".8"} fw={800} size="xs" ta="center" mb="xs" style={{ letterSpacing: 1 }}>{label}</Text>
    )
}

function SubLayerHeader({ label, color }: any) {
    return (
        <Badge color={color} variant="light" size="sm" mb="xs" fullWidth>{label}</Badge>
    )
}

function DetailBox({ icon: Icon, title, sub, details, color }: any) {
    return (
        <Paper p="xs" withBorder radius="md" bg="white" className="shadow-xs hover:shadow-md transition-all">
            <Group gap="xs" mb={4}>
                <ThemeIcon color={color} variant="light" size="sm"><Icon size={14} /></ThemeIcon>
                <Text size="sm" fw={700} lh={1}>{title}</Text>
            </Group>
            <Text size="xs" c="dimmed" mb={5}>{sub}</Text>
            <Stack gap={2}>
                {details.map((d: string) => (
                    <Group gap={4} key={d} wrap="nowrap">
                        <Box w={4} h={4} bg={color + ".4"} style={{ borderRadius: '50%' }} />
                        <Text size="9px" c="dimmed" truncate>{d}</Text>
                    </Group>
                ))}
            </Stack>
        </Paper>
    )
}

function TechBox({ icon: Icon, title, tech, desc, color }: any) {
    return (
        <Paper p="xs" withBorder radius="sm" bg={color + ".0"}>
            <Group gap="xs" mb={2}>
                <ThemeIcon color={color} variant="transparent" size="sm"><Icon size={16} /></ThemeIcon>
                <Text size="xs" fw={700} c={color + ".9"}>{title}</Text>
            </Group>
            <Text size="11px" fw={600}>{tech}</Text>
            <Text size="9px" c="dimmed">{desc}</Text>
        </Paper>
    )
}

function StoreBox({ title, desc, color }: any) {
    return (
        <Paper p="xs" withBorder radius="sm" bg={color + ".0"} ta="center">
            <IconTable size={16} className={`text-${color}-600 mx-auto mb-1`} />
            <Text size="xs" fw={700}>{title}</Text>
            <Text size="9px" c="dimmed" lh={1.2}>{desc}</Text>
        </Paper>
    )
}

function Divider({ my, label }: any) {
    return (
        <div style={{ margin: `${my} 0`, textAlign: 'center', borderBottom: '1px dashed #ccc', height: 10, position: 'relative' }}>
            <span style={{ background: '#fff', padding: '0 5px', fontSize: 10, fontWeight: 700, color: '#888', position: 'absolute', top: 0, left: '50%', transform: 'translateX(-50%)' }}>{label}</span>
        </div>
    )
}
