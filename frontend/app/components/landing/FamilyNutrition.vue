<template>
  <section class="relative overflow-hidden bg-[linear-gradient(154deg,#233144_0%,#565e74_100%)] px-6 py-20 lg:px-10 lg:py-[100px]">
    <div class="marquee-wrap">
      <div class="marquee-track">
        <span class="marquee-text">NUTRITION FIRST&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NUTRITION FIRSTR&nbsp;&nbsp;&nbsp;</span>
        <span class="marquee-text">NUTRITION FIRST&nbsp;&nbsp;&nbsp;</span>
      </div>
    </div>

    <div class="relative z-10 mx-auto grid max-w-[1200px] items-center gap-12 lg:grid-cols-2">
      <div>
        <h2 class="font-playfair text-[44px] font-semibold leading-[54px] text-white lg:text-[64px] lg:leading-[64px]">
          Is Your Family Eating Right ?
        </h2>

        <div class="mt-6 flex flex-col gap-6">
          <div v-for="item in nutritionItems" :key="item.number" class="nutrition-row">
            <div class="number-badge">
              {{ item.number }}
            </div>

            <div>
              <h3 class="font-playfair text-[24px] font-semibold leading-[32px] text-white">
                {{ item.title }}
              </h3>
              <p class="mt-1 max-w-[540px] font-jakarta text-[16px] leading-[24px] text-white/80">
                {{ item.text }}
              </p>
            </div>
          </div>
        </div>

        <NuxtLink to="/nutrition-guide" class="start-learning-button">
          Start Learning
        </NuxtLink>
      </div>

      <div class="nutrition-image-wrap">
        <img
          src="/images/landing/landing-4.png"
          alt="Nutritious food bowl"
          class="nutrition-image"
        />
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

const cards = [
  {
    title: 'I need food today',
    text: 'Find open relief services near you right now',
    icon: '/images/landing/landing-4.png',
    to: '/food-banks',
  },
  {
    title: 'I have a limited budget',
    text: 'Stretch your weekly shop further',
    icon: '/images/landing/landing-4.png',
    to: '/get-food',
  },
  {
    title: "Unsure what's in my food?",
    text: 'Know nutritious food that benefits your child',
    icon: '/images/landing/landing-4.png',
    to: '/nutrition-guide',
  },
  {
    title: 'Understand my area',
    text: 'Explore food insecurity data in Victoria',
    icon: '/images/landing/landing-4.png',
    to: '/learn-more',
  },
]
</script>

<style scoped>
.font-playfair {
  font-family: 'Playfair Display', serif;
}

.font-jakarta {
  font-family: 'Plus Jakarta Sans', sans-serif;
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
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
}

.start-learning-button {
  margin-top: 32px;
  display: inline-flex;
  height: 56px;
  width: 258px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #396477;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 800;
  line-height: 20px;
  color: #ffffff;
  box-shadow:
    0 8px 10px -6px #0000001a,
    0 20px 25px -5px #0000001a;
}

.action-plan-button {
  margin-top: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #131b2e;
  padding: 16px 48px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 18px;
  font-weight: 400;
  line-height: 24px;
  color: #ffffff;
  box-shadow:
    0 4px 6px -4px #0000001a,
    0 10px 15px -3px #0000001a;
}

.cta-card {
  display: flex;
  min-height: 220px;
  flex-direction: column;
  align-items: center;
  border: 1px solid #c6c6cd33;
  border-radius: 12px;
  background: #eff4ff;
  padding: 24px 16px 32px;
  text-align: center;
  box-shadow: 0 1px 2px #0000000d;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.cta-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px #00000014;
}
.marquee-wrap {
  pointer-events: none;
  position: absolute;
  left: 13%;
  bottom: 0px;
  z-index: 0;
  width: 100%;
  height: 180px;
  overflow: hidden;
  opacity: 0.035;
  transform: rotate(90deg);
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
  font-family: 'Playfair Display', serif;
  font-size: 240px;
  font-weight: 600;
  line-height: 160px;
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
  justify-content: center;
  align-items: center;
}

.nutrition-image {
  width: 560px;
  height: 560px;
  border-radius: 9999px;
  object-fit: cover;

  box-shadow: none;

  transform: translateX(24px);
}

@media (max-width: 768px) {
  .start-learning-button,
  .action-plan-button {
    width: 100%;
  }
}
</style>