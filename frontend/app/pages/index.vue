<template>
  <TopNavigation />
  <div class="h-[72px]" />
    <main class="bg-white overflow-hidden">
      <LandingHeroContent />
      <LandingImpact />
      <LandingGroceryCostSection />
      <LandingFamilyNutrition />
      <LandingActionPlan />
    </main>

  <Footer />
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl - Home' })
</script>