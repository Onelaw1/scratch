"use client";

import { AppShell, Burger, Group, NavLink, ScrollArea, Text, ThemeIcon, SegmentedControl } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import {
    IconLayoutDashboard, IconSitemap, IconBriefcase, IconUsers,
    IconBrain, IconDeviceMobile, IconServer, IconChartDots, IconSchool,
    IconAnalyze, IconSettings, IconSearch, IconBulb, IconChartPie, IconTrendingUp
} from '@tabler/icons-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

// Navigation Data
type NavItem = {
    label?: string;
    labelKey?: string;
    icon: any;
    link?: string;
    links?: { label: string; labelKey?: string; link: string; icon?: any }[];
};

const NAV_ITEMS: NavItem[] = [
    { labelKey: 'nav.dashboard', icon: IconLayoutDashboard, link: '/' },

    {
        labelKey: 'nav.org_jobs', icon: IconSitemap, links: [
            { label: 'Job Classification', labelKey: 'nav.job_class', link: '/job-classification' },
            { label: 'Job Descriptions', labelKey: 'nav.job_desc', link: '/job-descriptions' },
            { label: 'Job Evaluation', labelKey: 'nav.job_eval', link: '/job-evaluation' },
            { label: 'Org Chart (Span)', labelKey: 'nav.span', link: '/admin/span-of-control', icon: IconSitemap },
        ]
    },

    {
        labelKey: 'nav.workforce', icon: IconAnalyze, links: [
            { label: 'Workforce Planning', labelKey: 'nav.wf_planning', link: '/workforce-planning' },
            { label: 'Workload Analysis', labelKey: 'nav.wl_analysis', link: '/workload-analysis' },
            { label: 'Simulation Board', labelKey: 'nav.sim_board', link: '/simulation' },
        ]
    },

    {
        labelKey: 'nav.personnel', icon: IconUsers, links: [
            { label: 'Personnel Records', labelKey: 'nav.personnel_rec', link: '/personnel-record' },
            { label: 'Performance Mgmt', labelKey: 'nav.perf_mgmt', link: '/performance-management' },
            { label: 'Career Development', labelKey: 'nav.career_dev', link: '/career-development' },
            { label: 'Talent Mapping (9-Box)', labelKey: 'nav.talent_map', link: '/scientific-hr/9-box', icon: IconChartDots },
            { label: 'Competency Radar', labelKey: 'nav.comp_radar', link: '/admin/competency', icon: IconBrain },
        ]
    },

    {
        labelKey: 'nav.ai_brain', icon: IconBrain, links: [
            { label: 'AI Semantic Search', labelKey: 'nav.ai_search', link: '/ai-search', icon: IconSearch },
            { label: 'JD Generator', labelKey: 'nav.jd_gen', link: '/jd-generator', icon: IconBulb },
            { label: 'Smart Gap Analysis', labelKey: 'nav.gap_analysis', link: '/smart-gap-analysis', icon: IconChartPie },
            { label: 'Predictive Analytics', labelKey: 'nav.pred_analytics', link: '/admin/prediction', icon: IconTrendingUp },
        ]
    },

    {
        labelKey: 'nav.emp_exp', icon: IconDeviceMobile, links: [
            { label: 'My Job (Mobile)', labelKey: 'nav.my_job', link: '/my-job' },
            { label: 'Job Survey (Input)', labelKey: 'nav.job_survey', link: '/job-survey' },
        ]
    },

    {
        labelKey: 'nav.admin', icon: IconServer, links: [
            { label: 'ERP Sync', labelKey: 'nav.erp_sync', link: '/admin/erp-sync' },
        ]
    },
];

export function Shell({ children }: { children: ReactNode }) {
    const [opened, { toggle }] = useDisclosure();
    const pathname = usePathname();
    const { language, toggleLanguage, t } = useLanguage();

    const isMobileView = pathname.startsWith('/my-job');

    // Mobile View: Hide Shell (Full screen app feel)
    if (isMobileView) {
        return <>{children}</>;
    }

    return (
        <AppShell
            header={{ height: 60 }}
            navbar={{ width: 300, breakpoint: 'sm', collapsed: { mobile: !opened } }}
            padding="md"
        >
            <AppShell.Header>
                <Group h="100%" px="md" justify="space-between">
                    <Group>
                        <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
                        <Group gap="xs">
                            <ThemeIcon content="gradient" gradient={{ from: 'violet', to: 'indigo' }} size="lg" radius="md">
                                <IconBriefcase size={20} />
                            </ThemeIcon>
                            <Text fw={700} size="lg" variant="gradient" gradient={{ from: 'violet', to: 'indigo' }}>
                                Job Management System
                            </Text>
                        </Group>
                    </Group>
                    <SegmentedControl
                        value={language}
                        onChange={toggleLanguage}
                        data={[
                            { label: '한글', value: 'ko' },
                            { label: 'EN', value: 'en' },
                        ]}
                        size="xs"
                        radius="xl"
                    />
                </Group>
            </AppShell.Header>

            <AppShell.Navbar p="md">
                <ScrollArea className="h-full">
                    <div className="space-y-1">
                        {NAV_ITEMS.map((item) => {
                            if (item.links) {
                                return (
                                    <NavLink
                                        key={item.labelKey || item.label}
                                        label={t(item.labelKey || '') || item.label}
                                        leftSection={<item.icon size="1rem" stroke={1.5} />}
                                        childrenOffset={28}
                                        defaultOpened
                                    >
                                        {item.links.map((sublink) => (
                                            <NavLink
                                                key={sublink.link}
                                                component={Link}
                                                href={sublink.link}
                                                label={t(sublink.labelKey || '') || sublink.label}
                                                active={pathname === sublink.link}
                                                leftSection={'icon' in sublink && sublink.icon ? <sublink.icon size="0.8rem" /> : null}
                                            />
                                        ))}
                                    </NavLink>
                                );
                            }
                            return (
                                <NavLink
                                    key={item.link}
                                    component={Link}
                                    href={item.link || '#'}
                                    label={t(item.labelKey || '') || item.label}
                                    leftSection={<item.icon size="1rem" stroke={1.5} />}
                                    active={pathname === item.link}
                                />
                            );
                        })}
                    </div>
                </ScrollArea>

                <div className="border-t border-gray-200 pt-4 mt-4">
                    <Text size="xs" c="dimmed" ta="center">v2.0 Enterprise Edition</Text>
                </div>
            </AppShell.Navbar>

            <AppShell.Main className="bg-gray-50/50 min-h-screen">
                {children}
            </AppShell.Main>
        </AppShell>
    );
}
