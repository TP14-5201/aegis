<template>
  <footer class="bg-[#dce9ff] px-6 py-10 lg:px-10">
    <div class="mx-auto flex max-w-7xl flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <NuxtLink
          to="/"
          class="text-[22px] font-bold text-black"
          style="font-family: 'Playfair Display', serif"
        >
          ChèreBowl
        </NuxtLink>

        <p class="mt-1 text-[13px] text-[#6b7280]">
          © 2026 ChèreBowl. Dignity in Every Bowl.
        </p>
      </div>

      <nav class="flex flex-wrap gap-x-8 gap-y-3 text-[14px] text-[#6b7280]">
        <NuxtLink to="/" class="hover:text-black">Home</NuxtLink>
        <NuxtLink to="/food-banks" class="hover:text-black">Food Bank</NuxtLink>
        <NuxtLink to="/get-food" class="hover:text-black">Get Food</NuxtLink>
        <NuxtLink to="/nutrition-guide" class="hover:text-black">Nutrition Guide</NuxtLink>
        <NuxtLink to="/health-tracking" class="nav-link">Health Tracking</NuxtLink>
        <NuxtLink to="/learn-more" class="nav-link">Know more</NuxtLink>
        <NuxtLink to="/quick-action" class="nav-link">Quick Action</NuxtLink>
      </nav>
    </div>
  </footer>
</template>

<style scoped>
footer {
  font-family: 'Plus Jakarta Sans', sans-serif;
}
</style>