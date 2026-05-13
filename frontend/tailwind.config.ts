import type { Config } from 'tailwindcss'

export default {
  content: ['./app/**/*.{vue,ts,js}'],
  theme: {
    extend: {
      colors: {
        chere: {
          navy: '#0D1C2E',
          ink: '#131B2E',
          blue: '#396477',
          sky: '#DCE9FF',
          skySoft: '#E6EEFF',
          skyPale: '#F8F9FF',
          coral: '#DF6951',
          text: '#45464D',
          muted: '#6B7280',
          border: '#C6C6CD',
          cream: '#FFF8E8',
        },
      },

      fontFamily: {
        display: ['"Playfair Display"', 'serif'],
        body: ['"Plus Jakarta Sans"', 'sans-serif'],

        playfair: ['"Playfair Display"', 'serif'],
        jakarta: ['"Plus Jakarta Sans"', 'sans-serif'],
        volkhov: ['"Playfair Display"', 'serif'],
        roboto: ['"Plus Jakarta Sans"', 'sans-serif'],
      },

      maxWidth: {
        container: '1200px',
      },

      minHeight: {
        section: 'clamp(640px, 82vh, 760px)',
        'section-lg': 'clamp(700px, 86vh, 820px)',
        'section-xl': 'clamp(720px, 88vh, 860px)',
      },

      spacing: {
        nav: '72px',
      },

      borderRadius: {
        card: '24px',
        button: '20px',
      },

      boxShadow: {
        card: '0 12px 30px rgba(0, 0, 0, 0.10)',
        soft: '0 24px 60px -8px rgba(68, 154, 196, 0.22)',
        button: '0 12px 28px rgba(68,154,196,0.22)',
      },

      backgroundImage: {
        'chere-hero': 'linear-gradient(180deg, #F8F9FF 0%, #E6EEFF 100%)',
        'chere-dark': 'linear-gradient(163deg, #131B2E 0%, #396477 100%)',
        'chere-slate': 'linear-gradient(154deg, #233144 0%, #565E74 100%)',
      },
    },
  },
  plugins: [],
} satisfies Config