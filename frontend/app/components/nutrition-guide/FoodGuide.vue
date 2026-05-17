<template>
  <section id="food-guide" class="food-guide">
    <div class="guide-heading">
      <h2>Food Guide : What’s in your food?</h2>
      <p>Simple information about foods that are affordable and easy to find.</p>
    </div>

    <div class="guide-layout">
      <!-- LEFT CARD -->
      <article class="featured-card">
        <div class="blur blur-top" />
        <div class="blur blur-bottom" />

        <button class="arrow-btn arrow-left" @click="previousFood">‹</button>
        <button class="arrow-btn arrow-right" @click="nextFood">›</button>

        <h3>{{ currentFood.name }}</h3>

        <div class="food-image-ring">
          <img :src="currentFood.name.toLowerCase() === 'salmon'
              ? '/images/foodguide/fg-1.webp'
              : currentFood.image
            " :alt="currentFood.name" />
        </div>

        <div class="tag-row">
          <span v-for="tag in currentFood.tags" :key="tag">
            {{ tag }}
          </span>
        </div>
      </article>

      <!-- RIGHT CONTENT -->
      <div class="content-stack">
        <article class="profile-card">
          <div class="profile-title">
            <h4>Nutritional Profile</h4>
            <span>(per 100g)</span>
          </div>

          <div class="macro-grid">
            <div v-for="macro in currentFood.macros" :key="macro.label" class="macro-card">
              <strong>
                {{ macro.value.replace('g', '') }}<span class="macro-unit">g</span>
              </strong>
              <span>{{ macro.label }}</span>
            </div>
          </div>
        </article>

        <article class="recommendation-card">
          <div class="calendar-icon">
            <img src="/images/foodguide/fg-4.webp" alt="Calendar icon" />
          </div>
          <h4>How often?</h4>
          <p>{{ currentFood.howOften }}</p>
        </article>
        <NuxtLink to="/get-food" class="food-guide-cta">
          <div>
            <h4>Looking for healthier alternatives?</h4>
            <p>Learn about alternate foods to swap your food with.</p>
          </div>

          <span>Explore Smart swaps</span>
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { foodGuideItems, findFoodGuideIndex } from '~/data/foodGuide'

const props = defineProps<{
  selectedFood?: string | null
}>()

const activeIndex = ref(0)

const foods = foodGuideItems

const currentFood = computed(() => foods[activeIndex.value])

watch(
  () => props.selectedFood,
  (foodName) => {
    if (!foodName) return

    const index = findFoodGuideIndex(foodName)

    if (index !== -1) {
      activeIndex.value = index

      document.getElementById('food-guide')?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      })
    }
  },
)

const nextFood = () => {
  activeIndex.value = (activeIndex.value + 1) % foods.length
}

const previousFood = () => {
  activeIndex.value = (activeIndex.value - 1 + foods.length) % foods.length
}
</script>

<style scoped>
.food-guide {
  width: min(1120px, calc(100% - 48px));
  margin: 0 auto;
  padding: 56px 0 72px;
  min-height: 820px;
}

.guide-heading {
  margin-bottom: 32px;
}

.guide-heading h2 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(32px, 3.4vw, 42px);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.96px;
  color: #000;
}

.guide-heading p {
  margin: 14px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 18px;
  line-height: 1.55;
  color: #45464d;
}

.guide-layout {
  display: grid;
  grid-template-columns: 0.95fr 1.35fr;
  gap: 22px;
  align-items: stretch;
  min-height: 642px;
}

/* LEFT FEATURE CARD */
.featured-card {
  position: relative;
  height: 642px;
  overflow: hidden;
  border-radius: 12px;
  background: #d5e3fc;
  padding: 56px 28px 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.blur {
  position: absolute;
  border-radius: 9999px;
  filter: blur(32px);
  pointer-events: none;
}

.blur-top {
  width: 256px;
  height: 256px;
  right: -80px;
  top: -80px;
  background: #e6eeff;
  opacity: 0.5;
}

.blur-bottom {
  width: 192px;
  height: 192px;
  left: -40px;
  bottom: -40px;
  background: #bae6fd;
  opacity: 0.3;
}

.featured-card h3 {
  position: relative;
  z-index: 2;
  height: 150px;
  max-width: 340px;
  margin: 0 0 18px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(34px, 3.3vw, 48px);
  font-weight: 700;
  line-height: 1.12;
  color: #0d1c2e;
  text-align: center;

  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.food-image-ring {
  position: relative;
  z-index: 2;
  width: 260px;
  height: 260px;
  flex: 0 0 260px;
  padding: 16px;
  border-radius: 9999px;
  background: #fff;
  border: 1px solid #bae6fd;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.food-image-ring img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 9999px;
}

.tag-row {
  position: relative;
  z-index: 2;
  min-height: 40px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-top: 26px;
}

.tag-row span {
  padding: 8px 16px;
  border-radius: 9999px;
  background: #fff;
  border: 1px solid #bae6fd;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #3d687c;
}

.arrow-btn {
  position: absolute;
  top: 50%;
  z-index: 5;
  width: 46px;
  height: 46px;
  border: 1px solid #bae6fd;
  border-radius: 9999px;
  background: #ffffff;
  color: #0d1c2e;
  font-size: 34px;
  line-height: 1;
  cursor: pointer;
  transform: translateY(-50%);
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 4px;
}

.arrow-btn:hover {
  background: #eff4ff;
  transform: translateY(-50%) scale(1.08);
  box-shadow: 0 8px 20px rgba(13, 28, 46, 0.12);
}

.arrow-left {
  left: 24px;
}

.arrow-right {
  right: 24px;
}

/* RIGHT SIDE */
.content-stack {
  height: 642px;
  display: grid;
  grid-template-rows: 320px 152px 136px;
  gap: 18px;
}

.profile-card,
.recommendation-card,
.food-guide-cta {
  overflow: hidden;
}

.profile-card {
  padding: 24px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #c6c6cd;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.profile-title {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding-bottom: 18px;
  margin-bottom: 24px;
  border-bottom: 1px solid #c6c6cd;
}

.profile-title h4 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(26px, 2.5vw, 30px);
  font-weight: 700;
  line-height: 1.25;
  color: #0d1c2e;
}

.profile-title span {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  color: #45464d;
}

.macro-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.macro-card {
  min-height: 150px;
  border-radius: 4px;
  border: 1px solid #d5e3fc;
  background: #f8f9ff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding: 18px;
}

.macro-card strong {
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(42px, 4vw, 56px);
  font-weight: 700;
  line-height: 0.9;
  color: #0d1c2e;
}

.macro-card>span {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.7px;
  color: #45464d;
}

.macro-unit {
  display: inline-block;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 0.55em;
  font-weight: 700;
  line-height: 1;
  margin-left: 2px;
  transform: translateY(8px);
}

.swap-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.swap-card {
  min-height: 210px;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #c6c6cd;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.swap-card.budget {
  background: #eff4ff;
}

.swap-card.optimal {
  background: #dce9ff;
}

.swap-label {
  display: flex;
  align-items: center;
  gap: 12px;
}

.swap-icon {
  width: 22px;
  height: 22px;
  object-fit: contain;
  flex-shrink: 0;
}

.icon-dot {
  width: 20px;
  height: 20px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  background: #3d687c;
  color: #fff;
  font-size: 10px;
}

.swap-card h5 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 22px;
  font-weight: 600;
  color: #0d1c2e;
}

.swap-card h6 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(34px, 3.4vw, 42px);
  font-weight: 700;
  line-height: 1.1;
  color: #131b2e;
}

.swap-card p {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 15px;
  line-height: 1.5;
  color: #45464d;
}

.recommendation-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border-radius: 12px;
  background: #131b2e;
  height: 100%;
}

.calendar-icon {
  flex: 0 0 auto;
  width: 58px;
  height: 58px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.14);
}

.calendar-icon img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.recommendation-card h4 {
  margin: 0 0 8px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 22px;
  font-weight: 600;
  color: #fff;
}

.recommendation-card p {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 15px;
  line-height: 1.5;
  color: #d5e3fc;
}

.food-guide-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px 20px;
  border: 1px solid #c6c6cd;
  border-radius: 12px;
  background: #ffffff;
  color: #0d1c2e;
  text-decoration: none;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.food-guide-cta h4 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 22px;
  font-weight: 700;
  color: #0d1c2e;
}

.food-guide-cta p {
  margin: 6px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 1.4;
  color: #45464d;
}

.food-guide-cta span {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 0 24px;
  border-radius: 8px;
  background: #000000;
  color: #ffffff;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  font-weight: 500;
}

/* RESPONSIVE */
@media (max-width: 1100px) {
  .food-guide {
    width: calc(100% - 48px);
  }

  .guide-layout {
    grid-template-columns: 1fr;
  }

  .featured-card {
    min-height: 520px;
  }
}

@media (max-width: 720px) {
  .food-guide {
    width: calc(100% - 32px);
    padding: 48px 0;
  }

  .guide-heading {
    margin-bottom: 28px;
  }

  .featured-card {
    min-height: 500px;
    padding: 64px 20px;
  }

  .food-image-ring {
    width: 220px;
    height: 220px;
  }

  .profile-card {
    padding: 20px;
  }

  .profile-title {
    flex-direction: column;
    gap: 4px;
  }

  .macro-grid,
  .swap-grid {
    grid-template-columns: 1fr;
  }

  .macro-card {
    min-height: 130px;
  }

  .recommendation-card {
    align-items: flex-start;
  }
}
</style>