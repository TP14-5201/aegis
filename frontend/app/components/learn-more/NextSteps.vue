<template>
  <section class="w-full bg-white py-12 lg:py-20">
    <div class="section-inner">
      <!-- Header Area -->
      <div class="mt-5 grid items-end gap-8 lg:grid-cols-[minmax(0,800px)_300px] lg:justify-between mb-14">
        <div class="flex-1">
          <div class="flex items-center gap-4 mb-4">
            <span class="font-volkhov text-[48px] font-bold leading-none text-[#DF6951] lg:text-[60px]">04</span>
            <span
              class="font-body text-[14px] font-semibold uppercase tracking-[0.18em] text-[#3D687C] lg:text-[16px]">FINDING
              SUPPORT. NEXT ACTION</span>
          </div>
          <h2 class="mt-5 font-volkhov text-[48px] font-semibold leading-[0.95] text-black sm:text-[60px] lg:text-[64px]">
            Ready to take <span class="text-[#cd5005] italic font-normal">the next step?</span>
          </h2>
        </div>
        <div class="border-l border-[#C6C6CD] pl-7 pb-1">
          <p class="font-roboto text-gray-700 text-[16px] lg:text-[18px] leading-relaxed">
            Three direct routes - pick the one closest to where you are right now.
          </p>
        </div>
      </div>

      <!-- Main Card -->
      <div class="w-full bg-[#292D3E] rounded-[32px] p-6 sm:p-8 lg:p-14 relative shadow-soft">
        <div class="flex flex-col relative">
          <!-- Vertical Line -->
          <div class="absolute left-[29.5px] top-[40px] bottom-[40px] w-[1px] bg-coral/40 hidden md:block"></div>

          <!-- Items -->
          <div v-for="(item, index) in steps" :key="index"
            class="relative flex flex-col md:flex-row md:items-center gap-6 md:gap-10 py-8 border-b border-white/10 last:border-0">
            <!-- Number Circle -->
            <div
              class="w-[60px] h-[60px] rounded-full border border-[#FFB59F] flex items-center justify-center shrink-0 bg-[#292D3E] z-10 relative mx-auto md:mx-0">
              <span class="text-[#FFDBD1] font-volkhov font-bold text-[20px]">0{{ index + 1 }}</span>
            </div>

            <!-- Text Content -->
            <div class="flex-1 text-center md:text-left">
              <h3 class="text-[#EEF0FF] font-volkhov font-bold text-[22px] lg:text-[26px] mb-2">{{ item.title }}</h3>
              <p class="text-[#DCE2F9] font-roboto text-[15px] lg:text-[16px]">{{ item.desc }}</p>
            </div>

            <!-- Button -->
            <NuxtLink :to="item.to"
              class="shrink-0 bg-white hover:bg-[#F8F9FF] text-[#96432A] font-roboto font-bold text-[15px] py-4 px-6 lg:px-8 rounded-[12px] transition-transform duration-300 hover:scale-[1.03] inline-block text-center shadow-button w-full md:w-auto min-w-[240px]">
              {{ item.ctaLabel }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  {
    title: 'Find Food Banks near me.',
    desc: 'Free food support open right now within 5 km of you.',
    to: '/food-banks',
    ctaLabel: 'Find Nearby Food Banks',
  },
  {
    title: 'Find groceries with nutritional values',
    desc: "Tell us your needs and we'll find you the right groceries.",
    to: '/get-food',
    ctaLabel: 'Explore Groceries',
  },
  {
    title: 'Know more about nutrition.',
    desc: "Simple guides for your family's health",
    to: '/nutrition-guide',
    ctaLabel: 'Learn about Nutrition',
  },
]
</script>