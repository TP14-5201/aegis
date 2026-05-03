<template>
  <section class="relative w-full overflow-hidden bg-white">
    <!-- GLOBAL BLOB BACKGROUND -->
    <img
      src="/images/Decore.png"
      alt=""
      class="absolute z-0 -translate-x-1/2
             left-1/2 top-0 w-[180%] max-w-[700px]
             sm:max-w-[760px]
             lg:left-[64%] lg:top-auto lg:bottom-0 lg:w-[120%] lg:max-w-[980px]"
    />

    <div
      class="relative z-10 mx-auto grid max-w-8xl
             grid-cols-1 gap-6 px-5 pt-10
             min-h-[70vh]
             lg:min-h-[80vh] lg:grid-cols-2 lg:gap-12 lg:px-12 lg:pt-0"
    >
      <!-- LEFT CONTENT -->
      <div class="flex flex-col justify-center lg:self-center">
        <p class="text-sm font-bold uppercase tracking-wider text-[#DF6951]">
          Food Banks around you
        </p>

        <h1
          class="mt-3 font-volkhov text-[42px] font-bold leading-[0.95]
                 text-navy lg:text-[64px]"
        >
          Help is here<br />
          when you need it
        </h1>

        <p class="mt-5 max-w-xl text-[18px] leading-tight text-black lg:text-[21px]">
          Immediate access to food support across Victoria.
          No judgment, no barriers.
        </p>

        <NuxtLink
          to="/services"
          class="group mt-6 inline-flex items-center justify-center gap-3
                rounded-[20px]
                h-[64px] lg:h-[76px]
                px-8 lg:px-12
                bg-sky
                font-roboto font-extrabold text-navy-deep
                text-[18px] lg:text-[24px]
                max-w-[400px]
                w-full
                shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                transition-transform duration-300 ease-out
                hover:-translate-y-1
                active:translate-y-0"
        >
          Find Nearby Food Banks
          <span class="transition-transform duration-300 group-hover:translate-x-1">
          </span>
        </NuxtLink>

        <p class="mt-4 text-sm text-gray-500">
          Browse anonymously · Available 24/7
        </p>
      </div>

      <!-- RIGHT IMAGE -->
      <div
        class="relative flex min-h-[420px] items-end justify-center
               self-end lg:min-h-[640px]"
      >
        <img
          src="/images/landing-hero.png"
          alt="Family"
          class="relative z-10 block w-[115%] max-w-[520px]
                 sm:max-w-[620px]
                 lg:w-[130%] lg:max-w-[950px]
                 translate-y-[1px]"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts"></script>