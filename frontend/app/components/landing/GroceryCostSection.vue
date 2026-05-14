<template>
  <section class="section-large bg-chere-skySoft">
    <div class="section-inner grocery-inner">
      <h2 class="heading-lg text-center">
        Shop Smarter, Eat Better
      </h2>

      <div class="grocery-grid mt-6">
        <article class="large-feature-card">
          <div>
            <h3 class="font-display text-[32px] font-bold leading-[40px] text-chere-navy">
              Mastering the Weekly Grocery Shop
            </h3>

            <div class="mt-4 flex flex-col gap-4">
              <div v-for="tip in tips" :key="tip" class="flex gap-4">
                <img src="/images/landing/icon-1.png" alt="" class="mt-1 h-5 w-5 shrink-0" />
                <p class="font-body text-[16px] leading-6 text-chere-text">
                  {{ tip }}
                </p>
              </div>
            </div>
          </div>

          <img src="/images/landing/landing-3.png" alt="Groceries on table"
            class="mt-6 h-[216px] w-full rounded-lg object-cover" />
        </article>

        <article class="small-tip-card bg-chere-blue">
          <img src="/images/landing/icon-2.png" alt="" class="h-[35px] w-[30px]" />
          <h3 class="mt-2 font-display text-[24px] font-semibold leading-8 text-white">
            Meal plan
          </h3>
          <p class="mt-2 font-body text-[16px] leading-6 text-white/90">
            Tell us your weekly budget and family size - we'll build you a full meal plan
            using affordable, nutritious ingredients available near you.
          </p>
        </article>

        <article class="small-tip-card bg-chere-ink">
          <img src="/images/landing/icon-3.png" alt="" class="h-[33px] w-[33px]" />
          <h3 class="mt-2 font-display text-[24px] font-semibold leading-8 text-white">
            Substitutions
          </h3>
          <p class="mt-2 font-body text-[16px] leading-6 text-white/90">
            Can't find an ingredient or need to swap it out? We'll suggest affordable
            alternatives that keep your meal just as nutritious.
          </p>
        </article>

        <article class="horizontal-highlight">
          <div>
            <h3 class="font-display text-[32px] font-bold leading-[40px] text-chere-navy">
              Groceries Costing Too Much?
            </h3>
            <p class="mt-3 font-body text-[16px] leading-6 text-chere-text">
              Master budget-friendly shopping with weekly meal plans, smart swaps,
              and nutritional information.
            </p>
          </div>

          <NuxtLink to="/get-food" class="btn-dark grocery-button">
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
.grocery-inner {
  max-width: 1200px;
}

.grocery-grid {
  display: grid;
  gap: 16px;
}

.large-feature-card,
.horizontal-highlight {
  border: 1px solid rgb(198 198 205 / 30%);
  border-radius: 12px;
  background: #ffffff;
  padding: 24px;
  box-shadow: 0 1px 2px #0000000d;
}

.large-feature-card {
  min-height: 538px;
}

.small-tip-card {
  position: relative;
  z-index: 1;
  overflow: hidden;
  min-height: 400px;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 2px #0000000d;
}

.horizontal-highlight {
  position: relative;
  z-index: 3;
  min-height: 206px;
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
}

@media (min-width: 1024px) {
  .grocery-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-template-rows: 316px 206px;
  }

  .large-feature-card {
    grid-column: span 2 / span 2;
    grid-row: span 2 / span 2;
  }

  .horizontal-highlight {
    grid-column: span 2 / span 2;
    margin-top: -42px;
  }

  .small-tip-card {
    margin-bottom: 60px;
  }
}

@media (max-width: 1023px) {
  .large-feature-card {
    min-height: auto;
  }

  .small-tip-card {
    min-height: auto;
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
}
</style>