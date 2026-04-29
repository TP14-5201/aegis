<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <!-- Section heading -->
      <p
        class="font-roboto font-bold text-coral text-[16px] lg:text-[20px] tracking-[2px] uppercase"
      >
        Around Us
      </p>
      <h2
        class="mt-3 font-volkhov font-bold text-navy
               text-[28px] sm:text-[36px] lg:text-[48px] leading-tight"
      >
        It's happening right here
      </h2>
      <p class="mt-4 font-roboto text-[16px] lg:text-[20px] text-black max-w-4xl leading-relaxed">
        Every region in Victoria tells a different story. Click yours to see the
        full picture — food insecurity rates, people affected, and the food banks
        trying to help.
      </p>

      <!-- Search row -->
      <div class="mt-8 flex flex-col sm:flex-row gap-3 sm:gap-4">
        <div class="relative flex-1 sm:flex-[2]">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Enter your LGA (e.g. Melbourne)"
            class="w-full h-[52px] bg-white border border-gray-300 rounded-[14px] px-5 pl-12
                   text-navy placeholder-gray-400 font-roboto text-[15px]
                   focus:outline-none focus:border-sky-active focus:ring-2 focus:ring-sky-active/20"
            @input="filterLgas"
            @focus="showDropdown = filteredLgas.length > 0"
            @blur="onSearchBlur"
          />
          <!-- Search icon -->
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" stroke-linecap="round" />
          </svg>
          <!-- Autocomplete dropdown -->
          <ul
            v-if="showDropdown && filteredLgas.length"
            class="absolute z-30 w-full bg-white border border-gray-200 rounded-[14px] mt-2 max-h-60 overflow-y-auto shadow-card"
          >
            <li
              v-for="lga in filteredLgas"
              :key="lga"
              class="px-5 py-3 text-navy hover:bg-sky-tint cursor-pointer font-roboto text-[15px]"
              @mousedown.prevent="selectLgaFromSearch(lga)"
            >
              {{ lga }}
            </li>
          </ul>
        </div>

        <button
          class="h-[52px] flex items-center justify-center gap-2 px-5 sm:px-6
                 bg-white border border-gray-300 rounded-[14px]
                 text-navy font-roboto font-semibold text-[14px]
                 hover:bg-sky-tint transition-colors disabled:opacity-50"
          :disabled="isLoadingLocation"
          @click="useMyLocation"
        >
          <span v-if="isLoadingLocation" class="inline-block w-4 h-4 border-2 border-navy border-t-transparent rounded-full animate-spin" />
          <span v-else>📍</span>
          Use My Location
        </button>

        <button
          v-if="selectedLgaName"
          class="h-[52px] flex items-center justify-center gap-2 px-5 sm:px-6
                 bg-navy hover:bg-navy-deep rounded-[14px]
                 text-white font-roboto font-semibold text-[14px] transition-colors"
          @click="resetMap"
        >
          Reset Map
        </button>
      </div>

      <!-- Metric toggle pills (cherebowl style) -->
      <div class="mt-6 flex flex-wrap gap-3">
        <button
          v-for="m in metrics"
          :key="m.key"
          class="px-5 lg:px-6 h-11 rounded-[20px] shadow-nav
                 font-roboto font-semibold text-[14px] lg:text-[15px]
                 text-white whitespace-nowrap transition-transform duration-150 hover:scale-[1.03]"
          :class="currentMetric === m.key ? 'ring-4 ring-offset-2' : 'opacity-90'"
          :style="{
            backgroundColor: m.color,
            '--tw-ring-color': m.color + '55',
          }"
          @click="setMetric(m.key)"
        >
          {{ m.label }}
        </button>
      </div>

      <!-- Map + stat cards layout -->
      <div class="mt-8 lg:mt-10 grid grid-cols-1 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] gap-6 lg:gap-8">
        <!-- Map container -->
        <div class="relative w-full h-[420px] sm:h-[500px] lg:h-[700px] bg-[#E8EEF4] rounded-[20px] overflow-hidden border border-gray-200 shadow-card">
          <!-- Loading overlay -->
          <div
            v-if="isMapLoading"
            class="absolute inset-0 z-10 bg-white/95 backdrop-blur-sm flex flex-col items-center justify-center gap-4"
          >
            <div class="relative w-14 h-14">
              <div class="absolute inset-0 border-[3px] border-sky rounded-full" />
              <div class="absolute inset-0 border-[3px] border-t-sky-active rounded-full animate-spin" />
            </div>
            <p class="font-roboto font-bold text-navy">Mapping Victoria…</p>
          </div>

          <div ref="mapEl" class="w-full h-full" />

          <!-- Map legend -->
          <div class="absolute bottom-4 left-4 bg-white p-4 rounded-[14px] shadow-card border border-gray-200">
            <h4 class="font-roboto text-xs font-bold text-navy mb-3 uppercase tracking-wider">
              {{ legendTitle }}
            </h4>
            <div class="flex flex-col gap-2 text-[13px] font-medium text-ash">
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full" :style="{ backgroundColor: legendColors[0] }" />
                Low
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full" :style="{ backgroundColor: legendColors[1] }" />
                Medium
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full" :style="{ backgroundColor: legendColors[2] }" />
                High
              </div>
            </div>
          </div>
        </div>

        <!-- Stat cards (cherebowl visual style) -->
        <div class="flex flex-col gap-5">
          <!-- Empty state -->
          <div
            v-if="!selectedLgaStat"
            class="flex flex-col items-center justify-center text-center p-8 bg-sky-tint/40 rounded-[20px] border border-dashed border-sky min-h-[200px]"
          >
            <span class="text-3xl mb-3">👆</span>
            <p class="font-roboto text-ash text-[16px] leading-relaxed">
              Select a region on the map or search above to view local statistics.
            </p>
          </div>

          <template v-else>
            <!-- Food insecurity -->
            <div class="rounded-[20px] bg-[#d9d9d94a] shadow-nav p-5 lg:p-6 text-center">
              <p class="font-roboto font-bold text-black text-[14px] lg:text-[16px] tracking-wider uppercase">
                Food Insecurity
              </p>
              <p class="mt-2 font-roboto font-extrabold text-black text-[36px] lg:text-[48px] leading-none">
                {{ displayFoodInsecurity }}%
              </p>
              <p class="mt-2 font-roboto text-ash text-[14px] lg:text-[16px]">
                in {{ selectedLgaStat.lga_name }}
              </p>
            </div>

            <!-- People affected (with men/women gauges) -->
            <div class="rounded-[20px] bg-[#d9d9d94a] shadow-nav p-5 lg:p-6">
              <p class="font-roboto font-bold text-black text-[14px] lg:text-[16px] tracking-wider uppercase text-center">
                People Affected
              </p>
              <p class="mt-2 font-roboto font-extrabold text-black text-[32px] lg:text-[40px] leading-none text-center">
                {{ displayPeopleAffected.toLocaleString() }}
              </p>

              <div class="mt-4 space-y-3" :class="['picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
                <!-- Men row -->
                <div>
                  <div class="flex justify-between font-roboto text-[12px] font-bold text-navy mb-1 px-1">
                    <span>MEN</span>
                    <span>{{ menNeedRatio }}/10</span>
                  </div>
                  <div class="flex gap-1 justify-center">
                    <svg
                      v-for="n in 10"
                      :key="'m' + n"
                      class="w-5 h-5 fill-current transition-colors"
                      :class="n <= menNeedRatio ? 'text-navy' : 'text-gray-300'"
                      viewBox="0 0 24 24"
                    >
                      <path d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                    </svg>
                  </div>
                </div>

                <!-- Women row -->
                <div>
                  <div class="flex justify-between font-roboto text-[12px] font-bold text-coral mb-1 px-1">
                    <span>WOMEN</span>
                    <span>{{ womenNeedRatio }}/10</span>
                  </div>
                  <div class="flex gap-1 justify-center">
                    <svg
                      v-for="n in 10"
                      :key="'w' + n"
                      class="w-5 h-5 fill-current transition-colors"
                      :class="n <= womenNeedRatio ? 'text-coral' : 'text-gray-300'"
                      viewBox="0 0 24 24"
                    >
                      <path d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Food banks -->
            <div class="rounded-[20px] bg-[#d9d9d94a] shadow-nav p-5 lg:p-6 text-center">
              <p class="font-roboto font-bold text-black text-[14px] lg:text-[16px] tracking-wider uppercase">
                Food Banks
              </p>
              <p class="mt-2 font-roboto font-extrabold text-black text-[36px] lg:text-[48px] leading-none">
                {{ displayFoodBanks }}
              </p>
              <p class="mt-2 font-roboto text-ash text-[14px] lg:text-[16px]">
                in {{ selectedLgaStat.lga_name }}
              </p>
            </div>
          </template>
        </div>
      </div>

      <!-- Data resources -->
      <div class="mt-10 lg:mt-12 pt-6 border-t border-gray-200 text-[11px] text-ash">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Food Insecurity:</span>
            <a href="https://vahi.vic.gov.au/reports/victorian-population-health-survey-2023" target="_blank" rel="noopener" class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              VAHI (2023 Survey)
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Emergency Services:</span>
            <a href="https://data.melbourne.vic.gov.au/explore/dataset/free-and-cheap-support-services-with-opening-hours-public-transport-and-parking-/table/" target="_blank" rel="noopener" class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              data.melbourne.vic.gov.au
            </a>
            <span class="opacity-30">&amp;</span>
            <a href="https://data.gov.au/data/dataset/emergency-relief-provider-outlets/resource/0e32d958-3796-4dca-8312-489ef7a610f6" target="_blank" rel="noopener" class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              data.gov.au
            </a>
          </span>
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Population by LGA:</span>
            <a href="https://digital.atlas.gov.au/datasets/digitalatlas::abs-population-and-people-data-by-region-lga-november-2025/about" target="_blank" rel="noopener" class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
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

const config = useRuntimeConfig()
const API_URL = config.public.apiBase || 'http://127.0.0.1:8000'

// ── Refs / state ──────────────────────────────────────────────────────────
const mapEl = ref(null)
let mapInstance = null
let lgaGeojson = null
let hoveredLgaId = null
let tooltipPopup = null

const lgaStats = ref([])
const selectedLgaName = ref(null)
const currentMetric = ref('foodInsecurity')

const searchQuery = ref('')
const filteredLgas = ref([])
const showDropdown = ref(false)
const searchIndex = ref([])
const isLoadingLocation = ref(false)
const isMapLoading = ref(true)

// ── Metric definitions (cherebowl palette) ────────────────────────────────
const metrics = [
  { key: 'foodInsecurity', label: '🔴 Food Insecurity', color: '#df6951' },  // coral
  { key: 'foodBanks',       label: '🟢 Food Banks',       color: '#0d400d' },
  { key: 'peopleAffected',  label: '🔵 People Affected',  color: '#6b88ff' },
]

function setMetric(key) {
  if (currentMetric.value === key) return
  currentMetric.value = key
}

// ── Search handlers ───────────────────────────────────────────────────────
function filterLgas() {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) { filteredLgas.value = []; showDropdown.value = false; return }
  filteredLgas.value = searchIndex.value.filter(l => l.toLowerCase().includes(q)).slice(0, 12)
  showDropdown.value = filteredLgas.value.length > 0
}
function selectLgaFromSearch(lga) {
  searchQuery.value = lga
  showDropdown.value = false
  selectLga(lga)
}
function onSearchBlur() {
  // Delay so click-on-dropdown registers before close
  setTimeout(() => { showDropdown.value = false }, 150)
}

// ── Map selection ─────────────────────────────────────────────────────────
function getFeatureBounds(feature) {
  const bounds = new mapboxgl.LngLatBounds()
  const coords = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates
  coords.forEach(polygon => polygon.forEach(ring => ring.forEach(c => bounds.extend(c))))
  return bounds
}
function selectLga(lgaName) {
  if (selectedLgaName.value === lgaName) { resetMap(); return }
  selectedLgaName.value = lgaName
  if (mapInstance && mapInstance.isStyleLoaded() && lgaGeojson) {
    const feature = lgaGeojson.features.find(f => f.properties.lga_name === lgaName)
    if (feature) {
      mapInstance.fitBounds(getFeatureBounds(feature), {
        padding: 60, maxZoom: 10, duration: 1000, essential: true,
      })
    }
    mapInstance.setPaintProperty('lga-fills', 'fill-opacity', [
      'case',
      ['==', ['get', 'lga_name'], lgaName], 1.0,
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

// ── Geolocation ───────────────────────────────────────────────────────────
function useMyLocation() {
  if (!navigator.geolocation) { alert('Geolocation not supported.'); return }
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

// ── Stats / count-up ──────────────────────────────────────────────────────
const statsMap = computed(() => {
  const m = {}
  lgaStats.value.forEach(s => { m[s.lga_name] = s })
  return m
})
const selectedLgaStat = computed(() => {
  if (!selectedLgaName.value) return null
  return statsMap.value[selectedLgaName.value] || null
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
const foodBanksStat = computed(() => selectedLgaStat.value?.emergency_services_count ?? 0)

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

// Pictogram fade on LGA change
const pictogramVisible = ref(true)
watch(selectedLgaName, () => {
  pictogramVisible.value = false
  setTimeout(() => { pictogramVisible.value = true }, 280)
})

// ── Legend / colour ramp ──────────────────────────────────────────────────
const legendTitle = computed(() => {
  if (currentMetric.value === 'foodInsecurity') return 'Food Insecurity'
  if (currentMetric.value === 'foodBanks') return 'Food Banks'
  return 'People Affected'
})
const legendColors = computed(() => {
  if (currentMetric.value === 'foodInsecurity') return ['#FED7AA', '#F97316', '#C2410C']
  if (currentMetric.value === 'foodBanks')      return ['#BBF7D0', '#22C55E', '#15803D']
  return                                                 ['#BAE6FD', '#0EA5E9', '#0369A1']
})
function getFillColorExpression() {
  if (!lgaStats.value.length) return '#cccccc'
  const expr = ['match', ['get', 'lga_name']]
  lgaStats.value.forEach(stat => {
    let color = '#cccccc'
    if (currentMetric.value === 'foodInsecurity') {
      const v = (stat.men_pct + stat.women_pct) / 2
      color = v < 5 ? legendColors.value[0] : v < 10 ? legendColors.value[1] : legendColors.value[2]
    } else if (currentMetric.value === 'foodBanks') {
      const v = stat.emergency_services_count
      color = v <= 2 ? legendColors.value[0] : v <= 5 ? legendColors.value[1] : legendColors.value[2]
    } else {
      const v = (stat.pop_2024_total * (stat.men_pct + stat.women_pct) / 200)
      color = v < 5000 ? legendColors.value[0] : v < 15000 ? legendColors.value[1] : legendColors.value[2]
    }
    expr.push(stat.lga_name, color)
  })
  expr.push('#cccccc')
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

// ── Init ──────────────────────────────────────────────────────────────────
onMounted(async () => {
  // Fetch stats
  try {
    const res = await fetch(`${API_URL}/lga/stats`)
    lgaStats.value = await res.json()
    searchIndex.value = [...new Set(lgaStats.value.map(s => s.lga_name))].sort()
  } catch (e) {
    console.error('Failed to fetch LGA stats', e)
  }

  const token = config.public.mapboxToken
  if (!token) {
    console.warn('NUXT_PUBLIC_MAPBOX_TOKEN is not set; map will not load.')
    isMapLoading.value = false
    return
  }
  mapboxgl.accessToken = token

  await nextTick()
  mapInstance = new mapboxgl.Map({
    container: mapEl.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: [144.5, -36.5],
    zoom: 5.5,
    scrollZoom: false,
  })
  mapInstance.addControl(new mapboxgl.NavigationControl(), 'top-right')
  tooltipPopup = new mapboxgl.Popup({ closeButton: false, closeOnClick: false, className: 'lga-tooltip-popup' })

  mapInstance.on('load', async () => {
    try {
      const r = await fetch(`${API_URL}/lga/boundaries`)
      lgaGeojson = await r.json()
      lgaGeojson.features.forEach((f, i) => f.id = i)

      mapInstance.addSource('lga', { type: 'geojson', data: lgaGeojson })
      mapInstance.addLayer({
        id: 'lga-fills', type: 'fill', source: 'lga',
        paint: {
          'fill-color': ['case', ['boolean', ['feature-state', 'hover'], false], '#FFFFFF', getFillColorExpression()],
          'fill-opacity': ['case', ['boolean', ['feature-state', 'hover'], false], 1, 0.75],
        },
      })
      mapInstance.addLayer({
        id: 'lga-borders', type: 'line', source: 'lga',
        paint: { 'line-color': '#888', 'line-width': 0.6 },
      })

      mapInstance.on('mousemove', 'lga-fills', (e) => {
        if (!e.features.length) return
        if (hoveredLgaId !== null) mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: false })
        hoveredLgaId = e.features[0].id
        mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: true })
        mapInstance.getCanvas().style.cursor = 'pointer'
        const lgaName = e.features[0].properties.lga_name
        tooltipPopup.setLngLat(e.lngLat)
          .setHTML(`<div style="color:#181e4b;font-weight:bold;">${lgaName}</div>`)
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
  font-family: 'Roboto', sans-serif;
}
:deep(.mapboxgl-popup-tip) { display: none; }

.picto-fade { transition: opacity 0.25s ease; }
.picto-out  { opacity: 0; }
.picto-in   { opacity: 1; }
</style>
