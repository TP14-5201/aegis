<template>
  <TopNavigation />

  <div>
    <GetFoodHero />

    <GetFoodGroceryPlanner
      :showing-results="showRecommendations"
      @submit-planner="handlePlannerSubmit"
      @reset-planner="handleReset"
    />

    <GetFoodGroceryBag
      v-if="showRecommendations"
      :planner-data="plannerData"
    />
  </div>
  <Footer />
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl - Get Food' })

export type PlannerData = {
  budget: number
  dietaryNeeds: string[]
  dietaryGoal: string | null
  description: string | null
  budgetTier: string
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

const handleReset = () => {
  showRecommendations.value = false
  plannerData.value = null

  nextTick(() => {
    document
      .getElementById('grocery-planner')
      ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}
</script>
