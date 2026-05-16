<template>
  <TopNavigation />
  <div class="h-[72px]" />

  <div
    class="min-h-screen w-full"
    style="background: linear-gradient(180deg, #f8f9ff 0%, #dce9ff 25%, #f4f8fe 60%, #ffffff 100%); color: #0d1c2e;"
  >
    <!-- Background blobs -->
    <div aria-hidden class="pointer-events-none fixed inset-0 overflow-hidden" style="z-index:0;">
      <div class="absolute -top-40 -right-40 w-[480px] h-[480px] rounded-full blur-3xl opacity-40" style="background:#dce9ff;" />
      <div class="absolute top-1/3 -left-40 w-[380px] h-[380px] rounded-full blur-3xl opacity-20" style="background:#0d1c2e;" />
    </div>

    <main class="relative" style="z-index:1;">
      <!-- Hero section -->
      <section class="max-w-[1200px] mx-auto px-6 lg:px-10 pt-14 lg:pt-18 pb-8 text-center">
        <div
          class="inline-flex items-center gap-2 mb-5"
        >
          <span style="color:#EF6C00; font-family:'Plus Jakarta Sans', sans-serif; font-size:20px; font-style:normal; font-weight:700; line-height:15px; letter-spacing:1.8px; text-transform:uppercase;">
            DAILY CHECK-IN . 60 SEC
          </span>
        </div>
        <h1
          class="max-w-[1200px] mx-auto px-6 lg:px-10 pt-18 lg:pt-0 pb-8 text-center"
          style="color:#142741; text-align:center; font-family:'Playfair Display'; font-size:64px; font-style:normal; font-weight:800; line-height:67.2px; letter-spacing:-1.6px;"
        >
          A gentle place to care for <span style="color:#EF6C00;">your family</span>
        </h1>
        <p
          class="mt-4 mx-auto"
          style="width:576px; max-width:100%; flex-shrink:0; color:#142741; text-align:center; font-family:'Plus Jakarta Sans'; font-size:17px; font-style:normal; font-weight:500; line-height:27.2px;"
        >
          Track seven kind habits - with a focus on real, daily nutrition - in under a minute. Watch your little companion grow alongside the small things you already do.
        </p>
      </section>

      <!-- Pet + Survey side by side -->
      <section class="max-w-[1200px] mx-auto px-6 lg:px-10 pb-16">
        <div class="grid lg:grid-cols-12 gap-6 items-stretch">
          <!-- Virtual pet card -->
          <div class="lg:col-span-4 flex" style="min-height:560px;">
            <HealthTrackingVirtualPetCard
              :mood="petMood"
              :level="petLevel"
              :exp="petExp"
              :exp-to-next="EXP_TO_NEXT"
              :stage-label="currentStageObj.label"
              :is-muted="isMuted"
              class="w-full"
            />
          </div>

          <!-- Survey card -->
          <div class="lg:col-span-8 flex" style="min-height:560px;">
            <HealthTrackingSurveyCard
              v-model:stage="stage"
              :has-visited="hasVisited"
              :today-completed="todayCompleted"
              :phase="surveyPhase"
              :is-muted="isMuted"
              class="w-full"
              @start="startSurvey"
              @complete="onSurveyComplete"
              @redo="redoSurvey"
              @toggle-mute="isMuted = !isMuted"
            />
          </div>
        </div>
      </section>

      <!-- Weekly insights -->
      <section class="max-w-[1200px] mx-auto px-6 lg:px-10 py-12">
        <div class="mb-8 flex items-end justify-between flex-wrap gap-4">
          <div>
            <div class="font-body" style="font-weight:700; font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:#0d1c2e; opacity:0.6;">
              Seven-day insights
            </div>
            <h2
              class="font-display mt-2"
              style="font-size:clamp(30px,4vw,44px); color:#0d1c2e; font-weight:800; letter-spacing:-0.015em; line-height:1.05;"
            >
              Patterns, not pressure.
            </h2>
          </div>
          <p class="font-body max-w-sm" style="color:#0d1c2e; opacity:0.7; font-weight:500; font-size:14px; line-height:1.6;">
            A soft view of your week - totals, balance, and what lifted you up. Notice gently, celebrate softly.
          </p>
        </div>

        <HealthTrackingWeeklyInsights
          :week-data="weekData"
          :today-dimensions="todayDimensions"
          :today-exp="todayExp"
          :today-max-exp="todayMaxExp"
          :today-mood="todayMood"
        />
      </section>

      <!-- Encouragement cards -->
      <section class="max-w-[1200px] mx-auto px-6 lg:px-10 py-10">
        <div class="grid md:grid-cols-3 gap-5">
          <div
            v-for="card in encouragementCards"
            :key="card.title"
            class="rounded-3xl p-6 border"
            style="background:rgba(255,255,255,0.85); border-color:#dce9ff;"
          >
            <h4 class="font-display" style="font-size:19px; color:#0d1c2e; font-weight:800;">{{ card.title }}</h4>
            <p class="font-body mt-2" style="font-size:14px; color:#0d1c2e; opacity:0.7; font-weight:500; line-height:1.6;">{{ card.body }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>

  <Footer />
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

useHead({ title: 'ChereBowl - Health Tracking' })

// -- Types --
type AgeStage = 'newborns' | 'infants' | 'toddlers' | 'young_kids' | 'pre_teens'
type PetMood = 'idle' | 'happy' | 'neutral' | 'sad'
type SurveyPhase = 'intro' | 'survey' | 'done'

interface DayData {
  day: string
  date: string
  exp: number
  mood: 'happy' | 'neutral' | 'sad' | 'none'
  scores?: Record<string, number>
}

interface TodayDim {
  key: string
  label: string
  exp: number
}

// --- Constants ---
const EXP_TO_NEXT = 200
const STAGES = [
  { id: 'newborns' as AgeStage, label: 'Newborns', sub: '0-3 months' },
  { id: 'infants' as AgeStage, label: 'Infants', sub: '4-12 months' },
  { id: 'toddlers' as AgeStage, label: 'Toddlers', sub: '1-3 years' },
  { id: 'young_kids' as AgeStage, label: 'Young Kids', sub: '4-8 years' },
  { id: 'pre_teens' as AgeStage, label: 'Pre-teens', sub: '9-12 years' },
]

const LS_STAGE = 'ht_stage'
const LS_VISITED = 'ht_visited'
const LS_LEVEL = 'ht_level'
const LS_EXP = 'ht_exp'
const LS_WEEK = 'ht_week'
const LS_TODAY_DATE = 'ht_today_date'
const LS_TODAY_DATA = 'ht_today_data'
const LS_MUTED = 'ht_muted'
// Snapshot of pet EXP/level taken before today's first survey submission,
// so that redo always restores to the pre-survey baseline (no accumulation).
const LS_BASE_EXP = 'ht_base_exp'
const LS_BASE_LEVEL = 'ht_base_level'

// --- Reactive state ---
const stage = ref<AgeStage>('newborns')
const hasVisited = ref(false)
const surveyPhase = ref<SurveyPhase>('intro')
const petMood = ref<PetMood>('idle')
const petLevel = ref(1)
const petExp = ref(0)
const isMuted = ref(true)

const weekData = ref<DayData[]>(buildEmptyWeek())
const todayDimensions = ref<TodayDim[]>([])
const todayExp = ref(0)
const todayMaxExp = ref(80)
const todayMood = ref<'happy' | 'neutral' | 'sad' | 'none'>('none')
const todayCompleted = ref(false)

// --- Computed ---
const currentStageObj = computed(() => STAGES.find(s => s.id === stage.value) ?? STAGES[0])

// -- Helpers --
function todayKey(): string {
  return new Date().toISOString().slice(0, 10)
}

function buildEmptyWeek(): DayData[] {
  const names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
  const today = new Date()
  return Array.from({ length: 7 }, (_, i) => {
    const dt = new Date(today)
    dt.setDate(today.getDate() - (6 - i))
    return {
      day: names[dt.getDay()],
      date: dt.toISOString().slice(0, 10),
      exp: 0,
      mood: 'none' as const,
    }
  })
}

// Rebuild week structure around today, preserving matching dates from saved data
function reconcileWeek(saved: DayData[]): DayData[] {
  const fresh = buildEmptyWeek()
  for (const day of fresh) {
    const match = saved.find(s => s.date === day.date)
    if (match) {
      day.exp = match.exp
      day.mood = match.mood
      day.scores = match.scores
    }
  }
  return fresh
}

function ls(key: string): string | null {
  try { return localStorage.getItem(key) } catch { return null }
}

function lsSet(key: string, val: string) {
  try { localStorage.setItem(key, val) } catch { /* ignore */ }
}

function lsRemove(key: string) {
  try { localStorage.removeItem(key) } catch { /* ignore */ }
}

function checkMidnightReset() {
  const stored = ls(LS_TODAY_DATE)
  const today = todayKey()
  if (stored && stored !== today) {
    // New day - today data was already written to week on last completion; just clear daily keys
    lsSet(LS_TODAY_DATE, today)
    lsRemove(LS_TODAY_DATA)
    lsRemove(LS_BASE_EXP)
    lsRemove(LS_BASE_LEVEL)
    todayCompleted.value = false
    todayDimensions.value = []
    todayExp.value = 0
    todayMood.value = 'none'
  } else if (!stored) {
    lsSet(LS_TODAY_DATE, today)
  }
}

function loadState() {
  // Stage
  const savedStage = ls(LS_STAGE) as AgeStage | null
  if (savedStage && STAGES.some(s => s.id === savedStage)) {
    stage.value = savedStage
  }

  // Visited
  hasVisited.value = ls(LS_VISITED) === '1'

  // Pet level / exp
  const savedLevel = ls(LS_LEVEL)
  const savedExp = ls(LS_EXP)
  if (savedLevel) petLevel.value = parseInt(savedLevel) || 1
  if (savedExp) petExp.value = parseInt(savedExp) || 0

  // Sound - default to muted when no saved preference
  const savedMuted = ls(LS_MUTED)
  isMuted.value = savedMuted === null ? true : savedMuted === '1'

  // Week data - always reconcile against current 7-day window
  const savedWeek = ls(LS_WEEK)
  if (savedWeek) {
    try {
      const parsed: DayData[] = JSON.parse(savedWeek)
      if (Array.isArray(parsed)) {
        weekData.value = reconcileWeek(parsed)
      }
    } catch { /* ignore */ }
  }

  // Midnight reset check
  checkMidnightReset()

  // Today data
  const savedToday = ls(LS_TODAY_DATA)
  if (savedToday && ls(LS_TODAY_DATE) === todayKey()) {
    try {
      const data = JSON.parse(savedToday)
      todayExp.value = data.exp ?? 0
      todayMaxExp.value = data.maxExp ?? 80
      todayMood.value = data.mood ?? 'none'
      todayDimensions.value = data.dimensions ?? []
      todayCompleted.value = true
      // Restore pet mood from today's result
      petMood.value = data.mood === 'happy' ? 'happy' : data.mood === 'sad' ? 'sad' : 'neutral'
    } catch { /* ignore */ }
  }
}

function saveState() {
  lsSet(LS_STAGE, stage.value)
  lsSet(LS_VISITED, hasVisited.value ? '1' : '0')
  lsSet(LS_LEVEL, String(petLevel.value))
  lsSet(LS_EXP, String(petExp.value))
  lsSet(LS_MUTED, isMuted.value ? '1' : '0')
  lsSet(LS_WEEK, JSON.stringify(weekData.value))
}

// --- Survey flow ---
function startSurvey() {
  hasVisited.value = true
  surveyPhase.value = 'survey'
  // Pet stays idle during survey
}

function onSurveyComplete(payload: {
  totalExp: number
  maxExp: number
  dimensionScores: Record<string, number>
  answers: { id: string; dimension: string; exp: number }[]
}) {
  const { totalExp, maxExp, dimensionScores, answers } = payload

  // Classify mood from EXP percentage
  const pct = maxExp > 0 ? totalExp / maxExp : 0
  const mood: 'happy' | 'neutral' | 'sad' = pct >= 0.7 ? 'happy' : pct >= 0.4 ? 'neutral' : 'sad'

  // EXP snapshot: save baseline before first submission; restore it on any redo
  const savedBase = ls(LS_BASE_EXP)
  if (savedBase === null) {
    // First submission today - record baseline so redo can restore it
    lsSet(LS_BASE_EXP, String(petExp.value))
    lsSet(LS_BASE_LEVEL, String(petLevel.value))
  } else {
    // Redo - restore to pre-today baseline to avoid accumulation
    const baseExp = parseInt(savedBase)
    const baseLevel = parseInt(ls(LS_BASE_LEVEL) ?? '1')
    if (!isNaN(baseExp)) petExp.value = baseExp
    if (!isNaN(baseLevel)) petLevel.value = baseLevel
  }

  // Add today's EXP on top of the (possibly restored) baseline
  let newExp = petExp.value + totalExp
  let newLevel = petLevel.value
  while (newExp >= EXP_TO_NEXT) {
    newExp -= EXP_TO_NEXT
    newLevel++
  }
  petExp.value = newExp
  petLevel.value = newLevel
  petMood.value = mood

  // Today data
  const dimLabelMap: Record<string, string> = {
    mood: 'Mood', rest: 'Rest', exercise: 'Exercise',
    self_discipline: 'Self-care', vitamin: 'Vitamins', protein: 'Protein', carb: 'Energy',
  }
  const dimMap: Record<string, number[]> = {}
  for (const a of answers) {
    if (!dimMap[a.dimension]) dimMap[a.dimension] = []
    dimMap[a.dimension].push(a.exp)
  }
  const dims: TodayDim[] = Object.entries(dimMap).map(([k, vals]) => ({
    key: k,
    label: dimLabelMap[k] ?? k,
    exp: Math.round(vals.reduce((a, b) => a + b, 0) / vals.length),
  }))

  todayDimensions.value = dims
  todayExp.value = totalExp
  todayMaxExp.value = maxExp
  todayMood.value = mood
  todayCompleted.value = true

  // Save today data to localStorage
  const todayPayload = { exp: totalExp, maxExp, mood, dimensions: dims }
  lsSet(LS_TODAY_DATA, JSON.stringify(todayPayload))
  lsSet(LS_TODAY_DATE, todayKey())

  // Update week data for today (last slot or today's matching date)
  const todayStr = todayKey()
  const weekIdx = weekData.value.findIndex(d => d.date === todayStr)
  const weekScores: Record<string, number> = {}
  for (const [k, vals] of Object.entries(dimMap)) {
    weekScores[k] = Math.round(vals.reduce((a, b) => a + b, 0) / vals.length)
  }
  const updatedDay: DayData = {
    day: weekData.value[weekIdx >= 0 ? weekIdx : 6]?.day ?? 'Today',
    date: todayStr,
    exp: totalExp,
    mood,
    scores: weekScores,
  }
  if (weekIdx >= 0) {
    weekData.value[weekIdx] = updatedDay
  } else {
    weekData.value[6] = updatedDay
  }

  surveyPhase.value = 'done'
  saveState()
}

function redoSurvey() {
  // Restore pet EXP/level to the pre-today baseline
  const savedBase = ls(LS_BASE_EXP)
  if (savedBase !== null) {
    const baseExp = parseInt(savedBase)
    const baseLevel = parseInt(ls(LS_BASE_LEVEL) ?? '1')
    if (!isNaN(baseExp)) petExp.value = baseExp
    if (!isNaN(baseLevel)) petLevel.value = baseLevel
  }

  // Clear all of today's in-memory data
  todayDimensions.value = []
  todayExp.value = 0
  todayMood.value = 'none'
  todayCompleted.value = false

  // Clear today's persisted data (NOT the base snapshot - keep it for the next submission)
  lsRemove(LS_TODAY_DATA)

  // Reset today's slot in the week chart
  const todayStr = todayKey()
  const weekIdx = weekData.value.findIndex(d => d.date === todayStr)
  if (weekIdx >= 0) {
    weekData.value[weekIdx] = {
      day: weekData.value[weekIdx].day,
      date: todayStr,
      exp: 0,
      mood: 'none',
    }
  }

  surveyPhase.value = 'intro'
  petMood.value = 'idle'
  saveState()
}

// --- Watchers ---
watch(stage, (val) => { lsSet(LS_STAGE, val) })
watch(isMuted, (val) => { lsSet(LS_MUTED, val ? '1' : '0') })

// --- Lifecycle ---
onMounted(() => {
  loadState()
})

// --- Encouragement cards ---
const encouragementCards = [
  {
    title: 'For the quiet hours',
    body: 'Tiny rituals after the kids sleep - a glass of water, two minutes of stillness - count more than you think.',
  },
  {
    title: 'On the harder days',
    body: 'Bright days and heavy days both belong. Your companion loves you the same - your only job is to keep showing up gently.',
  },
  {
    title: 'Together with little ones',
    body: 'Want to make it a family habit? Invite your child to pick one answer with you. Connection counts.',
  },
]
</script>
