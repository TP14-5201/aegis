<template>
  <TopNavigation />
  <div class="h-[72px] lg:h-[100px]" />

  <NutritionGuideNutritionHero />

  <NutritionGuideBodyMap
    @select-food="handleFoodSelect"
  />

  <NutritionGuideFoodGuide
    :selected-food="selectedFood"
  />

  <NutritionGuideWellnessGuide />

  <Footer />
</template>

<script setup lang="ts">
import { ref } from 'vue'

useHead({ title: 'ChereBowl - Nutrition Guide' })

const selectedFood = ref<string | null>(null)

const handleFoodSelect = (foodName: string) => {
  selectedFood.value = foodName
}
</script>