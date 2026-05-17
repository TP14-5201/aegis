<template>
  <section class="w-full bg-white">
    <div class="max-w-8xl mx-auto px-5 lg:px-12
             grid lg:grid-cols-2 gap-12
             min-h-[70vh] lg:min-h-[80vh]
             items-center">
      <!-- LEFT CONTENT -->
      <div class="flex flex-col justify-center">
        <p class="text-sm font-bold uppercase tracking-wider text-[#DF6951]">
          Under Development
        </p>

        <h1 class="font-volkhov font-bold text-navy
                 text-[42px] lg:text-[64px]
                 leading-[0.95]">
          Nutritious meals,<br />
          gentle on your <span class="text-clay">wallet</span>
        </h1>

        <p class="mt-5 max-w-xl text-black text-[18px] lg:text-[21px] leading-tight">
          Tell us your budget, family size, and what you love to cook.
          We'll hand you the cheapest wholesome ingredients — with smart swaps
          and quiet little health perks.
        </p>

        <a href="#grocery-planner" class="group mt-6 inline-flex items-center justify-center gap-3
                bg-sky rounded-[20px]
                h-[64px] lg:h-[74px]
                px-8 lg:px-12
                font-roboto font-extrabold text-navy-deep
                text-[18px] lg:text-[24px]
                max-w-[400px]
                w-full
                shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                transition-all duration-300 ease-out
                hover:-translate-y-1
                active:translate-y-0">
          Find my ingredients
        </a>

        <div class="mt-7 flex flex-wrap gap-4 text-sm text-gray-600">
          <span>♡ Heart-healthy</span>
          <span>☾ Better sleep</span>
          <span>✧ Stress easing</span>
        </div>
      </div>

      <!-- RIGHT VISUAL -->
      <div class="relative flex min-h-[360px] lg:min-h-[560px] items-end justify-center">
        <img src="/images/get-food/Vector(1).webp" alt=""
          class="absolute bottom-0 left-1/2 z-0 w-[85%] max-w-[360px] -translate-x-1/2 sm:w-[90%] sm:max-w-[500px] lg:w-[120%] lg:max-w-[760px]" />

        <img src="/images/get-food/getfoodhero.webp" alt="Basket of groceries"
          class="relative z-10 w-full max-w-[360px] sm:max-w-[500px] lg:max-w-[650px]" />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const benefits = ['Heart-healthy', 'Better sleep', 'Stress easing']
</script>
