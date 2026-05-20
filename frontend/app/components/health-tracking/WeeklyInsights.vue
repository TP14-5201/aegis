<template>
  <div class="w-full space-y-5">
    <!-- Stat cards row -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="rounded-2xl p-5 border"
        style="background:rgba(255,255,255,0.9); border-color:#dce9ff;"
      >
        <div class="flex items-center gap-2 mb-2">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background:#dce9ff; color:#0d1c2e;">
            <component :is="stat.icon" class="w-4 h-4" stroke-width="2.5" />
          </div>
          <span class="font-body" style="font-weight:700; font-size:10px; letter-spacing:0.14em; text-transform:uppercase; color:#0d1c2e; opacity:0.6;">
            {{ stat.label }}
          </span>
        </div>
        <div class="font-display" style="font-size:30px; font-weight:800; color:#0d1c2e; line-height:1;">
          {{ stat.value }}<span style="font-size:14px; opacity:0.55; font-weight:700;">{{ stat.suffix }}</span>
        </div>
      </div>
    </div>

    <!-- Line chart + Insight card row -->
    <div class="grid lg:grid-cols-3 gap-5">
      <!-- Line chart (7-day EXP trend) -->
      <div class="lg:col-span-2 rounded-3xl p-7 border shadow-xl" style="background:rgba(255,255,255,0.95); border-color:#dce9ff;">
        <div class="flex items-center justify-between mb-5">
          <div>
            <div class="font-body" style="color:#0d1c2e; opacity:0.55; font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">
              Last 7 days
            </div>
            <h3 class="font-display" style="color:#0d1c2e; font-size:22px; line-height:1.1; font-weight:800;">
              Your weekly rhythm
            </h3>
          </div>
        </div>
        <div v-if="hasAnyData" class="w-full" style="height:200px; overflow:visible;">
          <svg :viewBox="`0 0 ${lineW} ${lineH}`" class="w-full h-full" preserveAspectRatio="xMidYMid meet">
            <!-- Y-axis rotated label -->
            <text
              x="6"
              :y="padT + (lineH - padT - padB) / 2"
              text-anchor="middle"
              font-family="Plus Jakarta Sans"
              font-weight="700"
              font-size="9"
              fill="#0d1c2e"
              opacity="0.42"
              :transform="`rotate(-90, 6, ${padT + (lineH - padT - padB) / 2})`"
            >pts</text>
            <!-- Y-axis value labels -->
            <text
              v-for="(gl, idx) in gridLines"
              :key="'yl-' + idx"
              :x="padL - 5"
              :y="gl + 3"
              text-anchor="end"
              font-family="Plus Jakarta Sans"
              font-weight="700"
              font-size="9"
              fill="#0d1c2e"
              opacity="0.38"
            >{{ gridLineValues[idx] }}</text>
            <!-- Grid lines -->
            <line v-for="gl in gridLines" :key="gl" :x1="padL" :y1="gl" :x2="lineW - padR" :y2="gl" stroke="#dce9ff" stroke-dasharray="3 3" stroke-width="1" />
            <!-- Area fill -->
            <path :d="areaPath" fill="#0d1c2e" fill-opacity="0.06" />
            <!-- Line -->
            <polyline :points="linePoints" fill="none" stroke="#0d1c2e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
            <!-- Dots -->
            <circle
              v-for="(pt, i) in chartPts"
              :key="i"
              :cx="pt.x"
              :cy="pt.y"
              r="5"
              fill="white"
              stroke="#0d1c2e"
              stroke-width="2.5"
            />
            <!-- X labels -->
            <text
              v-for="(d, i) in weekData"
              :key="'xl-' + i"
              :x="chartPts[i]?.x ?? 0"
              :y="lineH - 2"
              text-anchor="middle"
              font-family="Plus Jakarta Sans"
              font-weight="700"
              font-size="11"
              fill="#0d1c2e"
              opacity="0.55"
            >{{ d.day }}</text>
          </svg>
        </div>
        <div v-else class="w-full flex items-center justify-center text-center font-body" style="height:200px; color:#0d1c2e; opacity:0.45; font-weight:600; font-size:13px;">
          Complete a check-in to see your weekly rhythm.
        </div>
      </div>

      <!-- Insight card -->
      <div class="rounded-3xl p-7 border shadow-xl flex flex-col gap-4" style="background:#0d1c2e; color:#dce9ff; border-color:#0d1c2e;">
        <div>
          <span class="font-body" style="font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; opacity:0.7;">
            Gentle insight
          </span>
        </div>
        <h3 class="font-display" style="font-size:22px; line-height:1.15; color:white; font-weight:800;">
          {{ insight.title }}
        </h3>
        <p class="font-body" style="font-weight:500; font-size:14px; line-height:1.6; opacity:0.85;">
          {{ insight.body }}
        </p>
      </div>
    </div>

    <!-- Radar + Today row -->
    <div class="grid lg:grid-cols-2 gap-5">
      <!-- Radar chart - 7-day average balance -->
      <div class="rounded-3xl p-6 border shadow-xl" style="background:rgba(255,255,255,0.95); border-color:#dce9ff;">
        <div class="font-body" style="color:#0d1c2e; opacity:0.55; font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">
          Habit balance
        </div>
        <h4 class="font-display mb-4" style="color:#0d1c2e; font-size:20px; font-weight:800;">7-day average</h4>
        <div v-if="hasRadarData" class="flex items-center justify-center" style="height:210px;">
          <svg :viewBox="`0 0 ${radarSize} ${radarSize}`" class="w-full h-full" style="max-width:210px;" preserveAspectRatio="xMidYMid meet">
            <!-- Background grid rings -->
            <polygon
              v-for="ring in radarRings"
              :key="ring"
              :points="radarGridPoly(ring)"
              fill="none"
              stroke="#dce9ff"
              stroke-width="1"
            />
            <!-- Axes -->
            <line
              v-for="(dim, i) in radarDims"
              :key="'ax-' + i"
              :x1="radarCenter"
              :y1="radarCenter"
              :x2="radarAxisEnd(i).x"
              :y2="radarAxisEnd(i).y"
              stroke="#dce9ff"
              stroke-width="1"
            />
            <!-- Data polygon -->
            <polygon
              :points="radarDataPoly"
              fill="#0d1c2e"
              fill-opacity="0.2"
              stroke="#0d1c2e"
              stroke-width="2"
            />
            <!-- Labels -->
            <text
              v-for="(dim, i) in radarDims"
              :key="'lb-' + i"
              :x="radarLabelPos(i).x"
              :y="radarLabelPos(i).y"
              text-anchor="middle"
              dominant-baseline="middle"
              font-family="Plus Jakarta Sans"
              font-weight="700"
              font-size="10"
              fill="#0d1c2e"
              opacity="0.7"
            >{{ dim.label }}</text>
          </svg>
        </div>
        <div v-else class="w-full flex items-center justify-center text-center font-body" style="height:210px; color:#0d1c2e; opacity:0.45; font-weight:600; font-size:13px;">
          Complete a check-in to see your habit balance.
        </div>
      </div>

      <!-- Today's result -->
      <div class="rounded-3xl p-6 border shadow-xl" style="background:rgba(255,255,255,0.95); border-color:#dce9ff;">
        <div class="font-body" style="color:#0d1c2e; opacity:0.55; font-weight:700; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">
          Today's result
        </div>
        <h4 class="font-display mb-4" style="color:#0d1c2e; font-size:20px; font-weight:800;">How today felt</h4>
        <div v-if="hasTodayData" class="flex flex-col gap-3">
          <!-- EXP gauge -->
          <div>
            <div class="flex justify-between font-body mb-1" style="font-size:12px; font-weight:700; color:#0d1c2e; opacity:0.6;">
              <span>pts earned today</span>
              <span>{{ todayExpValue }} pts</span>
            </div>
            <div class="w-full h-3 rounded-full overflow-hidden" style="background:#dce9ff;">
              <div
                class="h-full rounded-full transition-all duration-700"
                :style="{ width: todayExpPct + '%', background: expBarColor }"
              />
            </div>
            <div class="flex justify-between font-body mt-1" style="font-size:11px; font-weight:700; color:#0d1c2e; opacity:0.4;">
              <span>Needs care</span><span>Thriving</span>
            </div>
          </div>

          <!-- Mood badge -->
          <div
            class="flex items-center gap-3 p-3 rounded-2xl"
            :style="{ background: moodBgColor }"
          >
            <span style="font-size:28px;">{{ moodEmoji }}</span>
            <div>
              <div class="font-body" style="font-weight:700; font-size:13px; color:#0d1c2e;">{{ moodLabel }}</div>
              <div class="font-body" style="font-weight:600; font-size:11px; color:#0d1c2e; opacity:0.6;">{{ moodDescription }}</div>
            </div>
          </div>

          <!-- Dimension breakdown -->
          <div class="space-y-1.5">
            <div v-for="dim in todayDimensions" :key="dim.key" class="flex items-center gap-2">
              <div class="font-body shrink-0" style="font-size:10px; font-weight:700; color:#0d1c2e; opacity:0.55; width:72px; text-transform:uppercase; letter-spacing:0.06em;">
                {{ dim.label }}
              </div>
              <div class="flex-1 h-1.5 rounded-full overflow-hidden" style="background:#dce9ff;">
                <div class="h-full rounded-full" :style="{ width: dim.pct + '%', background: '#0d1c2e' }" />
              </div>
              <span class="font-body shrink-0" style="font-size:10px; font-weight:700; color:#0d1c2e; opacity:0.55; width:24px; text-align:right;">
                {{ dim.exp }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="w-full flex items-center justify-center text-center font-body" style="height:210px; color:#0d1c2e; opacity:0.45; font-weight:600; font-size:13px;">
          Complete a check-in to see today's blend.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TrendingUp, Heart, Flame, Award } from 'lucide-vue-next'

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

const props = defineProps<{
  weekData: DayData[]
  todayDimensions: TodayDim[]
  todayExp: number
  todayMaxExp: number
  todayMood: 'happy' | 'neutral' | 'sad' | 'none'
}>()

// --- Stat cards ---
const totalExp = computed(() => props.weekData.reduce((s, d) => s + d.exp, 0))
const avgExp = computed(() => {
  const days = props.weekData.filter(d => d.exp > 0)
  return days.length ? Math.round(totalExp.value / days.length) : 0
})
const happyDays = computed(() => props.weekData.filter(d => d.mood === 'happy').length)
const streak = computed(() => {
  let s = 0
  for (let i = props.weekData.length - 1; i >= 0; i--) {
    if (props.weekData[i].exp > 0) s++
    else break
  }
  return s
})

const stats = computed(() => [
  { icon: Award, label: 'Total pts', value: totalExp.value, suffix: '' },
  { icon: TrendingUp, label: 'Daily avg', value: avgExp.value, suffix: ' pts' },
  { icon: Heart, label: 'Bright days', value: happyDays.value, suffix: ' / 7' },
  { icon: Flame, label: 'Streak', value: streak.value, suffix: ' days' },
])

const hasAnyData = computed(() => props.weekData.some(d => d.exp > 0))

// --- Insight text ---
const insight = computed(() => {
  if (happyDays.value >= 5) return {
    title: 'You are glowing this week.',
    body: 'Your habits show real care for yourself. Keep the gentle rhythm - small consistency is everything.',
  }
  if (happyDays.value >= 2) return {
    title: 'Steady, soft progress.',
    body: 'Try anchoring one habit - water, a short walk, or quiet - to a moment you already protect.',
  }
  return {
    title: 'Heavy weeks are real.',
    body: 'Be kind to yourself. Even one tiny thing counts. You showed up to track, and that matters.',
  }
})

// --- Line chart ---
const lineW = 400
const lineH = 170
const padL = 40
const padR = 10
const padT = 12
const padB = 22

const lineMaxExp = computed(() => Math.max(...props.weekData.map(d => d.exp), 10))
const gridLineValues = computed(() => [0.25, 0.5, 0.75, 1].map(f => Math.round(lineMaxExp.value * f)))

const chartPts = computed(() => {
  const maxExp = Math.max(...props.weekData.map(d => d.exp), 10)
  return props.weekData.map((d, i) => {
    const x = padL + (i / (props.weekData.length - 1)) * (lineW - padL - padR)
    const y = padT + (1 - d.exp / maxExp) * (lineH - padT - padB)
    return { x, y }
  })
})

const linePoints = computed(() =>
  chartPts.value.map(p => `${p.x},${p.y}`).join(' ')
)

const areaPath = computed(() => {
  const pts = chartPts.value
  if (!pts.length) return ''
  const bottom = lineH - padB
  const first = pts[0]
  const last = pts[pts.length - 1]
  return `M${first.x},${bottom} ${pts.map(p => `L${p.x},${p.y}`).join(' ')} L${last.x},${bottom} Z`
})

const gridLines = computed(() => {
  const bottom = lineH - padB
  const top = padT
  return [0.25, 0.5, 0.75, 1].map(f => top + (1 - f) * (bottom - top))
})

// --- Radar chart ---
const radarSize = 210
const radarCenter = radarSize / 2
const radarRadius = radarSize / 2 - 28
const radarRings = [0.25, 0.5, 0.75, 1.0]

const radarDims = [
  { key: 'mood', label: 'Mood' },
  { key: 'rest', label: 'Rest' },
  { key: 'exercise', label: 'Exercise' },
  { key: 'self_discipline', label: 'Self-care' },
  { key: 'vitamin', label: 'Vitamins' },
  { key: 'protein', label: 'Protein' },
  { key: 'carb', label: 'Energy' },
]

function radarAngle(i: number) {
  return (2 * Math.PI * i) / radarDims.length - Math.PI / 2
}

function radarPoint(i: number, r: number) {
  const a = radarAngle(i)
  return { x: radarCenter + r * Math.cos(a), y: radarCenter + r * Math.sin(a) }
}

function radarGridPoly(fraction: number) {
  return radarDims.map((_, i) => {
    const p = radarPoint(i, radarRadius * fraction)
    return `${p.x},${p.y}`
  }).join(' ')
}

function radarAxisEnd(i: number) {
  return radarPoint(i, radarRadius)
}

function radarLabelPos(i: number) {
  const p = radarPoint(i, radarRadius + 14)
  return p
}

const radarAverages = computed(() => {
  const days = props.weekData.filter(d => d.exp > 0 && d.scores)
  return radarDims.map(dim => {
    const vals = days.map(d => d.scores?.[dim.key] ?? 0).filter(v => v > 0)
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0
  })
})

const hasRadarData = computed(() => radarAverages.value.some(v => v > 0))

const radarDataPoly = computed(() => {
  return radarDims.map((_, i) => {
    const fraction = Math.min(1, radarAverages.value[i] / 20)
    const p = radarPoint(i, radarRadius * fraction)
    return `${p.x},${p.y}`
  }).join(' ')
})

const hasTodayData = computed(() => props.todayDimensions.length > 0)

// --- Today mood / EXP ---
const todayExpValue = computed(() => props.todayExp)
const todayExpPct = computed(() => props.todayMaxExp > 0 ? Math.round((props.todayExp / props.todayMaxExp) * 100) : 0)

const expBarColor = computed(() => {
  const pct = todayExpPct.value
  if (pct >= 70) return 'linear-gradient(90deg, #0d1c2e, #7fe3c4)'
  if (pct >= 40) return 'linear-gradient(90deg, #396477, #dce9ff)'
  return 'linear-gradient(90deg, #f8c7c7, #e78284)'
})

const moodEmoji = computed(() => {
  if (props.todayMood === 'happy') return '🌟'
  if (props.todayMood === 'sad') return '💙'
  return '🌤'
})
const moodLabel = computed(() => {
  if (props.todayMood === 'happy') return 'Healthy day!'
  if (props.todayMood === 'sad') return 'Needs more care'
  return 'Steady progress'
})
const moodDescription = computed(() => {
  if (props.todayMood === 'happy') return 'Your habits are really shining today.'
  if (props.todayMood === 'sad') return 'Tomorrow is a fresh start.'
  return 'Every effort counts - keep going.'
})
const moodBgColor = computed(() => {
  if (props.todayMood === 'happy') return '#f0fdf4'
  if (props.todayMood === 'sad') return '#fef2f2'
  return '#f0f9ff'
})

const todayDimensions = computed(() =>
  props.todayDimensions.map(d => ({
    ...d,
    pct: Math.round((d.exp / 20) * 100),
  }))
)
</script>
