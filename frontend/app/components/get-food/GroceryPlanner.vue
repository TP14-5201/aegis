<template>
  <section id="grocery-planner" class="w-full bg-white py-16 lg:py-20">
    <div class="mx-auto max-w-2xl px-5">
      <form
        @submit.prevent="handleSubmit"
        novalidate
        class="rounded-3xl bg-white p-8 shadow-[0_20px_60px_rgba(0,0,0,0.1)] lg:p-12"
      >
        <!-- Section label + heading -->
        <p class="text-sm font-bold uppercase tracking-widest text-coral">Get Food</p>
        <h2 class="mt-2 font-volkhov text-[26px] font-bold text-navy lg:text-[36px]">
          Tell us what you're <em class="text-[#396477] not-italic">shopping for</em>
        </h2>

        <!-- Step progress dots -->
        <div class="mt-6 flex items-center gap-2">
          <div
            v-for="n in TOTAL_STEPS"
            :key="n"
            :class="[
              'h-2 rounded-full transition-all duration-300',
              n === step
                ? 'w-8 bg-navy'
                : n < step
                  ? 'w-2 bg-[#396477]'
                  : 'w-2 bg-gray-200'
            ]"
          />
          <span class="ml-auto text-xs text-gray-400 font-roboto">{{ step }} / {{ TOTAL_STEPS }}</span>
        </div>

        <!-- ── STEP 1: Budget ───────────────────────────────────────────── -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="step === 1" key="step1" class="mt-10">
            <p class="font-roboto text-[13px] font-bold uppercase tracking-wider text-gray-400">Step 1 of {{ TOTAL_STEPS }}</p>
            <h3 class="mt-2 font-volkhov text-[24px] font-bold text-navy lg:text-[30px]">
              What's your budget for this shop?
            </h3>
            <p class="mt-2 font-roboto text-[14px] text-gray-500">Drag to set your total grocery budget in AUD.</p>

            <!-- Budget display -->
            <div class="mt-8 flex flex-col items-center">
              <div class="relative">
                <span class="font-volkhov text-[64px] font-bold text-navy leading-none">${{ budget }}</span>
                <span class="absolute -right-8 bottom-3 font-roboto text-[14px] font-semibold text-gray-400">AUD</span>
              </div>
            </div>

            <!-- Slider -->
            <div class="mt-6 px-2">
              <input
                type="range"
                v-model.number="budget"
                :min="BUDGET_MIN"
                :max="BUDGET_MAX"
                :step="1"
                class="budget-slider w-full"
                :style="`--pct: ${budgetPct}%`"
              />
              <div class="mt-2 flex justify-between font-roboto text-[11px] text-gray-400">
                <span>${{ BUDGET_MIN }}</span>
                <span>${{ BUDGET_MAX }}</span>
              </div>
            </div>
          </div>
        </transition>

        <!-- ── STEP 2: People + Days ───────────────────────────────────── -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="step === 2" key="step2" class="mt-10">
            <p class="font-roboto text-[13px] font-bold uppercase tracking-wider text-gray-400">Step 2 of {{ TOTAL_STEPS }}</p>
            <h3 class="mt-2 font-volkhov text-[24px] font-bold text-navy lg:text-[30px]">
              Who are you cooking for?
            </h3>
            <p class="mt-2 font-roboto text-[14px] text-gray-500">Set your household size and how many days this grocery bag should last.</p>

            <div class="mt-10 space-y-8">
              <!-- People -->
              <div>
                <p class="font-roboto text-[15px] font-semibold text-navy">Number of people</p>
                <div class="mt-4 flex items-center gap-5">
                  <button
                    type="button"
                    @click="people = Math.max(1, people - 1)"
                    class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-2xl font-bold text-navy transition hover:bg-gray-200 active:scale-95"
                  >−</button>
                  <div class="flex min-w-[3rem] flex-col items-center">
                    <span class="font-volkhov text-[42px] font-bold text-navy leading-none">{{ people }}</span>
                    <span class="mt-1 font-roboto text-[12px] text-gray-400">{{ people === 1 ? 'person' : 'people' }}</span>
                  </div>
                  <button
                    type="button"
                    @click="people = Math.min(20, people + 1)"
                    class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-2xl font-bold text-navy transition hover:bg-gray-200 active:scale-95"
                  >+</button>
                </div>
              </div>

              <div class="border-t border-gray-100" />

              <!-- Days -->
              <div>
                <p class="font-roboto text-[15px] font-semibold text-navy">Number of days</p>
                <div class="mt-4 flex items-center gap-5">
                  <button
                    type="button"
                    @click="days = Math.max(1, days - 1)"
                    class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-2xl font-bold text-navy transition hover:bg-gray-200 active:scale-95"
                  >−</button>
                  <div class="flex min-w-[3rem] flex-col items-center">
                    <span class="font-volkhov text-[42px] font-bold text-navy leading-none">{{ days }}</span>
                    <span class="mt-1 font-roboto text-[12px] text-gray-400">{{ days === 1 ? 'day' : 'days' }}</span>
                  </div>
                  <button
                    type="button"
                    @click="days = Math.min(14, days + 1)"
                    class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-2xl font-bold text-navy transition hover:bg-gray-200 active:scale-95"
                  >+</button>
                </div>
                <p class="mt-3 font-roboto text-[12px] text-gray-400">
                  Daily budget per person: <strong class="text-navy">${{ bdpp.toFixed(2) }}</strong>
                </p>
              </div>
            </div>
          </div>
        </transition>

        <!-- ── STEP 3: Dietary goal + restrictions + description ────────── -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="step === 3" key="step3" class="mt-10">
            <p class="font-roboto text-[13px] font-bold uppercase tracking-wider text-gray-400">Step 3 of {{ TOTAL_STEPS }}</p>
            <h3 class="mt-2 font-volkhov text-[24px] font-bold text-navy lg:text-[30px]">
              Tell us your preferences
            </h3>
            <p class="mt-2 font-roboto text-[14px] text-gray-500">Skip any section that doesn't apply.</p>

            <!-- Dietary goal -->
            <div class="mt-8">
              <p class="font-roboto text-[14px] font-semibold text-navy">
                Dietary goal
                <span class="ml-1 font-normal text-gray-400">(optional)</span>
              </p>
              <p class="mt-1 font-roboto text-[12px] text-gray-500">Matching picks will be highlighted in the results.</p>
              <div class="mt-3 flex flex-wrap gap-2">
                <button
                  v-for="goal in dietaryGoals"
                  :key="goal"
                  type="button"
                  @click="toggleGoal(goal)"
                  :class="[
                    'rounded-full px-4 py-2 font-roboto text-[13px] font-semibold transition',
                    dietaryGoal === goal
                      ? 'bg-[#396477] text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ goal }}
                </button>
              </div>
            </div>

            <!-- Dietary restrictions -->
            <div class="mt-8">
              <p class="font-roboto text-[14px] font-semibold text-navy">
                Dietary restrictions
                <span class="ml-1 font-normal text-gray-400">(optional)</span>
              </p>
              <div class="mt-3 flex flex-wrap gap-3">
                <button
                  v-for="need in dietaryOptions"
                  :key="need"
                  type="button"
                  @click="toggleDietaryNeed(need)"
                  :class="[
                    'flex items-center gap-2 rounded-2xl border-2 px-5 py-3 font-roboto text-[14px] font-semibold transition',
                    dietaryNeeds.includes(need)
                      ? 'border-navy bg-navy text-white'
                      : 'border-gray-200 bg-white text-gray-700 hover:border-gray-400'
                  ]"
                >
                  <span>{{ dietaryIcon(need) }}</span>
                  <span>{{ need }}</span>
                </button>
              </div>
            </div>

            <!-- Free-text description -->
            <div class="mt-8">
              <p class="font-roboto text-[14px] font-semibold text-navy">
                Describe your ideal shop
                <span class="ml-1 font-normal text-gray-400">(optional)</span>
              </p>
              <p class="mt-1 font-roboto text-[12px] text-gray-500">Tell us anything — cuisine, flavours, cooking style. We'll personalise your results.</p>
              <div class="mt-3 flex flex-wrap gap-2">
                <button
                  v-for="chip in PROMPT_CHIPS"
                  :key="chip"
                  type="button"
                  @click="appendChip(chip)"
                  class="rounded-full bg-gray-100 px-3 py-1.5 font-roboto text-[12px] text-gray-700 hover:bg-gray-200 transition"
                >+ {{ chip }}</button>
              </div>
              <textarea
                v-model="descriptionInput"
                :maxlength="DESCRIPTION_MAX"
                rows="3"
                placeholder="e.g. I love spicy food and prefer quick Asian-style meals..."
                class="mt-3 w-full rounded-xl border border-gray-200 px-4 py-3 font-roboto text-[14px] text-gray-700 outline-none focus:ring-2 focus:ring-[#B8DEFF] resize-none"
              />
              <div class="mt-1 flex justify-between font-roboto text-[11px] text-gray-400">
                <button type="button" @click="descriptionInput = ''; step++" class="text-[#396477] hover:underline">Skip →</button>
                <span>{{ descriptionInput.length }} / {{ DESCRIPTION_MAX }}</span>
              </div>
            </div>
          </div>
        </transition>

        <!-- ── STEP 4: Summary ────────────────────────────────────────── -->
        <transition name="fade-slide" mode="out-in">
          <div v-if="step === 4" key="step4" class="mt-10">
            <p class="font-roboto text-[13px] font-bold uppercase tracking-wider text-gray-400">Step 4 of {{ TOTAL_STEPS }}</p>
            <h3 class="mt-2 font-volkhov text-[24px] font-bold text-navy lg:text-[30px]">
              Ready to build your bag?
            </h3>
            <p class="mt-2 font-roboto text-[14px] text-gray-500">
              Here's a summary of your selections. Hit "Suggest options" to see personalised picks.
            </p>

            <!-- Summary card -->
            <div class="mt-8 rounded-2xl bg-[#F0F6FF] p-5">
              <p class="font-roboto text-[12px] font-bold uppercase tracking-wider text-[#396477]">Your selections</p>
              <div class="mt-3 space-y-2 font-roboto text-[13px] text-navy">
                <div class="flex justify-between">
                  <span class="text-gray-500">Budget</span>
                  <strong>${{ budget }} AUD</strong>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">People</span>
                  <strong>{{ people }}</strong>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Days</span>
                  <strong>{{ days }}</strong>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Goal</span>
                  <strong>{{ dietaryGoal ?? 'None' }}</strong>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Restrictions</span>
                  <strong>{{ dietaryNeeds.length ? dietaryNeeds.join(', ') : 'None' }}</strong>
                </div>
                <div class="flex justify-between gap-4">
                  <span class="text-gray-500 shrink-0">Description</span>
                  <strong class="text-right truncate max-w-[60%]">{{ descriptionInput.trim() || 'None' }}</strong>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <!-- ── NAVIGATION ─────────────────────────────────────────────── -->
        <div class="mt-10 flex items-center justify-between gap-4 border-t border-gray-100 pt-6">
          <button
            v-if="step > 1"
            type="button"
            @click="handleBack"
            class="font-roboto text-[14px] font-semibold text-gray-500 hover:text-navy transition"
          >
            ← {{ props.showingResults && step === 4 ? 'Edit selections' : 'Back' }}
          </button>
          <div v-else />

          <button
            v-if="step < TOTAL_STEPS"
            type="button"
            @click="step++"
            class="flex items-center gap-2 h-[52px] px-8 rounded-[16px] bg-navy text-white font-roboto font-bold text-[15px] transition-all hover:-translate-y-0.5 hover:bg-[#182d47] active:translate-y-0"
          >
            Continue →
          </button>

          <button
            v-else
            type="submit"
            class="flex items-center gap-2 h-[52px] px-8 rounded-[16px] bg-[#396477] text-white font-roboto font-bold text-[15px] transition-all hover:-translate-y-0.5 hover:bg-[#2d5262] active:translate-y-0"
          >
            ✦ Suggest options
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { PlannerData } from '~/pages/get-food.vue'

const props = defineProps<{
  showingResults?: boolean
}>()

const BUDGET_MIN = 1
const BUDGET_MAX = 50
const TOTAL_STEPS = 4

const step = ref(1)
const budget = ref(30)
const people = ref(2)
const days = ref(4)
const descriptionInput = ref('')
const dietaryGoal = ref<string | null>(null)
const dietaryNeeds = ref<string[]>([])

const DESCRIPTION_MAX = 300
const PROMPT_CHIPS = [
  'I love spicy food',
  'I prefer Asian-style meals',
  'No onion or garlic',
  'Kid-friendly meals',
  'High protein focus',
  'Quick to prepare',
]

const dietaryGoals = ['More fibre', 'More protein', 'Less fat', 'Less sugar', 'Less sodium']
const dietaryOptions = ['Vegetarian', 'Vegan', 'Gluten-free', 'Dairy-free', 'Halal']

const emit = defineEmits<{
  submitPlanner: [data: PlannerData]
  resetPlanner: []
}>()

// ── Budget slider helpers ──────────────────────────────────────────────────

const budgetPct = computed(() =>
  Math.round(((budget.value - BUDGET_MIN) / (BUDGET_MAX - BUDGET_MIN)) * 100)
)

const TIERS = [
  { max: 25,  label: 'Very Low',    hint: 'Pantry staples & long-life basics — easy on any budget.',          badge: 'bg-green-100 text-green-700'    },
  { max: 50,  label: 'Low',         hint: 'Everyday affordable picks for most families.',                      badge: 'bg-emerald-100 text-emerald-700' },
  { max: 75,  label: 'Medium-Low',  hint: 'A small step up — still gentle on the shop.',                       badge: 'bg-yellow-100 text-yellow-700'   },
  { max: 125, label: 'Medium-High', hint: 'A balanced splurge — fits a comfortable budget.',                   badge: 'bg-orange-100 text-orange-700'   },
  { max: 200, label: 'High',        hint: 'Premium ingredients — best as occasional features.',                badge: 'bg-red-100 text-red-700'         },
  { max: 999, label: 'Very High',   hint: 'Luxury or specialty items — consider swaps to save.',              badge: 'bg-purple-100 text-purple-700'   },
]

const currentTier = computed(() => TIERS.find(t => budget.value <= t.max) ?? TIERS[TIERS.length - 1])
const currentTierLabel = computed(() => currentTier.value.label)
const currentTierHint = computed(() => currentTier.value.hint)
const tierBadgeClass = computed(() => currentTier.value.badge)

// ── Per-person per-dish budget ─────────────────────────────────────────────

const bdpp = computed(() => budget.value / Math.max(people.value, 1) / Math.max(days.value, 1))

// ── Description chip helper ────────────────────────────────────────────────

const appendChip = (chip: string) => {
  const cur = descriptionInput.value.trim()
  descriptionInput.value = cur ? `${cur} ${chip}` : chip
}

// ── Dietary icons ──────────────────────────────────────────────────────────

const dietaryIcon = (need: string) => {
  const map: Record<string, string> = {
    Vegetarian: '🌿', Vegan: '🌱', 'Gluten-free': '🌾', 'Dairy-free': '🥛', Halal: '☪️',
  }
  return map[need] ?? ''
}

// ── Toggles ────────────────────────────────────────────────────────────────

const toggleGoal = (goal: string) => {
  dietaryGoal.value = dietaryGoal.value === goal ? null : goal
}

const toggleDietaryNeed = (need: string) => {
  if (dietaryNeeds.value.includes(need)) {
    dietaryNeeds.value = dietaryNeeds.value.filter(n => n !== need)
  } else {
    dietaryNeeds.value.push(need)
  }
}

// ── Navigation ────────────────────────────────────────────────────────────

const handleBack = () => {
  if (props.showingResults && step.value === 4) {
    step.value = 1
    emit('resetPlanner')
  } else {
    step.value--
  }
}

// ── Submit ─────────────────────────────────────────────────────────────────

const handleSubmit = () => {
  emit('submitPlanner', {
    budget: budget.value,
    people: people.value,
    days: days.value,
    dietaryNeeds: dietaryNeeds.value,
    dietaryGoal: dietaryGoal.value,
    description: descriptionInput.value.trim() || null,
    budgetTier: currentTierLabel.value,
  })
}
</script>

<style scoped>
/* Fade + slide transition between steps */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(16px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-16px);
}

/* Budget range slider */
.budget-slider {
  -webkit-appearance: none;
  appearance: none;
  height: 6px;
  border-radius: 9999px;
  outline: none;
  cursor: pointer;
  background: linear-gradient(
    to right,
    #0D1C2E 0%,
    #0D1C2E var(--pct),
    #E5E7EB var(--pct),
    #E5E7EB 100%
  );
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0D1C2E;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  cursor: pointer;
  transition: transform 0.15s ease;
}

.budget-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.budget-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0D1C2E;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  cursor: pointer;
}
</style>
