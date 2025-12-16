"use client";

import { AppShell, Burger, Group, NavLink, ScrollArea, Text, ThemeIcon, SegmentedControl } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import {
    IconBrain, IconDeviceMobile, IconServer, IconChartDots, IconSchool,
    IconAnalyze, IconSettings, IconSearch, IconBulb, IconChartPie, IconTrendingUp,
    IconSchema, IconLayoutDashboard, IconSitemap, IconBriefcase, IconUsers, IconFileDescription, IconClipboardCheck
} from '@tabler/icons-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';
import { useLanguage } from '@/contexts/LanguageContext';

// Navigation Data
type NavItem = {
    label?: string;
    labelKey?: string;
    icon?: any;
    link?: string;
    links?: NavItem[];
};

const NAV_ITEMS: NavItem[] = [
    { label: '대시보드', labelKey: 'nav.dashboard', icon: IconLayoutDashboard, link: '/analytics/dashboard' },
    { label: '시스템 개요', labelKey: 'nav.overview', icon: IconSchema, link: '/system-overview' },

    {
        label: '직무 관리 흐름', labelKey: 'nav.workflow', icon: IconTrendingUp, links: [
            { label: '1. 직무 기술서', labelKey: 'nav.job_desc', link: '/job-descriptions', icon: IconFileDescription },
            { label: '2. 직무 분류', labelKey: 'nav.job_class', link: '/job-classification', icon: IconSitemap },
            { label: '3. 적정 인력', labelKey: 'nav.workload', link: '/workload-analysis', icon: IconChartPie },
            {
                label: '4. 직무 평가',
                labelKey: 'nav.job_eval',
                icon: IconClipboardCheck,
                links: [
                    { label: '개별 평가', link: '/evaluation/rate/demo-job-001' },
                    { label: '종합 매트릭스', link: '/evaluation/matrix' }
                ]
            },
        ]
    },

    {
        label: '분석 및 최적화', labelKey: 'nav.analytics', icon: IconAnalyze, links: [
            { label: '전략 대시보드', labelKey: 'nav.strat_dash', link: '/analytics/dashboard', icon: IconLayoutDashboard },
            { label: '조직 구조 분석', labelKey: 'nav.span', link: '/admin/span-of-control', icon: IconUsers },
            { label: 'AI 시맨틱 검색', labelKey: 'nav.ai_search', link: '/ai-search', icon: IconSearch },
            { label: '예측 분석', labelKey: 'nav.pred', link: '/admin/prediction', icon: IconBrain },
        ]
    },

    {
        label: '직원 경험', labelKey: 'nav.emp_exp', icon: IconDeviceMobile, links: [
            { label: '나의 직무 관리', labelKey: 'nav.my_job', link: '/my-job' },
            { label: '직무 조사', labelKey: 'nav.job_survey', link: '/job-survey' },
        ]
    },

    {
        label: '관리자', labelKey: 'nav.admin', icon: IconServer, links: [
            { label: 'ERP 데이터 연동', labelKey: 'nav.erp_sync', link: '/admin/erp-sync' },
            { label: '사용자 권한 관리', labelKey: 'nav.permissions', link: '/admin/permissions', icon: IconUsers },
        ]
    },
];

export function Shell({ children }: { children: ReactNode }) {
    const [opened, { toggle }] = useDisclosure();
    const pathname = usePathname();
    const { language, toggleLanguage, t } = useLanguage();

    const isMobileView = pathname.startsWith('/my-job');

    if (isMobileView) {
        return <>{children}</>;
    }

    const renderNavItem = (item: any) => {
        if (item.links && item.links.length > 0) {
            return (
                <NavLink
                    key={item.labelKey || item.label}
                    label={t(item.labelKey || '') || item.label}
                    leftSection={item.icon ? <item.icon size="1rem" stroke={1.5} /> : null}
                    childrenOffset={28}
                    defaultOpened
                >
                    {item.links.map(renderNavItem)}
                </NavLink>
            );
        }

        return (
            <NavLink
                key={item.link || item.label}
                component={Link}
                href={item.link || '#'}
                label={t(item.labelKey || '') || item.label}
                leftSection={item.icon ? <item.icon size="1rem" stroke={1.5} /> : null}
                active={pathname === item.link}
            />
        );
    };

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
                        {NAV_ITEMS.map(renderNavItem)}
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
