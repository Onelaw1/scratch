"use client";

import React, { useState } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, Button, Image, Divider, Notification
} from "@mantine/core";
import { IconCertificate, IconCheck, IconDownload, IconShare, IconLock, IconQrcode } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function CertificatePage() {
    const [cert, setCert] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    // Mock User ID for demo (In real app, get from auth context)
    const MOCK_USER_ID = "00000000-0000-0000-0000-000000000001";

    const handleIssue = async () => {
        setLoading(true);
        setError("");
        try {
            const res = await api.issueBlockchainCertificate(MOCK_USER_ID);
            setCert(res);
        } catch (e) {
            console.error(e);
            setError("Failed to issue certificate. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container size="md" py="xl">
            <div className="mb-8 text-center">
                <ThemeIcon size={64} radius="xl" color="yellow" variant="light" className="mb-4">
                    <IconCertificate size={36} />
                </ThemeIcon>
                <Title order={1}>Digital Experience Certificate</Title>
                <Text c="dimmed" size="lg">Blockchain-verified proof of your career history.</Text>
            </div>

            {!cert ? (
                <Paper p="xl" radius="md" withBorder className="text-center bg-gray-50">
                    <Stack align="center" gap="md" py="xl">
                        <IconLock size={48} color="gray" />
                        <Title order={3}>Secure Issuance</Title>
                        <Text c="dimmed" maw={500}>
                            Generate a cryptographically signed certificate of your employment.
                            This record is immutable and can be verified by third parties.
                        </Text>
                        <Button
                            size="lg"
                            color="yellow"
                            onClick={handleIssue}
                            loading={loading}
                            leftSection={<IconCertificate size={20} />}
                        >
                            Issue Certificate to Blockchain
                        </Button>
                        {error && <Text c="red" size="sm">{error}</Text>}
                    </Stack>
                </Paper>
            ) : (
                <Stack>
                    <Notification icon={<IconCheck size={18} />} color="teal" title="Success" onClose={() => { }}>
                        Certificate successfully minted on the Private Consortium Chain.
                    </Notification>

                    <Paper p={0} radius="md" withBorder shadow="md" className="overflow-hidden">
                        {/* Certificate Header */}
                        <div className="bg-slate-800 p-8 text-white text-center">
                            <ThemeIcon size={60} radius="xl" color="yellow" className="mb-4">
                                <IconCertificate size={32} />
                            </ThemeIcon>
                            <Title order={2} className="uppercase tracking-widest">Certificate of Experience</Title>
                            <Text c="dimmed" size="sm" mt="xs">{cert.data.issuer}</Text>
                        </div>

                        {/* Certificate Body */}
                        <div className="p-10 bg-white">
                            <Stack gap="xl">
                                <Text ta="center" size="lg">This is to certify that</Text>
                                <Title order={1} ta="center" className="text-4xl font-serif">{cert.data.recipient_name}</Title>

                                <Divider label={<IconCheck size={12} />} labelPosition="center" />

                                <Grid>
                                    <Grid.Col span={6}><Text c="dimmed">Position</Text><Text fw={700} size="lg">{cert.data.position}</Text></Grid.Col>
                                    <Grid.Col span={6}><Text c="dimmed">Department</Text><Text fw={700} size="lg">{cert.data.department}</Text></Grid.Col>
                                    <Grid.Col span={6}><Text c="dimmed">Hire Date</Text><Text fw={700} size="lg">{cert.data.hire_date}</Text></Grid.Col>
                                    <Grid.Col span={6}><Text c="dimmed">Issue Date</Text><Text fw={700} size="lg">{cert.data.issue_date.split('T')[0]}</Text></Grid.Col>
                                </Grid>

                                <Divider my="sm" />

                                <Group align="center" justify="space-between" className="bg-gray-50 p-4 rounded-lg border border-gray-100">
                                    <Stack gap={0}>
                                        <Text size="xs" fw={700} c="dimmed" tt="uppercase">Blockchain Verification</Text>
                                        <Text size="xs" ff="monospace" c="dimmed" className="break-all">{cert.blockchain_proof.transaction_hash}</Text>
                                        <Group gap="xs" mt="xs">
                                            <Badge color="gray" size="sm">{cert.blockchain_proof.network}</Badge>
                                            <Badge color="green" size="sm">Block #{cert.blockchain_proof.block_height}</Badge>
                                        </Group>
                                    </Stack>
                                    <ThemeIcon size={60} color="dark" variant="outline" radius="md">
                                        <IconQrcode size={36} />
                                    </ThemeIcon>
                                </Group>
                            </Stack>
                        </div>

                        {/* Footer Actions */}
                        <div className="p-4 bg-gray-50 border-t flex justify-end gap-2">
                            <Button variant="default" leftSection={<IconShare size={16} />}>Share Link</Button>
                            <Button color="yellow" leftSection={<IconDownload size={16} />}>Download PDF</Button>
                        </div>
                    </Paper>
                </Stack>
            )}
        </Container>
    );
}
