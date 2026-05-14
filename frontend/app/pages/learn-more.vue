<template>
  <TopNavigation />
  <div class="h-[72px] lg:h-[100px] bg-[#F8F9FF]" />
  <LearnMoreTheStoryHero />
  <LearnMoreThePath />
  <LearnMoreRegionMap id="region-map" />
  <LearnMoreChildrenAgeGroups id="children-age-groups" />
  <LearnMoreBehaviouralImpact id="behavioural-impact" />
  <LearnMoreNextSteps id="next-steps" />
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl - Learn More' })
</script>
