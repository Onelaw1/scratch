"use client";

import React, { useState } from "react";
import {
    Container, Title, Text, Paper, Group, Stack,
    Button, ThemeIcon, Slider, Textarea, ActionIcon,
    SimpleGrid, Transition, Badge
} from "@mantine/core";
import {
    IconMoodSad, IconMoodEmpty, IconMoodSmile, IconMoodHappy, IconMoodCrazyHappy,
    IconCheck, IconArrowLeft
} from "@tabler/icons-react";
import { notifications } from "@mantine/notifications";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

const MOODS = [
    { value: 1, icon: IconMoodSad, color: 'red', label: 'Stressed' },
    { value: 2, icon: IconMoodEmpty, color: 'orange', label: 'Anxious' },
    { value: 3, icon: IconMoodSmile, color: 'yellow', label: 'Okay' },
    { value: 4, icon: IconMoodHappy, color: 'lime', label: 'Good' },
    { value: 5, icon: IconMoodCrazyHappy, color: 'green', label: 'Great' },
];

const WORKLOAD_MARKS = [
    { value: 0, label: 'Low' },
    { value: 33, label: 'Normal' },
    { value: 66, label: 'High' },
    { value: 100, label: 'Overload' },
];

export default function PulseCheckPage() {
    const router = useRouter();
    const [mood, setMood] = useState<number | null>(null);
    const [workload, setWorkload] = useState(33); // Normal default
    const [note, setNote] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const getWorkloadLabel = (val: number) => {
        if (val <= 20) return "LOW";
        if (val <= 50) return "NORMAL";
        if (val <= 85) return "HIGH";
        return "OVERLOAD";
    };

    const handleSubmit = async () => {
        if (!mood) {
            notifications.show({ message: 'Please select a mood', color: 'red' });
            return;
        }

        setSubmitting(true);
        try {
            await api.submitPulseCheck({
                mood,
                workload: getWorkloadLabel(workload),
                note
            });
            notifications.show({ title: 'Logged', message: 'Thanks for your feedback!', color: 'green' });
            router.push("/my-job");
        } catch (e) {
            notifications.show({ title: 'Error', message: 'Failed to submit', color: 'red' });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <Container size="xs" p="md" className="bg-gray-50 min-h-screen">
            {/* Header */}
            <Group mb="xl">
                <ActionIcon variant="transparent" color="gray" onClick={() => router.back()}>
                    <IconArrowLeft />
                </ActionIcon>
                <div>
                    <Title order={3}>Daily Check-in</Title>
                    <Text size="xs" c="dimmed">Share how you're feeling today</Text>
                </div>
            </Group>

            {/* Mood Selector */}
            <Paper radius="lg" p="xl" className="bg-white shadow-sm mb-6 text-center">
                <Text fw={700} mb="lg">HOW ARE YOU FEELING?</Text>
                <Group justify="center" gap="lg" mb="md">
                    {MOODS.map((m) => (
                        <Stack key={m.value} align="center" gap={4}>
                            <ActionIcon
                                size={56}
                                radius="xl"
                                variant={mood === m.value ? 'filled' : 'subtle'}
                                color={m.color}
                                onClick={() => setMood(m.value)}
                                className="transition-transform active:scale-95"
                            >
                                <m.icon size={32} />
                            </ActionIcon>
                            <Text size="xs" fw={mood === m.value ? 700 : 400} c={mood === m.value ? m.color : 'dimmed'}>
                                {m.label}
                            </Text>
                        </Stack>
                    ))}
                </Group>
            </Paper>

            {/* Workload Slider */}
            <Paper radius="lg" p="xl" className="bg-white shadow-sm mb-6">
                <Group justify="space-between" mb="lg">
                    <Text fw={700}>WORKLOAD LEVEL</Text>
                    <Badge size="lg" variant="light" color={workload > 85 ? 'red' : 'blue'}>
                        {getWorkloadLabel(workload)}
                    </Badge>
                </Group>

                <div className="px-2 pb-6">
                    <Slider
                        value={workload}
                        onChange={setWorkload}
                        marks={WORKLOAD_MARKS}
                        step={10}
                        color={workload > 85 ? 'red' : 'blue'}
                        size="lg"
                    />
                </div>
            </Paper>

            {/* Note */}
            <Paper radius="lg" p="md" className="bg-white shadow-sm mb-8">
                <Textarea
                    placeholder="Anything else on your mind? (Optional)"
                    variant="unstyled"
                    minRows={3}
                    value={note}
                    onChange={(e) => setNote(e.target.value)}
                />
            </Paper>

            {/* Submit */}
            <Button
                fullWidth
                size="xl"
                radius="xl"
                color="dark"
                onClick={handleSubmit}
                loading={submitting}
                leftSection={<IconCheck />}
            >
                Log Check-in
            </Button>
        </Container>
    );
}
