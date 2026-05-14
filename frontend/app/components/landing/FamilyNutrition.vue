<template>
  <section class="section-large relative overflow-hidden bg-chere-slate">
    <div class="marquee-wrap">
      <div class="marquee-track">
        <span class="marquee-text">NUTRITION FIRST&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NUTRITION FIRST&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NUTRITION FIRST&nbsp;&nbsp;&nbsp;</span>
      </div>
    </div>

    <div class="section-inner family-inner relative z-10 grid items-center gap-12 lg:grid-cols-2">
      <div>
        <h2 class="font-display text-[44px] font-semibold leading-[54px] text-white lg:text-[64px] lg:leading-[64px]">
          Is Your Family Eating Right ?
        </h2>

        <div class="mt-6 flex flex-col gap-6">
          <div v-for="item in nutritionItems" :key="item.number" class="nutrition-row">
            <div class="number-badge">
              {{ item.number }}
            </div>

            <div>
              <h3 class="font-display text-[24px] font-semibold leading-8 text-white">
                {{ item.title }}
              </h3>
              <p class="mt-1 max-w-[540px] font-body text-[16px] leading-6 text-white/80">
                {{ item.text }}
              </p>
            </div>
          </div>
        </div>

        <NuxtLink to="/nutrition-guide" class="btn-blue start-learning-button">
          Start Learning
        </NuxtLink>
      </div>

      <div class="nutrition-image-wrap">
        <img src="/images/landing/landing-4.webp" alt="Nutritious food bowl" class="nutrition-image" />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const nutritionItems = [
  {
    number: 1,
    title: 'Growth and Development',
    text: "Understand how nutrition fuels your child's brain, bones and energy at every stage of childhood.",
  },
  {
    number: 2,
    title: 'Health conditions and Food Sensitivities',
    text: 'Bite-sized guides tailored to common food allergies, intolerance, and dietary needs in kids.',
  },
  {
    number: 3,
    title: 'Simple Meal Planning',
    text: "Affordable, nutritious meal ideas that meet your family's daily needs - without breaking the bank.",
  },
]
</script>

<style scoped>
.family-inner {
  min-height: theme('minHeight.section-lg');
}

.nutrition-row {
  display: flex;
  gap: 16px;
  border-bottom: 1px solid #ffffff33;
  padding-bottom: 16px;
}

.number-badge {
  display: flex;
  height: 48px;
  width: 48px;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  background: #ffffff33;
  font-family: theme('fontFamily.body');
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
}

.start-learning-button {
  margin-top: 32px;
}

.marquee-wrap {
  pointer-events: none;
  position: absolute;
  right: 8%;
  top: 50%;
  z-index: 0;
  width: 760px;
  height: 760px;
  overflow: visible;
  opacity: 0.035;
  transform: translateY(-50%) rotate(90deg);
}

.marquee-track {
  display: flex;
  width: max-content;
  white-space: nowrap;
  animation: marquee-scroll 22s linear infinite;
}

.marquee-text {
  flex-shrink: 0;
  color: #ffffff;
  font-family: theme('fontFamily.display');
  font-size: clamp(150px, 16vw, 240px);
  font-weight: 600;
  line-height: 1;
  letter-spacing: -2px;
}

@keyframes marquee-scroll {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-33.333%);
  }
}

.nutrition-image-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
}

.nutrition-image {
  width: clamp(440px, 40vw, 560px);
  height: clamp(440px, 40vw, 560px);
  border-radius: 9999px;
  object-fit: cover;
  transform: translateX(24px);
}

@media (max-width: 1024px) {
  .family-inner {
    min-height: auto;
  }

  .nutrition-image {
    transform: none;
  }
}

@media (max-width: 768px) {
  .marquee-wrap {
    left: 0;
    bottom: -10px;
    height: 90px;
    transform: none;
  }

  .marquee-text {
    font-size: 96px;
    line-height: 120px;
  }

  .nutrition-image {
    width: 100%;
    height: auto;
    max-width: 420px;
  }
}
</style>