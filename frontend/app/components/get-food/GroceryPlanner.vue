<template>
  <section id="grocery-planner" class="w-full bg-white py-16 lg:py-20">
    <div class="mx-auto max-w-6xl px-5">
      <form
        @submit.prevent="handleSubmit"
        novalidate
        class="rounded-3xl bg-white p-8 shadow-[0_20px_60px_rgba(0,0,0,0.1)] lg:p-12"
      >
        <h2 class="font-volkhov text-[28px] font-bold text-navy lg:text-[40px]">
          Tell us what you need
        </h2>

        <p class="mt-3 text-gray-600">
          Find budget-friendly ingredients tailored to your family's needs
        </p>

        <!-- Required hint -->
        <p class="mt-2 text-sm text-gray-500">
          Fields marked with <span class="text-red-500">*</span> are required
        </p>

        <!-- Form level error -->
        <p v-if="formError" class="mt-5 rounded-xl bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
          {{ formError }}
        </p>

        <div class="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
          
          <!-- Budget -->
          <div>
            <label for="budget" class="text-sm font-semibold text-navy">
              Budget ($) <span class="text-red-500">*</span>
            </label>

            <input
              id="budget"
              v-model="budget"
              type="text"
              placeholder="e.g. 100 (0-1000)"
              @input="validateBudget"
              @blur="validateBudget"
              :aria-invalid="!!errors.budget"
              aria-describedby="budget-error"
              :class="inputClass(errors.budget)"
            />

            <p v-if="errors.budget" id="budget-error" class="mt-2 text-sm text-red-600">
              {{ errors.budget }}
            </p>
          </div>

          <!-- Number of People -->
          <div>
            <label for="people" class="text-sm font-semibold text-navy">
              Number of People <span class="text-red-500">*</span>
            </label>

            <input
              id="people"
              v-model="people"
              type="text"
              placeholder="e.g. 2 (1-20)"
              @input="validatePeople"
              @blur="validatePeople"
              :aria-invalid="!!errors.people"
              aria-describedby="people-error"
              :class="inputClass(errors.people)"
            />

            <p v-if="errors.people" id="people-error" class="mt-2 text-sm text-red-600">
              {{ errors.people }}
            </p>
          </div>

          <!-- Number of Dishes -->
          <div>
            <label for="dishes" class="text-sm font-semibold text-navy">
              Number of Different Dishes <span class="text-red-500">*</span>
            </label>

            <input
              id="dishes"
              v-model="dishes"
              type="text"
              placeholder="e.g. 4 (1-20)"
              @input="validateDishes"
              @blur="validateDishes"
              :aria-invalid="!!errors.dishes"
              aria-describedby="dishes-error"
              :class="inputClass(errors.dishes)"
            />

            <p v-if="errors.dishes" id="dishes-error" class="mt-2 text-sm text-red-600">
              {{ errors.dishes }}
            </p>
          </div>

          <!-- Cuisine (Optional) -->
          <div>
            <label for="cuisine" class="text-sm font-semibold text-navy">
              Type of Cuisine <span class="text-gray-400">(optional)</span>
            </label>

            <div class="relative mt-2">
              <select
                id="cuisine"
                v-model="cuisine"
                class="h-12 w-full appearance-none rounded-xl bg-[#E6F0FA] px-4 pr-10 text-gray-700 outline-none focus:ring-2 focus:ring-[#B8DEFF]"
              >
                <option value="">No preference</option>
                <option value="Australian">Australian</option>
                <option value="Indian">Indian</option>
                <option value="Chinese">Chinese</option>
                <option value="Japanese">Japanese</option>
                <option value="Italian">Italian</option>
                <option value="Mediterranean">Mediterranean</option>
                <option value="Thai">Thai</option>
                <option value="Vietnamese">Vietnamese</option>
              </select>

              <span class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">
                ▼
              </span>
            </div>

            <p class="mt-2 text-sm text-gray-500">
              Leave blank to see a mix of cuisines.
            </p>
          </div>
        </div>

        <!-- Dietary Needs (Optional) -->
        <div class="mt-8">
          <p class="mb-3 text-sm font-semibold text-navy">
            Dietary Needs <span class="text-gray-400">(optional)</span>
          </p>

          <div class="flex flex-wrap gap-3">
            <button
              v-for="need in dietaryOptions"
              :key="need"
              type="button"
              @click="toggleDietaryNeed(need)"
              :class="[
                'rounded-full px-4 py-2 transition',
                dietaryNeeds.includes(need)
                  ? 'bg-[#B8DEFF] font-semibold text-navy ring-2 ring-navy'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              {{ need }}
            </button>
          </div>

          <p class="mt-2 text-sm text-gray-500">
            Select any that apply, or skip if none.
          </p>
        </div>

        <!-- Submit -->
        <div class="mt-10 flex justify-center">
          <button
            type="submit"
            class="group mt-10 inline-flex items-center justify-center
                  h-[58px] lg:h-[70px]
                  rounded-[20px]
                  bg-sky px-6
                  font-roboto font-bold
                  text-[16px] lg:text-[18px]
                  text-navy-deep
                  shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                  transition-all duration-300 ease-out
                  hover:-translate-y-1 hover:bg-[#9ed2ff]
                  hover:shadow-[0_16px_34px_rgba(68,154,196,0.28)]
                  active:translate-y-0"
          >
            Get Ingredient Recommendations
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
const budget = ref('')
const people = ref('')
const dishes = ref('')
const cuisine = ref('')
const dietaryNeeds = ref<string[]>([])
const formError = ref('')

const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-free', 'Dairy-free', 'Halal']

const emit = defineEmits<{
  submitPlanner: [data: {
    budget: number
    people: number
    dishes: number
    cuisine: string | null
    dietaryNeeds: string[]
  }]
}>()

const errors = reactive({
  budget: '',
  people: '',
  dishes: ''
})

const inputClass = (error: string) => [
  'mt-2 h-12 w-full rounded-xl px-4 outline-none transition',
  error
    ? 'bg-red-50 border border-red-500 text-red-700 focus:ring-2 focus:ring-red-300'
    : 'bg-[#E6F0FA] border border-transparent focus:ring-2 focus:ring-[#B8DEFF]'
]

const isWholeNumber = (value: string) => /^\d+$/.test(value)

/* VALIDATIONS */

const validateBudget = () => {
  const value = budget.value.trim()

  if (!value) {
    errors.budget = 'Please enter your budget.'
  } else if (isNaN(Number(value))) {
    errors.budget = 'Budget must be a valid number.'
  } else if (Number(value) <= 0) {
    errors.budget = 'Budget should be more than $0.'
  } else if (Number(value) > 1000) {
    errors.budget = 'Budget should not exceed $1000.'
  } else {
    errors.budget = ''
  }
}

const validatePeople = () => {
  const value = people.value.trim()

  if (!value) {
    errors.people = 'Please enter the number of people.'
  } else if (!isWholeNumber(value)) {
    errors.people = 'Please enter a whole number.'
  } else if (Number(value) < 1) {
    errors.people = 'There must be at least 1 person.'
  } else if (Number(value) > 20) {
    errors.people = 'Maximum is 20 people.'
  } else {
    errors.people = ''
  }
}

const validateDishes = () => {
  const value = dishes.value.trim()

  if (!value) {
    errors.dishes = 'Please enter how many dishes you want to prepare.'
  } else if (!isWholeNumber(value)) {
    errors.dishes = 'Please enter a whole number.'
  } else if (Number(value) < 1) {
    errors.dishes = 'You need at least 1 dish.'
  } else if (Number(value) > 20) {
    errors.dishes = 'Maximum is 20 dishes.'
  } else {
    errors.dishes = ''
  }
}

const validateForm = () => {
  validateBudget()
  validatePeople()
  validateDishes()

  return !errors.budget && !errors.people && !errors.dishes
}

/* DIETARY */
const toggleDietaryNeed = (need: string) => {
  if (dietaryNeeds.value.includes(need)) {
    dietaryNeeds.value = dietaryNeeds.value.filter(item => item !== need)
  } else {
    dietaryNeeds.value.push(need)
  }
}

/* SUBMIT */
const handleSubmit = () => {
  formError.value = ''

  const isValid = validateForm()

  if (!isValid) {
    formError.value = 'We just need a few details to find the best options for you.'
    return
  }

  const groceryPlannerData = {
    budget: Number(budget.value),
    people: Number(people.value),
    dishes: Number(dishes.value),
    cuisine: cuisine.value || null,
    dietaryNeeds: dietaryNeeds.value
  }

  emit('submitPlanner', groceryPlannerData)
}
</script>