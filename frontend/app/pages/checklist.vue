<template>
  <TopNavigation />

  <div class="min-h-screen bg-white pt-[72px] lg:pt-[100px]">
    <div class="mx-auto max-w-7xl px-5 py-12 lg:px-12 lg:py-16">

      <!-- Back link -->
      <NuxtLink
        to="/get-food"
        class="mb-8 inline-flex items-center gap-2 font-body text-[14px] font-semibold text-[#0054cd] hover:underline"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Back to Get Food
      </NuxtLink>

      <GetFoodPackChecklist @close="$router.back()" />

    </div>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl — Pack-Up Checklist' })
</script>
