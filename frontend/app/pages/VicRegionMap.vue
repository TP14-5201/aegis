<template>
  <div class="w-full min-h-screen flex flex-col font-sans bg-[#F7F9FB]">
    <LayoutNavbar />

    <!-- Hero Section -->
    <section class="w-full bg-bg-blue pt-12 pb-24 border-b border-border-grey overflow-hidden relative">

      <div class="relative w-full h-[380px] mb-8">

        <svg class="absolute top-[-80px] left-0 w-full h-[220px] pointer-events-none" preserveAspectRatio="none"
          viewBox="0 0 1200 120">
          <path d="M -50 10 Q 600 130 1250 10" stroke="#D2B48C" stroke-width="4" fill="none" stroke-dasharray="2,1"
            class="rope-shadow" />
        </svg>

        <div class="relative flex items-center justify-center gap-2 sm:gap-6 w-full px-4 mt-16 z-10">
          <div v-for="(img, index) in polaroids" :key="index" class="polaroid-card"
            :style="precomputedPolaroidStyles[index]">
            <div class="clip">
              <div class="clip-inner"></div>
            </div>

            <div class="bg-gray-100 overflow-hidden mb-2 border border-[#E8EEF4]">
              <img :src="img" loading="lazy" decoding="async" class="w-full h-[100px] sm:h-[130px] object-cover"
                alt="Community Story" />
            </div>
          </div>
        </div>
      </div>

      <div class="max-w-[1200px] mx-auto px-6 text-center relative z-20">
        <h1 class="font-serif font-bold text-primary mb-8"
          style="font-size: 75.8px; line-height: 1.1; letter-spacing: -3.03px;">
          The story the <span class="data-highlight">data</span>
          tells
        </h1>
        <p class="font-sans text-[#6F7979] italic text-[24px] max-w-3xl mx-auto leading-[35px] mb-12">
          Behind every statistic is a Victorian family. Explore the reality of food insecurity,
          malnutrition, and the cost of eating well across our state.
        </p>

        <div class="flex flex-wrap justify-center gap-6">
          <div class="flex flex-wrap justify-center gap-6 mt-10">

            <div @click="scrollToSection('map-section')"
              class="group relative bg-white border border-border-grey rounded-20 p-8 w-[320px] h-[360px] cursor-pointer overflow-hidden transition-all duration-300 shadow-card-white hover:-translate-y-2">

              <div
                class="absolute inset-0 translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-out z-0 will-change-transform">
                <div class="absolute inset-0 bg-cover bg-center"
                  style="background-image: url('/visualisation/regional_map.webp');"></div>
                <div class="absolute inset-0 bg-primary/60"></div>
              </div>

              <div class="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <div
                  class="w-20 h-20 bg-bg-input group-hover:bg-white/20 rounded-full flex items-center justify-center mb-6 transition-all duration-300">
                  <span class="text-4xl group-hover:scale-110 transition-transform duration-300">🗺️</span>
                </div>

                <h3
                  class="font-serif font-bold text-primary text-2xl group-hover:text-white transition-colors duration-300">
                  Regional Map
                </h3>

                <p
                  class="font-sans text-base text-body-grey mt-3 group-hover:text-white/90 transition-colors duration-300 leading-relaxed px-2">
                  Explore food insecurity statistics by LGA
                </p>
              </div>
            </div>

            <div @click="scrollToSection('child-section')"
              class="group relative bg-white border border-border-grey rounded-20 p-8 w-[320px] h-[360px] cursor-pointer overflow-hidden transition-all duration-300 shadow-card-white hover:-translate-y-2">

              <div
                class="absolute inset-0 translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-out z-0 will-change-transform">
                <div class="absolute inset-0 bg-cover bg-center"
                  style="background-image: url('/visualisation/child_nutrition.webp');"></div>
                <div class="absolute inset-0 bg-coral-orange/60"></div>
              </div>

              <div class="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <div
                  class="w-20 h-20 bg-bg-input group-hover:bg-white/20 rounded-full flex items-center justify-center mb-6 transition-all duration-300">
                  <span class="text-4xl group-hover:scale-110 transition-transform duration-300">👶</span>
                </div>

                <h3
                  class="font-serif font-bold text-primary text-2xl group-hover:text-white transition-colors duration-300">
                  Child Health
                </h3>

                <p
                  class="font-sans text-base text-body-grey mt-3 group-hover:text-white/90 transition-colors duration-300 leading-relaxed px-2">
                  The impact of malnutrition on young Victorians
                </p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- 1st Section: Map -->
    <section class="relative w-full bg-[#FFFFFF] overflow-hidden" style="padding-top: 100px; padding-bottom: 80px;">
      <div class="max-w-[1200px] mx-auto px-6">
        <div id="map-section" class="mb-12">
          <span class="text-[#DF6651] font-bold text-sm tracking-wider uppercase mb-3 block">Around Us</span>
          <h2 class="font-serif font-bold text-primary mb-6" style="font-size: 54px; line-height: 1.1;">
            It's happening right here
          </h2>
          <p class="font-sans text-[#6F7979] text-[18px] max-w-2xl mb-10 leading-relaxed">
            Every region in Victoria tells a different story. Click yours to see the full picture — food insecurity
            rates, people affected, and the food banks trying to help.
          </p>

          <!-- Search Bar & Location -->
          <div class="flex flex-col sm:flex-row gap-5 mb-10">
            <div class="relative flex-[2]">
              <input type="text" v-model="searchQuery" @input="filterLgas" placeholder="Enter your LGA (e.g. Melbourne)"
                class="w-full h-[53px] bg-white border border-border-grey text-primary placeholder-[#5F7979] rounded-14 px-6 focus:outline-none focus:border-bright-blue shadow-sm" />
              <ul v-if="showDropdown && filteredLgas.length"
                class="absolute z-[9999] w-full bg-white border border-border-grey rounded-14 mt-2 max-h-60 overflow-y-auto shadow-card-white">
                <li v-for="lga in filteredLgas" :key="lga" @click="selectLgaFromSearch(lga)"
                  class="px-6 py-3 text-primary hover:bg-bg-input cursor-pointer font-sans">
                  {{ lga }}
                </li>
              </ul>
            </div>
            <button @click="useMyLocation"
              class="flex-1 h-[53px] flex items-center justify-center gap-2 bg-white hover:bg-bg-input text-primary border border-border-grey px-6 rounded-14 font-semibold transition-colors shadow-sm">
              <span v-if="isLoadingLocation"
                class="animate-spin h-4 w-4 border-2 border-primary border-t-transparent rounded-full inline-block"></span>
              <span v-else>📍</span> Use My Location
            </button>
            <button @click="resetMap" v-if="selectedLgaName"
              class="h-[53px] flex items-center justify-center gap-2 bg-primary hover:bg-primary/90 text-black px-8 rounded-14 font-semibold transition-colors shadow-sm">
              Reset Map
            </button>
          </div>

          <!-- Toggle Buttons -->
          <div class="flex flex-wrap gap-4 mb-10">
            <button @click="setMetric('foodInsecurity')"
              :class="['px-8 h-[50px] rounded-full font-bold transition-all shadow-sm', currentMetric === 'foodInsecurity' ? 'bg-[#F97316] text-white ring-4 ring-[#F97316]/25' : 'bg-white text-primary border border-border-grey hover:bg-[#FED7AA]/30']">
              🔴 Food Insecurity
            </button>
            <button @click="setMetric('foodBanks')"
              :class="['px-8 h-[50px] rounded-full font-bold transition-all shadow-sm', currentMetric === 'foodBanks' ? 'bg-[#22C55E] text-white ring-4 ring-[#22C55E]/25' : 'bg-white text-primary border border-border-grey hover:bg-[#BBF7D0]/30']">
              🟢 Food Banks
            </button>
            <button @click="setMetric('peopleAffected')"
              :class="['px-8 h-[50px] rounded-full font-bold transition-all shadow-sm', currentMetric === 'peopleAffected' ? 'bg-[#0EA5E9] text-white ring-4 ring-[#0EA5E9]/25' : 'bg-white text-primary border border-border-grey hover:bg-[#BAE6FD]/30']">
              🔵 People Affected
            </button>
          </div>
        </div>

        <div class="flex flex-col lg:flex-row gap-8 items-stretch lg:h-[600px]">
          <!-- Map Container -->
          <div
            :class="['lg:flex-[2] h-[420px] lg:h-auto w-full bg-white rounded-[16px] overflow-hidden relative shadow-lg border border-[#D8DADC]', mapShifting ? 'map-shifting' : '']">
            <div ref="mapEl" class="w-full h-full bg-[#E8EEF4]" />

            <!-- Map Legend -->
            <div class="absolute bottom-6 left-6 bg-white p-5 rounded-14 shadow-card-white border border-border-grey">
              <h4 class="font-sans text-xs font-bold text-primary mb-4 uppercase tracking-wider">{{ legendTitle }}</h4>
              <div class="flex flex-col gap-3 text-sm font-medium text-body-grey">
                <div class="flex items-center gap-3">
                  <span class="w-4 h-4 rounded-full shadow-inner" :style="{ backgroundColor: legendColors[0] }"></span>
                  Low
                </div>
                <div class="flex items-center gap-3">
                  <span class="w-4 h-4 rounded-full shadow-inner" :style="{ backgroundColor: legendColors[1] }"></span>
                  Medium
                </div>
                <div class="flex items-center gap-3">
                  <span class="w-4 h-4 rounded-full shadow-inner" :style="{ backgroundColor: legendColors[2] }"></span>
                  High
                </div>
              </div>
            </div>
          </div>

          <!-- Details Panel -->
          <div class="lg:flex-1 w-full flex flex-col gap-6">
            <div v-if="!selectedLgaStat"
              class="h-full flex flex-col items-center justify-center bg-white rounded-20 border border-dashed border-border-grey shadow-sm p-8 text-center">
              <span class="text-4xl mb-4 opacity-50">👆</span>
              <p class="font-sans text-body-grey text-[18px] font-medium leading-relaxed">Select a region on the map or
                use the search box to view local statistics.</p>
            </div>
            <template v-else>
              <!-- Food Insecurity Card -->
              <div
                class="bg-white rounded-20 p-6 text-center border-t-4 border-[#F97316] shadow-card-white flex flex-col items-center justify-center flex-1 transition-transform hover:scale-[1.02]">
                <h3 class="font-sans text-[14px] font-bold text-[#F97316] uppercase tracking-wide mb-2">Food Insecurity
                </h3>
                <div class="font-serif text-[42px] font-bold text-[#C2410C] leading-none mb-2">{{ displayFoodInsecurity
                  }}%</div>
                <div class="font-sans text-[14px] text-body-grey">in {{ selectedLgaStat.lga_name }}</div>
              </div>

              <!-- People Affected Card -->
              <div
                class="bg-white rounded-20 p-6 text-center border-t-4 border-[#0EA5E9] shadow-card-white flex flex-col items-center justify-center flex-[1.5] transition-transform hover:scale-[1.02]">
                <h3 class="font-sans text-[14px] font-bold text-[#0EA5E9] uppercase tracking-wide mb-2">People Affected
                </h3>
                <div class="font-serif text-[36px] font-bold text-[#0369A1] leading-none mb-4">{{
                  displayPeopleAffected.toLocaleString() }}</div>

                <div class="w-full flex justify-between items-center mb-2 px-4">
                  <span class="font-sans text-xs font-bold text-blue-600">MEN</span>
                  <span class="font-sans text-xs font-bold text-blue-600">{{ menNeedRatio }}/10</span>
                </div>
                <div
                  :class="['flex justify-center gap-1 mb-4 px-2 picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
                  <svg v-for="n in 10" :key="'m' + n" :class="n <= menNeedRatio ? 'text-blue-600' : 'text-border-grey'"
                    class="w-6 h-6 fill-current transition-colors duration-300" viewBox="0 0 24 24">
                    <path
                      d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                  </svg>
                </div>

                <div class="w-full flex justify-between items-center mb-2 px-4">
                  <span class="font-sans text-xs font-bold text-[#EC4899]">WOMEN</span>
                  <span class="font-sans text-xs font-bold text-[#EC4899]">{{ womenNeedRatio }}/10</span>
                </div>
                <div
                  :class="['flex justify-center gap-1 px-2 picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
                  <svg v-for="n in 10" :key="'w' + n"
                    :class="n <= womenNeedRatio ? 'text-[#EC4899]' : 'text-border-grey'"
                    class="w-6 h-6 fill-current transition-colors duration-300" viewBox="0 0 24 24">
                    <path
                      d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                  </svg>
                </div>
              </div>

              <!-- Food Banks Card -->
              <div
                class="bg-white rounded-20 p-6 text-center border-t-4 border-[#22C55E] shadow-card-white flex flex-col items-center justify-center flex-1 transition-transform hover:scale-[1.02]">
                <h3 class="font-sans text-[14px] font-bold text-[#22C55E] uppercase tracking-wide mb-2">Food Banks</h3>
                <div class="font-serif text-[42px] font-bold text-[#15803D] leading-none mb-2">{{ displayFoodBanks }}
                </div>
                <div class="font-sans text-[14px] text-body-grey">in {{ selectedLgaStat.lga_name }}</div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- 2nd Section: The Children -->
    <section id="child-section" class="py-[100px] bg-white border-t border-border-grey">
      <div class="max-w-[1200px] mx-auto px-6">
        <span class="text-[#DF6651] font-bold text-sm tracking-wider uppercase mb-3 block">The Children</span>
        <h2 class="font-serif font-bold text-primary mb-8" style="font-size: 54px; line-height: 1.1;">
          No child should grow up hungry
        </h2>
        <p class="font-sans text-[#6F7979] text-[18px] max-w-2xl mb-14 leading-relaxed">
          Malnutrition affects Victorian children differently across age groups. Select an age group to see how many are
          going without the nutrition they need.
        </p>

        <!-- Placeholder for Visualisation -->
        <div class="w-full flex flex-col items-center">
          <div class="w-full max-w-4xl overflow-x-auto mb-12">
            <div class="flex justify-between items-end h-64 border-b-2 border-[#D8DADC] pb-4 px-4 min-w-[320px]">
              <div class="flex flex-col items-center group cursor-pointer">
                <div
                  class="w-12 h-16 bg-[#B3D9FF] rounded-t-full group-hover:bg-[#7392FF] transition-colors mb-4 flex items-center justify-center">
                  <span class="text-[#1A234E] text-xs font-bold">👶</span>
                </div>
                <span class="text-[#FF6B6B] font-medium text-sm text-center">Infants<br><span
                    class="text-[#1A234E] text-xs font-bold">(0-1)</span></span>
              </div>
              <div class="flex flex-col items-center group cursor-pointer">
                <div
                  class="w-16 h-24 bg-[#B3D9FF] rounded-t-full group-hover:bg-[#7392FF] transition-colors mb-4 flex items-center justify-center">
                  <span class="text-[#1A234E] text-xs font-bold">🧒</span>
                </div>
                <span class="text-[#FF6B6B] font-medium text-sm text-center">Toddlers<br><span
                    class="text-[#1A234E] text-xs font-bold">(1-3)</span></span>
              </div>
              <div class="flex flex-col items-center group cursor-pointer">
                <div
                  class="w-20 h-32 bg-[#B3D9FF] rounded-t-full group-hover:bg-[#7392FF] transition-colors mb-4 flex items-center justify-center">
                  <span class="text-[#1A234E] text-xs font-bold">👧</span>
                </div>
                <span class="text-[#FF6B6B] font-medium text-sm text-center">Pre-School<br><span
                    class="text-[#1A234E] text-xs font-bold">(3-5)</span></span>
              </div>
              <div class="flex flex-col items-center group cursor-pointer">
                <div
                  class="w-24 h-40 bg-[#B3D9FF] rounded-t-full group-hover:bg-[#7392FF] transition-colors mb-4 flex items-center justify-center">
                  <span class="text-[#1A234E] text-xs font-bold">🎒</span>
                </div>
                <span class="text-[#FF6B6B] font-medium text-sm text-center">School age<br><span
                    class="text-[#1A234E] text-xs font-bold">(5-12)</span></span>
              </div>
              <div class="flex flex-col items-center group cursor-pointer">
                <div
                  class="w-28 h-52 bg-[#B3D9FF] rounded-t-full group-hover:bg-[#7392FF] transition-colors mb-4 flex items-center justify-center">
                  <span class="text-[#1A234E] text-xs font-bold">🧑</span>
                </div>
                <span class="text-[#FF6B6B] font-medium text-sm text-center">Adolescent<br><span
                    class="text-[#1A234E] text-xs font-bold">(13-17)</span></span>
              </div>
            </div>
          </div>
          <div
            class="bg-bg-input rounded-20 w-full max-w-4xl flex flex-col sm:flex-row items-stretch border border-border-grey shadow-sm overflow-hidden">
            <div class="bg-light-blue p-8 sm:w-1/3 flex flex-col justify-center items-center">
              <span class="font-serif text-[64px] font-bold text-primary leading-none mb-2">12%</span>
              <span class="font-sans text-primary font-bold text-[20px]">Malnourished</span>
            </div>
            <div class="p-8 sm:w-2/3 flex items-center bg-white">
              <p class="font-sans text-body-grey text-[18px] leading-[32px]">
                Infants in Victoria aren't getting adequate nutrition — putting their brain development and immune
                system at serious risk.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3rd Section: Ready to take the next step? -->
    <section class="py-[80px] bg-[#DBEDFF]" style="content-visibility: auto; contain-intrinsic-size: 0 500px;">
      <div class="max-w-[1200px] mx-auto px-6">
        <h2 class="font-serif font-bold text-[#1A234E] mb-2" style="font-size: 32px;">
          Ready to take the next step?
        </h2>
        <span class="text-[#FF6B6B] font-medium text-[16px] block mb-12">Here is where to start</span>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Card 1: Light Blue — Find Food Banks -->
          <div
            class="bg-[#FFFFFF] rounded-20 p-8 shadow-card-white border border-[#FFFFFF] flex flex-col h-full hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <h3 class="font-serif font-bold text-primary text-[28px] leading-tight mb-4">Find Food Banks near me</h3>
            <p class="font-sans text-black text-[16px] flex-grow mb-10 leading-relaxed">Find free food support open
              right now</p>
            <NuxtLink to="/services">
              <button
                class="bg-[#1B1E45] text-white h-[70px] px-8 rounded-20 font-bold hover:bg-[#1B1E45]/85 transition-all w-full text-sm shadow-md">
                Find Nearby Food Banks
              </button>
            </NuxtLink>
          </div>

          <!-- Card 2: Navy — Groceries -->
          <div
            class="bg-[#FFFFFF] rounded-20 p-8 shadow-card-white border border-[#FFFFFF] flex flex-col h-full hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <h3 class="font-serif font-bold text-black text-[28px] leading-tight mb-4">Find groceries at best prices
            </h3>
            <p class="font-sans text-black text-[16px] flex-grow mb-10 leading-relaxed">Tell us your needs and we'll
              find you the right groceries</p>
            <button
              class="bg-[#1B1E45] text-white h-[70px] px-8 rounded-20 font-bold hover:bg-[#1B1E45]/85 transition-all w-full text-sm shadow-md">
              Explore Groceries
            </button>
          </div>

          <!-- Card 3: Coral — Nutrition -->
          <div
            class="bg-[#FFFFFF] rounded-20 p-8 shadow-card-white border border-[#FFFFFF] flex flex-col h-full hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
            <h3 class="font-serif font-bold text-black text-[28px] leading-tight mb-4">Know more about nutrition</h3>
            <p class="font-sans text-black text-[16px] flex-grow mb-10 leading-relaxed">Simple guides for your
              family's health</p>
            <button
              class="bg-[#1B1E45] text-white h-[70px] px-8 rounded-20 font-bold hover:bg-[#1B1E45]/85 transition-all w-full text-sm shadow-md">
              Learn about Nutrition
            </button>
          </div>
        </div>
      </div>
    </section>

    <LayoutFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { point } from '@turf/helpers'
import booleanPointInPolygon from '@turf/boolean-point-in-polygon'
import { useRuntimeConfig } from '#imports'

const config = useRuntimeConfig()
const API_URL = config.public.apiBase || 'http://127.0.0.1:8000'

const mapEl = ref(null)
let mapInstance = null
let lgaGeojson = null
let hoveredLgaId = null
let tooltipPopup = null

const lgaStats = ref([])
const selectedLgaName = ref(null)
const currentMetric = ref('foodInsecurity')

// Search & Location
const searchQuery = ref('')
const filteredLgas = ref([])
const showDropdown = ref(false)
const searchIndex = ref([])
const isLoadingLocation = ref(false)

const mapShifting = ref(false)

const setMetric = (metric) => {
  if (currentMetric.value === metric) return
  mapShifting.value = true
  currentMetric.value = metric
  setTimeout(() => { mapShifting.value = false }, 600)
}

function filterLgas() {
  if (!searchQuery.value) {
    filteredLgas.value = []
    showDropdown.value = false
    return
  }
  const query = searchQuery.value.toLowerCase()
  filteredLgas.value = searchIndex.value.filter(lga => lga.toLowerCase().includes(query))
  showDropdown.value = true
}

function selectLgaFromSearch(lgaName) {
  searchQuery.value = lgaName
  showDropdown.value = false
  selectLga(lgaName)
}

function getFeatureBounds(feature) {
  const bounds = new mapboxgl.LngLatBounds()
  const coords = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates
  coords.forEach(polygon => {
    polygon.forEach(ring => {
      ring.forEach(coord => {
        bounds.extend(coord)
      })
    })
  })
  return bounds
}

function selectLga(lgaName) {
  if (selectedLgaName.value === lgaName) {
    resetMap()
    return
  }

  selectedLgaName.value = lgaName

  if (mapInstance && mapInstance.isStyleLoaded() && lgaGeojson) {
    const feature = lgaGeojson.features.find(f => f.properties.lga_name === lgaName)
    if (feature) {
      const bounds = getFeatureBounds(feature)
      mapInstance.fitBounds(bounds, {
        padding: 60,
        maxZoom: 10,
        duration: 1200,
        essential: true,
        easing: (t) => t * (2 - t)
      })
    }

    // Dim others by updating paint property
    mapInstance.setPaintProperty('lga-fills', 'fill-opacity', [
      'case',
      ['==', ['get', 'lga_name'], lgaName], 1.0,
      ['boolean', ['feature-state', 'hover'], false], 1.0,
      0.3
    ])
  }
}

function resetMap() {
  selectedLgaName.value = null
  searchQuery.value = ''
  if (mapInstance && mapInstance.isStyleLoaded()) {
    mapInstance.flyTo({
      center: [144.5, -36.5],
      zoom: 5.5,
      duration: 1200,
      essential: true
    })

    // Reset opacity and colors
    mapInstance.setPaintProperty('lga-fills', 'fill-opacity', [
      'case',
      ['boolean', ['feature-state', 'hover'], false], 1,
      0.75
    ])

    mapInstance.setPaintProperty('lga-fills', 'fill-color', [
      'case',
      ['boolean', ['feature-state', 'hover'], false],
      '#FFFFFF',
      getFillColorExpression()
    ])
  }
}

function useMyLocation() {
  isLoadingLocation.value = true
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
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
    }, () => {
      alert('Unable to retrieve your location.')
      isLoadingLocation.value = false
    })
  } else {
    isLoadingLocation.value = false
  }
}

const scrollToSection = (id) => {
  const el = document.getElementById(id);
  if (!el) return;
  const NAVBAR_OFFSET = 150; // matches scroll-margin-top in CSS
  const top = el.getBoundingClientRect().top + window.scrollY - NAVBAR_OFFSET;
  window.scrollTo({ top, behavior: 'smooth' });
};

// Hero section
const polaroids = [
  '/visualisation/family1.webp',
  '/visualisation/child2.webp',
  '/visualisation/kitchen3.webp',
  '/visualisation/community4.webp',
  '/visualisation/farmer5.webp',
  '/visualisation/meal6.webp'
]

// Pre-compute polaroid styles once at module level — no reactive deps, no per-render recalculation
const precomputedPolaroidStyles = (() => {
  const total = polaroids.length
  return polaroids.map((_, index) => {
    const x = (index - (total - 1) / 2) / ((total - 1) / 2)
    const verticalOffset = Math.pow(x, 2) * -60 + 70
    const rotation = x * 8 + (index % 2 === 0 ? 2 : -2)
    return {
      transform: `translateY(${verticalOffset}px) rotate(${rotation}deg)`,
      zIndex: 10 + index
    }
  })
})()

// Stats mapping
const statsMap = computed(() => {
  const map = {}
  lgaStats.value.forEach(s => {
    map[s.lga_name] = s
  })
  return map
})

const selectedLgaStat = computed(() => {
  if (!selectedLgaName.value || !statsMap.value[selectedLgaName.value]) return null
  return statsMap.value[selectedLgaName.value]
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

// ── Count-up animation ──────────────────────────────────────────────────────
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
      const eased = 1 - Math.pow(1 - progress, 3) // ease-out cubic
      display.value = Math.round(startVal + (endVal - startVal) * eased)
      if (progress < 1) rafId = requestAnimationFrame(step)
    }
    rafId = requestAnimationFrame(step)
  })
  return display
}

const foodBanksStat = computed(() => selectedLgaStat.value?.emergency_services_count ?? 0)
const displayFoodInsecurity = useCountUp(foodInsecurityStat)
const displayPeopleAffected = useCountUp(peopleAffectedStat)
const displayFoodBanks = useCountUp(foodBanksStat)

// Pictogram fade-out → fade-in on LGA change
const pictogramVisible = ref(true)
watch(selectedLgaName, () => {
  pictogramVisible.value = false
  setTimeout(() => { pictogramVisible.value = true }, 280)
})

// Legend Info
const legendTitle = computed(() => {
  if (currentMetric.value === 'foodInsecurity') return 'Food Insecurity'
  if (currentMetric.value === 'foodBanks') return 'Food Banks'
  return 'People Affected'
})

const legendColors = computed(() => {
  if (currentMetric.value === 'foodInsecurity') return ['#FED7AA', '#F97316', '#C2410C'] // Shades of Orange
  if (currentMetric.value === 'foodBanks') return ['#BBF7D0', '#22C55E', '#15803D']      // Shades of Green
  return ['#BAE6FD', '#0EA5E9', '#0369A1']                                              // Shades of Blue
})

const getFillColorExpression = () => {
  if (!lgaStats.value.length) return '#333333'

  const expr = ['match', ['get', 'lga_name']]

  lgaStats.value.forEach(stat => {
    let color = '#333333'
    if (currentMetric.value === 'foodInsecurity') {
      const val = (stat.men_pct + stat.women_pct) / 2
      color = val < 5 ? legendColors.value[0] : val < 10 ? legendColors.value[1] : legendColors.value[2]
    } else if (currentMetric.value === 'foodBanks') {
      const val = stat.emergency_services_count
      color = val <= 2 ? legendColors.value[0] : val <= 5 ? legendColors.value[1] : legendColors.value[2]
    } else if (currentMetric.value === 'peopleAffected') {
      const val = (stat.pop_2024_total * (stat.men_pct + stat.women_pct) / 200)
      color = val < 5000 ? legendColors.value[0] : val < 15000 ? legendColors.value[1] : legendColors.value[2]
    }
    expr.push(stat.lga_name, color)
  })

  expr.push('#CCCCCC') // default color
  return expr
}

watch(currentMetric, () => {
  if (mapInstance && mapInstance.isStyleLoaded() && mapInstance.getSource('lga')) {
    mapInstance.setPaintProperty('lga-fills', 'fill-color', [
      'case',
      ['boolean', ['feature-state', 'hover'], false],
      '#FFFFFF',
      getFillColorExpression()
    ])
  }
})

onMounted(async () => {
  // Fetch Data
  try {
    const statsRes = await fetch(`${API_URL}/lga/stats`)
    lgaStats.value = await statsRes.json()
    searchIndex.value = [...new Set(lgaStats.value.map(d => d.lga_name))].sort()
  } catch (err) {
    console.error("Failed to fetch LGA stats", err)
  }

  const token = config.public.mapboxToken || 'pk.eyJ1IjoiYWVnaXMiLCJhIjoiY20waThnZjA2MDNtMTJzcHk2bW5mZGR1cSJ9.abc'
  mapboxgl.accessToken = token

  mapInstance = new mapboxgl.Map({
    container: mapEl.value,
    style: 'mapbox://styles/mapbox/light-v11',
    center: [144.5, -36.5],
    zoom: 5.5,
    scrollZoom: false,
    pitch: 0
  })

  mapInstance.addControl(new mapboxgl.NavigationControl(), 'top-right')

  tooltipPopup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false,
    className: 'lga-tooltip-popup'
  })

  mapInstance.on('load', async () => {
    try {
      const geoResponse = await fetch(`${API_URL}/lga/boundaries`)
      lgaGeojson = await geoResponse.json()

      lgaGeojson.features.forEach((f, i) => f.id = i)

      mapInstance.addSource('lga', {
        type: 'geojson',
        data: lgaGeojson
      })

      // Flat 2D fill layer — fill-opacity supports feature-state expressions unlike fill-extrusion-opacity
      mapInstance.addLayer({
        id: 'lga-fills',
        type: 'fill',
        source: 'lga',
        paint: {
          'fill-color': [
            'case',
            ['boolean', ['feature-state', 'hover'], false],
            '#FFFFFF',
            getFillColorExpression()
          ],
          'fill-opacity': [
            'case',
            ['boolean', ['feature-state', 'hover'], false], 1,
            0.75
          ]
        }
      })

      // LGA boundary lines
      mapInstance.addLayer({
        id: 'lga-borders',
        type: 'line',
        source: 'lga',
        paint: {
          'line-color': '#888888',
          'line-width': 0.6
        }
      })

      // Hover effect
      mapInstance.on('mousemove', 'lga-fills', (e) => {
        if (e.features.length > 0) {
          if (hoveredLgaId !== null) {
            mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: false })
          }
          hoveredLgaId = e.features[0].id
          mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: true })
          mapInstance.getCanvas().style.cursor = 'pointer'

          const lgaName = e.features[0].properties.lga_name
          tooltipPopup.setLngLat(e.lngLat)
            .setHTML(`<div style="color: #1A234E; font-weight: bold;">${lgaName}</div>`)
            .addTo(mapInstance)
        }
      })

      mapInstance.on('mouseleave', 'lga-fills', () => {
        if (hoveredLgaId !== null) {
          mapInstance.setFeatureState({ source: 'lga', id: hoveredLgaId }, { hover: false })
        }
        hoveredLgaId = null
        mapInstance.getCanvas().style.cursor = ''
        tooltipPopup.remove()
      })

      // Click event
      mapInstance.on('click', 'lga-fills', (e) => {
        if (e.features.length > 0) {
          const lgaName = e.features[0].properties.lga_name
          searchQuery.value = lgaName
          selectLga(lgaName)
        }
      })

    } catch (err) {
      console.error("Map load error", err)
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
  font-family: 'Inter', sans-serif;
}

:deep(.mapboxgl-popup-tip) {
  display: none;
}

/* Pictogram fade-out → fade-in on LGA change */
.picto-fade {
  transition: opacity 0.25s ease;
}

.picto-out {
  opacity: 0;
}

.picto-in {
  opacity: 1;
}

#map-section,
#child-section {
  scroll-margin-top: 150px;
}

/* Real Clothesline Rope Texture */
.rope-shadow {
  /* Use opacity-based shadow instead of filter to avoid costly compositing layer */
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.08));
  will-change: auto;
}

.polaroid-card {
  @apply bg-white p-2 sm:p-3 pb-5 sm:pb-8 shadow-xl border border-[#D8DADC] w-[110px] sm:w-[170px];
  /* Only transition transform and box-shadow — NOT all properties */
  transition: transform 300ms ease, box-shadow 300ms ease;
  flex-shrink: 0;
  position: relative;
  /* Slight rough paper texture */
  background-image: linear-gradient(to bottom right, #ffffff, #fdfdfd);
  /* Promote to GPU compositing layer so hover/scroll transform is handled by compositor */
  will-change: transform;
}

.polaroid-card:hover {
  @apply z-50;
  transform: translateY(60px) rotate(0deg) scale(1.1) !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
}

/* Clothespin Style */
.clip {
  @apply w-3 h-8 sm:w-4 sm:h-10 absolute rounded-sm shadow-sm z-20;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: #e3c193;
  /* Wood color */
  border: 1px solid #c9a67a;
}

/* The metal spring of the clothespin */
.clip-inner {
  @apply w-full h-[2px] bg-gray-400 absolute top-1/2 left-0;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.polaroid-card:nth-child(odd) .clip {
  background: #FF6B6B;
  border-color: #ee5a5a;
}

/* ── "data" word: bright-blue + animated underline drawn on load ── */
.data-highlight {
  color: #0298C5;
  position: relative;
  display: inline-block;
  white-space: nowrap;
}

.data-highlight::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 0;
  height: 6px;
  width: 0;
  background: linear-gradient(90deg, #B5DCFF, #0298C5);
  border-radius: 4px;
  animation: drawUnderline 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.4s forwards;
}

@keyframes drawUnderline {
  from {
    width: 0;
    opacity: 0.4;
  }

  to {
    width: 100%;
    opacity: 1;
  }
}

/* ── Choropleth map shift animation on metric toggle ── */
.map-shifting {
  animation: mapShift 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes mapShift {
  0% {
    opacity: 1;
    transform: scale(1);
  }

  25% {
    opacity: 0.55;
    transform: scale(0.985);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>