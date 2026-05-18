<template>
  <section class="w-full bg-get-food-hero mt-nav min-h-[calc(100vh-72px)] flex items-center">
    <div class="section-inner py-16 lg:py-20">
      <div class="grid items-center gap-10 lg:grid-cols-[1.08fr_0.92fr]">

        <!-- LEFT CONTENT -->
        <div class="flex flex-col justify-center">
          <h1 class="heading-xl text-white">
            Nutritious meals,<br />
            gentle on your <span class="text-[#b5dcff]">wallet</span>
          </h1>

          <p class="body-copy mt-4 max-w-[560px] text-white/80">
            Tell us your budget, family size, and what you love to cook.
            We'll hand you the cheapest wholesome ingredients — with smart swaps
            and quiet little health perks.
          </p>

          <div class="mt-8">
            <a href="#grocery-planner" class="btn-dark">Find my ingredients</a>
          </div>

          <div class="mt-7 flex flex-wrap gap-3">
            <span class="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-sm text-white/70">♡ Heart-healthy</span>
            <span class="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-sm text-white/70">☾ Better sleep</span>
            <span class="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-sm text-white/70">✧ Stress easing</span>
          </div>
        </div>

        <!-- RIGHT VISUAL -->
        <div class="flex items-center justify-center lg:justify-end min-h-[320px] lg:min-h-[500px]">
          <img
            src="/images/get-food/Image (Healthy food) (1).png"
            alt="Healthy food bag"
            class="w-full max-w-[360px] sm:max-w-[460px] lg:max-w-[520px] object-contain"
          />
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
</script>
