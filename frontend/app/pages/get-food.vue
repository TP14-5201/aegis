<template>
  <TopNavigation />

  <div>
    <div class="h-[72px] lg:h-[100px]" />
    <GetFoodHero />

    <GetFoodGroceryPlanner @submit-planner="handlePlannerSubmit" />

    <GetFoodGroceryRecommendation
      v-if="showRecommendations"
      :planner-data="plannerData"
    />
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl - Get Food' })

type PlannerData = {
  budget: number
  people: number
  dishes: number
  dietaryNeeds: string[]
}

const showRecommendations = ref(false)
const plannerData = ref<PlannerData | null>(null)

const handlePlannerSubmit = (data: PlannerData) => {
  plannerData.value = data
  showRecommendations.value = true

  nextTick(() => {
    document
      .getElementById('grocery-recommendations')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}
</script>