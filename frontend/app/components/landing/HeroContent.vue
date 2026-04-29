<template>
  <section class="relative w-full max-w-8xl mx-auto px-5 lg:px-12
                pt-20 lg:pt-28 pb-0
                min-h-[720px] lg:min-h-[820px]
                overflow-hidden">
    <div
      class="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]
             gap-8 lg:gap-12 items-stretch"
    >
      <!-- TEXT -->
      <div class="order-1 lg:order-1 flex flex-col justify-center pt-8 lg:pt-12 pb-12 lg:pb-16">
        <h2
          class="font-roboto font-bold text-coral
                 text-[26px] sm:text-[30px] lg:text-[34px] leading-tight"
        >
          Food Banks around Victoria
        </h2>

        <h1
          class="mt-3 lg:mt-4 font-volkhov font-bold text-navy
                 text-[44px] sm:text-[58px] lg:text-[68px] xl:text-[75.8px]
                 leading-[1.05] tracking-[-1.2px] lg:tracking-[-3px]"
        >
          Help is here<br />
          when you<br />
          need it
        </h1>

        <p
          class="mt-6 lg:mt-9 font-roboto
                 text-[18px] sm:text-[20px] lg:text-[24px]
                 leading-[1.5] text-black"
        >
          Immediate access to food support.<br />
          No judgment, no barriers.
        </p>

        <!-- CTA INSIDE HERO -->
        <NuxtLink
          to="/services"
          class="btn-cta mt-10 lg:mt-14 inline-flex items-center justify-center
                 bg-sky shadow-cta rounded-[20px]
                 h-[64px] lg:h-[76px] px-8 lg:px-12
                 font-roboto font-extrabold text-navy-deep
                 text-[18px] lg:text-[24px] w-fit"
        >
          Find Nearby Food Banks
        </NuxtLink>

        <p class="mt-4 font-roboto text-[16px] lg:text-[20px] text-ink">
          Browse anonymously&nbsp;&nbsp;•&nbsp;&nbsp;Available 24/7
        </p>
      </div>

      <!-- IMAGE -->
      <div
        class="relative order-2 lg:order-2 self-stretch
              flex items-end justify-center lg:justify-end
              h-full min-h-[320px] lg:min-h-[700px]"
      >
        <!-- BACKGROUND DECORE -->
        <img
          class="hidden lg:block absolute -top-[120px] right-[-80px]
                 w-[620px] xl:w-[720px] h-auto object-contain
                 z-0 pointer-events-none"
          src="/images/Decore.png"
          alt=""
          aria-hidden="true"
        />

        <!-- HERO IMAGE (BOTTOM ALIGNED) -->
        <img
          class="relative z-10 block w-full max-w-[720px] h-auto object-contain translate-y-[8px]"
          src="/images/landing-hero.png"
          alt="A volunteer hands a food parcel to a recipient"
          loading="eager"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>