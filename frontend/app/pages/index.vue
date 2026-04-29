<template>
  <div class="w-full bg-white overflow-x-hidden">
    <TopNavigation />

    <!-- Hero Section -->
    <LandingHeroContent />

    <!-- You're Not Alone Section -->
    <LandingYouAreNotAlone />

    <!-- Groceries Costing Too Much Section -->
    <section class="relative w-full bg-white overflow-hidden">
      <!-- ellipse background -->
      <div
        class="hidden lg:block absolute right-0 top-0 w-[520px] h-[520px] bg-blue-soft rounded-full -z-10"
      />

      <div class="max-w-8xl mx-auto px-5 lg:px-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-end">
          <!-- Text keeps padding -->
          <div class="py-16 lg:py-24">
            <h2
              class="font-volkhov font-bold text-navy
                    text-[36px] sm:text-[48px] lg:text-[64px] leading-[1.1]"
            >
              Groceries costing too much?
            </h2>

            <p class="mt-6 lg:mt-8 font-roboto font-bold text-coral text-[24px] lg:text-[34px]">
              Healthy eating on a budget
            </p>

            <p class="mt-4 lg:mt-6 font-roboto text-[18px] lg:text-[24px] leading-relaxed text-black max-w-xl">
              Smart ingredient swaps and budget-friendly recipes. Learn to stretch your
              grocery budget while nourishing your family without breaking the bank.
            </p>

            <NuxtLink
              to="/get-food"
              class="btn-cta mt-8 lg:mt-10 inline-flex items-center justify-center
                    bg-sky shadow-cta rounded-[20px]
                    h-[64px] lg:h-[76px] px-8 lg:px-12
                    font-roboto font-extrabold text-navy-deep
                    text-[18px] lg:text-[24px]"
            >
              Build My Grocery List
            </NuxtLink>
          </div>

          <!-- Image sits at section bottom -->
          <div class="self-end flex justify-center lg:justify-end">
            <img
              class="block w-full max-w-[680px] h-auto object-contain"
              src="/images/landing-grocery.png"
              alt="Fresh groceries on a kitchen table"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Family Nutrition Section -->
    <LandingFamilyNutrition />

    <!-- About Us Section (to add later)-->

  </div>
</template>

<script setup lang="ts">
useHead({ title: 'ChereBowl - Home' })
</script>
