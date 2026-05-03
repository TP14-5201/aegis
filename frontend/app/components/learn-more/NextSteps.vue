<template>
  <section class="w-full bg-sky-tint py-12 lg:py-20">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <h2
        class="font-volkhov font-bold text-navy
               text-[30px] sm:text-[36px] lg:text-[48px] leading-tight"
      >
        Ready to take the next step?
      </h2>

      <p class="mt-3 font-roboto font-bold text-coral text-[20px] lg:text-[28px]">
        Here is where to start
      </p>

      <div class="mt-10 lg:mt-14 grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
        <article
          v-for="card in cards"
          :key="card.title"
          class="rounded-[30px] bg-white p-6 lg:p-8 shadow-card flex flex-col h-full transition-all duration-300 hover:-translate-y-1 hover:shadow-xl"
        >
          <h3 class="font-roboto font-bold text-black text-[22px] lg:text-[28px] leading-tight">
            {{ card.title }}
          </h3>

          <p class="mt-3 lg:mt-4 font-roboto text-[15px] lg:text-[16px] text-black leading-relaxed flex-grow">
            {{ card.desc }}
          </p>

          <NuxtLink
            :to="card.to"
            class="mt-6 lg:mt-8 inline-flex h-[58px] lg:h-[70px] items-center justify-center rounded-[20px]
                   bg-navy px-6 text-center font-roboto text-[14px] lg:text-[15px] font-bold text-white
                   shadow-[0_12px_28px_rgba(20,45,76,0.18)]
                   transition-all duration-300 ease-out
                   hover:-translate-y-1 hover:bg-navy-deep hover:shadow-[0_16px_34px_rgba(20,45,76,0.25)]
                   active:translate-y-0"
          >
            {{ card.ctaLabel }}
          </NuxtLink>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const cards = [
  {
    title: 'Find Food Banks near me',
    desc:  'Find free food support open right now.',
    to:    '/food-banks',
    ctaLabel: 'Find Nearby Food Banks',
  },
  {
    title: 'Find groceries at best prices',
    desc: "Tell us your needs and we'll find you the right groceries.",
    to: '/get-food',
    ctaLabel: 'Explore Groceries',
  },
  {
    title: 'Know more about nutrition',
    desc: "Simple guides for your family's health.",
    to: '/nutrition-guide',
    ctaLabel: 'Learn about Nutrition',
  },
]
</script>