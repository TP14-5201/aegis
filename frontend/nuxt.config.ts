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
      link: [
        {
          rel: 'icon',
          type: 'image/png',
          href: '/images/logo.png'
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.googleapis.com'
        },
        {
          rel: 'preconnect',
          href: 'https://fonts.gstatic.com',
          crossorigin: ''
        },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Volkhov:wght@400;700&family=Roboto:wght@300;400;500;700&display=swap'
        }
      ]
    }
  }
})
