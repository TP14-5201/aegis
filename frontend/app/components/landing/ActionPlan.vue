<template>
  <section class="bg-[#dce9ff99] px-6 py-16 lg:px-10">
    <div
      class="relative mx-auto max-w-[1200px] overflow-hidden rounded-[24px] border border-[#c6c6cd4c] bg-white px-6 py-12 shadow-[0_25px_50px_-12px_rgba(0,0,0,0.25)] lg:px-16 lg:py-14"
    >
        <!-- Decorative background -->
        <img
        src="/images/landing/landing-5.png"
        alt=""
        class="pointer-events-none absolute -right-16 top-0 h-full w-[30%] object-fill opacity-100"
        />

      <!-- Header -->
      <div class="relative z-10 text-center">
        <h2
          class="font-playfair text-[38px] font-bold leading-[46px] tracking-[-0.96px] text-[#131b2e] lg:text-[48px] lg:leading-[56px]"
        >
          Not Sure Where to Start?
        </h2>

        <p
          class="mx-auto mt-3 max-w-[840px] font-jakarta text-[18px] leading-[28px] text-[#45464d]"
        >
          Tell us what you are facing and we'll guide you to the right support —
          in under 30 seconds.
        </p>

        <NuxtLink to="/get-food" class="action-plan-button">
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
            <div class="flex h-14 w-14 items-center justify-center rounded-full bg-[#dce9ff]">
            <img
                :src="card.icon"
                :alt="card.title"
                class="h-8 w-8 object-contain"
            />
            </div>

            <h3 class="mt-4 font-playfair text-[22px] font-semibold leading-[30px] text-[#0d1c2e]">
            {{ card.title }}
            </h3>

            <p class="mt-2 font-jakarta text-[15px] leading-[22px] text-[#45464d]">
            {{ card.text }}
            </p>
        </NuxtLink>
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
.font-playfair {
  font-family: 'Playfair Display', serif;
}

.font-jakarta {
  font-family: 'Plus Jakarta Sans', sans-serif;
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
  font-weight: 700;
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
</style>