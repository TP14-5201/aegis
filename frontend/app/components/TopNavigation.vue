<template>
  <header
    class="fixed left-0 right-0 top-0 z-50 border-b border-[#e5e7eb] bg-[#f8f9ff]/95 backdrop-blur"
    :class="menuOpen ? 'h-auto' : 'h-[72px]'"
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
        <NuxtLink to="/learn-more" class="nav-link">Know more</NuxtLink>
      </nav>

      <NuxtLink
        to="/get-food"
        class="hidden h-10 items-center justify-center rounded-md bg-black px-7 text-[13px] font-bold text-white transition hover:opacity-90 lg:inline-flex"
      >
        Quick Action
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
        <NuxtLink to="/learn-more" class="mobile-link">Know more</NuxtLink>

        <NuxtLink
          to="/get-food"
          class="mt-3 inline-flex h-11 items-center justify-center rounded-md bg-black px-6 font-bold text-white"
        >
          Quick Action
        </NuxtLink>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
const menuOpen = ref(false)
const route = useRoute()

watch(
  () => route.path,
  () => {
    menuOpen.value = false
  }
)
</script>

<style scoped>
header {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.nav-link {
  position: relative;
  padding-bottom: 5px;
  color: #1f2937;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #000000;
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

.mobile-link {
  border-radius: 8px;
  padding: 10px 0;
  color: #0d1c2e;
}

.mobile-link.router-link-active {
  font-weight: 700;
}
</style>