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
  padding: 48px 0 56px;
}

.guide-heading {
  margin-bottom: 26px;
}

.guide-heading h2 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(30px, 3vw, 38px);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.6px;
  color: #000;
}

.guide-heading p {
  margin: 10px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #45464d;
}

.guide-layout {
  display: grid;
  grid-template-columns: 0.95fr 1.35fr;
  gap: 22px;
  align-items: stretch;
}

/* LEFT FEATURE CARD */
.featured-card {
  position: relative;
  min-height: 500px;
  overflow: hidden;
  border-radius: 12px;
  background: #d5e3fc;
  padding: 36px 26px;
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
  width: 220px;
  height: 220px;
  right: -80px;
  top: -80px;
  background: #e6eeff;
  opacity: 0.5;
}

.blur-bottom {
  width: 160px;
  height: 160px;
  left: -40px;
  bottom: -40px;
  background: #bae6fd;
  opacity: 0.3;
}

.featured-card h3 {
  position: relative;
  z-index: 2;
  min-height: 92px;
  max-width: 320px;
  margin: 0 0 14px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(30px, 3vw, 40px);
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
  width: 220px;
  height: 220px;
  flex: 0 0 220px;
  padding: 14px;
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
  min-height: 36px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
}

.tag-row span {
  padding: 7px 14px;
  border-radius: 9999px;
  background: #fff;
  border: 1px solid #bae6fd;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #3d687c;
}

.arrow-btn {
  position: absolute;
  top: 50%;
  z-index: 5;
  width: 40px;
  height: 40px;
  border: 1px solid #bae6fd;
  border-radius: 9999px;
  background: #ffffff;
  color: #0d1c2e;
  font-size: 30px;
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
  left: 20px;
}

.arrow-right {
  right: 20px;
}

/* RIGHT SIDE */
.content-stack {
  display: grid;
  grid-template-rows: auto auto auto;
  gap: 16px;
}

.profile-card,
.recommendation-card,
.food-guide-cta {
  overflow: hidden;
}

.profile-card {
  padding: 22px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #c6c6cd;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.profile-title {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding-bottom: 14px;
  margin-bottom: 18px;
  border-bottom: 1px solid #c6c6cd;
}

.profile-title h4 {
  margin: 0;
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(24px, 2.3vw, 28px);
  font-weight: 700;
  line-height: 1.25;
  color: #0d1c2e;
}

.profile-title span {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  color: #45464d;
}

.macro-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.macro-card {
  min-height: 118px;
  border-radius: 6px;
  border: 1px solid #d5e3fc;
  background: #f8f9ff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 14px;
}

.macro-card strong {
  font-family: "Playfair Display", Georgia, serif;
  font-size: clamp(34px, 3.4vw, 46px);
  font-weight: 700;
  line-height: 0.9;
  color: #0d1c2e;
}

.macro-card > span {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: #45464d;
}

.macro-unit {
  display: inline-block;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 0.55em;
  font-weight: 700;
  line-height: 1;
  margin-left: 2px;
  transform: translateY(6px);
}

.recommendation-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 20px;
  border-radius: 12px;
  background: #131b2e;
}

.calendar-icon {
  flex: 0 0 auto;
  width: 52px;
  height: 52px;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.14);
}

.calendar-icon img {
  width: 26px;
  height: 26px;
  object-fit: contain;
}

.recommendation-card h4 {
  margin: 0 0 6px;
  font-family: "Playfair Display", Georgia, serif;
  font-size: 21px;
  font-weight: 600;
  color: #fff;
}

.recommendation-card p {
  margin: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 14px;
  line-height: 1.45;
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
  font-size: 21px;
  font-weight: 700;
  color: #0d1c2e;
}

.food-guide-cta p {
  margin: 5px 0 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
  line-height: 1.4;
  color: #45464d;
}

.food-guide-cta span {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
  padding: 0 20px;
  border-radius: 8px;
  background: #000000;
  color: #ffffff;
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 13px;
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
    min-height: 460px;
  }
}

@media (max-width: 720px) {
  .food-guide {
    width: calc(100% - 32px);
    padding: 42px 0 48px;
  }

  .guide-heading {
    margin-bottom: 24px;
  }

  .featured-card {
    min-height: auto;
    padding: 56px 20px 40px;
  }

  .featured-card h3 {
    min-height: auto;
    font-size: clamp(28px, 8vw, 34px);
  }

  .food-image-ring {
    width: 190px;
    height: 190px;
    flex-basis: 190px;
  }

  .profile-card {
    padding: 20px;
  }

  .profile-title {
    flex-direction: column;
    gap: 4px;
  }

  .macro-grid {
    grid-template-columns: 1fr;
  }

  .macro-card {
    min-height: 112px;
  }

  .recommendation-card {
    align-items: flex-start;
  }

  .food-guide-cta {
    flex-direction: column;
    align-items: flex-start;
  }

  .food-guide-cta span {
    width: 100%;
  }
}
</style>