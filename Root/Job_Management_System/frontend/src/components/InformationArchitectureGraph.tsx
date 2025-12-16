
"use client";

import { Card, Group, Title, ThemeIcon, Text, Badge, Paper, Box, Stack, Divider, Grid, RingProgress, Center } from '@mantine/core';
import { IconSchema, IconId, IconSchool, IconCertificate, IconTools, IconClipboardList, IconArrowRight, IconLink, IconCheck, IconSitemap, IconBriefcase, IconChartPie } from '@tabler/icons-react';
import { motion } from 'framer-motion';

// --- DATA STRUCTURES ---

interface EntityField {
  name: string;
  val: string;
  icon?: any;
  isKey?: boolean;
  isLink?: boolean;
}

interface EntityCardData {
  id: string;
  title: string;
  subtitle: string;
  color: string;
  x: number;
  y: number;
  w: number;
  h: number;
  sections: {
    label: string;
    fields: EntityField[];
  }[];
}

interface LinkData {
  from: string;
  fromPort: 'right' | 'bottom';
  to: string;
  toPort: 'left' | 'top';
  label: string;
  dashed?: boolean;
}

// --- CONFIGURATION ---

const CARD_W = 280;
const CARD_H = 320;

const ENTITIES: EntityCardData[] = [
  // 1. JOB CLASSIFICATION (The Hierarchy)
  {
    id: 'job_class', title: 'Job Classification', subtitle: 'Org Structure Definition', color: 'indigo',
    x: 20, y: 50, w: CARD_W, h: CARD_H,
    sections: [
      {
        label: 'Hierarchy Keys',
        fields: [
          { name: 'Job Group', val: 'IT / R&D', isKey: true, icon: IconId },
          { name: 'Job Series', val: 'SW Engineering', isKey: true },
          { name: 'Job Position', val: 'Senior Backend Dev', isKey: true, isLink: true },
        ]
      },
      {
        label: 'Attributes',
        fields: [
          { name: 'Grade Level', val: 'Lvl 4 (Lead)' },
          { name: 'Managerial', val: 'Yes' },
        ]
      }
    ]
  },

  // 2. JOB DESCRIPTION (The Standard Spec)
  {
    id: 'job_desc', title: 'Job Description', subtitle: 'Requirements & Standards', color: 'blue',
    x: 460, y: 50, w: CARD_W, h: CARD_H + 40, // Taller
    sections: [
      {
        label: 'Task Standards',
        fields: [
          { name: 'NCS Code', val: 'SW-Eng-2024-01', icon: IconClipboardList },
          { name: 'Difficulty', val: 'High (Expert)' },
        ]
      },
      {
        label: 'Requirements (The Bar)',
        fields: [
          { name: 'Min Degree', val: 'Bachelor (BS)', icon: IconSchool, isLink: true },
          { name: 'Target Major', val: 'Comp Sci / Math', isLink: true },
          { name: 'Core Skill', val: 'Python, System Design', icon: IconTools, isLink: true },
        ]
      }
    ]
  },

  // 3. HUMAN CAPITAL (The Asset)
  {
    id: 'human_cap', title: 'Human Capital', subtitle: 'Employee Profile (Asset)', color: 'teal',
    x: 900, y: 50, w: CARD_W, h: CARD_H + 40,
    sections: [
      {
        label: 'Identity',
        fields: [
          { name: 'User ID', val: 'EMP-00921', isKey: true, icon: IconId },
          { name: 'Hire Date', val: '2021-03-15' },
        ]
      },
      {
        label: 'Possessed Specs',
        fields: [
          { name: 'Education', val: 'Master (MS)', icon: IconSchool, isLink: true },
          { name: 'Major', val: 'Computer Science', isLink: true },
          { name: 'Skill Set', val: 'Python, AWS, React', icon: IconTools, isLink: true },
          { name: 'Certifications', val: 'AWS Sol. Arch.', icon: IconCertificate },
        ]
      }
    ]
  }
];

const LINKS: LinkData[] = [
  { from: 'job_class', fromPort: 'right', to: 'job_desc', toPort: 'left', label: 'Defines Spec' },
  { from: 'job_desc', fromPort: 'right', to: 'human_cap', toPort: 'left', label: 'Competency Fit Analysis', dashed: true },
];

// --- COMPONENT ---

export function InformationArchitectureGraph() {
  // CONFIG
  const CARD_W = 200;
  const CARD_H = 140; // Smaller formatting for granular cards
  const GAP_X = 80;
  const GAP_Y = 80;

  // NODES (3-Depth Granularity)
  const NODES = [
    // ROW 1: Definition
    {
      id: 'jg', title: 'Job Group', sub: 'Classification', x: 50, y: 50, color: 'indigo', icon: IconSitemap,
      details: ['Code: JG_001', 'Type: Corp/Field']
    },
    {
      id: 'js', title: 'Job Series', sub: 'Standardization', x: 50 + (CARD_W + GAP_X), y: 50, color: 'indigo', icon: IconSitemap,
      details: ['NCS Integration', 'Competency Unit']
    },
    {
      id: 'jp', title: 'Job Position', sub: 'The Core Anchor', x: 50 + (CARD_W + GAP_X) * 2, y: 50, color: 'blue', icon: IconBriefcase, isMain: true,
      details: ['Grade: G1-G5', 'JD: Versioned', 'KPIs: Linked']
    },

    // ROW 2: Description & Tasks
    {
      id: 'task', title: 'Job Task', sub: 'NCS / R&R', x: 50 + (CARD_W + GAP_X) * 3, y: 50, color: 'cyan', icon: IconClipboardList,
      details: ['Freq: D/W/M/Y', 'Diff: 1-5', 'Skill: Python']
    },

    // ROW 3: Human Side
    {
      id: 'user', title: 'User (Employee)', sub: 'Human Capital', x: 50 + (CARD_W + GAP_X) * 2, y: 50 + (CARD_H + GAP_Y), color: 'teal', icon: IconId,
      details: ['Tenure: Dual', 'Skills: Verified', 'Edu: Degree']
    },

    // ROW 4: Analytics & Evaluation
    {
      id: 'load', title: 'Workload (FTE)', sub: 'Survey Data', x: 50 + (CARD_W + GAP_X) * 3, y: 50 + (CARD_H + GAP_Y), color: 'green', icon: IconChartPie,
      details: ['Time: Annual', 'FTE: < 1.0', 'Volume: #']
    },
    {
      id: 'eval', title: 'Job Evaluation', sub: 'Grading & Comp', x: 50 + (CARD_W + GAP_X) * 2, y: 50 - (CARD_H + GAP_Y), color: 'grape', icon: IconCertificate,
      details: ['Score: 0-100', 'Matrix: 9-Box', 'Impact: Pay']
    },
  ];

  // EDGES (With Backlinks)
  const EDGES = [
    { from: 'jg', to: 'js', label: 'Includes' },
    { from: 'js', to: 'jp', label: 'Defines' },
    { from: 'jp', to: 'task', label: 'Consists of' },
    { from: 'user', to: 'jp', label: 'Assigned to' },
    { from: 'user', to: 'load', label: 'Reports' },
    { from: 'load', to: 'task', label: 'Measures', dashed: true },
    { from: 'eval', to: 'jp', label: 'Rates', color: 'grape' },

    // Backlinks (User Feedback)
    { from: 'jp', to: 'js', label: 'Extends', dashed: true, color: 'orange', backlink: true },
    { from: 'task', to: 'jp', label: 'Aggregates', dashed: true, color: 'orange', backlink: true },
    { from: 'load', to: 'user', label: 'Feedback', dashed: true, color: 'orange', backlink: true },
  ];

  return (
    <Card p="xl" radius="lg" withBorder bg="white" mb="xl">
      <Group justify="space-between" mb="lg">
        <Group>
          <ThemeIcon size="xl" radius="md" color="dark" variant="filled">
            <IconSchema size={28} />
          </ThemeIcon>
          <div>
            <Title order={2}>Total Data Entity Map (3-Depth)</Title>
            <Text c="dimmed">Full Granularity: Classification structure, Task details, Workload links, Job Evaluation, and Backlinks.</Text>
          </div>
        </Group>
        <Badge size="lg" color="dark" variant="light">Live Schema</Badge>
      </Group>

      <Paper withBorder bg="gray.0" style={{ height: 600, position: 'relative', overflow: 'hidden' }}>
        <svg width="100%" height="100%" viewBox="0 0 1200 600">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#adb5bd" />
            </marker>
            <marker id="arrowhead-grape" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#be4bdb" />
            </marker>
            <marker id="arrowhead-orange" markerWidth="10" markerHeight="7" refX="28" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#fd7e14" />
            </marker>
          </defs>

          {/* EDGES */}
          {EDGES.map((edge, i) => {
            const s = NODES.find(n => n.id === edge.from)!;
            const t = NODES.find(n => n.id === edge.to)!;

            // Center-to-Center logic roughly, or specific ports? Let's do simple center-nearest.
            // Actually, let's hardcode ports for cleaner lines.
            // Simplified: Center to Center
            const sx = s.x + CARD_W / 2;
            const sy = s.y + CARD_H / 2;
            const tx = t.x + CARD_W / 2;
            const ty = t.y + CARD_H / 2;

            const path = "M " + sx + " " + sy + " L " + tx + " " + ty;

            return (
              <g key={i}>
                <motion.path
                  d={path}
                  fill="none"
                  stroke={edge.color === 'grape' ? '#be4bdb' : edge.color === 'orange' ? '#fd7e14' : '#adb5bd'}
                  strokeWidth={2}
                  strokeDasharray={edge.dashed ? "5,5" : "0"}
                  markerEnd={edge.color === 'grape' ? "url(#arrowhead-grape)" : edge.color === 'orange' ? "url(#arrowhead-orange)" : "url(#arrowhead)"}
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ duration: 0.8, delay: 0.2 + (i * 0.1) }}
                />
                <foreignObject x={(sx + tx) / 2 - 40} y={(sy + ty) / 2 - 10} width="80" height="20">
                  <Center bg="white" style={{ borderRadius: 4, border: '1px solid #eee' }}>
                    <Text size="8px" fw={700} c="dimmed">{edge.label}</Text>
                  </Center>
                </foreignObject>
              </g>
            )
          })}

          {/* NODES */}
          {NODES.map((node, i) => (
            <foreignObject key={node.id} x={node.x} y={node.y} width={CARD_W} height={CARD_H}>
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
              >
                <Paper
                  shadow={node.isMain ? "xl" : "sm"}
                  radius="md"
                  p="sm"
                  withBorder
                  style={{
                    height: '100%',
                    borderColor: node.isMain ? '#339af0' : '#dee2e6',
                    borderWidth: node.isMain ? 2 : 1,
                    background: 'white'
                  }}
                >
                  <Stack gap="xs" align="center" justify="center" h="100%">
                    <ThemeIcon color={node.color} size="lg" radius="xl" variant="light">
                      <node.icon size={20} />
                    </ThemeIcon>
                    <div style={{ textAlign: 'center' }}>
                      <Text fw={700} size="sm" c="dark.8">{node.title}</Text>
                      <Text size="xs" c="dimmed">{node.sub}</Text>
                    </div>
                    {/* 3rd Depth Details */}
                    {node.details && (
                      <Group gap={4} justify="center" mt={4} style={{ flexWrap: 'wrap' }}>
                        {node.details.map((d: string) => (
                          <Badge key={d} size="xs" variant="outline" color={node.color} style={{ fontSize: 9, height: 16 }}>{d}</Badge>
                        ))}
                      </Group>
                    )}
                  </Stack>
                </Paper>
              </motion.div>
            </foreignObject>
          ))}
        </svg>
      </Paper>
    </Card>
  );
}

