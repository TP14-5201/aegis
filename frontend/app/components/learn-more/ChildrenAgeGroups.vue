<template>
  <section id="children-age-groups" class="bg-white pb-16 pt-8 lg:pb-20 lg:pt-10">
    <div class="section-inner flex flex-col">
      <!-- Heading Section -->
      <div class="w-full">
        <div class="flex items-center gap-4">
          <span class="font-volkhov text-[42px] font-bold leading-none text-[#DF6951]">
            02
          </span>

          <span class="font-roboto text-[18px] font-bold uppercase tracking-[0.12em] text-[#396477]">
            The Children
          </span>
        </div>

        <div class="mt-5 grid items-end gap-8 lg:grid-cols-[minmax(0,760px)_320px] lg:justify-between">
          <h2 class="font-volkhov text-[48px] font-bold leading-[0.95] text-black sm:text-[60px] lg:text-[64px]">
            What every child needs-
            <br />
            <span class="font-normal italic text-[#DF6951]">
              at every stage of growth
            </span>
          </h2>

          <div class="border-[#C6C6CD] lg:border-l lg:pl-6 lg:pb-2">
            <p class="font-roboto text-[15px] leading-6 text-[#45464D]">
              Nutrition needs shift as children grow. Tap a stage to see the recommended daily intake of nutrients.
            </p>
          </div>
        </div>
      </div>

      <!-- Age Group Selection Tabs -->
      <div
        class="w-full bg-[#E6EEFF] rounded-[32px] px-4 sm:px-8 pt-8 pb-4 mt-12 flex flex-wrap justify-center sm:justify-between items-end gap-y-8 gap-x-4">
        <button v-for="g in ageGroups" :key="g.label"
          class="flex flex-col items-center transition-all duration-500 group relative w-[110px] sm:w-[140px] lg:w-[180px]"
          :class="selectedGroupLabel === g.label ? 'scale-110' : 'opacity-70 hover:opacity-100 hover:scale-105'"
          @click="selectGroup(g.label, true)">
          <div class="h-[130px] sm:h-[170px] lg:h-[220px] w-full flex items-end justify-center mb-2">
            <img :src="g.img" class="object-contain transition-all duration-500 origin-bottom" :class="[
              selectedGroupLabel === g.label ? '' : 'grayscale group-hover:grayscale-0',
              getImageScale(g.label)
            ]" alt="Child silhouette" />
          </div>
          <div class="text-center">
            <h4
              class="font-roboto font-bold text-[13px] sm:text-[15px] lg:text-[17px] leading-tight transition-colors duration-300"
              :class="selectedGroupLabel === g.label ? 'text-[#396477]' : 'text-navy/60'">
              {{ getGroupName(g.label) }}
            </h4>
            <p class="font-roboto font-semibold text-[11px] sm:text-[13px] lg:text-[15px] mt-1 transition-colors duration-300"
              :class="selectedGroupLabel === g.label ? 'text-navy/60' : 'text-gray-400'">
              {{ g.label }}
            </p>
          </div>
        </button>
      </div>

      <!-- Main Interactive Display -->
      <div id="age-group-details" class="mt-8 grid w-full items-stretch gap-4 lg:grid-cols-[240px_minmax(0,1fr)]">
        <!-- LEFT: Currently Viewing Card -->
        <div
          class="flex h-full min-h-[456px] w-full flex-col overflow-hidden rounded-[20px] border border-[#C6C6CD] bg-[#E6EEFF] p-6 shadow-[0_8px_18px_rgba(19,27,46,0.16)]">
          <div class="relative z-10">
            <p class="font-roboto font-bold text-[12px] tracking-[2px] text-[#396477] uppercase">
              Currently viewing
            </p>
            <h3 class="mt-1 font-playfair text-[36px] font-bold leading-tight text-[#0D1C2E]">
              {{ getGroupName(selectedGroupLabel) }}
            </h3>

            <p class="font-roboto text-[#45464D] text-[15px] leading-relaxed mt-6">
              {{ groupDescriptions[selectedGroupLabel] || 'Proper nutrition is critical during this stage to ensure \
              healthy physical and cognitive development.' }}
            </p>
          </div>

          <!-- Silhouette -->
          <div class="flex-1 w-full flex justify-center items-end mt-6 pointer-events-none opacity-40 z-0">
            <div class="w-[240px] h-[220px] lg:w-[260px] lg:h-[240px]">
              <transition name="logo-fade" mode="out-in" @after-enter="onLogoEnter">
                <div :key="selectedGroupLabel" class="relative w-full h-full flex justify-center items-center">
                  <div class="absolute inset-0 w-full h-full" :style="{
                    maskImage: `url(${selectedGroupImage})`,
                    WebkitMaskImage: `url(${selectedGroupImage})`,
                    maskSize: 'contain',
                    WebkitMaskSize: 'contain',
                    maskPosition: 'center',
                    WebkitMaskPosition: 'center',
                    maskRepeat: 'no-repeat',
                    WebkitMaskRepeat: 'no-repeat'
                  }">
                    <div class="absolute inset-0 w-full h-full bg-[#396477] opacity-80"></div>
                    <div class="absolute bottom-0 left-0 w-full bg-navy transition-all duration-[1500ms] ease-out"
                      :style="{ height: fillTrigger ? '100%' : '0%' }"></div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>

        <!-- RIGHT: Macronutrient Cards Grid -->
        <div class="flex-1 w-full relative">
          <div v-if="pending" class="absolute inset-0 flex justify-center items-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-navy"></div>
          </div>

          <transition name="slide-fade" mode="out-in">
            <div v-if="!pending" :key="selectedGroupLabel"
              class="grid h-full w-full grid-cols-1 gap-5 md:grid-cols-2 md:grid-rows-3">
              <div v-for="(nutrient, index) in selectedGroupNutrients" :key="nutrient.id"
                class="group flex min-h-[140px] overflow-hidden rounded-[18px] border border-[#C6C6CD] bg-white shadow-[0_8px_18px_rgba(19,27,46,0.16)] transition-all duration-300 hover:-translate-y-1"
                :style="{ animationDelay: `${index * 100}ms` }">
                <div class="flex flex-1 flex-col justify-center p-6">
                  <h4 class="font-playfair font-semibold text-[18px] text-[#396477]">
                    {{ nutrient.nutrient }}
                  </h4>
                  <p
                    class="mt-1 font-playfair text-[32px] font-bold leading-none tracking-tight text-[#0D1C2E]">
                    {{ extractValue(nutrient.goal) }}
                  </p>
                  <p class="font-roboto text-[11px] lg:text-[12px] text-[#45464D] mt-3 line-clamp-2 leading-snug pr-2">
                    {{ nutrient.actionable_guidance || nutrient.portion_guide }}
                  </p>
                </div>

                <!-- Right Side Image Placeholder -->
                <div class="h-full w-[42%] shrink-0 overflow-hidden bg-gray-100">
                  <img :src="getNutrientImage(nutrient.nutrient, selectedGroupLabel)"
                    class="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity group-hover:scale-105 duration-500"
                    alt="Nutrient placeholder" />
                </div>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- Bottom Banner -->
      <div
        class="mt-5 flex w-full flex-col items-center justify-between gap-5 rounded-[16px] border border-[#131B2E] bg-white px-6 py-5 shadow-[0_8px_18px_rgba(19,27,46,0.12)] lg:flex-row">
        <div>
          <h4 class="font-playfair font-bold text-[24px] lg:text-[28px] text-navy text-center lg:text-left">Unsure what
            your child needs right now ?</h4>
          <p class="font-roboto text-[#45464D] text-[15px] mt-2 text-center lg:text-left">
            Learn exactly what to feed your child for their development and explore what habits are good for them
          </p>
        </div>
        <NuxtLink to="/nutrition-guide">
          <button
            class="h-[54px] rounded-[8px] bg-black px-8 font-roboto text-[14px] font-semibold text-white transition hover:bg-[#131B2E]">
            Explore Nutrition Guide
          </button>
        </NuxtLink>
      </div>

      <!-- Data resources -->
      <div class="w-full mt-10 pt-6 border-t border-gray-200 text-[11px] text-[#6B7280]">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">
          Data Resources Used
        </p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Children Macronutrients:</span>
            <a href="https://www.eatforhealth.gov.au/nutrient-reference-values/nutrients" target="_blank" rel="noopener"
              class="hover:text-[#396477] underline decoration-gray-300 underline-offset-2">
              NHMRC Nutrient Reference Values
            </a>
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useFetch, useRuntimeConfig } from '#app'

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

const { data: macronutrientsData, pending } = useFetch<NutrientData[]>(
  `${apiBase}/recommended-macronutrients`,
  { lazy: true }
)

const ageImageMap: Record<string, string> = {
  '0-6 months': '/images/learn-more/children-newborn.webp',
  '7-12 months': '/images/learn-more/children-infant.webp',
  '1-3 years': '/images/learn-more/children-toddler.webp',
  '4-8 years': '/images/learn-more/children-preschool.webp',
  '9-13 years': '/images/learn-more/children-school-age.webp',
}

const nutrientImageMap: Record<string, Record<string, string>> = {
  '0-6 months': {
    carbohydrate: '/images/learn-more/macro/nb-1.webp',
    energy: '/images/learn-more/macro/nb-2.webp',
    protein: '/images/learn-more/macro/nb-3.webp',
    fibre: '/images/learn-more/macro/nb-4.webp',
    fat: '/images/learn-more/macro/nb-5.webp',
    fluid: '/images/learn-more/macro/nb-6.webp',
  },
  '7-12 months': {
    carbohydrate: '/images/learn-more/macro/in-1.webp',
    energy: '/images/learn-more/macro/in-2.webp',
    protein: '/images/learn-more/macro/in-3.webp',
    fibre: '/images/learn-more/macro/in-4.webp',
    fat: '/images/learn-more/macro/in-5.webp',
    fluid: '/images/learn-more/macro/in-6.webp',
  },
  '1-3 years': {
    carbohydrate: '/images/learn-more/macro/td-1.webp',
    energy: '/images/learn-more/macro/td-2.webp',
    protein: '/images/learn-more/macro/td-3.webp',
    fibre: '/images/learn-more/macro/td-4.webp',
    fat: '/images/learn-more/macro/td-5.webp',
    fluid: '/images/learn-more/macro/td-6.webp',
  },
  '4-8 years': {
    carbohydrate: '/images/learn-more/macro/yc-1.webp',
    energy: '/images/learn-more/macro/yc-2.webp',
    protein: '/images/learn-more/macro/yc-3.webp',
    fibre: '/images/learn-more/macro/yc-4.webp',
    fat: '/images/learn-more/macro/yc-5.webp',
    fluid: '/images/learn-more/macro/yc-6.webp',
  },
  '9-13 years': {
    carbohydrate: '/images/learn-more/macro/pt-1.webp',
    energy: '/images/learn-more/macro/pt-2.webp',
    protein: '/images/learn-more/macro/pt-3.webp',
    fibre: '/images/learn-more/macro/pt-4.webp',
    fat: '/images/learn-more/macro/pt-5.webp',
    fluid: '/images/learn-more/macro/pt-6.webp',
  },
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

const groupDescriptions: Record<string, string> = {
  '0-6 months': "Breastmilk or formula provides all necessary nutrients. Iron stores from birth begin to deplete slowly.",
  '7-12 months': "Solids begin to complement milk. Iron-rich foods are critical from 6 months as babies' iron stores deplete.",
  '1-3 years': "Rapid growth continues. Focus on establishing healthy eating habits and providing balanced, nutrient-dense meals.",
  '4-8 years': "Energy needs increase with activity levels. Calcium and protein are essential for developing strong bones and muscles.",
  '9-13 years': "Pre-puberty growth spurts require significant energy and nutrients. Calcium and iron intake become increasingly important."
}

const ageGroups = computed(() => {
  if (!macronutrientsData.value) return []

  const uniqueAges = Array.from(new Set(macronutrientsData.value.map(item => item.age)))

  uniqueAges.sort((a, b) => {
    const aIndex = ageOrder.indexOf(a)
    const bIndex = ageOrder.indexOf(b)

    return (aIndex === -1 ? 999 : aIndex) - (bIndex === -1 ? 999 : bIndex)
  })

  return uniqueAges.map(age => ({
    label: age,
    img: ageImageMap[age]
  }))
})

// Returns a height percentage class based on the age group to simulate growth
const getImageScale = (label: string) => {
  if (label.includes('0-6')) return 'h-[40%]'
  if (label.includes('7-12')) return 'h-[55%]'
  if (label.includes('1-3')) return 'h-[70%]'
  if (label.includes('4-8')) return 'h-[85%]'
  return 'h-full' // 9-13
}

const selectedGroupLabel = ref('7-12 months')
const fillTrigger = ref(false)

const selectedGroupImage = computed(() => {
  return ageImageMap[selectedGroupLabel.value]
})

const selectedGroupNutrients = computed(() => {
  if (!macronutrientsData.value) return []
  return macronutrientsData.value.filter(item => item.age === selectedGroupLabel.value)
})

const selectGroup = async (label: string, shouldScroll = false) => {
  if (selectedGroupLabel.value !== label) {
    fillTrigger.value = false
    selectedGroupLabel.value = label
  }

  if (shouldScroll) {
    await nextTick()

    const el = document.getElementById('age-group-details')
    if (!el) return

    const yOffset = -130
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset

    window.scrollTo({
      top: Math.max(0, y),
      behavior: 'smooth',
    })
  }
}

const onLogoEnter = () => {
  setTimeout(() => {
    fillTrigger.value = true
  }, 100)
}

onMounted(() => {
  setTimeout(() => {
    fillTrigger.value = true
  }, 300)
})

// Extract just the number and unit from goal strings like "2,700 kJ/d" -> "2,700 kJ"
const extractValue = (goal: string | undefined) => {
  if (!goal) return ''
  return goal.split('/')[0].trim()
}

// Generate real images based on nutrient name
const getNutrientKey = (nutrient: string) => {
  const n = (nutrient || '').toLowerCase()

  if (n.includes('carbohydrate')) return 'carbohydrate'
  if (n.includes('energy')) return 'energy'
  if (n.includes('protein')) return 'protein'
  if (n.includes('fibre') || n.includes('fiber')) return 'fibre'
  if (n.includes('fat')) return 'fat'
  if (n.includes('fluid')) return 'fluid'

  return 'carbohydrate'
}

const getNutrientImage = (nutrient: string, age = selectedGroupLabel.value) => {
  const key = getNutrientKey(nutrient)
  return nutrientImageMap[age]?.[key] || '/images/learn-more/macro/carbohydrate.webp'
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