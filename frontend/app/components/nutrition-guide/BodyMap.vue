<template>
  <section id="body-map" class="body-map-section">
    <div class="body-map-inner">
      <div class="section-heading">
        <h2>Interactive Body Map : Feed Your Body Right</h2>
        <p>
          Select a body-part to explore the foods required to make them grow stronger.
        </p>
      </div>

      <div class="body-layout">
        <!-- LEFT BUTTONS -->
        <div class="part-list" aria-label="Body parts">
          <button
            v-for="part in bodyParts"
            :key="part.key"
            class="part-button"
            :class="{ active: activePart === part.key }"
            type="button"
            @click="togglePart(part.key)"
          >
            <span class="part-icon">
              <img :src="part.icon" :alt="`${part.label} icon`" />
            </span>
            <span>{{ part.label }}</span>
          </button>
        </div>

        <!-- BODY IMAGE -->
        <div class="body-figure">
          <div class="body-image-wrap">
            <Transition name="body-highlight" mode="out-in">
              <img
                v-if="!selectedPart"
                key="base"
                src="/images/bodymap/base.svg"
                alt="Body map illustration"
                class="body-image"
              />

              <img
                v-else
                :key="selectedPart.key"
                :src="selectedPart.image"
                :alt="`${selectedPart.label} body highlight`"
                class="body-image"
              />
            </Transition>
            
            <!-- BODY BUTTONS -->
            <button
              v-for="part in bodyParts"
              :key="part.key + '-hotspot'"
              class="body-hotspot"
              :class="['hotspot-' + part.key, { active: activePart === part.key }]"
              type="button"
              :aria-label="'Show ' + part.label + ' nutrition information'"
              @click="togglePart(part.key)"
            >
              <img :src="part.icon" alt="" />
            </button>

            <!-- DASHED CONNECTOR LINE -->
            <svg
              v-if="selectedPart"
              class="connector-svg"
              viewBox="0 0 520 500"
              preserveAspectRatio="none"
              aria-hidden="true"
            >
              <path :d="selectedPart.linePath" class="connector-line" />
            </svg>
          </div>

          <div class="click-hint">
            <img src="/images/bodymap/bm-8.png" alt="" />
            <span>Click on any body part to explore</span>
          </div>
        </div>

        <!-- RIGHT PANEL -->
        <article v-if="selectedPart" class="info-panel">
          <h3>{{ selectedPart.label }}</h3>
          <p class="description">{{ selectedPart.description }}</p>

          <h4>Optimal Food Sources</h4>

          <div class="food-grid">
            <div
              v-for="food in selectedPart.foods"
              :key="food.name"
              class="food-card"
            >
              <img :src="food.image" :alt="food.name" />
              <span>{{ food.name }}</span>
            </div>
          </div>

          <div class="why-card">
            <h5>Why it helps</h5>
            <p>{{ selectedPart.why }}</p>
          </div>
        </article>

        <article v-else class="info-panel empty-panel">
          <h3>Select a body part</h3>
          <p class="description">
            Choose one area from the left to learn what foods can support it.
          </p>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type Food = {
  name: string
  image: string
}

type BodyPart = {
  key: string
  label: string
  icon: string
  image: string
  linePath: string
  description: string
  foods: Food[]
  why: string
}

const activePart = ref<string | null>('brain')

function togglePart(key: string) {
  activePart.value = activePart.value === key ? null : key
}

const image = {
  walnuts: '/images/bodymap/bm-walnuts.png',
  blueberries: '/images/bodymap/bm-blueberries.png',
  eggs: '/images/bodymap/bm-eggs.png',
  milk: '/images/bodymap/bm-milk.png',
}

const bodyParts: BodyPart[] = [
  {
    key: 'brain',
    label: 'Brain',
    icon: '/images/bodymap/bm-1.png',
    image: '/images/bodymap/brain.svg',
    linePath: 'M 245 88 C 320 80, 405 115, 515 165',
    description:
      "The brain is the body's most energy-demanding organ. Targeted nutrition supports neuroplasticity, memory retention, and long-term cognitive health.",
    foods: [
      { name: 'Walnuts', image: image.walnuts },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'Eggs', image: image.eggs },
      { name: 'milk', image: image.milk },
    ],
    why:
      'These foods are rich in Omega-3, good fats, vitamins and minerals that support brain growth and memory.',
  },
  {
    key: 'eyes',
    label: 'Eye',
    icon: '/images/bodymap/bm-2.png',
    image: '/images/bodymap/eyes.svg',
    linePath: 'M 250 128 C 325 125, 410 145, 515 178',
    description:
      'Supports healthy vision and helps children see clearly during learning, reading and play.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'milk', image: image.milk },
      { name: 'Walnuts', image: image.walnuts },
    ],
    why:
      'Vitamin-rich foods, protein and minerals help support everyday eye health.',
  },
  {
    key: 'bones',
    label: 'Bones',
    icon: '/images/bodymap/bm-3.png',
    image: '/images/bodymap/bones.svg',
    linePath: 'M 245 315 C 330 315, 410 270, 515 230',
    description:
      'Bones give the body shape and help children stand, walk and grow strong.',
    foods: [
      { name: 'milk', image: image.milk },
      { name: 'Eggs', image: image.eggs },
      { name: 'Walnuts', image: image.walnuts },
      { name: 'Blueberries', image: image.blueberries },
    ],
    why:
      'Calcium, vitamin D and protein help build strong bones during childhood.',
  },
  {
    key: 'muscles',
    label: 'Muscles',
    icon: '/images/bodymap/bm-4.png',
    image: '/images/bodymap/muscles.svg',
    linePath: 'M 245 245 C 330 245, 415 235, 515 215',
    description:
      'Muscles help children move, run, play and stay active throughout the day.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'milk', image: image.milk },
      { name: 'Walnuts', image: image.walnuts },
      { name: 'Blueberries', image: image.blueberries },
    ],
    why:
      'Protein-rich foods help muscles grow, repair and stay strong.',
  },
  {
    key: 'immunity',
    label: 'Immunity',
    icon: '/images/bodymap/bm-5.png',
    image: '/images/bodymap/immunity.svg',
    linePath: 'M 245 205 C 330 205, 415 205, 515 200',
    description:
      'Immunity protects the body from germs and helps children stay healthy.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'milk', image: image.milk },
      { name: 'Walnuts', image: image.walnuts },
    ],
    why:
      'Vitamins, minerals and protein support the immune system and help the body fight sickness.',
  },
  {
    key: 'energy',
    label: 'Energy',
    icon: '/images/bodymap/bm-6.png',
    image: '/images/bodymap/energy.svg',
    linePath: 'M 245 275 C 330 280, 415 250, 515 220',
    description:
      'Energy gives children power for learning, playing and daily activities.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'milk', image: image.milk },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'Walnuts', image: image.walnuts },
    ],
    why:
      'Balanced meals provide steady energy throughout the day.',
  },
  {
    key: 'teeth',
    label: 'Teeth',
    icon: '/images/bodymap/bm-7.png',
    image: '/images/bodymap/teeth.svg',
    linePath: 'M 250 155 C 330 155, 415 165, 515 190',
    description:
      'Teeth help children bite, chew and keep a bright smile.',
    foods: [
      { name: 'milk', image: image.milk },
      { name: 'Eggs', image: image.eggs },
      { name: 'Walnuts', image: image.walnuts },
      { name: 'Blueberries', image: image.blueberries },
    ],
    why:
      'Calcium-rich and low-sugar foods help protect teeth and support healthy gums.',
  },
]

const selectedPart = computed(() => {
  return bodyParts.find((part) => part.key === activePart.value) || null
})
</script>

<style scoped>
.body-map-section {
  width: 100%;
  min-height: 760px;
  padding: 48px 0 52px;
  scroll-margin-top: 100px;
  background:
    radial-gradient(
      circle at 42% 52%,
      rgba(255, 255, 255, 0.62) 0%,
      rgba(255, 255, 255, 0) 36%
    ),
    linear-gradient(116deg, #e6eeff 0%, #d7e7f8 47%, #8298ab 100%);
}

.body-map-inner {
  width: min(1200px, calc(100% - 80px));
  margin: 0 auto;
}

/* HEADING */
.section-heading {
  margin-bottom: 24px;
}

.section-heading h2 {
  margin: 0;
  color: #000000;
  font-family: 'Playfair Display', serif;
  font-size: 44px;
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -0.8px;
}

.section-heading p {
  margin: 12px 0 0;
  color: #45464d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  line-height: 1.45;
}

/* MAIN LAYOUT */
.body-layout {
  display: grid;
  grid-template-columns: 180px minmax(360px, 1fr) 380px;
  gap: 30px;
  align-items: center;
  min-height: 560px;
}

/* LEFT BUTTONS */
.part-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.part-button {
  display: flex;
  align-items: center;
  gap: 16px;

  min-height: 56px;

  border: none;
  border-radius: 18px;

  padding: 12px 18px;

  background: #f8f9ff;
  color: #181e4b;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  font-weight: 500;

  cursor: pointer;

  box-shadow: 0 5px 8px rgba(24, 30, 75, 0.18);

  transition:
    background 0.22s ease,
    transform 0.22s ease,
    color 0.22s ease;
}

.part-button:hover,
.part-button.active {
  background: #181e4b;
  color: #ffffff;
  transform: translateY(-2px);
}

.part-icon {
  display: grid;
  place-items: center;

  width: 38px;
  height: 38px;

  border-radius: 999px;

  background: transparent;

  flex-shrink: 0;

  transition: background 0.22s ease;
}

.part-button.active .part-icon {
  background: #ffffff;
}

.part-icon img {
  width: 28px;
  height: 28px;

  object-fit: contain;
  display: block;
}

/* BODY FIGURE */
.body-figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;

  min-height: 560px;

  position: relative;
  z-index: 2;
}

.body-image-wrap {
  width: min(100%, 350px);
  min-height: 450px;

  display: grid;
  place-items: center;

  position: relative;
  overflow: visible;
}

.body-image {
  width: 100%;
  max-height: 480px;

  object-fit: contain;
  display: block;

  position: relative;
  z-index: 2;
}

/* DASHED CONNECTOR */
.connector-svg {
  position: absolute;
  top: 0;
  left: 0;

  width: 155%;
  height: 100%;

  pointer-events: none;

  z-index: 1;
  overflow: visible;
}

.connector-line {
  fill: none;

  stroke: #000000;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-dasharray: 9 9;

  opacity: 0.8;

  animation: dashMove 1s linear infinite;
}

@keyframes dashMove {
  from {
    stroke-dashoffset: 18;
  }

  to {
    stroke-dashoffset: 0;
  }
}
/* BODY BUTTONS */
.body-hotspot {
  position: absolute;
  z-index: 4;

  display: grid;
  place-items: center;

  width: 34px;
  height: 34px;

  border: 2px solid #ffffff;
  border-radius: 999px;

  background: rgba(255, 255, 255, 0.92);

  box-shadow: 0 8px 18px rgba(24, 30, 75, 0.22);

  cursor: pointer;

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.body-hotspot img {
  width: 21px;
  height: 21px;
  object-fit: contain;
}

.body-hotspot:hover,
.body-hotspot.active {
  background: #181e4b;
  transform: translateY(-2px) scale(1.08);
  box-shadow: 0 12px 24px rgba(24, 30, 75, 0.3);
}

.body-hotspot:hover img,
.body-hotspot.active img {
  filter: brightness(0) invert(1);
}

/* adjust these positions based on your boy image */
.body-hotspot.hotspot-brain {
  top: 58px;
  left: 204px;
}

.body-hotspot.hotspot-eyes {
  top: 100px;
  left: 222px;
}

.body-hotspot.hotspot-teeth {
  top: 134px;
  left: 200px;
}

.body-hotspot.hotspot-immunity {
  top: 288px;
  left: 236px;
}

.body-hotspot.hotspot-muscles {
  top: 209px;
  left: 235px;
}

.body-hotspot.hotspot-energy {
  top: 198px;
  left: 200px;
}

.body-hotspot.hotspot-bones {
  top: 366px;
  left: 210px;
}

/* CLICK HINT */
.click-hint {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-top: 18px;

  color: #0d1c2e;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  line-height: 20px;
}

.click-hint img {
  width: 18px;
  height: 18px;

  object-fit: contain;
}

/* RIGHT PANEL */
.info-panel {
  align-self: center;

  border-radius: 28px;

  padding: 24px;

  background: #ffffff;

  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);

  position: relative;
  z-index: 3;
}

.info-panel h3 {
  margin: 0 0 8px;

  color: #006a61;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;

  letter-spacing: 1.3px;
  text-transform: uppercase;
}

.description {
  margin: 0;

  color: #45464d;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  line-height: 1.5;
}

.info-panel h4 {
  margin: 22px 0 14px;

  padding-bottom: 8px;

  border-bottom: 1px solid #c6c6cd;

  color: #76777d;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;

  letter-spacing: 1.3px;
  text-transform: uppercase;
}

/* FOOD GRID */
.food-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.food-card {
  overflow: hidden;

  border: 1px solid #c6c6cd;
  border-radius: 4px;

  background: #ffffff;
}

.food-card img {
  width: 100%;
  height: 104px;

  object-fit: cover;
  display: block;
}

.food-card span {
  display: block;

  padding: 8px;

  color: #191c1e;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
}

/* WHY CARD */
.why-card {
  margin-top: 22px;

  border: 1px solid #c6c6cd;
  border-radius: 4px;

  padding: 18px;

  background: #f2f4f6;
}

.why-card h5 {
  margin: 0 0 10px;

  color: #006a61;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 700;

  letter-spacing: 1.3px;
  text-transform: uppercase;
}

.why-card p {
  margin: 0;

  color: #191c1e;

  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  line-height: 1.5;
}

/* EMPTY PANEL */
.empty-panel {
  min-height: 260px;

  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* TRANSITION */
.body-highlight-enter-active,
.body-highlight-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.body-highlight-enter-from,
.body-highlight-leave-to {
  opacity: 0;
  transform: scale(0.98);
}

/* TABLET */
@media (max-width: 1024px) {
  .body-map-inner {
    width: min(900px, calc(100% - 40px));
  }

  .body-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .part-list {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
  }

  .part-button {
    justify-content: center;
    padding: 12px;
  }

  .connector-svg {
    display: none;
  }

  .info-panel {
    width: min(100%, 520px);
    margin: 0 auto;
  }
}

/* MOBILE */
@media (max-width: 640px) {
  .body-map-section {
    padding: 48px 0 60px;
  }

  .body-map-inner {
    width: calc(100% - 32px);
  }

  .section-heading h2 {
    font-size: 34px;
    line-height: 1.15;
  }

  .section-heading p {
    font-size: 15px;
  }

  .part-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .part-button {
    min-height: 54px;
    border-radius: 16px;
    gap: 10px;
    font-size: 14px;
  }

  .part-icon {
    width: 32px;
    height: 32px;
  }

  .part-icon img {
    width: 24px;
    height: 24px;
  }

  .body-figure {
    min-height: auto;
  }

  .body-image-wrap {
    width: min(100%, 280px);
    min-height: 380px;
  }

  .body-image {
    max-height: 380px;
  }

  .info-panel {
    border-radius: 24px;
    padding: 22px;
  }

  .food-card img {
    height: 110px;
  }
}
</style>