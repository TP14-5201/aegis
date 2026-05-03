<template>
  <section id="food-guide" class="food-guide">
    <!-- HEADER -->
    <div class="guide-heading">
      <p class="eyebrow">Food Guide</p>
      <h2>What's in your food?</h2>
      <p>
        Simple information about foods that are affordable and easy to find.
      </p>
    </div>

    <div class="guide-layout">
      <!-- LEFT -->
      <div class="food-left">
        <h3>{{ currentFood.name }}</h3>

        <div class="image-wrap">
          <button class="arrow-btn arrow-left" @click="previousFood">‹</button>

          <img :src="currentFood.image" :alt="currentFood.name" />

          <button class="arrow-btn arrow-right" @click="nextFood">›</button>
        </div>
      </div>

      <!-- RIGHT -->
      <aside class="food-right">
        <!-- DONUT -->
        <div class="info-block">
          <h4>Whats in it ?</h4>

          <div class="donut-row">
            <div
              v-for="macro in currentFood.macros"
              :key="macro.label"
              class="donut-item"
            >
              <div
                class="donut"
                :style="{ '--percent': macro.percent + '%', '--accent': macro.color }"
              >
                <span>{{ macro.value }}</span>
              </div>
              <p>{{ macro.label }}</p>
            </div>
          </div>
        </div>

        <!-- SWAPS -->
        <div class="info-block">
          <h4>Smart Swaps</h4>

          <div class="swap-grid">
            <article
              v-for="swap in currentFood.swaps"
              :key="swap.name"
              class="swap-card"
            >
              <h5>{{ swap.type }}</h5>
              <img :src="swap.image" :alt="swap.name" />
              <p>{{ swap.name }}</p>
            </article>
          </div>
        </div>

        <!-- HOW OFTEN -->
        <div class="info-block">
          <h4>How Often ?</h4>

          <div class="how-often">
            <p>{{ currentFood.howOften }}</p>
          </div>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from "vue";

const activeIndex = ref(0);

const foods = [
  {
    name: "EGGS",
    image: "/images/foodguide/eggs.png",
    macros: [
      { label: "Fat", value: "5 g", percent: 65, color: "#24145f" },
      { label: "Carbs", value: "1 g", percent: 20, color: "#f26432" },
      { label: "Protein", value: "6 g", percent: 75, color: "#24145f" },
    ],
    swaps: [
      {
        type: "Cheaper",
        name: "Lentils",
        image: "/images/foodguide/lentils.png",
      },
      {
        type: "Healthier",
        name: "Canned Tuna",
        image: "/images/foodguide/canned-tuna.png",
      },
    ],
    howOften:
      "1–2 eggs per day is recommended for optimal growth.",
  },
  {
    name: "PASTA",
    image: "/images/foodguide/pasta.png",
    macros: [
      { label: "Fat", value: "1 g", percent: 15, color: "#24145f" },
      { label: "Carbs", value: "43 g", percent: 78, color: "#f26432" },
      { label: "Protein", value: "8 g", percent: 45, color: "#24145f" },
    ],
    swaps: [
      {
        type: "Cheaper",
        name: "Rice",
        image: "/images/foodguide/rice.png",
      },
      {
        type: "Healthier",
        name: "Wholemeal Pasta",
        image: "/images/foodguide/wholemeal-pasta.png",
      },
    ],
    howOften:
      "Pasta can be eaten regularly when balanced with vegetables and protein.",
  },
  {
    name: "CHICKEN",
    image: "/images/foodguide/chicken.png",
    macros: [
      { label: "Fat", value: "4 g", percent: 45, color: "#24145f" },
      { label: "Carbs", value: "0 g", percent: 5, color: "#f26432" },
      { label: "Protein", value: "31 g", percent: 85, color: "#24145f" },
    ],
    swaps: [
      {
        type: "Cheaper",
        name: "Beans",
        image: "/images/foodguide/beans.png",
      },
      {
        type: "Healthier",
        name: "Canned Tuna",
        image: "/images/foodguide/canned-tuna.png",
      },
    ],
    howOften:
      "Chicken is a good protein source but should be balanced with plant-based foods.",
  },
];

const currentFood = computed(() => foods[activeIndex.value]);

const nextFood = () => {
  activeIndex.value = (activeIndex.value + 1) % foods.length;
};

const previousFood = () => {
  activeIndex.value =
    (activeIndex.value - 1 + foods.length) % foods.length;
};
</script>

<style scoped>
.food-guide {
  width: min(1240px, calc(100% - 96px));
  margin: 0 auto;
  padding: 80px 0;
}

.guide-heading {
  margin-bottom: 34px;
}

.eyebrow {
  margin: 0 0 6px;
  color: #df6951 !important;
  font-weight: 900;
  text-transform: uppercase;
}

.guide-heading h2 {
  margin: 0;
  font-family: Volkhov, Georgia, serif;
  color: #07192f;
  font-size: clamp(32px, 4vw, 42px);
  line-height: 1.05;
}

.guide-heading p {
  margin: 10px 0 0;
  font-size: 18px;
  color: #111;
}

.guide-layout {
  display: grid;
  grid-template-columns: 1.2fr 0.95fr;
  gap: 54px;
  align-items: stretch;
}

.food-left {
  display: flex;
  flex-direction: column;
}

.food-left h3 {
  margin: 0 0 28px;
  text-align: center;
  font-family: Volkhov, Georgia, serif;
  font-size: 30px;
  color: #07192f;
}

.image-wrap {
  position: relative;
  flex: 1;
  min-height: 390px;
  overflow: hidden;
  background: #f6f6f6;
}

.image-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.arrow-btn {
  position: absolute;
  top: 50%;
  z-index: 2;
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 999px;
  background: #e6f4ff;
  color: #07192f;
  font-size: 30px;
  cursor: pointer;
  transform: translateY(-50%);
  transition: transform 0.25s ease, background 0.25s ease;
}

.arrow-btn:hover {
  background: #cfe9ff;
  transform: translateY(-50%) scale(1.08);
}

.arrow-left {
  left: 22px;
}

.arrow-right {
  right: 22px;
}

.food-right {
  display: grid;
  gap: 24px;
}

.info-block h4 {
  margin: 0 0 18px;
  font-family: Volkhov, Georgia, serif;
  font-size: 22px;
  color: #07192f;
}

.donut-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 26px;
}

.donut-item {
  text-align: center;
}

.donut {
  width: 94px;
  height: 94px;
  margin: 0 auto;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    radial-gradient(circle at center, white 0 42%, transparent 43%),
    conic-gradient(var(--accent) var(--percent), #f26432 0);
  transition: transform 0.3s ease, filter 0.3s ease;
}

.donut:hover {
  transform: translateY(-5px) scale(1.06);
  filter: drop-shadow(0 12px 18px rgba(7, 25, 47, 0.18));
}

.donut span {
  font-weight: 900;
  color: #07192f;
}

.donut-item p {
  margin: 10px 0 0;
  color: #111;
}

.swap-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}

.swap-card {
  min-height: 190px;
  padding: 22px;
  border-radius: 16px;
  background: #e9fff2;
  box-shadow: 0 4px 6px rgba(7, 25, 47, 0.22);
  text-align: center;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.swap-card h5 {
  margin: 0 0 16px;
  font-family: Volkhov, Georgia, serif;
  font-size: 24px;
  color: #07192f;
}

.swap-card img {
  height: 92px;
  max-width: 140px;
  object-fit: contain;
}

.swap-card p {
  margin: 16px 0 0;
  color: #111;
  font-size: 17px;
}

.how-often {
  padding: 22px 30px;
  border-radius: 16px;
  background: #dff0ff;
}

.how-often p {
  margin: 0;
  color: #07192f;
  line-height: 1.35;
}

@media (max-width: 1024px) {
  .food-guide {
    width: calc(100% - 48px);
  }

  .guide-layout {
    grid-template-columns: 1fr;
    gap: 42px;
  }
}

@media (max-width: 640px) {
  .food-guide {
    width: calc(100% - 32px);
    padding: 56px 0;
  }

  .image-wrap {
    height: 280px;
  }

  .donut-row {
    gap: 14px;
  }

  .donut {
    width: 76px;
    height: 76px;
  }

  .swap-grid {
    grid-template-columns: 1fr;
  }
}
</style>