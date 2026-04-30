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
        Malnutrition affects Victorian children differently across age groups.
        Each photo represents the relative impact on that age band.
      </p>

      <!-- Bar-chart-style age groups -->
      <div class="mt-10 overflow-x-auto pb-4 -mx-5 px-5">
        <div class="flex items-end justify-between gap-4 sm:gap-6 lg:gap-8 min-w-[600px] lg:min-w-0">
          <figure v-for="g in ageGroups" :key="g.label"
            class="flex flex-col items-center text-center shrink-0 cursor-pointer group"
            :style="{ width: 'clamp(80px, 12vw, 180px)' }" @click="selectedGroupLabel = g.label">

            <!-- Image Container (handles hover effect) -->
            <div
              class="relative w-full h-[300px] flex justify-center items-end transition-transform duration-300 group-hover:-translate-y-2 group-hover:drop-shadow-[0_10px_15px_rgba(27,30,69,0.3)]">

              <!-- Mask Container (keeps logo shape constant) -->
              <div class="absolute inset-0 w-full h-full" :style="{
                maskImage: `url(${g.img})`,
                WebkitMaskImage: `url(${g.img})`,
                maskSize: 'contain',
                WebkitMaskSize: 'contain',
                maskPosition: 'bottom center',
                WebkitMaskPosition: 'bottom center',
                maskRepeat: 'no-repeat',
                WebkitMaskRepeat: 'no-repeat'
              }">

                <!-- Light Blue Base (#B5DCFF) -->
                <div class="absolute inset-0 w-full h-full bg-[#B5DCFF] transition-opacity duration-300"
                  :class="selectedGroupLabel === g.label ? 'opacity-100' : 'opacity-80'"></div>

                <!-- Navy Blue Fill (#1B1E45) -->
                <div class="absolute bottom-0 left-0 w-full bg-[#1B1E45] transition-all duration-1000 ease-out"
                  :style="{ height: selectedGroupLabel === g.label ? '100%' : '0%' }"></div>
              </div>
            </div>

            <figcaption
              class="mt-4 font-roboto text-[16px] lg:text-[20px] font-semibold leading-tight transition-colors duration-300"
              :class="selectedGroupLabel === g.label ? 'scale-110' : ''">
              <span class="block transition-colors duration-300"
                :class="selectedGroupLabel === g.label ? 'text-navy' : 'text-[#525252]'">{{ g.label }}</span>
              <span class="text-gray-500 text-sm lg:text-base font-normal">{{ g.range }}</span>
            </figcaption>
          </figure>
        </div>
      </div>

      <!-- Stats panel: dynamically updated based on selection -->
      <div
        class="mt-10 lg:mt-14 grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] gap-0 rounded-[20px] overflow-hidden shadow-[0px_10px_30px_0px_rgba(0,0,0,0.1)] transition-all duration-500">
        <div
          class="bg-[#B5DCFF] p-8 lg:p-10 flex flex-col items-center justify-center text-center transition-colors duration-500"
          :class="selectedGroupLabel === 'Infants' ? 'bg-[#D8EDFF]' : 'bg-[#B5DCFF]'">
          <p class="font-roboto font-extrabold text-navy text-[48px] lg:text-[64px] leading-none">
            {{ displayPercentage }}%
          </p>
          <p class="mt-2 font-roboto font-semibold text-navy text-[24px] lg:text-[32px] leading-tight">
            Malnourished
          </p>
        </div>
        <div class="bg-[#F4F4F9] p-8 lg:p-10 flex items-center relative overflow-hidden">
          <transition name="slide-fade" mode="out-in">
            <p :key="selectedGroup?.label"
              class="font-roboto text-[18px] lg:text-[22px] text-gray-700 leading-relaxed min-h-[80px]">
              {{ selectedGroup?.description || '' }}
            </p>
          </transition>
        </div>
      </div>

      <!-- Data resources -->
      <div class="mt-10 lg:mt-12 pt-6 border-t border-gray-200 text-[11px] text-ash">
        <p class="font-bold uppercase tracking-widest mb-3 text-navy/60">Data Resources Used</p>
        <div class="flex flex-wrap gap-x-8 gap-y-3">
          <span class="flex items-center gap-2">
            <span class="font-semibold text-navy/70">Children Malnourishment:</span>
            <a href="https://vahi.vic.gov.au/reports/victorian-population-health-survey-2023" target="_blank"
              rel="noopener" class="hover:text-sky-active underline decoration-gray-300 underline-offset-2">
              VCHWS Summary Findings 2021 (Victorian Child Health and Wellbeing Survey)
            </a>
          </span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const ageGroups = [
  {
    label: 'Infants',
    range: '(0-1)',
    img: '/images/children-infant.png',
    percentage: 12,
    description: "Infants in Victoria aren't getting adequate nutrition — putting their brain development and immune system at serious risk."
  },
  {
    label: 'Toddlers',
    range: '(1-3)',
    img: '/images/children-toddler.png',
    percentage: 18,
    description: "Toddlers face significant risks of stunting and delayed cognitive development due to food insecurity, affecting their early learning capabilities."
  },
  {
    label: 'Pre-School',
    range: '(3-5)',
    img: '/images/children-preschool.png',
    percentage: 15,
    description: "Pre-schoolers without reliable access to nutritious food often experience weakened immune systems and lower energy levels for active play."
  },
  {
    label: 'School age',
    range: '(5-12)',
    img: '/images/children-school-age.png',
    percentage: 22,
    description: "School-age children struggle with concentration, academic performance, and physical activity when facing hunger during the school day."
  },
  {
    label: 'Adolescent',
    range: '(13-17)',
    img: '/images/children-adolescent.png',
    percentage: 19,
    description: "Adolescents dealing with food insecurity often face increased mental health challenges, social anxiety, and developmental hurdles."
  },
]

const selectedGroupLabel = ref('Infants')

const selectedGroup = computed(() => {
  return ageGroups.find(g => g.label === selectedGroupLabel.value)
})

const displayPercentage = ref(12)

watch(() => selectedGroup.value?.percentage, (newVal) => {
  if (newVal === undefined) return

  const start = displayPercentage.value
  const end = newVal
  const duration = 600 // ms
  const startTime = performance.now()

  const animate = (time: number) => {
    const elapsed = time - startTime
    const progress = Math.min(elapsed / duration, 1)

    // easeOutCubic
    const easeProgress = 1 - Math.pow(1 - progress, 3)

    displayPercentage.value = Math.round(start + (end - start) * easeProgress)

    if (progress < 1) {
      requestAnimationFrame(animate)
    }
  }

  requestAnimationFrame(animate)
})
</script>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.4s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
  transform: translateY(15px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-15px);
  opacity: 0;
}
</style>
