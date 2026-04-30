<template>
  <section class="w-full bg-white">
    <div
      class="max-w-8xl mx-auto px-5 lg:px-12
             grid lg:grid-cols-2 gap-12
             min-h-[70vh] lg:min-h-[80vh]
             items-center"
    >
      <!-- LEFT CONTENT -->
      <div class="flex flex-col justify-center">
        <h1
          class="font-volkhov font-bold text-navy
                 text-[42px] lg:text-[64px]
                 leading-[0.95]"
        >
          Nutritious meals,<br />
          gentle on your <span class="text-clay">wallet</span>
        </h1>

        <p class="mt-5 max-w-xl text-black text-[18px] lg:text-[21px] leading-tight">
          Tell us your budget, family size, and what you love to cook.
          We'll hand you the cheapest wholesome ingredients — with smart swaps
          and quiet little health perks.
        </p>

        <a
          href="#grocery-planner"
          class="mt-6 inline-flex w-fit rounded-full bg-[#B8DEFF] px-7 py-3 font-bold text-navy"
        >
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
        <img
          src="/images/get-food/Vector(1).png"
          alt=""
          class="absolute bottom-0 left-1/2 z-0 w-[85%] max-w-[360px] -translate-x-1/2 sm:w-[90%] sm:max-w-[500px] lg:w-[120%] lg:max-w-[760px]"
        />

        <img
          src="/images/get-food/getfoodhero.png"
          alt="Basket of groceries"
          class="relative z-10 w-full max-w-[360px] sm:max-w-[500px] lg:max-w-[650px]"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const benefits = ['Heart-healthy', 'Better sleep', 'Stress easing']
</script>