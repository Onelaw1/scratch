"use client";

import { useState } from 'react';
import { Container, Paper, Title, Text, TextInput, Button, Group, Image, ThemeIcon, Stack } from '@mantine/core';
import { IconAtom, IconLock } from '@tabler/icons-react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
    const router = useRouter();
    const [empId, setEmpId] = useState('');

    const handleLogin = () => {
        // Mock Login
        if (typeof window !== 'undefined') {
            localStorage.setItem('currentUser', JSON.stringify({ id: empId || 'USER001', name: '홍길동' }));
        }
        router.push('/system-overview');
    };

    return (
        <div className="min-h-screen bg-slate-900 flex items-center justify-center relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500 rounded-full blur-[100px]" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500 rounded-full blur-[100px]" />
            </div>

            <Container size="xs" style={{ zIndex: 1 }}>
                <Paper p="xl" radius="lg" shadow="xl" withBorder className="bg-white/95 backdrop-blur-sm">
                    <Stack align="center" mb="xl">
                        <ThemeIcon size={80} radius="full" variant="gradient" gradient={{ from: 'indigo', to: 'cyan' }}>
                            <IconAtom size={40} />
                        </ThemeIcon>
                        <Title order={2} ta="center" mt="sm">KORAD JMS</Title>
                        <Text c="dimmed" size="sm">직무 관리 시스템 (Job Management System)</Text>
                    </Stack>

                    <Stack>
                        <TextInput
                            label="사번 (Employee ID)"
                            placeholder="사번을 입력하세요 (예: 12345)"
                            leftSection={<IconLock size={16} />}
                            value={empId}
                            onChange={(e) => setEmpId(e.target.value)}
                        />

                        <Button fullWidth size="lg" variant="gradient" gradient={{ from: 'indigo', to: 'cyan' }} onClick={handleLogin}>
                            로그인
                        </Button>

                        <Text size="xs" c="dimmed" ta="center" mt="xs">
                            * 데모 버전입니다. 아무 번호나 입력하여 진행하세요.
                        </Text>
                    </Stack>
                </Paper>
            </Container>
        </div>
    );
}
