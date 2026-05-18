<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="visible" class="consent-overlay">
        <Transition
          enter-active-class="transition duration-250 ease-out"
          enter-from-class="opacity-0 scale-95 translate-y-2"
          enter-to-class="opacity-100 scale-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="visible" class="consent-card">
            <!-- Icon -->
            <div class="consent-icon-wrap">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="#142741" stroke-width="1.8" stroke-linejoin="round"/>
                <path d="M9 12l2 2 4-4" stroke="#EF6C00" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>

            <!-- Heading -->
            <h2 class="consent-title">Before we begin</h2>

            <!-- Body -->
            <p class="consent-body">
              To track your progress, this feature saves your check-in responses to
              <strong>your device only</strong>. Nothing is ever sent to our servers.
            </p>

            <!-- What's stored list -->
            <ul class="consent-list">
              <li>Daily mood &amp; habit answers</li>
              <li>Pet companion level &amp; progress</li>
              <li>7-day insights history</li>
              <li>Your selected age stage &amp; sound setting</li>
            </ul>

            <p class="consent-note">
              You can clear this data at any time by clearing your browser's site data.
            </p>

            <!-- Actions -->
            <div class="consent-actions">
              <button class="btn-accept" @click="emit('accept')">
                Allow &amp; Start Check-in
              </button>
              <button class="btn-decline" @click="emit('decline')">
                Not now
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{ visible: boolean }>()
const emit = defineEmits<{ accept: []; decline: [] }>()
</script>

<style scoped>
.consent-overlay {
  position: fixed;
  inset: 0;
  z-index: 1250;
  background: rgba(0, 0, 0, 0.52);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.consent-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 36px 32px 32px;
  max-width: 440px;
  width: 100%;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.18);
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.consent-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: #f4f7fb;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.consent-title {
  font-family: 'Playfair Display', serif;
  font-size: 26px;
  font-weight: 800;
  color: #142741;
  margin: 0 0 12px;
  line-height: 1.2;
}

.consent-body {
  font-size: 14px;
  line-height: 1.65;
  color: #44474e;
  margin: 0 0 16px;
}

.consent-list {
  list-style: none;
  padding: 0;
  margin: 0 0 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.consent-list li {
  font-size: 13px;
  color: #142741;
  padding-left: 20px;
  position: relative;
}

.consent-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 7px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #EF6C00;
}

.consent-note {
  font-size: 12px;
  color: #74777f;
  margin: 0 0 28px;
  line-height: 1.5;
}

.consent-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-accept {
  width: 100%;
  height: 52px;
  border-radius: 14px;
  background: #142741;
  color: #ffffff;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.btn-accept:hover {
  background: #0d1c2e;
  transform: translateY(-2px);
}

.btn-decline {
  width: 100%;
  height: 44px;
  border-radius: 14px;
  background: transparent;
  color: #74777f;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid #e0e3e5;
  cursor: pointer;
  transition: color 0.18s ease, border-color 0.18s ease;
}

.btn-decline:hover {
  color: #44474e;
  border-color: #c4c6cf;
}
</style>
