export default defineNuxtPlugin(() => {
  if (document.querySelector('script[src*="acsbapp.com"]')) return

  const script = document.createElement('script')
  script.src = 'https://acsbapp.com/apps/app/dist/js/app.js'
  script.async = true
  script.onload = () => {
    ;(window as Window & { acsbJS?: { init: () => void } }).acsbJS?.init()
  }
  ;(document.head || document.body).appendChild(script)
})