"use client";

import { useState } from 'react';
import { Modal, TextInput, Select, NumberInput, Button, Stack, Text, Title, Group, Slider, ThemeIcon, Progress, Card, Badge } from '@mantine/core';
import { IconBuilding, IconUser, IconClock, IconBriefcase, IconArrowRight } from '@tabler/icons-react';

interface UserProfile {
    company: string;
    department: string;
    name: string;
    position: string;
    baseHours: number;
    overtimeHours: number; // Annual
}

interface UserOnboardingProps {
    onComplete: (profile: UserProfile) => void;
    opened: boolean;
}

export function UserOnboarding({ onComplete, opened }: UserOnboardingProps) {
    const [step, setStep] = useState(1);
    const [profile, setProfile] = useState<UserProfile>({
        company: '한국원자력환경공단(KORAD)',
        department: '',
        name: '',
        position: '',
        baseHours: 2080, // Standard 40h * 52w
        overtimeHours: 0
    });

    const handleNext = () => {
        if (step === 1) {
            if (!profile.department || !profile.name || !profile.position) return; // Validation
            setStep(2);
        } else {
            onComplete(profile);
        }
    };

    return (
        <Modal
            opened={opened}
            onClose={() => { }}
            withCloseButton={false}
            size="lg"
            centered
            overlayProps={{
                backgroundOpacity: 0.55,
                blur: 3,
            }}
        >
            <div className="p-4">
                {step === 1 ? (
                    <Stack gap="lg">
                        <div className="text-center mb-4">
                            <ThemeIcon size={60} radius="full" variant="light" color="blue" className="mb-4">
                                <IconUser size={30} />
                            </ThemeIcon>
                            <Title order={2}>나의 직무 프로필 설정</Title>
                            <Text c="dimmed">정확한 직무 분석을 위해 기본 정보를 입력해주세요.</Text>
                        </div>

                        <TextInput
                            label="회사"
                            value={profile.company}
                            readOnly
                            leftSection={<IconBuilding size={16} />}
                        />

                        <Select
                            label="소속 (본부/실/팀)"
                            placeholder="소속 부서를 선택하세요"
                            data={[
                                '중저준위운영실', '중저준위기획실', '중저준위안전실',
                                '고준위기획실', '고준위기술개발원',
                                '품질안전단', '소통협력단', '경영관리실'
                            ]}
                            value={profile.department}
                            onChange={(v) => setProfile({ ...profile, department: v || '' })}
                            leftSection={<IconBriefcase size={16} />}
                            searchable
                        />

                        <Group grow>
                            <TextInput
                                label="이름"
                                placeholder="성명 입력"
                                value={profile.name}
                                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                            />
                            <Select
                                label="직급"
                                placeholder="선택"
                                data={['본부장', '실장', '팀장', '차장', '과장', '대리', '사원']}
                                value={profile.position}
                                onChange={(v) => setProfile({ ...profile, position: v || '' })}
                            />
                        </Group>

                        <Button fullWidth size="lg" onClick={handleNext} mt="md" rightSection={<IconArrowRight size={18} />}>
                            다음: 근무 시간 설정
                        </Button>
                    </Stack>
                ) : (
                    <Stack gap="lg">
                        <div className="text-center mb-4">
                            <ThemeIcon size={60} radius="full" variant="light" color="orange" className="mb-4">
                                <IconClock size={30} />
                            </ThemeIcon>
                            <Title order={2}>연간 근무 시간 설정</Title>
                            <Text c="dimmed">작년 한 해 동안의 대략적인 총 근무 시간을 설정합니다.</Text>
                        </div>

                        <Card withBorder padding="lg" radius="md" bg="gray.0">
                            <Group justify="space-between" mb="xs">
                                <Text fw={600}>기본 근무 시간</Text>
                                <Text fw={700}>2,080 시간</Text>
                            </Group>
                            <Text size="xs" c="dimmed">주 40시간 × 52주</Text>
                        </Card>

                        <div>
                            <Group justify="space-between" mb="xs">
                                <Text fw={600}>월 평균 야근 시간</Text>
                                <Badge size="lg" variant="filled" color="orange">{Math.round(profile.overtimeHours / 12)} 시간 / 월</Badge>
                            </Group>
                            <Slider
                                value={profile.overtimeHours / 12}
                                onChange={(v) => setProfile({ ...profile, overtimeHours: v * 12 })}
                                min={0} max={100} step={5}
                                marks={[
                                    { value: 0, label: '0h' },
                                    { value: 20, label: '20h' },
                                    { value: 50, label: '50h' },
                                    { value: 80, label: '80h' },
                                ]}
                                color="orange"
                                size="lg"
                                className="mb-6"
                            />
                            <Text size="sm" c="dimmed" ta="center">슬라이더를 움직여 월 평균 야근 시간을 설정하세요.</Text>
                        </div>

                        <Card withBorder padding="lg" radius="md" bg="blue.0" style={{ borderColor: 'var(--mantine-color-blue-3)' }}>
                            <Group justify="space-between" align="center">
                                <div>
                                    <Text size="sm" tt="uppercase" fw={700} c="blue">총 연간 가용 시간</Text>
                                    <Title order={1} c="blue" style={{ lineHeight: 1 }}>
                                        {(profile.baseHours + profile.overtimeHours).toLocaleString()} <span className="text-lg font-normal text-gray-500">시간</span>
                                    </Title>
                                </div>
                                <ThemeIcon size={48} color="blue" variant="white" radius="md">
                                    <IconClock size={28} />
                                </ThemeIcon>
                            </Group>
                        </Card>

                        <Button fullWidth size="lg" onClick={handleNext} mt="md" color="blue">
                            설정 완료 및 직무 조사 시작
                        </Button>
                        <Button variant="subtle" size="sm" onClick={() => setStep(1)}>이전으로</Button>
                    </Stack>
                )}
            </div>
        </Modal>
    );
}
