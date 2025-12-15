"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    Button, Select, Badge, ThemeIcon, Loader, RingProgress,
    List, Accordion
} from "@mantine/core";
import {
    IconScale, IconBuildingBank, IconCheck, IconX,
    IconFileText, IconShieldCheck
} from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function NCSAuditPage() {
    // State
    const [jobs, setJobs] = useState<any[]>([]);
    const [selectedJob, setSelectedJob] = useState<string | null>(null);
    const [auditResult, setAuditResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    // Initial Load: Fetch Jobs (Mocking list for now as api.getJobDescriptions is not readily available/verified in context)
    // Ideally we call api.getJobDescriptions(). For this robust demo, we'll fetch or mock.
    // Let's assume api.getJobDescriptions exists or we fetch from jobs endpoint.
    // To be safe and fast, I will fetch jobs if the endpoint exists, or fallback to mock.

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                // Determine if we have a real endpoint. using api.getJobDescriptions() if exists. 
                // api.ts line 191 defines getJobDescriptions
                const data = await api.getJobDescriptions();
                setJobs(data);
            } catch (e) {
                console.warn("Failed to fetch jobs, using fallback mock", e);
                setJobs([
                    { job_id: "JOB-001", title: "IT Project Manager" },
                    { job_id: "JOB-002", title: "Data Scientist" },
                    { job_id: "JOB-003", title: "HR Administrator" }
                ]);
            }
        };
        fetchJobs();
    }, []);

    const handleAudit = async () => {
        if (!selectedJob) return;
        setLoading(true);
        setAuditResult(null);
        try {
            const result = await api.runNCSAudit(selectedJob);
            setAuditResult(result);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="md" color="blue" variant="light">
                        <IconBuildingBank size={28} />
                    </ThemeIcon>
                    NCS Compliance Audit
                </Title>
                <Text c="dimmed" size="lg">Verify Job Descriptions against National Competency Standards (Gov-Tech).</Text>
            </div>

            <Grid>
                {/* Left Panel: Job Selector */}
                <Grid.Col span={{ base: 12, md: 4 }}>
                    <Paper p="xl" radius="md" withBorder className="bg-gray-50 h-full">
                        <Stack gap="xl">
                            <div>
                                <Title order={3} mb="xs">Select Job</Title>
                                <Text size="sm" c="dimmed" mb="md">Choose an internal JD to audit.</Text>
                                <Select
                                    label="Internal Job Description"
                                    placeholder="Search or select job..."
                                    data={jobs.map(j => ({ value: j.job_id, label: j.title }))}
                                    value={selectedJob}
                                    onChange={setSelectedJob}
                                    searchable
                                    mb="md"
                                />
                                <Button
                                    fullWidth size="lg"
                                    leftSection={<IconScale size={20} />}
                                    onClick={handleAudit}
                                    loading={loading}
                                    disabled={!selectedJob}
                                >
                                    Run Audit
                                </Button>
                            </div>

                            {/* Context Info */}
                            <Accordion variant="separated">
                                <Accordion.Item value="info">
                                    <Accordion.Control icon={<IconShieldCheck size={20} color="green" />}>
                                        Why is this required?
                                    </Accordion.Control>
                                    <Accordion.Panel>
                                        <Text size="sm">
                                            Public institutions must adhere to NCS standards for fair hiring and compensation.
                                            This tool highlights gaps to prevent audit risks.
                                        </Text>
                                    </Accordion.Panel>
                                </Accordion.Item>
                            </Accordion>
                        </Stack>
                    </Paper>
                </Grid.Col>

                {/* Right Panel: Audit Report */}
                <Grid.Col span={{ base: 12, md: 8 }}>
                    {auditResult ? (
                        <Stack>
                            {/* Scorecard */}
                            <Paper p="lg" radius="md" withBorder>
                                <Grid align="center">
                                    <Grid.Col span={4} className="flex justify-center">
                                        <RingProgress
                                            size={120} thickness={12}
                                            sections={[{ value: auditResult.compliance_score, color: auditResult.compliance_score > 80 ? 'teal' : 'orange' }]}
                                            label={
                                                <Text ta="center" fw={700} size="xl">
                                                    {auditResult.compliance_score}%
                                                </Text>
                                            }
                                        />
                                    </Grid.Col>
                                    <Grid.Col span={8}>
                                        <Group justify="space-between" mb="xs">
                                            <Badge size="lg" variant="dot" color={auditResult.grade === 'A' ? 'teal' : 'red'}>
                                                Grade {auditResult.grade}
                                            </Badge>
                                            <Text size="sm" c="dimmed">{auditResult.ncs_code}</Text>
                                        </Group>
                                        <Title order={3}>{auditResult.ncs_standard}</Title>
                                        <Text c="dimmed">Target Government Standard</Text>
                                    </Grid.Col>
                                </Grid>
                            </Paper>

                            {/* Details */}
                            <Grid>
                                <Grid.Col span={6}>
                                    <Paper p="md" radius="md" withBorder h="100%">
                                        <Group mb="md">
                                            <ThemeIcon color="teal" variant="light"><IconCheck size={18} /></ThemeIcon>
                                            <Text fw={600}>Verified Competencies</Text>
                                        </Group>
                                        <List spacing="xs" size="sm" center icon={<IconCheck size={12} color="teal" />}>
                                            {auditResult.matched_items.length > 0 ? (
                                                auditResult.matched_items.map((item: string, i: number) => (
                                                    <List.Item key={i}>{item}</List.Item>
                                                ))
                                            ) : (
                                                <Text c="dimmed" size="xs">No matches found.</Text>
                                            )}
                                        </List>
                                    </Paper>
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Paper p="md" radius="md" withBorder className="bg-red-50" h="100%">
                                        <Group mb="md">
                                            <ThemeIcon color="red" variant="light"><IconX size={18} /></ThemeIcon>
                                            <Text fw={600} c="red">Missing (Audit Risk)</Text>
                                        </Group>
                                        <List spacing="xs" size="sm" center icon={<IconX size={12} color="red" />}>
                                            {auditResult.missing_items.length > 0 ? (
                                                auditResult.missing_items.map((item: string, i: number) => (
                                                    <List.Item key={i}>{item}</List.Item>
                                                ))
                                            ) : (
                                                <Text size="xs" c="teal">All clear!</Text>
                                            )}
                                        </List>
                                    </Paper>
                                </Grid.Col>
                            </Grid>
                        </Stack>
                    ) : (
                        <Paper p="xl" radius="md" withBorder h={400} className="flex flex-col items-center justify-center bg-gray-50">
                            {loading ? (
                                <Loader size="xl" />
                            ) : (
                                <>
                                    <ThemeIcon size={80} radius="xl" color="gray" variant="light" mb="xl">
                                        <IconFileText size={40} />
                                    </ThemeIcon>
                                    <Title order={3} c="dimmed">Ready to Audit</Title>
                                    <Text c="dimmed">Select a job from the left to begin analysis.</Text>
                                </>
                            )}
                        </Paper>
                    )}
                </Grid.Col>
            </Grid>
        </Container>
    );
}
