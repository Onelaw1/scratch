import { createTheme } from '@mantine/core';

export const theme = createTheme({
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"',
    headings: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
        fontWeight: '700',
    },
    primaryColor: 'dark',
    defaultRadius: 'xl',
    colors: {
        // Custom Apple-like greys if needed, but Mantine's gray is close.
        // We can override 'dark' to be a true black or deep grey.
        dark: [
            '#C1C2C5',
            '#A6A7AB',
            '#909296',
            '#5C5F66',
            '#373A40',
            '#2C2E33',
            '#25262B',
            '#1A1B1E',
            '#141517',
            '#101113',
        ],
    },
    components: {
        Button: {
            defaultProps: {
                size: 'md',
                radius: 'xl',
            },
        },
        Container: {
            defaultProps: {
                size: 'xl',
            },
        },
    },
});
