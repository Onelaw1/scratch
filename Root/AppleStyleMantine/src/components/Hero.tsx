import { Container, Title, Text, Button, Group, Stack } from '@mantine/core';

export function Hero() {
    return (
        <Container size="xl" py={120}>
            <Stack align="center" gap="xl">
                <Title
                    order={1}
                    style={{
                        fontSize: '4rem',
                        fontWeight: 700,
                        letterSpacing: '-0.02em',
                        lineHeight: 1.1,
                        textAlign: 'center',
                        color: '#f5f5f7'
                    }}
                >
                    Pro. Beyond.
                </Title>
                <Text
                    size="xl"
                    c="dimmed"
                    maw={600}
                    ta="center"
                    style={{ fontSize: '1.5rem', lineHeight: 1.4 }}
                >
                    A mind-blowing chip. A massive leap in battery life. And a camera system that captures it all.
                </Text>

                <Group mt="xl">
                    <Button size="lg" variant="filled" color="blue" radius="xl">
                        Buy Now
                    </Button>
                    <Button size="lg" variant="outline" color="blue" radius="xl">
                        Learn More
                    </Button>
                </Group>
            </Stack>
        </Container>
    );
}
