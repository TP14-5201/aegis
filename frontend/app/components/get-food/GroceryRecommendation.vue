<template>
  <section id="grocery-recommendations" class="w-full bg-white py-16 lg:py-20">
    <div class="mx-auto max-w-7xl px-5 lg:px-8">
      <div class="mb-8">
        <h2 class="font-volkhov text-[30px] font-bold text-navy lg:text-[42px]">
          <span>{{ dishes.length }}</span>
          <span class="italic text-coral">
            {{ props.plannerData?.cuisine || 'recommended' }}
          </span>
          dishes for the family
        </h2>

        <p class="mt-2 font-roboto text-[15px] text-gray-500">
          Tap a dish to view its ingredients. Choose alternatives if an ingredient is unavailable.
        </p>
      </div>

      <!-- Dish cards -->
      <div class="mb-10 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <button
          v-for="dish in dishes"
          :key="dish.name"
          type="button"
          @click="selectedDishName = dish.name"
          :class="[
            'rounded-2xl px-5 py-5 text-left font-roboto shadow-md transition',
            selectedDishName === dish.name
              ? 'bg-[#D9ECFF] text-navy ring-2 ring-navy'
              : 'bg-white text-gray-700 hover:bg-[#EEF7FF]'
          ]"
        >
          <span class="block text-[17px] font-bold">
            {{ dish.name }}
          </span>

          <span class="mt-2 block text-[13px] text-gray-500">
            {{ dish.ingredients.length }} ingredients
          </span>

          <span class="mt-4 block text-[22px] font-bold text-navy">
            ${{ getDishCost(dish).toFixed(2) }}
          </span>
        </button>
      </div>

      <!-- Selected dish panel -->
      <div class="rounded-3xl bg-[#DCEEFF] px-5 py-7 lg:px-10 lg:py-9">
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
    </div>
  </section>
</template>

<script setup lang="ts">
type PlannerData = {
  budget: number
  people: number
  dishes: number
  cuisine: string | null
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

// TEMP: Hardcoded recommendation result.
// Later, replace this with backend API response based on plannerData.
const dishes: Dish[] = [
  {
    name: 'Spaghetti Bolognese',
    ingredients: [
      {
        name: 'Spaghetti',
        amount: '500g pack',
        price: 1.8,
        benefits: ['Energy', 'Brain'],
        swaps: [
          { name: 'Wholemeal spaghetti', price: 2.2 },
          { name: 'Penne pasta', price: 1.8 }
        ]
      },
      {
        name: 'Beef Mince',
        amount: '500g pack',
        price: 9.0,
        benefits: ['Muscles', 'Energy', 'Immunity'],
        swaps: [
          { name: 'Lentils', price: 1.4 },
          { name: 'Turkey mince', price: 8.5 },
          { name: 'Canned beans', price: 1.6 }
        ]
      },
      {
        name: 'Canned Tomatoes',
        amount: '400g tin',
        price: 1.5,
        benefits: ['Immunity', 'Brain'],
        swaps: [
          { name: 'Passata', price: 2.2 },
          { name: 'Fresh tomatoes', price: 3.5 }
        ]
      },
      {
        name: 'Onions',
        amount: '1 kg bag',
        price: 2.0,
        benefits: ['Immunity'],
        swaps: [
          { name: 'Frozen onion', price: 2.5 },
          { name: 'Spring onion', price: 2.2 }
        ]
      },
      {
        name: 'Garlic',
        amount: '1 bulb',
        price: 1.5,
        benefits: ['Immunity'],
        swaps: [
          { name: 'Garlic paste', price: 2.0 },
          { name: 'Garlic powder', price: 1.8 }
        ]
      }
    ]
  },
  {
    name: 'Pesto Pasta',
    ingredients: [
      {
        name: 'Fusilli',
        amount: '500g pack',
        price: 1.8,
        benefits: ['Energy', 'Brain'],
        swaps: [
          { name: 'Penne pasta', price: 1.8 },
          { name: 'Wholemeal pasta', price: 2.2 }
        ]
      },
      {
        name: 'Pesto Sauce',
        amount: '190g jar',
        price: 4.0,
        benefits: ['Brain'],
        swaps: [
          { name: 'Spinach pesto', price: 3.8 },
          { name: 'Tomato pasta sauce', price: 2.5 }
        ]
      },
      {
        name: 'Garlic',
        amount: '1 bulb',
        price: 1.5,
        benefits: ['Immunity'],
        swaps: [
          { name: 'Garlic paste', price: 2.0 },
          { name: 'Garlic powder', price: 1.8 }
        ]
      },
      {
        name: 'Parmesan Cheese',
        amount: '200g block',
        price: 5.5,
        benefits: ['Bones', 'Teeth', 'Muscles'],
        swaps: [
          { name: 'Grated parmesan', price: 4.8 },
          { name: 'Tasty cheese', price: 4.0 }
        ]
      }
    ]
  },
  {
    name: 'Margherita Pizza',
    ingredients: [
      {
        name: 'Pizza Bases',
        amount: '2 pack',
        price: 3.0,
        benefits: ['Energy'],
        swaps: [
          { name: 'Wraps', price: 2.8 },
          { name: 'Flatbread', price: 3.2 }
        ]
      },
      {
        name: 'Canned Tomatoes',
        amount: '400g tin',
        price: 1.5,
        benefits: ['Immunity', 'Brain'],
        swaps: [
          { name: 'Passata', price: 2.2 },
          { name: 'Tomato paste', price: 1.6 }
        ]
      },
      {
        name: 'Mozzarella Cheese',
        amount: '250g pack',
        price: 4.5,
        benefits: ['Bones', 'Teeth', 'Muscles'],
        swaps: [
          { name: 'Tasty cheese', price: 4.0 },
          { name: 'Ricotta', price: 4.2 }
        ]
      },
      {
        name: 'Dried Oregano',
        amount: '30g jar',
        price: 2.0,
        benefits: ['Immunity'],
        swaps: [
          { name: 'Mixed herbs', price: 2.0 },
          { name: 'Dried basil', price: 2.1 }
        ]
      }
    ]
  },
  {
    name: 'Pasta Carbonara',
    ingredients: [
      {
        name: 'Spaghetti',
        amount: '500g pack',
        price: 1.8,
        benefits: ['Energy', 'Brain'],
        swaps: [
          { name: 'Wholemeal spaghetti', price: 2.2 },
          { name: 'Rice noodles', price: 2.0 }
        ]
      },
      {
        name: 'Eggs',
        amount: '12 pack',
        price: 5.0,
        benefits: ['Brain', 'Muscles', 'Energy'],
        swaps: [
          { name: 'Free-range eggs', price: 4.5 },
          { name: 'Silken tofu', price: 1.8 }
        ]
      },
      {
        name: 'Bacon',
        amount: '250g pack',
        price: 5.0,
        benefits: ['Energy', 'Muscles'],
        swaps: [
          { name: 'Turkey bacon', price: 4.8 },
          { name: 'Mushrooms', price: 3.0 }
        ]
      },
      {
        name: 'Parmesan',
        amount: '200g block',
        price: 5.5,
        benefits: ['Bones', 'Teeth', 'Muscles'],
        swaps: [
          { name: 'Grated parmesan', price: 4.8 },
          { name: 'Tasty cheese', price: 4.0 }
        ]
      },
      {
        name: 'Garlic',
        amount: '1 bulb',
        price: 1.5,
        benefits: ['Immunity'],
        swaps: [
          { name: 'Garlic paste', price: 2.0 },
          { name: 'Garlic powder', price: 1.8 }
        ]
      }
    ]
  }
]

const selectedDishName = ref(dishes[0].name)

const selectedSwaps = ref<Record<string, Swap>>({})

const selectedDish = computed(() => {
  return dishes.find(dish => dish.name === selectedDishName.value) || dishes[0]
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
  return dishes.reduce((total, dish) => {
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