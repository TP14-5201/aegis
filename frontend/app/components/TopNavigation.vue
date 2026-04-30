<template>
  <header
    class="fixed top-0 left-0 right-0 z-50 bg-white shadow-nav"
    :class="menuOpen ? 'h-auto' : 'h-[72px] lg:h-[100px]'"
  >
    <div class="mx-auto flex items-center justify-between h-[72px] lg:h-[100px] px-5 lg:px-10 max-w-8xl">
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center shrink-0" aria-label="cherebowl home">
        <img
          class="h-9 lg:h-11 w-auto object-contain"
          src="/images/ChereBowl-Logo.png"
          alt="cherebowl"
        />
      </NuxtLink>

      <!-- Desktop nav -->
      <nav class="hidden lg:flex items-center gap-1 xl:gap-2">
        <NavLink to="/services">Food Banks</NavLink>
        <NavLink to="/get-food">Get Food</NavLink>
        <NavLink to="/nutrition-guide">Nutrition Guide</NavLink>
        <NavLink to="/learn-more">Learn More</NavLink>
        <NavLink to="/about-us">About Us</NavLink>
      </nav>

      <!-- Mobile: hamburger -->
      <button
        @click="menuOpen = !menuOpen"
        class="lg:hidden inline-flex flex-col justify-center items-center gap-[5px] p-2 -mr-2"
        :aria-expanded="menuOpen"
        aria-label="Toggle menu"
      >
        <span
          class="block h-[2px] w-6 bg-navy rounded transition-transform"
          :class="menuOpen ? 'translate-y-[7px] rotate-45' : ''"
        />
        <span
          class="block h-[2px] w-6 bg-navy rounded transition-opacity"
          :class="menuOpen ? 'opacity-0' : ''"
        />
        <span
          class="block h-[2px] w-6 bg-navy rounded transition-transform"
          :class="menuOpen ? '-translate-y-[7px] -rotate-45' : ''"
        />
      </button>
    </div>

    <!-- Mobile drawer -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <nav
        v-if="menuOpen"
        class="lg:hidden flex flex-col gap-1 px-5 pb-4 border-t border-gray-100"
      >
        <NavLink to="/services" @navigate="menuOpen = false">Food Banks</NavLink>
        <NavLink to="/get-food" @navigate="menuOpen = false">Get Food</NavLink>
        <NavLink to="/nutrition-guide" @navigate="menuOpen = false">Nutrition Guide</NavLink>
        <NavLink to="/learn-more" @navigate="menuOpen = false">Learn More</NavLink>
        <NavLink to="/about-us" @navigate="menuOpen = false">About Us</NavLink>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
const menuOpen = ref(false)
const route = useRoute()
// Close drawer when route changes (e.g. when a NavLink is clicked)
watch(() => route.path, () => { menuOpen.value = false })
</script>
