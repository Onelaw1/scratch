"use client";

import React, { useState, useEffect } from "react";
import {
    Container, Title, Text, Paper, Grid, Stack, Group,
    ThemeIcon, Loader, Badge, Select, Button, Table
} from "@mantine/core";
import { IconWorld, IconCurrencyDollar, IconRefresh } from "@tabler/icons-react";
import { api } from "@/lib/api";

export default function GlobalSettingsPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [currency, setCurrency] = useState("KRW");

    useEffect(() => {
        const load = async () => {
            try {
                const res = await api.getGlobalSettings();
                setData(res);
                if (res.default) setCurrency(res.default);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    if (loading) return <Container py="xl" className="flex justify-center"><Loader /></Container>;
    if (!data) return <Container py="xl"><Text c="red">Failed to load global settings.</Text></Container>;

    const rates = data.rates;
    const symbols = data.symbols;

    return (
        <Container size="xl" py="xl">
            <div className="mb-8">
                <Title order={1} className="flex items-center gap-3">
                    <ThemeIcon size={48} radius="md" color="cyan" variant="light">
                        <IconWorld size={28} />
                    </ThemeIcon>
                    Global Localization Engine
                </Title>
                <Text c="dimmed" size="lg">Manage Multi-Currency and Regional compliance settings.</Text>
            </div>

            <Grid>
                {/* Control Panel */}
                <Grid.Col span={{ base: 12, md: 5 }}>
                    <Paper p="xl" radius="md" withBorder>
                        <Stack gap="lg">
                            <Title order={3}>Display Preferences</Title>

                            <Select
                                label="System Currency"
                                description="All financial data will be converted to this currency."
                                data={Object.keys(rates)}
                                value={currency}
                                onChange={(val) => setCurrency(val || "KRW")}
                                leftSection={<IconCurrencyDollar size={16} />}
                            />

                            <Button fullWidth color="cyan" variant="light">
                                Save Preference
                            </Button>

                            <Text size="xs" c="dimmed" ta="center">
                                * Exchange rates are updated daily from Central Bank API.
                            </Text>
                        </Stack>
                    </Paper>
                </Grid.Col>

                {/* Exchange Rates Table */}
                <Grid.Col span={{ base: 12, md: 7 }}>
                    <Paper p="xl" radius="md" withBorder>
                        <Group justify="space-between" mb="md">
                            <Title order={3}>Live Exchange Rates</Title>
                            <Badge variant="dot" color="green">Live</Badge>
                        </Group>

                        <Table striped highlightOnHover>
                            <Table.Thead>
                                <Table.Tr>
                                    <Table.Th>Currency</Table.Th>
                                    <Table.Th>Symbol</Table.Th>
                                    <Table.Th>Rate (vs KRW)</Table.Th>
                                    <Table.Th>Status</Table.Th>
                                </Table.Tr>
                            </Table.Thead>
                            <Table.Tbody>
                                {Object.keys(rates).map((curr) => (
                                    <Table.Tr key={curr}>
                                        <Table.Td fw={600}>{curr}</Table.Td>
                                        <Table.Td>{symbols[curr]}</Table.Td>
                                        <Table.Td>
                                            {curr === "KRW" ? "1.00" : `1 ${curr} = ${rates[curr]} KRW`}
                                        </Table.Td>
                                        <Table.Td>
                                            <Badge size="sm" color="gray">Active</Badge>
                                        </Table.Td>
                                    </Table.Tr>
                                ))}
                            </Table.Tbody>
                        </Table>
                    </Paper>
                </Grid.Col>
            </Grid>
        </Container>
    );
}
