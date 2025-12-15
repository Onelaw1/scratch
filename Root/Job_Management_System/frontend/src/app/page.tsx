"use client";

import { Container, Title, SimpleGrid, Card, Text, Button, Group, List, ThemeIcon, Badge } from "@mantine/core";
import { IconChartPie, IconBriefcase, IconUsers, IconBrain, IconScale, IconGavel, IconCertificate, IconRobot, IconChartBar, IconTrophy, IconListNumbers, IconCalculator, IconRefresh, IconMap, IconSitemap, IconGridDots, IconHierarchy, IconRadar } from "@tabler/icons-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <Container size="lg" py="xl">
      <Group justify="space-between" mb="xl">
        <Title order={1}>Job Management System</Title>
        <Button variant="light">Settings</Button>
      </Group>

      <SimpleGrid cols={{ base: 1, sm: 2, lg: 3 }} spacing="lg">
        {/* Existing Cards */}
        <Card withBorder padding="lg">
          <Title order={3} mb="sm">Job Analysis</Title>
          <Text size="sm" c="dimmed" mb="md">
            Conduct time studies and workload analysis.
          </Text>
          <Button component={Link} href="/job-survey" fullWidth>
            Go to Survey
          </Button>
        </Card>

        <Card withBorder padding="lg">
          <Title order={3} mb="sm">Workload Analysis</Title>
          <Text size="sm" c="dimmed" mb="md">
            Analyze FTE, Standard Time, and ROI.
          </Text>
          <Button component={Link} href="/workload-analysis" fullWidth>
            View Dashboard
          </Button>
        </Card>

        <Card withBorder padding="lg">
          <Title order={3} mb="sm">Job Classification</Title>
          <Text size="sm" c="dimmed" mb="md">
            Manage job hierarchy and descriptions.
          </Text>
          <Button component={Link} href="/job-classification" fullWidth>
            Manage Jobs
          </Button>
        </Card>

        <Card withBorder padding="lg">
          <Title order={3} mb="sm">Productivity Analytics</Title>
          <Text size="sm" c="dimmed" mb="md">
            View HCROI and HCVA metrics.
          </Text>
          <Button component={Link} href="/productivity" fullWidth>
            View Metrics
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Classification AI</Text>
            <Badge color="pink" variant="light">Beta</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            AI-driven job classification and analysis.
          </Text>
          <Button component={Link} href="/classification-ai" fullWidth variant="light" color="pink">
            AI Assistant
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Fairness Check</Text>
            <Badge color="orange" variant="light">Compliance</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Verification of equal pay and non-discrimination.
          </Text>
          <Button component={Link} href="/admin/fairness" fullWidth variant="light" color="orange">
            Run Audit
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>AI Prediction</Text>
            <Badge color="violet" variant="light">Future</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Predict future role demand and skills.
          </Text>
          <Button component={Link} href="/admin/prediction" fullWidth variant="light" color="violet">
            View Forecast
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Global HR</Text>
            <Badge color="cyan" variant="light">Global</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Multi-currency and global policy management.
          </Text>
          <Button component={Link} href="/admin/global" fullWidth variant="light" color="cyan">
            Global Settings
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Digital Wallet</Text>
            <Badge color="indigo" variant="light">Blockchain</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Verifiable Career & Experience Certificates.
          </Text>
          <Button component={Link} href="/my-job/certificate" fullWidth variant="light" color="indigo">
            My Wallet
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Job Calibration Bot</Text>
            <Badge color="red" variant="light">Drift</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Detect workload drift and suggest upgrades.
          </Text>
          <Button component={Link} href="/admin/calibration" fullWidth variant="light" color="red">
            Check Drift
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Growth Integral</Text>
            <Badge color="teal" variant="light">Longitudinal</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            View long-term performance consistency (Area).
          </Text>
          <Button component={Link} href="/admin/performance-integral" fullWidth variant="light" color="teal">
            View Integral
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Promotion Game</Text>
            <Badge color="grape" variant="light">Sim</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Tenure vs. Growth Slope Simulation.
          </Text>
          <Button component={Link} href="/admin/promotion-sim" fullWidth variant="light" color="grape">
            Run Simulation
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Promotion Ranker</Text>
            <Badge color="dark" variant="filled">Official</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Generate binding Scientific Promotion List (SPS).
          </Text>
          <Button component={Link} href="/admin/rank" fullWidth variant="filled" color="dark">
            Open Register
          </Button>
        </Card>

        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Workforce Optimizer</Text>
            <Badge color="orange" variant="filled">TO Calc</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Calculate Required FTE using Standard Time.
          </Text>
          <Button component={Link} href="/admin/optimal-workforce" fullWidth variant="outline" color="orange">
            Calculate TO
          </Button>
        </Card>

        {/* Phase 8: Dynamic JD */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Dynamic JD Generator</Text>
            <Badge color="blue" variant="filled">Living JD</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Auto-update JDs based on Workload Logs.
          </Text>
          <Button component={Link} href="/admin/dynamic-jd" fullWidth variant="outline" color="blue">
            Sync JD
          </Button>
        </Card>

        {/* Phase 8: R&R Conflict */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>R&R Conflict Map</Text>
            <Badge color="red" variant="filled">Gap/Dup</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Visualize Duplication & Gaps in R&R.
          </Text>
          <Button component={Link} href="/admin/r-and-r" fullWidth variant="outline" color="red">
            View Matrix
          </Button>
        </Card>

        {/* Phase 8.5: RACI Chart */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>RACI Generator</Text>
            <Badge color="cyan" variant="filled">Toolkit</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Auto-generate Responsibility Matrix (R/A/C/I).
          </Text>
          <Button component={Link} href="/admin/raci" fullWidth variant="outline" color="cyan">
            View RACI
          </Button>
        </Card>

        {/* Phase 8.5: 9-Box Grid */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>9-Box Grid</Text>
            <Badge color="teal" variant="filled">Talent</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Visualize Performance vs. Potential Matrix.
          </Text>
          <Button component={Link} href="/admin/9-box" fullWidth variant="outline" color="teal">
            View Talent Map
          </Button>
        </Card>

        {/* Phase 8.5: Span of Control */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Span of Control</Text>
            <Badge color="pink" variant="filled">Org</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Analyze Org Depth & Manager Reports.
          </Text>
          <Button component={Link} href="/admin/span-of-control" fullWidth variant="outline" color="pink">
            Analyze Structure
          </Button>
        </Card>

        {/* Phase 8.6: Competency Fit Radar */}
        <Card withBorder padding="lg" radius="md">
          <Group justify="space-between" mb="xs">
            <Text fw={500}>Competency Radar</Text>
            <Badge color="indigo" variant="filled">Soft HR</Badge>
          </Group>
          <Text size="sm" c="dimmed" mb="md">
            Job-Person Fit Radar & Gap Analysis.
          </Text>
          <Button component={Link} href="/admin/competency" fullWidth variant="outline" color="indigo">
            View Fit
          </Button>
        </Card>

      </SimpleGrid>
    </Container>
  );
}
