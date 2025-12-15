"use client";

import React, { useEffect, useState } from "react";
import {
    Container, Title, Text, Paper, Group, Table, Badge, Button,
    ThemeIcon, Alert, LoadingOverlay
} from "@mantine/core";
import {
    IconDatabaseImport, IconServer, IconRefresh, IconCheck,
    IconAlertTriangle, IconArrowRight
} from "@tabler/icons-react";
import { notifications } from "@mantine/notifications";
import { api } from "@/lib/api";

export default function ERPSyncPage() {
    const [diffs, setDiffs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);

    const loadPreview = async () => {
        setLoading(true);
        try {
            const res = await api.previewERPSync();
            setDiffs(res);
        } catch (e) {
            console.error(e);
            notifications.show({ title: 'Error', message: 'Failed to fetch ERP data', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadPreview();
    }, []);

    const handleSync = async () => {
        setSyncing(true);
        try {
            const res = await api.executeERPSync();
            notifications.show({
                title: 'Sync Complete',
                message: `Updated ${res.updated} records successfully.`,
                color: 'green'
            });
            await loadPreview(); // Refresh to show matches
        } catch (e) {
            notifications.show({ title: 'Sync Failed', message: 'Could not update system', color: 'red' });
        } finally {
            setSyncing(false);
        }
    };

    const hasDiffs = diffs.some(d => d.status === 'DIFF');

    return (
        <Container size="lg" py="xl">
            {/* Header */}
            <div className="mb-8">
                <Group mb="xs">
                    <ThemeIcon size={40} radius="md" color="grape" variant="light">
                        <IconServer size={24} />
                    </ThemeIcon>
                    <Title order={2}>Enterprise Integration (ERP)</Title>
                </Group>
                <Text c="dimmed">
                    Synchronize Authorized Headcount and Budget data from the external ERP system (SAP/Oracle).
                </Text>
            </div>

            {/* Sync Status Card */}
            <Paper radius="md" p="xl" withBorder className="bg-gray-50 mb-8">
                <Group justify="space-between">
                    <div>
                        <Title order={4} mb={4}>Connection Status</Title>
                        <Group>
                            <Badge color="green" variant="dot">Online</Badge>
                            <Text size="sm" c="dimmed">Mock ERP Service v1.0</Text>
                        </Group>
                    </div>
                    <Button
                        size="md"
                        color="grape"
                        leftSection={<IconDatabaseImport size={20} />}
                        onClick={handleSync}
                        loading={syncing}
                        disabled={!hasDiffs && !loading} // Disable if everything matches
                    >
                        {hasDiffs ? "Sync All Changes" : "Everything is up to date"}
                    </Button>
                </Group>
            </Paper>

            {/* Diff Table */}
            <Paper radius="md" withBorder className="relative overflow-hidden">
                <LoadingOverlay visible={loading} />
                <div className="p-4 border-b border-gray-200 bg-gray-50">
                    <Group justify="space-between">
                        <Text fw={700}>Data Comparison Preview</Text>
                        <Button variant="subtle" size="xs" leftSection={<IconRefresh size={14} />} onClick={loadPreview}>Refresh</Button>
                    </Group>
                </div>

                <Table striped highlightOnHover verticalSpacing="sm">
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>Dept Code</Table.Th>
                            <Table.Th>Department Name</Table.Th>
                            <Table.Th>Budget (ERP vs Sys)</Table.Th>
                            <Table.Th>Auth TO (ERP vs Sys)</Table.Th>
                            <Table.Th>Status</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {diffs.map((row) => {
                            const isDiff = row.status === 'DIFF';
                            return (
                                <Table.Tr key={row.dept_code} className={isDiff ? "bg-yellow-50" : ""}>
                                    <Table.Td><Text fw={500} size="sm">{row.dept_code}</Text></Table.Td>
                                    <Table.Td>{row.dept_name}</Table.Td>
                                    <Table.Td>
                                        <Group gap="xs">
                                            <Text fw={700}>${row.erp_budget}M</Text>
                                            {isDiff && row.erp_budget !== row.system_budget && (
                                                <>
                                                    <IconArrowRight size={14} className="text-gray-400" />
                                                    <Text c="dimmed" td="line-through">${row.system_budget}M</Text>
                                                </>
                                            )}
                                        </Group>
                                    </Table.Td>
                                    <Table.Td>
                                        <Group gap="xs">
                                            <Text fw={700}>{row.erp_to} FTE</Text>
                                            {isDiff && row.erp_to !== row.system_to && (
                                                <>
                                                    <IconArrowRight size={14} className="text-gray-400" />
                                                    <Text c="dimmed" td="line-through">{row.system_to}</Text>
                                                </>
                                            )}
                                        </Group>
                                    </Table.Td>
                                    <Table.Td>
                                        {isDiff ? (
                                            <Badge color="yellow" leftSection={<IconAlertTriangle size={12} />}>Update Req</Badge>
                                        ) : (
                                            <Badge color="green" variant="light" leftSection={<IconCheck size={12} />}>Synced</Badge>
                                        )}
                                    </Table.Td>
                                </Table.Tr>
                            );
                        })}
                    </Table.Tbody>
                </Table>

                {!loading && diffs.length === 0 && (
                    <Text ta="center" py="xl" c="dimmed">No data found from ERP.</Text>
                )}
            </Paper>
        </Container>
    );
}
