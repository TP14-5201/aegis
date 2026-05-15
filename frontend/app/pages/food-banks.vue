<template>
  <div class="page-wrap">
    <TopNavigation />
    <div class="h-[72px] lg:h-[100px]" />

    <!-- ── Search & Filter Header ── -->
    <div ref="headerEl" class="page-header">
      <h1
        class="text-center font-volkhov font-bold text-navy
              text-[24px] sm:text-[28px] lg:text-[32px]
              mb-4 lg:mb-5"
      >
        Find Nearby Food Banks
      </h1>

      <!-- Search row -->
      <div class="search-row">
        <div style="flex:1; position:relative;">
          <div style="display:flex; align-items:center; background:white; border:1.5px solid #b8d9f8; border-radius:10px; padding:0 16px; gap:10px;">
            <svg width="18" height="18" fill="none" viewBox="0 0 24 24" style="flex-shrink:0;">
              <circle cx="11" cy="11" r="8" stroke="#9ca3af" stroke-width="2"/>
              <path d="m21 21-4.35-4.35" stroke="#9ca3af" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <input
              ref="searchInputEl"
              v-model="searchQuery"
              type="text"
              placeholder="Enter an address or suburb to find nearby food banks"
              style="flex:1; border:none; outline:none; font-size:15px; color:#333; height:48px; background:transparent; font-family:Inter,sans-serif;"
              @keydown.enter="searchByAddress"
              @input="onSearchInput"
              @blur="hideSuggestionsDelayed"
            />
            <button v-if="searchQuery" @click="searchQuery = ''; addressSuggestions = []; showSuggestions = false"
              style="background:none; border:none; cursor:pointer; padding:4px; color:#aaa; display:flex; align-items:center;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Autocomplete suggestions dropdown -->
          <div v-if="showSuggestions && addressSuggestions.length"
            style="position:absolute; top:calc(100% + 4px); left:0; right:0; background:white;
                   border:1.5px solid #b8d9f8; border-radius:10px; z-index:1200;
                   box-shadow:0 4px 16px rgba(0,0,0,0.10); overflow:hidden;">
            <div v-for="(s, i) in addressSuggestions" :key="s.place_id"
              @mousedown.prevent="selectSuggestion(s)"
              style="padding:11px 16px; cursor:pointer; font-size:14px; color:#333; font-family:Inter,sans-serif;
                     display:flex; align-items:center; gap:10px;"
              :style="i < addressSuggestions.length - 1 ? 'border-bottom:1px solid #f0f4ff;' : ''">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" style="flex-shrink:0; color:#9ca3af;">
                <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
              {{ s.description }}
            </div>
          </div>
        </div>

        <!-- Search button -->
        <button @click="searchByAddress" :disabled="!searchQuery.trim()"
          style="background:#181e4b; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif;"
          :style="!searchQuery.trim() ? 'opacity:0.45;cursor:not-allowed;' : ''">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="white" stroke-width="2"/>
            <path d="m21 21-4.35-4.35" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          Search
        </button>

        <!-- Locate Me button -->
        <button @click="locateMe" :disabled="locating"
          style="background:#181e4b; color:white; border:none; border-radius:10px; padding:0 20px; font-size:14px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:8px; white-space:nowrap; font-family:Inter,sans-serif;"
          :style="locating ? 'opacity:0.7;cursor:not-allowed;' : ''">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="3" stroke="white" stroke-width="2"/>
            <path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
          {{ locating ? 'Locating…' : 'Locate Me' }}
        </button>
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
              style="display:inline-flex; align-items:center; gap:6px; background:none; border:none; cursor:pointer; font-size:14px; font-weight:600; color:#0298C5; font-family:Inter,sans-serif; padding:0; margin-bottom:12px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Back to results
            </button>

            <!-- Drive / Transit mode toggle -->
            <div style="display:flex; gap:8px; margin-bottom:12px;">
              <button @click="setRouteMode('drive')"
                :style="routeMode === 'drive'
                  ? 'background:#181e4b; color:white; border:none;'
                  : 'background:white; color:#181e4b; border:1.5px solid #181e4b;'"
                style="flex:1; border-radius:8px; padding:9px 8px; font-size:13px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; display:flex; align-items:center; justify-content:center; gap:6px;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                  <path d="M5 17H3a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h13l4 4v6a2 2 0 0 1-2 2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="7.5" cy="17.5" r="2.5" stroke="currentColor" stroke-width="2"/>
                  <circle cx="17.5" cy="17.5" r="2.5" stroke="currentColor" stroke-width="2"/>
                </svg>
                Drive
              </button>
              <button @click="setRouteMode('transit')"
                :style="routeMode === 'transit'
                  ? 'background:#181e4b; color:white; border:none;'
                  : 'background:white; color:#181e4b; border:1.5px solid #181e4b;'"
                style="flex:1; border-radius:8px; padding:9px 8px; font-size:13px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; display:flex; align-items:center; justify-content:center; gap:6px;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="2" width="18" height="14" rx="3" stroke="currentColor" stroke-width="2"/>
                  <path d="M7 16v3M17 16v3M3 9h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="7.5" cy="12.5" r="1" fill="currentColor"/>
                  <circle cx="16.5" cy="12.5" r="1" fill="currentColor"/>
                </svg>
                Transit
              </button>
              <button @click="setRouteMode('walk')"
                :style="routeMode === 'walk'
                  ? 'background:#181e4b; color:white; border:none;'
                  : 'background:white; color:#181e4b; border:1.5px solid #181e4b;'"
                style="flex:1; border-radius:8px; padding:9px 8px; font-size:13px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; display:flex; align-items:center; justify-content:center; gap:6px;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                  <circle cx="13" cy="4" r="2" fill="currentColor"/>
                  <path d="M13 6L11 13M12 8L9 10M12 8L15 9M11 13L14 20M11 13L8 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Walk
              </button>
            </div>

            <!-- Drive: route summary -->
            <div v-if="routeMode === 'drive' && directionsInfo" style="background:white; border:1px solid #D8EDFF; border-radius:12px; padding:16px; margin-bottom:14px;">
              <p style="font-size:11px; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">Directions to</p>
              <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:14px; line-height:1.3;">{{ directionsInfo.service }}</p>
              <div style="display:flex; gap:20px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#D8EDFF; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#0298C5" stroke-width="2"/>
                      <circle cx="12" cy="10" r="3" stroke="#0298C5" stroke-width="2"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#0298C5; margin:0; line-height:1;">{{ directionsInfo.distance }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">distance</p>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#D8EDFF; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="#0298C5" stroke-width="2"/>
                      <path d="M12 7v5l3 3" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#0298C5; margin:0; line-height:1;">{{ directionsInfo.duration }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">by car</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Transit: route summary -->
            <div v-if="routeMode === 'transit' && transitInfo" style="background:white; border:1px solid #D8EDFF; border-radius:12px; padding:16px; margin-bottom:14px;">
              <p style="font-size:11px; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">Public transport to</p>
              <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:14px; line-height:1.3;">{{ transitInfo.service }}</p>
              <div style="display:flex; gap:20px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#D8EDFF; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="#0298C5" stroke-width="2"/>
                      <path d="M12 7v5l3 3" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#0298C5; margin:0; line-height:1;">{{ transitInfo.duration }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">by public transport</p>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#D8EDFF; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#0298C5" stroke-width="2"/>
                      <circle cx="12" cy="10" r="3" stroke="#0298C5" stroke-width="2"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#0298C5; margin:0; line-height:1;">{{ transitInfo.distance }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">distance</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Walk: route summary -->
            <div v-if="routeMode === 'walk' && walkInfo" style="background:white; border:1px solid #e8f0eb; border-radius:12px; padding:16px; margin-bottom:14px;">
              <p style="font-size:11px; font-weight:700; color:#888; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">Walking route to</p>
              <p style="font-size:15px; font-weight:700; color:#1a1a1a; margin-bottom:14px; line-height:1.3;">{{ walkInfo.service }}</p>
              <div style="display:flex; gap:20px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#eaf3ec; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="#2e7d32" stroke-width="2"/>
                      <path d="M12 7v5l3 3" stroke="#2e7d32" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#2e7d32; margin:0; line-height:1;">{{ walkInfo.duration }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">on foot</p>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                  <div style="width:32px; height:32px; background:#eaf3ec; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#2e7d32" stroke-width="2"/>
                      <circle cx="12" cy="10" r="3" stroke="#2e7d32" stroke-width="2"/>
                    </svg>
                  </div>
                  <div>
                    <p style="font-size:17px; font-weight:800; color:#2e7d32; margin:0; line-height:1;">{{ walkInfo.distance }}</p>
                    <p style="font-size:11px; color:#888; margin:0;">distance</p>
                  </div>
                </div>
              </div>
            </div>

            <p style="font-size:11px; font-weight:700; color:#aaa; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">Step-by-step</p>
          </div>

          <!-- Step list -->
          <div class="cards-scroll" style="padding:0 16px 24px;">
            <div v-if="directionsLoading" style="padding:20px 0; text-align:center; color:#aaa; font-size:14px;">
              Calculating route…
            </div>
            <div v-else>
              <!-- Drive steps -->
              <template v-if="routeMode === 'drive'">
                <div v-for="(step, i) in directionsSteps" :key="i"
                  style="display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px solid #e8f0fb;">
                  <div style="width:28px; height:28px; background:#D8EDFF; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                      <path :d="step.iconPath" stroke="#0298C5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <div style="flex:1;">
                    <p style="font-size:13px; color:#333; margin:0 0 2px; line-height:1.4;">{{ step.instruction }}</p>
                    <p style="font-size:12px; color:#aaa; margin:0;">{{ step.distance }}</p>
                  </div>
                </div>
              </template>

              <!-- Transit steps -->
              <template v-if="routeMode === 'transit'">
                <div v-if="transitLegs.length === 0 && !directionsLoading"
                  style="padding:20px 0; text-align:center; color:#aaa; font-size:14px;">
                  No public transport route found.
                </div>
                <div v-for="(leg, i) in transitLegs" :key="i"
                  style="display:flex; align-items:flex-start; gap:10px; padding:12px 0; border-bottom:1px solid #e8f0fb;">
                  <!-- Mode icon -->
                  <div :style="`width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; background:${transitLegBg(leg.mode)};`">
                    <svg v-if="leg.mode === 'walk'" width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M13 4a1 1 0 1 0 2 0 1 1 0 0 0-2 0M6 20l4-8 2 3 2-2 4 7" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <svg v-else-if="leg.mode === 'train'" width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <rect x="3" y="2" width="18" height="14" rx="3" stroke="#0298C5" stroke-width="2"/>
                      <path d="M3 9h18M7 16v3M17 16v3" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                      <circle cx="7.5" cy="12.5" r="1" fill="#0298C5"/>
                      <circle cx="16.5" cy="12.5" r="1" fill="#0298C5"/>
                    </svg>
                    <svg v-else-if="leg.mode === 'tram'" width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M8 2h8M12 2v2" stroke="#2e7d32" stroke-width="2" stroke-linecap="round"/>
                      <rect x="4" y="4" width="16" height="13" rx="2" stroke="#2e7d32" stroke-width="2"/>
                      <path d="M4 11h16M8 17v3M16 17v3" stroke="#2e7d32" stroke-width="2" stroke-linecap="round"/>
                      <circle cx="8.5" cy="14.5" r="1" fill="#2e7d32"/>
                      <circle cx="15.5" cy="14.5" r="1" fill="#2e7d32"/>
                    </svg>
                    <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path d="M2 17h2m16 0h2M1 11l2-6h18l2 6v4a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-4z" stroke="#e65100" stroke-width="2" stroke-linecap="round"/>
                      <circle cx="6" cy="17" r="2" stroke="#e65100" stroke-width="2"/>
                      <circle cx="18" cy="17" r="2" stroke="#e65100" stroke-width="2"/>
                    </svg>
                  </div>

                  <!-- Leg details -->
                  <div style="flex:1;">
                    <template v-if="leg.mode === 'walk'">
                      <p style="font-size:11px; font-weight:700; color:#4a5568; text-transform:uppercase; letter-spacing:0.7px; margin:0 0 3px;">Walk</p>
                      <p style="font-size:13px; color:#333; margin:0 0 3px; line-height:1.4;">{{ leg.instructions }}</p>
                      <p style="font-size:12px; color:#555; margin:0; font-weight:500;">{{ leg.distance }} · {{ leg.duration }}</p>
                    </template>
                    <template v-else>
                      <p v-if="leg.route_name" style="font-size:13px; font-weight:600; margin:0 0 3px; line-height:1.3;"
                        :style="`color:${transitLegColor(leg.mode)}`">
                        {{ leg.route_name }}
                      </p>
                      <p v-if="leg.from_name || leg.to_name" style="font-size:12px; color:#333; margin:0 0 2px; line-height:1.4;">
                        <span v-if="leg.from_name" style="color:#555; font-weight:500;">{{ leg.from_name }}</span>
                        <span v-if="leg.from_name && leg.to_name" style="color:#aaa;"> → </span>
                        <span v-if="leg.to_name" style="color:#555; font-weight:500;">{{ leg.to_name }}</span>
                      </p>
                      <p style="font-size:12px; color:#888; margin:0;">
                        <span v-if="leg.depart">Depart {{ leg.depart }} · </span>
                        <span v-if="leg.num_stops != null">{{ leg.num_stops }} stop{{ leg.num_stops !== 1 ? 's' : '' }} · </span>
                        <span v-if="leg.duration">{{ leg.duration }}</span>
                        <span v-if="leg.instructions && !leg.from_name">{{ leg.instructions }}</span>
                      </p>
                    </template>
                  </div>
                </div>

                <!-- Live vehicles notice -->
                <div v-if="transitLegs.length > 0" style="margin-top:12px; padding:10px 12px; background:#f0f8ff; border-radius:8px; border:1px solid #D8EDFF; display:flex; align-items:center; gap:8px;">
                  <span style="width:8px; height:8px; border-radius:50%; background:#0298C5; flex-shrink:0; animation:pulse 1.5s infinite;"></span>
                  <p style="font-size:12px; color:#555; margin:0; line-height:1.4;">Live vehicle positions updating every 30 seconds</p>
                </div>
              </template>

              <!-- Walk steps -->
              <template v-if="routeMode === 'walk'">
                <div v-if="walkLegs.length === 0 && !directionsLoading"
                  style="padding:20px 0; text-align:center; color:#aaa; font-size:14px;">
                  No walking route found.
                </div>
                <div v-for="(step, i) in walkLegs" :key="i"
                  style="display:flex; align-items:flex-start; gap:10px; padding:12px 0; border-bottom:1px solid #e8f0fb;">
                  <div style="width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; background:#eaf3ec;">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
                      <path :d="step.iconPath" stroke="#2e7d32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <div style="flex:1;">
                    <p style="font-size:13px; color:#333; margin:0 0 3px; line-height:1.4;">{{ step.instruction }}</p>
                    <p style="font-size:12px; color:#555; margin:0; font-weight:500;">{{ step.distance }}</p>
                  </div>
                </div>
                <div v-if="walkLegs.length > 0" style="margin-top:12px; padding:10px 12px; background:#f1f8f2; border-radius:8px; border:1px solid #c8e6c9; display:flex; align-items:center; gap:8px;">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                    <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#2e7d32" stroke-width="2"/>
                    <circle cx="12" cy="10" r="3" stroke="#2e7d32" stroke-width="2"/>
                  </svg>
                  <p style="font-size:12px; color:#2e7d32; margin:0; line-height:1.4; font-weight:500;">Safe walking route via Google Maps</p>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- ── Services List ── -->
        <div v-show="!showingDirections" class="cards-scroll">

          <!-- Result count -->
          <p v-if="!loading" style="font-size:13px; color:#888; margin-bottom:12px; padding:0 2px;">
            <strong style="color:#555;">{{ filteredServices.length }}</strong> {{ filteredServices.length === 1 ? 'service' : 'services' }} found
            <span v-if="locationLabel"> · near <strong style="color:#555;">{{ locationLabel }}</strong></span>
            <span v-else> across Victoria</span>
          </p>

          <!-- Loading skeletons -->
          <div v-if="loading">
            <div v-for="i in 4" :key="i" style="background:white; border:1px solid #D8EDFF; border-radius:12px; padding:18px; margin-bottom:12px;">
              <div style="height:22px; width:130px; background:#e8f0fb; border-radius:20px; margin-bottom:12px;"></div>
              <div style="height:18px; background:#e8f0fb; border-radius:4px; margin-bottom:8px; width:75%;"></div>
              <div style="height:14px; background:#e8f0fb; border-radius:4px; margin-bottom:6px;"></div>
              <div style="height:14px; background:#e8f0fb; border-radius:4px; width:60%;"></div>
            </div>
          </div>

          <!-- Empty -->
          <div v-else-if="filteredServices.length === 0" style="padding:40px 8px; text-align:center; color:#999;">
            <p style="font-size:15px; font-weight:600; color:#444; margin-bottom:6px;">No services found</p>
            <p style="font-size:13px;">Try adjusting your filters.</p>
          </div>

          <!-- Service Cards -->
          <div v-else>
            <div v-for="service in visibleServices" :key="service.id"
              style="background:white; border-radius:12px; margin-bottom:10px; overflow:hidden; transition:box-shadow 0.2s, border-color 0.2s;"
              :style="{
                border: selectedService?.id === service.id ? '2px solid #0298C5' : '1px solid #e0edf8',
                boxShadow: selectedService?.id === service.id ? '0 2px 14px rgba(2,152,197,0.13)' : '0 1px 3px rgba(0,0,0,0.04)',
              }">

              <!-- Collapsed row (always visible) -->
              <div style="padding:14px 16px; cursor:pointer;"
                @click="expandedServiceId = expandedServiceId === service.id ? null : service.id; selectService(service)">
                <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:8px;">
                  <div style="flex:1; min-width:0;">
                    <!-- Status + Name -->
                    <div style="display:flex; align-items:center; gap:6px; margin-bottom:5px; flex-wrap:wrap;">
                      <span v-if="getStatusLabel(service)" :style="getStatusBadgeStyle(service)" style="flex-shrink:0;">
                        {{ getStatusLabel(service) }}
                      </span>
                    </div>
                    <h3 style="font-size:15px; font-weight:700; color:#1a1a1a; line-height:1.3; margin:0 0 7px;">{{ service.name }}</h3>
                    <!-- Address -->
                    <div v-if="hasValue(service.address)" style="display:flex; align-items:flex-start; gap:7px; font-size:12px; color:#555; margin-bottom:4px;">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" style="flex-shrink:0; margin-top:1px;">
                        <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z" stroke="#0298C5" stroke-width="2"/>
                        <circle cx="12" cy="10" r="3" stroke="#0298C5" stroke-width="2"/>
                      </svg>
                      <span>{{ service.address }}</span>
                    </div>
                    <!-- Phone or website -->
                    <div v-if="hasValue(service.primary_phone)" style="display:flex; align-items:center; gap:7px; font-size:12px; color:#555;">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.99 12 19.79 19.79 0 0 1 1.92 3.4 2 2 0 0 1 3.9 1.22h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9a16 16 0 0 0 6.29 6.29l1.06-1.06a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                      </svg>
                      <span>{{ service.primary_phone }}</span>
                    </div>
                    <div v-else-if="hasValue(service.website)" style="display:flex; align-items:center; gap:7px; font-size:12px;">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                        <circle cx="12" cy="12" r="10" stroke="#0298C5" stroke-width="2"/>
                        <line x1="2" y1="12" x2="22" y2="12" stroke="#0298C5" stroke-width="2"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke="#0298C5" stroke-width="2"/>
                      </svg>
                      <a :href="service.website" target="_blank" rel="noopener"
                        style="color:#0298C5; text-decoration:none; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:180px;"
                        @click.stop>{{ service.website.replace(/^https?:\/\//, '') }}</a>
                    </div>
                  </div>
                  <!-- Chevron -->
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style="flex-shrink:0; margin-top:2px; transition:transform 0.2s;"
                    :style="expandedServiceId === service.id ? 'transform:rotate(180deg)' : ''">
                    <path d="M6 9l6 6 6-6" stroke="#aaa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </div>

              <!-- Expanded detail panel -->
              <div v-if="expandedServiceId === service.id"
                style="padding:0 16px 14px; border-top:1px solid #f0f4fb;">
                <div style="display:flex; flex-direction:column; gap:7px; margin-top:12px; margin-bottom:14px;">
                  <!-- Description / target audience -->
                  <p v-if="hasValue(service.description) || hasValue(service.target_audience)"
                    style="font-size:13px; color:#555; line-height:1.6; margin:0 0 4px;">
                    {{ hasValue(service.description) ? service.description : service.target_audience }}
                  </p>
                  <div v-if="hasValue(service.target_audience) && hasValue(service.description)" style="display:flex; align-items:center; gap:8px; font-size:13px; color:#525252;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                      <circle cx="12" cy="7" r="4" stroke="#0298C5" stroke-width="2"/>
                    </svg>
                    {{ service.target_audience }}
                  </div>
                  <!-- Phone (if not shown above, show here) -->
                  <div v-if="hasValue(service.primary_phone) && hasValue(service.website)" style="display:flex; align-items:center; gap:8px; font-size:13px; color:#525252;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.99 12 19.79 19.79 0 0 1 1.92 3.4 2 2 0 0 1 3.9 1.22h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9a16 16 0 0 0 6.29 6.29l1.06-1.06a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    {{ service.primary_phone }}
                  </div>
                  <!-- Website (if not shown above) -->
                  <div v-if="hasValue(service.website) && hasValue(service.primary_phone)" style="display:flex; align-items:center; gap:8px; font-size:13px;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                      <circle cx="12" cy="12" r="10" stroke="#0298C5" stroke-width="2"/>
                      <line x1="2" y1="12" x2="22" y2="12" stroke="#0298C5" stroke-width="2"/>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke="#0298C5" stroke-width="2"/>
                    </svg>
                    <a :href="service.website" target="_blank" rel="noopener"
                      style="color:#0298C5; text-decoration:none; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:200px;"
                      @click.stop>{{ service.website.replace(/^https?:\/\//, '') }}</a>
                  </div>
                  <!-- Hours -->
                  <div v-if="getHoursDisplay(service)" style="display:flex; align-items:center; gap:8px; font-size:13px; color:#525252;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">
                      <circle cx="12" cy="12" r="10" stroke="#0298C5" stroke-width="2"/>
                      <path d="M12 7v5l3 3" stroke="#0298C5" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    Open: {{ getHoursDisplay(service) }}
                  </div>
                </div>

                <!-- Get Directions button -->
                <button @click.stop="getDirections(service)" :disabled="!userLocation"
                  style="width:100%; display:flex; align-items:center; justify-content:center; gap:8px; padding:11px; border-radius:10px; font-size:14px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; border:none; transition:opacity 0.15s;"
                  :style="userLocation
                    ? 'background:#0298C5; color:white;'
                    : 'background:#e8f0fb; color:#aaa; cursor:not-allowed;'"
                  :title="userLocation ? 'Show route on map' : 'Enter your location first'">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M3 11l19-9-9 19-2-8-8-2z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
                  </svg>
                  Get Directions
                </button>
              </div>
            </div>

            <!-- Show more -->
            <div v-if="visibleCount < filteredServices.length"
              style="text-align:center; padding:4px 0 8px;">
              <button @click="visibleCount += 10"
                style="background:white; border:1.5px solid #0298C5; color:#0298C5; border-radius:10px; padding:10px 28px; font-size:13px; font-weight:600; cursor:pointer; font-family:Inter,sans-serif; width:100%;">
                Show more ({{ filteredServices.length - visibleCount }} remaining)
              </button>
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
          <div style="width:36px; height:36px; background:#D8EDFF; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M3 11l19-9-9 19-2-8-8-2z" stroke="#0298C5" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <p style="font-size:12px; color:#888; margin:0 0 2px;">Route to</p>
            <p style="font-size:13px; font-weight:700; color:#1a1a1a; margin:0; max-width:200px; overflow:hidden; text-overflow:ellipsis;">{{ directionsInfo.service }}</p>
          </div>
          <div style="border-left:1px solid #e8f0fb; padding-left:14px;">
            <p style="font-size:15px; font-weight:700; color:#0298C5; margin:0;">{{ directionsInfo.distance }}</p>
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
const expandedServiceId = ref(null)
const visibleCount = ref(10)
const userLocation = ref(null)
const locationLabel = ref('')
const mainHeight = ref('600px')
const directionsInfo = ref(null)
const directionsSteps = ref([])
const directionsLoading = ref(false)
const showingDirections = ref(false)

// Transit routing state
const routeMode = ref('drive')
const transitLegs = ref([])
const transitInfo = ref(null)
const walkLegs = ref([])
const walkInfo = ref(null)

// Address autocomplete state
const addressSuggestions = ref([])
const showSuggestions = ref(false)
let acTimer = null

let mapInstance = null
let markersMap = {}
let userMarker = null
let destinationMarker = null
let routeLayer = null
let transitRouteLayers = []
let vehicleMarkers = {}
let vehiclePollTimer = null
let highlightedTripIds = new Set()

// Google Maps service handles
let autocompleteService = null
let placesService = null
let directionsService = null

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

const visibleServices = computed(() => filteredServices.value.slice(0, visibleCount.value))

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
  if (s.beds_available != null) return base + 'background:#D8EDFF;color:#0298C5;'
  if (s.is_open_now === true) return base + 'background:#D8EDFF;color:#0298C5;'
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
  const icon = L.divIcon({
    className: '',
    html: `<div style="position:relative;width:22px;height:22px;">
      <div style="position:absolute;inset:0;border-radius:50%;background:#0298C5;opacity:0.25;animation:userPulse 2s ease-out infinite;"></div>
      <div style="position:absolute;inset:4px;border-radius:50%;background:#0298C5;border:2.5px solid white;box-shadow:0 1px 6px rgba(0,0,0,0.35);"></div>
    </div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11],
  })
  userMarker = L.marker([lat, lon], { icon, zIndexOffset: 1000 })
    .addTo(mapInstance)
    .bindPopup('<strong style="font-family:Inter,sans-serif;">Your location</strong>')
}

function placeDestinationMarker(lat, lon, name) {
  if (!mapInstance) return
  destinationMarker?.remove()
  const icon = L.divIcon({
    className: '',
    html: `<div style="position:relative;width:28px;height:36px;">
      <svg viewBox="0 0 28 36" width="28" height="36" xmlns="http://www.w3.org/2000/svg">
        <path d="M14 0C6.27 0 0 6.27 0 14c0 9.33 14 22 14 22s14-12.67 14-22C28 6.27 21.73 0 14 0z" fill="#181e4b"/>
        <circle cx="14" cy="14" r="6" fill="white"/>
      </svg>
    </div>`,
    iconSize: [28, 36],
    iconAnchor: [14, 36],
  })
  destinationMarker = L.marker([lat, lon], { icon, zIndexOffset: 900 })
    .addTo(mapInstance)
    .bindPopup(`<strong style="font-family:Inter,sans-serif;">${name}</strong>`)
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
      ${s.primary_phone ? `<p style="font-size:12px;color:#0298C5;margin:0 0 4px;">${s.primary_phone}</p>` : ''}
      ${s.website ? `<a href="${s.website}" target="_blank" rel="noopener" style="font-size:12px;color:#0298C5;">Visit website ↗</a>` : ''}
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
    const color = housing ? '#181e4b' : '#0298C5'
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
  visibleCount.value = 10
  expandedServiceId.value = null
})

// ── Autocomplete ───────────────────────────────────────────────────────────
function hideSuggestionsDelayed() {
  setTimeout(() => { showSuggestions.value = false }, 150)
}

function onSearchInput() {
  clearTimeout(acTimer)
  const q = searchQuery.value.trim()
  if (!q || !autocompleteService) { addressSuggestions.value = []; showSuggestions.value = false; return }
  acTimer = setTimeout(() => {
    autocompleteService.getPlacePredictions(
      { input: q, componentRestrictions: { country: 'au' }, types: ['geocode'] },
      (preds, status) => {
        console.log('[GM] autocomplete status:', status, 'predictions:', preds?.length ?? 0)
        if (status === 'OK' && preds?.length) {
          addressSuggestions.value = preds.slice(0, 5).map(p => ({ description: p.description, place_id: p.place_id }))
          showSuggestions.value = true
        } else {
          addressSuggestions.value = []
          showSuggestions.value = false
        }
      }
    )
  }, 300)
}

async function selectSuggestion(s) {
  searchQuery.value = s.description
  showSuggestions.value = false
  addressSuggestions.value = []
  clearDirections()
  loading.value = true
  try {
    const place = new window.google.maps.places.Place({ id: s.place_id })
    await place.fetchFields({ fields: ['location'] })
    const lat = place.location.lat()
    const lon = place.location.lng()
    userLocation.value = { lat, lon }
    locationLabel.value = s.description.split(',')[0]
    mapInstance?.setView([lat, lon], 13)
    placeUserMarker(lat, lon)
    sortByDistance(lat, lon)
    updateMapMarkers()
  } catch {
    // Fallback to Nominatim geocoding
    try {
      const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(s.description)}&format=json&limit=1`, { headers: { 'User-Agent': 'ChereBowl/1.0' } })
      const data = await res.json()
      if (data.length) {
        const lat = parseFloat(data[0].lat)
        const lon = parseFloat(data[0].lon)
        userLocation.value = { lat, lon }
        locationLabel.value = s.description.split(',')[0]
        mapInstance?.setView([lat, lon], 13)
        placeUserMarker(lat, lon)
        sortByDistance(lat, lon)
        updateMapMarkers()
      }
    } catch { /* silent */ }
  } finally {
    loading.value = false
  }
}

// ── Route mode toggle ──────────────────────────────────────────────────────
function setRouteMode(mode) {
  routeMode.value = mode
  if (mode === 'drive') {
    clearTransitLayers()
    stopVehiclePolling()
    directionsInfo.value = null; directionsSteps.value = []
    walkInfo.value = null; walkLegs.value = []
    if (selectedService.value) getDriveDirections(selectedService.value)
  } else if (mode === 'transit') {
    routeLayer?.remove(); routeLayer = null
    directionsInfo.value = null; directionsSteps.value = []
    walkInfo.value = null; walkLegs.value = []
    if (selectedService.value) getTransitDirections(selectedService.value)
  } else if (mode === 'walk') {
    routeLayer?.remove(); routeLayer = null
    clearTransitLayers(); stopVehiclePolling()
    directionsInfo.value = null; directionsSteps.value = []
    transitInfo.value = null; transitLegs.value = []
    if (selectedService.value) getWalkingDirections(selectedService.value)
  }
}

// ── Driving directions via OSRM (free, no key) ─────────────────────────────
async function getDriveDirections(service) {
  if (!userLocation.value || !mapInstance) return
  selectedService.value = service
  showingDirections.value = true
  directionsLoading.value = true
  directionsSteps.value = []
  directionsInfo.value = null

  routeLayer?.remove()
  routeLayer = null
  placeDestinationMarker(service.latitude, service.longitude, service.name)

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
      duration: durMin >= 60 ? `${Math.floor(durMin/60)}h ${durMin%60}m` : `${durMin} min`,
    }

    routeLayer = L.geoJSON(route.geometry, {
      style: { color: '#0298C5', weight: 5, opacity: 0.85 },
    }).addTo(mapInstance)
    mapInstance.fitBounds(routeLayer.getBounds(), { padding: [60, 60] })

    const steps = route.legs.flatMap(leg => leg.steps)
    directionsSteps.value = steps.map(step => ({
      instruction: formatManeuver(step),
      distance: formatMeters(step.distance),
      iconPath: maneuverIcon(step.maneuver),
    }))
  } catch {
    directionsInfo.value = directionsInfo.value || { service: service.name, distance: '—', duration: '—' }
    directionsSteps.value = [{ instruction: 'Could not calculate route. Check your connection.', distance: '', iconPath: 'M12 9v4M12 17h.01' }]
  } finally {
    directionsLoading.value = false
  }
}

// Keep old name as alias so existing "Get Directions" button call still works
function getDirections(service) {
  routeMode.value = 'drive'
  getDriveDirections(service)
}

// ── Transit directions via Google Maps ─────────────────────────────────────
function getTransitDirections(service) {
  if (!userLocation.value || !directionsService) {
    transitLegs.value = [{ mode: 'error', instructions: 'Transit directions require the Google Maps API key to be configured.' }]
    return
  }

  selectedService.value = service
  showingDirections.value = true
  directionsLoading.value = true
  placeDestinationMarker(service.latitude, service.longitude, service.name)
  transitLegs.value = []
  transitInfo.value = null
  clearTransitLayers()
  stopVehiclePolling()

  const request = {
    origin: new window.google.maps.LatLng(userLocation.value.lat, userLocation.value.lon),
    destination: new window.google.maps.LatLng(service.latitude, service.longitude),
    travelMode: window.google.maps.TravelMode.TRANSIT,
    transitOptions: { modes: ['BUS', 'RAIL', 'TRAM'] },
  }

  directionsService.route(request, (result, status) => {
    directionsLoading.value = false
    console.log('[Transit] status:', status, 'result:', result)

    if (status !== 'OK') {
      transitLegs.value = [{ mode: 'error', instructions: `No public transport route found (${status}). Ensure Directions API is enabled.` }]
      return
    }

    const leg = result.routes[0].legs[0]
    const allCoords = []
    highlightedTripIds = new Set()
    const modeColors = { walk: '#4a5568', train: '#0298C5', tram: '#2e7d32', bus: '#e65100' }

    transitLegs.value = leg.steps.map(step => {
      const isTransit = step.travel_mode === 'TRANSIT'
      const td = step.transit

      const decoded = window.google.maps.geometry.encoding
        .decodePath(step.polyline.points)
        .map(p => [p.lat(), p.lng()])
      allCoords.push(...decoded)

      let mode = 'walk'
      if (isTransit) {
        const vtype = td.line.vehicle.type
        mode = ['SUBWAY', 'HEAVY_RAIL', 'COMMUTER_TRAIN', 'RAIL'].includes(vtype) ? 'train'
             : vtype === 'TRAM' ? 'tram'
             : 'bus'
      }

      const layer = L.polyline(decoded, {
        color: modeColors[mode],
        weight: mode === 'walk' ? 4 : 6,
        dashArray: mode === 'walk' ? '3,7' : null,
        opacity: mode === 'walk' ? 0.75 : 0.9,
      }).addTo(mapInstance)
      transitRouteLayers.push(layer)

      const tripId = isTransit ? (td.trip?.trip_id ?? null) : null
      if (tripId) highlightedTripIds.add(tripId)

      return {
        mode,
        instructions: step.html_instructions?.replace(/<[^>]+>/g, '') ?? '',
        distance: step.distance?.text ?? null,
        duration: step.duration?.text ?? null,
        from_name: isTransit ? td.departure_stop.name : null,
        to_name: isTransit ? td.arrival_stop.name : null,
        depart: isTransit ? td.departure_time.text : null,
        arrive: isTransit ? td.arrival_time.text : null,
        num_stops: isTransit ? td.num_stops : null,
        route_name: isTransit ? (td.line.short_name || td.line.name) : null,
        route_id: isTransit ? (td.line.gtfs_id ?? td.line.short_name ?? null) : null,
        trip_id: tripId,
      }
    })

    if (allCoords.length) {
      mapInstance.fitBounds(L.latLngBounds(allCoords), { padding: [60, 60] })
    }

    transitInfo.value = {
      service: service.name,
      duration: leg.duration.text,
      distance: leg.distance.text,
    }

    startVehiclePolling()
  })
}

// ── GTFSR vehicle polling ─────────────────────────────────────────────────
const VEHICLE_MODE_COLORS = { train: '#0298C5', tram: '#2e7d32', bus: '#e65100' }

async function pollVehicles() {
  try {
    const routeIds = transitLegs.value
      .filter(l => l.route_id).map(l => l.route_id).join(',')
    const params = routeIds ? `?route_ids=${encodeURIComponent(routeIds)}` : ''
    const res = await fetch(`${API_BASE}/gtfsr/vehicles${params}`)
    if (!res.ok) return
    const vehicles = await res.json()

    const seen = new Set()
    for (const v of vehicles) {
      if (!v.lat || !v.lon) continue
      seen.add(v.id)
      const isHighlighted = highlightedTripIds.has(v.trip_id)
      const color = VEHICLE_MODE_COLORS[vehicleMode(v.route_id)] || '#0298C5'

      if (vehicleMarkers[v.id]) {
        vehicleMarkers[v.id].setLatLng([v.lat, v.lon])
      } else {
        const icon = L.divIcon({
          className: '',
          html: buildVehicleIconHtml(color, v.bearing, isHighlighted),
          iconSize: [28, 28],
          iconAnchor: [14, 14],
        })
        vehicleMarkers[v.id] = L.marker([v.lat, v.lon], { icon, zIndexOffset: 500 })
          .bindPopup(buildVehiclePopup(v))
          .addTo(mapInstance)
      }
    }

    for (const id of Object.keys(vehicleMarkers)) {
      if (!seen.has(id)) { vehicleMarkers[id].remove(); delete vehicleMarkers[id] }
    }
  } catch { /* real-time is best-effort */ }
}

function vehicleMode(routeId) {
  if (!routeId) return 'train'
  const id = String(routeId).toLowerCase()
  if (id.includes('tram')) return 'tram'
  if (id.includes('bus')) return 'bus'
  return 'train'
}

function buildVehicleIconHtml(color, bearing, highlighted) {
  const rotation = bearing != null ? bearing : 0
  const border = highlighted ? `border:2.5px solid #181e4b;` : `border:1.5px solid rgba(255,255,255,0.8);`
  const pulse = highlighted ? `box-shadow:0 0 0 4px ${color}44;` : ''
  return `<div style="width:24px;height:24px;border-radius:50%;background:${color};${border}${pulse}
    display:flex;align-items:center;justify-content:center;transform:rotate(${rotation}deg);">
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
      <path d="M5 1L8 8H5H2L5 1Z" fill="white" opacity="0.9"/>
    </svg>
  </div>`
}

function buildVehiclePopup(v) {
  const ts = v.timestamp ? new Date(v.timestamp * 1000).toLocaleTimeString('en-AU', { hour: '2-digit', minute: '2-digit' }) : 'unknown'
  return `<div style="font-family:Inter,sans-serif;font-size:12px;min-width:120px;">
    <p style="font-weight:700;margin:0 0 4px;color:#1a1a1a;">Route ${v.route_id || '—'}</p>
    <p style="color:#888;margin:0;">Last updated ${ts}</p>
  </div>`
}

// ── Walking directions via Google Maps (WALKING travel mode) ──────────────
function getWalkingDirections(service) {
  if (!userLocation.value || !directionsService) {
    walkLegs.value = [{ instruction: 'Walking directions require the Google Maps API key to be configured.', distance: '', iconPath: 'M12 9v4M12 17h.01' }]
    return
  }

  selectedService.value = service
  showingDirections.value = true
  directionsLoading.value = true
  placeDestinationMarker(service.latitude, service.longitude, service.name)
  walkLegs.value = []
  walkInfo.value = null

  const request = {
    origin: new window.google.maps.LatLng(userLocation.value.lat, userLocation.value.lon),
    destination: new window.google.maps.LatLng(service.latitude, service.longitude),
    travelMode: window.google.maps.TravelMode.WALKING,
  }

  directionsService.route(request, (result, status) => {
    directionsLoading.value = false

    if (status !== 'OK') {
      walkLegs.value = [{ instruction: `No walking route found (${status}).`, distance: '', iconPath: 'M12 9v4M12 17h.01' }]
      return
    }

    const leg = result.routes[0].legs[0]
    const allCoords = []

    walkLegs.value = leg.steps.map(step => {
      const decoded = window.google.maps.geometry.encoding
        .decodePath(step.polyline.points)
        .map(p => [p.lat(), p.lng()])
      allCoords.push(...decoded)

      const layer = L.polyline(decoded, {
        color: '#2e7d32',
        weight: 4,
        dashArray: '3,7',
        opacity: 0.85,
      }).addTo(mapInstance)
      transitRouteLayers.push(layer)

      const instr = step.html_instructions?.replace(/<[^>]+>/g, '') ?? ''
      return {
        instruction: instr,
        distance: step.distance?.text ?? '',
        iconPath: walkStepIcon(step.html_instructions ?? ''),
      }
    })

    if (allCoords.length) mapInstance.fitBounds(L.latLngBounds(allCoords), { padding: [60, 60] })

    walkInfo.value = {
      service: service.name,
      duration: leg.duration.text,
      distance: leg.distance.text,
    }
  })
}

function walkStepIcon(html) {
  const h = html.toLowerCase()
  if (h.includes('left'))  return 'M9 19l-7-7 7-7M2 12h20'
  if (h.includes('right')) return 'M15 19l7-7-7-7M22 12H2'
  if (h.includes('slight left') || h.includes('keep left'))  return 'M5 19l7-7M12 12H2'
  if (h.includes('slight right') || h.includes('keep right')) return 'M19 19l-7-7M12 12h10'
  if (h.includes('arrive') || h.includes('destination')) return 'M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8zM12 10m-3 0a3 3 0 1 0 6 0 3 3 0 0 0-6 0'
  return 'M12 19V5M5 12l7-7 7 7'
}

function startVehiclePolling() {
  pollVehicles()
  vehiclePollTimer = setInterval(pollVehicles, 30_000)
}

function stopVehiclePolling() {
  clearInterval(vehiclePollTimer)
  vehiclePollTimer = null
  Object.values(vehicleMarkers).forEach(m => m.remove())
  vehicleMarkers = {}
}

function clearTransitLayers() {
  transitRouteLayers.forEach(l => l.remove())
  transitRouteLayers = []
}

function clearDirections() {
  routeLayer?.remove()
  routeLayer = null
  destinationMarker?.remove()
  destinationMarker = null
  clearTransitLayers()
  stopVehiclePolling()
  directionsInfo.value = null
  directionsSteps.value = []
  transitInfo.value = null
  transitLegs.value = []
  walkInfo.value = null
  walkLegs.value = []
  showingDirections.value = false
  routeMode.value = 'drive'
}

// ── Transit leg colour helpers ─────────────────────────────────────────────
function hasValue(v) {
  return v != null && v !== '' && String(v) !== 'NaN'
}

function transitLegColor(mode) {
  return { train: '#0298C5', tram: '#2e7d32', bus: '#e65100', walk: '#888888' }[mode] || '#333'
}
function transitLegBg(mode) {
  return { train: '#D8EDFF', tram: '#e8f5e9', bus: '#fbe9e7', walk: '#f5f5f5' }[mode] || '#f5f5f5'
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

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
  }).addTo(mapInstance)

  // Load Google Maps JS API (Places autocomplete + DirectionsService)
  const gmKey = config.public.googleMapsApiKey
  console.log('[GM] key resolved to:', gmKey ? gmKey.slice(0,12) + '...' : 'EMPTY — check NUXT_PUBLIC_GOOGLE_MAPS_API_KEY in .env.local')
  if (gmKey && !window.__gmLoaded) {
    await new Promise(resolve => {
      window.__gmReady = () => { window.__gmLoaded = true; resolve() }
      const s = document.createElement('script')
      s.src = `https://maps.googleapis.com/maps/api/js?key=${gmKey}&libraries=places,geometry&callback=__gmReady`
      s.onerror = () => { console.error('[ChereBowl] Google Maps failed to load — check API key and enabled APIs (Maps JavaScript API, Places API, Directions API)'); resolve() }
      document.head.appendChild(s)
    })
  }
  if (window.__gmLoaded && window.google) {
    autocompleteService = new window.google.maps.places.AutocompleteService()
    directionsService = new window.google.maps.DirectionsService()
  }

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
  nextTick(() => setTimeout(() => mapInstance?.invalidateSize(), 50))
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayout)
  stopVehiclePolling()
  clearTimeout(acTimer)
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
.page-header {
  background: #D8EDFF;
  padding: 28px 40px 20px;
  border-bottom: 1px solid #b8d9f8;
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
  flex-shrink: 0;
  overflow: hidden;
}

/* ── Left card panel ─────────────────────────────────── */
.left-panel {
  width: 390px;
  min-width: 340px;
  background: #fafafa;
  border-right: 1px solid #e0edf8;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
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
  position: relative;
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

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.4); }
}

@keyframes userPulse {
  0% { transform: scale(0.8); opacity: 0.6; }
  70% { transform: scale(2.2); opacity: 0; }
  100% { transform: scale(0.8); opacity: 0; }
}

/* ── Mobile (≤ 767px) ────────────────────────────────── */
@media (max-width: 767px) {
  .page-header {
    padding: 16px 16px 12px;
  }

  .page-header h1 {
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
  }

  .left-panel {
    width: 100%;
    min-width: unset;
    height: auto;
    overflow: visible;
    border-right: none;
    border-top: 1px solid #e0edf8;
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
  border: 1px solid #b8d9f8;
  border-radius: 10px;
  padding: 14px 16px;
  min-width: 180px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.11);
  z-index: 1100;
  white-space: nowrap;
}

/* Show panel on hover of either the button or the panel itself */
.filters-dropdown:hover .filters-panel {
  display: block;
}
</style>
