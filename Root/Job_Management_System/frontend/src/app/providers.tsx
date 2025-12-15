"use client";

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { theme } from '../theme';
import { LanguageProvider } from "@/contexts/LanguageContext";

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <LanguageProvider>
            <MantineProvider theme={theme}>
                <Notifications />
                {children}
            </MantineProvider>
        </LanguageProvider>
    );
}
