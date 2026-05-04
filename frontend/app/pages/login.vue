<template>
  <main class="login-page">
    <img class="login-bg" src="/images/login-bg.png" alt="" />

    <div class="login-container">
      <div class="welcome-block">
        <h1>Welcome</h1>
        <p>A safe, quiet space for you.</p>
      </div>

      <form class="login-card" @submit.prevent="handleLogin">
        <div class="decorative-line" />

        <div class="logo-area">
          <img
            class="logo"
            src="/images/ChereBowl-Logo.png"
            alt="ChèreBowl"
          />
        </div>

        <div class="form-area">
          <p class="intro">
            Find open food banks and the fastest routes to get there
          </p>

          <div class="password-area">
            <label for="password">Password</label>

            <div class="input-wrapper">
              <img src="/images/lock.svg" alt="" class="lock-icon" />
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Enter your password"
                :disabled="loading"
              />
            </div>

            <p v-if="error" class="error">{{ error }}</p>
          </div>

          <button type="submit" :disabled="loading">
            <span v-if="loading" class="spinner" />
            <span v-else>Sign In</span>
          </button>
        </div>

        <p class="bottom-text">Breaking barriers to basic needs</p>
      </form>
    </div>
  </main>
</template>

<script setup lang="ts">
definePageMeta({ layout: false })

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!password.value) {
    error.value = 'Please enter a password.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const res = await $fetch<{ success: boolean }>(`${apiBase}/auth/login`, {
      method: 'POST',
      body: { password: password.value },
    })

    if (res.success) {
      const authCookie = useCookie('cherebowl_demo_auth', { maxAge: 60 * 60 * 24 })
      authCookie.value = 'true'
      await navigateTo('/')
    }
  } catch {
    error.value = 'Incorrect password. Please try again.'
    password.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  width: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.login-container {
  position: relative;
  z-index: 1;
  width: 448px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.welcome-block {
  text-align: center;
}

.welcome-block h1 {
  margin: 0;
  font-family: Volkhov, serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.1;
  color: #161d1f;
}

.welcome-block p {
  margin: 8px 0 0;
  font-family: Roboto, sans-serif;
  font-size: 16px;
  color: #3f4948;
}

.login-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #bec8c8;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  padding: 56px 25px 32px;
}

.decorative-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #0086ff 0%, #b5dcff 100%);
}

.logo-area {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.logo {
  width: 240px;
  height: auto;
  object-fit: contain;
}

.intro {
  margin: 0 auto 24px;
  text-align: center;
  font-family: Roboto, sans-serif;
  font-size: 13px;
  line-height: 1.5;
  color: #525252;
  max-width: 340px;
}

.password-area {
  margin-bottom: 20px;
}

.password-area label {
  display: block;
  margin-bottom: 8px;
  font-family: Roboto, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #161d1f;
}

.input-wrapper {
  position: relative;
}

.lock-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  opacity: 0.55;
}

.input-wrapper input {
  width: 100%;
  box-sizing: border-box;
  background: #f4fafd;
  border: 1px solid #bec8c8;
  border-radius: 8px;
  padding: 14px 16px 14px 42px;
  font-family: Roboto, sans-serif;
  font-size: 15px;
  color: #161d1f;
  outline: none;
  transition: border-color 0.2s;
}

.input-wrapper input::placeholder {
  color: rgba(111, 121, 121, 0.6);
}

.input-wrapper input:focus {
  border-color: #0086ff;
  box-shadow: 0 0 0 3px rgba(0, 134, 255, 0.12);
}

.input-wrapper input:disabled {
  opacity: 0.6;
}

.error {
  margin: 8px 0 0;
  font-family: Roboto, sans-serif;
  font-size: 13px;
  color: #e77c6b;
}

button[type="submit"] {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 8px;
  background: #b5dcff;
  font-family: Roboto, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #000;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background 0.2s, color 0.2s;
}

button[type="submit"]:hover:not(:disabled) {
  background: #0086ff;
  color: white;
}

button[type="submit"]:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.bottom-text {
  margin: 24px 0 0;
  text-align: center;
  font-family: Roboto, sans-serif;
  font-size: 13px;
  color: #525252;
}

@media (max-width: 520px) {
  .login-container {
    width: calc(100vw - 32px);
  }
}
</style>
