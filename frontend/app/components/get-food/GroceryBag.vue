<template>
  <section id="grocery-recommendations" class="w-full bg-[#F5F7FA] py-16 lg:py-20">
    <div class="mx-auto max-w-3xl px-5 lg:px-8">

      <!-- ── HEADER ──────────────────────────────────────────────────── -->
      <div class="mb-6">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-bold uppercase tracking-widest text-[#396477]">Your Grocery Bag</p>
            <h2 class="mt-1 font-volkhov text-[28px] font-bold text-navy lg:text-[38px]">
              <span class="italic text-coral">One wholesome shop</span>
              <span> for {{ props.plannerData?.days ?? 4 }} days</span>
            </h2>
          </div>
        </div>
        <p class="mt-1 font-roboto text-[14px] text-gray-500">
          Top picks globally ranked for your
          <strong>${{ props.plannerData?.budget }} AUD</strong> budget,
          {{ props.plannerData?.people ?? 2 }} {{ (props.plannerData?.people ?? 2) === 1 ? 'person' : 'people' }}.
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
            <p class="mb-2 text-[12px] font-bold uppercase tracking-wider text-gray-400">Relative cost — six levels</p>
            <div class="space-y-1">
              <div v-for="tier in priceTierGuide" :key="tier.label" class="flex items-center gap-2 text-[12px]">
                <span :class="tierBadgeClass(tier.label)" class="shrink-0 rounded-full px-2 py-0.5 text-[10px] font-bold">{{ tier.symbol }} {{ tier.label }}</span>
                <span class="text-gray-500">{{ tier.description }}</span>
              </div>
            </div>
          </div>
        </div>
      </details>

      <!-- ── LOADING ─────────────────────────────────────────────────── -->
      <div v-if="pending" class="space-y-4">
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
              <!-- Sub-category label + price tier badge -->
              <div class="flex flex-wrap items-center gap-2 mb-1">
                <p class="font-roboto text-[11px] font-bold uppercase tracking-wider text-[#396477]">{{ slot.sub_category }}</p>
                <span :class="tierBadgeClass(priceTier(slot.selected.retail_price))" class="rounded-full px-2 py-0.5 text-[10px] font-bold">
                  {{ priceTierSymbol(slot.selected.retail_price) }} {{ priceTier(slot.selected.retail_price) }}
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

            <!-- Price + swap -->
            <div class="flex shrink-0 flex-col items-end gap-3">
              <div class="text-right">
                <p class="font-roboto text-[18px] font-bold text-navy">${{ slot.selected.retail_price.toFixed(2) }}</p>
                <p class="text-[11px] text-gray-400">retail est.</p>
              </div>
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
                    <div class="flex flex-wrap items-center gap-1.5 mb-1">
                      <span :class="tierBadgeClass(priceTier(alt.retail_price))" class="rounded-full px-2 py-0.5 text-[10px] font-bold">
                        {{ priceTierSymbol(alt.retail_price) }} {{ priceTier(alt.retail_price) }}
                      </span>
                    </div>
                    <p class="font-roboto text-[14px] font-semibold text-navy leading-snug">{{ alt.product_name }}</p>
                    <div class="mt-1.5 flex flex-wrap gap-1">
                      <span v-for="badge in alt.nutrient_badges" :key="badge" :class="badgeClass(badge)" class="text-[10px]">
                        {{ badgeIcon(badge) }} {{ badge }}
                      </span>
                    </div>
                  </div>
                  <div class="shrink-0 text-right">
                    <p class="font-roboto text-[15px] font-bold text-navy">${{ alt.retail_price.toFixed(2) }}</p>
                    <p class="text-[10px] text-[#396477] font-semibold">Select →</p>
                  </div>
                </button>
              </div>
            </div>
          </transition>
        </article>
      </div>

      <!-- ── RUNNING TOTAL ──────────────────────────────────────────── -->
      <div v-if="!pending && !fetchError && resolvedSlots.length > 0" class="mt-6 rounded-2xl bg-navy px-6 py-5 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-roboto text-[12px] font-bold uppercase tracking-wider text-[#8BAFC8]">Estimated basket total</p>
            <p class="mt-0.5 font-roboto text-[11px] text-[#8BAFC8]">Sum of selected ingredients · swap to update</p>
          </div>
          <p class="font-volkhov text-[32px] font-bold">${{ runningTotal.toFixed(2) }}</p>
        </div>
      </div>

      <!-- ── FOOTER NOTE ─────────────────────────────────────────────── -->
      <p v-if="!pending && !fetchError" class="mt-6 text-center font-roboto text-[12px] text-gray-400">
        Note: These are decision-support suggestions, not live prices. Relative cost levels reflect typical Australian supermarket ranges and may vary by store and season.
      </p>
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
    people: props.plannerData?.people ?? 2,
    days: props.plannerData?.days ?? 4,
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

const runningTotal = computed(() =>
  resolvedSlots.value.reduce((sum, slot) => sum + slot.selected.retail_price, 0)
)

// ── Category initial avatar ────────────────────────────────────────────────

const categoryInitial = (cat: string): string =>
  (cat || '?').trim().charAt(0).toUpperCase()

// ── Price tier helpers ─────────────────────────────────────────────────────

const priceTier = (price: number): string => {
  if (price < 5)   return 'Very Low'
  if (price < 10)  return 'Low'
  if (price < 15)  return 'Medium-Low'
  if (price < 25)  return 'Medium-High'
  if (price < 40)  return 'High'
  return 'Very High'
}

const priceTierSymbol = (price: number): string => {
  const map: Record<string, string> = {
    'Very Low': '$', 'Low': '$', 'Medium-Low': '$$',
    'Medium-High': '$$', 'High': '$$$', 'Very High': '$$$',
  }
  return map[priceTier(price)] ?? '$'
}

const tierBadgeClass = (tier: string): string => {
  const map: Record<string, string> = {
    'Very Low':    'bg-green-100 text-green-700',
    'Low':         'bg-emerald-100 text-emerald-700',
    'Medium-Low':  'bg-yellow-100 text-yellow-700',
    'Medium-High': 'bg-orange-100 text-orange-700',
    'High':        'bg-red-100 text-red-700',
    'Very High':   'bg-purple-100 text-purple-700',
  }
  return map[tier] ?? 'bg-gray-100 text-gray-600'
}

const priceTierGuide = [
  { label: 'Very Low',    symbol: '$',   description: 'AU$1–5 · Pantry staples & long-life basics — easy on any budget.' },
  { label: 'Low',         symbol: '$',   description: 'AU$5–10 · Everyday affordable picks for most families.' },
  { label: 'Medium-Low',  symbol: '$$',  description: 'AU$10–15 · A small step up — still gentle on the shop.' },
  { label: 'Medium-High', symbol: '$$',  description: 'AU$15–25 · A balanced splurge — fits a comfortable budget.' },
  { label: 'High',        symbol: '$$$', description: 'AU$25–40 · Premium ingredients — best as occasional features.' },
  { label: 'Very High',   symbol: '$$$', description: 'AU$40+ · Luxury or specialty items — consider swaps to save.' },
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
