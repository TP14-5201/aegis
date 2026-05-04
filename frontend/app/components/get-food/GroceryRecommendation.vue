<template>
  <section id="grocery-recommendations" class="w-full bg-white py-16 lg:py-20">
    <div class="mx-auto max-w-7xl px-5 lg:px-8">
      <!-- Loading / error states -->
      <div v-if="loading" class="py-20 text-center font-roboto text-gray-500">
        Loading recommendations…
      </div>

      <div v-else-if="error" class="py-12 text-center font-roboto text-red-500">
        {{ error }}
      </div>

      <template v-else-if="dishes.length">

      <div class="mb-8">
        <h2 class="font-volkhov text-[30px] font-bold text-navy lg:text-[42px]">
          <span>{{ dishes.length }}</span>
          <span class="italic text-coral"> recommended </span>
          dishes for the family
        </h2>

        <p class="mt-2 font-roboto text-[15px] text-gray-500">
          Tap a dish to view its ingredients. Choose alternatives if an ingredient is unavailable.
        </p>
      </div>

      <!-- Dish cards -->
      <div class="mb-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="dish in dishes"
          :key="dish.name"
          :class="[
            'flex flex-col rounded-2xl px-5 py-5 font-roboto shadow-md transition cursor-pointer',
            selectedDishName === dish.name
              ? 'bg-[#D9ECFF] text-navy ring-2 ring-navy'
              : 'bg-white text-gray-700 hover:bg-[#EEF7FF]'
          ]"
          @click="selectedDishName = dish.name"
        >
          <div class="flex-1">
            <span class="block text-[17px] font-bold">
              {{ dish.name }}
            </span>

            <span class="mt-2 block text-[13px] text-gray-500">
              {{ dish.ingredients.length }} ingredients
            </span>

            <span class="mt-4 block text-[22px] font-bold text-navy">
              ${{ getDishCost(dish).toFixed(2) }}
            </span>
          </div>

          <button
            type="button"
            @click.stop="swapDish(dish.name)"
            :disabled="!swapPool.length"
            :class="[
              'mt-4 flex items-center gap-1 rounded-lg px-3 py-1.5 text-[12px] font-semibold transition self-start',
              swapPool.length
                ? 'bg-white/70 text-navy hover:bg-white'
                : 'cursor-not-allowed bg-white/30 text-gray-400'
            ]"
          >
            ↻ Swap dish
          </button>
        </div>
      </div>

      <!-- Selected dish panel -->
      <div v-if="selectedDish" class="rounded-3xl bg-[#DCEEFF] px-5 py-7 lg:px-10 lg:py-9">
        <div class="mb-10 flex items-start justify-between gap-6">
          <div>
            <h3 class="font-volkhov text-[26px] font-bold text-navy lg:text-[32px]">
              {{ selectedDish.name }}
            </h3>

            <p class="mt-2 font-roboto text-[14px] text-gray-600">
              Current selected ingredients for this dish.
            </p>
          </div>

          <div class="text-right font-roboto">
            <p class="text-[13px] text-gray-500">Dish cost</p>
            <p class="text-[26px] font-bold text-navy">
              ${{ getDishCost(selectedDish).toFixed(2) }}
            </p>
          </div>
        </div>

        <!-- Ingredients -->
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="ingredient in selectedDish.ingredients"
            :key="ingredient.name"
            class="overflow-hidden rounded-3xl bg-white shadow-sm"
          >
            <div class="p-6">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <p class="font-roboto text-[12px] font-semibold uppercase tracking-wide text-gray-400">
                    Selected ingredient
                  </p>

                  <h4 class="mt-1 font-roboto text-[17px] font-bold text-navy">
                    {{ getSelectedName(selectedDish.name, ingredient) }}
                  </h4>

                  <p class="mt-1 font-roboto text-[14px] text-gray-500">
                    {{ ingredient.amount }}
                  </p>
                </div>

                <p class="font-roboto text-[18px] font-semibold text-navy">
                  ${{ getSelectedPrice(selectedDish.name, ingredient).toFixed(2) }}
                </p>
              </div>

              <p class="mt-5 font-roboto text-[13px] text-gray-500">
                Helps your child's
              </p>

              <div class="mt-2 flex flex-wrap gap-2">
                <span
                  v-for="benefit in ingredient.benefits"
                  :key="benefit"
                  :class="benefitClass(benefit)"
                >
                  {{ benefitIcon(benefit) }} {{ benefit }}
                </span>
              </div>

            
            </div>

            <!-- Alternatives shown immediately -->
            <div class="border-t border-gray-100 bg-gray-50 px-6 py-5">
              <p class="mb-1 font-roboto text-[13px] font-semibold text-navy">
                Alternatives
              </p>

              <p class="mb-3 font-roboto text-[12px] text-gray-500">
                Click an alternative to swap. Click the selected alternative again to return to the original ingredient.
              </p>

              <div class="grid grid-cols-1 gap-2">
                <button
                  v-for="swap in ingredient.swaps"
                  :key="swap.name"
                  type="button"
                  @click="toggleSwap(selectedDish.name, ingredient, swap)"
                  :class="alternativeClass(selectedDish.name, ingredient, swap.name)"
                >
                  <span>{{ swap.name }}</span>
                  <span>${{ swap.price.toFixed(2) }}</span>
                </button>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- Total grocery price -->
      <div class="mt-8 rounded-3xl bg-navy px-6 py-6 text-center shadow-lg lg:px-10">
        <p class="font-roboto text-[15px] font-semibold text-white/70">
          Total Estimated Grocery Price
        </p>

        <p class="mt-2 font-volkhov text-[34px] font-bold text-white lg:text-[46px]">
          ${{ totalEstimatedGroceryPrice.toFixed(2) }}
        </p>
      </div>

      </template>
    </div>
  </section>
</template>

<script setup lang="ts">
type PlannerData = {
  budget: number
  people: number
  dishes: number
  dietaryNeeds: string[]
}

const props = defineProps<{
  plannerData: PlannerData | null
}>()

type Benefit = 'Energy' | 'Brain' | 'Muscles' | 'Immunity' | 'Bones' | 'Teeth'

type Swap = {
  name: string
  price: number
}

type Ingredient = {
  name: string
  amount: string
  price: number
  benefits: Benefit[]
  swaps: Swap[]
}

type Dish = {
  name: string
  ingredients: Ingredient[]
}

const config = useRuntimeConfig()

const dishes = ref<Dish[]>([])
const swapPool = ref<Dish[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

function transformDishes(apiDishes: any[]): Dish[] {
  return apiDishes.map(d => ({
    name: d.name,
    ingredients: (d.ingredients ?? []).map((ing: any) => ({
      name: ing.name,
      amount: ing.packLabel ?? '',
      price: ing.priceAUD ?? 0,
      benefits: ing.benefits ?? [],
      swaps: (ing.alternatives ?? []).map((alt: any) => ({
        name: alt.name,
        price: alt.priceAUD ?? 0,
      })),
    })),
  }))
}

watch(
  () => props.plannerData,
  async (data) => {
    if (!data) return
    loading.value = true
    error.value = null
    selectedSwaps.value = {}
    try {
      const res = await $fetch<any>(`${config.public.apiBase}/api/recommendations`, {
        method: 'POST',
        body: {
          budget: data.budget,
          numberOfPeople: data.people,
          numberOfDishes: data.dishes,
          dietaryNeeds: data.dietaryNeeds,
        },
      })
      const all = transformDishes(res.dishes ?? [])
      dishes.value = all.slice(0, data.dishes)
      swapPool.value = all.slice(data.dishes)
      selectedDishName.value = dishes.value[0]?.name ?? ''
    } catch (e: any) {
      error.value = e?.data?.detail ?? 'Something went wrong. Please try again.'
    } finally {
      loading.value = false
    }
  },
  { immediate: true }
)

function swapDish(dishName: string) {
  if (!swapPool.value.length) return
  const idx = dishes.value.findIndex(d => d.name === dishName)
  if (idx === -1) return
  const [next, ...rest] = swapPool.value
  const outgoing = dishes.value[idx]
  dishes.value = [
    ...dishes.value.slice(0, idx),
    next,
    ...dishes.value.slice(idx + 1),
  ]
  swapPool.value = [...rest, outgoing]
  if (selectedDishName.value === dishName) {
    selectedDishName.value = next.name
  }
}

const selectedDishName = ref('')

const selectedSwaps = ref<Record<string, Swap>>({})

const selectedDish = computed(() => {
  if (!dishes.value.length) return null
  return dishes.value.find(dish => dish.name === selectedDishName.value) || dishes.value[0]
})

const ingredientKey = (dishName: string, ingredientName: string) => {
  return `${dishName}-${ingredientName}`
}

const getSelectedSwap = (dishName: string, ingredient: Ingredient) => {
  const key = ingredientKey(dishName, ingredient.name)
  return selectedSwaps.value[key]
}

const getSelectedName = (dishName: string, ingredient: Ingredient) => {
  return getSelectedSwap(dishName, ingredient)?.name || ingredient.name
}

const getSelectedPrice = (dishName: string, ingredient: Ingredient) => {
  return getSelectedSwap(dishName, ingredient)?.price ?? ingredient.price
}

const toggleSwap = (dishName: string, ingredient: Ingredient, swap: Swap) => {
  const key = ingredientKey(dishName, ingredient.name)
  const currentSwap = selectedSwaps.value[key]

  if (currentSwap?.name === swap.name) {
    delete selectedSwaps.value[key]
  } else {
    selectedSwaps.value[key] = swap
  }
}

const getDishCost = (dish: Dish) => {
  return dish.ingredients.reduce((total, ingredient) => {
    return total + getSelectedPrice(dish.name, ingredient)
  }, 0)
}

const totalEstimatedGroceryPrice = computed(() => {
  return dishes.value.reduce((total, dish) => {
    return total + getDishCost(dish)
  }, 0)
})

const alternativeClass = (
  dishName: string,
  ingredient: Ingredient,
  optionName: string
) => {
  const isSelected = getSelectedName(dishName, ingredient) === optionName

  return [
    'flex w-full items-center justify-between rounded-xl px-4 py-3 text-left font-roboto text-[13px] transition',
    isSelected
      ? 'bg-navy font-semibold text-white ring-2 ring-navy'
      : 'bg-white text-gray-700 hover:bg-[#D9ECFF]'
  ]
}

const benefitIcon = (benefit: Benefit) => {
  const icons: Record<Benefit, string> = {
    Energy: '⚡',
    Brain: '🧠',
    Muscles: '💪',
    Immunity: '🛡',
    Bones: '🦴',
    Teeth: '☻'
  }

  return icons[benefit]
}

const benefitClass = (benefit: Benefit) => {
  const base = 'rounded-full px-3 py-1 font-roboto text-[12px] font-semibold'

  const styles: Record<Benefit, string> = {
    Energy: 'bg-[#FFF1C7] text-[#B07A00]',
    Brain: 'bg-[#E8EEF9] text-[#526B91]',
    Muscles: 'bg-[#FCE4EF] text-[#B65375]',
    Immunity: 'bg-[#DFF3D8] text-[#3E7A47]',
    Bones: 'bg-[#EFE6D7] text-[#8A6C35]',
    Teeth: 'bg-[#EDE2F3] text-[#7B5B92]'
  }

  return `${base} ${styles[benefit]}`
}
</script>