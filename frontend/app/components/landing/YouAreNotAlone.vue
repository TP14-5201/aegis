<template>
  <section class="relative w-full overflow-hidden bg-[#DBEDFF]/50">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">
      <div class="relative grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-stretch">

        <!-- Left image + vector -->
        <div class="relative order-2 lg:order-1 self-stretch flex items-center justify-center min-h-[430px]">

          <!-- wrapper to center everything -->
          <div class="relative w-full flex justify-center items-center">

            <!-- Vector -->
            <img
              class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2
                    w-[420px] lg:w-[620px] xl:w-[700px]
                    opacity-100 object-contain z-0"
              src="/images/Vector.png"
            />

            <!-- Family image -->
            <img
              class="relative z-10 
                    w-[420px] lg:w-[520px] xl:w-[620px]
                    object-contain"
              src="/images/landing-know-more.png"
            />

          </div>
        </div>

        <!-- Right content: must be above vector -->
        <div class="relative z-20 order-1 lg:order-2 py-16 lg:py-20 flex flex-col items-center justify-center">
          <h2 class="font-volkhov font-bold text-navy text-[40px] lg:text-[64px] leading-tight text-center">
            You are not alone
          </h2>

          <p class="mt-4 lg:mt-6 max-w-2xl text-center font-roboto text-[16px] lg:text-[18px] text-ash">
            Thousands of families in Victoria face the same challenges every day.
          </p>

          <div class="mt-10 lg:mt-14 grid grid-cols-1 sm:grid-cols-2 gap-8 sm:gap-8 max-w-3xl">
            <div class="bg-white rounded-[16px] px-10 py-10 flex flex-col items-center text-center gap-4">
              <img
                class="h-20 lg:h-[86px] w-auto object-contain"
                src="/images/landing-1in3.png"
                alt="People icon"
                loading="lazy"
              />
              <p class="font-roboto font-black text-[36px] lg:text-[40px] leading-none text-black">
                1 in 3
              </p>
              <p class="font-roboto text-[18px] lg:text-[22px] leading-snug text-black">
                People experience<br />food insecurity
              </p>
            </div>

            <div class="bg-white rounded-[16px] px-10 py-10 flex flex-col items-center text-center gap-4">
              <img
                class="h-20 lg:h-[85px] w-auto object-contain"
                src="/images/landing-piechart.png"
                alt="Pie chart icon"
                loading="lazy"
              />
              <p class="font-roboto font-black text-[36px] lg:text-[40px] leading-none text-black">
                48%
              </p>
              <p class="font-roboto text-[18px] lg:text-[22px] leading-snug text-black">
                Renters experience<br />food insecurity
              </p>
            </div>
          </div>

          <NuxtLink
            to="/learn-more"
            class="btn-cta mt-10 lg:mt-14 inline-flex items-center justify-center
                  bg-sky shadow-cta rounded-[20px]
                  h-[64px] lg:h-[74px] px-8 lg:px-12
                  font-roboto font-extrabold text-navy-deep
                  text-[18px] lg:text-[24px]"
          >
            Get to Know More
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>