import { createTheme, rem, MantineTheme } from '@mantine/core';

export const theme = createTheme({
    primaryColor: 'violet',
    primaryShade: 6,
    defaultRadius: 'lg',
    fontFamily: 'var(--font-geist-sans), -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif, Apple Color Emoji, Segoe UI Emoji',
    headings: {
        fontFamily: 'var(--font-geist-sans), -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
        sizes: {
            h1: { fontSize: rem(34), lineHeight: '1.3' },
            h2: { fontSize: rem(26), lineHeight: '1.35' },
        },
    },
    shadows: {
        md: '0 8px 30px rgba(0, 0, 0, 0.05)',
        lg: '0 30px 60px rgba(0, 0, 0, 0.08)',
        xl: '0 30px 60px rgba(0, 0, 0, 0.12)',
    },
    components: {
        Button: {
            defaultProps: {
                radius: 'xl', // Pill shape for premium feel
                size: 'md',
            },
        },
        Card: {
            defaultProps: {
                radius: 'xl',
                shadow: 'md',
                withBorder: true,
            },
            styles: (theme: MantineTheme) => ({
                root: {
                    backgroundColor: 'rgba(255, 255, 255, 0.8)', // Glassmorphism base
                    backdropFilter: 'blur(12px)',
                    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                    '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: theme.shadows.xl,
                    },
                },
            }),
        },
        Paper: {
            defaultProps: {
                radius: 'xl',
                shadow: 'sm',
                withBorder: true,
            },
            styles: (theme: MantineTheme) => ({
                root: {
                    backgroundColor: 'rgba(255, 255, 255, 0.7)',
                    backdropFilter: 'blur(10px)',
                },
            }),
        },
        Modal: {
            defaultProps: {
                radius: 'lg',
            }
        }
    },
});
