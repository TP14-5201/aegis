<template>
  <section class="w-full bg-white pt-16 lg:pt-24 pb-20 lg:pb-24">
  <div class="max-w-8xl mx-auto px-5 lg:px-12 grid lg:grid-cols-2 gap-12 items-end">
    
    <!-- LEFT -->
    <div>
      <h1 class="font-volkhov font-bold text-navy text-[42px] lg:text-[64px] leading-[0.95]">
        Nutritious meals,<br />
        gentle on your <span class="text-clay">wallet</span>
      </h1>

      <p class="mt-5 max-w-xl text-black text-[18px] lg:text-[21px] leading-tight">
        Tell us your budget, family size, and what you love to cook.
        We'll hand you the cheapest wholesome ingredients - with smart swaps
        and quiet little health perks.
      </p>

      <a
        href="#grocery-planner"
        class="inline-flex mt-6 bg-[#B8DEFF] text-navy font-bold px-7 py-3 rounded-full"
      >
        Find my ingredients
      </a>

      <div class="mt-7 flex flex-wrap gap-4 text-sm text-gray-600">
        <span>♡ Heart-healthy</span>
        <span>☾ Better sleep</span>
        <span>✧ Stress easing</span>
      </div>
    </div>

    <!-- RIGHT -->
    <div class="relative mt-10 lg:mt-0 flex min-h-[520px] justify-center items-end">
      
      <img
        src="/images/get-food/Vector(1).png"
        class="absolute bottom-0 z-0 w-[120%] max-w-[760px]"
      />

      <img
        src="/images/get-food/getfoodhero.png"
        class="relative z-10 w-full max-w-[650px] translate-y-6"
      />

    </div>
  </div>
</section>
</template>

<script setup lang="ts">
const benefits = ['Heart-healthy', 'Better sleep', 'Stress easing']
</script>