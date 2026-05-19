<template>
  <div
    class="rounded-3xl border shadow-xl flex flex-col w-full overflow-hidden relative"
    style="background: linear-gradient(180deg, #ffffff 0%, #dce9ff 100%); border-color: #dce9ff; min-height: 620px;"
  >
    <!-- Header -->
    <div class="px-6 pt-6 flex items-center justify-between">
      <div class="font-body" style="font-weight: 700; font-size: 10px; letter-spacing: 0.16em; text-transform: uppercase; color: #0d1c2e; opacity: 0.6;">
        Your companion
      </div>
      <div
        class="px-2.5 py-1 rounded-full font-body"
        style="background: #0d1c2e; color: #dce9ff; font-weight: 700; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;"
      >
        {{ stageLabel }}
      </div>
    </div>

    <!-- Video frame -->
    <div class="relative flex-1 flex items-center justify-center px-6 py-4">
      <div
        class="absolute rounded-full blur-3xl pointer-events-none"
        :style="{ width: '280px', height: '280px', background: glowColor, opacity: 0.6 }"
      />
      <div class="relative z-10 rounded-2xl overflow-hidden shadow-xl" style="width: 260px; height: 260px; background: #0d1c2e10;">
        <video
          ref="videoEl"
          :key="videoSrc"
          :src="videoSrc"
          autoplay
          loop
          :muted="isMuted"
          playsinline
          class="w-full h-full object-cover"
          style="border-radius: 16px;"
        />
      </div>
      <template v-if="mood === 'happy'">
        <span
          v-for="(s, i) in sparkles"
          :key="i"
          class="absolute pointer-events-none select-none"
          :style="s.style"
        >{{ s.char }}</span>
      </template>
    </div>

    <!-- Speech bubble -->
    <div class="px-6 pb-3">
      <div
        class="px-3.5 py-2.5 rounded-2xl bg-white/95 border border-white shadow text-center transition-all duration-500"
        style="color: #0d1c2e;"
      >
        <span class="font-body" style="font-weight: 700; font-size: 13px;">{{ bubbleText }}</span>
      </div>
    </div>

    <!-- Health level bar + tips -->
    <div class="px-6 pb-6">

      <!-- Segment row: dot indicator + bar per level -->
      <div class="flex gap-1.5 mb-1">
        <div
          v-for="i in 6"
          :key="i"
          class="flex-1 flex flex-col items-center gap-1"
        >
          <!-- active marker dot -->
          <div
            class="w-1.5 h-1.5 rounded-full transition-all duration-500"
            :style="{
              background: i === healthLevel && healthLevel > 0 ? SEGMENT_COLORS[i - 1].filled : 'transparent',
            }"
          />
          <!-- segment bar -->
          <div
            class="w-full rounded-full transition-all duration-500"
            :style="{
              height: i === healthLevel && healthLevel > 0 ? '12px' : '10px',
              background: segmentColor(i - 1),
            }"
          />
        </div>
      </div>

      <!-- Scale labels -->
      <div class="flex justify-between font-body mb-3" style="font-size: 10px; font-weight: 700; color: #0d1c2e; opacity: 0.38; letter-spacing: 0.03em;">
        <span>Unhealthy</span>
        <span>Healthy</span>
      </div>

      <!-- Level badge + tips — visible only after survey -->
      <Transition
        enter-active-class="transition duration-400 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0"
      >
        <div v-if="healthInfo" class="space-y-2.5">

          <!-- Level identifier -->
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-body px-2 py-0.5 rounded-full shrink-0" :style="levelBadgeStyle">
              Level {{ healthLevel }}/6
            </span>
            <span class="font-body" style="font-size: 12px; font-weight: 800; color: #0d1c2e; text-transform: uppercase; letter-spacing: 0.07em;">
              {{ healthInfo.name }}
            </span>
          </div>

          <!-- Divider -->
          <div style="height: 1px; background: rgba(13,28,46,0.08);" />

          <!-- Tips list -->
          <ul class="space-y-1.5">
            <li
              v-for="(tip, idx) in healthInfo.tips"
              :key="idx"
              class="flex items-start gap-2"
            >
              <span class="shrink-0 font-body" style="font-size: 11px; color: #0d1c2e; opacity: 0.35; line-height: 1.6; font-weight: 700;">-</span>
              <span class="font-body" style="font-size: 11px; font-weight: 600; color: #0d1c2e; opacity: 0.62; line-height: 1.55;">{{ tip }}</span>
            </li>
          </ul>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

type PetMood = 'idle' | 'happy' | 'neutral' | 'sad'

const props = defineProps<{
  mood: PetMood
  healthPct: number | null
  stageLabel: string
  isMuted: boolean
}>()

const videoEl = ref<HTMLVideoElement | null>(null)

const videoSrc = computed(() => {
  if (props.mood === 'happy') return '/videos/HAPPY.mp4'
  if (props.mood === 'sad') return '/videos/SAD.mp4'
  return '/videos/NORMAL.mp4'
})

const glowColor = computed(() => {
  if (props.mood === 'happy') return 'radial-gradient(circle, #7fe3c499 0%, transparent 70%)'
  if (props.mood === 'sad') return 'radial-gradient(circle, #f8c7c799 0%, transparent 70%)'
  return 'radial-gradient(circle, #dce9ff99 0%, transparent 70%)'
})

const bubbleText = computed(() => {
  if (props.mood === 'happy') return 'Wonderful! You are doing great today!'
  if (props.mood === 'sad') return 'Every small step counts. I am right here with you.'
  if (props.mood === 'neutral') return 'Steady progress - keep it up!'
  return 'Hi there. Ready when you are.'
})

const healthLevel = computed(() => {
  if (props.healthPct === null || props.mood === 'idle') return 0
  return Math.min(6, Math.max(1, Math.ceil(props.healthPct * 6)))
})

const HEALTH_INFOS = [
  null,
  {
    name: 'Needs attention',
    tier: 'unhealthy',
    tips: [
      'Start with one gentle habit - even a glass of water counts.',
      'Rest is the priority right now. Protect sleep above all else.',
      'Be patient with yourself - rebuilding always takes time.',
    ],
  },
  {
    name: 'Low energy',
    tier: 'unhealthy',
    tips: [
      'Pair protein with each meal to help stabilise energy.',
      'A 10-minute walk outdoors can reset a difficult afternoon.',
      'Small wins matter - acknowledge every step forward.',
    ],
  },
  {
    name: 'Getting steady',
    tier: 'normal',
    tips: [
      'You have a foundation. Build one consistent daily habit on it.',
      'Aim for varied colours on your child\'s plate today.',
      'Momentum builds quietly - keep showing up, even briefly.',
    ],
  },
  {
    name: 'On track',
    tier: 'normal',
    tips: [
      'Solid habits are forming. Stay consistent this week.',
      'Hydration is often overlooked - keep water visible and close.',
      'Celebrate this week\'s progress, even in a small way.',
    ],
  },
  {
    name: 'Thriving',
    tier: 'healthy',
    tips: [
      'Great balance across all habits. Protect what is working.',
      'Share your routine with your child - they absorb it naturally.',
      'This consistency is quietly compounding into lasting health.',
    ],
  },
  {
    name: 'Excellent',
    tier: 'healthy',
    tips: [
      'Exceptional effort today - your dedication is clearly showing.',
      'You are building resilience for the whole family.',
      'Maintain this rhythm and notice how your energy follows.',
    ],
  },
]

const healthInfo = computed(() => HEALTH_INFOS[healthLevel.value] ?? null)

const SEGMENT_COLORS = [
  { filled: '#ef4444', empty: '#fecaca' },
  { filled: '#ef4444', empty: '#fecaca' },
  { filled: '#f59e0b', empty: '#fde68a' },
  { filled: '#f59e0b', empty: '#fde68a' },
  { filled: '#10b981', empty: '#a7f3d0' },
  { filled: '#10b981', empty: '#a7f3d0' },
]

function segmentColor(i: number): string {
  const c = SEGMENT_COLORS[i]
  return (i + 1) <= healthLevel.value ? c.filled : c.empty
}

const levelBadgeStyle = computed(() => {
  const tier = healthInfo.value?.tier
  const base = 'font-size:10px; font-weight:800; letter-spacing:0.08em; text-transform:uppercase;'
  if (tier === 'unhealthy') return `background:#fee2e2; color:#ef4444; ${base}`
  if (tier === 'healthy') return `background:#d1fae5; color:#10b981; ${base}`
  return `background:#fef3c7; color:#d97706; ${base}`
})

const sparkles = [
  { char: '✦', style: 'left: 12%; top: 14%; color: #FFD56B; font-size: 18px; font-weight: 700;' },
  { char: '✦', style: 'left: 30%; top: 20%; color: #FFD56B; font-size: 14px; font-weight: 700;' },
  { char: '✦', style: 'right: 14%; top: 14%; color: #FFD56B; font-size: 18px; font-weight: 700;' },
  { char: '✦', style: 'right: 30%; top: 22%; color: #FFD56B; font-size: 14px; font-weight: 700;' },
]

watch(() => props.mood, () => {
  // Let the :key on video handle reload
})
</script>
