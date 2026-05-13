// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      googleMapsApiKey: '',   // set via NUXT_PUBLIC_GOOGLE_MAPS_API_KEY in .env
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',  // set via NUXT_PUBLIC_API_BASE in .env
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
          href: '/logo/favicon.ico',
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
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap',
        },
      ],
    }
  }
})
