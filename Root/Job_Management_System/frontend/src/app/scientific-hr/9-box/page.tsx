"use client";

import React, { useEffect, useState } from "react";
import {
    Container, Title, Text, Button, Group, Alert, LoadingOverlay, Tabs,
    ThemeIcon
} from "@mantine/core";
import { IconGridDots, IconRefresh, IconInfoCircle, IconArrowRight } from "@tabler/icons-react";
import { api } from "@/lib/api";
import { NineBoxGrid } from "@/components/ScientificHR/NineBoxGrid";
import { notifications } from "@mantine/notifications";

export default function NineBoxPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);

    const fetchData = async () => {
        setLoading(true);
        try {
            const res = await api.getNineBoxGrid();
            setData(res);
        } catch (e) {
            console.error(e);
            notifications.show({ title: "Error", message: "Failed to load 9-Box data", color: "red" });
        } finally {
            setLoading(false);
        }
    };

    const handleAutoMap = async () => {
        if (!confirm("This will reset all manual placements based on scores. Continue?")) return;

        setRefreshing(true);
        try {
            const res = await api.autoMapNineBox();
            notifications.show({ title: "Success", message: `Reset ${res.updated_count} employees`, color: "green" });
            fetchData();
        } catch (e) {
            notifications.show({ title: "Error", message: "Auto-Map failed", color: "red" });
        } finally {
            setRefreshing(false);
        }
    };

    const handleMove = async (reviewId: string, targetBox: number) => {
        // Optimistic UI update could be done here, but for safety we'll just reload or patch local state
        try {
            await api.moveEmployeeInNineBox(reviewId, targetBox);
            notifications.show({ title: "Updated", message: "Employee moved successfully", color: "blue" });

            // Local update to avoid full reload flicker
            setData((prev: any) => {
                if (!prev) return prev;
                const newEmps = prev.employees.map((e: any) =>
                    e.review_id === reviewId ? { ...e, box: targetBox } : e
                );
                return { ...prev, employees: newEmps };
            });

        } catch (e) {
            notifications.show({ title: "Error", message: "Move failed", color: "red" });
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <Container size="xl" py="xl">
            <LoadingOverlay visible={loading} />

            <div className="flex justify-between items-end mb-8">
                <div>
                    <Group mb="xs">
                        <ThemeIcon size={40} radius="md" color="indigo" variant="light">
                            <IconGridDots />
                        </ThemeIcon>
                        <div>
                            <Title order={2}>9-Box Talent Matrix</Title>
                            <Text c="dimmed" size="sm">Performance vs. Potential Mapping</Text>
                        </div>
                    </Group>
                </div>
                <Button
                    variant="light"
                    leftSection={<IconRefresh size={16} />}
                    onClick={handleAutoMap}
                    loading={refreshing}
                >
                    Reset & Auto-Map
                </Button>
            </div>

            <Alert icon={<IconInfoCircle size={16} />} title="Calibration Guide" color="indigo" variant="light" mb="xl">
                Drag and drop employees to adjust their placement. Manual adjustments are persisted until "Reset" is clicked.
                <br />
                <b>X-Axis:</b> Performance Review Score | <b>Y-Axis:</b> Potential (Competency) Score
            </Alert>

            {data && (
                <NineBoxGrid
                    employees={data.employees}
                    onMove={handleMove}
                />
            )}

            {!loading && (!data || data.employees.length === 0) && (
                <Text ta="center" c="dimmed" py="xl">No employee data found.</Text>
            )}

        </Container>
    );
}
