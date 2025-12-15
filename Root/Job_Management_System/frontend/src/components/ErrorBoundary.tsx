"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { Center, Paper, Title, Text, Button, ThemeIcon, Container } from "@mantine/core";
import { IconAlertTriangle, IconRefresh } from "@tabler/icons-react";

interface Props {
    children?: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error("Uncaught error:", error, errorInfo);
    }

    public render() {
        if (this.state.hasError) {
            return (
                <Center h="100vh" bg="gray.1">
                    <Paper p="xl" radius="lg" withBorder shadow="lg" className="text-center max-w-md">
                        <ThemeIcon size={80} radius="xl" color="red" variant="light" className="mb-6 mx-auto">
                            <IconAlertTriangle size={48} />
                        </ThemeIcon>
                        <Title order={2} className="mb-2">Something went wrong</Title>
                        <Text c="dimmed" mb="lg">
                            The application encountered an unexpected error.
                            Our team has been notified.
                        </Text>
                        <Button
                            size="md"
                            variant="outline"
                            color="red"
                            leftSection={<IconRefresh size={20} />}
                            onClick={() => window.location.reload()}
                        >
                            Reload Application
                        </Button>
                        {this.state.error && (
                            <Text size="xs" c="dimmed" mt="lg" className="font-mono bg-gray-50 p-2 rounded">
                                {this.state.error.toString()}
                            </Text>
                        )}
                    </Paper>
                </Center>
            );
        }

        return this.props.children;
    }
}
