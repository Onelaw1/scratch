import { createTheme, MantineColorsTuple } from '@mantine/core';

const appleBlue: MantineColorsTuple = [
    '#e5f4ff',
    '#cce6ff',
    '#99caff',
    '#66adff',
    '#3390ff',
    '#0073ff', // Primary
    '#005bc4',
    '#004494',
    '#002d63',
    '#001633',
];

export const theme = createTheme({
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"',
    primaryColor: 'blue',
    colors: {
        blue: appleBlue,
    },
    defaultRadius: 'xl',
    shadows: {
        md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    },
    components: {
        Button: {
            defaultProps: {
                fw: 500,
            },
        },
        Card: {
            defaultProps: {
                shadow: 'sm',
                radius: 'lg',
                withBorder: true,
            },
        },
    },
});
