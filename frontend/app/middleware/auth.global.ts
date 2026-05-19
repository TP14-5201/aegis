export default defineNuxtRouteMiddleware((to) => {
  const loginDisabled = true

  if (loginDisabled) {
    if (to.path === '/login') {
      return navigateTo('/')
    }

    return
  }

  if (to.path === '/login') return

  const auth = useCookie('cherebowl_demo_auth')
  if (!auth.value) {
    return navigateTo('/login')
  }
})
