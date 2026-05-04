export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/login') return

  const auth = useCookie('cherebowl_demo_auth')
  if (!auth.value) {
    return navigateTo('/login')
  }
})
