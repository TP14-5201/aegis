<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">

      <!-- Heading -->
      <p class="font-roboto font-bold text-coral text-[16px] lg:text-[20px] tracking-[2px] uppercase">
        The Children
      </p>
      <h2 class="mt-3 font-volkhov font-bold text-navy text-[28px] sm:text-[36px] lg:text-[48px] leading-tight">
        No child should grow up hungry
      </h2>
      <p class="mt-4 font-roboto text-[16px] lg:text-[20px] text-black max-w-3xl leading-relaxed">
        Nutrition needs change as children grow. See the recommended daily intake goals for each age group.
      </p>

      <!-- Unified Interactive Panel -->
      <div class="mt-8 rounded-[28px] bg-[#F4F9FF] border border-[#D8EDFF] overflow-hidden">

        <!-- Tab Bar -->
        <div class="flex items-end justify-around px-4 sm:px-8 pt-5 flex-wrap border-b border-[#D8EDFF]">
          <button
            v-for="g in ageGroups"
            :key="g.label"
            class="relative flex flex-col items-center gap-1.5 pb-3 px-2 sm:px-4 min-w-[64px] sm:min-w-[90px] transition-all duration-300 group"
            :class="selectedGroupLabel === g.label ? 'opacity-100' : 'opacity-45 hover:opacity-75'"
            @click="selectGroup(g.label)"
          >
            <img
              :src="g.img"
              class="w-10 h-10 sm:w-14 sm:h-14 object-contain transition-all duration-300"
              :class="selectedGroupLabel === g.label ? '' : 'grayscale group-hover:grayscale-0'"
            />
            <div class="text-center">
              <h4
                class="font-volkhov font-bold text-[13px] sm:text-[15px] leading-tight"
                :class="selectedGroupLabel === g.label ? 'text-navy' : 'text-navy/50'"
              >
                {{ getGroupName(g.label) }}
              </h4>
              <p
                class="font-roboto font-semibold text-[9px] sm:text-[10px] mt-0.5 uppercase tracking-wider"
                :class="selectedGroupLabel === g.label ? 'text-coral' : 'text-gray-400'"
              >
                {{ g.label }}
              </p>
            </div>
            <!-- Active underline -->
            <div
              v-if="selectedGroupLabel === g.label"
              class="absolute bottom-0 left-0 right-0 h-[3px] bg-coral rounded-t-full"
            />
          </button>
        </div>

        <!-- Content Row: Silhouette + Cards -->
        <div class="grid grid-cols-1 lg:grid-cols-[200px_1fr] xl:grid-cols-[240px_1fr] items-center">

          <!-- Silhouette -->
          <div class="hidden lg:flex justify-center items-end py-6 px-4 border-r border-[#D8EDFF] self-stretch">
            <transition name="logo-fade" mode="out-in" @after-enter="onLogoEnter">
              <div
                :key="selectedGroupLabel"
                class="relative w-[160px] xl:w-[200px] h-[240px] xl:h-[280px] flex justify-center items-end"
              >
                <div
                  class="absolute inset-0 w-full h-full"
                  :style="{
                    maskImage: `url(${selectedGroupImage})`,
                    WebkitMaskImage: `url(${selectedGroupImage})`,
                    maskSize: 'contain',
                    WebkitMaskSize: 'contain',
                    maskPosition: 'bottom center',
                    WebkitMaskPosition: 'bottom center',
                    maskRepeat: 'no-repeat',
                    WebkitMaskRepeat: 'no-repeat'
                  }"
                >
                  <div class="absolute inset-0 w-full h-full bg-[#D8EDFF] opacity-90" />
                  <div
                    class="absolute bottom-0 left-0 w-full bg-[#1B1E45] transition-all duration-[1500ms] ease-out"
                    :style="{ height: fillTrigger ? '100%' : '0%' }"
                  />
                </div>
              </div>
            </transition>
          </div>

          <!-- Nutrient Cards -->
          <div class="p-4 sm:p-6 lg:p-8">
            <div v-if="pending" class="flex justify-center items-center h-36">
              <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-navy" />
            </div>

            <transition name="slide-fade" mode="out-in">
              <div
                v-if="!pending"
                :key="selectedGroupLabel"
                class="grid grid-cols-2 xl:grid-cols-3 gap-3 lg:gap-4"
              >
                <div
                  v-for="(nutrient, index) in selectedGroupNutrients"
                  :key="nutrient.id"
                  class="bg-white rounded-[16px] px-4 py-3 border border-[#D8EDFF] shadow-sm
                         flex flex-col min-h-[130px]
                         hover:shadow-md hover:-translate-y-0.5 transition-all duration-300"
                  :style="{ animationDelay: `${index * 80}ms` }"
                >
                  <!-- Header -->
                  <div class="flex items-center gap-2 mb-2">
                    <div class="w-7 h-7 rounded-full bg-[#EBF5FF] flex items-center justify-center shrink-0">
                      <component :is="getNutrientIcon(nutrient.nutrient)" class="w-3.5 h-3.5 text-coral" />
                    </div>
                    <h3 class="font-volkhov font-bold text-navy text-[13px] lg:text-[14px] leading-tight">
                      {{ nutrient.nutrient }}
                    </h3>
                  </div>

                  <!-- Portion Guide -->
                  <div class="bg-[#F4F9FF] rounded-lg px-2.5 py-2 mb-2">
                    <p class="font-roboto text-[8px] text-navy/50 uppercase tracking-widest font-bold mb-0.5">
                      Portion Guide
                    </p>
                    <p class="font-roboto font-bold text-coral text-[11px] leading-tight">
                      {{ nutrient.portion_guide }}
                    </p>
                  </div>

                  <!-- Guidance -->
                  <div class="mt-auto">
                    <p class="font-roboto text-[8px] text-navy/40 uppercase tracking-wider font-bold mb-1">
                      Guidance
                    </p>
                    <p class="font-roboto text-gray-600 text-[10px] leading-snug">
                      {{ nutrient.actionable_guidance }}
                    </p>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Data resources -->
      <div class="mt-8 pt-6 border-t border-gray-200 text-[11px] text-ash">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">
          Data Resources Used
        </p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Children Macronutrients:</span>
            <a
              href="https://www.eatforhealth.gov.au/nutrient-reference-values/nutrients"
              target="_blank"
              rel="noopener"
              class="hover:text-sky-active underline decoration-gray-300 underline-offset-2"
            >
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
  Droplet,
  Beef,
  Wheat,
  Activity,
  Zap
} from 'lucide-vue-next'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase || 'http://localhost:8000'

interface NutrientData {
  id: number
  age: string
  nutrient: string
  goal: string
  portion_guide: string
  rationale_summary: string
  actionable_guidance: string
}

const { data: macronutrientsData, pending } = await useFetch<NutrientData[]>(
  `${apiBase}/recommended-macronutrients`
)

const ageImageMap: Record<string, string> = {
  '0-6 months': '/images/boy-1.png',
  '7-12 months': '/images/boy-2.png',
  '1-3 years': '/images/boy-3.png',
  '4-8 years': '/images/boy-4.png',
  '9-13 years': '/images/boy-5.png'
}

const ageOrder = ['0-6 months', '7-12 months', '1-3 years', '4-8 years', '9-13 years']

const getGroupName = (age: string) => {
  if (age.includes('0-6')) return 'Newborns'
  if (age.includes('7-12')) return 'Infants'
  if (age.includes('1-3')) return 'Toddlers'
  if (age.includes('4-8')) return 'Young Kids'
  if (age.includes('9-13')) return 'Pre-Teens'
  return 'Children'
}

const ageGroups = computed(() => {
  if (!macronutrientsData.value) return []
  const uniqueAges = Array.from(new Set(macronutrientsData.value.map(item => item.age)))
  uniqueAges.sort((a, b) => {
    const aIndex = ageOrder.indexOf(a)
    const bIndex = ageOrder.indexOf(b)
    return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex)
  })
  return uniqueAges.map(age => ({ label: age, img: ageImageMap[age] || '/images/boy-5.png' }))
})

const selectedGroupLabel = ref('0-6 months')
const fillTrigger = ref(false)

const selectedGroupImage = computed(() => ageImageMap[selectedGroupLabel.value] || '/images/boy-5.png')

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
  setTimeout(() => { fillTrigger.value = true }, 100)
}

onMounted(() => {
  setTimeout(() => { fillTrigger.value = true }, 300)
})

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
</script>

<style scoped>
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

.slide-fade-enter-active {
  transition: all 0.45s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.slide-fade-leave-active {
  transition: all 0.25s ease-in;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
</style>
