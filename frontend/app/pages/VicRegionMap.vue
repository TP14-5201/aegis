<template>
  <div class="w-full min-h-screen flex flex-col" style="background-color: #fafafa; font-family: 'Inter', sans-serif;">
    <LayoutNavbar />

    <section class="relative w-full overflow-hidden bg-[#041627]" style="min-height: 100vh; padding-top: 100px;">
      <div class="relative z-10 max-w-[1440px] mx-auto px-6 sm:px-12 lg:px-16 pb-20">
        
        <div class="reveal mb-12">
          <h1 class="text-white font-bold leading-tight" style="font-size: clamp(32px, 4vw, 56px); letter-spacing: -1px;">
            Regional Insights
          </h1>
          <p class="text-white/70 mt-4 max-w-xl" style="font-size: 18px;">
            Select a region on the map to view local food insecurity and housing data.
          </p>
        </div>

        <div class="flex flex-col lg:flex-row gap-8 items-stretch min-h-[600px]">
          
          <div class="flex-[1.5] bg-white/5 rounded-2xl p-4 backdrop-blur-sm border border-white/10 shadow-2xl reveal">
            <div ref="mapEl" class="w-full h-full min-h-[400px] lg:min-h-0 rounded-xl overflow-hidden" />
          </div>

          <div class="flex-1 flex flex-col reveal" style="transition-delay: 0.1s;">
            <div v-if="!selectedRegion" class="h-full flex flex-col justify-center items-center text-center p-12 bg-white/5 rounded-2xl border border-dashed border-white/20">
              <div class="w-16 h-16 mb-6 opacity-20">
                <svg fill="white" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
              </div>
              <p class="text-white/50 font-medium">Click a region on the map to explore detailed statistics</p>
            </div>

            <div v-else class="h-full bg-[#f5f3ef] rounded-2xl p-8 lg:p-12 shadow-xl flex flex-col justify-between">
              <div>
                <h2 style="font-size: 32px; font-weight: 700; color: #171717; margin-bottom: 8px;">
                  {{ selectedRegion.name }}
                </h2>
                <div class="w-12 h-1 bg-[#2d5016] mb-8"></div>

                <div class="space-y-10">
                  <div class="flex flex-col">
                    <span style="font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Food Insecurity</span>
                    <div class="flex items-baseline gap-2">
                      <span style="font-size: 42px; font-weight: 900; color: #ef4444; line-height: 1;">{{ selectedRegion.data.foodInsecurity }}</span>
                      <span style="font-size: 16px; color: #525252; font-weight: 500;">people</span>
                    </div>
                  </div>

                  <div class="flex flex-col">
                    <span style="font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Median House Price</span>
                    <span style="font-size: 42px; font-weight: 900; color: #3b82f6; line-height: 1;">{{ selectedRegion.data.housePrice }}</span>
                  </div>
                </div>
              </div>

              <div class="mt-12">
                <NuxtLink to="/services">
                  <button class="w-full btn-primary text-white font-extrabold rounded-[10px] shadow-lg cursor-pointer"
                    style="background-color: #2d5016; font-size: 16px; padding: 18px 32px;">
                    FIND LOCAL HELP
                  </button>
                </NuxtLink>
                <p class="mt-4 text-center text-[#525252] text-sm">
                  Available support in {{ selectedRegion.name }}
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <LayoutFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import dissolve from '@turf/dissolve'

// (REGIONS, PLACEHOLDER_DATA, and FORMATTED_NAMES remain identical to your previous source)
const REGIONS = {
  'Mallee': { color: '#C85A4A', labelPos: [-35.3, 142.4], lgas: ['Buloke', 'Gannawarra', 'Mildura', 'Swan Hill'] },
  'Wimmera Southern Mallee': { color: '#7B3F7A', labelPos: [-36.6, 141.8], lgas: ['Hindmarsh', 'Horsham', 'Northern Grampians', 'West Wimmera', 'Yarriambiack'] },
  'Loddon Campaspe': { color: '#C0508A', labelPos: [-36.7, 144.3], lgas: ['Campaspe', 'Central Goldfields', 'Greater Bendigo', 'Loddon', 'Macedon Ranges', 'Mount Alexander'] },
  'Goulburn': { color: '#4A9B50', labelPos: [-36.8, 145.4], lgas: ['Greater Shepparton', 'Mitchell', 'Moira', 'Murrindindi', 'Strathbogie'] },
  'Ovens Murray': { color: '#6070B8', labelPos: [-36.5, 147.0], lgas: ['Alpine', 'Benalla', 'Indigo', 'Mansfield', 'Towong', 'Wangaratta', 'Wodonga'] },
  'Central Highlands': { color: '#D48A1A', labelPos: [-37.5, 143.8], lgas: ['Ararat', 'Ballarat', 'Golden Plains', 'Hepburn', 'Moorabool', 'Pyrenees'] },
  'Barwon': { color: '#A01830', labelPos: [-38.2, 144.1], lgas: ['Colac Otway', 'Greater Geelong', 'Queenscliffe', 'Surf Coast'] },
  'Great South Coast': { color: '#2A9A78', labelPos: [-38.1, 142.5], lgas: ['Corangamite', 'Glenelg', 'Moyne', 'Southern Grampians', 'Warrnambool'] },
  'Gippsland': { color: '#1A9EBB', labelPos: [-38.0, 147.0], lgas: ['Bass Coast', 'Baw Baw', 'East Gippsland', 'Latrobe', 'South Gippsland', 'Wellington'] },
}

const PLACEHOLDER_DATA = {
  'Mallee': { foodInsecurity: '15,200', housePrice: '$420,000' },
  'Wimmera Southern Mallee': { foodInsecurity: '11,400', housePrice: '$380,000' },
  'Loddon Campaspe': { foodInsecurity: '25,600', housePrice: '$550,000' },
  'Goulburn': { foodInsecurity: '18,300', housePrice: '$490,000' },
  'Ovens Murray': { foodInsecurity: '14,100', housePrice: '$510,000' },
  'Central Highlands': { foodInsecurity: '22,500', housePrice: '$600,000' },
  'Barwon': { foodInsecurity: '28,900', housePrice: '$780,000' },
  'Great South Coast': { foodInsecurity: '13,800', housePrice: '$450,000' },
  'Gippsland': { foodInsecurity: '31,200', housePrice: '$520,000' },
}

const FORMATTED_NAMES = {
  'Mallee': 'Mallee', 'Wimmera Southern Mallee': 'Wimmera<br/>Southern Mallee',
  'Loddon Campaspe': 'Loddon<br/>Campaspe', 'Goulburn': 'Goulburn',
  'Ovens Murray': 'Ovens Murray', 'Central Highlands': 'Central<br/>Highlands',
  'Barwon': 'Barwon', 'Great South Coast': 'Great South<br/>Coast', 'Gippsland': 'Gippsland'
};

const props = defineProps({
  geojsonPath: { type: String, default: '/vic_lga.geojson' }
})

const emit = defineEmits(['regionSelected'])
const selectedRegion = ref(null)
const mapEl = ref(null)
let mapInstance = null
let geoLayer = null

function getRegionName(abbName) {
  if (!abbName) return null
  for (const [name, cfg] of Object.entries(REGIONS)) {
    if (cfg.lgas.some((lga) => lga.toLowerCase() === abbName.toLowerCase())) return name
  }
  return null
}

function initReveal() {
  const elements = document.querySelectorAll('.reveal')
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add('visible')
    })
  }, { threshold: 0.1 })
  elements.forEach((el) => observer.observe(el))
}

onMounted(async () => {
  initReveal()
  if (!mapEl.value) return

  mapInstance = L.map(mapEl.value, {
    zoomControl: true, attributionControl: false, 
    scrollWheelZoom: false, renderer: L.svg({ padding: 0.1 })
  })

  try {
    const geoResponse = await fetch(props.geojsonPath)
    const rawGeojson = await geoResponse.json()
    rawGeojson.features.forEach(f => f.properties.REGION_NAME = getRegionName(f.properties.ABB_NAME));
    const filtered = { type: 'FeatureCollection', features: rawGeojson.features.filter(f => f.properties.REGION_NAME) };
    const mergedGeojson = dissolve(filtered, { propertyName: 'REGION_NAME' });

    geoLayer = L.geoJSON(mergedGeojson, {
      style: (feat) => ({
        fillColor: REGIONS[feat.properties.REGION_NAME].color,
        fillOpacity: 0.6, color: '#ffffff', weight: 1.5,
        className: 'region-path'
      }),
      onEachFeature(feat, layer) {
        const name = feat.properties.REGION_NAME;
        layer.on('click', (e) => {
          selectedRegion.value = { name, data: PLACEHOLDER_DATA[name] }
          emit('regionSelected', selectedRegion.value);
          // Highlight logic
          geoLayer.eachLayer(l => l.setStyle({ fillOpacity: 0.6, weight: 1.5 }));
          layer.setStyle({ fillOpacity: 0.9, weight: 3 });
        });
      }
    }).addTo(mapInstance);

    mapInstance.fitBounds(geoLayer.getBounds(), { padding: [30, 30] })

    for (const [name, data] of Object.entries(REGIONS)) {
       const html = `<div class="map-label">${FORMATTED_NAMES[name]}</div>`;
       L.marker(data.labelPos, { icon: L.divIcon({ className: '', html, iconSize:[0,0] }), interactive: false }).addTo(mapInstance);
    }
  } catch (err) {
    console.error("Map Error:", err)
  }
})

onBeforeUnmount(() => mapInstance?.remove())
</script>

<style scoped>
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

:deep(.leaflet-container) { background: transparent !important; }

:deep(.region-path) {
  transition: all 0.3s ease;
  cursor: pointer;
}

:deep(.map-label) {
  transform: translate(-50%,-50%);
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 10px;
  text-transform: uppercase;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  pointer-events: none;
  letter-spacing: 1px;
}
</style>