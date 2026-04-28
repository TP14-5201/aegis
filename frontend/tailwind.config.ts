import type { Config } from 'tailwindcss'

export default {
  content: [
    './app/**/*.{vue,ts,js}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1B1E45',
        'bright-blue': '#0298C5',
        'light-blue': '#B5DCFF',
        'coral-orange': '#DF6651',
        'bg-blue': '#D8EDFF',
        'bg-input': '#F4F4F9',
        'heading-dark': '#1C1C11',
        'body-grey': '#525252',
        'border-grey': '#DEDEDB',
      },
      fontFamily: {
        serif: ['Volkhov', 'serif'],
        sans: ['Roboto', 'sans-serif'],
      },
      boxShadow: {
        'card-white': '0px 12px 30px rgba(0,0,0,0.1)',
        'card-blue': '0px 10px 15px rgba(0,0,0,0.1)',
      },
      borderRadius: {
        '20': '20px',
        '14': '14px',
        '10': '10px',
        '6': '6px',
      },
    },
  },
  plugins: [],
} satisfies Config
