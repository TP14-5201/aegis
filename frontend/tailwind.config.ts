import type { Config } from 'tailwindcss'

export default {
  content: [
    './app/**/*.{vue,ts,js}',
  ],
  theme: {
    extend: {
      colors: {
        navy: '#181e4b',
        'navy-deep': '#231c4e',
        coral: '#df6951',
        sky: '#b5dcff',
        'sky-tint': '#dbedff6b',
        'sky-active': '#029bc5',
        'blue-glow': '#59b1e6cc',
        ink: '#403b3b',
        ash: '#525252',
        muted: '#44474c',

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
        roboto: ['Roboto', 'Helvetica', 'sans-serif'],
        volkhov: ['Volkhov', 'Helvetica', 'serif'],
        sans: ['Roboto', 'Helvetica', 'sans-serif'],
        serif: ['Volkhov', 'Helvetica', 'serif'],
      },
      boxShadow: {
        cta: '0px 18.05px 31.58px #f1a50126',
        nav: '0px 4px 4px #00000040',
        card: '0px 10px 30px #0000001a',

        'card-white': '0px 12px 30px rgba(0,0,0,0.1)',
        'card-blue': '0px 10px 15px rgba(0,0,0,0.1)',
      },
      borderRadius: {
        '20': '20px',
        '14': '14px',
        '10': '10px',
        '6': '6px',
      },
      maxWidth: {
        '8xl': '1440px',
      },
    },
  },
  plugins: [],
} satisfies Config
