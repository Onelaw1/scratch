import { SimpleGrid, Card, Image, Text, Container, Title } from '@mantine/core';

const mockdata = [
    {
        title: 'Titanium Design',
        image: 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&q=80&w=800&h=600',
        date: 'Stronger. Lighter. Pro.',
    },
    {
        title: 'A17 Pro Chip',
        image: 'https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?auto=format&fit=crop&q=80&w=800&h=600',
        date: 'Monster win for gaming.',
    },
    {
        title: 'New Camera System',
        image: 'https://images.unsplash.com/photo-1696446701796-da61225697cc?auto=format&fit=crop&q=80&w=800&h=600',
        date: 'Megapixel massive.',
    },
    {
        title: 'Action Button',
        image: 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&q=80&w=800&h=600',
        date: 'Fast track to your favorite feature.',
    },
];

export function Features() {
    const cards = mockdata.map((article) => (
        <Card key={article.title} p="xl" radius="lg" style={{ backgroundColor: '#1d1d1f', border: 'none' }}>
            <Card.Section>
                <Image
                    src={article.image}
                    height={300}
                    alt={article.title}
                    style={{ objectFit: 'cover' }}
                />
            </Card.Section>

            <Text fw={700} size="xl" mt="md" c="white">
                {article.title}
            </Text>

            <Text size="md" c="dimmed" mt="xs">
                {article.date}
            </Text>
        </Card>
    ));

    return (
        <Container size="xl" py="xl">
            <Title order={2} mb="xl" c="white" style={{ fontSize: '3rem' }}>Highlights.</Title>
            <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="xl">
                {cards}
            </SimpleGrid>
        </Container>
    );
}
