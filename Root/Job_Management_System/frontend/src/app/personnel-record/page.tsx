"use client";

import { useState, useEffect } from "react";
import {
    Container, Title, Text, Grid, Paper, Group, Stack, Badge,
    Select, Loader, Progress, ThemeIcon, Button, Modal, RingProgress, Card
} from "@mantine/core";
import { DateInput } from "@mantine/dates";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { IconBuildingSkyscraper, IconBriefcase, IconCertificate, IconCalendar, IconUser } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { useLanguage } from "@/contexts/LanguageContext";

export default function PersonnelRecordPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [allTenureData, setAllTenureData] = useState<any[]>([]);
    const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const { t } = useLanguage();

    // Edit Modal
    const [opened, { open, close }] = useDisclosure(false);
    const [editDate, setEditDate] = useState<Date | null>(null);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const data = await api.getDualTenureAnalysis();
            setAllTenureData(data);

            const userOptions = data.map((u: any) => ({
                value: u.user_id,
                label: `${u.name} (${u.position_title})`
            }));
            setUsers(userOptions);

            if (data.length > 0) {
                setSelectedUserId(data[0].user_id);
            }
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to load personnel data', color: 'red' });
        } finally {
            setLoading(false);
        }
    };

    const handleSaveDate = async () => {
        if (!selectedUserId || !editDate) return;
        try {
            const dateStr = editDate.toISOString().split('T')[0];
            await api.assignJobDate(selectedUserId, dateStr);
            notifications.show({ title: 'Success', message: 'Job assignment date updated', color: 'green' });
            close();
            loadData(); // Reload to refresh calculatons
        } catch (error) {
            console.error(error);
            notifications.show({ title: 'Error', message: 'Failed to update date', color: 'red' });
        }
    };

    const selectedData = allTenureData.find(d => d.user_id === selectedUserId);

    return (
        <Container size="xl" py="xl">
            <Group justify="space-between" mb="xl">
                <div>
                    <Title order={2} style={{ letterSpacing: '-0.5px' }}>{t('personnel.title')}</Title>
                    <Text c="dimmed">{t('personnel.subtitle')}</Text>
                </div>
                <Select
                    placeholder={t('personnel.search_placeholder')}
                    data={users}
                    value={selectedUserId}
                    onChange={setSelectedUserId}
                    searchable
                    className="w-72"
                    leftSection={<IconUser size={16} />}
                />
            </Group>

            {loading ? (
                <Grid><Grid.Col span={12}><Loader /></Grid.Col></Grid>
            ) : selectedData ? (
                <Stack gap="xl">
                    {/* Main Personnel Card (Glassmorphism) */}
                    <Paper
                        p="xl"
                        radius="lg"
                        style={{
                            background: 'rgba(255, 255, 255, 0.8)',
                            backdropFilter: 'blur(12px)',
                            border: '1px solid rgba(255,255,255,0.5)',
                            boxShadow: '0 4px 20px rgba(0,0,0,0.05)'
                        }}
                    >
                        <Group justify="space-between" align="start">
                            <Group>
                                <ThemeIcon size={80} radius="full" color="indigo" variant="gradient" gradient={{ from: 'indigo', to: 'violet' }}>
                                    <IconCertificate size={40} />
                                </ThemeIcon>
                                <div>
                                    <Text size="xl" fw={800}>{selectedData.name}</Text>
                                    <Text c="dimmed" size="md">{selectedData.position_title} • {selectedData.org_unit_name}</Text>
                                    <Group mt="xs" gap="xs">
                                        <Badge variant="light" color="blue">Grade 3</Badge>
                                        <Badge variant="outline" color="gray">{t('personnel.full_time')}</Badge>
                                    </Group>
                                </div>
                            </Group>
                            <Button variant="light" leftSection={<IconCalendar size={16} />} onClick={open}>
                                {t('personnel.set_date')}
                            </Button>
                        </Group>

                        <Grid mt="xl" gutter="xl">
                            {/* Left: Dual Tenure Progress */}
                            <Grid.Col span={{ base: 12, md: 8 }}>
                                <Card padding="lg" radius="md" withBorder bg="gray.0">
                                    <Stack gap="lg">
                                        <div>
                                            <Group justify="space-between" mb="xs">
                                                <Group gap="xs">
                                                    <IconBuildingSkyscraper size={18} className="text-gray-500" />
                                                    <Text fw={600} size="sm" tt="uppercase" c="dimmed">{t('personnel.org_tenure')}</Text>
                                                </Group>
                                                <Text fw={700}>{selectedData.absolute_tenure} years</Text>
                                            </Group>
                                            <Progress size="xl" radius="xl" value={100} color="gray" />
                                        </div>

                                        <div>
                                            <Group justify="space-between" mb="xs">
                                                <Group gap="xs">
                                                    <IconBriefcase size={18} className="text-indigo-500" />
                                                    <Text fw={600} size="sm" tt="uppercase" c="indigo">{t('personnel.job_tenure')}</Text>
                                                </Group>
                                                <Text fw={700} c="indigo">{selectedData.job_tenure} years</Text>
                                            </Group>
                                            <Progress
                                                size="xl"
                                                radius="xl"
                                                value={Math.min((selectedData.job_tenure / Math.max(selectedData.absolute_tenure, 0.1)) * 100, 100)}
                                                color="indigo"
                                                striped
                                                animated
                                            />
                                        </div>
                                    </Stack>
                                </Card>
                            </Grid.Col>

                            {/* Right: Specialization Ratio */}
                            <Grid.Col span={{ base: 12, md: 4 }}>
                                <Card padding="lg" radius="md" withBorder style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                                    <Text fw={700} mb="md" size="lg">{t('personnel.spec_ratio')}</Text>
                                    <RingProgress
                                        size={140}
                                        thickness={12}
                                        roundCaps
                                        sections={[{ value: selectedData.specialization_ratio, color: selectedData.specialization_ratio > 50 ? 'teal' : 'orange' }]}
                                        label={
                                            <Text c="dark" fw={900} ta="center" size="xl">
                                                {selectedData.specialization_ratio}%
                                            </Text>
                                        }
                                    />
                                    <Text size="sm" c="dimmed" ta="center" mt="md" px="md">
                                        {selectedData.specialization_ratio > 50
                                            ? t('personnel.high_spec')
                                            : t('personnel.low_spec')}
                                    </Text>
                                </Card>
                            </Grid.Col>
                        </Grid>
                    </Paper>
                </Stack>
            ) : (
                <Text c="dimmed" ta="center" py="xl">No personnel data available.</Text>
            )}

            <Modal opened={opened} onClose={close} title="Set Job Assignment Date">
                <Stack>
                    <DateInput
                        label="Assignment Date"
                        placeholder="Pick date"
                        value={editDate}
                        onChange={(val: any) => setEditDate(val)}
                    />
                    <Button onClick={handleSaveDate}>Save & Recalculate</Button>
                </Stack>
            </Modal>
        </Container>
    );
}
