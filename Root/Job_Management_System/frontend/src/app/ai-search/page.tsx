"use client";

import React, { useState } from "react";
import {
    Container, Title, Text, TextInput, Paper, Group, Stack, Badge,
    ThemeIcon, Loader, Transition, ActionIcon
} from "@mantine/core";
import {
    IconSearch, IconBrain, IconBriefcase, IconUser, IconFileDescription, IconArrowRight
} from "@tabler/icons-react";
import { useInputState, useDebouncedValue } from "@mantine/hooks";
import { api } from "@/lib/api";
import { useEffect } from "react";

export default function AiSearchPage() {
    const [query, setQuery] = useInputState("");
    const [debouncedQuery] = useDebouncedValue(query, 300);
    const [results, setResults] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (debouncedQuery.trim().length > 2) {
            handleSearch(debouncedQuery);
        } else {
            setResults([]);
        }
    }, [debouncedQuery]);

    const handleSearch = async (q: string) => {
        setLoading(true);
        try {
            const data = await api.getAiSearchResults(q);
            setResults(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const getTypeColor = (type: string) => {
        switch (type.toLowerCase()) {
            case 'task': return 'blue';
            case 'position': return 'teal';
            case 'job description': return 'grape';
            default: return 'gray';
        }
    };

    const getTypeIcon = (type: string) => {
        switch (type.toLowerCase()) {
            case 'task': return <IconBriefcase size={14} />;
            case 'position': return <IconUser size={14} />;
            case 'job description': return <IconFileDescription size={14} />;
            default: return <IconSearch size={14} />;
        }
    };

    return (
        <Container size="md" py="xl">
            {/* Header */}
            <div className="text-center mb-12">
                <ThemeIcon size={64} radius="xl" variant="gradient" gradient={{ from: 'indigo', to: 'cyan' }} className="mb-4">
                    <IconBrain size={32} />
                </ThemeIcon>
                <Title order={1} className="mb-2">AI Workforce Intelligence</Title>
                <Text c="dimmed" size="lg">Semantic Search across Jobs, Tasks, and Talent.</Text>
            </div>

            {/* Search Bar */}
            <Paper shadow="lg" radius="xl" p="xs" className="mb-8 border border-indigo-100 focus-within:ring-2 ring-indigo-200 transition-all">
                <TextInput
                    size="xl"
                    variant="unstyled"
                    placeholder="Ask anything... e.g., 'Leadership roles with data skills'"
                    value={query}
                    onChange={setQuery}
                    leftSection={<IconSearch size={22} className="text-gray-400" />}
                    rightSection={loading && <Loader size="sm" />}
                    classNames={{ input: 'pl-2' }}
                />
            </Paper>

            {/* Results */}
            <Stack gap="md">
                {results.map((item) => (
                    <Paper
                        key={`${item.type}-${item.id}`}
                        p="md"
                        radius="md"
                        withBorder
                        className="hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer group"
                    >
                        <Group justify="space-between" align="start">
                            <Group>
                                <ThemeIcon variant="light" color={getTypeColor(item.type)} size="lg" radius="md">
                                    {getTypeIcon(item.type)}
                                </ThemeIcon>
                                <div>
                                    <Group gap="xs">
                                        <Text fw={600} size="lg">{item.title}</Text>
                                        <Badge variant="outline" size="sm" color={getTypeColor(item.type)}>{item.type}</Badge>
                                    </Group>
                                    <Text c="dimmed" size="sm" mt={2}>{item.description}</Text>
                                </div>
                            </Group>

                            <Group>
                                <Badge variant="dot" color={item.score > 0.5 ? 'green' : 'yellow'}>
                                    Match: {Math.round(item.score * 100)}%
                                </Badge>
                                <ActionIcon variant="subtle" color="gray" className="opacity-0 group-hover:opacity-100 transition-opacity">
                                    <IconArrowRight size={18} />
                                </ActionIcon>
                            </Group>
                        </Group>
                    </Paper>
                ))}

                {results.length === 0 && query.length > 0 && !loading && (
                    <div className="text-center py-12 text-gray-400">
                        <Text>No semantic matches found.</Text>
                    </div>
                )}
            </Stack>
        </Container>
    );
}
