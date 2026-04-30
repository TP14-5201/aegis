<template>
  <section class="w-full bg-sky-tint pt-16 lg:pt-24 pb-0 overflow-hidden">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 items-stretch">
        <!-- Image -->
        <div class="order-2 lg:order-1 self-end flex items-end justify-center">
          <img
            class="w-full max-w-[620px] mx-auto h-auto object-contain"
            src="/images/landing-family.png"
            alt="A family eating together at a kitchen table"
            loading="lazy"
          />
        </div>

        <!-- Text -->
        <div class="order-1 lg:order-2 flex flex-col gap-5 lg:gap-7">
          <h2
            class="font-volkhov font-bold text-navy
                   text-[36px] sm:text-[48px] lg:text-[64px] leading-[1.1]"
          >
            Is your family<br />eating right?
          </h2>

          <p class="font-roboto font-bold text-coral text-[26px] lg:text-[34px] leading-tight">
            Empowered Learning
          </p>

          <p class="font-roboto text-[18px] lg:text-[24px] leading-[1.5] text-black max-w-xl">
            Access bite-sized guides on kids' nutrition – from growth and sleep to
            health conditions and food sensitivities. Every meal counts.
          </p>

          <div class="mt-2 lg:mt-4">
            <NuxtLink
              to="/nutrition-guide"
              class="btn-cta inline-flex items-center justify-center
                     bg-sky shadow-cta rounded-[20px]
                     h-[64px] lg:h-[76px] px-8 lg:px-12
                     font-roboto font-extrabold text-black
                     text-[18px] lg:text-[24px]"
            >
              Start Learning
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>
