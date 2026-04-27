<template>
  <div class="w-full min-h-screen flex flex-col font-sans bg-[#F7F9FB]">
    <LayoutNavbar />

    <!-- Hero Section -->
    <section class="w-full bg-[#F7F9FB] pt-10 pb-20 border-b border-[#D8DADC] overflow-hidden relative">

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
        <h1 class="font-serif font-bold text-[#1A234E] mb-6" style="font-size: 56px; line-height: 1.1;">
          The story the <span class="text-[#7392FF]">data</span> tells
        </h1>
        <p class="text-[#1A234E] text-[20px] max-w-2xl mx-auto leading-relaxed mb-10 opacity-90">
          Behind every statistic is a Victorian family. Explore the reality of food insecurity,
          malnutrition, and the cost of eating well across our state.
        </p>

        <div class="flex flex-wrap justify-center gap-6">
          <div class="flex flex-wrap justify-center gap-6 mt-10">

            <div @click="scrollToSection('map-section')"
              class="group relative bg-white border border-[#D8DADC] rounded-2xl p-8 w-[320px] h-[360px] cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">

              <div
                class="absolute inset-0 translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-out z-0 will-change-transform">
                <div class="absolute inset-0 bg-cover bg-center"
                  style="background-image: url('/visualisation/regional_map.jpg');"></div>
                <div class="absolute inset-0 bg-[#1A234E]/50"></div>
              </div>

              <div class="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <div
                  class="w-20 h-20 bg-[#F7F9FB] group-hover:bg-white/20 rounded-full flex items-center justify-center mb-6 transition-all duration-300">
                  <span class="text-4xl group-hover:scale-110 transition-transform duration-300">🗺️</span>
                </div>

                <h3
                  class="font-serif font-bold text-[#1A234E] text-2xl group-hover:text-white transition-colors duration-300">
                  Regional Map
                </h3>

                <p
                  class="text-base text-[#5F6368] mt-3 group-hover:text-white/90 transition-colors duration-300 leading-relaxed px-2">
                  Explore food insecurity statistics by LGA
                </p>
              </div>
            </div>

            <div @click="scrollToSection('child-section')"
              class="group relative bg-white border border-[#D8DADC] rounded-2xl p-8 w-[320px] h-[360px] cursor-pointer overflow-hidden transition-all duration-300 hover:shadow-2xl hover:-translate-y-2">

              <div
                class="absolute inset-0 translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-out z-0 will-change-transform">
                <div class="absolute inset-0 bg-cover bg-center"
                  style="background-image: url('/visualisation/child_nutrition.jpg');"></div>
                <div class="absolute inset-0 bg-[#FF6B6B]/60"></div>
              </div>

              <div class="relative z-10 flex flex-col items-center justify-center h-full text-center">
                <div
                  class="w-20 h-20 bg-[#F7F9FB] group-hover:bg-white/20 rounded-full flex items-center justify-center mb-6 transition-all duration-300">
                  <span class="text-4xl group-hover:scale-110 transition-transform duration-300">👶</span>
                </div>

                <h3
                  class="font-serif font-bold text-[#1A234E] text-2xl group-hover:text-[#FFF5CC] transition-colors duration-300">
                  Child Health
                </h3>

                <p
                  class="text-base text-[#5F6368] mt-3 group-hover:text-white transition-colors duration-300 leading-relaxed px-2">
                  The impact of malnutrition on young Victorians
                </p>
              </div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- 1st Section: Map -->
    <section class="relative w-full overflow-hidden"
      style="padding-top: 100px; padding-bottom: 80px; content-visibility: auto; contain-intrinsic-size: 0 800px;">
      <div class="max-w-[1200px] mx-auto px-6">
        <div id="map-section" class="mb-8">
          <span class="text-[#FF6B6B] font-bold text-sm tracking-wider uppercase mb-2 block">Around Us</span>
          <h2 class="font-serif font-semibold text-[#1A234E] mb-4" style="font-size: 32px;">
            It's happening right here
          </h2>
          <p class="text-[#5F6368] text-[16px] max-w-2xl mb-8">
            Every region in Victoria tells a different story. Click yours to see the full picture — food insecurity
            rates, people affected, and the food banks trying to help.
          </p>

          <!-- Search Bar & Location -->
          <div class="flex flex-col sm:flex-row gap-4 mb-8">
            <div class="relative flex-[2]">
              <input type="text" v-model="searchQuery" @input="filterLgas" placeholder="Enter your LGA (e.g. Melbourne)"
                class="w-full bg-white border border-[#D8DADC] text-[#1A234E] placeholder-[#5F6368] rounded-xl px-4 py-3 focus:outline-none focus:border-[#7392FF] shadow-sm" />
              <ul v-if="showDropdown && filteredLgas.length"
                class="absolute z-[9999] w-full bg-white border border-[#D8DADC] rounded-xl mt-2 max-h-60 overflow-y-auto shadow-lg">
                <li v-for="lga in filteredLgas" :key="lga" @click="selectLgaFromSearch(lga)"
                  class="px-4 py-3 text-[#1A234E] hover:bg-[#F7F9FB] cursor-pointer">
                  {{ lga }}
                </li>
              </ul>
            </div>
            <button @click="useMyLocation"
              class="flex-1 flex items-center justify-center gap-2 bg-white hover:bg-[#F7F9FB] text-[#1A234E] border border-[#D8DADC] px-4 py-3 rounded-xl font-medium transition-colors shadow-sm">
              <span v-if="isLoadingLocation"
                class="animate-spin h-4 w-4 border-2 border-[#1A234E] border-t-transparent rounded-full inline-block"></span>
              <span v-else>📍</span> Use My Location
            </button>
            <button @click="resetMap" v-if="selectedLgaName"
              class="flex items-center justify-center gap-2 bg-[#F7F9FB] hover:bg-[#E8EEF4] text-[#1A234E] border border-[#D8DADC] px-6 py-3 rounded-xl font-medium transition-colors shadow-sm">
              Reset Map
            </button>
          </div>

          <!-- Toggle Buttons -->
          <div class="flex flex-wrap gap-4 mb-8">
            <button @click="setMetric('foodInsecurity')"
              :class="['px-6 py-3 rounded-full font-medium transition-colors shadow-sm', currentMetric === 'foodInsecurity' ? 'bg-[#F26442] text-white' : 'bg-white text-[#1A234E] border border-[#D8DADC] hover:bg-[#F7F9FB]']">
              Food Insecurity
            </button>
            <button @click="setMetric('foodBanks')"
              :class="['px-6 py-3 rounded-full font-medium transition-colors shadow-sm', currentMetric === 'foodBanks' ? 'bg-[#195128] text-white' : 'bg-white text-[#1A234E] border border-[#D8DADC] hover:bg-[#F7F9FB]']">
              Food Banks
            </button>
            <button @click="setMetric('peopleAffected')"
              :class="['px-6 py-3 rounded-full font-medium transition-colors shadow-sm', currentMetric === 'peopleAffected' ? 'bg-[#7392FF] text-white' : 'bg-white text-[#1A234E] border border-[#D8DADC] hover:bg-[#F7F9FB]']">
              People affected
            </button>
          </div>
        </div>

        <div class="flex flex-col lg:flex-row gap-8 items-stretch lg:h-[600px]">
          <!-- Map Container -->
          <div
            class="lg:flex-[2] h-[420px] lg:h-auto w-full bg-white rounded-[16px] overflow-hidden relative shadow-lg border border-[#D8DADC]">
            <div ref="mapEl" class="w-full h-full bg-[#E8EEF4]" />

            <!-- Map Legend -->
            <div class="absolute bottom-6 left-6 bg-white p-4 rounded-xl shadow-md border border-[#D8DADC]">
              <h4 class="text-xs font-bold text-[#1A234E] mb-3 uppercase tracking-wider">{{ legendTitle }}</h4>
              <div class="flex items-center gap-4 text-sm font-medium text-[#5F6368]">
                <div class="flex items-center gap-2">
                  <span class="w-4 h-4 rounded-full" :style="{ backgroundColor: legendColors[0] }"></span>
                  Low
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-4 h-4 rounded-full" :style="{ backgroundColor: legendColors[1] }"></span>
                  Medium
                </div>
                <div class="flex items-center gap-2">
                  <span class="w-4 h-4 rounded-full" :style="{ backgroundColor: legendColors[2] }"></span>
                  High
                </div>
              </div>
            </div>
          </div>

          <!-- Details Panel -->
          <div class="lg:flex-1 w-full flex flex-col gap-6">
            <div v-if="!selectedLgaStat"
              class="h-full flex flex-col items-center justify-center bg-white rounded-[16px] border border-dashed border-[#D8DADC] shadow-sm p-8 text-center">
              <span class="text-4xl mb-4 opacity-50">👆</span>
              <p class="text-[#5F6368] text-[16px] font-medium">Select a region on the map or use the search box to view
                local statistics.</p>
            </div>
            <template v-else>
              <!-- Food Insecurity Card -->
              <div
                class="bg-white rounded-[16px] p-6 text-center border border-[#D8DADC] shadow-sm flex flex-col items-center justify-center flex-1">
                <h3 class="text-[14px] font-bold text-[#1A234E] uppercase tracking-wide mb-2">Food Insecurity</h3>
                <div class="text-[42px] font-bold text-[#1A234E] leading-none mb-2">{{ displayFoodInsecurity }}%</div>
                <div class="text-[14px] text-[#5F6368]">in {{ selectedLgaStat.lga_name }}</div>
              </div>

              <!-- People Affected Card -->
              <div
                class="bg-white rounded-[16px] p-6 text-center border border-[#D8DADC] shadow-sm flex flex-col items-center justify-center flex-[1.5]">
                <h3 class="text-[14px] font-bold text-[#1A234E] uppercase tracking-wide mb-2">People Affected</h3>
                <div class="text-[36px] font-bold text-[#1A234E] leading-none mb-4">{{
                  displayPeopleAffected.toLocaleString() }}</div>

                <div class="w-full flex justify-between items-center mb-2 px-4">
                  <span class="text-xs font-bold text-[#1A234E]">MEN</span>
                  <span class="text-xs font-bold text-[#1A234E]">{{ menNeedRatio }}/10</span>
                </div>
                <div
                  :class="['flex justify-center gap-1 mb-4 px-2 picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
                  <svg v-for="n in 10" :key="'m' + n" :class="n <= menNeedRatio ? 'text-[#7392FF]' : 'text-[#D8DADC]'"
                    class="w-6 h-6 fill-current" viewBox="0 0 24 24">
                    <path
                      d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                  </svg>
                </div>

                <div class="w-full flex justify-between items-center mb-2 px-4">
                  <span class="text-xs font-bold text-[#1A234E]">WOMEN</span>
                  <span class="text-xs font-bold text-[#1A234E]">{{ womenNeedRatio }}/10</span>
                </div>
                <div
                  :class="['flex justify-center gap-1 px-2 picto-fade', pictogramVisible ? 'picto-in' : 'picto-out']">
                  <svg v-for="n in 10" :key="'w' + n" :class="n <= womenNeedRatio ? 'text-[#EC4899]' : 'text-[#D8DADC]'"
                    class="w-6 h-6 fill-current" viewBox="0 0 24 24">
                    <path
                      d="M12 2C10.62 2 9.5 3.12 9.5 4.5C9.5 5.88 10.62 7 12 7C13.38 7 14.5 5.88 14.5 4.5C14.5 3.12 13.38 2 12 2ZM12 9C9.33 9 4 10.34 4 13V22H8V16H16V22H20V13C20 10.34 14.67 9 12 9Z" />
                  </svg>
                </div>
              </div>

              <!-- Food Banks Card -->
              <div
                class="bg-white rounded-[16px] p-6 text-center border border-[#D8DADC] shadow-sm flex flex-col items-center justify-center flex-1">
                <h3 class="text-[14px] font-bold text-[#1A234E] uppercase tracking-wide mb-2">Food Banks</h3>
                <div class="text-[42px] font-bold text-[#1A234E] leading-none mb-2">{{ displayFoodBanks }}</div>
                <div class="text-[14px] text-[#5F6368]">in {{ selectedLgaStat.lga_name }}</div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- 2nd Section: The Children -->
    <section id="child-section" class="py-[80px] bg-white border-t border-[#D8DADC]"
      style="content-visibility: auto; contain-intrinsic-size: 0 700px;">
      <div class="max-w-[1200px] mx-auto px-6">
        <span class="text-[#FF6B6B] font-bold text-sm tracking-wider uppercase mb-2 block">The Children</span>
        <h2 class="font-serif font-semibold text-[#1A234E] mb-6" style="font-size: 32px;">
          No child should grow up hungry
        </h2>
        <p class="text-[#5F6368] text-[16px] max-w-2xl mb-12">
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
            class="bg-[#F7F9FB] rounded-[16px] w-full max-w-4xl flex flex-col sm:flex-row items-stretch border border-[#D8DADC] shadow-sm overflow-hidden">
            <div class="bg-[#B3D9FF] p-8 sm:w-1/3 flex flex-col justify-center items-center">
              <span class="text-[48px] font-bold text-[#1A234E] leading-none mb-2">12%</span>
              <span class="text-[#1A234E] font-bold text-[18px]">Malnourished</span>
            </div>
            <div class="p-8 sm:w-2/3 flex items-center">
              <p class="text-[#5F6368] text-[16px] leading-relaxed">
                Infants in Victoria aren't getting adequate nutrition — putting their brain development and immune
                system at
                serious risk.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3rd Section: Ready to take the next step? -->
    <section class="py-[80px] bg-[#EAF2FF]" style="content-visibility: auto; contain-intrinsic-size: 0 500px;">
      <div class="max-w-[1200px] mx-auto px-6">
        <h2 class="font-serif font-bold text-[#1A234E] mb-2" style="font-size: 32px;">
          Ready to take the next step?
        </h2>
        <span class="text-[#FF6B6B] font-medium text-[16px] block mb-12">Here is where to start</span>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Card 1 -->
          <div
            class="bg-white rounded-[16px] p-8 shadow-sm border border-[#D8DADC] flex flex-col h-full hover:shadow-md transition-shadow">
            <h3 class="font-serif font-bold text-[#1A234E] text-[24px] mb-4">Find Food Banks<br>near me</h3>
            <p class="text-[#5F6368] text-[16px] flex-grow mb-8">Find free food support open right now</p>
            <NuxtLink to="/services">
              <button
                class="bg-[#B3D9FF] text-[#1A234E] px-6 py-3 rounded-full font-bold hover:bg-[#99C2FF] transition-colors w-auto text-sm">
                Find Nearby Food Banks
              </button>
            </NuxtLink>
          </div>

          <!-- Card 2 -->
          <div
            class="bg-white rounded-[16px] p-8 shadow-sm border border-[#D8DADC] flex flex-col h-full hover:shadow-md transition-shadow">
            <h3 class="font-serif font-bold text-[#1A234E] text-[24px] mb-4">Find groceries at<br>best prices</h3>
            <p class="text-[#5F6368] text-[16px] flex-grow mb-8">Tell us your needs and we'll find you the right
              groceries
            </p>
            <button
              class="bg-[#B3D9FF] text-[#1A234E] px-6 py-3 rounded-full font-bold hover:bg-[#99C2FF] transition-colors w-auto text-sm self-start">
              Explore Ingredients
            </button>
          </div>

          <!-- Card 3 -->
          <div
            class="bg-white rounded-[16px] p-8 shadow-sm border border-[#D8DADC] flex flex-col h-full hover:shadow-md transition-shadow">
            <h3 class="font-serif font-bold text-[#1A234E] text-[24px] mb-4">Know more<br>about nutrition</h3>
            <p class="text-[#5F6368] text-[16px] flex-grow mb-8">Simple guides for your family's health</p>
            <button
              class="bg-[#B3D9FF] text-[#1A234E] px-6 py-3 rounded-full font-bold hover:bg-[#99C2FF] transition-colors w-auto text-sm self-start">
              Learn about nutrition
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

const setMetric = (metric) => {
  currentMetric.value = metric
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
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
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
  if (currentMetric.value === 'foodInsecurity') return ['#FFD180', '#FF9800', '#E65100']
  if (currentMetric.value === 'foodBanks') return ['#A5D6A7', '#4CAF50', '#1B5E20']
  return ['#90CAF9', '#2196F3', '#0D47A1']
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

.polaroid-card:nth-child(even) .clip {
  background: #7392FF;
  border-color: #5f7ee8;
}
</style>