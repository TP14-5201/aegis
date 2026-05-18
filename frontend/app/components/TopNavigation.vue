<template>
  <!-- Floating notch -->
  <div
    v-if="isNavHidden"
    class="fixed left-1/2 top-0 z-[1300] flex -translate-x-1/2 items-center justify-center"
    @mouseenter="isNavHidden = false"
  >
    <div
      class="flex h-6 w-14 items-end justify-center rounded-b-full border border-[#e5e7eb] bg-[#f8f9ff]/95 pb-1 shadow-md backdrop-blur"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-4 w-4 text-[#396477]"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M19 9l-7 7-7-7"
        />
      </svg>
    </div>
  </div>

  <!-- Desktop -->
  <header
    class="fixed left-0 right-0 top-0 z-[1300] border-b border-[#e5e7eb] bg-[#f8f9ff]/95 backdrop-blur transition-transform duration-300"
    :class="[
      menuOpen ? 'h-auto' : 'h-[72px]',
      isNavHidden ? '-translate-y-full' : 'translate-y-0',
    ]"
  >
    <div class="mx-auto flex h-[72px] max-w-[1200px] items-center justify-between px-6 lg:px-10">
      <NuxtLink
        to="/"
        class="shrink-0 text-[22px] font-bold text-black"
        style="font-family: 'Playfair Display', serif"
      >
        ChèreBowl
      </NuxtLink>

      <nav class="hidden items-center gap-8 text-[14px] font-medium text-[#1f2937] lg:flex">
        <NuxtLink to="/" class="nav-link">Home</NuxtLink>
        <NuxtLink to="/food-banks" class="nav-link">Find Food Banks</NuxtLink>
        <NuxtLink to="/get-food" class="nav-link">Get Food</NuxtLink>
        <NuxtLink to="/nutrition-guide" class="nav-link">Nutrition Guide</NuxtLink>
        <NuxtLink to="/health-tracking" class="nav-link">Health Tracking</NuxtLink>
        <NuxtLink to="/learn-more" class="nav-link">Know more</NuxtLink>
      </nav>

      <NuxtLink
        to="/quick-action"
        class="quick-action-btn hidden h-10 items-center justify-center rounded-md bg-black px-7 text-[13px] font-bold text-white lg:inline-flex"
        style="transition: opacity 0.22s ease, transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);"
      >
        <span class="quick-action-text">
          Quick Action
        </span>
      </NuxtLink>

      <button
        class="-mr-2 inline-flex flex-col items-center justify-center gap-[5px] p-2 lg:hidden"
        :aria-expanded="menuOpen"
        aria-label="Toggle menu"
        @click="menuOpen = !menuOpen"
      >
        <span
          class="block h-[2px] w-6 rounded bg-[#0d1c2e] transition-transform"
          :class="menuOpen ? 'translate-y-[7px] rotate-45' : ''"
        />
        <span
          class="block h-[2px] w-6 rounded bg-[#0d1c2e] transition-opacity"
          :class="menuOpen ? 'opacity-0' : ''"
        />
        <span
          class="block h-[2px] w-6 rounded bg-[#0d1c2e] transition-transform"
          :class="menuOpen ? '-translate-y-[7px] -rotate-45' : ''"
        />
      </button>
    </div>

    <!-- Mobile-->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-2 opacity-0"
    >
      <nav
        v-if="menuOpen"
        class="flex flex-col gap-1 border-t border-[#e5e7eb] bg-[#f8f9ff] px-6 pb-5 pt-3 text-[15px] lg:hidden"
      >
        <NuxtLink to="/" class="mobile-link">Home</NuxtLink>
        <NuxtLink to="/food-banks" class="mobile-link">Find Food Banks</NuxtLink>
        <NuxtLink to="/get-food" class="mobile-link">Get Food</NuxtLink>
        <NuxtLink to="/nutrition-guide" class="mobile-link">Nutrition Guide</NuxtLink>
        <NuxtLink to="/health-tracking" class="mobile-link">Health Tracking</NuxtLink>
        <NuxtLink to="/learn-more" class="mobile-link">Know more</NuxtLink>

        <NuxtLink
          to="/quick-action"
          class="quick-action-mobile mt-3 inline-flex h-11 items-center justify-center rounded-md bg-black px-6 font-bold text-white"
        >
          Quick Action
        </NuxtLink>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
const menuOpen = ref(false)
const isNavHidden = ref(false)
const route = useRoute()

watch(
  () => route.path,
  () => {
    menuOpen.value = false
  }
)

function handleScroll() {
  isNavHidden.value = window.scrollY > 80
}

function handleMouseMove(event: MouseEvent) {
  if (event.clientY <= 28) {
    isNavHidden.value = false
  } else if (window.scrollY > 80) {
    isNavHidden.value = true
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('mousemove', handleMouseMove)
})
</script>

<style scoped>
header {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.nav-link {
  position: relative;
  padding-bottom: 5px;
  color: #1f2937;
  display: inline-block;
  transition: color 0.22s ease, transform 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.nav-link:hover {
  color: #000000;
  transform: translateY(-3px);
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -3px;
  height: 2px;
  border-radius: 999px;
  background-color: #000000;
}

.quick-action-btn:hover {
  opacity: 0.9;
  transform: translateY(-3px);
}

.quick-action-text {
  position: relative;
}

.quick-action-btn.router-link-active .quick-action-text::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -4px;
  width: 100%;
  height: 2px;
  transform: translateX(-50%);
  border-radius: 999px;
  background-color: #ffffff;
}

.quick-action-mobile.router-link-active {
  box-shadow: 0 0 0 3px rgba(57, 100, 119, 0.22);
}

.mobile-link {
  border-radius: 8px;
  padding: 10px 0;
  color: #0d1c2e;
}

.mobile-link.router-link-active {
  font-weight: 700;
}
</style>