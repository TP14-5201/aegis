<template>
  <section id="body-map" class="section-shell body-map">
    <div class="section-heading">
      <p class="eyebrow">Interactive body map</p>
      <h2>Feed your body right.</h2>
      <p>
        Check what your kid ate today - watch the body light up.
        Click any of the body part tab to explore.
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
          <span class="part-icon">{{ part.icon }}</span>
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
              src="/images/bodyparts/base.svg"
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
        </div>

        
      </div>

      <!-- RIGHT PANEL -->
      <article v-if="selectedPart" class="info-panel">
        <h3>{{ selectedPart.label }}</h3>
        <p class="description">{{ selectedPart.description }}</p>

        <h4>Best Foods</h4>

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
          <h4>Why it helps</h4>
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
  </section>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

type Food = {
  name: string
  image: string
}

type BodyPart = {
  key: string
  label: string
  icon: string
  image: string
  description: string
  foods: Food[]
  why: string
}

const activePart = ref<string | null>(null)

function togglePart(key: string) {
  activePart.value = activePart.value === key ? null : key
}

const image = {
  eggs: 'https://c.animaapp.com/OAm0AsyE/img/subject-36-1@2x.png',
  walnuts: 'https://c.animaapp.com/OAm0AsyE/img/subject-37-1@2x.png',
  blueberries: 'https://c.animaapp.com/OAm0AsyE/img/subject-38-1@2x.png',
  oats: 'https://c.animaapp.com/OAm0AsyE/img/subject-39-1@2x.png',
  milk: 'https://c.animaapp.com/OAm0AsyE/img/subject-40-1@2x.png',
  banana: 'https://c.animaapp.com/OAm0AsyE/img/subject-41-1@2x.png',
}

const bodyParts: BodyPart[] = [
  {
    key: 'brain',
    label: 'Brain',
    icon: '🧠',
    image: '/images/bodyparts/brain.svg',
    description: 'Helps you think, learn, remember and stay focused.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Walnut', image: image.walnuts },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'Oats', image: image.oats },
      { name: 'Banana', image: image.banana },
      { name: 'Milk', image: image.milk },
    ],
    why: 'These foods are rich in Omega-3, good fats, vitamins and minerals that support brain growth and memory.',
  },
  {
    key: 'eyes',
    label: 'Eye',
    icon: '👁️',
    image: '/images/bodyparts/eyes.svg',
    description: 'Supports healthy vision and helps children see clearly.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'Milk', image: image.milk },
    ],
    why: 'Vitamin-rich foods, protein and minerals help support everyday eye health.',
  },
  {
    key: 'bones',
    label: 'Bones',
    icon: '🦴',
    image: '/images/bodyparts/bones.svg',
    description: 'Gives your body shape and helps children stand, walk and grow strong.',
    foods: [
      { name: 'Milk', image: image.milk },
      { name: 'Eggs', image: image.eggs },
      { name: 'Oats', image: image.oats },
    ],
    why: 'Calcium, vitamin D and protein help build strong bones during childhood.',
  },
  {
    key: 'muscles',
    label: 'Muscles',
    icon: '💪',
    image: '/images/bodyparts/muscles.svg',
    description: 'Helps children move, run, play and stay active.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Milk', image: image.milk },
      { name: 'Banana', image: image.banana },
    ],
    why: 'Protein-rich foods help muscles grow, repair and stay strong.',
  },
  {
    key: 'immunity',
    label: 'Immunity',
    icon: '🛡️',
    image: '/images/bodyparts/immunity.svg',
    description: 'Protects your body from germs and helps children stay healthy.',
    foods: [
      { name: 'Eggs', image: image.eggs },
      { name: 'Blueberries', image: image.blueberries },
      { name: 'Milk', image: image.milk },
    ],
    why: 'Vitamins, minerals and protein support the immune system and help the body fight sickness.',
  },
  {
    key: 'energy',
    label: 'Energy',
    icon: '⚡',
    image: '/images/bodyparts/energy.svg',
    description: 'Gives children power for learning, playing and daily activities.',
    foods: [
      { name: 'Oats', image: image.oats },
      { name: 'Banana', image: image.banana },
      { name: 'Milk', image: image.milk },
    ],
    why: 'Carbohydrates and balanced meals provide steady energy throughout the day.',
  },
  {
    key: 'teeth',
    label: 'Teeth',
    icon: '🦷',
    image: '/images/bodyparts/teeth.svg',
    description: 'Helps children bite, chew and keep a bright smile.',
    foods: [
      { name: 'Milk', image: image.milk },
      { name: 'Eggs', image: image.eggs },
      { name: 'Oats', image: image.oats },
    ],
    why: 'Calcium-rich and low-sugar foods help protect teeth and support healthy gums.',
  },
]

const selectedPart = computed(() => {
  return bodyParts.find((part) => part.key === activePart.value) || null
})
</script>

<style scoped>
.section-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
}

.body-map {
  padding: 56px 0 72px;
  background: #ffffff;
}

.section-heading {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #df6951 !important;
  font-size: 16px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.section-heading h2 {
  margin: 0;
  color: #181e4b;
  font-family: Volkhov, Georgia, serif;
  font-size: clamp(34px, 4vw, 54px);
  line-height: 1.05;
  font-weight: 700;
}

.section-heading p {
  margin: 14px 0 0;
  color: #111111;
  font-size: clamp(16px, 1.5vw, 22px);
  line-height: 1.5;
}

.body-layout {
  display: grid;
  grid-template-columns: 170px minmax(280px, 1fr) 360px;
  gap: 40px;
  align-items: center;
}

.part-list {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.part-button {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 56px;
  border: none;
  border-radius: 18px;
  padding: 12px 18px;
  background: #d9efff;
  color: #181e4b;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 5px 8px rgba(24, 30, 75, 0.18);
  transition: 0.22s ease;
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
  background: rgba(255, 255, 255, 0.95);
  color: #181e4b;
  font-size: 20px;
  flex-shrink: 0;
}

.body-figure {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 520px;
}

.body-image-wrap {
  width: min(100%, 340px);
  min-height: 470px;
  display: grid;
  place-items: center;
}

.body-image {
  width: 100%;
  max-height: 500px;
  object-fit: contain;
  display: block;
}

.hint {
  margin: 18px 0 0;
  color: #181e4b;
  font-size: 14px;
  font-weight: 500;
}

.info-panel {
  align-self: center;
  border-radius: 28px;
  padding: 28px;
  background: #dff1ff;
}

.info-panel h3 {
  margin: 0 0 18px;
  color: #000000;
  font-size: 24px;
  font-weight: 800;
}

.description {
  margin: 0;
  color: #111111;
  font-size: 16px;
  line-height: 1.55;
}

.info-panel h4 {
  margin: 24px 0 14px;
  color: #df6951;
  font-size: 16px;
  font-weight: 800;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.food-card {
  min-height: 86px;
  border-radius: 18px;
  padding: 10px;
  background: #ffffff;
  text-align: center;
}

.food-card img {
  width: 46px;
  height: 38px;
  object-fit: contain;
  display: block;
  margin: 0 auto 8px;
}

.food-card span {
  color: #111111;
  font-size: 14px;
}

.why-card {
  margin-top: 28px;
  border-radius: 22px;
  padding: 22px;
  background: #ffffff;
}

.why-card h4 {
  margin: 0 0 12px;
  color: #000000;
}

.why-card p {
  margin: 0;
  color: #111111;
  font-size: 16px;
  line-height: 1.5;
}

.empty-panel {
  min-height: 260px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.body-highlight-enter-active,
.body-highlight-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.body-highlight-enter-from,
.body-highlight-leave-to {
  opacity: 0;
  transform: scale(0.98);
}

/* TABLET */
@media (max-width: 1024px) {
  .body-layout {
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .part-list {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    order: 1;
  }

  .body-figure {
    order: 2;
    min-height: auto;
  }

  .info-panel {
    order: 3;
    width: min(100%, 620px);
    margin: 0 auto;
  }

  .part-button {
    justify-content: center;
    padding: 12px;
  }
}

/* MOBILE */
@media (max-width: 640px) {
  .section-shell {
    width: min(100% - 24px, 1180px);
  }

  .body-map {
    padding: 40px 0 56px;
  }

  .section-heading {
    text-align: left;
    margin-bottom: 24px;
  }

  .eyebrow {
    font-size: 13px;
  }

  .section-heading h2 {
    font-size: 34px;
  }

  .section-heading p {
    font-size: 16px;
  }

  .part-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .part-button {
    min-height: 54px;
    border-radius: 16px;
    font-size: 14px;
    gap: 10px;
  }

  .part-icon {
    width: 32px;
    height: 32px;
    font-size: 17px;
  }

  .body-image-wrap {
    width: min(100%, 260px);
    min-height: 360px;
  }

  .body-image {
    max-height: 360px;
  }

  .hint {
    font-size: 13px;
  }

  .info-panel {
    border-radius: 24px;
    padding: 22px;
  }

  .info-panel h3 {
    font-size: 22px;
  }

  .description,
  .why-card p {
    font-size: 15px;
  }

  .food-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }

  .food-card {
    min-height: 84px;
  }

  .why-card {
    padding: 18px;
  }
}

/* SMALL MOBILE */
@media (max-width: 380px) {
  .part-list,
  .food-grid {
    grid-template-columns: 1fr;
  }

  .body-image-wrap {
    width: min(100%, 230px);
    min-height: 320px;
  }
}
</style>