<template>
  <section class="w-full bg-white py-8 lg:py-12">
    <div class="mx-auto min-h-[1240px] w-full max-w-[1280px] px-4 sm:px-6 lg:px-4">
      <div class="flex items-center gap-4">
        <span class="font-volkhov text-[42px] font-bold leading-none text-[#DF6951]">01</span>
        <p class="font-roboto text-[18px] font-bold uppercase tracking-[0.12em] text-[#434656]">
          Around Us . Victoria
        </p>
      </div>

      <h2 class="mt-5 font-volkhov text-[42px] font-bold leading-[0.95] text-black sm:text-[56px] lg:text-[64px]">
        It's happening
        <span class="font-normal italic text-[#DF6951]">right here.</span>
      </h2>
      <p class="mt-5 max-w-[720px] font-roboto text-[16px] leading-7 text-[#434656]">
        Every region in Victoria tells a different story. Click a category on the left - the
        map recolours to that data layer. Click any region to read its story on the right.
      </p>

      <div class="mt-7 flex flex-col gap-3 lg:flex-row">
        <div class="relative flex-1">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Mount Alexander"
            class="h-[50px] w-full rounded-[6px] border border-[#C3C5D9] bg-white px-5 pl-12 font-roboto text-[14px]
                   text-[#131B2E] shadow-sm outline-none transition placeholder:text-[#6B7280]
                   focus:border-[#0052FF] focus:ring-2 focus:ring-[#B5DCFF99]"
            @input="filterLgas"
            @focus="showDropdown = filteredLgas.length > 0"
            @blur="onSearchBlur"
          />
          <Search class="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-[#434656]" :stroke-width="2" />

          <ul
            v-if="showDropdown && filteredLgas.length"
            class="absolute z-30 mt-2 max-h-60 w-full overflow-y-auto rounded-[8px] border border-[#C3C5D9] bg-white shadow-card"
          >
            <li
              v-for="lga in filteredLgas"
              :key="lga"
              class="cursor-pointer px-5 py-3 font-roboto text-[15px] text-[#131B2E] hover:bg-[#B5DCFF54]"
              @mousedown.prevent="selectLgaFromSearch(lga)"
            >
              {{ lga }}
            </li>
          </ul>
        </div>

        <button
          class="flex h-[46px] items-center justify-center gap-2 rounded-[6px] bg-[#B5DCFF99] px-6
                 font-roboto text-[13px] font-semibold text-[#131B2E] transition hover:bg-[#B5DCFF] disabled:opacity-60 lg:h-[44px]"
          :disabled="isLoadingLocation"
          @click="useMyLocation"
        >
          <span v-if="isLoadingLocation" class="inline-block h-4 w-4 animate-spin rounded-full border-2 border-[#131B2E] border-t-transparent" />
          <LocateFixed v-else class="h-4 w-4" :stroke-width="2" />
          Use My Location
        </button>

        <button
          class="flex h-[46px] items-center justify-center rounded-[6px] bg-black px-7
                 font-roboto text-[13px] font-semibold text-white transition hover:bg-[#131B2E] disabled:cursor-not-allowed disabled:opacity-50 lg:h-[44px]"
          :disabled="!selectedLgaName"
          @click="resetMap"
        >
          Reset
        </button>
      </div>

      <div class="mt-6 grid grid-cols-1 gap-x-5 gap-y-7 lg:grid-cols-[230px_minmax(0,1fr)]">
        <aside class="space-y-6 lg:row-span-2">
          <div>
            <p class="mb-5 font-roboto text-[12px] font-bold uppercase tracking-[0.14em] text-[#434656]">
              Headline Data
            </p>
            <div class="space-y-4">
              <button
                v-for="m in metrics"
                :key="m.key"
                class="group flex h-[90px] w-full items-center gap-4 rounded-[8px] px-6 text-left shadow-card transition duration-200 hover:-translate-y-0.5"
                :class="currentMetric === m.key ? 'ring-2 ring-[#131B2E]/20' : ''"
                :style="{ backgroundColor: m.color }"
                @click="setMetric(m.key)"
              >
                <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-[4px] bg-white/20 text-white">
                  <component :is="m.icon" class="h-5 w-5" :stroke-width="2" />
                </span>
                <span>
                  <span class="block font-roboto text-[12px] font-bold uppercase leading-tight tracking-[0.08em] text-white">
                    {{ m.eyebrow }}
                  </span>
                  <span class="block font-volkhov text-[18px] font-bold leading-tight text-white">
                    {{ m.label }}
                  </span>
                </span>
              </button>
            </div>
          </div>

          <div class="h-px bg-[#C3C5D9]" />

          <div>
            <p class="mb-5 font-roboto text-[12px] font-bold uppercase tracking-[0.14em] text-[#434656]">
              Why? - Barriers
            </p>
            <div class="space-y-3">
              <button
                v-for="reason in barrierMetrics"
                :key="reason.key"
                class="flex min-h-[78px] w-full items-center gap-4 rounded-[8px] border bg-white px-6 text-left shadow-card transition duration-200 hover:-translate-y-0.5"
                :class="currentMetric === reason.key ? 'border-[#131B2E] ring-2 ring-[#B5DCFF99]' : 'border-[#C3C5D9]'"
                @click="setMetric(reason.key)"
              >
                <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-[6px] bg-[#B5DCFF99] text-[#131B2E]">
                  <component :is="reason.icon" class="h-4 w-4" :stroke-width="2" />
                </span>
                <span>
                  <span class="block font-roboto text-[11px] font-bold uppercase tracking-[0.08em] text-[#434656]">
                    {{ reason.eyebrow }}
                  </span>
                  <span class="block font-roboto text-[13px] font-extrabold leading-tight text-[#131B2E]">
                    {{ reason.label }}
                  </span>
                </span>
              </button>
            </div>
          </div>
        </aside>

        <div class="relative h-[420px] w-full overflow-hidden rounded-[10px] border border-[#C3C5D9] bg-[#B5DCFF99] shadow-sm sm:h-[520px] lg:h-[622px]">
          <div
            v-if="isMapLoading"
            class="absolute inset-0 z-20 flex flex-col items-center justify-center gap-4 bg-white/90 backdrop-blur-sm"
          >
            <div class="relative h-14 w-14">
              <div class="absolute inset-0 rounded-full border-[3px] border-[#B5DCFF99]" />
              <div class="absolute inset-0 animate-spin rounded-full border-[3px] border-t-[#0052FF]" />
            </div>
            <p class="font-roboto font-bold text-[#131B2E]">Mapping Victoria...</p>
          </div>

          <div ref="mapEl" class="h-full w-full" />

          <div class="absolute left-4 top-4 z-10 rounded-[6px] bg-white/90 px-5 py-4 shadow-sm">
            <p class="font-roboto text-[10px] font-bold uppercase tracking-[0.12em] text-[#434656]">Layer</p>
            <p class="font-volkhov text-[18px] font-bold leading-tight text-[#131B2E]">{{ currentLayerTitle }}</p>
          </div>

          <div class="absolute right-4 top-4 z-10 flex flex-col overflow-hidden rounded-[6px] border border-[#C3C5D9] bg-white shadow-sm">
            <button class="flex h-10 w-10 items-center justify-center border-b border-[#C3C5D9] text-[#131B2E] hover:bg-[#B5DCFF54]" aria-label="Zoom in" @click="zoomMapIn">
              <Plus class="h-4 w-4" :stroke-width="2.5" />
            </button>
            <button class="flex h-10 w-10 items-center justify-center border-b border-[#C3C5D9] text-[#131B2E] hover:bg-[#B5DCFF54]" aria-label="Zoom out" @click="zoomMapOut">
              <Minus class="h-4 w-4" :stroke-width="2.5" />
            </button>
            <button class="flex h-10 w-10 items-center justify-center text-[#131B2E] hover:bg-[#B5DCFF54]" aria-label="Reset map view" @click="resetMap">
              <Home class="h-4 w-4" :stroke-width="2" />
            </button>
          </div>

          <div class="absolute bottom-5 left-4 z-10 rounded-[6px] bg-white/90 p-4 shadow-sm">
            <h4 class="mb-3 font-roboto text-[12px] font-bold uppercase tracking-[0.08em] text-[#434656]">
              {{ legendTitle }}
            </h4>
            <div class="flex flex-col gap-2 font-roboto text-[12px] font-semibold text-[#434656]">
              <div v-for="item in legendItems" :key="item.label" class="flex items-center gap-2">
                <span class="h-3 w-3" :style="{ backgroundColor: item.color }" />
                {{ item.label }}
              </div>
            </div>
          </div>

          <p class="absolute bottom-5 right-5 z-10 rounded bg-white/30 px-2 py-1 font-roboto text-[9px] text-[#434656]">
            Mapbox - Victoria LGA boundaries
          </p>
        </div>

        <div class="grid gap-5 lg:col-start-2 lg:grid-cols-[minmax(0,1fr)_230px_255px]">
          <div class="rounded-[8px] border border-[#C3C5D9] bg-white px-7 py-7 shadow-card">
            <div v-if="isStatsLoading" class="animate-pulse space-y-4">
              <div class="h-3 w-32 rounded bg-[#C3C5D9]" />
              <div class="h-7 w-56 rounded bg-[#C3C5D9]" />
              <div class="h-4 w-full rounded bg-[#C3C5D9]" />
              <div class="h-4 w-2/3 rounded bg-[#C3C5D9]" />
            </div>
            <div v-else :class="['picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
              <p class="font-roboto text-[11px] font-bold uppercase tracking-[0.12em] text-[#434656]">
                Now Viewing
              </p>
              <h3 class="mt-2 font-volkhov text-[24px] font-bold leading-tight text-[#DF6951]">
                {{ selectedLgaStat?.lga_name || 'Select a region' }}
              </h3>
              <p class="mt-7 font-roboto text-[15px] leading-6 text-[#434656]">
                {{ selectedStory }}
              </p>
            </div>
          </div>

          <div class="flex min-h-[160px] flex-col items-center justify-center rounded-[8px] border border-[#131B2E] bg-[#B5DCFF54] px-5 py-6 text-center">
            <p class="font-roboto text-[12px] font-bold uppercase tracking-[0.08em] text-[#434656]">
              {{ selectedMetricLabel }}
            </p>
            <p class="mt-5 font-volkhov text-[50px] font-bold leading-none text-[#DF6951]">
              {{ selectedMetricDisplay }}<span v-if="selectedMetricSuffix" class="font-normal">{{ selectedMetricSuffix }}</span>
            </p>
          </div>

          <div class="flex min-h-[160px] flex-col justify-between rounded-[8px] border border-[#131B2E] bg-white px-6 py-7 shadow-sm">
            <p class="font-roboto text-[18px] leading-7 text-black">
              Need food now? Find the nearest open site today.
            </p>
            <NuxtLink
              to="/food-banks"
              class="mt-5 flex h-[58px] items-center justify-center rounded-[6px] bg-black px-5 font-roboto text-[16px] font-semibold text-white transition hover:bg-[#131B2E]"
            >
              View Food Banks
            </NuxtLink>
          </div>
        </div>
      </div>

      <div class="mt-10 pt-6 text-[11px] text-[#6B7280]">
        <p class="mb-3 font-bold uppercase tracking-widest text-[#434656]">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-[#434656]">Food Insecurity:</span>
            <a href="https://vahi.vic.gov.au/reports/victorian-population-health-survey-2023" target="_blank" rel="noopener" class="underline decoration-[#C3C5D9] underline-offset-2 hover:text-[#0052FF]">
              VAHI (2023 Survey)
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-[#434656]">Emergency Services:</span>
            <a href="https://data.melbourne.vic.gov.au/explore/dataset/free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-/table/" target="_blank" rel="noopener" class="underline decoration-[#C3C5D9] underline-offset-2 hover:text-[#0052FF]">
              data.melbourne.vic.gov.au
            </a>
            <span class="opacity-30">&amp;</span>
            <a href="https://data.gov.au/data/dataset/emergency-relief-provider-outlets/resource/0e32d958-3796-4dca-8312-489ef7a610f6" target="_blank" rel="noopener" class="underline decoration-[#C3C5D9] underline-offset-2 hover:text-[#0052FF]">
              data.gov.au
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-[#434656]">Population by LGA:</span>
            <a href="https://digital.atlas.gov.au/datasets/digitalatlas::abs-population-and-people-data-by-region-lga-november-2025/about" target="_blank" rel="noopener" class="underline decoration-[#C3C5D9] underline-offset-2 hover:text-[#0052FF]">
              ABS (Nov 2025)
            </a>
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { point } from '@turf/helpers'
import booleanPointInPolygon from '@turf/boolean-point-in-polygon'
import {
  BadgeDollarSign,
  BarChart3,
  ClipboardX,
  Home,
  LocateFixed,
  Minus,
  Plus,
  Search,
  Store,
  Truck,
  UsersRound,
  WheatOff,
} from 'lucide-vue-next'

const config = useRuntimeConfig()
const API_URL = config.public.apiBase || 'http://127.0.0.1:8000'

const mapEl = ref(null)
let mapInstance = null
let lgaGeojson = null
let hoveredLgaId = null
let tooltipPopup = null

const lgaStats = ref([])
const reasonStats = ref([])
const selectedLgaName = ref(null)
const currentMetric = ref('foodInsecurity')

const searchQuery = ref('')
const filteredLgas = ref([])
const showDropdown = ref(false)
const searchIndex = ref([])
const isLoadingLocation = ref(false)
const isMapLoading = ref(true)
const isStatsLoading = ref(true)

const metrics = [
  {
    key: 'foodInsecurity',
    eyebrow: 'Food Insecurity',
    label: 'Rate %',
    layerLabel: 'Food Insecurity',
    color: '#DF6951',
    icon: BarChart3,
  },
  {
    key: 'peopleAffected',
    eyebrow: 'People Affected',
    label: 'Adults',
    layerLabel: 'People Affected',
    color: '#5F805F',
    icon: UsersRound,
  },
  {
    key: 'foodBanks',
    eyebrow: 'Food Banks',
    label: 'Active sites',
    layerLabel: 'Food Banks',
    color: '#B995E5',
    icon: Store,
  },
]

const barrierMetrics = [
  {
    key: 'limited_variety',
    eyebrow: 'Reason 01',
    label: 'Limited variety',
    layerLabel: 'Limited Variety',
    icon: WheatOff,
  },
  {
    key: 'too_expensive',
    eyebrow: 'Reason 02',
    label: 'Too expensive',
    layerLabel: 'Too Expensive',
    icon: BadgeDollarSign,
  },
  {
    key: 'wrong_quality',
    eyebrow: 'Reason 03',
    label: 'Wrong quality',
    layerLabel: 'Wrong Quality',
    icon: ClipboardX,
  },
  {
    key: 'transport_gap',
    eyebrow: 'Reason 04',
    label: 'Transport gap',
    layerLabel: 'Transport Gap',
    icon: Truck,
  },
]

const barrierKeys = new Set(barrierMetrics.map(m => m.key))

function getMetricDefinition(key) {
  return [...metrics, ...barrierMetrics].find(m => m.key === key) || metrics[0]
}

function setMetric(key) {
  if (currentMetric.value === key) return
  currentMetric.value = key
}

function filterLgas() {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) {
    filteredLgas.value = []
    showDropdown.value = false
    return
  }
  filteredLgas.value = searchIndex.value.filter(l => l.toLowerCase().includes(q)).slice(0, 12)
  showDropdown.value = filteredLgas.value.length > 0
}

function selectLgaFromSearch(lga) {
  searchQuery.value = lga
  showDropdown.value = false
  selectLga(lga)
}

function onSearchBlur() {
  setTimeout(() => { showDropdown.value = false }, 150)
}

function getFeatureBounds(feature) {
  const bounds = new mapboxgl.LngLatBounds()
  const coords = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates
  coords.forEach(polygon => polygon.forEach(ring => ring.forEach(c => bounds.extend(c))))
  return bounds
}

function normalizeLgaName(name) {
  return String(name || '')
    .toLowerCase()
    .replace(/\s*\(vic\.\)\s*/g, '')
    .replace(/\s*\((?:c|s|rc|b|shire|city)\)\s*/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

function selectLga(lgaName) {
  if (selectedLgaName.value === lgaName) {
    resetMap()
    return
  }
  selectedLgaName.value = lgaName
  if (mapInstance && mapInstance.isStyleLoaded() && lgaGeojson) {
    const lgaKey = normalizeLgaName(lgaName)
    const feature = lgaGeojson.features.find(f => f.properties.lga_name === lgaName || f.properties.lga_key === lgaKey)
    if (feature) {
      mapInstance.fitBounds(getFeatureBounds(feature), {
        padding: 60,
        maxZoom: 10,
        duration: 1000,
        essential: true,
      })
    }
    mapInstance.setPaintProperty('lga-fills', 'fill-opacity', [
      'case',
      ['==', ['get', 'lga_key'], lgaKey], 1.0,
      ['boolean', ['feature-state', 'hover'], false], 1.0,
      0.3,
    ])
  }
}

function resetMap() {
  selectedLgaName.value = null
  searchQuery.value = ''
  if (mapInstance && mapInstance.isStyleLoaded()) {
    mapInstance.flyTo({ center: [144.5, -36.5], zoom: 5.5, duration: 1000, essential: true })
    mapInstance.setPaintProperty('lga-fills', 'fill-opacity', [
      'case',
      ['boolean', ['feature-state', 'hover'], false], 1,
      0.75,
    ])
    mapInstance.setPaintProperty('lga-fills', 'fill-color', [
      'case',
      ['boolean', ['feature-state', 'hover'], false], '#FFFFFF',
      getFillColorExpression(),
    ])
  }
}

function zoomMapIn() {
  if (mapInstance) mapInstance.zoomIn({ duration: 300 })
}

function zoomMapOut() {
  if (mapInstance) mapInstance.zoomOut({ duration: 300 })
}

function useMyLocation() {
  if (!navigator.geolocation) {
    alert('Geolocation not supported.')
    return
  }
  isLoadingLocation.value = true
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const pt = point([position.coords.longitude, position.coords.latitude])
      if (lgaGeojson) {
        const feature = lgaGeojson.features.find(f => booleanPointInPolygon(pt, f))
        if (feature) {
          const lgaName = feature.properties.lga_name
          searchQuery.value = lgaName
          selectLga(lgaName)
        } else {
          alert('Your location is not within a known Victorian LGA.')
        }
      }
      isLoadingLocation.value = false
    },
    () => {
      alert('Unable to retrieve your location.')
      isLoadingLocation.value = false
    },
    { timeout: 10000 }
  )
}

const statsMap = computed(() => {
  const m = {}
  lgaStats.value.forEach((s) => {
    m[s.lga_name] = s
    m[s.lga_key] = s
  })
  return m
})

const reasonStatsMap = computed(() => {
  const m = {}
  reasonStats.value.forEach(s => { m[s.lga_name] = s })
  return m
})

const selectedLgaStat = computed(() => {
  if (!selectedLgaName.value) return null
  return statsMap.value[selectedLgaName.value] || statsMap.value[normalizeLgaName(selectedLgaName.value)] || null
})

const foodInsecurityStat = computed(() => {
  if (!selectedLgaStat.value) return 0
  return Math.round((selectedLgaStat.value.men_pct + selectedLgaStat.value.women_pct) / 2)
})

const peopleAffectedStat = computed(() => {
  if (!selectedLgaStat.value) return 0
  const totalPct = (selectedLgaStat.value.men_pct + selectedLgaStat.value.women_pct) / 2
  return Math.round((selectedLgaStat.value.pop_2024_total * totalPct) / 100)
})

const menNeedRatio = computed(() => {
  if (!selectedLgaStat.value) return 0
  return Math.max(1, Math.min(10, Math.round(selectedLgaStat.value.men_pct / 10)))
})

const womenNeedRatio = computed(() => {
  if (!selectedLgaStat.value) return 0
  return Math.max(1, Math.min(10, Math.round(selectedLgaStat.value.women_pct / 10)))
})

const foodBanksStat = computed(() => getFoodBankSites(selectedLgaStat.value))

function useCountUp(targetRef, duration = 700) {
  const display = ref(targetRef.value ?? 0)
  let rafId = null
  watch(targetRef, (newVal) => {
    if (rafId) cancelAnimationFrame(rafId)
    const startVal = display.value
    const endVal = newVal ?? 0
    let startTime = null
    function step(ts) {
      if (!startTime) startTime = ts
      const progress = Math.min((ts - startTime) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      display.value = Math.round(startVal + (endVal - startVal) * eased)
      if (progress < 1) rafId = requestAnimationFrame(step)
    }
    rafId = requestAnimationFrame(step)
  })
  return display
}

const displayFoodInsecurity = useCountUp(foodInsecurityStat)
const displayPeopleAffected = useCountUp(peopleAffectedStat)
const displayFoodBanks = useCountUp(foodBanksStat)

const selectedMetricValue = computed(() => {
  if (!selectedLgaStat.value) return 0
  return Math.round(getMetricValue(selectedLgaStat.value, currentMetric.value) ?? 0)
})

const displaySelectedMetric = useCountUp(selectedMetricValue)

const selectedMetricDisplay = computed(() => displaySelectedMetric.value.toLocaleString())
console.log(selectedMetricDisplay)

const selectedMetricSuffix = computed(() => {
  if (currentMetric.value === 'foodBanks' || currentMetric.value === 'peopleAffected') return ''
  return '%'
})

const selectedMetricLabel = computed(() => {
  if (currentMetric.value === 'foodInsecurity') return 'Food Insecurity Rate'
  return getMetricDefinition(currentMetric.value).layerLabel
})

const selectedStory = computed(() => {
  if (!selectedLgaStat.value) {
    return 'Select a region on the map or search above to view local statistics.'
  }

  const name = selectedLgaStat.value.lga_name
  if (currentMetric.value === 'foodBanks') {
    return `In ${name}, ${displayFoodBanks.value.toLocaleString()} active food bank sites are listed for people seeking food relief.`
  }
  if (currentMetric.value === 'peopleAffected') {
    return `In ${name}, roughly ${displayPeopleAffected.value.toLocaleString()} adults are estimated to have experienced food insecurity over the past year.`
  }
  if (barrierKeys.has(currentMetric.value)) {
    const value = getMetricValue(selectedLgaStat.value, currentMetric.value)
    if (value == null) {
      return `Barrier data for ${name} will appear here once the inaccessibility reasons API is available.`
    }
    return `In ${name}, roughly ${Math.round(value)}% of adults report "${getMetricDefinition(currentMetric.value).label.toLowerCase()}" as a barrier to food access.`
  }
  return `In ${name}, roughly ${displayFoodInsecurity.value}% of adults report going without enough food at some point over the past year.`
})

const pictogramVisible = ref(true)
watch(selectedLgaName, () => {
  pictogramVisible.value = false
  setTimeout(() => { pictogramVisible.value = true }, 280)
})

const currentLayerTitle = computed(() => getMetricDefinition(currentMetric.value).layerLabel)

const legendTitle = computed(() => {
  if (barrierKeys.has(currentMetric.value)) return 'Food Barriers'
  return currentLayerTitle.value
})

const paletteByMetric = {
  foodInsecurity: ['#FCE0D8', '#F4B5A6', '#EB8A75', '#DF6951', '#A83F2D'],
  peopleAffected: ['#E4EFE4', '#BFD2BF', '#92B092', '#5F805F', 'rgba(5, 52, 5, 0.66)'],
  foodBanks: ['#EFE4FA', '#D8BFF1', '#C49DE8', '#B995E5', 'rgba(84, 0, 195, 0.37)'],
  barrier: ['#EAF5FF', 'rgba(181, 220, 255, 0.6)', '#7EBEFF', '#0052FF', '#001452'],
}

function paletteForMetric(key) {
  if (key === 'foodBanks') return paletteByMetric.foodBanks
  if (key === 'peopleAffected') return paletteByMetric.peopleAffected
  if (barrierKeys.has(key)) return paletteByMetric.barrier
  return paletteByMetric.foodInsecurity
}

const legendItems = computed(() => {
  const palette = paletteForMetric(currentMetric.value)
  if (currentMetric.value === 'foodBanks') {
    return ['0-2', '3-5', '6-9', '10-14', '15+'].map((label, i) => ({ label, color: palette[i] }))
  }
  if (currentMetric.value === 'peopleAffected') {
    return ['<5k', '5-15k', '15-30k', '30-60k', '>60k'].map((label, i) => ({ label, color: palette[i] }))
  }
  if (barrierKeys.has(currentMetric.value)) {
    return ['<20%', '20-35%', '35-50%', '50-65%', '>65%'].map((label, i) => ({ label, color: palette[i] }))
  }
  return ['<6%', '6-8%', '8-10%', '10-12%', '>12%'].map((label, i) => ({ label, color: palette[i] }))
})

const legendColors = computed(() => legendItems.value.map(item => item.color))

function getMetricValue(stat, key) {
  if (!stat) return null
  if (key === 'foodInsecurity') return (stat.men_pct + stat.women_pct) / 2
  if (key === 'foodBanks') return getFoodBankSites(stat)
  if (key === 'peopleAffected') return stat.pop_2024_total * (stat.men_pct + stat.women_pct) / 200
  if (barrierKeys.has(key)) {
    const reason = reasonStatsMap.value[stat.lga_name]
    const value = reason?.[key]
    return Number.isFinite(value) ? value : null
  }
  return null
}

function colorForMetricValue(key, value) {
  if (value == null || Number.isNaN(value)) return '#C3C5D9'
  const palette = paletteForMetric(key)

  if (key === 'foodBanks') {
    if (value <= 2) return palette[0]
    if (value <= 5) return palette[1]
    if (value <= 9) return palette[2]
    if (value <= 14) return palette[3]
    return palette[4]
  }

  if (key === 'peopleAffected') {
    if (value < 5000) return palette[0]
    if (value < 15000) return palette[1]
    if (value < 30000) return palette[2]
    if (value < 60000) return palette[3]
    return palette[4]
  }

  if (barrierKeys.has(key)) {
    if (value < 20) return palette[0]
    if (value < 35) return palette[1]
    if (value < 50) return palette[2]
    if (value < 65) return palette[3]
    return palette[4]
  }

  if (value < 6) return palette[0]
  if (value < 8) return palette[1]
  if (value < 10) return palette[2]
  if (value < 12) return palette[3]
  return palette[4]
}

function getFillColorExpression() {
  if (!lgaStats.value.length) return '#C3C5D9'
  const expr = ['match', ['get', 'lga_key']]
  lgaStats.value.forEach(stat => {
    const color = colorForMetricValue(currentMetric.value, getMetricValue(stat, currentMetric.value))
    expr.push(stat.lga_key, color)
  })
  expr.push('#C3C5D9')
  return expr
}

watch(currentMetric, () => {
  if (mapInstance && mapInstance.isStyleLoaded() && mapInstance.getSource('lga')) {
    mapInstance.setPaintProperty('lga-fills', 'fill-color', [
      'case',
      ['boolean', ['feature-state', 'hover'], false], '#FFFFFF',
      getFillColorExpression(),
    ])
  }
})

watch(reasonStats, () => {
  if (mapInstance && mapInstance.isStyleLoaded() && mapInstance.getSource('lga') && barrierKeys.has(currentMetric.value)) {
    mapInstance.setPaintProperty('lga-fills', 'fill-color', [
      'case',
      ['boolean', ['feature-state', 'hover'], false], '#FFFFFF',
      getFillColorExpression(),
    ])
  }
})

function normalizeReasonRows(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(row => ({
    lga_name: row.lga_name ?? row.lga ?? row.name,
    limited_variety: toOptionalNumber(row.limited_variety ?? row.limitedVariety ?? row.variety),
    too_expensive: toOptionalNumber(row.too_expensive ?? row.tooExpensive ?? row.expensive),
    wrong_quality: toOptionalNumber(row.wrong_quality ?? row.wrongQuality ?? row.quality),
    transport_gap: toOptionalNumber(row.transport_gap ?? row.transportGap ?? row.transport),
  })).filter(row => row.lga_name)
}

function normalizeStatsRows(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(row => ({
    ...row,
    lga_key: normalizeLgaName(row.lga_name),
    men_pct: Number(row.men_pct ?? 0),
    women_pct: Number(row.women_pct ?? 0),
    pop_2024_total: Number(row.pop_2024_total ?? 0),
    food_bank_sites: getFoodBankSites(row),
  }))
}

function getFoodBankSites(stat) {
  if (!stat) return 0
  return toOptionalNumber(
    stat.food_bank_sites
    ?? stat.emergency_services_count
    ?? stat.foodBanks
    ?? stat.food_banks
    ?? stat.food_banks_count
    ?? stat.active_food_bank_sites
    ?? stat.support_services_count
  ) ?? 0
}

function toOptionalNumber(value) {
  if (value == null || value === '') return null
  const numberValue = Number(value)
  return Number.isFinite(numberValue) ? numberValue : null
}

async function fetchJsonIfOk(url) {
  const response = await fetch(url)
  if (!response.ok) return []
  return response.json()
}

onMounted(async () => {
  const token = config.public.mapboxToken
  if (!token) {
    console.warn('NUXT_PUBLIC_MAPBOX_TOKEN is not set; map will not load.')
    isMapLoading.value = false
  }

  const [statsResult, boundariesResult, reasonsResult] = await Promise.allSettled([
    fetch(`${API_URL}/lga/stats`).then(r => r.json()),
    fetch(`${API_URL}/lga/boundaries`).then(r => r.json()),
    fetchJsonIfOk(`${API_URL}/lga/food-inaccessibility-reasons`),
  ])

  if (statsResult.status === 'fulfilled') {
    lgaStats.value = normalizeStatsRows(statsResult.value)
    searchIndex.value = [...new Set(lgaStats.value.map(s => s.lga_name))].sort()
  } else {
    console.error('Failed to fetch LGA stats', statsResult.reason)
  }
  isStatsLoading.value = false

  if (boundariesResult.status === 'fulfilled') {
    lgaGeojson = boundariesResult.value
    lgaGeojson.features.forEach((f, i) => {
      f.id = i
      f.properties.lga_key = normalizeLgaName(f.properties.lga_name)
    })
  } else {
    console.error('Failed to fetch LGA boundaries', boundariesResult.reason)
  }

  if (reasonsResult.status === 'fulfilled') {
    reasonStats.value = normalizeReasonRows(reasonsResult.value)
  } else {
    reasonStats.value = []
  }

  if (!token) return

  mapboxgl.accessToken = token
  await nextTick()
  mapInstance = new mapboxgl.Map({
    container: mapEl.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: [144.5, -36.5],
    zoom: 5.5,
    scrollZoom: false,
  })
  tooltipPopup = new mapboxgl.Popup({ closeButton: false, closeOnClick: false, className: 'lga-tooltip-popup' })

  mapInstance.on('load', () => {
    try {
      if (!lgaGeojson) {
        console.warn('LGA boundaries not available; map layers skipped.')
        return
      }

      mapInstance.addSource('lga', { type: 'geojson', data: lgaGeojson })
      mapInstance.addLayer({
        id: 'lga-fills',
        type: 'fill',
        source: 'lga',
        paint: {
          'fill-color': ['case', ['boolean', ['feature-state', 'hover'], false], '#FFFFFF', getFillColorExpression()],
          'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 1, 0.75],
        },
      })
      mapInstance.addLayer({
        id: 'lga-borders',
        type: 'line',
        source: 'lga',
        paint: { 'line-color': '#FFFFFF', 'line-width': 0.8 },
      })

      mapInstance.on('mousemove', 'lga-fills', (e) => {
        if (!e.features.length) return
        if (hoveredLgaId !== null) mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: false })
        hoveredLgaId = e.features[0].id
        mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: true })
        mapInstance.getCanvas().style.cursor = 'pointer'
        const lgaName = e.features[0].properties.lga_name
        tooltipPopup.setLngLat(e.lngLat)
          .setHTML(`<div style="color:#131B2E;font-weight:bold;">${lgaName}</div>`)
          .addTo(mapInstance)
      })
      mapInstance.on('mouseleave', 'lga-fills', () => {
        if (hoveredLgaId !== null) mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: false })
        hoveredLgaId = null
        mapInstance.getCanvas().style.cursor = ''
        tooltipPopup.remove()
      })
      mapInstance.on('click', 'lga-fills', (e) => {
        if (!e.features.length) return
        const lgaName = e.features[0].properties.lga_name
        searchQuery.value = lgaName
        selectLga(lgaName)
      })
    } catch (err) {
      console.error('Map load error', err)
    } finally {
      setTimeout(() => { isMapLoading.value = false }, 300)
    }
  })
})

onBeforeUnmount(() => {
  if (mapInstance) mapInstance.remove()
})
</script>

<style scoped>
:deep(.mapboxgl-popup-content) {
  padding: 8px 12px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-family: 'Plus Jakarta Sans', sans-serif;
}

:deep(.mapboxgl-popup-tip) {
  display: none;
}

.picto-fade {
  transition: opacity 0.25s ease;
}

.picto-out {
  opacity: 0;
}

.picto-in {
  opacity: 1;
}
</style>
