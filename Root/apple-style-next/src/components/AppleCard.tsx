import { Paper, Text, Title, Button, Group, ThemeIcon } from '@mantine/core';
import { IconApple } from '@tabler/icons-react';

interface AppleCardProps {
    title: string;
    description: string;
    action?: string;
}

export function AppleCard({ title, description, action = "Learn more" }: AppleCardProps) {
    return (
        <Paper
            p="xl"
            radius="xl"
            style={{
                background: 'rgba(255, 255, 255, 0.8)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.3)',
                boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.07)',
            }}
        >
            <ThemeIcon size={48} radius="md" variant="light" color="gray" mb="lg">
                <IconApple size={24} />
            </ThemeIcon>

            <Title order={3} mb="xs" style={{ fontWeight: 600, letterSpacing: '-0.02em' }}>
                {title}
            </Title>

            <Text c="dimmed" mb="xl" size="sm" style={{ lineHeight: 1.6 }}>
                {description}
            </Text>

            <Button variant="light" radius="xl" size="md">
                {action}
            </Button>
        </Paper>
    );
}
