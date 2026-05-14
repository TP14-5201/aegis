<template>
  <TopNavigation />
  <main class="bg-chere-skyPale">
    <div class="h-[72px] lg:h-[100px]" />
  
    <QuickActionSupportHero />

    <QuickActionSupportSteps 
      :current-step="currentStep" />

    <QuickActionChooseActions
      v-if="currentStep === 1"
      :plans="plans"
      :selected-plan-id="selectedPlanId"
      @choose="choosePlan"
      @continue="continueToChecklist"
    />

    <QuickActionChecklist
      v-else-if="currentStep === 2 && selectedPlan"
      :plan="selectedPlan"
      :completed-step-indexes="completedStepIndexes"
      @toggle-step="toggleCompletedStep"
      @change-situation="changeSituation"
      @save="continueToSave"
    />

    <QuickActionSaveActions
      v-else-if="currentStep === 3 && selectedPlan"
      :plan="selectedPlan"
      :completed-step-indexes="completedStepIndexes"
      @back="currentStep = 2"
      @restart="startNewPlan"
    />

  </main>
  <Footer />
</template>

<script setup lang="ts">
type PlanId = 'food-today' | 'weekly-budget' | 'child-nutrition' | 'food-insecurity'

useHead({ title: 'ChereBowl - Quick Action' })

const currentStep = ref(1)
const selectedPlanId = ref<PlanId | null>(null)
const completedStepIndexes = ref<number[]>([])

const plans = {
'food-today': {
  category: 'Most urgent',
  badge: 'Urgent',
  title: 'I need food today',
  summaryTitle: 'Get food today.',
  checklistTitle: 'Find help near you.',
  steps: [
    {
      title: 'Find the nearest open food relief',
      detail: 'We’ll show open services sorted by distance',
      link: '/food-banks',
      linkText: 'Find Food Banks',
      time: '2 min',
    },
    {
      title: "Check today’s opening hours",
      detail: 'Hours change on weekends and holidays — confirm before you travel',
      time: '1 min',
    },
    {
      title: 'Plan your transport',
      detail: 'Free or low-cost public transport routes from your suburb',
      time: '2 min',
    },
    {
      title: 'Bring useful information',
      detail: 'Concession card if you have one. ID for adults. Reusable bags',
      link: '/food-banks',
      linkText: 'Checklist',
      time: '3 min',
    },
    {
      title: 'Save or Print this plan',
      detail: 'Take the address and hours with you in case the signal drops',
      time: '5 min',
    },
  ],
},
'weekly-budget': {
  category: 'Weekly stress',
  badge: 'Important',
  title: 'I have a small weekly budget',
  summaryTitle: 'Stretch your weekly budget.',
  checklistTitle: 'Stretch your weekly budget.',
  steps: [
    {
      title: 'Check budget ingredient recommendations',
      detail: 'A list of high-nutrition foods under budget.',
      link: '/get-food',
      linkText: 'Budget Ingredients',
      time: '4 min',
    },
    {
      title: 'Plan 3 simple meals from given ingredients',
      detail: 'Each meal feeds 2-4 and uses overlapping ingredients to reduce waste.',
      link: '/get-food',
      linkText: 'Meal planner',
      time: '6 min',
    },
    {
      title: 'Use a shopping list',
      detail: 'Stay on the list - it cuts impulse spend by ~22% on average.',
      time: '2 min',
    },
    {
      title: 'Pair shop visits with a relief drop',
      detail: 'Top up groceries with a fortnightly food parcel from a relief partner.',
      link: '/food-banks',
      linkText: 'Find Food Banks',
      time: '3 min',
    },
    {
      title: 'Read nutrition tips for kids',
      detail: 'Affordable foods that cover the key food groups for children.',
      link: '/nutrition-guide',
      linkText: 'Nutrition Guide',
      time: '5 min',
    },
  ],
},
'child-nutrition': {
  category: 'Long-term',
  badge: 'Helpful',
  title: "I don't know what to feed my child",
  summaryTitle: 'Build a Nutritious Week.',
  checklistTitle: 'Build a Nutritious Week',
  steps: [
    {
      title: 'Open the Nutrition Guide',
      detail: 'Body map shows what each food does for your child',
      link: '/nutrition-guide#body-map',
      linkText: 'Children Body Map',
      time: '4 min',
    },
    {
      title: 'Plan 4 simple foods you can afford',
      detail: 'Swap ingredients according to your preference for each of the ingredient listed',
      link: '/get-food',
      linkText: 'Smart Swaps',
      time: '6 min',
    },
    {
      title: 'Check how often your child should eat each',
      detail: 'Daily, weekly or “sometimes” - clear frequency for each food.',
      link: '/nutrition-guide#food-guide',
      linkText: 'Food Guide',
      time: '2 min',
    },
    {
      title: 'Plan a 7-day rotation',
      detail: 'Variety matters more than perfection. Rotate protein, grains, greens.',
      time: '3 min',
    },
    {
      title: 'Save the plan & Ingredient list',
      detail: 'Take it to the shops or to a food relief service.',
      time: '5 min',
    },
  ],
},
'food-insecurity': {
  category: 'Awareness',
  badge: 'Learn',
  title: 'I want to understand food insecurity in my area',
  summaryTitle: 'Understand the Bigger Picture.',
  checklistTitle: 'Understand the Bigger Picture',
  steps: [
    {
      title: 'Read the local data story',
      detail: 'How many families in victoria are food-insecure and where.',
      link: '/learn-more',
      linkText: 'Learn More',
      time: '4 min',
    },
    {
      title: 'Find a food bank or community shelter',
      detail: 'Locations, hours and what each one offers.',
      link: '/food-banks',
      linkText: 'Find Food Banks',
      time: '6 min',
    },
    {
      title: 'Share the guide with someone',
      detail: 'A friend, neighbour, or coworker who might benefit.',
      time: '2 min',
    },
  ],
},
} as const

const selectedPlan = computed(() => {
  if (!selectedPlanId.value) return null
  return plans[selectedPlanId.value]
})


function choosePlan(id: PlanId) {
  selectedPlanId.value = id
}

function toggleCompletedStep(index: number) {
  if (completedStepIndexes.value.includes(index)) {
    completedStepIndexes.value = completedStepIndexes.value.filter((item) => item !== index)
    return
  }

  completedStepIndexes.value.push(index)
}

function continueToChecklist() {
  if (!selectedPlanId.value) return
  currentStep.value = 2
}

function continueToSave() {
  if (completedStepIndexes.value.length === 0) return
  currentStep.value = 3
}

function changeSituation() {
  completedStepIndexes.value = []
  currentStep.value = 1
}

function startNewPlan() {
  selectedPlanId.value = null
  completedStepIndexes.value = []
  currentStep.value = 1
}
</script>