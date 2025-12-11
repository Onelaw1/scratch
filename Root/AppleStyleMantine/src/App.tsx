import { AppShell, Box } from '@mantine/core';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { Features } from './components/Features';

function App() {
  return (
    <AppShell header={{ height: 60 }} padding={0}>
      <Header />
      <AppShell.Main>
        <Box bg="#000000" c="white" style={{ minHeight: '100vh' }}>
          <Hero />
          <Features />
        </Box>
      </AppShell.Main>
    </AppShell>
  );
}

export default App;
