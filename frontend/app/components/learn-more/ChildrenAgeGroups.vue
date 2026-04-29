<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <!-- Heading -->
      <p class="font-roboto font-bold text-coral text-[16px] lg:text-[20px] tracking-[2px] uppercase">
        The Children
      </p>
      <h2
        class="mt-3 font-volkhov font-bold text-navy
               text-[28px] sm:text-[36px] lg:text-[48px] leading-tight"
      >
        No child should grow up hungry
      </h2>
      <p class="mt-4 font-roboto text-[16px] lg:text-[20px] text-black max-w-3xl leading-relaxed">
        Malnutrition affects Victorian children differently across age groups.
        Each photo represents the relative impact on that age band.
      </p>

      <!-- Bar-chart-style age groups (5 photos at staggered heights) -->
      <!-- On mobile: horizontally scrollable; on desktop: justify-between baseline-aligned -->
      <div class="mt-10 overflow-x-auto pb-4 -mx-5 px-5">
        <div class="flex items-end justify-between gap-4 sm:gap-6 lg:gap-8 min-w-[600px] lg:min-w-0">
          <figure
            v-for="g in ageGroups"
            :key="g.label"
            class="flex flex-col items-center text-center shrink-0"
            :style="{ width: 'clamp(80px, 12vw, 180px)' }"
          >
            <img
              :src="g.img"
              :alt="g.label"
              class="object-contain"
              :style="{ height: g.height + 'px', width: g.width + 'px' }"
              loading="lazy"
            />
            <figcaption class="mt-3 font-roboto text-[16px] lg:text-[20px] font-semibold leading-tight">
              <span class="text-coral block">{{ g.label }}</span>
              <span class="text-navy">{{ g.range }}</span>
            </figcaption>
          </figure>
        </div>
      </div>

      <!-- Stats panel: 12% Malnourished + supporting text -->
      <div class="mt-10 lg:mt-14 grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)] gap-0 rounded-[20px] overflow-hidden shadow-nav">
        <div class="bg-sky/60 p-8 lg:p-10 flex flex-col items-center justify-center text-center">
          <p class="font-roboto font-extrabold text-black text-[48px] lg:text-[64px] leading-none">
            12%
          </p>
          <p class="mt-2 font-roboto font-semibold text-black text-[24px] lg:text-[32px] leading-tight">
            Malnourished
          </p>
        </div>
        <div class="bg-[#d9d9d94a] p-8 lg:p-10 flex items-center">
          <p class="font-roboto text-[18px] lg:text-[22px] text-black leading-relaxed">
            Infants in Victoria aren't getting adequate nutrition — putting their
            brain development and immune system at serious risk.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const ageGroups = [
  { label: 'Infants',    range: '(0-1)',   img: '/images/children-infant.png', height: 600, width: 800 },
  { label: 'Toddlers',   range: '(1-3)',   img: '/images/children-toddler.png', height: 600, width: 600  },
  { label: 'Pre-School', range: '(3-5)',   img: '/images/children-preschool.png', height: 600, width: 600 },
  { label: 'School age', range: '(5-12)',  img: '/images/children-school-age.png', height: 600, width: 600 },
  { label: 'Adolescent', range: '(13-17)', img: '/images/children-adolescent.png', height: 600, width: 600 },
]
</script>
