<template>
  <section class="relative w-full bg-white overflow-hidden">
    <div
      class="hidden lg:block absolute right-0 top-0 w-[520px] h-[520px] bg-blue-soft rounded-full -z-10"
    />

    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-end">
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
            class="group mt-8 lg:mt-10 inline-flex items-center justify-center gap-3
                   rounded-[20px] bg-sky px-8 lg:px-12
                   h-[64px] lg:h-[76px]
                   font-roboto font-extrabold text-navy-deep
                   text-[18px] lg:text-[24px]
                   shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                   transition-transform duration-300 ease-out
                   hover:-translate-y-1
                   active:translate-y-0"
          >
            Build My Grocery List
            <span class="transition-transform duration-300 group-hover:translate-x-1">
            </span>
          </NuxtLink>
        </div>

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
</template>