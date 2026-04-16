<template>
  <div style="font-family:'Inter',sans-serif; display:flex; flex-direction:column; min-height:100vh; background:#fafafa;">
    <LayoutNavbar />

    <!-- ── Search & Filter Header ── -->
    <div ref="headerEl" style="background:#ede8df; padding:28px 40px 20px; border-bottom:1px solid #dfd7c7;">
      <h1 style="font-family:'Noto Serif',serif; font-size:26px; font-weight:700; color:#1a1a1a; text-align:center; margin-bottom:18px;">
        Find Nearby Relief Services
      </h1>

      <!-- Search row -->
      <div style="display:flex; gap:10px; max-width:860px; margin:0 auto 14px;">
        <!-- Input -->
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
          <!-- Clear input -->
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            style="background:none; border:none; cursor:pointer; padding:4px; color:#aaa; display:flex; align-items:center;"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- Search button -->
        <button
          @click="searchByAddress"
          :disabled="!searchQuery.trim()"
          style="background:#2D5016; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif; transition:opacity 0.2s;"
          :style="!searchQuery.trim() ? 'opacity:0.45;cursor:not-allowed;' : ''"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="white" stroke-width="2"/>
            <path d="m21 21-4.35-4.35" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Search
        </button>

        <!-- Locate Me button -->
        <button
          @click="locateMe"
          :disabled="locating"
          style="background:#2D5016; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif; transition:opacity 0.2s;"
          :style="locating ? 'opacity:0.7;cursor:not-allowed;' : ''"
        >
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
          <button
            v-for="tab in CATEGORY_TABS"
            :key="tab.value"
            @click="activeFilter = tab.value"
            style="padding:9px 18px; border:none; cursor:pointer; font-size:14px; font-family:Inter,sans-serif; transition:background 0.15s;"
            :style="{
              fontWeight: activeFilter === tab.value ? '700' : '400',
              color: activeFilter === tab.value ? '#1a1a1a' : '#777',
              background: activeFilter === tab.value ? 'white' : 'transparent',
            }"
          >{{ tab.label }}</button>
        </div>

        <div style="display:flex; align-items:center; gap:14px; margin-left:auto;">
          <label style="display:flex; align-items:center; gap:6px; font-size:14px; cursor:pointer; color:#444; user-select:none;">
            <input type="checkbox" v-model="openNowFilter" style="width:15px; height:15px; accent-color:#2D5016;" />
            Open Now
          </label>
          <button style="border:1px solid #ccc; background:white; border-radius:6px; padding:8px 14px; font-size:14px; cursor:pointer; display:flex; align-items:center; gap:6px; color:#444; font-family:Inter,sans-serif;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <line x1="4" y1="6" x2="20" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="7" y1="12" x2="17" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="10" y1="18" x2="14" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            Filters
          </button>
        </div>
      </div>
    </div>

    <!-- ── Main: Cards + Map ── -->
    <div :style="{ display:'flex', flex:'1', height:mainHeight, overflow:'hidden' }">

      <!-- ── Cards Panel ── -->
      <div style="width:390px; min-width:340px; overflow-y:auto; background:#fafafa; border-right:1px solid #e8e3da; position:relative;">

        <!-- ── In-page Directions Panel (v-show keeps DOM alive for setPanel) ── -->
        <div v-show="showingDirections" style="display:flex; flex-direction:column; height:100%; overflow-y:auto;">
          <!-- Back button -->
          <div style="padding:14px 16px 0; flex-shrink:0;">
            <button
              @click="clearDirections"
              style="display:inline-flex; align-items:center; gap:6px; background:none; border:none; cursor:pointer; font-size:14px; font-weight:600; color:#2D5016; font-family:Inter,sans-serif; padding:0; margin-bottom:12px;"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Back to results
            </button>

            <!-- Route summary card -->
            <div v-if="directionsInfo" style="background:white; border:1px solid #e8e3da; border-radius:12px; padding:16px; margin-bottom:14px;">
              <p style="font-size:11px; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">Directions to</p>
              <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:12px; line-height:1.3;">{{ directionsInfo.service }}</p>
              <div style="display:flex; gap:20px;">
                <div style="display:flex; align-items:center; gap:7px;">
                  <div style="width:32px; height:32px; background:#f0f5ec; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
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
                <div style="display:flex; align-items:center; gap:7px;">
                  <div style="width:32px; height:32px; background:#f0f5ec; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
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

          <!-- Google-rendered steps injected here -->
          <div ref="directionsPanelEl" class="directions-steps" style="padding:0 16px 24px; flex:1;"></div>
        </div>

        <!-- ── Services list (hidden while directions showing) ── -->
        <div v-show="!showingDirections" style="padding:16px;">

          <!-- Result count -->
          <p v-if="locationLabel && !loading" style="font-size:13px; color:#888; margin-bottom:12px; padding:0 2px;">
            <strong style="color:#555;">{{ filteredServices.length }}</strong>
            {{ filteredServices.length === 1 ? 'service' : 'services' }} near
            <strong style="color:#555;">{{ locationLabel }}</strong>
          </p>

          <!-- Loading skeletons -->
          <div v-if="loading">
            <div v-for="i in 3" :key="i" style="background:white; border:1px solid #e8e3da; border-radius:12px; padding:18px; margin-bottom:12px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <div style="height:22px; width:130px; background:#f0ede8; border-radius:20px;"></div>
                <div style="height:22px; width:100px; background:#f0ede8; border-radius:20px;"></div>
              </div>
              <div style="height:18px; background:#f0ede8; border-radius:4px; margin-bottom:8px; width:75%;"></div>
              <div style="height:14px; background:#f0ede8; border-radius:4px; margin-bottom:6px;"></div>
              <div style="height:14px; background:#f0ede8; border-radius:4px; width:60%;"></div>
            </div>
          </div>

          <!-- No location yet -->
          <div v-else-if="!userLocation" style="padding:40px 8px; text-align:center; color:#999;">
            <div style="width:52px; height:52px; background:#f0f5ec; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 16px;">
              <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="#2D5016"/>
              </svg>
            </div>
            <p style="font-size:15px; font-weight:600; color:#444; margin-bottom:6px;">Enter your location</p>
            <p style="font-size:13px; line-height:1.6;">Search a suburb or postcode, or tap <strong>Locate Me</strong> to find services near you.</p>
          </div>

          <!-- Empty results -->
          <div v-else-if="filteredServices.length === 0" style="padding:40px 8px; text-align:center; color:#999;">
            <p style="font-size:15px; font-weight:600; color:#444; margin-bottom:6px;">No services found</p>
            <p style="font-size:13px;">Try a different location or adjust your filters.</p>
          </div>

          <!-- Service Cards -->
          <div v-else>
            <div
              v-for="service in filteredServices"
              :key="service.id"
              style="background:white; border-radius:12px; padding:18px; margin-bottom:12px; cursor:pointer; transition:box-shadow 0.2s, border-color 0.2s;"
              :style="{
                border: selectedService?.id === service.id ? '2px solid #2D5016' : '1px solid #e8e3da',
                boxShadow: selectedService?.id === service.id ? '0 2px 14px rgba(45,80,22,0.13)' : '0 1px 3px rgba(0,0,0,0.04)',
              }"
              @click="selectService(service)"
            >
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

              <!-- Name -->
              <h3 style="font-size:17px; font-weight:700; color:#1a1a1a; margin-bottom:6px; line-height:1.3;">
                {{ service.name }}
              </h3>

              <!-- Description -->
              <p style="font-size:13px; color:#555; line-height:1.6; margin-bottom:12px; overflow:hidden; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;">
                {{ service.description || service.target_audience }}
              </p>

              <!-- Info row -->
              <div style="display:flex; gap:16px; flex-wrap:wrap; margin-bottom:12px;">
                <span v-if="getHoursDisplay(service)" style="display:flex; align-items:center; gap:5px; font-size:12px; color:#666;">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="#888" stroke-width="2"/>
                    <path d="M12 7v5l3 3" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
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

              <!-- Action row: Get Directions -->
              <div style="display:flex; gap:8px; padding-top:10px; border-top:1px solid #f0ece6;">
                <button
                  @click.stop="getDirections(service)"
                  :disabled="!userLocation"
                  style="flex:1; display:flex; align-items:center; justify-content:center; gap:6px; padding:8px 12px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; transition:all 0.15s; font-family:Inter,sans-serif;"
                  :style="userLocation
                    ? 'background:#f0f5ec; color:#2D5016; border:1.5px solid #2D5016;'
                    : 'background:#f5f5f5; color:#aaa; border:1.5px solid #ddd; cursor:not-allowed;'"
                  :title="userLocation ? 'Show route on map' : 'Enter your location first'"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M3 11l19-9-9 19-2-8-8-2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
                  </svg>
                  Get Directions
                </button>

                <a
                  v-if="service.address"
                  :href="`https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(service.address)}`"
                  target="_blank"
                  rel="noopener"
                  @click.stop
                  style="display:flex; align-items:center; justify-content:center; gap:6px; padding:8px 12px; border-radius:8px; font-size:13px; font-weight:600; cursor:pointer; transition:all 0.15s; font-family:Inter,sans-serif; text-decoration:none; border:1.5px solid #ddd; background:white; color:#555;"
                  title="Open in Google Maps"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M15 3h6v6M10 14 21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Open Maps
                </a>
              </div>
            </div>
          </div>

        </div>
        <!-- end services list -->
      </div>

      <!-- ── Map Panel ── -->
      <div style="flex:1; position:relative; background:#e8e5e0;">
        <div ref="mapEl" style="width:100%; height:100%;"></div>

        <!-- Directions info bar -->
        <div
          v-if="directionsInfo"
          style="position:absolute; bottom:16px; left:50%; transform:translateX(-50%); background:white; border-radius:12px; padding:12px 18px; box-shadow:0 4px 20px rgba(0,0,0,0.18); display:flex; align-items:center; gap:14px; z-index:10; white-space:nowrap;"
        >
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
          <button
            @click="clearDirections"
            style="width:30px; height:30px; border-radius:50%; border:1.5px solid #ddd; background:white; cursor:pointer; display:flex; align-items:center; justify-content:center; flex-shrink:0; color:#666;"
            title="Clear route"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
              <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <!-- No location overlay -->
        <div
          v-if="!userLocation && !loading && mapReady"
          style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:white; border-radius:14px; padding:28px 36px; box-shadow:0 4px 24px rgba(0,0,0,0.15); text-align:center; max-width:280px; z-index:10;"
        >
          <div style="width:52px; height:52px; background:#f0f5ec; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 14px;">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="#2D5016"/>
            </svg>
          </div>
          <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:8px;">Find help near you</p>
          <p style="font-size:13px; color:#777; margin-bottom:18px; line-height:1.55;">Enter a suburb or postcode, or share your location to find services.</p>
          <button
            @click="locateMe"
            style="background:#2D5016; color:white; border:none; border-radius:8px; padding:10px 22px; font-size:14px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; width:100%;"
          >
            Use My Location
          </button>
        </div>

        <!-- Map loading -->
        <div v-if="!mapReady" style="position:absolute; inset:0; display:flex; align-items:center; justify-content:center; background:#e8e5e0;">
          <p style="color:#888; font-size:14px;">Loading map…</p>
        </div>

        <!-- No API key -->
        <div v-if="mapError" style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#f5f3ef; text-align:center; padding:24px;">
          <div style="width:52px; height:52px; background:#fff3cd; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-bottom:14px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 19h20L12 2z" stroke="#856404" stroke-width="2" stroke-linejoin="round"/>
              <path d="M12 9v5M12 17v1" stroke="#856404" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <p style="font-weight:700; color:#444; margin-bottom:6px;">Map unavailable</p>
          <p style="font-size:13px; color:#888; max-width:240px; line-height:1.6;">Add your Google Maps API key to <code style="background:#f0f0f0; padding:2px 6px; border-radius:4px;">.env</code> to enable the map.</p>
        </div>
      </div>
    </div>

    <LayoutFooter />
  </div>
</template>

<script setup>
// ── Constants ──────────────────────────────────────────────────────────────
const CATEGORY_TABS = [
  { value: 'both', label: 'Show Both' },
  { value: 'food', label: 'Food Aid' },
  { value: 'housing', label: 'Housing Relief' },
]

const MOCK_SERVICES = [
  {
    id: 1,
    name: 'Foodbank Victoria',
    description: 'Emergency food hampers and fresh produce for individuals and families experiencing food insecurity. No appointment required during opening hours.',
    target_audience: 'Individuals and families',
    address: '2 Coventry St, Southbank VIC 3006',
    suburb: 'Southbank',
    primary_phone: '(03) 9362 8400',
    website: 'https://www.foodbank.org.au/',
    categories: ['Food Bank', 'Emergency Relief'],
    latitude: -37.8248, longitude: 144.9572,
    nearest_train_station: 'Flinders St. (8 min walk)',
    opening_hours: { monday: '9:00am - 5:00pm', tuesday: '9:00am - 5:00pm', wednesday: '9:00am - 5:00pm', thursday: '9:00am - 5:00pm', friday: '9:00am - 5:00pm' },
    is_open_now: true, distance_km: 0.8,
  },
  {
    id: 2,
    name: 'Melbourne City Mission',
    description: 'Emergency accommodation, food parcels and support services for people experiencing homelessness and hardship in Melbourne.',
    target_audience: 'People experiencing homelessness',
    address: 'Level 1/110 Victoria Parade, Collingwood VIC 3066',
    suburb: 'Collingwood',
    primary_phone: '(03) 9929 9889',
    website: 'https://www.mcm.org.au/',
    categories: ['Housing Service', 'Emergency Shelter'],
    latitude: -37.8032, longitude: 144.9792,
    nearest_train_station: 'Collingwood (5 min walk)',
    opening_hours: { monday: '24 hours', tuesday: '24 hours', wednesday: '24 hours', thursday: '24 hours', friday: '24 hours', saturday: '24 hours', sunday: '24 hours' },
    is_open_now: true, beds_available: 12, distance_km: 1.2,
  },
  {
    id: 3,
    name: 'The Salvation Army Melbourne',
    description: 'Food parcels, non-perishable pantry items, fresh produce and frozen meals available. Emergency financial assistance also offered.',
    target_audience: 'Individuals and families in need',
    address: '69 Bourke St, Melbourne VIC 3000',
    suburb: 'Melbourne',
    primary_phone: '(03) 9653 3300',
    website: 'https://www.salvationarmy.org.au/',
    categories: ['Food Bank', 'Emergency Relief'],
    latitude: -37.8123, longitude: 144.9647,
    nearest_train_station: 'Melbourne Central (3 min walk)',
    opening_hours: { monday: '10:00am - 3:00pm', tuesday: '10:00am - 3:00pm', wednesday: '10:00am - 3:00pm', thursday: '10:00am - 3:00pm', friday: '10:00am - 2:00pm' },
    is_open_now: true, distance_km: 0.3,
  },
  {
    id: 4,
    name: 'Wintringham Housing',
    description: 'Secure housing and specialist support services for older people who are homeless or at risk of homelessness.',
    target_audience: 'Older people (50+) experiencing homelessness',
    address: '141 Nicholson St, Carlton VIC 3053',
    suburb: 'Carlton',
    primary_phone: '(03) 9349 2300',
    website: 'https://www.wintringham.org.au/',
    categories: ['Housing Service', 'Aged Care'],
    latitude: -37.7989, longitude: 144.9669,
    nearest_train_station: 'Melbourne Central (8 min walk)',
    opening_hours: { monday: '9:00am - 5:00pm', tuesday: '9:00am - 5:00pm', wednesday: '9:00am - 5:00pm', thursday: '9:00am - 5:00pm', friday: '9:00am - 5:00pm' },
    is_open_now: true, beds_available: 8, distance_km: 2.1,
  },
  {
    id: 5,
    name: 'St Vincent de Paul – Melbourne Central',
    description: 'Free meals, food parcels, clothing and emergency financial assistance. Serving people in need with dignity and respect.',
    target_audience: 'General community',
    address: '43 Abbotsford St, North Melbourne VIC 3051',
    suburb: 'North Melbourne',
    primary_phone: '(03) 9329 8522',
    website: 'https://www.vinnies.org.au/',
    categories: ['Food Bank', 'Community Meal'],
    latitude: -37.7985, longitude: 144.9438,
    nearest_train_station: 'North Melbourne (6 min walk)',
    opening_hours: { monday: '9:00am - 4:30pm', tuesday: '9:00am - 4:30pm', wednesday: '9:00am - 4:30pm', thursday: '9:00am - 4:30pm', friday: '9:00am - 4:30pm' },
    is_open_now: true, distance_km: 2.8,
  },
  {
    id: 6,
    name: 'Launch Housing – Emergency',
    description: 'Crisis and emergency housing support, rough sleeper outreach, transitional housing and case management across Melbourne.',
    target_audience: 'People experiencing homelessness',
    address: '111 Sturt St, Southbank VIC 3006',
    suburb: 'Southbank',
    primary_phone: '(03) 8610 0800',
    website: 'https://www.launchhousing.org.au/',
    categories: ['Housing Service', 'Homelessness Support'],
    latitude: -37.8225, longitude: 144.9592,
    nearest_train_station: 'Flinders St. (10 min walk)',
    opening_hours: { monday: '9:00am - 5:00pm', tuesday: '9:00am - 5:00pm', wednesday: '9:00am - 5:00pm', thursday: '9:00am - 5:00pm', friday: '9:00am - 5:00pm' },
    is_open_now: false, distance_km: 1.0,
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
const mapReady = ref(false)
const mapError = ref(false)
const services = ref([])
const selectedService = ref(null)
const userLocation = ref(null)   // { lat, lon }
const locationLabel = ref('')
const mainHeight = ref('600px')
const directionsInfo = ref(null)    // { service, distance, duration }
const showingDirections = ref(false)
const directionsPanelEl = ref(null) // DOM node where Google renders steps

let mapInstance = null
let markersMap = {}
let infoWindow = null
let userMarker = null
let directionsRenderer = null

const config = useRuntimeConfig()
const MAPS_KEY = config.public.googleMapsKey
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
  if (s.is_open_now === true) {
    const closing = getClosingTime(s)
    return closing ? `Open Until ${closing}` : 'Open Now'
  }
  if (s.is_open_now === false) return 'Closed'
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
  const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
  const hours = s.opening_hours[days[new Date().getDay()]]
  if (!hours || typeof hours !== 'string') return null
  const m = hours.match(/[-–]\s*(\d+(?::\d+)?\s*(?:am|pm))/i)
  return m ? m[1].replace(':00', '').toUpperCase() : null
}

function getHoursDisplay(s) {
  if (s.opening_hours_display) return s.opening_hours_display
  if (!s.opening_hours) return null
  const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
  return s.opening_hours[days[new Date().getDay()]] || null
}

// ── API ────────────────────────────────────────────────────────────────────
async function fetchNearby(lat, lon) {
  loading.value = true
  try {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone
    const params = new URLSearchParams({ lat, lon, radius_km: '10', limit: '50', tz })
    const res = await fetch(`${API_BASE}/nearby?${params}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    services.value = data.length ? data : MOCK_SERVICES
  } catch {
    services.value = MOCK_SERVICES
  } finally {
    loading.value = false
    await nextTick()
    updateMapMarkers()
  }
}

// ── Geolocation ────────────────────────────────────────────────────────────
function locateMe() {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.')
    return
  }
  locating.value = true
  navigator.geolocation.getCurrentPosition(
    ({ coords: { latitude: lat, longitude: lon } }) => {
      locating.value = false
      userLocation.value = { lat, lon }
      locationLabel.value = 'your location'
      centerMap(lat, lon, 13)
      placeUserMarker(lat, lon)
      fetchNearby(lat, lon)
    },
    () => { locating.value = false },
    { timeout: 10000 }
  )
}

// ── Address search ─────────────────────────────────────────────────────────
async function searchByAddress() {
  const q = searchQuery.value.trim()
  if (!q) return

  // If Maps not loaded, fall back to mock data at Melbourne
  if (!window.google?.maps) {
    userLocation.value = { lat: -37.8136, lon: 144.9631 }
    locationLabel.value = q
    services.value = MOCK_SERVICES
    return
  }

  loading.value = true
  clearDirections()

  try {
    const geocoder = new window.google.maps.Geocoder()
    const { results } = await geocoder.geocode({ address: `${q}, Victoria, Australia` })
    if (!results.length) throw new Error('No results')

    const loc = results[0].geometry.location
    const lat = loc.lat()
    const lon = loc.lng()

    userLocation.value = { lat, lon }
    locationLabel.value = results[0].address_components?.[0]?.long_name || q
    centerMap(lat, lon, 13)
    placeUserMarker(lat, lon)
    fetchNearby(lat, lon)
  } catch {
    loading.value = false
  }
}

// ── Map helpers ────────────────────────────────────────────────────────────
function centerMap(lat, lon, zoom = 13) {
  mapInstance?.setCenter({ lat, lng: lon })
  mapInstance?.setZoom(zoom)
}

function placeUserMarker(lat, lon) {
  if (!mapInstance || !window.google) return
  userMarker?.setMap(null)
  userMarker = new window.google.maps.Marker({
    position: { lat, lng: lon },
    map: mapInstance,
    title: 'Your location',
    icon: {
      path: window.google.maps.SymbolPath.CIRCLE,
      scale: 9,
      fillColor: '#2D5016',
      fillOpacity: 1,
      strokeColor: 'white',
      strokeWeight: 3,
    },
    zIndex: 999,
  })
}

function selectService(service) {
  selectedService.value = service
  if (!service.latitude || !service.longitude || !mapInstance) return
  centerMap(service.latitude, service.longitude, 15)
  const marker = markersMap[service.id]
  if (marker && infoWindow) {
    infoWindow.setContent(buildInfoWindowHTML(service))
    infoWindow.open(mapInstance, marker)
  }
}

function buildInfoWindowHTML(s) {
  return `
    <div style="font-family:Inter,sans-serif;padding:4px 2px;max-width:230px;">
      <p style="font-size:13px;font-weight:700;margin:0 0 4px;color:#1a1a1a;line-height:1.3;">${s.name}</p>
      ${s.address ? `<p style="font-size:12px;color:#666;margin:0 0 6px;">${s.address}</p>` : ''}
      ${s.primary_phone ? `<p style="font-size:12px;color:#2D5016;margin:0 0 4px;">${s.primary_phone}</p>` : ''}
      ${s.website ? `<a href="${s.website}" target="_blank" rel="noopener" style="font-size:12px;color:#2D5016;text-decoration:none;">Visit website ↗</a>` : ''}
    </div>
  `
}

// ── Directions ─────────────────────────────────────────────────────────────
async function getDirections(service) {
  if (!userLocation.value || !window.google || !mapInstance) return

  selectedService.value = service

  // Initialise renderer once
  if (!directionsRenderer) {
    directionsRenderer = new window.google.maps.DirectionsRenderer({
      suppressMarkers: true,
      polylineOptions: {
        strokeColor: '#2D5016',
        strokeWeight: 5,
        strokeOpacity: 0.85,
      },
    })
  }
  directionsRenderer.setMap(mapInstance)

  try {
    const dirService = new window.google.maps.DirectionsService()
    const result = await dirService.route({
      origin: { lat: userLocation.value.lat, lng: userLocation.value.lon },
      destination: { lat: service.latitude, lng: service.longitude },
      travelMode: window.google.maps.TravelMode.DRIVING,
    })

    const leg = result.routes[0].legs[0]
    directionsInfo.value = {
      service: service.name,
      distance: leg.distance.text,
      duration: leg.duration.text,
    }

    // Show panel in left column, then wire renderer to DOM node
    showingDirections.value = true
    await nextTick()
    directionsRenderer.setPanel(directionsPanelEl.value)
    directionsRenderer.setDirections(result)
  } catch (err) {
    console.error('Directions failed:', err)
    centerMap(service.latitude, service.longitude, 15)
  }
}

function clearDirections() {
  directionsRenderer?.setPanel(null)
  directionsRenderer?.setMap(null)
  directionsInfo.value = null
  showingDirections.value = false
}

function updateMapMarkers() {
  if (!mapInstance || !window.google) return

  Object.values(markersMap).forEach(m => m.setMap(null))
  markersMap = {}

  if (!infoWindow) infoWindow = new window.google.maps.InfoWindow()

  filteredServices.value.forEach(service => {
    if (!service.latitude || !service.longitude) return

    const housing = isHousing(service)
    const isOpen = service.is_open_now

    const marker = new window.google.maps.Marker({
      position: { lat: service.latitude, lng: service.longitude },
      map: mapInstance,
      title: service.name,
      icon: {
        path: window.google.maps.SymbolPath.CIRCLE,
        scale: 10,
        fillColor: housing ? '#4A7A6D' : '#C07A2A',
        fillOpacity: isOpen === false ? 0.4 : 1,
        strokeColor: 'white',
        strokeWeight: 2.5,
      },
    })

    marker.addListener('click', () => {
      selectedService.value = service
      infoWindow.setContent(buildInfoWindowHTML(service))
      infoWindow.open(mapInstance, marker)
    })

    markersMap[service.id] = marker
  })
}

// Redraw markers on filter change
watch(filteredServices, () => {
  updateMapMarkers()
  clearDirections()
})

// ── Init ───────────────────────────────────────────────────────────────────
function loadGoogleMapsScript() {
  return new Promise((resolve, reject) => {
    if (window.google?.maps) return resolve()
    if (!MAPS_KEY) return reject(new Error('No API key'))
    const s = document.createElement('script')
    s.src = `https://maps.googleapis.com/maps/api/js?key=${MAPS_KEY}&libraries=places`
    s.async = true
    s.defer = true
    s.onload = resolve
    s.onerror = () => reject(new Error('Google Maps failed to load'))
    document.head.appendChild(s)
  })
}

onMounted(async () => {
  await nextTick()
  const navbarH = 86
  const headerH = headerEl.value?.offsetHeight ?? 185
  mainHeight.value = `calc(100vh - ${navbarH + headerH}px)`

  try {
    await loadGoogleMapsScript()
    mapInstance = new window.google.maps.Map(mapEl.value, {
      center: { lat: -37.8136, lng: 144.9631 },
      zoom: 11,
      zoomControl: true,
      streetViewControl: false,
      mapTypeControl: false,
      fullscreenControl: false,
    })
    mapReady.value = true
  } catch (err) {
    console.warn('Google Maps unavailable:', err.message)
    mapReady.value = true
    mapError.value = true
  }
})
</script>

<style scoped>
/* ── Style the Google DirectionsRenderer step-by-step output ── */
.directions-steps :deep(table) {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
}

.directions-steps :deep(tr) {
  border-bottom: 1px solid #f0ece6;
}

.directions-steps :deep(tr:last-child) {
  border-bottom: none;
}

.directions-steps :deep(td) {
  padding: 10px 6px;
  font-size: 13px;
  color: #444;
  vertical-align: top;
  line-height: 1.5;
}

/* Step number column */
.directions-steps :deep(td:first-child) {
  color: #2D5016;
  font-weight: 700;
  font-size: 12px;
  width: 28px;
  padding-top: 11px;
}

/* Distance column */
.directions-steps :deep(td:last-child) {
  color: #888;
  font-size: 12px;
  white-space: nowrap;
  text-align: right;
  padding-top: 11px;
}

/* Route summary row at top (start/end) */
.directions-steps :deep(.adp-placemark td) {
  font-weight: 600;
  color: #1a1a1a;
  padding: 10px 6px;
  background: #f8f6f2;
  border-radius: 6px;
}

/* Hide Google's default header/footer text */
.directions-steps :deep(.adp-legal),
.directions-steps :deep(.adp-text) {
  display: none;
}
</style>
