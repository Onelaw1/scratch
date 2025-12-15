"use client";

import { useState } from "react";
import { Container, Tabs, rem } from "@mantine/core"; // Updated for Mantine v7
import { IconHierarchy, IconGridDots } from "@tabler/icons-react";
import CascadingJobView from "@/components/CascadingJobView";
import JobMatrixGrid from "@/components/JobMatrixGrid";

export default function JobClassificationPage() {
    return (
        <Container size="xl" py="xl">
            <Tabs defaultValue="cascading" variant="pills" radius="xl">
                <Tabs.List mb="lg">
                    <Tabs.Tab
                        value="cascading"
                        leftSection={<IconHierarchy style={{ width: rem(16), height: rem(16) }} />}
                    >
                        Cascading View (Tree)
                    </Tabs.Tab>
                    <Tabs.Tab
                        value="matrix"
                        leftSection={<IconGridDots style={{ width: rem(16), height: rem(16) }} />}
                    >
                        Matrix View (Edit)
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
