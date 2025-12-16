"use client";

import { useState } from "react";
import { Container, Tabs, rem } from "@mantine/core"; // Updated for Mantine v7
import { IconHierarchy, IconGridDots } from "@tabler/icons-react";
import CascadingJobView from "@/components/CascadingJobView";
import JobMatrixGrid from "@/components/JobMatrixGrid";
import { JobMissionTracker } from "@/components/JobMissionTracker";

export default function JobClassificationPage() {
    return (
        <Container size="xl" py="xl">
            <JobMissionTracker currentStep={4} />
            <Tabs defaultValue="cascading" variant="pills" radius="xl">
                <Tabs.List mb="lg">
                    <Tabs.Tab
                        value="cascading"
                        leftSection={<IconHierarchy style={{ width: rem(16), height: rem(16) }} />}
                    >
                        계층형 뷰 (Tree View)
                    </Tabs.Tab>
                    <Tabs.Tab
                        value="matrix"
                        leftSection={<IconGridDots style={{ width: rem(16), height: rem(16) }} />}
                    >
                        매트릭스 뷰 (Matrix Edit)
                    </Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="cascading">
                    <CascadingJobView />
                </Tabs.Panel>

                <Tabs.Panel value="matrix">
                    <JobMatrixGrid />
                </Tabs.Panel>
            </Tabs>
        </Container>
    );
}
