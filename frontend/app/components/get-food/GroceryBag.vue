<template>
  <section id="grocery-recommendations" class="w-full bg-[#F5F7FA] py-16 lg:py-20">
    <div class="mx-auto max-w-3xl px-5 lg:px-8">

      <!-- ── HEADER ──────────────────────────────────────────────────── -->
      <div class="mb-6">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-bold uppercase tracking-widest text-[#396477]">Your Grocery Bag</p>
            <h2 class="mt-1 font-volkhov text-[28px] font-bold text-navy lg:text-[38px]">
              <span class="italic text-coral">One wholesome shop,</span>
              <span> built for you</span>
            </h2>
          </div>
        </div>
        <p class="mt-1 font-roboto text-[14px] text-gray-500">
          Top picks globally ranked for your budget.
          <template v-if="props.plannerData?.dietaryGoal"> Goal: <strong>{{ props.plannerData.dietaryGoal }}</strong>.</template>
          Hit <strong>Swap</strong> to pick an alternative for any slot.
        </p>
      </div>

      <!-- ── QUICK GUIDE ─────────────────────────────────────────────── -->
      <details class="mb-8 rounded-2xl border border-gray-200 bg-white px-6 py-4">
        <summary class="cursor-pointer font-roboto text-[13px] font-semibold text-navy select-none">
          ▸ Quick guide — what each tag means
        </summary>
        <div class="mt-4 grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div>
            <p class="mb-2 text-[12px] font-bold uppercase tracking-wider text-gray-400">Nutrient badges</p>
            <div class="space-y-1">
              <div class="flex items-start gap-2 text-[12px]">
                <span :class="badgeClass('High protein')" class="shrink-0">{{ badgeIcon('High protein') }} High protein</span>
                <span class="text-gray-500">Protein above 12.4 g/100 g — great for muscles and satiety.</span>
              </div>
              <div class="flex items-start gap-2 text-[12px]">
                <span :class="badgeClass('High fibre')" class="shrink-0">{{ badgeIcon('High fibre') }} High fibre</span>
                <span class="text-gray-500">Dietary fibre above 3.4 g/100 g — supports digestion and fullness.</span>
              </div>
              <div class="flex items-start gap-2 text-[12px]">
                <span :class="badgeClass('Low fat')" class="shrink-0">{{ badgeIcon('Low fat') }} Low fat</span>
                <span class="text-gray-500">Total fat below 3 g/100 g — lighter option for the whole family.</span>
              </div>
              <div class="flex items-start gap-2 text-[12px]">
                <span :class="badgeClass('Low sugar')" class="shrink-0">{{ badgeIcon('Low sugar') }} Low sugar</span>
                <span class="text-gray-500">Total sugars below 5 g/100 g — helps manage daily sugar intake.</span>
              </div>
            </div>
          </div>
          <div>
            <p class="mb-2 text-[12px] font-bold uppercase tracking-wider text-gray-400">Relative cost levels</p>
            <div class="space-y-1">
              <div v-for="tier in priceTierGuide" :key="tier.label" class="flex items-center gap-2 text-[12px]">
                <span :class="tierBadgeClass(tier.label)" class="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-bold">{{ tier.label }}</span>
                <span class="text-gray-500">{{ tier.description }}</span>
              </div>
            </div>
          </div>
        </div>
      </details>

      <p class="mt-3 font-roboto text-[12px] text-gray-500">
        <span class="font-semibold text-gray-600">Note:</span>
        When swapping, <span class="font-bold text-red-500">▲▲</span> means the alternative is relatively pricier,
        <span class="font-bold text-green-600">▼▼</span> means it's cheaper.
      </p>

      <!-- ── LOW BUDGET ────────────────────────────────────────────── -->
      <div v-if="(props.plannerData?.budget ?? 0) <= 2" class="rounded-2xl bg-amber-50 px-6 py-8 text-center">
        <p class="font-roboto text-[15px] font-semibold text-amber-700">Budget too low for recommendations</p>
        <p class="mt-1 text-[13px] text-amber-600">A budget of $2 or under doesn't cover any grocery items. Please increase your budget to see recommendations.</p>
      </div>

      <!-- ── LOADING ─────────────────────────────────────────────────── -->
      <div v-else-if="pending" class="space-y-4">
        <div v-for="i in 6" :key="i" class="animate-pulse rounded-3xl bg-white p-6 shadow-sm">
          <div class="mb-3 h-4 w-24 rounded bg-gray-200" />
          <div class="h-6 w-3/4 rounded bg-gray-200" />
          <div class="mt-2 h-4 w-1/2 rounded bg-gray-200" />
          <div class="mt-4 h-4 w-full rounded bg-gray-100" />
        </div>
      </div>

      <!-- ── ERROR ───────────────────────────────────────────────────── -->
      <div v-else-if="fetchError" class="rounded-2xl bg-red-50 px-6 py-8 text-center">
        <p class="font-roboto text-[15px] font-semibold text-red-700">Could not load recommendations</p>
        <p class="mt-1 text-[13px] text-red-500">{{ fetchError.message }}</p>
        <button
          type="button"
          @click="refresh()"
          class="mt-4 rounded-xl bg-red-100 px-5 py-2 text-[13px] font-semibold text-red-700 hover:bg-red-200"
        >
          Try again
        </button>
      </div>

      <!-- ── EMPTY ───────────────────────────────────────────────────── -->
      <div v-else-if="!pending && resolvedSlots.length === 0" class="rounded-2xl bg-white px-6 py-10 text-center shadow-sm">
        <p class="font-roboto text-[15px] text-gray-500">No ingredients found — try broadening your filters or choosing a different budget tier.</p>
      </div>

      <!-- ── BAG SLOTS ──────────────────────────────────────────────── -->
      <div v-else class="space-y-4">
        <article
          v-for="slot in resolvedSlots"
          :key="slot.sub_category"
          class="overflow-hidden rounded-3xl bg-white shadow-sm"
        >
          <!-- Slot header row -->
          <div class="flex items-start gap-4 p-6">
            <!-- Category initial avatar -->
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[#E6F0FA] font-roboto text-[18px] font-bold text-[#396477]">
              {{ categoryInitial(slot.sub_category) }}
            </div>

            <div class="flex-1 min-w-0">
              <!-- Sub-category label + cost tier -->
              <div class="flex flex-wrap items-center gap-2 mb-1">
                <p class="font-roboto text-[11px] font-bold uppercase tracking-wider text-[#396477]">{{ slot.sub_category }}</p>
                <span :class="tierBadgeClass(priceTier(slot.selected.retail_price))" class="rounded-full px-2 py-0.5 text-[10px] font-bold">
                  {{ priceTier(slot.selected.retail_price) }}
                </span>
                <span
                  v-if="matchesGoal(slot.selected, props.plannerData?.dietaryGoal ?? null)"
                  class="rounded-full bg-teal-100 px-2 py-0.5 text-[10px] font-bold text-teal-700"
                >
                  Matches goal
                </span>
              </div>

              <!-- Ingredient name -->
              <h3 class="font-roboto text-[16px] font-bold text-navy leading-snug">{{ slot.selected.product_name }}</h3>

              <!-- Nutrient badge chips -->
              <div class="mt-3 flex flex-wrap gap-1.5">
                <span
                  v-for="badge in slot.selected.nutrient_badges"
                  :key="badge"
                  :class="badgeClass(badge)"
                >
                  {{ badgeIcon(badge) }} {{ badge }}
                </span>
              </div>
            </div>

            <!-- Swap -->
            <div class="flex shrink-0 flex-col items-end gap-3">
              <button
                v-if="slot.alternatives.length > 0"
                type="button"
                @click="toggleSwap(slot.sub_category)"
                :class="[
                  'rounded-xl px-4 py-2 font-roboto text-[13px] font-semibold transition',
                  openSwap === slot.sub_category
                    ? 'bg-navy text-white'
                    : 'bg-[#E6F0FA] text-navy hover:bg-[#D0E8FF]'
                ]"
              >
                {{ openSwap === slot.sub_category ? '✕ Close' : '⇄ Swap' }}
              </button>
            </div>
          </div>

          <!-- ── SWAP PANEL ─────────────────────────────────────────── -->
          <transition name="expand">
            <div v-if="openSwap === slot.sub_category" class="border-t border-gray-100 bg-[#F8FAFC] px-6 py-5">
              <p class="mb-3 font-roboto text-[12px] font-bold uppercase tracking-wider text-gray-400">Pick an alternative</p>
              <div class="space-y-3">
                <button
                  v-for="alt in slot.alternatives"
                  :key="alt.ingredient_code"
                  type="button"
                  @click="selectIngredient(slot.sub_category, alt)"
                  class="flex w-full items-center justify-between gap-4 rounded-2xl border-2 border-gray-100 bg-white px-4 py-3 text-left transition hover:border-navy hover:shadow-sm"
                >
                  <div class="min-w-0">
                    <span :class="tierBadgeClass(priceTier(alt.retail_price))" class="rounded-full px-2 py-0.5 text-[10px] font-bold mb-1 inline-block">
                      {{ priceTier(alt.retail_price) }}
                    </span>
                    <p class="font-roboto text-[14px] font-semibold text-navy leading-snug">{{ alt.product_name }}</p>
                    <div class="mt-1.5 flex flex-wrap gap-1">
                      <span v-for="badge in alt.nutrient_badges" :key="badge" :class="badgeClass(badge)" class="text-[10px]">
                        {{ badgeIcon(badge) }} {{ badge }}
                      </span>
                    </div>
                  </div>
                  <div class="shrink-0 text-right">
                    <p
                      v-if="alt.retail_price !== slot.selected.retail_price"
                      class="font-bold text-[16px] leading-none"
                      :class="alt.retail_price > slot.selected.retail_price ? 'text-red-500' : 'text-green-600'"
                    >
                      {{ alt.retail_price > slot.selected.retail_price ? '▲▲' : '▼▼' }}
                    </p>
                    <p class="text-[10px] text-[#396477] font-semibold mt-1">Select →</p>
                  </div>
                </button>
              </div>
            </div>
          </transition>
        </article>
      </div>

      <!-- Data resources -->
      <div class="mt-10 pt-6 border-t border-gray-200 text-[11px] text-gray-500">
        <p class="font-bold uppercase tracking-widest mb-3 text-black/60">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-black/70">Nutrition:</span>
            <a href="https://www.foodstandards.gov.au/science-data/monitoringnutrients/afcd" target="_blank" rel="noopener"
              class="hover:text-[#396477] underline decoration-gray-300 underline-offset-2 transition-colors">
              AFCD — Food Standards Australia New Zealand
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-black/70">Nutrition:</span>
            <a href="https://fdc.nal.usda.gov/" target="_blank" rel="noopener"
              class="hover:text-[#396477] underline decoration-gray-300 underline-offset-2 transition-colors">
              USDA FoodData Central
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-black/70">Food Data:</span>
            <a href="https://world.openfoodfacts.org/" target="_blank" rel="noopener"
              class="hover:text-[#396477] underline decoration-gray-300 underline-offset-2 transition-colors">
              Open Food Facts (ODbL)
            </a>
          </span>
        </div>
        <p class="mt-4 text-[10px] text-black/40 leading-relaxed">
          Grocery prices are sourced from a 2022 Australian supermarket dataset and have been adjusted to reflect 2026 prices
          using the Consumer Price Index for food and non-alcoholic beverages, as published by the Australian Bureau of Statistics
          (<a href="http://abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release"
            target="_blank" rel="noopener"
            class="underline decoration-black/20 underline-offset-2 hover:text-[#396477] transition-colors">
            ABS CPI Report, April 2026
          </a>).
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { PlannerData } from '~/pages/get-food.vue'

const props = defineProps<{
  plannerData: PlannerData | null
}>()


// ── Types ──────────────────────────────────────────────────────────────────

type ScoredIngredient = {
  ingredient_code: string
  product_name: string
  sub_category: string
  retail_price: number
  unit_price: number | null
  unit_price_unit: string | null
  health_score: number
  rec_score: number
  nutrient_badges: string[]
}

type BagSlot = {
  sub_category: string
  selected: ScoredIngredient
  alternatives: ScoredIngredient[]
}

// ── API fetch ──────────────────────────────────────────────────────────────

const config = useRuntimeConfig()

const { data: apiData, pending, error: fetchError, refresh } = await useFetch<{
  ingredients: ScoredIngredient[]
  budget_per_dish_per_person: number
}>('/recommendations', {
  method: 'POST',
  baseURL: config.public.apiBase as string,
  query: { bag_size: 15 },
  body: {
    budget: props.plannerData?.budget ?? 60,
    people: 1,
    days: 4,
    dietary_needs: (props.plannerData?.dietaryNeeds ?? []).map(n => n.toLowerCase()),
    description: props.plannerData?.description ?? null,
    dietary_goal: props.plannerData?.dietaryGoal ?? null,
  },
})

// ── Build bag slots: one per sub_category ──────────────────────────────────

const bagSlots = computed<BagSlot[]>(() => {
  if (!apiData.value?.ingredients) return []

  const grouped = new Map<string, ScoredIngredient[]>()
  for (const ing of apiData.value.ingredients) {
    const arr = grouped.get(ing.sub_category) ?? []
    arr.push(ing)
    grouped.set(ing.sub_category, arr)
  }

  return Array.from(grouped.entries()).map(([sub_category, options]) => {
    const sorted = options.slice().sort((a, b) => b.rec_score - a.rec_score)
    return { sub_category, selected: sorted[0], alternatives: sorted.slice(1) }
  })
})

// Per-sub_category overrides when user picks a swap
const overrides = reactive<Record<string, ScoredIngredient>>({})

const resolvedSlots = computed<BagSlot[]>(() =>
  bagSlots.value.map(slot => ({
    ...slot,
    selected: overrides[slot.sub_category] ?? slot.selected,
    alternatives: (overrides[slot.sub_category]
      ? [slot.selected, ...slot.alternatives.filter(a => a.ingredient_code !== overrides[slot.sub_category]?.ingredient_code)]
      : slot.alternatives
    ).slice(0, 2),
  }))
)

const openSwap = ref<string | null>(null)

const toggleSwap = (sub_category: string) => {
  openSwap.value = openSwap.value === sub_category ? null : sub_category
}

const selectIngredient = (sub_category: string, ing: ScoredIngredient) => {
  overrides[sub_category] = ing
  openSwap.value = null
}

// ── Category initial avatar ────────────────────────────────────────────────

const categoryInitial = (cat: string): string =>
  (cat || '?').trim().charAt(0).toUpperCase()

// ── Price tier helpers ─────────────────────────────────────────────────────

// Reference = total budget ÷ 5 items, so tiers scale with the user's budget.
const budgetPerItem = computed(() => (props.plannerData?.budget ?? 30) / 5)

const priceTier = (price: number): string => {
  const b = budgetPerItem.value
  if (price < b * 0.4)  return 'Very Low'
  if (price < b * 0.7)  return 'Low'
  if (price < b)        return 'Medium-Low'
  if (price < b * 1.4)  return 'Medium-High'
  return 'High'
}

const tierBadgeClass = (tier: string): string => {
  const map: Record<string, string> = {
    'Very Low':    'bg-green-100 text-green-700',
    'Low':         'bg-emerald-100 text-emerald-700',
    'Medium-Low':  'bg-yellow-100 text-yellow-700',
    'Medium-High': 'bg-orange-100 text-orange-700',
    'High':        'bg-red-100 text-red-700',
  }
  return map[tier] ?? 'bg-gray-100 text-gray-600'
}

const priceTierGuide = [
  { label: 'Very Low',    description: 'Well under budget — maximum value for your spend.' },
  { label: 'Low',         description: 'Affordable pick — comfortably within your budget.' },
  { label: 'Medium-Low',  description: 'A small step up — still fits your budget.' },
  { label: 'Medium-High', description: 'Uses most of your per-item budget — consider swapping.' },
  { label: 'High',        description: 'At the top of your budget range — best as a feature item.' },
]

// ── Nutrient badge helpers ─────────────────────────────────────────────────

const badgeIcon = (badge: string): string => {
  const map: Record<string, string> = {
    'High protein': '💪',
    'High fibre':   '🌾',
    'Low fat':      '💧',
    'Low sugar':    '🍃',
  }
  return map[badge] ?? ''
}

const badgeClass = (badge: string): string => {
  const base = 'rounded-full px-2.5 py-0.5 font-roboto text-[11px] font-semibold'
  const styles: Record<string, string> = {
    'High protein': 'bg-[#FCE4EF] text-[#B65375]',
    'High fibre':   'bg-[#DFF3D8] text-[#3E7A47]',
    'Low fat':      'bg-[#E8EEF9] text-[#526B91]',
    'Low sugar':    'bg-[#FFF1C7] text-[#B07A00]',
  }
  return `${base} ${styles[badge] ?? 'bg-gray-100 text-gray-600'}`
}

// ── Dietary goal match ─────────────────────────────────────────────────────

const matchesGoal = (ing: ScoredIngredient, goal: string | null): boolean => {
  if (!goal) return false
  const badgeMap: Record<string, string> = {
    'More protein': 'High protein',
    'More fibre':   'High fibre',
    'Less fat':     'Low fat',
    'Less sugar':   'Low sugar',
  }
  const badge = badgeMap[goal]
  if (badge) return ing.nutrient_badges.includes(badge)
  // 'Less sodium' has no badge yet — fall back to health score
  if (goal === 'Less sodium') return ing.health_score > 0.5
  return false
}
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
