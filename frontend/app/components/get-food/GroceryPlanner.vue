<template>
  <section id="grocery-planner" class="w-full bg-white py-16 lg:py-20">
    <div class="mx-auto max-w-6xl px-5">
      <div class="rounded-3xl bg-white p-8 shadow-[0_20px_60px_rgba(0,0,0,0.1)] lg:p-12">
        <h2 class="font-volkhov text-[28px] font-bold text-navy lg:text-[40px]">
          Tell us what you need
        </h2>

        <p class="mt-3 text-gray-600">
          Find budget-friendly ingredients tailored to your family's needs
        </p>

        <div class="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
          <div>
            <label class="text-sm font-semibold text-navy">Budget ($)</label>
            <input
              type="text"
              placeholder="100"
              class="mt-2 h-12 w-full rounded-xl bg-[#E6F0FA] px-4 outline-none"
            />
          </div>

          <div>
            <label class="text-sm font-semibold text-navy">Number of People</label>
            <input
              type="text"
              placeholder="4"
              class="mt-2 h-12 w-full rounded-xl bg-[#E6F0FA] px-4 outline-none"
            />
          </div>

          <div>
            <label class="text-sm font-semibold text-navy">
              Number of Different Dishes
            </label>
            <input
              type="text"
              placeholder="4"
              class="mt-2 h-12 w-full rounded-xl bg-[#E6F0FA] px-4 outline-none"
            />
          </div>

          <div>
            <label class="text-sm font-semibold text-navy">Type of Cuisine</label>

            <div class="relative mt-2">
              <select
                v-model="cuisine"
                class="h-12 w-full appearance-none rounded-xl bg-[#E6F0FA] px-4 pr-10 text-gray-700 outline-none"
              >
                <option value="" disabled>Select cuisine</option>
                <option value="Australian">Australian</option>
                <option value="Indian">Indian</option>
                <option value="Chinese">Chinese</option>
                <option value="Japanese">Japanese</option>
                <option value="Italian">Italian</option>
                <option value="Mediterranean">Mediterranean</option>
                <option value="Thai">Thai</option>
                <option value="Vietnamese">Vietnamese</option>
              </select>

              <span
                class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"
              >
                ▼
              </span>
            </div>
          </div>
        </div>

        <div class="mt-8">
          <p class="mb-3 text-sm font-semibold text-navy">
            Dietary Needs (select all that apply)
          </p>

          <div class="flex flex-wrap gap-3">
            <button type="button" class="rounded-full bg-gray-100 px-4 py-2 text-gray-700">
              Vegetarian
            </button>
            <button type="button" class="rounded-full bg-gray-100 px-4 py-2 text-gray-700">
              Vegan
            </button>
            <button type="button" class="rounded-full bg-gray-100 px-4 py-2 text-gray-700">
              Gluten-free
            </button>
            <button type="button" class="rounded-full bg-gray-100 px-4 py-2 text-gray-700">
              Dairy-free
            </button>
            <button type="button" class="rounded-full bg-gray-100 px-4 py-2 text-gray-700">
              Halal
            </button>
          </div>
        </div>

        <div class="mt-10 flex justify-center">
          <button
            type="button"
            class="rounded-full bg-[#B8DEFF] px-8 py-4 font-bold text-navy"
          >
            Get Ingredient Recommendations
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const cuisine = ref('')
</script>