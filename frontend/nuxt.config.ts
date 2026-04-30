// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      googleMapsKey: '',   // set via NUXT_PUBLIC_GOOGLE_MAPS_KEY in .env
      apiBase: 'http://localhost:8000',  // set via NUXT_PUBLIC_API_BASE in .env
      mapboxToken: '',     // set via NUXT_PUBLIC_MAPBOX_TOKEN in .env
    },
  },
  app: {
    head: {
      title: 'cherebowl',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'cherebowl — help is here when you need it.' },
      ],
      link: [
        {
          rel: 'icon',
          type: 'image/png',
          href: '/images/logo.png',
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com',
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: '',
        },
        {
          // Loads both old (Volkhov 400/700, Roboto 300/400/500/700) and new
          // (Roboto 800/900) weights so every component renders correctly.
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Volkhov:wght@400;700&family=Roboto:wght@300;400;500;700;800;900&display=swap',
        },
      ],
    }
  }
})
