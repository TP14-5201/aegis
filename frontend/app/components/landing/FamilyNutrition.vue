<template>
  <section class="w-full bg-sky-tint pt-16 lg:pt-24 pb-12 lg:pb-16 overflow-hidden">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-center">
        <!-- Image frame -->
        <div class="order-2 lg:order-1 flex items-center justify-center">
          <div class="relative w-full max-w-[620px]">
  
            <!-- photo -->
            <img
              class="relative z-10 w-full h-auto object-contain"
              src="/images/landing/landing-4.png"
              alt="A child eating a meal"
              loading="lazy"
            />
          </div>
        </div>

        <!-- Text -->
        <div class="order-1 lg:order-2 flex flex-col gap-5 lg:gap-7 lg:pl-4">
          <!-- small gradient line -->
          <div class="flex justify-start lg:justify-end">
            <div class="h-[6px] w-[90px] bg-gradient-to-r from-sky to-coral" />
          </div>

          <h2
            class="font-volkhov font-bold text-navy
                   text-[36px] sm:text-[48px] lg:text-[64px] leading-[1.05]
                   lg:text-right"
          >
            Is your family<br />eating right?
          </h2>

          <p
            class="font-roboto font-bold text-coral
                   text-[24px] lg:text-[30px] leading-tight
                   lg:text-right"
          >
            Empowered Learning
          </p>

          <p
            class="font-roboto text-[17px] lg:text-[20px] leading-[1.5]
                   text-black max-w-xl lg:ml-auto lg:text-right"
          >
            Access bite-sized guides on kids' nutrition - from growth and sleep to
            health conditions and food sensitivities. Every meal counts.
          </p>

          <div class="mt-2 lg:mt-4 flex lg:justify-end">
            <NuxtLink
              to="/nutrition-guide"
              class="group inline-flex items-center justify-center gap-3
                    bg-sky rounded-[20px]
                    h-[64px] lg:h-[76px] px-8 lg:px-12
                    font-roboto font-extrabold text-black
                    text-[18px] lg:text-[24px]
                    shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                    transition-transform duration-300 ease-out
                    hover:-translate-y-1
                    active:translate-y-0"
            >
              Start Learning
              <span class="transition-transform duration-300 group-hover:translate-x-1">
              </span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>