<template>
  <section class="bg-[#e6eeff] px-6 py-12 lg:px-10">
    <div class="mx-auto max-w-[1200px]">
      <h2 class="text-center font-playfair text-[40px] font-bold leading-[50px] tracking-[-0.96px] text-[#0d1c2e] lg:text-[48px] lg:leading-[56px]">
        Shop Smarter, Eat Better
      </h2>

      <div class="mt-6 grid gap-4 xl:grid-cols-4 xl:grid-rows-[316px_206px]">
        <article class="large-feature-card">
          <div>
            <h3 class="font-playfair text-[32px] font-bold leading-[40px] text-[#0d1c2e]">
              Mastering the Weekly Grocery Shop
            </h3>

            <div class="mt-4 flex flex-col gap-4">
              <div v-for="tip in tips" :key="tip" class="flex gap-4">
                <img src="/images/landing/icon-1.png" alt="" class="mt-1 h-5 w-5 shrink-0" />
                <p class="font-jakarta text-[16px] leading-[24px] text-[#45464d]">
                  {{ tip }}
                </p>
              </div>
            </div>
          </div>

          <img
            src="/images/landing/landing-3.png"
            alt="Groceries on table"
            class="mt-6 h-[216px] w-full rounded-lg object-cover"
          />
        </article>

        <article class="small-tip-card bg-[#396477]">
          <img src="/images/landing/icon-2.png" alt="" class="h-[35px] w-[30px]" />
          <h3 class="mt-2 font-playfair text-[24px] font-semibold leading-[32px] text-white">
            Meal plan
          </h3>
          <p class="mt-2 font-jakarta text-[16px] leading-[24px] text-white/90">
            Tell us your weekly budget and family size - we'll build you a full meal plan
            using affordable, nutritious ingredients available near you.
          </p>
        </article>

        <article class="small-tip-card bg-[#131b2e]">
          <img src="/images/landing/icon-3.png" alt="" class="h-[33px] w-[33px]" />
          <h3 class="mt-2 font-playfair text-[24px] font-semibold leading-[32px] text-white">
            Substitutions
          </h3>
          <p class="mt-2 font-jakarta text-[16px] leading-[24px] text-white/90">
            Can't find an ingredient or need to swap it out? We'll suggest affordable
            alternatives that keep your meal just as nutritious.
          </p>
        </article>

        <article class="horizontal-highlight">
          <div>
            <h3 class="font-playfair text-[32px] font-bold leading-[40px] text-[#0d1c2e]">
              Groceries Costing Too Much?
            </h3>
            <p class="mt-3 font-jakarta text-[16px] leading-[24px] text-[#45464d]">
              Master budget-friendly shopping with weekly meal plans, smart swaps,
              and nutritional information.
            </p>
          </div>

          <NuxtLink to="/get-food" class="grocery-button">
            Build my Grocery List
          </NuxtLink>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const tips = [
  'Focus on bulk grains: Rice, oats, and lentils provide the base of most nutritious meals for pennies.',
  'Prioritize frozen vegetables: Often more nutritious and less waste than fresh produce.',
  'Plan meals around “The Three Ps”: Proteins, Produce, and Pantry Staples.',
]
</script>

<style scoped>
.font-playfair {
  font-family: 'Playfair Display', serif;
}

.font-jakarta {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.large-feature-card {
  border: 1px solid #c6c6cd4c;
  border-radius: 12px;
  background: #ffffff;
  padding: 24px;
  box-shadow: 0 1px 2px #0000000d;
}

@media (min-width: 1280px) {
  .large-feature-card {
    grid-column: span 2 / span 2;
    grid-row: span 2 / span 2;
  }

  .horizontal-highlight {
    grid-column: span 2 / span 2;
    margin-top: -42px;
  }
}

.small-tip-card {
  position: relative;
  margin-bottom: 60px;
  z-index: 1;
  overflow: hidden;
  min-height: 400px;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 2px #0000000d;
}

.horizontal-highlight {
  grid-column: span 2 / span 2;
  position: relative;
  z-index: 3;
  min-height: 206px;
  border: 1px solid #c6c6cd4c;
  border-radius: 12px;
  background: #ffffff;
  padding: 24px;
  box-shadow: 0 1px 2px #0000000d;
}

.horizontal-highlight h3 {
  max-width: 480px;
}

.horizontal-highlight p {
  max-width: 560px;
}

.grocery-button {
  position: absolute;
  right: 24px;
  bottom: 24px;
  display: inline-flex;
  height: 56px;
  width: 258px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #131b2e;
  padding: 16px 32px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 700;
  line-height: 28px;
  color: #ffffff;
}
@media (max-width: 1279px) {
  .large-feature-card,
  .horizontal-highlight {
    grid-column: auto;
    grid-row: auto;
  }

  .horizontal-highlight {
    padding-bottom: 96px;
  }

  .grocery-button {
    left: 24px;
    right: 24px;
    bottom: 24px;
    width: auto;
  }

  .small-tip-card {
    min-height: auto;
  }
}
</style>