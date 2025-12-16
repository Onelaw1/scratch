"use client";

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { theme } from '../theme';
import { LanguageProvider } from "@/contexts/LanguageContext";
import { AuthProvider } from "@/contexts/AuthContext";

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <LanguageProvider>
            <AuthProvider>
                <MantineProvider theme={theme}>
                    <Notifications />
                    {children}
                </MantineProvider>
            </AuthProvider>
        </LanguageProvider>
    );
}
