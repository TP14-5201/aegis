<template>
  <section class="w-full bg-white py-16 lg:py-24">
    <div class="max-w-8xl mx-auto px-5 lg:px-12">

      <!-- Heading -->
      <p class="text-coral font-bold uppercase tracking-widest text-[14px] lg:text-[16px]">
        The behavioural impact
      </p>

      <h2 class="mt-3 font-volkhov font-bold text-navy text-[28px] lg:text-[48px]">
        The hidden cost of food insecurity
      </h2>

      <p class="mt-4 text-black max-w-3xl text-[16px] lg:text-[20px]">
        Food insecurity doesn't just leave families hungry. It reshapes habits, emotions, and long-term wellbeing.
      </p>

      <!-- ================= DESKTOP ================= -->
      <div class="relative mt-12 min-h-[600px] hidden lg:block">

        <!-- Donut -->
        <img
          src="/images/impacts-donut.png"
          class="absolute left-1/2 top-1/2 w-[420px] -translate-x-1/2 -translate-y-1/2"
          alt="Impacts donut chart"
        />

        <!-- LEFT TOP -->
        <div class="absolute left-[6%] top-[20%] border border-[#6A8F7B] rounded-[8px] px-4 py-3 bg-white w-[260px]">
          <p class="font-bold text-[22px] text-[#6A8F7B]">13.9%</p>
          <p>Drink sugary soft drinks daily</p>
        </div>

        <!-- LEFT MID -->
        <div class="absolute left-[0%] top-[48%] border border-[#E9B15C] rounded-[8px] px-4 py-3 bg-white w-[240px]">
          <p class="font-bold text-[22px] text-[#E9B15C]">15.7%</p>
          <p>Eat fast food 2x a week</p>
        </div>

        <!-- LEFT BOTTOM -->
        <div class="absolute left-[14%] bottom-[12%] border border-[#B43D68] rounded-[8px] px-4 py-3 bg-white w-[280px]">
          <p class="font-bold text-[22px] text-[#B43D68]">31.3%</p>
          <p>Report poor physical health</p>
        </div>

        <!-- RIGHT TOP -->
        <div class="absolute right-[8%] top-[10%] border border-[#4F83AF] rounded-[8px] px-4 py-3 bg-white w-[280px]">
          <p class="font-bold text-[22px] text-[#4F83AF]">7.8%</p>
          <p>Eat almost no vegetables daily</p>
        </div>

        <!-- RIGHT MID -->
        <div class="absolute right-[0%] top-[45%] border border-[#4F83AF] rounded-[8px] px-4 py-3 bg-white w-[300px]">
          <p class="font-bold text-[22px] text-[#4F83AF]">31.3%</p>
          <p>Suffer serious mental distress</p>
        </div>

      </div>

      <!-- ================= MOBILE ================= -->
      <div class="mt-10 flex flex-col items-center gap-6 lg:hidden">

        <img
          src="/images/impacts-donut.png"
          class="w-[260px]"
          alt="Impacts donut chart"
        />

        <div class="w-full flex flex-col gap-4">

          <div class="border border-[#4F83AF] rounded-[8px] px-4 py-3 bg-white">
            <p class="font-bold text-[20px] text-[#4F83AF]">7.8%</p>
            <p>Eat almost no vegetables daily</p>
          </div>

          <div class="border border-[#4F83AF] rounded-[8px] px-4 py-3 bg-white">
            <p class="font-bold text-[20px] text-[#4F83AF]">31.3%</p>
            <p>Suffer serious mental distress</p>
          </div>

          <div class="border border-[#B43D68] rounded-[8px] px-4 py-3 bg-white">
            <p class="font-bold text-[20px] text-[#B43D68]">31.3%</p>
            <p>Report poor physical health</p>
          </div>

          <div class="border border-[#E9B15C] rounded-[8px] px-4 py-3 bg-white">
            <p class="font-bold text-[20px] text-[#E9B15C]">15.7%</p>
            <p>Eat fast food 2x a week</p>
          </div>

          <div class="border border-[#6A8F7B] rounded-[8px] px-4 py-3 bg-white">
            <p class="font-bold text-[20px] text-[#6A8F7B]">13.9%</p>
            <p>Drink sugary soft drinks daily</p>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>