"use client";

import { useState } from "react";
import SmartJobSurveyGrid from "@/components/SmartJobSurveyGrid";
import { UserOnboarding } from "@/components/UserOnboarding";
import { Container, Button } from "@mantine/core";
import { JobMissionTracker } from "@/components/JobMissionTracker";
import { IconArrowRight } from "@tabler/icons-react";

export default function JobSurveyPage() {
    const [onboardingComplete, setOnboardingComplete] = useState(false);
    const [userProfile, setUserProfile] = useState<any>(null);

    const handleOnboardingComplete = (profile: any) => {
        setUserProfile(profile);
        setOnboardingComplete(true);
    };

    const totalHours = userProfile ? (userProfile.baseHours + userProfile.overtimeHours) : 2080;

    return (
        <main className="min-h-screen bg-slate-50 p-8">
            <Container size="xl">
                <JobMissionTracker currentStep={2} />
                {/* Note: Ideally dynamic 2->3 based on progress, but hardcoded 2 (Breakdown/Measure phase) for now */}
            </Container>

            <UserOnboarding
                opened={!onboardingComplete}
                onComplete={handleOnboardingComplete}
            />

            <div className="max-w-[1600px] mx-auto filter transition-all duration-500" style={{ filter: onboardingComplete ? 'none' : 'blur(5px)' }}>
                <SmartJobSurveyGrid totalHours={totalHours} />
            </div>

            <Container size="xl" mt="xl" display="flex" style={{ justifyContent: 'flex-end' }}>
                <Button
                    size="lg"
                    rightSection={<IconArrowRight />}
                    variant="gradient"
                    gradient={{ from: 'indigo', to: 'cyan' }}
                    component="a"
                    href="/job-classification"
                >
                    미션 완료: 직무 분류로 이동 (Step 4)
                </Button>
            </Container>
        </main>
    );
}
