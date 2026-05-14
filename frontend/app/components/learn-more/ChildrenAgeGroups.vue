<template>
  <section class="w-full bg-white py-12 lg:py-20 flex justify-center">
    <div class="w-full max-w-[1280px] px-5 lg:px-12 flex flex-col items-center">
      <!-- Heading Section -->
      <div class="w-full flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
        <div class="flex-1">
          <div class="flex items-center gap-4">
            <span class="text-[#DF6951] text-[40px] md:text-[56px] font-playfair font-bold leading-none">02</span>
            <span class="text-[#396477] text-sm md:text-base font-bold tracking-[2px] uppercase">The Children</span>
          </div>
          <h2 class="mt-4 text-[40px] md:text-[56px] lg:text-[64px] font-playfair font-bold text-navy leading-[1.1]">
            What every child needs- <br />
            <span class="italic text-[#DF6951] font-normal">at every stage of growth</span>
          </h2>
        </div>
        <div class="lg:w-[300px] lg:border-l lg:border-[#C6C6CD] lg:pl-6 pt-2">
          <p class="text-[#45464D] text-sm md:text-base leading-relaxed">
            Nutrition needs shift as children grow. Tap a stage to see the recommended daily intake of nutrients.
          </p>
        </div>
      </div>

      <!-- Age Group Selection Tabs -->
      <div
        class="w-full bg-[#E6EEFF] rounded-[32px] px-4 sm:px-8 pt-8 pb-4 mt-12 flex flex-wrap justify-center sm:justify-between items-end gap-y-8 gap-x-4">
        <button v-for="g in ageGroups" :key="g.label"
          class="flex flex-col items-center transition-all duration-500 group relative w-[100px] sm:w-[120px] lg:w-[160px]"
          :class="selectedGroupLabel === g.label ? 'scale-110' : 'opacity-70 hover:opacity-100 hover:scale-105'"
          @click="selectGroup(g.label)">
          <div class="h-[100px] sm:h-[140px] lg:h-[180px] w-full flex items-end justify-center mb-3">
            <img :src="g.img" class="object-contain transition-all duration-500 origin-bottom" :class="[
              selectedGroupLabel === g.label ? '' : 'grayscale group-hover:grayscale-0',
              getImageScale(g.label)
            ]" alt="Child silhouette" />
          </div>
          <div class="text-center">
            <h4
              class="font-playfair font-bold text-[16px] sm:text-[18px] lg:text-[22px] leading-tight transition-colors duration-300"
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
      <div class="w-full mt-8 flex flex-col lg:flex-row gap-8">
        <!-- LEFT: Currently Viewing Card -->
        <div
          class="w-full lg:w-[320px] xl:w-[380px] bg-[#E6EEFF] rounded-[32px] p-8 flex flex-col relative overflow-hidden min-h-[450px]">
          <div class="relative z-10">
            <p class="font-roboto font-bold text-[12px] tracking-[2px] text-[#396477] uppercase">
              Currently viewing
            </p>
            <h3 class="font-playfair font-bold text-[36px] lg:text-[42px] text-navy mt-1 leading-tight">
              {{ getGroupName(selectedGroupLabel) }}
            </h3>

            <p class="font-roboto text-[#45464D] text-[15px] leading-relaxed mt-6">
              {{ groupDescriptions[selectedGroupLabel] || 'Proper nutrition is critical during this stage to ensure \
              healthy physical and cognitive development.' }}
            </p>
          </div>

          <!-- Silhouette -->
          <div class="flex-1 w-full flex justify-center items-center mt-6 pointer-events-none opacity-40 z-0">
            <div class="w-[180px] h-[160px] lg:w-[150px] lg:h-[100px]">
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
              class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 w-full">
              <div v-for="(nutrient, index) in selectedGroupNutrients" :key="nutrient.id"
                class="bg-white border border-[#C6C6CD] rounded-[24px] overflow-hidden flex h-[160px] shadow-[0px_4px_12px_rgba(0,0,0,0.05)] hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 group"
                :style="{ animationDelay: `${index * 100}ms` }">
                <div class="p-5 flex-1 flex flex-col justify-center">
                  <h4 class="font-playfair text-[18px] lg:text-[20px] text-[#396477]">
                    {{ nutrient.nutrient }}
                  </h4>
                  <p
                    class="font-playfair font-bold text-[32px] lg:text-[38px] text-navy mt-1 leading-none tracking-tight">
                    {{ extractValue(nutrient.goal) }}
                  </p>
                  <p class="font-roboto text-[11px] lg:text-[12px] text-[#45464D] mt-3 line-clamp-2 leading-snug pr-2">
                    {{ nutrient.actionable_guidance || nutrient.portion_guide }}
                  </p>
                </div>

                <!-- Right Side Image Placeholder -->
                <div class="w-[40%] bg-gray-100 h-full overflow-hidden shrink-0">
                  <img :src="getNutrientImage(nutrient.nutrient)"
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
        class="w-full mt-12 border border-[#C6C6CD] rounded-[20px] p-6 lg:p-8 flex flex-col lg:flex-row justify-between items-center gap-6">
        <div>
          <h4 class="font-playfair font-bold text-[24px] lg:text-[28px] text-navy text-center lg:text-left">Unsure what
            your child needs right now ?</h4>
          <p class="font-roboto text-[#45464D] text-[15px] mt-2 text-center lg:text-left">
            Learn exactly what to feed your child for their development and explore what habits are good for them
          </p>
        </div>
        <NuxtLink to="/nutrition-guide">
          <button
            class="bg-black text-white px-8 py-4 rounded-[16px] font-roboto font-medium hover:bg-[#396477] transition-colors duration-300 whitespace-nowrap text-[15px]">
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
import { ref, computed, onMounted } from 'vue'
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
  '9-13 years': '/images/learn-more/children-school-age.webp'
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
const getNutrientImage = (nutrient: string) => {
  const n = (nutrient || '').toLowerCase()

  if (n.includes('energy')) return '/images/learn-more/energy.webp'
  if (n.includes('protein')) return '/images/learn-more/protein.webp'
  if (n.includes('fibre') || n.includes('fiber')) return '/images/learn-more/fibre.webp'
  if (n.includes('fluid')) return '/images/learn-more/fluid.webp'
  if (n.includes('fat')) return '/images/learn-more/fat.webp'
  if (n.includes('carbohydrate')) return '/images/learn-more/carbohydrate.webp'

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