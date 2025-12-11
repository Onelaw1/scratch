import { Container, Title, Text, SimpleGrid, Group, Button, Stack, Box } from '@mantine/core';
import { AppleCard } from '../components/AppleCard';

export default function Home() {
  return (
    <Box style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      padding: '4rem 0'
    }}>
      <Container size="lg">
        <Stack gap="xl" align="center" mb={50}>
          <Title
            order={1}
            style={{
              fontSize: '4rem',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              background: 'linear-gradient(180deg, #1a1a1a 0%, #4a4a4a 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Antigravity
          </Title>
          <Text size="xl" c="dimmed" style={{ maxWidth: 600, textAlign: 'center', fontSize: '1.5rem' }}>
            The next generation of consulting intelligence.
            Powered by Context7 and Mantine.
          </Text>
          <Group>
            <Button size="xl" radius="xl" variant="filled" color="black">Get Started</Button>
            <Button size="xl" radius="xl" variant="default">Documentation</Button>
          </Group>
        </Stack>

        <SimpleGrid cols={{ base: 1, sm: 2, md: 3 }} spacing="xl">
          <AppleCard
            title="MCP-First"
            description="Leveraging the Model Context Protocol for seamless tool integration and context awareness."
            action="Explore MCP"
          />
          <AppleCard
            title="Apple Aesthetics"
            description="Mantine UI customized with system fonts, glassmorphism, and subtle shadows."
            action="View Design"
          />
          <AppleCard
            title="Fast Backend"
            description="Optimized FastAPI architecture ensuring sub-millisecond response times."
            action="Check Performance"
          />
          <AppleCard
            title="Advanced Prompting"
            description="Chain of Thought and Persona-based reasoning for complex problem solving."
            action="Learn More"
          />
          <AppleCard
            title="Long-Term Memory"
            description="Persistent context retention across sessions for continuous intelligence."
            action="View Memory"
          />
          <AppleCard
            title="Visual Engine"
            description="Consulting-grade charts and diagrams generated automatically."
            action="See Visuals"
          />
        </SimpleGrid>
      </Container>
    </Box>
  );
}
