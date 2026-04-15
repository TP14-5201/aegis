<template>
  <nav
    class="w-full sticky top-0 z-50"
    style="background-color: #2D5016; font-family: 'Noto Serif', serif;"
  >
    <div class="w-full px-6 sm:px-10 h-[86px] flex items-center justify-between">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center gap-3 shrink-0 cursor-pointer">
        <div style="width: 46px; height: 56px; position: relative; overflow: hidden; flex-shrink: 0;">
          <img
            src="/images/logo.png"
            alt="Open Door Victoria"
            style="position: absolute; max-width: none; width: 283.99%; height: 240.96%; top: -48.28%; left: -92.05%; pointer-events: none;"
          />
        </div>
        <div style="display: flex; flex-direction: column; line-height: 1;">
          <span style="color: white; font-weight: 700; font-size: 28px;">Open Door</span>
          <span style="color: #ffb900; font-weight: 700; font-size: 18px; letter-spacing: 1px;">VICTORIA</span>
        </div>
      </NuxtLink>

      <!-- Nav Links -->
      <div class="flex items-center gap-6 sm:gap-8">
        <span class="nav-link text-white font-medium hidden sm:block" style="font-size: 17px; cursor: default;">
          Find Nearby
        </span>
        <NuxtLink
          to="/learn-more"
          class="nav-link text-white font-medium hidden sm:block"
          style="font-size: 17px;"
        >
          Learn More
        </NuxtLink>
        <button
          @click="quickExit"
          class="btn-exit flex items-center gap-2 rounded-[10px] shadow-lg cursor-pointer"
          style="background-color: #e7000b; padding: 8px 16px;"
        >
          <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
            <path d="M15 5L5 15" stroke="white" stroke-width="1.67" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M5 5L15 15" stroke="white" stroke-width="1.67" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span style="color: white; font-weight: 500; font-size: 16px;">Quick Exit</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
function quickExit() {
  window.location.href = 'https://www.google.com'
}
</script>
