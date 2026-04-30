<template>
  <div class="page-wrap">
    <TopNavigation />
    <div class="h-[72px] lg:h-[100px]" />

    <!-- ── Search & Filter Header ── -->
    <div ref="headerEl" class="services-header">
      <h1 style="font-family:'Noto Serif',serif; font-size:26px; font-weight:700; color:#1a1a1a; text-align:center; margin-bottom:18px;">
        Find Nearby Relief Services
      </h1>

      <!-- Search row -->
      <div class="search-row">
        <div style="flex:1; display:flex; align-items:center; background:white; border:1.5px solid #d0cbbf; border-radius:10px; padding:0 16px; gap:10px;">
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" style="flex-shrink:0;">
            <circle cx="11" cy="11" r="8" stroke="#9ca3af" stroke-width="2"/>
            <path d="m21 21-4.35-4.35" stroke="#9ca3af" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input
            ref="searchInputEl"
            v-model="searchQuery"
            type="text"
            placeholder="Enter suburb or postcode"
            style="flex:1; border:none; outline:none; font-size:15px; color:#333; height:48px; background:transparent; font-family:Inter,sans-serif;"
            @keydown.enter="searchByAddress"
          />
          <button v-if="searchQuery" @click="searchQuery = ''"
            style="background:none; border:none; cursor:pointer; padding:4px; color:#aaa; display:flex; align-items:center;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- Search button -->
        <button @click="searchByAddress" :disabled="!searchQuery.trim()"
          style="background:#2D5016; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif;"
          :style="!searchQuery.trim() ? 'opacity:0.45;cursor:not-allowed;' : ''">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="white" stroke-width="2"/>
            <path d="m21 21-4.35-4.35" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Search
        </button>

        <!-- Locate Me button -->
        <button @click="locateMe" :disabled="locating"
          style="background:#2D5016; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif;"
          :style="locating ? 'opacity:0.7;cursor:not-allowed;' : ''">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="3" stroke="white" stroke-width="2"/>
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          {{ locating ? 'Locating…' : 'Locate Me' }}
        </button>
      </div>

      <!-- Filter row -->
      <div style="display:flex; align-items:center; max-width:860px; margin:0 auto; gap:12px; flex-wrap:wrap;">
        <div style="display:flex; border:1px solid #ccc; border-radius:8px; overflow:hidden;">
          <button v-for="tab in CATEGORY_TABS" :key="tab.value" @click="activeFilter = tab.value"
            style="padding:9px 18px; border:none; cursor:pointer; font-size:14px; font-family:Inter,sans-serif; transition:background 0.15s;"
            :style="{
              fontWeight: activeFilter === tab.value ? '700' : '400',
              color: activeFilter === tab.value ? '#1a1a1a' : '#777',
              background: activeFilter === tab.value ? 'white' : 'transparent',
            }">{{ tab.label }}</button>
        </div>
        <!-- Filters dropdown (hover to open) -->
        <div class="filters-dropdown" style="margin-left:auto; position:relative;">
          <button
            class="filters-btn"
            style="border:1px solid #ccc; background:white; border-radius:6px; padding:8px 14px; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:6px; color:#444; font-family:Inter,sans-serif;"
            :style="openNowFilter ? 'border-color:#2D5016; color:#2D5016; font-weight:600;' : ''"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <line x1="4" y1="6" x2="20" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="7" y1="12" x2="17" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="10" y1="18" x2="14" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Filters
            <span v-if="openNowFilter"
              style="background:#2D5016; color:white; border-radius:10px; font-size:11px; font-weight:700; padding:1px 7px; margin-left:2px;">1</span>
          </button>

          <!-- Dropdown panel -->
          <div class="filters-panel">
            <p style="font-size:11px; font-weight:700; color:#aaa; text-transform:uppercase; letter-spacing:0.7px; margin:0 0 10px;">Availability</p>
            <label style="display:flex; align-items:center; gap:10px; font-size:14px; cursor:pointer; color:#333; user-select:none; font-family:Inter,sans-serif;">
              <input type="checkbox" v-model="openNowFilter" style="width:16px; height:16px; accent-color:#2D5016; cursor:pointer;" />
              <span>Open Now</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Main: Cards + Map ── -->
    <div class="main-panel" :style="{ height: mainHeight }">

      <!-- ── Left Panel ── -->
      <div class="left-panel">

        <!-- ── Directions Panel ── -->
        <div v-show="showingDirections" style="display:flex; flex-direction:column; flex:1; min-height:0; overflow:hidden;">
          <div style="padding:14px 16px 0; flex-shrink:0;">
            <button @click="clearDirections"
              style="display:inline-flex; align-items:center; gap:6px; background:none; border:none; cursor:pointer; font-size:14px; font-weight:600; color:#2D5016; font-family:Inter,sans-serif; padding:0; margin-bottom:12px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Back to results
            </button>

            <!-- Route summary -->
            <div v-if="directionsInfo" style="background:white; border:1px solid #e8e3da; border-radius:12px; padding:16px; margin-bottom:14px;">
              <p style="font-size:11px; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">Directions to</p>
              <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:14px; line-height:1.3;">{{ directionsInfo.service }}</p>
              <div style="display:flex; gap:20px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#f0f5ec; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#2D5016" stroke-width="2"/>
                      <circle cx="12" cy="10" r="3" stroke="#2D5016" stroke-width="2"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#2D5016; margin:0; line-height:1;">{{ directionsInfo.distance }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">distance</p>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#f0f5ec; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="#2D5016" stroke-width="2"/>
                      <path d="M12 7v5l3 3" stroke="#2D5016" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#2D5016; margin:0; line-height:1;">{{ directionsInfo.duration }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">by car</p>
                  </div>
                </div>
              </div>
            </div>
            <p style="font-size:11px; font-weight:700; color:#aaa; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">Step-by-step</p>
          </div>

          <!-- Step list (rendered from OSRM) -->
          <div class="cards-scroll" style="padding:0 16px 24px;">
            <div v-if="directionsLoading" style="padding:20px 0; text-align:center; color:#aaa; font-size:14px;">
              Calculating route…
            </div>
            <div v-else>
              <div v-for="(step, i) in directionsSteps" :key="i"
                style="display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px solid #f0ece6;">
                <!-- Maneuver icon -->
                <div style="width:28px; height:28px; background:#f0f5ec; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path :d="step.iconPath" stroke="#2D5016" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div style="flex:1;">
                  <p style="font-size:13px; color:#333; margin:0 0 2px; line-height:1.4;">{{ step.instruction }}</p>
                  <p style="font-size:12px; color:#aaa; margin:0;">{{ step.distance }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ── Services List ── -->
        <div v-show="!showingDirections" class="cards-scroll">

          <!-- Result count -->
          <p v-if="!loading" style="font-size:13px; color:#888; margin-bottom:12px; padding:0 2px;">
            <strong style="color:#555;">{{ filteredServices.length }}</strong> {{ filteredServices.length === 1 ? 'service' : 'services' }}
            <span v-if="locationLabel"> · sorted by distance from <strong style="color:#555;">{{ locationLabel }}</strong></span>
            <span v-else> across Victoria</span>
          </p>

          <!-- Loading skeletons -->
          <div v-if="loading">
            <div v-for="i in 4" :key="i" style="background:white; border:1px solid #e8e3da; border-radius:12px; padding:18px; margin-bottom:12px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <div style="height:22px; width:130px; background:#f0ede8; border-radius:20px;"></div>
                <div style="height:22px; width:100px; background:#f0ede8; border-radius:20px;"></div>
              </div>
              <div style="height:18px; background:#f0ede8; border-radius:4px; margin-bottom:8px; width:75%;"></div>
              <div style="height:14px; background:#f0ede8; border-radius:4px; margin-bottom:6px;"></div>
              <div style="height:14px; background:#f0ede8; border-radius:4px; width:60%;"></div>
            </div>
          </div>

          <!-- Empty -->
          <div v-else-if="filteredServices.length === 0" style="padding:40px 8px; text-align:center; color:#999;">
            <p style="font-size:15px; font-weight:600; color:#444; margin-bottom:6px;">No services found</p>
            <p style="font-size:13px;">Try adjusting your filters.</p>
          </div>

          <!-- Service Cards -->
          <div v-else>
            <div v-for="service in filteredServices" :key="service.id"
              style="background:white; border-radius:12px; padding:18px; margin-bottom:12px; cursor:pointer; transition:box-shadow 0.2s, border-color 0.2s;"
              :style="{
                border: selectedService?.id === service.id ? '2px solid #2D5016' : '1px solid #e8e3da',
                boxShadow: selectedService?.id === service.id ? '0 2px 14px rgba(45,80,22,0.13)' : '0 1px 3px rgba(0,0,0,0.04)',
              }"
              @click="selectService(service)">

              <!-- Badges -->
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; gap:8px;">
                <span :style="getCategoryBadgeStyle(service)">
                  <svg v-if="isHousing(service)" width="12" height="12" viewBox="0 0 24 24" fill="currentColor" style="margin-right:4px; flex-shrink:0;">
                    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
                  </svg>
                  <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="currentColor" style="margin-right:4px; flex-shrink:0;">
                    <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                  </svg>
                  {{ getCategoryLabel(service) }}
                </span>
                <span v-if="getStatusLabel(service)" :style="getStatusBadgeStyle(service)">
                  {{ getStatusLabel(service) }}
                </span>
              </div>

              <!-- Name + distance -->
              <div style="display:flex; align-items:baseline; justify-content:space-between; gap:8px; margin-bottom:6px;">
                <h3 style="font-size:17px; font-weight:700; color:#1a1a1a; line-height:1.3; margin:0;">{{ service.name }}</h3>
                <span v-if="service.distance_km != null" style="font-size:12px; color:#888; white-space:nowrap; flex-shrink:0;">
                  {{ service.distance_km.toFixed(1) }} km
                </span>
              </div>

              <!-- Description -->
              <p style="font-size:13px; color:#555; line-height:1.6; margin-bottom:12px; overflow:hidden; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;">
                {{ service.description || service.target_audience }}
              </p>

              <!-- Info row -->
              <div style="display:flex; gap:16px; flex-wrap:wrap; margin-bottom:12px;">
                <span v-if="getHoursDisplay(service)" style="display:flex; align-items:center; gap:5px; font-size:12px; color:#666;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="#888" stroke-width="2"/>
                    <path d="M12 7v5l3 3" stroke="#888" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  {{ getHoursDisplay(service) }}
                </span>
                <span v-if="service.nearest_train_station" style="display:flex; align-items:center; gap:5px; font-size:12px; color:#666;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                    <rect x="6" y="2" width="12" height="15" rx="2" stroke="#888" stroke-width="2"/>
                    <path d="M6 9h12M9 19l-2 3M15 19l2 3" stroke="#888" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="9" cy="14" r="1" fill="#888"/>
                    <circle cx="15" cy="14" r="1" fill="#888"/>
                  </svg>
                  {{ service.nearest_train_station }}
                </span>
              </div>

              <!-- Actions -->
              <div style="display:flex; gap:8px; padding-top:10px; border-top:1px solid #f0ece6;">
                <button @click.stop="getDirections(service)" :disabled="!userLocation"
                  style="flex:1; display:flex; align-items:center; justify-content:center; gap:6px; padding:8px 12px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif;"
                  :style="userLocation
                    ? 'background:#f0f5ec; color:#2D5016; border:1.5px solid #2D5016;'
                    : 'background:#f5f5f5; color:#aaa; border:1.5px solid #ddd; cursor:not-allowed;'"
                  :title="userLocation ? 'Show route on map' : 'Enter your location first'">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M3 11l19-9-9 19-2-8-8-2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
                  </svg>
                  Get Directions
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Map Panel ── -->
      <div class="map-panel">
        <div ref="mapEl" style="position:absolute; inset:0;"></div>

        <!-- Route info bar -->
        <div v-if="directionsInfo"
          style="position:absolute; bottom:16px; left:50%; transform:translateX(-50%); background:white; border-radius:12px; padding:12px 18px; box-shadow:0 4px 20px rgba(0,0,0,0.18); display:flex; align-items:center; gap:14px; z-index:1000; white-space:nowrap;">
          <div style="width:36px; height:36px; background:#f0f5ec; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M3 11l19-9-9 19-2-8-8-2z" stroke="#2D5016" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <p style="font-size:12px; color:#888; margin:0 0 2px;">Route to</p>
            <p style="font-size:13px; font-weight:700; color:#1a1a1a; margin:0; max-width:200px; overflow:hidden; text-overflow:ellipsis;">{{ directionsInfo.service }}</p>
          </div>
          <div style="border-left:1px solid #e8e3da; padding-left:14px;">
            <p style="font-size:15px; font-weight:700; color:#2D5016; margin:0;">{{ directionsInfo.distance }}</p>
            <p style="font-size:12px; color:#888; margin:0;">{{ directionsInfo.duration }} drive</p>
          </div>
          <button @click="clearDirections"
            style="width:30px; height:30px; border-radius:50%; border:1.5px solid #ddd; background:white; cursor:pointer; display:flex; align-items:center; justify-content:center; color:#666;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import TopNavigation from '../components/TopNavigation.vue'

definePageMeta({ ssr: false })

// Leaflet is browser-only — loaded dynamically inside onMounted
let L = null

// ── Constants ──────────────────────────────────────────────────────────────
const CATEGORY_TABS = [
  { value: 'food', label: 'Food Aid' },
  { value: 'housing', label: 'Housing Relief' },
  { value: 'both', label: 'Show Both' },
]

const MOCK_SERVICES = [
  {
    id: 1, name: 'Foodbank Victoria',
    description: 'Emergency food hampers and fresh produce for individuals and families experiencing food insecurity.',
    target_audience: 'Individuals and families',
    address: '2 Coventry St, Southbank VIC 3006', suburb: 'Southbank',
    primary_phone: '(03) 9362 8400', website: 'https://www.foodbank.org.au/',
    categories: ['Food Bank'], latitude: -37.8248, longitude: 144.9572,
    nearest_train_station: 'Flinders St. (8 min walk)',
    opening_hours: { monday: '9:00am - 5:00pm', tuesday: '9:00am - 5:00pm', wednesday: '9:00am - 5:00pm', thursday: '9:00am - 5:00pm', friday: '9:00am - 5:00pm' },
    is_open_now: true, distance_km: null,
  },
  {
    id: 2, name: 'Melbourne City Mission',
    description: 'Emergency accommodation, food parcels and support services for people experiencing homelessness.',
    target_audience: 'People experiencing homelessness',
    address: 'Level 1/110 Victoria Parade, Collingwood VIC 3066', suburb: 'Collingwood',
    primary_phone: '(03) 9929 9889', website: 'https://www.mcm.org.au/',
    categories: ['Housing Service', 'Emergency Shelter'], latitude: -37.8032, longitude: 144.9792,
    nearest_train_station: 'Collingwood (5 min walk)',
    opening_hours: { monday: '24 hours', tuesday: '24 hours', wednesday: '24 hours', thursday: '24 hours', friday: '24 hours', saturday: '24 hours', sunday: '24 hours' },
    is_open_now: true, beds_available: 12, distance_km: null,
  },
  {
    id: 3, name: 'The Salvation Army Melbourne',
    description: 'Food parcels, pantry items, fresh produce and frozen meals. Emergency financial assistance also offered.',
    target_audience: 'Individuals and families in need',
    address: '69 Bourke St, Melbourne VIC 3000', suburb: 'Melbourne',
    primary_phone: '(03) 9653 3300', website: 'https://www.salvationarmy.org.au/',
    categories: ['Food Bank'], latitude: -37.8123, longitude: 144.9647,
    nearest_train_station: 'Melbourne Central (3 min walk)',
    opening_hours: { monday: '10:00am - 3:00pm', tuesday: '10:00am - 3:00pm', wednesday: '10:00am - 3:00pm', thursday: '10:00am - 3:00pm', friday: '10:00am - 2:00pm' },
    is_open_now: true, distance_km: null,
  },
  {
    id: 4, name: 'Wintringham Housing',
    description: 'Secure housing and specialist support services for older people who are homeless or at risk of homelessness.',
    target_audience: 'Older people (50+)', address: '141 Nicholson St, Carlton VIC 3053', suburb: 'Carlton',
    primary_phone: '(03) 9349 2300', website: 'https://www.wintringham.org.au/',
    categories: ['Housing Service'], latitude: -37.7989, longitude: 144.9669,
    nearest_train_station: 'Melbourne Central (8 min walk)',
    opening_hours: { monday: '9:00am - 5:00pm', tuesday: '9:00am - 5:00pm', wednesday: '9:00am - 5:00pm', thursday: '9:00am - 5:00pm', friday: '9:00am - 5:00pm' },
    is_open_now: true, beds_available: 8, distance_km: null,
  },
]

// ── State ──────────────────────────────────────────────────────────────────
const mapEl = ref(null)
const headerEl = ref(null)
const searchQuery = ref('')
const activeFilter = ref('both')
const openNowFilter = ref(false)
const loading = ref(false)
const locating = ref(false)
const services = ref([])
const selectedService = ref(null)
const userLocation = ref(null)
const locationLabel = ref('')
const mainHeight = ref('600px')
const directionsInfo = ref(null)
const directionsSteps = ref([])
const directionsLoading = ref(false)
const showingDirections = ref(false)

let mapInstance = null
let markersMap = {}
let userMarker = null
let routeLayer = null

const config = useRuntimeConfig()
const API_BASE = config.public.apiBase

// ── Computed ───────────────────────────────────────────────────────────────
const filteredServices = computed(() => {
  let result = services.value
  if (activeFilter.value === 'food') result = result.filter(isFood)
  else if (activeFilter.value === 'housing') result = result.filter(isHousing)
  if (openNowFilter.value) result = result.filter(s => s.is_open_now === true)
  return result
})

// ── Category helpers ───────────────────────────────────────────────────────
function isFood(s) {
  return /food|meal|pantry|groceries|relief|provision/i.test(
    [...(s.categories || []), s.name || '', s.description || ''].join(' ')
  )
}
function isHousing(s) {
  return /hous|shelter|accommodation|refuge|bedroom|beds|homelessness/i.test(
    [...(s.categories || []), s.name || '', s.description || ''].join(' ')
  )
}
function getCategoryLabel(s) {
  if (isHousing(s)) return 'HOUSING SERVICE'
  if (isFood(s)) return 'FOOD BANK'
  return 'SUPPORT SERVICE'
}
function getCategoryBadgeStyle(s) {
  const base = 'display:inline-flex;align-items:center;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;padding:4px 10px;border-radius:20px;'
  if (isHousing(s)) return base + 'background:#e0ede9;color:#2A6355;'
  if (isFood(s)) return base + 'background:#fdebd4;color:#954E0F;'
  return base + 'background:#e8eaf6;color:#3949AB;'
}
function getStatusLabel(s) {
  if (s.beds_available != null) return `${s.beds_available} Beds Available`
  if (s.is_open_now === true) { const c = getClosingTime(s); return c ? `Open Until ${c}` : 'Open Now' }
  if (s.is_open_now === false) return 'Closed'
  const hasHours = s.opening_hours && Object.keys(s.opening_hours).length > 0
  if (!hasHours) return 'Hours not listed'
  return null
}
function getStatusBadgeStyle(s) {
  const base = 'display:inline-flex;align-items:center;font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px;white-space:nowrap;'
  if (s.beds_available != null) return base + 'background:#dff0d8;color:#2D5016;'
  if (s.is_open_now === true) return base + 'background:#f0ece4;color:#6B5022;'
  if (s.is_open_now === false) return base + 'background:#fde8e8;color:#c0392b;'
  return base + 'background:#f5f5f5;color:#666;'
}
function getClosingTime(s) {
  if (!s.opening_hours) return null
  const days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
  const hours = s.opening_hours[days[new Date().getDay()]]
  if (!hours || typeof hours !== 'string') return null
  const m = hours.match(/[-–]\s*(\d+(?::\d+)?\s*(?:am|pm))/i)
  return m ? m[1].replace(':00','').toUpperCase() : null
}
function getHoursDisplay(s) {
  if (s.opening_hours_display) return s.opening_hours_display
  if (!s.opening_hours) return null
  const days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
  return s.opening_hours[days[new Date().getDay()]] || null
}

// ── API ────────────────────────────────────────────────────────────────────
async function fetchAllServices() {
  loading.value = true
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone
    const res = await fetch(`${API_BASE}/services?tz=${encodeURIComponent(tz)}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    services.value = data.length ? data : MOCK_SERVICES
  } catch {
    services.value = MOCK_SERVICES
  } finally {
    loading.value = false
    await nextTick()
    updateMapMarkers()
    fitMapToMarkers()
  }
}

// ── Distance ───────────────────────────────────────────────────────────────
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLon = (lon2 - lon1) * Math.PI / 180
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
}
function sortByDistance(lat, lon) {
  services.value = services.value.map(s => ({
    ...s,
    distance_km: s.latitude && s.longitude ? haversine(lat, lon, s.latitude, s.longitude) : null,
  })).sort((a, b) => {
    if (a.distance_km == null) return 1
    if (b.distance_km == null) return -1
    return a.distance_km - b.distance_km
  })
}

// ── Geolocation ────────────────────────────────────────────────────────────
function locateMe() {
  if (!navigator.geolocation) { alert('Geolocation not supported.'); return }
  locating.value = true
  navigator.geolocation.getCurrentPosition(
    ({ coords: { latitude: lat, longitude: lon } }) => {
      locating.value = false
      userLocation.value = { lat, lon }
      locationLabel.value = 'your location'
      mapInstance?.setView([lat, lon], 13)
      placeUserMarker(lat, lon)
      sortByDistance(lat, lon)
      updateMapMarkers()
    },
    () => { locating.value = false },
    { timeout: 10000 }
  )
}

// ── Geocoding via Nominatim (free, no key) ─────────────────────────────────
async function searchByAddress() {
  const q = searchQuery.value.trim()
  if (!q) return
  clearDirections()
  loading.value = true
  try {
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(q + ', Victoria, Australia')}&format=json&limit=1&countrycodes=au`
    const res = await fetch(url, { headers: { 'User-Agent': 'OpenDoorVictoria/1.0 (university project)' } })
    const data = await res.json()
    if (!data.length) throw new Error('No results')
    const lat = parseFloat(data[0].lat)
    const lon = parseFloat(data[0].lon)
    const label = data[0].display_name.split(',')[0]
    userLocation.value = { lat, lon }
    locationLabel.value = label
    mapInstance?.setView([lat, lon], 13)
    placeUserMarker(lat, lon)
    sortByDistance(lat, lon)
    updateMapMarkers()
  } catch {
    // Geocode failed — list stays sorted as-is
  } finally {
    loading.value = false
  }
}

// ── Map helpers ────────────────────────────────────────────────────────────
function placeUserMarker(lat, lon) {
  if (!mapInstance) return
  userMarker?.remove()
  userMarker = L.circleMarker([lat, lon], {
    radius: 9, fillColor: '#2D5016', fillOpacity: 1,
    color: 'white', weight: 3
  }).addTo(mapInstance).bindPopup('<strong>Your location</strong>')
}

function selectService(service) {
  selectedService.value = service
  if (!service.latitude || !service.longitude || !mapInstance) return
  mapInstance.setView([service.latitude, service.longitude], 15)
  markersMap[service.id]?.openPopup()
}

function buildPopupHTML(s) {
  return `
    <div style="font-family:Inter,sans-serif;min-width:180px;">
      <p style="font-size:13px;font-weight:700;margin:0 0 4px;color:#1a1a1a;line-height:1.3;">${s.name || ''}</p>
      ${s.address ? `<p style="font-size:12px;color:#666;margin:0 0 5px;">${s.address}</p>` : ''}
      ${s.primary_phone ? `<p style="font-size:12px;color:#2D5016;margin:0 0 4px;">${s.primary_phone}</p>` : ''}
      ${s.website ? `<a href="${s.website}" target="_blank" rel="noopener" style="font-size:12px;color:#2D5016;">Visit website ↗</a>` : ''}
    </div>
  `
}

function updateMapMarkers() {
  if (!mapInstance) return
  Object.values(markersMap).forEach(m => m.remove())
  markersMap = {}
  filteredServices.value.forEach(service => {
    if (!service.latitude || !service.longitude) return
    const housing = isHousing(service)
    const color = housing ? '#4A7A6D' : '#C07A2A'
    const marker = L.circleMarker([service.latitude, service.longitude], {
      radius: 9,
      fillColor: color,
      fillOpacity: service.is_open_now === false ? 0.4 : 1,
      color: 'white',
      weight: 2,
    }).addTo(mapInstance)
    marker.bindPopup(buildPopupHTML(service))
    marker.on('click', () => { selectedService.value = service })
    markersMap[service.id] = marker
  })
}

function fitMapToMarkers() {
  if (!mapInstance) return
  const coords = filteredServices.value
    .filter(s => s.latitude && s.longitude)
    .map(s => [s.latitude, s.longitude])
  if (coords.length) mapInstance.fitBounds(L.latLngBounds(coords), { padding: [40, 40] })
}

// Re-draw on filter change
watch(filteredServices, () => {
  updateMapMarkers()
  clearDirections()
})

// ── Directions via OSRM (free, no key) ─────────────────────────────────────
async function getDirections(service) {
  if (!userLocation.value || !mapInstance) return
  selectedService.value = service
  showingDirections.value = true
  directionsLoading.value = true
  directionsSteps.value = []
  directionsInfo.value = null

  // Remove previous route
  routeLayer?.remove()
  routeLayer = null

  try {
    const { lat, lon } = userLocation.value
    const url = `https://router.project-osrm.org/route/v1/driving/${lon},${lat};${service.longitude},${service.latitude}?overview=full&geometries=geojson&steps=true`
    const res = await fetch(url)
    const data = await res.json()
    if (data.code !== 'Ok' || !data.routes.length) throw new Error('No route')

    const route = data.routes[0]
    const distKm = (route.distance / 1000).toFixed(1)
    const durMin = Math.round(route.duration / 60)

    directionsInfo.value = {
      service: service.name,
      distance: `${distKm} km`,
      duration: durMin >= 60
        ? `${Math.floor(durMin/60)}h ${durMin%60}m`
        : `${durMin} min`,
    }

    // Draw route polyline
    routeLayer = L.geoJSON(route.geometry, {
      style: { color: '#2D5016', weight: 5, opacity: 0.85 }
    }).addTo(mapInstance)
    mapInstance.fitBounds(routeLayer.getBounds(), { padding: [60, 60] })

    // Build step list from OSRM legs
    const steps = route.legs.flatMap(leg => leg.steps)
    directionsSteps.value = steps.map(step => ({
      instruction: formatManeuver(step),
      distance: formatMeters(step.distance),
      iconPath: maneuverIcon(step.maneuver),
    }))
  } catch {
    directionsInfo.value = directionsInfo.value || {
      service: service.name, distance: '—', duration: '—'
    }
    directionsSteps.value = [{ instruction: 'Could not calculate route. Check your connection.', distance: '', iconPath: 'M12 9v4M12 17h.01' }]
  } finally {
    directionsLoading.value = false
  }
}

function clearDirections() {
  routeLayer?.remove()
  routeLayer = null
  directionsInfo.value = null
  directionsSteps.value = []
  showingDirections.value = false
}

// ── OSRM step formatting ───────────────────────────────────────────────────
function formatManeuver(step) {
  const t = step.maneuver?.type || ''
  const mod = step.maneuver?.modifier || ''
  const name = step.name ? ` onto ${step.name}` : ''
  if (t === 'depart') return `Head ${mod || 'forward'}${name}`
  if (t === 'arrive') return 'Arrive at your destination'
  if (t === 'turn') return `Turn ${mod}${name}`
  if (t === 'fork') return `Keep ${mod}${name}`
  if (t === 'merge') return `Merge ${mod}${name}`
  if (t === 'roundabout' || t === 'rotary') return `Enter roundabout${name}`
  if (t === 'exit roundabout' || t === 'exit rotary') return `Exit roundabout${name}`
  if (t === 'new name') return `Continue${name}`
  return `Continue${name}`
}

function formatMeters(m) {
  if (!m) return ''
  return m < 1000 ? `${Math.round(m)} m` : `${(m/1000).toFixed(1)} km`
}

function maneuverIcon(maneuver) {
  const mod = maneuver?.modifier || ''
  const type = maneuver?.type || ''
  if (type === 'arrive') return 'M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8zM12 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4z'
  if (type === 'depart') return 'M12 19V5M5 12l7-7 7 7'
  if (mod.includes('left')) return 'M10 19l-7-7 7-7M3 12h18'
  if (mod.includes('right')) return 'M14 5l7 7-7 7M21 12H3'
  return 'M12 19V5M5 12l7-7 7 7' // straight
}

// ── Init ───────────────────────────────────────────────────────────────────
onMounted(async () => {
  await nextTick()
  updateLayout()
  window.addEventListener('resize', updateLayout)

  // Dynamic import — Leaflet requires browser globals (window/document)
  await import('leaflet/dist/leaflet.css')
  L = (await import('leaflet')).default

  // Leaflet initialisation — no API key needed
  mapInstance = L.map(mapEl.value, {
    center: [-36.8, 144.9],
    zoom: 7,
    zoomControl: true,
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  }).addTo(mapInstance)

  await fetchAllServices()
})

function updateLayout() {
  const headerH = headerEl.value?.offsetHeight ?? 185
  const navbarH = 86
  if (window.innerWidth >= 768) {
    mainHeight.value = `calc(100vh - ${navbarH + headerH}px)`
  } else {
    mainHeight.value = 'auto'
  }
  // Delay lets the browser finish the CSS reflow before Leaflet measures the container
  nextTick(() => setTimeout(() => mapInstance?.invalidateSize(), 50))
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayout)
  mapInstance?.remove()
})
</script>

<style scoped>
/* ── Page shell ─────────────────────────────────────── */
.page-wrap {
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #fafafa;
  overflow-x: hidden;
}

/* ── Search / filter header ─────────────────────────── */
.services-header {
  background: #ede8df;
  padding: 28px 40px 20px;
  border-bottom: 1px solid #dfd7c7;
  flex-shrink: 0;
  position: relative;
  z-index: 1100;
}

/* ── Search row ─────────────────────────────────────── */
.search-row {
  display: flex;
  gap: 10px;
  max-width: 860px;
  margin: 0 auto 14px;
}

/* ── Main panel (cards + map side by side) ──────────── */
.main-panel {
  display: flex;
  /* height is set by JS inline style (calc 100vh - navbar - header).
     flex:1 is intentionally absent — it would let children expand the panel
     beyond the viewport height, making the page scroll endlessly. */
  flex-shrink: 0;
  overflow: hidden;
}

/* ── Left card panel ─────────────────────────────────── */
.left-panel {
  width: 390px;
  min-width: 340px;
  background: #fafafa;
  border-right: 1px solid #e8e3da;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
  /* Without min-height:0, flex items refuse to shrink below content height
     — cards would expand the panel instead of scrolling inside it */
  min-height: 0;
}

/* ── Scrollable cards list ───────────────────────────── */
.cards-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 16px;
}

/* ── Map panel ───────────────────────────────────────── */
.map-panel {
  flex: 1;
  position: relative;   /* required: map div uses position:absolute;inset:0 */
  min-width: 0;
  min-height: 0;
}

/* ── Leaflet overrides ───────────────────────────────── */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  font-family: 'Inter', sans-serif;
}
:deep(.leaflet-popup-tip) { background: white; }
:deep(.leaflet-control-attribution) { font-size: 10px; }

/* ── Mobile (≤ 767px) ────────────────────────────────── */
@media (max-width: 767px) {
  .services-header {
    padding: 16px 16px 12px;
  }

  .services-header h1 {
    font-size: 20px !important;
    margin-bottom: 12px !important;
  }

  .search-row {
    flex-wrap: wrap;
    gap: 8px;
  }

  /* Stack map on top, cards below */
  .main-panel {
    flex-direction: column;
    height: auto !important;
    overflow: visible;
  }

  .map-panel {
    height: 45vh;
    min-height: 280px;
    order: 1;
    width: 100%;
    /* position:relative already set above — map div fills this via inset:0 */
  }

  .left-panel {
    width: 100%;
    min-width: unset;
    /* No height cap on mobile — cards expand naturally,
       user scrolls the page to see more cards then footer */
    height: auto;
    overflow: visible;
    border-right: none;
    border-top: 1px solid #e8e3da;
    order: 2;
  }

  /* On mobile, cards-scroll expands to full content height */
  .left-panel .cards-scroll {
    overflow: visible;
    height: auto;
    flex: none;
  }
}

/* ── Filters dropdown ────────────────────────────────── */
.filters-dropdown {
  position: relative;
}

.filters-panel {
  display: none;
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: white;
  border: 1px solid #e0dbd2;
  border-radius: 10px;
  padding: 14px 16px;
  min-width: 180px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.11);
  z-index: 1100;  /* above Leaflet's z-index (400–1000 range) */
  white-space: nowrap;
}

/* Show panel on hover of either the button or the panel itself */
.filters-dropdown:hover .filters-panel {
  display: block;
}
</style>
