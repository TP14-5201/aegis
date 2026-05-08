<template>
  <section class="relative w-full bg-white overflow-hidden">
    <!-- background blob -->
    <div
      class="hidden lg:block absolute right-0 top-0 w-[520px] h-[520px]
             bg-blue-soft rounded-full -z-10"
    />

    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-end">
        
        <!-- LEFT -->
        <div class="py-16 lg:py-24">
          
          <!-- TITLE WITH GRADIENT LINE -->
          <div class="relative pl-6">
            <div
              class="absolute left-0 top-2 h-[80px] w-[6px]
                     bg-gradient-to-b from-coral to-sky rounded-full"
            />

            <h2
              class="font-volkhov font-bold text-navy
                     text-[36px] sm:text-[48px] lg:text-[64px] leading-[1.1]"
            >
              Groceries costing too much?
            </h2>
          </div>

          <!-- DESCRIPTION -->
          <p class="mt-4 lg:mt-6 font-roboto text-[18px] lg:text-[22px] leading-relaxed text-black max-w-xl">
            Master budget-friendly shopping with weekly meal plans,
            smart swaps, and nutritional information.
          </p>

          <!-- NUMBERED FEATURES -->
          <div class="mt-7 space-y-5">
            
            <!-- ITEM 1 -->
            <div class="flex items-center gap-5">
              <div
                class="flex h-14 w-14 shrink-0 items-center justify-center
                       bg-coral text-white font-roboto font-bold text-[22px]
                       rounded-[6px]"
              >
                1
              </div>

              <p class="font-roboto font-extrabold text-[16px] text-navy">
                Meal plans under budget
              </p>
            </div>

            <!-- ITEM 2 -->
            <div class="flex items-center gap-5">
              <div
                class="flex h-14 w-14 shrink-0 items-center justify-center
                       bg-sky text-white font-roboto font-bold text-[22px]
                       rounded-[6px]"
              >
                2
              </div>

              <p class="font-roboto font-extrabold text-[16px] text-navy">
                Smart ingredient substitutions
              </p>
            </div>
          </div>

          <!-- CTA -->
          <NuxtLink
            to="/get-food"
            class="group mt-8 lg:mt-10 inline-flex items-center justify-center gap-3
                   rounded-[20px] bg-sky px-8 lg:px-12
                   h-[64px] lg:h-[76px]
                   font-roboto font-extrabold text-navy-deep
                   text-[18px] lg:text-[24px]
                   shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                   transition-transform duration-300 ease-out
                   hover:-translate-y-1 active:translate-y-0"
          >
            Build My Grocery List
          </NuxtLink>
        </div>

        <!-- RIGHT IMAGE -->
        <div class="self-end flex justify-center lg:justify-end">
          <img
            class="block w-full max-w-[680px] h-auto object-contain"
            src="/images/landing/landing-3.png"
            alt="Fresh groceries on a kitchen table"
            loading="lazy"
          />
        </div>

      </div>
    </div>
  </section>
</template>