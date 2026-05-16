<template>
  <div
    class="rounded-3xl border shadow-xl flex flex-col w-full overflow-hidden relative"
    style="background: linear-gradient(180deg, #ffffff 0%, #dce9ff 100%); border-color: #dce9ff; min-height: 560px;"
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
      <!-- Glow -->
      <div
        class="absolute rounded-full blur-3xl pointer-events-none"
        :style="{
          width: '280px', height: '280px',
          background: glowColor,
          opacity: 0.6,
        }"
      />

      <!-- Video player -->
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

      <!-- Sparkles when happy -->
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
    <div class="px-6 pb-2">
      <div
        class="px-3.5 py-2.5 rounded-2xl bg-white/95 border border-white shadow text-center transition-all duration-500"
        style="color: #0d1c2e;"
      >
        <span class="font-body" style="font-weight: 700; font-size: 13px;">{{ bubbleText }}</span>
      </div>
    </div>

    <!-- EXP bar -->
    <div class="px-6 pb-6 pt-2">
      <div class="flex items-center justify-between mb-1.5 font-body" style="color: #0d1c2e; font-weight: 700;">
        <span style="font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase;">
          Lv. {{ level }}
        </span>
        <span style="font-size: 12px; opacity: 0.65;">{{ exp }} / {{ expToNext }}</span>
      </div>
      <div class="w-full h-2.5 rounded-full overflow-hidden border border-white" style="background: rgba(255,255,255,0.8);">
        <div
          class="h-full rounded-full transition-all duration-700"
          :style="{ width: expPct + '%', background: 'linear-gradient(90deg, #0d1c2e 0%, #396477 60%, #7fe3c4 100%)' }"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

type PetMood = 'idle' | 'happy' | 'neutral' | 'sad'

const props = defineProps<{
  mood: PetMood
  level: number
  exp: number
  expToNext: number
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

const expPct = computed(() => Math.min(100, (props.exp / props.expToNext) * 100))

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
