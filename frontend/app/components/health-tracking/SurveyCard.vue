<template>
  <div
    class="w-full rounded-3xl border shadow-xl flex flex-col overflow-hidden"
    style="background: #ffffff; border-color: #dce9ff; min-height: 560px;"
  >
    <!-- Card header -->
    <div
      class="px-8 pt-7 pb-4 flex items-center justify-between border-b gap-3 flex-wrap"
      style="border-color: #eef4fb;"
    >
      <div>
        <div class="font-body" style="color: #EF6C00; font-family: 'Plus Jakarta Sans'; font-size: 12px; font-style: normal; font-weight: 800; line-height: 15px; letter-spacing: 1.8px; text-transform: uppercase;">
          {{ headerKicker }}
        </div>
        <h2 class="font-display mt-1" style="font-size: 22px; color: #0d1c2e; font-weight: 800; letter-spacing: -0.01em;">
          {{ headerTip }}
        </h2>
      </div>
      <div class="flex items-center gap-3">
        <!-- Sound toggle - top right of survey card -->
        <button
          @click="$emit('toggleMute')"
          class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border font-body transition-colors"
          :style="isMuted
            ? 'background:#f4f8fe; border-color:#dce9ff; color:#0d1c2e; opacity:0.55;'
            : 'background:#0d1c2e; border-color:#0d1c2e; color:#dce9ff;'"
          :title="isMuted ? 'Unmute sounds' : 'Mute sounds'"
        >
          <svg v-if="!isMuted" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.536 8.464a5 5 0 010 7.072M12 6.5v11M9 9.5l-2.5 2.5H4v3h2.5L9 17.5" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
          </svg>
          <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.06em;">{{ isMuted ? 'Sound off' : 'Sound on' }}</span>
        </button>

        <!-- Stage chip (return visits, not during survey) -->
        <div v-if="hasVisited && phase !== 'survey'" class="relative">
          <button
            @click="stageDropOpen = !stageDropOpen"
            class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border font-body"
            style="background:#dce9ff; color:#0d1c2e; border-color:#0d1c2e; font-weight:700; font-size:12px; letter-spacing:0.06em;"
          >
            <span style="text-transform:uppercase;">{{ currentStageObj.label }}</span>
            <span style="opacity:0.6; font-weight:700; font-size:10px;">{{ currentStageObj.sub }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <Transition
            enter-active-class="transition duration-150 ease-out"
            enter-from-class="opacity-0 -translate-y-1 scale-95"
            enter-to-class="opacity-100 translate-y-0 scale-100"
            leave-active-class="transition duration-100 ease-in"
            leave-from-class="opacity-100 translate-y-0 scale-100"
            leave-to-class="opacity-0 -translate-y-1 scale-95"
          >
            <div
              v-if="stageDropOpen"
              class="absolute right-0 mt-2 w-60 rounded-2xl border shadow-2xl z-30 overflow-hidden"
              style="background:white; border-color:#dce9ff;"
            >
              <div class="px-4 py-2.5 border-b" style="border-color:#eef4fb;">
                <div class="font-body" style="font-weight:700; font-size:10px; letter-spacing:0.14em; text-transform:uppercase; color:#0d1c2e; opacity:0.55;">
                  Change age stage
                </div>
              </div>
              <div class="py-1">
                <button
                  v-for="s in STAGES"
                  :key="s.id"
                  @click="selectStage(s.id)"
                  class="w-full flex items-center justify-between px-4 py-2 font-body hover:bg-[#f4f8fe] transition-colors"
                  :style="{ color:'#0d1c2e', fontWeight: modelStage === s.id ? 800 : 600, fontSize:'13px' }"
                >
                  <span>
                    {{ s.label }}
                    <span style="opacity:0.55; font-weight:600; margin-left:8px; font-size:11px;">{{ s.sub }}</span>
                  </span>
                  <svg v-if="modelStage === s.id" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>

    <!-- Card body -->
    <div class="flex-1 px-8 py-7 overflow-y-auto">

      <!-- INTRO phase -->
      <Transition name="fade-slide" mode="out-in">
        <div v-if="phase === 'intro'" key="intro" class="h-full flex flex-col">
          <h3 class="font-display" style="font-size:28px; color:#0d1c2e; font-weight:800; letter-spacing:-0.01em;">
            Ready when you are.
          </h3>
          <p class="font-body mt-3 max-w-lg" style="font-size:15px; color:#0d1c2e; opacity:0.7; font-weight:500; line-height:1.6;">
            No right answers - just a soft check-in with how today actually felt. Your companion grows alongside you.
          </p>

          <!-- First visit: Stage picker -->
          <div v-if="!hasVisited" class="mt-7">
            <div class="font-body mb-3" style="color:#0d1c2e; opacity:0.6; font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">
              Who are we caring for today?
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-5 gap-2">
              <button
                v-for="s in STAGES"
                :key="s.id"
                @click="$emit('update:stage', s.id)"
                class="rounded-xl border-2 px-2 py-3 text-center transition-all duration-200"
                :style="modelStage === s.id
                  ? 'background:#0d1c2e; color:#dce9ff; border-color:#0d1c2e;'
                  : 'background:white; color:#0d1c2e; border-color:#dce9ff;'"
              >
                <div class="font-display" style="font-weight:800; font-size:12px; line-height:1.1;">{{ s.label }}</div>
                <div class="font-body mt-0.5" style="font-weight:700; font-size:9px; opacity:0.7; letter-spacing:0.05em;">{{ s.sub }}</div>
              </button>
            </div>
          </div>

          <!-- Return visit: show current stage -->
          <div v-else class="mt-7 flex items-center gap-3 p-4 rounded-2xl" style="background:#f4f8fe;">
            <span class="font-body" style="font-weight:700; font-size:13px; color:#0d1c2e; opacity:0.7;">Caring for:</span>
            <span class="px-3 py-1 rounded-full font-body" style="background:#0d1c2e; color:#dce9ff; font-weight:700; font-size:12px; text-transform:uppercase; letter-spacing:0.06em;">
              {{ currentStageObj.label }}
            </span>
            <span class="font-body" style="font-weight:600; font-size:11px; color:#0d1c2e; opacity:0.45;">Use the chip above to change</span>
          </div>

          <!-- Today completed banner -->
          <div v-if="todayCompleted" class="mt-4 flex items-center gap-3 p-4 rounded-2xl" style="background:#f0fdf4; border: 1px solid #bbf7d0;">
            <svg class="w-5 h-5 text-green-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="font-body" style="font-size:13px; font-weight:700; color:#15803d;">
              Today's check-in is done! You can redo it below.
            </span>
          </div>

          <div class="mt-auto pt-10 flex flex-col items-center gap-4">
            <button
              @click="$emit('start')"
              :disabled="!modelStage"
              class="inline-flex items-center gap-2 px-7 py-3.5 rounded-full shadow-xl font-body transition-all hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
              style="background:#0d1c2e; color:#dce9ff; font-weight:700; font-size:15px;"
            >
              {{ todayCompleted ? 'Redo today\'s check-in' : 'Begin today\'s check-in' }}
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
            <div class="flex items-center gap-2 font-body" style="color:#0d1c2e; font-weight:700; font-size:12px; opacity:0.65;">
              <span class="inline-block w-2 h-2 rounded-full" style="background:#7fe3c4;" />
              Private - judgment-free - yours
            </div>
          </div>
        </div>

        <!-- SURVEY phase -->
        <div v-else-if="phase === 'survey'" key="survey" class="w-full">
          <!-- Progress bar -->
          <div class="mb-5">
            <div class="flex items-center justify-between mb-2 font-body" style="color:#0d1c2e;">
              <span style="font-weight:700; font-size:11px; letter-spacing:0.14em; text-transform:uppercase; opacity:0.6;">
                Step {{ currentIndex + 1 }} of {{ currentQuestions.length }}
              </span>
              <span style="font-weight:700; font-size:11px; letter-spacing:0.08em; opacity:0.6;">~60 seconds</span>
            </div>
            <div class="w-full h-2 rounded-full overflow-hidden" style="background:#f0f5fb;">
              <div
                class="h-full rounded-full transition-all duration-400"
                :style="{ width: progressPct + '%', background: 'linear-gradient(90deg, #0d1c2e, #7fe3c4)' }"
              />
            </div>
          </div>

          <!-- Question -->
          <Transition name="q-slide" mode="out-in">
            <div :key="currentIndex" class="w-full">
              <!-- Dimension badge + question -->
              <div class="flex items-center gap-3 mb-5">
                <div
                  class="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0"
                  :style="isNutritionDim ? 'background:#0d1c2e; color:#dce9ff;' : 'background:#dce9ff; color:#0d1c2e;'"
                >
                  <component :is="currentQ.icon" class="w-5 h-5" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="font-body" style="color:#0d1c2e; opacity:0.55; font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">
                      {{ currentQ.dimensionLabel }}
                    </span>
                    <span
                      v-if="isNutritionDim"
                      class="font-body px-2 py-0.5 rounded-full"
                      style="background:#0d1c2e; color:#dce9ff; font-weight:700; font-size:9px; letter-spacing:0.12em; text-transform:uppercase;"
                    >
                      Nutrition
                    </span>
                  </div>
                  <h3 class="font-display" style="color:#0d1c2e; font-size:20px; line-height:1.2; font-weight:800;">
                    {{ currentQ.question }}
                  </h3>
                </div>
              </div>

              <!-- SLIDER -->
              <div v-if="currentQ.type === 'slider'" class="space-y-4">
                <div class="flex items-center justify-between text-sm font-body" style="color:#0d1c2e; opacity:0.55; font-weight:600;">
                  <span>{{ currentQ.sliderMin }}</span>
                  <span>{{ currentQ.sliderMax }}</span>
                </div>
                <div class="flex gap-2 justify-between">
                  <button
                    v-for="v in [1,2,3,4,5]"
                    :key="v"
                    @click="sliderVal = v; autoAdvanceIfNeeded()"
                    class="flex-1 h-14 rounded-xl border-2 flex flex-col items-center justify-center font-body transition-all"
                    :style="sliderVal === v
                      ? 'background:#0d1c2e; border-color:#0d1c2e; color:#dce9ff;'
                      : 'background:white; border-color:#dce9ff; color:#0d1c2e;'"
                  >
                    <span style="font-size:16px;">{{ sliderEmojis[v - 1] }}</span>
                    <span style="font-size:11px; font-weight:700; opacity:0.7; margin-top:2px;">{{ v }}</span>
                  </button>
                </div>
                <div class="text-center font-body" style="font-size:13px; color:#0d1c2e; opacity:0.5; font-weight:600;">
                  Tap a point to select
                </div>
                <button
                  v-if="sliderVal !== null"
                  @click="submitAnswer()"
                  class="w-full py-3 rounded-2xl font-body font-bold text-sm transition-all hover:opacity-90"
                  style="background:#0d1c2e; color:#dce9ff;"
                >
                  Next
                </button>
              </div>

              <!-- SINGLE CHOICE -->
              <div v-else-if="currentQ.type === 'single_choice'" class="space-y-2.5">
                <button
                  v-for="opt in currentQ.options"
                  :key="opt.label"
                  @click="selectSingle(opt)"
                  class="w-full text-left p-3.5 rounded-2xl border-2 font-body flex items-center justify-between transition-all duration-150 hover:bg-[#dce9ff] hover:border-[#0d1c2e]"
                  :style="selectedSingle === opt.label
                    ? 'background:#dce9ff; border-color:#0d1c2e; color:#0d1c2e;'
                    : 'background:white; border-color:#dce9ff; color:#0d1c2e;'"
                  style="font-weight:600; font-size:14px;"
                >
                  <span>{{ opt.label }}</span>
                  <span style="font-weight:700; font-size:12px; color:#0d1c2e; opacity:0.5; white-space:nowrap; margin-left:12px;">
                    +{{ opt.exp }} EXP
                  </span>
                </button>
              </div>

              <!-- MULTI SELECT -->
              <div v-else-if="currentQ.type === 'multi_select'" class="space-y-2.5">
                <label
                  v-for="opt in currentQ.multiOptions"
                  :key="opt.label"
                  class="flex items-center gap-3 p-3.5 rounded-2xl border-2 cursor-pointer font-body transition-all duration-150 hover:bg-[#f4f8fe]"
                  :style="multiSelected.includes(opt.label)
                    ? 'background:#dce9ff; border-color:#0d1c2e; color:#0d1c2e;'
                    : 'background:white; border-color:#dce9ff; color:#0d1c2e;'"
                >
                  <input
                    type="checkbox"
                    :value="opt.label"
                    v-model="multiSelected"
                    class="w-4 h-4 accent-[#0d1c2e] rounded"
                  />
                  <span style="font-weight:600; font-size:14px;">{{ opt.label }}</span>
                </label>
                <button
                  @click="submitAnswer()"
                  class="w-full py-3 rounded-2xl font-body font-bold text-sm transition-all hover:opacity-90"
                  style="background:#0d1c2e; color:#dce9ff; margin-top:8px;"
                >
                  Next
                </button>
              </div>

              <!-- STEPPER -->
              <div v-else-if="currentQ.type === 'stepper'" class="space-y-4">
                <div class="flex items-center justify-center gap-6">
                  <button
                    @click="stepperVal = Math.max(currentQ.stepperMin ?? 0, stepperVal - (currentQ.stepperStep ?? 1))"
                    class="w-12 h-12 rounded-full border-2 flex items-center justify-center font-body font-bold text-xl transition-all hover:bg-[#dce9ff]"
                    style="border-color:#dce9ff; color:#0d1c2e;"
                  >-</button>
                  <div class="text-center">
                    <div class="font-display" style="font-size:40px; font-weight:800; color:#0d1c2e; line-height:1;">
                      {{ stepperVal }}{{ stepperVal >= (currentQ.stepperMax ?? 12) ? '+' : '' }}
                    </div>
                    <div class="font-body" style="font-size:13px; color:#0d1c2e; opacity:0.6; font-weight:600;">
                      {{ currentQ.stepperUnit ?? 'hours' }}
                    </div>
                  </div>
                  <button
                    @click="stepperVal = Math.min(currentQ.stepperMax ?? 12, stepperVal + (currentQ.stepperStep ?? 1))"
                    class="w-12 h-12 rounded-full border-2 flex items-center justify-center font-body font-bold text-xl transition-all hover:bg-[#dce9ff]"
                    style="border-color:#dce9ff; color:#0d1c2e;"
                  >+</button>
                </div>
                <button
                  @click="submitAnswer()"
                  class="w-full py-3 rounded-2xl font-body font-bold text-sm transition-all hover:opacity-90"
                  style="background:#0d1c2e; color:#dce9ff;"
                >
                  Next
                </button>
              </div>

              <!-- ICON RATING -->
              <div v-else-if="currentQ.type === 'icon_rating'" class="space-y-3">
                <div class="grid grid-cols-3 gap-3">
                  <button
                    v-for="opt in currentQ.iconOptions"
                    :key="opt.label"
                    @click="selectIconRating(opt)"
                    class="flex flex-col items-center gap-2 p-4 rounded-2xl border-2 font-body transition-all duration-150 hover:bg-[#dce9ff] hover:border-[#0d1c2e]"
                    :style="selectedIconRating === opt.label
                      ? 'background:#0d1c2e; border-color:#0d1c2e; color:#dce9ff;'
                      : 'background:white; border-color:#dce9ff; color:#0d1c2e;'"
                  >
                    <span style="font-size:28px;">{{ opt.icon }}</span>
                    <span style="font-weight:700; font-size:12px; text-align:center; line-height:1.2;">{{ opt.label }}</span>
                    <span style="font-weight:700; font-size:11px; opacity:0.6;">+{{ opt.exp }} EXP</span>
                  </button>
                </div>
              </div>

            </div>
          </Transition>
        </div>

        <!-- DONE phase -->
        <div v-else-if="phase === 'done'" key="done" class="h-full flex flex-col">
          <div class="font-body" style="font-weight:700; font-size:11px; letter-spacing:0.18em; text-transform:uppercase; opacity:0.6; color:#0d1c2e;">
            Check-in complete
          </div>
          <h3 class="font-display mt-2" style="font-size:28px; font-weight:800; color:#0d1c2e; line-height:1.15; letter-spacing:-0.01em;">
            Thank you for showing up today.
          </h3>
          <p class="font-body mt-3 max-w-md" style="font-size:15px; color:#0d1c2e; opacity:0.7; font-weight:500; line-height:1.6;">
            Your companion felt every answer. Insights are below - gentle patterns, never pressure.
          </p>

          <!-- Results summary -->
          <div class="mt-5 grid grid-cols-3 gap-3">
            <div
              v-for="dim in completedDimensions"
              :key="dim.key"
              class="rounded-2xl p-3 border text-center"
              style="background:#f4f8fe; border-color:#dce9ff;"
            >
              <div class="font-body" style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#0d1c2e; opacity:0.55;">
                {{ dim.label }}
              </div>
              <div class="font-display mt-1" style="font-size:22px; font-weight:800; color:#0d1c2e;">
                +{{ dim.totalExp }}
              </div>
              <div class="font-body" style="font-size:10px; font-weight:700; color:#0d1c2e; opacity:0.4;">EXP</div>
            </div>
          </div>

          <div class="mt-auto pt-8 flex justify-center">
            <button
              @click="$emit('redo')"
              class="inline-flex items-center gap-2 px-6 py-3 rounded-full font-body font-bold text-sm transition-all hover:opacity-90"
              style="background:#0d1c2e; color:#dce9ff;"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Start a new check-in
            </button>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  Heart, Moon, Activity, BookOpen, Apple, Beef, Wheat,
  Sun, Smile, Baby, Users, Zap, Salad, Milk
} from 'lucide-vue-next'

// --------------- Types ---------------
type AgeStage = 'newborns' | 'infants' | 'toddlers' | 'young_kids' | 'pre_teens'
type UIType = 'slider' | 'single_choice' | 'multi_select' | 'stepper' | 'icon_rating'

interface SingleOption { label: string; exp: number }
interface MultiOption { label: string }
interface IconOption { label: string; icon: string; exp: number }

interface Question {
  id: string
  dimension: 'mood' | 'rest' | 'exercise' | 'self_discipline' | 'vitamin' | 'protein' | 'carb'
  dimensionLabel: string
  question: string
  type: UIType
  icon: any
  // slider
  sliderMin?: string
  sliderMax?: string
  sliderExpFn?: (v: number) => number
  // single_choice
  options?: SingleOption[]
  // multi_select
  multiOptions?: MultiOption[]
  multiExpFn?: (selected: string[]) => number
  // stepper
  stepperMin?: number
  stepperMax?: number
  stepperStep?: number
  stepperUnit?: string
  stepperExpFn?: (v: number) => number
  // icon_rating
  iconOptions?: IconOption[]
}

// --------------- Stage definitions ---------------
const STAGES = [
  { id: 'newborns' as AgeStage, label: 'Newborns', sub: '0-3 months' },
  { id: 'infants' as AgeStage, label: 'Infants', sub: '4-12 months' },
  { id: 'toddlers' as AgeStage, label: 'Toddlers', sub: '1-3 years' },
  { id: 'young_kids' as AgeStage, label: 'Young Kids', sub: '4-8 years' },
  { id: 'pre_teens' as AgeStage, label: 'Pre-teens', sub: '9-12 years' },
]

// --------------- Helper for standard slider EXP ---------------
const stdSlider = (v: number) => v >= 4 ? 10 : v === 3 ? 5 : 2

// --------------- Survey questions per stage ---------------
const SURVEYS: Record<AgeStage, Question[]> = {
  newborns: [
    {
      id: 'nb_mood1', dimension: 'mood', dimensionLabel: 'Mood', icon: Smile,
      question: 'How was your baby\'s overall temperament today?',
      type: 'slider', sliderMin: 'Very tearful', sliderMax: 'Very calm',
      sliderExpFn: (v) => v === 5 ? 10 : v === 4 ? 8 : v === 3 ? 5 : v === 2 ? 3 : 2,
    },
    {
      id: 'nb_mood2', dimension: 'mood', dimensionLabel: 'Mood', icon: Heart,
      question: 'How did they respond to your comforting?',
      type: 'single_choice',
      options: [
        { label: 'Settled quickly in my arms', exp: 10 },
        { label: 'Took a little while, but we got there', exp: 5 },
        { label: 'Very hard to soothe today', exp: 2 },
      ],
    },
    {
      id: 'nb_rest1', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'How would you rate their daytime naps?',
      type: 'icon_rating',
      iconOptions: [
        { label: 'Solid long naps', icon: '🔋', exp: 10 },
        { label: 'Short catnaps', icon: '🌗', exp: 5 },
        { label: 'Fought sleep all day', icon: '😴', exp: 2 },
      ],
    },
    {
      id: 'nb_rest2', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'Roughly how many hours did they sleep last night?',
      type: 'stepper', stepperMin: 0, stepperMax: 12, stepperStep: 1, stepperUnit: 'hours',
      stepperExpFn: (v) => v >= 9 ? 10 : v >= 5 ? 5 : 2,
    },
    {
      id: 'nb_ex1', dimension: 'exercise', dimensionLabel: 'Exercise', icon: Activity,
      question: 'Did we manage to do some Tummy Time today?',
      type: 'single_choice',
      options: [
        { label: 'Yes, great sessions!', exp: 10 },
        { label: 'Tried a little bit', exp: 5 },
        { label: 'Skipped it for rest', exp: 2 },
      ],
    },
    {
      id: 'nb_self1', dimension: 'self_discipline', dimensionLabel: 'Self-discipline', icon: BookOpen,
      question: 'How readable were their hunger and sleep cues today?',
      type: 'slider', sliderMin: 'Very confusing', sliderMax: 'Crystal clear',
      sliderExpFn: stdSlider,
    },
    {
      id: 'nb_vit1', dimension: 'vitamin', dimensionLabel: 'Vitamin intake', icon: Apple,
      question: 'How comfortable was their digestion and tummy today?',
      type: 'icon_rating',
      iconOptions: [
        { label: 'Very comfortable', icon: '😊', exp: 10 },
        { label: 'A bit gassy', icon: '😐', exp: 5 },
        { label: 'Lots of discomfort', icon: '😣', exp: 2 },
      ],
    },
    {
      id: 'nb_pro1', dimension: 'protein', dimensionLabel: 'Protein intake', icon: Beef,
      question: 'How did the feeding sessions go today?',
      type: 'slider', sliderMin: 'Very frustrating', sliderMax: 'Very smooth',
      sliderExpFn: stdSlider,
    },
    {
      id: 'nb_carb1', dimension: 'carb', dimensionLabel: 'Carb intake', icon: Zap,
      question: 'How alert was baby during their awake windows?',
      type: 'single_choice',
      options: [
        { label: 'Bright-eyed and looking around', exp: 10 },
        { label: 'A bit drowsy but awake', exp: 5 },
        { label: 'Very lethargic or instantly fussy', exp: 2 },
      ],
    },
  ],

  infants: [
    {
      id: 'in_mood1', dimension: 'mood', dimensionLabel: 'Mood', icon: Smile,
      question: 'What was your baby\'s main vibe today? Select all that apply.',
      type: 'multi_select',
      multiOptions: [
        { label: 'Smiley' }, { label: 'Babbling' }, { label: 'Curious' },
        { label: 'Clingy' }, { label: 'Teething discomfort' }, { label: 'Cautious' },
        { label: 'Tearful' }, { label: 'Overwhelmed' },
      ],
      multiExpFn: (sel) => {
        const neg = ['Tearful', 'Overwhelmed']
        const pos = ['Smiley', 'Babbling', 'Curious']
        if (sel.some(s => neg.includes(s))) return 2
        if (pos.filter(p => sel.includes(p)).length >= 2) return 10
        return 5
      },
    },
    {
      id: 'in_mood2', dimension: 'mood', dimensionLabel: 'Mood', icon: Heart,
      question: 'How did they react to new things (toys, faces, foods)?',
      type: 'slider', sliderMin: 'Very upset', sliderMax: 'Very excited',
      sliderExpFn: stdSlider,
    },
    {
      id: 'in_rest1', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'How many times did they wake up last night?',
      type: 'stepper', stepperMin: 0, stepperMax: 5, stepperStep: 1, stepperUnit: 'wake-ups',
      stepperExpFn: (v) => v <= 1 ? 10 : v <= 3 ? 5 : 2,
    },
    {
      id: 'in_ex1', dimension: 'exercise', dimensionLabel: 'Exercise', icon: Activity,
      question: 'Which activities did they do today? Select all that apply.',
      type: 'multi_select',
      multiOptions: [
        { label: 'Rolling' }, { label: 'Crawling' }, { label: 'Sitting up' }, { label: 'Reaching for objects' },
      ],
      multiExpFn: (sel) => sel.length >= 3 ? 10 : sel.length >= 1 ? 5 : 2,
    },
    {
      id: 'in_self1', dimension: 'self_discipline', dimensionLabel: 'Self-discipline', icon: BookOpen,
      question: 'How smoothly did they handle the bedtime routine?',
      type: 'single_choice',
      options: [
        { label: 'Calmly accepted the routine', exp: 10 },
        { label: 'Fussy but settled eventually', exp: 5 },
        { label: 'Lots of resistance', exp: 2 },
      ],
    },
    {
      id: 'in_vit1', dimension: 'vitamin', dimensionLabel: 'Vitamin intake', icon: Apple,
      question: 'How many colours of natural food (purees or solids) did they eat?',
      type: 'stepper', stepperMin: 0, stepperMax: 4, stepperStep: 1, stepperUnit: 'colours',
      stepperExpFn: (v) => v >= 2 ? 10 : v === 1 ? 5 : 2,
    },
    {
      id: 'in_pro1', dimension: 'protein', dimensionLabel: 'Protein intake', icon: Milk,
      question: 'Did they have a good source of protein (milk, pureed meats, yogurt)?',
      type: 'single_choice',
      options: [
        { label: 'Yes, a healthy portion', exp: 10 },
        { label: 'Just a little bit', exp: 5 },
        { label: 'Struggled to get protein in', exp: 2 },
      ],
    },
    {
      id: 'in_carb1', dimension: 'carb', dimensionLabel: 'Carb intake', icon: Zap,
      question: 'How was their energy stability after eating?',
      type: 'slider', sliderMin: 'Major crash', sliderMax: 'Steady and active',
      sliderExpFn: stdSlider,
    },
  ],

  toddlers: [
    {
      id: 'td_mood1', dimension: 'mood', dimensionLabel: 'Mood', icon: Smile,
      question: 'How well did they handle their big emotions today?',
      type: 'slider', sliderMin: 'Constant meltdowns', sliderMax: 'Easily redirected',
      sliderExpFn: stdSlider,
    },
    {
      id: 'td_mood2', dimension: 'mood', dimensionLabel: 'Mood', icon: Users,
      question: 'How was their social mood?',
      type: 'single_choice',
      options: [
        { label: 'Affectionate and playful', exp: 10 },
        { label: 'A bit shy or independent', exp: 5 },
        { label: 'Easily frustrated with others', exp: 2 },
      ],
    },
    {
      id: 'td_rest1', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'Did they get a daytime nap or quiet time?',
      type: 'single_choice',
      options: [
        { label: 'Yes, rested perfectly', exp: 10 },
        { label: 'Short rest, woke up grumpy', exp: 5 },
        { label: 'Refused to rest completely', exp: 2 },
      ],
    },
    {
      id: 'td_ex1', dimension: 'exercise', dimensionLabel: 'Exercise', icon: Activity,
      question: 'How much outdoor or active indoor play did they get?',
      type: 'stepper', stepperMin: 0, stepperMax: 60, stepperStep: 15, stepperUnit: 'minutes',
      stepperExpFn: (v) => v >= 45 ? 10 : v >= 15 ? 5 : 2,
    },
    {
      id: 'td_self1', dimension: 'self_discipline', dimensionLabel: 'Self-discipline', icon: BookOpen,
      question: 'How well did they listen to simple instructions?',
      type: 'icon_rating',
      iconOptions: [
        { label: 'Listened well', icon: '👍', exp: 10 },
        { label: 'Needed reminders', icon: '😐', exp: 5 },
        { label: 'Ignored completely', icon: '👎', exp: 2 },
      ],
    },
    {
      id: 'td_vit1', dimension: 'vitamin', dimensionLabel: 'Vitamin intake', icon: Salad,
      question: 'How many portions of fruits and veggies did they eat?',
      type: 'stepper', stepperMin: 0, stepperMax: 5, stepperStep: 1, stepperUnit: 'portions',
      stepperExpFn: (v) => v >= 2 ? 10 : v === 1 ? 5 : 2,
    },
    {
      id: 'td_pro1', dimension: 'protein', dimensionLabel: 'Protein intake', icon: Beef,
      question: 'How was their overall appetite for their main meals?',
      type: 'slider', sliderMin: 'Picky - refused', sliderMax: 'Ate very well',
      sliderExpFn: stdSlider,
    },
    {
      id: 'td_carb1', dimension: 'carb', dimensionLabel: 'Carb intake', icon: Wheat,
      question: 'Did they eat healthy grains (wholewheat bread, rice, oats)?',
      type: 'single_choice',
      options: [
        { label: 'Yes, healthy energy sources', exp: 10 },
        { label: 'Mostly white carbs (crackers, white bread)', exp: 5 },
        { label: 'Only wanted sugary snacks', exp: 2 },
      ],
    },
  ],

  young_kids: [
    {
      id: 'yk_mood1', dimension: 'mood', dimensionLabel: 'Mood', icon: Smile,
      question: 'How did they handle a minor disappointment today?',
      type: 'slider', sliderMin: 'Major meltdown', sliderMax: 'Bounced back quickly',
      sliderExpFn: stdSlider,
    },
    {
      id: 'yk_mood2', dimension: 'mood', dimensionLabel: 'Mood', icon: Sun,
      question: 'What was their general attitude towards the day?',
      type: 'icon_rating',
      iconOptions: [
        { label: 'Great day!', icon: '😊', exp: 10 },
        { label: 'Mixed day', icon: '😐', exp: 5 },
        { label: 'Tough day', icon: '😢', exp: 2 },
      ],
    },
    {
      id: 'yk_rest1', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'How many hours of sleep did they get last night?',
      type: 'stepper', stepperMin: 0, stepperMax: 12, stepperStep: 1, stepperUnit: 'hours',
      stepperExpFn: (v) => v >= 9 ? 10 : v >= 7 ? 5 : 2,
    },
    {
      id: 'yk_ex1', dimension: 'exercise', dimensionLabel: 'Exercise', icon: Activity,
      question: 'Did they engage in any active outdoor play?',
      type: 'single_choice',
      options: [
        { label: 'Yes, played outside nicely', exp: 10 },
        { label: 'Played actively, but indoors', exp: 5 },
        { label: 'Mostly screens or sedentary today', exp: 2 },
      ],
    },
    {
      id: 'yk_self1', dimension: 'self_discipline', dimensionLabel: 'Self-discipline', icon: BookOpen,
      question: 'How did they manage their screen-time limits?',
      type: 'slider', sliderMin: 'Huge tantrum', sliderMax: 'Turned off smoothly',
      sliderExpFn: stdSlider,
    },
    {
      id: 'yk_vit1', dimension: 'vitamin', dimensionLabel: 'Vitamin intake', icon: Apple,
      question: 'Did they try any new or varied healthy foods today? Select all that apply.',
      type: 'multi_select',
      multiOptions: [
        { label: 'Ate veggies without fuss' },
        { label: 'Tried something new' },
        { label: 'Drank lots of water' },
      ],
      multiExpFn: (sel) => sel.length >= 2 ? 10 : sel.length === 1 ? 5 : 2,
    },
    {
      id: 'yk_pro1', dimension: 'protein', dimensionLabel: 'Protein intake', icon: Beef,
      question: 'Did they feel full and satisfied after meals?',
      type: 'single_choice',
      options: [
        { label: 'Yes, stayed full until the next meal', exp: 10 },
        { label: 'Asked for snacks shortly after', exp: 5 },
        { label: 'Always hungry, meals were not filling', exp: 2 },
      ],
    },
    {
      id: 'yk_carb1', dimension: 'carb', dimensionLabel: 'Carb intake', icon: Wheat,
      question: 'What did they mostly drink today?',
      type: 'single_choice',
      options: [
        { label: 'Mostly water or milk', exp: 10 },
        { label: 'Mix of water and juice', exp: 5 },
        { label: 'Mostly sugary drinks or soda', exp: 2 },
      ],
    },
  ],

  pre_teens: [
    {
      id: 'pt_mood1', dimension: 'mood', dimensionLabel: 'Mood', icon: Smile,
      question: 'How was their communication with you today?',
      type: 'slider', sliderMin: 'Shut down - silent', sliderMax: 'Very open - chatty',
      sliderExpFn: stdSlider,
    },
    {
      id: 'pt_mood2', dimension: 'mood', dimensionLabel: 'Mood', icon: Heart,
      question: 'How would you describe their stress levels regarding school or friends?',
      type: 'icon_rating',
      iconOptions: [
        { label: 'Relaxed', icon: '😌', exp: 10 },
        { label: 'Slightly worried', icon: '😟', exp: 5 },
        { label: 'Very anxious', icon: '😰', exp: 2 },
      ],
    },
    {
      id: 'pt_rest1', dimension: 'rest', dimensionLabel: 'Rest', icon: Moon,
      question: 'Were screens put away before bedtime last night?',
      type: 'single_choice',
      options: [
        { label: 'Yes, screens away - slept well', exp: 10 },
        { label: 'Looked at screens, but slept okay', exp: 5 },
        { label: 'Stayed up late on devices, exhausted today', exp: 2 },
      ],
    },
    {
      id: 'pt_ex1', dimension: 'exercise', dimensionLabel: 'Exercise', icon: Activity,
      question: 'What kind of physical activity did they do today? Select all that apply.',
      type: 'multi_select',
      multiOptions: [
        { label: 'Sports practice' },
        { label: 'PE at school' },
        { label: 'Walking outside' },
        { label: 'Stretching or yoga' },
      ],
      multiExpFn: (sel) => sel.length >= 2 ? 10 : sel.length === 1 ? 5 : 2,
    },
    {
      id: 'pt_self1', dimension: 'self_discipline', dimensionLabel: 'Self-discipline', icon: BookOpen,
      question: 'How did they manage their homework or household chores?',
      type: 'slider', sliderMin: 'Completely avoided', sliderMax: 'Did it independently',
      sliderExpFn: stdSlider,
    },
    {
      id: 'pt_vit1', dimension: 'vitamin', dimensionLabel: 'Vitamin intake', icon: Salad,
      question: 'Did they independently choose to eat fruits, veggies or drink water?',
      type: 'single_choice',
      options: [
        { label: 'Yes, made healthy choices willingly', exp: 10 },
        { label: 'Ate or drank them only when reminded', exp: 5 },
        { label: 'Actively avoided them or snuck junk food', exp: 2 },
      ],
    },
    {
      id: 'pt_pro1', dimension: 'protein', dimensionLabel: 'Protein intake', icon: Beef,
      question: 'Did they eat a solid, protein-rich breakfast to start the day?',
      type: 'single_choice',
      options: [
        { label: 'Yes (eggs, yogurt, beans, meat)', exp: 10 },
        { label: 'Just a quick carb (cereal, toast)', exp: 5 },
        { label: 'Skipped breakfast entirely', exp: 2 },
      ],
    },
    {
      id: 'pt_carb1', dimension: 'carb', dimensionLabel: 'Carb intake', icon: Zap,
      question: 'How was their energy and focus throughout the afternoon?',
      type: 'slider', sliderMin: 'Major sugar crash', sliderMax: 'Steady and focused',
      sliderExpFn: stdSlider,
    },
  ],
}

// --------------- Props & Emits ---------------
const props = defineProps<{
  stage: AgeStage
  hasVisited: boolean
  todayCompleted: boolean
  phase: 'intro' | 'survey' | 'done'
  isMuted: boolean
}>()

const emit = defineEmits<{
  'update:stage': [stage: AgeStage]
  'start': []
  'complete': [payload: { totalExp: number; maxExp: number; dimensionScores: Record<string, number>; answers: { id: string; dimension: string; exp: number }[] }]
  'redo': []
  'toggleMute': []
}>()

// --------------- Local state ---------------
const stageDropOpen = ref(false)
const currentIndex = ref(0)
const sliderVal = ref<number | null>(null)
const selectedSingle = ref<string | null>(null)
const multiSelected = ref<string[]>([])
const stepperVal = ref(0)
const selectedIconRating = ref<string | null>(null)

// answers collected during survey
const answersLog = ref<{ id: string; dimension: string; exp: number }[]>([])

// completed dimension rollup for "done" view
const completedDimensions = ref<{ key: string; label: string; totalExp: number }[]>([])

const modelStage = computed(() => props.stage)
const currentStageObj = computed(() => STAGES.find(s => s.id === props.stage) ?? STAGES[0])
const currentQuestions = computed(() => SURVEYS[props.stage] ?? SURVEYS.newborns)
const currentQ = computed(() => currentQuestions.value[currentIndex.value])
const progressPct = computed(() => (currentIndex.value / currentQuestions.value.length) * 100)
const isNutritionDim = computed(() => ['vitamin', 'protein', 'carb'].includes(currentQ.value?.dimension ?? ''))
const currentTipIndex = ref(0)
const healthTips: Record<Question['dimension'], string[]> = {
  mood: [
    'Small moments of comfort help children feel safe and connected.',
    'Naming feelings can make big emotions easier to understand.',
    'A calm voice and steady presence can help reset a difficult moment.',
  ],
  rest: [
    'A steady wind-down routine can make sleep feel easier to enter.',
    'Dim lights and quiet play help the body prepare for rest.',
    'Consistent sleep and wake times support better daytime energy.',
  ],
  exercise: [
    'Short bursts of movement count, especially when they feel playful.',
    'Active play helps build strength, coordination and confidence.',
    'Outdoor movement can lift mood while giving the body useful practice.',
  ],
  self_discipline: [
    'Simple routines build confidence when they are repeated gently.',
    'Small choices help children practise independence without pressure.',
    'Clear, predictable steps make daily tasks easier to follow.',
  ],
  vitamin: [
    'Colourful fruit, vegetables and water support everyday growth.',
    'Trying one colourful food at a time can make variety feel easier.',
    'Whole foods often bring vitamins, fibre and hydration together.',
  ],
  protein: [
    'Protein-rich foods help keep energy steady between meals.',
    'Milk, yoghurt, eggs, beans, fish or meat can support growing bodies.',
    'Adding protein to breakfast can help the morning feel more stable.',
  ],
  carb: [
    'Whole-grain carbs can support longer-lasting focus and play.',
    'Pairing carbs with protein or fibre can smooth out energy dips.',
    'Steady meals and snacks help avoid big afternoon energy crashes.',
  ],
}
const headerKicker = computed(() => props.phase === 'survey' ? `${currentQ.value.dimensionLabel} tip` : 'The daily moment')
const headerTip = computed(() => {
  if (props.phase === 'done') return 'Healthy patterns grow through small daily choices.'
  if (props.phase !== 'survey') return 'Start with one kind habit you can repeat today.'
  const tips = healthTips[currentQ.value.dimension]
  return tips[currentTipIndex.value] ?? tips[0]
})

const sliderEmojis = ['😢', '😕', '😐', '🙂', '😄']

// --------------- Methods ---------------
function selectStage(id: AgeStage) {
  emit('update:stage', id)
  stageDropOpen.value = false
}

function resetAnswerState() {
  sliderVal.value = null
  selectedSingle.value = null
  multiSelected.value = []
  stepperVal.value = currentQ.value?.stepperMin ?? 0
  selectedIconRating.value = null
}

function pickRandomTip() {
  const tips = healthTips[currentQ.value.dimension]
  currentTipIndex.value = Math.floor(Math.random() * tips.length)
}

function autoAdvanceIfNeeded() {
  // slider: auto-advance only after user explicitly confirms
}

function selectSingle(opt: SingleOption) {
  selectedSingle.value = opt.label
  const exp = opt.exp
  recordAnswer(exp)
  advance()
}

function selectIconRating(opt: IconOption) {
  selectedIconRating.value = opt.label
  recordAnswer(opt.exp)
  advance()
}

function submitAnswer() {
  const q = currentQ.value
  let exp = 0
  if (q.type === 'slider' && sliderVal.value !== null) {
    exp = q.sliderExpFn?.(sliderVal.value) ?? 5
  } else if (q.type === 'multi_select') {
    exp = q.multiExpFn?.(multiSelected.value) ?? 5
  } else if (q.type === 'stepper') {
    exp = q.stepperExpFn?.(stepperVal.value) ?? 5
  }
  recordAnswer(exp)
  advance()
}

function recordAnswer(exp: number) {
  answersLog.value.push({ id: currentQ.value.id, dimension: currentQ.value.dimension, exp })
}

function advance() {
  const total = currentQuestions.value.length
  if (currentIndex.value + 1 >= total) {
    finishSurvey()
  } else {
    setTimeout(() => {
      currentIndex.value++ // watch(currentIndex) handles resetAnswerState
    }, 300)
  }
}

function finishSurvey() {
  const log = answersLog.value
  const totalExp = log.reduce((s, a) => s + a.exp, 0)
  const maxExp = currentQuestions.value.length * 10

  // Aggregate by dimension
  const dimMap: Record<string, number[]> = {}
  for (const a of log) {
    if (!dimMap[a.dimension]) dimMap[a.dimension] = []
    dimMap[a.dimension].push(a.exp)
  }

  const dimensionScores: Record<string, number> = {}
  for (const [k, vals] of Object.entries(dimMap)) {
    dimensionScores[k] = Math.round(vals.reduce((a, b) => a + b, 0) / vals.length * 10)
  }

  // Dimension label map
  const dimLabels: Record<string, string> = {
    mood: 'Mood', rest: 'Rest', exercise: 'Exercise',
    self_discipline: 'Self-care', vitamin: 'Vitamins', protein: 'Protein', carb: 'Energy',
  }
  completedDimensions.value = Object.entries(dimMap).map(([k, vals]) => ({
    key: k,
    label: dimLabels[k] ?? k,
    totalExp: vals.reduce((a, b) => a + b, 0),
  }))

  emit('complete', { totalExp, maxExp, dimensionScores, answers: log })
}

// Reset when survey phase starts
watch(() => props.phase, (newPhase) => {
  if (newPhase === 'survey') {
    currentIndex.value = 0
    answersLog.value = []
    completedDimensions.value = []
    pickRandomTip()
    resetAnswerState()
  }
})

// Reset stepper on question change
watch(currentIndex, () => {
  pickRandomTip()
  resetAnswerState()
})


</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active { transition: opacity 0.2s, transform 0.2s; }
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }

.q-slide-enter-active,
.q-slide-leave-active { transition: opacity 0.25s, transform 0.25s; }
.q-slide-enter-from { opacity: 0; transform: translateX(24px); }
.q-slide-leave-to { opacity: 0; transform: translateX(-24px); }
</style>
