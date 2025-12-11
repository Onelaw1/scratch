import { AppShell, Group, Burger, Text, Button, Container } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

export function Header() {
    const [opened, { toggle }] = useDisclosure();

    return (
        <AppShell.Header
            withBorder={false}
            style={{
                background: 'rgba(0, 0, 0, 0.8)',
                backdropFilter: 'blur(10px)',
                WebkitBackdropFilter: 'blur(10px)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
            }}
        >
            <Container size="xl" h="100%">
                <Group h="100%" justify="space-between">
                    <Group>
                        <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" color="white" />
                        <Text fw={700} c="white" size="lg">Antigravity</Text>
                    </Group>

                    <Group visibleFrom="sm" gap="xl">
                        <Button variant="subtle" color="gray" c="dimmed">Store</Button>
                        <Button variant="subtle" color="gray" c="dimmed">Mac</Button>
                        <Button variant="subtle" color="gray" c="dimmed">iPad</Button>
                        <Button variant="subtle" color="gray" c="dimmed">iPhone</Button>
                        <Button variant="subtle" color="gray" c="dimmed">Watch</Button>
                        <Button variant="subtle" color="gray" c="dimmed">Vision</Button>
                        <Button variant="subtle" color="gray" c="dimmed">AirPods</Button>
                    </Group>

                    <Group>
                        <Button variant="filled" color="white" c="black" radius="xl" size="xs">Buy</Button>
                    </Group>
                </Group>
            </Container>
        </AppShell.Header>
    );
}
