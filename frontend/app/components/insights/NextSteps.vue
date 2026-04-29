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

      <!-- Three cards -->
      <div class="mt-10 lg:mt-14 grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
        <article
          v-for="card in cards"
          :key="card.title"
          class="rounded-[30px] bg-white p-6 lg:p-8 shadow-card flex flex-col h-full transition-transform hover:-translate-y-1 hover:shadow-2xl"
        >
          <h3 class="font-roboto font-bold text-black text-[22px] lg:text-[28px] leading-tight">
            {{ card.title }}
          </h3>
          <p class="mt-3 lg:mt-4 font-roboto text-[15px] lg:text-[16px] text-black leading-relaxed flex-grow">
            {{ card.desc }}
          </p>
          <NuxtLink
            :to="card.to"
            class="btn-cta mt-6 lg:mt-8 inline-flex items-center justify-center
                   bg-navy hover:bg-navy-deep rounded-[20px]
                   h-[58px] lg:h-[70px] px-6
                   font-roboto font-bold text-white text-[14px] lg:text-[15px]
                   text-center"
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
    to:    '/services',
    ctaLabel: 'Find Nearby Food Banks',
  },
  {
    title: 'Find groceries at best prices',
    desc:  "Tell us your needs and we'll find you the right groceries.",
    to:    '/get-food',
    ctaLabel: 'Explore Groceries',
  },
  {
    title: 'Know more about nutrition',
    desc:  "Simple guides for your family's health.",
    to:    '/nutrition-guide',
    ctaLabel: 'Learn about Nutrition',
  },
]
</script>
