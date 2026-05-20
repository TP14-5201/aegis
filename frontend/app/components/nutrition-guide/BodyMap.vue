<template>
  <section id="body-map" class="body-map-section section-large">
    <div class="section-inner body-map-inner">
      <div class="section-heading">
        <h2>Interactive Body Map : Feed Your Body Right</h2>
        <p>Select a body-part to explore the foods required to make them grow stronger.</p>
      </div>

      <div class="body-layout">
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
            <img src="/images/bodymap/bm-8.webp" alt="" />
            <span>Click on any body part to explore</span>
          </div>
        </div>

        <article v-if="selectedPart" class="info-panel">
          <h3>{{ selectedPart.label }}</h3>

          <p class="description">
            {{ selectedPart.description }}
          </p>

          <h4>Optimal Food Sources</h4>

          <div class="food-grid">
            <button
              v-for="food in selectedPart.foods"
              :key="food.name"
              type="button"
              class="food-card"
              @click="handleFoodSelect(food.name)"
            >
              <img :src="food.image" :alt="food.name" />

              <span>{{ food.name }}</span>
            </button>
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

const activePart = ref<string | null>(null)

const emit = defineEmits<{
  'select-food': [foodName: string]
}>()

function togglePart(key: string) {
  activePart.value = activePart.value === key ? null : key
}

function handleFoodSelect(foodName: string) {
  emit('select-food', foodName)

  requestAnimationFrame(() => {
    const section = document.getElementById('food-guide')

    if (!section) return

    const navbarOffset = 110

    const top =
      section.getBoundingClientRect().top +
      window.scrollY -
      navbarOffset

    window.scrollTo({
      top,
      behavior: 'smooth',
    })
  })
}

const image = {
  eggs: '/images/bodymap/bmp-11.webp',
  milk: '/images/bodymap/bmp-9.webp',
  beefLean: '/images/bodymap/bmp-1.webp',
  mushrooms: '/images/bodymap/bmp-2.webp',
  proteinCereal: '/images/bodymap/bmp-3.webp',
  salmon: '/images/bodymap/bmp-4.webp',
  carrots: '/images/bodymap/bmp-5.webp',
  spinach: '/images/bodymap/bmp-6.webp',
  silverbeet: '/images/bodymap/bmp-7.webp',
  tomatoKumato: '/images/bodymap/bmp-8.webp',
  yoghurt: '/images/bodymap/bmp-25.webp',
  parmesan: '/images/bodymap/bmp-26.webp',
  qukes: '/images/bodymap/bmp-27.webp',
  onions: '/images/bodymap/bmp-28.webp',
  oats: '/images/bodymap/bmp-21.webp',
  wholemealBread: '/images/bodymap/bmp-22.webp',
  sourdough: '/images/bodymap/bmp-23.webp',
  turkey: '/images/bodymap/bmp-24.webp',
  chicken: '/images/bodymap/bmp-13.webp',
  beefRump: '/images/bodymap/bmp-14.webp',
  lamb: '/images/bodymap/bmp-15.webp',
  fishBasa: '/images/bodymap/bmp-16.webp',
  brusselSprouts: '/images/bodymap/bmp-17.webp',
  redCabbage: '/images/bodymap/bmp-18.webp',
  prawns: '/images/bodymap/bmp-19.webp',
  yellowNectarines: '/images/bodymap/bmp-20.webp',
  cheddar: '/images/bodymap/bmp-10.webp',
  redSnapper: '/images/bodymap/bmp-12.webp',
}

const bodyParts: BodyPart[] = [
  {
    key: 'brain',
    label: 'Brain',
    icon: '/images/bodymap/bm-1.webp',
    image: '/images/bodymap/brain.svg',
    linePath: 'M 245 88 C 320 80, 405 115, 515 165',
    description:
      "Children's brains develop faster in the first five years than at any other time – this is when the foundations for learning, health and behaviour are laid down.",
    foods: [
      { name: 'Lean red meat(Beef)', image: image.beefLean },
      { name: 'Mushrooms', image: image.mushrooms },
      { name: 'Protein cereal', image: image.proteinCereal },
      { name: 'Salmon', image: image.salmon },
    ],
    why:
      'Omega-3 drives brain development and learning. Iodine fuels tissue growth. Iron powers brain function and oxygen supply.',
  },
  {
    key: 'eyes',
    label: 'Eyes',
    icon: '/images/bodymap/bm-2.webp',
    image: '/images/bodymap/eyes.svg',
    linePath: 'M 250 128 C 325 125, 410 145, 515 178',
    description:
      'Good eyesight starts on the plate. Vitamin A is needed for eyesight, growth & development - found in orange vegetables like carrots , and leafy greens like spinach and broccoli',
    foods: [
      { name: 'carrots', image: image.carrots },
      { name: 'Spinach', image: image.spinach },
      { name: 'Silverbeet', image: image.silverbeet },
      { name: 'Tomato (kumato)', image: image.tomatoKumato },
    ],
    why:
      'Carrots & leafy greens are rich in beta-carotene, which converts to Vitamin A , the that retina needs for healthy vision.',
  },
  {
    key: 'teeth',
    label: 'Teeth',
    icon: '/images/bodymap/bm-7.webp',
    image: '/images/bodymap/teeth.svg',
    linePath: 'M 210 155 C 360 155, 500 175, 660 210',
    description:
      'Tooth decay is a common diet-related disease - 1 in 3 children already have untreated tooth decay and what they eat from the start makes all the difference.',
    foods: [
      { name: 'Yoghurt', image: image.yoghurt },
      { name: 'Cheese. (Parmeasan)', image: image.parmesan },
      { name: 'Qukes', image: image.qukes },
      { name: 'Onions', image: image.onions },
    ],
    why:
      'Calcium gives teeth their strength, fluoride in tap water prevents decay and Vitamin C keeps gums healthy.',
  },
  {
    key: 'energy',
    label: 'Energy',
    icon: '/images/bodymap/bm-6.webp',
    image: '/images/bodymap/energy.svg',
    linePath: 'M 205 220 C 330 200, 515 150, 600 200',
    description:
      "A child's immune system needs Vitamin C to fight infections and zinc to heal and grow. Vitamin E also boosts immunity – the right foods together build a strong daily protection.",
    foods: [
      { name: 'oats', image: image.oats },
      { name: 'wholemeal bread', image: image.wholemealBread },
      { name: 'Sourdough', image: image.sourdough },
      { name: 'Turkey', image: image.turkey },
    ],
    why:
      "Vitamin C, zinc, iron and Vitamin E work together by fighting infections, healing wounds and building the body's immunity",
  },
  {
    key: 'muscles',
    label: 'Muscles',
    icon: '/images/bodymap/bm-4.webp',
    image: '/images/bodymap/muscles.svg',
    linePath: 'M 245 245 C 330 245, 415 235, 515 215',
    description:
      'Muscles grow and repair throughout childhood .Protein is the building block that makes it happen. Iron stores oxygen in muscle cells to fuel growth.',
    foods: [
      { name: 'chicken', image: image.chicken },
      { name: 'Red meat(Beef Rump)', image: image.beefRump },
      { name: 'Lean red meat (Lamb)', image: image.lamb },
      { name: 'Fish( Basa fillets)', image: image.fishBasa },
    ],
    why:
      'Protein builds muscle. Iron fuels its growth and stores oxygen in muscle cells via myoglobin.',
  },
  {
    key: 'immunity',
    label: 'Immunity',
    icon: '/images/bodymap/bm-5.webp',
    image: '/images/bodymap/immunity.svg',
    linePath: 'M 245 315 C 330 315, 410 270, 515 230',
    description:
      "A child's immune system needs Vitamin C to fight infections and zinc to heal and grow. Vitamin E also boosts immunity - the right foods together build a strong daily protection.",
    foods: [
      { name: 'Brussel sprouts', image: image.brusselSprouts },
      { name: 'Red Cabbage', image: image.redCabbage },
      { name: 'Prawns (black Tiger)', image: image.prawns },
      { name: 'Yellow nectarines', image: image.yellowNectarines },
    ],
    why:
      "Vitamin C, zinc, iron and Vitamin E work together by fighting infections, healing wounds and building the body's immunity",
  },
  {
    key: 'bones',
    label: 'Bones',
    icon: '/images/bodymap/bm-3.webp',
    image: '/images/bodymap/bones.svg',
    linePath: 'M 235 385 C 330 205, 415 205, 515 200',
    description:
      'Bones grow fast in childhood and even faster in the teen years. Calcium is vital for healthy bones and teeth - strong bones built now reduce the risk of osteoporosis later in life.',
    foods: [
      { name: 'Milk', image: image.milk },
      { name: 'Cheddar cheese', image: image.cheddar },
      { name: 'Eggs', image: image.eggs },
      { name: 'Fish (Red Snapper)', image: image.redSnapper },
    ],
    why:
      'Calcium is vital for bones ,teeth and skeleton development . Vitamin D helps the body absorb it to keep bones strong.',
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
  padding: 44px 0 52px;
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
  margin: 0 auto;
}

.section-heading {
  margin-bottom: 18px;
}

.section-heading h2 {
  margin: 0;
  color: #0d1c2e;
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  font-weight: 700;
  line-height: 1.08;
  letter-spacing: -0.8px;
}

.section-heading p {
  margin: 8px 0 0;
  color: #45464d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  line-height: 1.45;
}

.body-layout {
  display: grid;
  grid-template-columns: 170px minmax(320px, 1fr) 360px;
  gap: 24px;
  align-items: center;
  min-height: 590px;
}

.part-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.part-button {
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 52px;
  border: none;
  border-radius: 18px;
  padding: 10px 16px;
  background: #f8f9ff;
  color: #181e4b;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 5px 8px rgba(24, 30, 75, 0.16);
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
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: transparent;
  flex-shrink: 0;
  transition: background 0.22s ease;
}

.part-button.active .part-icon {
  background: #ffffff;
}

.part-icon img {
  width: 26px;
  height: 26px;
  object-fit: contain;
  display: block;
}

.body-figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  min-height: 520px;
  position: relative;
  z-index: 2;
}

.body-image-wrap {
  width: min(100%, 320px);
  min-height: 410px;
  display: grid;
  place-items: center;
  position: relative;
  overflow: visible;
}

.body-image {
  width: 100%;
  max-height: 430px;
  object-fit: contain;
  display: block;
  position: relative;
  z-index: 2;
}

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
  stroke-width: 2.3;
  stroke-linecap: round;
  stroke-dasharray: 9 9;
  opacity: 0.75;
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

.body-hotspot {
  position: absolute;
  z-index: 4;
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
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
  width: 20px;
  height: 20px;
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

.body-hotspot.hotspot-brain {
  top: 54px;
  left: 186px;
}

.body-hotspot.hotspot-eyes {
  top: 94px;
  left: 202px;
}

.body-hotspot.hotspot-teeth {
  top: 126px;
  left: 182px;
}

.body-hotspot.hotspot-immunity {
  top: 262px;
  left: 216px;
}

.body-hotspot.hotspot-muscles {
  top: 192px;
  left: 214px;
}

.body-hotspot.hotspot-energy {
  top: 184px;
  left: 184px;
}

.body-hotspot.hotspot-bones {
  top: 334px;
  left: 192px;
}

.click-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  color: #0d1c2e;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  line-height: 20px;
}

.click-hint img {
  width: 17px;
  height: 17px;
  object-fit: contain;
}

.info-panel {
  align-self: center;
  width: 100%;
  min-height: 560px;
  border-radius: 28px;
  padding: 22px;
  background: #ffffff;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
  position: relative;
  z-index: 3;
}

.info-panel h3 {
  margin: 0 0 8px;
  color: #006a61;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: 1.6px;
  text-transform: uppercase;
}

.description {
  display: -webkit-box;
  min-height: 66px;
  margin: 0;
  overflow: hidden;
  color: #45464d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13.5px;
  line-height: 1.55;
  -webkit-box-orient: vertical;
}

.info-panel h4 {
  margin: 16px 0 12px;
  padding-bottom: 7px;
  border-bottom: 1px solid #c6c6cd;
  color: #76777d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 1.4px;
  text-transform: uppercase;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.food-card {
  overflow: hidden;
  border: 1px solid #c6c6cd;
  border-radius: 8px;
  background: #ffffff;
  padding: 0;
  box-shadow: 0 14px 28px rgba(13, 28, 46, 0.14);
  cursor: pointer;
  text-align: left;
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease,
    background 0.22s ease;
}

.food-card:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: #7aa6d9;
  background: #f8fbff;
  box-shadow: 0 14px 28px rgba(13, 28, 46, 0.14);
}

.food-card:active {
  transform: translateY(-1px) scale(0.99);
}

.food-card img {
  width: 100%;
  height: 82px;
  object-fit: cover;
  display: block;
  transition:
    transform 0.3s ease,
    filter 0.3s ease;
}

.food-card:hover img {
  transform: scale(1.05);
  filter: brightness(1.03);
}

.food-card span {
  display: block;
  min-height: 34px;
  padding: 7px 9px;
  color: #191c1e;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 12.5px;
  font-weight: 800;
  line-height: 1.15;
  transition: color 0.22s ease;
}

.food-card:hover span {
  color: #0d1c2e;
}

.why-card {
  margin-top: 14px;
  border: 1px solid #c6c6cd;
  border-radius: 8px;
  padding: 14px;
  background: #f2f4f6;
}

.why-card h5 {
  margin: 0 0 7px;
  color: #006a61;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.why-card p {
  display: -webkit-box;
  margin: 0;
  overflow: hidden;
  color: #191c1e;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13.5px;
  line-height: 1.5;
  -webkit-box-orient: vertical;
}

.empty-panel {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

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

@media (max-width: 1024px) {
  .body-map-section {
    min-height: auto;
  }

  .body-layout {
    grid-template-columns: 1fr;
    gap: 28px;
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
    height: auto;
    min-height: 520px;
    margin: 0 auto;
  }
}

@media (max-width: 640px) {
  .body-map-section {
    padding: 48px 0 60px;
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
    min-height: unset;
    height: auto;
    border-radius: 24px;
    padding: 22px;
  }

  .description,
  .why-card p {
    -webkit-line-clamp: unset;
  }

  .food-card img {
    height: 110px;
  }
}
</style>