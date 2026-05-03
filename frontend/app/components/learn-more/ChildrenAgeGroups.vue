<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <!-- Heading -->
      <p class="font-roboto font-bold text-coral text-[16px] lg:text-[20px] tracking-[2px] uppercase">
        The Children
      </p>
      <h2 class="mt-3 font-volkhov font-bold text-navy
               text-[28px] sm:text-[36px] lg:text-[48px] leading-tight">
        No child should grow up hungry
      </h2>
      <p class="mt-4 font-roboto text-[16px] lg:text-[20px] text-black max-w-3xl leading-relaxed">
        Nutrition needs change as children grow. See the recommended daily intake goals for each age group.
      </p>

      <!-- Age Group Selection Tabs -->
      <div class="flex flex-wrap justify-center gap-6 mb-16 lg:mb-24">
        <button v-for="g in ageGroups" :key="g.label"
          class="flex flex-col items-center gap-4 transition-all duration-500 group relative min-w-[160px] pb-4"
          :class="selectedGroupLabel === g.label
            ? 'scale-110'
            : 'opacity-70 hover:opacity-100 hover:scale-105'"
          @click="selectGroup(g.label)">
          
          <!-- Logo -->
          <img :src="g.img" 
            class="w-32 h-32 lg:w-44 lg:h-44 object-contain transition-all duration-500"
            :class="selectedGroupLabel === g.label ? '' : 'grayscale group-hover:grayscale-0'" />

          <!-- Label -->
          <div class="text-center">
            <h4 class="font-volkhov font-bold text-[18px] lg:text-[22px] leading-tight"
               :class="selectedGroupLabel === g.label ? 'text-navy' : 'text-navy/60'">
               {{ getGroupName(g.label) }}
            </h4>
            <p class="font-roboto font-semibold text-[13px] lg:text-[15px] mt-1 uppercase tracking-wider transition-colors duration-300"
               :class="selectedGroupLabel === g.label ? 'text-coral' : 'text-gray-400'">
               {{ g.label }}
            </p>
          </div>

          <!-- Active Indicator Dot -->
          <div v-if="selectedGroupLabel === g.label" 
            class="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-coral"></div>
        </button>
      </div>


      <!-- Main Interactive Display -->
      <div class="grid grid-cols-1 lg:grid-cols-[1fr_2fr] gap-12 lg:gap-16 items-start min-h-[600px]">

        <!-- LEFT: Enlarged Logo with Fill Animation -->
        <div class="relative w-full flex justify-center items-start lg:sticky lg:top-24">
          <transition name="logo-fade" mode="out-in" @after-enter="onLogoEnter">
            <div :key="selectedGroupLabel"
              class="relative w-full max-w-[360px] h-[450px] flex justify-center items-end">
              <div class="absolute inset-0 w-full h-full" :style="{
                maskImage: `url(${selectedGroupImage})`,
                WebkitMaskImage: `url(${selectedGroupImage})`,
                maskSize: 'contain',
                WebkitMaskSize: 'contain',
                maskPosition: 'bottom center',
                WebkitMaskPosition: 'bottom center',
                maskRepeat: 'no-repeat',
                WebkitMaskRepeat: 'no-repeat'
              }">
                <!-- Light Blue Base -->
                <div class="absolute inset-0 w-full h-full bg-[#D8EDFF] opacity-90"></div>

                <!-- Navy Fill animating from 0 to 100% -->
                <div class="absolute bottom-0 left-0 w-full bg-[#1B1E45] transition-all duration-[1500ms] ease-out"
                  :style="{ height: fillTrigger ? '100%' : '0%' }"></div>
              </div>
            </div>
          </transition>
        </div>

        <!-- RIGHT: The Macronutrient Cards Grid -->
        <div class="relative min-h-[500px]">
          <div v-if="pending" class="absolute inset-0 flex justify-center items-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-navy"></div>
          </div>

          <transition name="slide-fade" mode="out-in">
            <div :key="selectedGroupLabel" v-if="!pending" class="grid grid-cols-1 md:grid-cols-2 gap-6 pb-10">
              <div v-for="(nutrient, index) in selectedGroupNutrients" :key="nutrient.id"
                class="bg-white rounded-[24px] p-6 shadow-[0px_8px_24px_rgba(27,30,69,0.04)] hover:shadow-[0px_16px_40px_rgba(27,30,69,0.12)] transition-all duration-300 border border-gray-100 flex flex-col h-full transform hover:-translate-y-1"
                :style="{ animationDelay: `${index * 100}ms` }">

                <!-- Header: Nutrient Name -->
                <div class="flex items-center gap-3 mb-5 border-b border-gray-100 pb-4">
                  <div
                    class="w-12 h-12 rounded-full bg-[#F4F8FF] flex items-center justify-center text-[#1B1E45] font-bold shadow-sm shrink-0">
                    <component :is="getNutrientIcon(nutrient.nutrient)" class="w-6 h-6 text-coral" />
                  </div>
                  <h3 class="font-volkhov font-bold text-navy text-[22px] leading-tight">{{ nutrient.nutrient }}</h3>
                </div>

                <!-- Visual Portion Guide -->
                <div class="bg-[#F8FBFF] rounded-2xl p-5 mb-5 flex items-center gap-4 border border-[#E5F3FF]">
                  <div
                    class="w-14 h-14 shrink-0 rounded-full bg-white flex items-center justify-center shadow-sm text-navy">
                    <component :is="getPortionIcon(nutrient.portion_guide)" class="w-7 h-7" />
                  </div>
                  <div class="flex-grow">
                    <p class="font-roboto text-[11px] text-navy/60 uppercase tracking-widest font-bold mb-1">Portion
                      Guide</p>
                    <p class="font-roboto font-bold text-coral text-[16px] leading-tight">{{ nutrient.portion_guide }}
                    </p>
                  </div>
                </div>

                <!-- Actionable Guidance -->
                <div class="mt-auto">
                  <p class="font-roboto text-xs text-gray-400 uppercase tracking-wider font-semibold mb-2">Guidance</p>
                  <p class="font-roboto text-gray-700 text-[15px] leading-relaxed">
                    {{ nutrient.actionable_guidance }}
                  </p>
                </div>

              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- Data resources -->
      <div class="mt-8 pt-6 border-t border-gray-200 text-[11px] text-ash">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Children Macronutrients:</span>
            <a href="https://www.eatforhealth.gov.au/nutrient-reference-values/nutrients" target="_blank" rel="noopener"
              class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              NHMRC Nutrient Reference Values
            </a>
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useFetch, useRuntimeConfig } from '#app'
import {
  Hand,
  HandPlatter,
  Soup,
  Coffee,
  Utensils,
  Baby,
  Droplet,
  Beef,
  Wheat,
  Activity,
  Zap,
  Circle,
  GlassWater,
  CupSoda
} from 'lucide-vue-next'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

interface NutrientData {
  id: number;
  age: string;
  nutrient: string;
  goal: string;
  portion_guide: string;
  rationale_summary: string;
  actionable_guidance: string;
}

// Fetch recommended macronutrients data
const { data: macronutrientsData, pending } = await useFetch<NutrientData[]>(`${apiBase}/recommended-macronutrients`)

// Image mapping based on API age labels
const ageImageMap: Record<string, string> = {
  '0-6 months': '/images/children-infant.png',
  '7-12 months': '/images/children-infant.png',
  '1-3 years': '/images/children-toddler.png',
  '4-8 years': '/images/children-preschool.png',
  '9-13 years': '/images/children-school-age.png'
}

// Order of ages
const ageOrder = ['0-6 months', '7-12 months', '1-3 years', '4-8 years', '9-13 years']

const getGroupName = (age: string) => {
  if (age.includes('0-6') || age.includes('7-12')) return 'Infants'
  if (age.includes('1-3')) return 'Toddlers'
  if (age.includes('4-8')) return 'Pre-schoolers'
  if (age.includes('9-13')) return 'School-age'
  return 'Children'
}

// Compute dynamic age groups
const ageGroups = computed(() => {
  if (!macronutrientsData.value) return []

  const uniqueAges = Array.from(new Set(macronutrientsData.value.map(item => item.age)))

  // Sort ages based on predefined order
  uniqueAges.sort((a, b) => {
    return ageOrder.indexOf(a) - ageOrder.indexOf(b)
  })

  return uniqueAges.map(age => ({
    label: age,
    img: ageImageMap[age] || '/images/children-school-age.png'
  }))
})

const selectedGroupLabel = ref('0-6 months')
const fillTrigger = ref(false)

const selectedGroupImage = computed(() => {
  return ageImageMap[selectedGroupLabel.value] || '/images/children-school-age.png'
})

// Filter nutrients for the selected age group
const selectedGroupNutrients = computed(() => {
  if (!macronutrientsData.value) return []
  return macronutrientsData.value.filter(item => item.age === selectedGroupLabel.value)
})

const selectGroup = (label: string) => {
  if (selectedGroupLabel.value === label) return
  fillTrigger.value = false
  selectedGroupLabel.value = label
}

const onLogoEnter = () => {
  setTimeout(() => {
    fillTrigger.value = true
  }, 100)
}

// Ensure fill animation triggers on initial mount
onMounted(() => {
  setTimeout(() => {
    fillTrigger.value = true
  }, 300)
})

// Icon mapping helpers
const getNutrientIcon = (nutrient: string) => {
  const n = (nutrient || '').toLowerCase()
  if (n.includes('energy')) return Zap
  if (n.includes('protein')) return Beef
  if (n.includes('fibre') || n.includes('fiber')) return Wheat
  if (n.includes('fluid')) return Droplet
  if (n.includes('fat')) return Activity
  if (n.includes('carbohydrate')) return Wheat
  return Activity
}

const getPortionIcon = (portionGuide: string) => {
  const p = (portionGuide || '').toLowerCase()
  if (p.includes('handful')) return Hand
  if (p.includes('palm') || p.includes('hand')) return HandPlatter
  if (p.includes('glass') || p.includes('water')) return GlassWater
  if (p.includes('cup')) return CupSoda
  if (p.includes('bowl')) return Soup
  if (p.includes('plate')) return Circle
  if (p.includes('tablespoon')) return Utensils
  if (p.includes('milk') || p.includes('feed on demand')) return Baby
  return Utensils
}
</script>

<style scoped>
/* Main Logo Transition */
.logo-fade-enter-active {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.logo-fade-leave-active {
  transition: all 0.3s ease-in;
}

.logo-fade-enter-from,
.logo-fade-leave-to {
  opacity: 0;
  transform: scale(0.85);
}

/* Cards List Transition */
.slide-fade-enter-active {
  transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
