<template>
  <section class="section-large bg-chere-sky/60">
    <div class="section-inner">
      <div class="action-panel">
        <!-- Decorative background -->
        <img
          src="/images/landing/landing-5.png"
          alt=""
          class="pointer-events-none absolute -right-16 top-0 h-full w-[30%] object-fill opacity-100"
        />

        <!-- Header -->
        <div class="relative z-10 text-center">
          <h2 class="heading-lg text-chere-ink">
            Not Sure Where to Start?
          </h2>

          <p class="mx-auto mt-3 max-w-[840px] font-body text-[18px] leading-7 text-chere-text">
            Tell us what you are facing and we'll guide you to the right support —
            in under 30 seconds.
          </p>

          <NuxtLink to="/get-food" class="btn-dark mt-7">
            Get My Action Plan
          </NuxtLink>
        </div>

        <!-- Cards -->
        <div class="relative z-10 mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <NuxtLink
            v-for="card in cards"
            :key="card.title"
            :to="card.to"
            class="cta-card"
          >
            <div
              class="flex h-14 w-14 items-center justify-center rounded-full border border-white/60 bg-white/70 shadow-sm backdrop-blur-sm"
            >
              <img
                :src="card.icon"
                :alt="card.title"
                class="h-8 w-8 object-contain"
              />
            </div>

            <h3 class="mt-4 font-display text-[22px] font-semibold leading-[30px] text-chere-navy">
              {{ card.title }}
            </h3>

            <p class="mt-2 font-body text-[15px] leading-[22px] text-chere-text">
              {{ card.text }}
            </p>
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const cards = [
  {
    icon: '/images/landing/icon-4.png',
    title: 'I need food today',
    text: 'Find open relief services near you right now',
    to: '/food-banks',
  },
  {
    icon: '/images/landing/icon-5.png',
    title: 'I have a limited budget',
    text: 'Stretch your weekly shop further',
    to: '/get-food',
  },
  {
    icon: '/images/landing/icon-6.png',
    title: "Unsure what's in my food?",
    text: 'Know nutritious food that benefits your child',
    to: '/nutrition-guide',
  },
  {
    icon: '/images/landing/icon-7.png',
    title: 'Understand my area',
    text: 'Explore food insecurity data in Victoria',
    to: '/learn-more',
  },
]
</script>

<style scoped>
.action-panel {
  position: relative;
  overflow: hidden;
  border: 1px solid rgb(198 198 205 / 30%);
  border-radius: 24px;
  background: #ffffff;
  padding: clamp(40px, 6vh, 56px) clamp(24px, 5vw, 64px);
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 25%);
}

.cta-card {
  display: flex;
  min-height: 220px;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgb(198 198 205 / 22%);
  border-radius: 20px;
  background: linear-gradient(
    180deg,
    rgb(239 244 255 / 96%) 0%,
    rgb(231 238 255 / 92%) 100%
  );
  padding: 28px 18px 34px;
  text-align: center;
  box-shadow:
    0 10px 30px rgb(0 0 0 / 6%),
    0 2px 6px rgb(0 0 0 / 4%);
  backdrop-filter: blur(6px);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease,
    border-color 0.25s ease;
}

.cta-card:hover {
  transform: translateY(-6px);
  border-color: rgb(184 222 255 / 70%);
  box-shadow:
    0 20px 40px rgb(68 154 196 / 14%),
    0 8px 18px rgb(0 0 0 / 8%);
}

@media (max-width: 768px) {
  .action-panel {
    border-radius: 20px;
  }
}
</style>