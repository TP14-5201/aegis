<template>
  <div class="relative w-full overflow-hidden rounded-3xl border border-[#c4c6cf4c] bg-[#f2f4f6]">

    <!-- Low-opacity background icon -->
    <div class="pointer-events-none absolute right-[-39px] top-[-23px] opacity-[0.03]">
      <svg width="161" height="177" viewBox="0 0 161 177" fill="#000">
        <rect x="10" y="10" width="141" height="157" rx="16" ry="16"/>
      </svg>
    </div>

    <!-- Counter pill -->
    <div class="absolute left-10 top-14 inline-flex items-baseline gap-2 rounded-2xl border border-[#c4c6cf33] bg-white px-6 py-3 shadow-sm">
      <span class="font-body text-[48px] font-bold leading-none tracking-tight text-[#df6951]">{{ checkedCount }}</span>
      <span class="font-body text-[24px] font-semibold text-[#44474e]">/ {{ items.length }}</span>
    </div>

    <!-- Title area -->
    <div class="ml-[191px] pt-16">
      <p class="font-body text-[14px] font-bold uppercase tracking-[1.4px] text-[#df6951]">Pack-Up Checklist</p>
      <h2 class="mt-2 font-display text-[28px] font-semibold text-[#191c1e] lg:text-[32px]">
        Tick off as you go — items to bring.
      </h2>
    </div>

    <!-- Close button -->
    <button
      @click="$emit('close')"
      class="absolute right-10 top-9 rounded-xl bg-[#0054cd] px-10 py-4 font-body text-[18px] font-semibold text-white shadow transition hover:brightness-110 active:scale-95"
    >
      Close
    </button>

    <!-- Checklist grid -->
    <div class="mx-10 mb-10 mt-8 grid grid-cols-2 gap-5 lg:grid-cols-4">
      <div
        v-for="(item, i) in items"
        :key="i"
        class="flex cursor-pointer items-start gap-4 rounded-2xl border bg-white p-6 transition-all duration-150 hover:shadow-sm"
        :class="checked[i] ? 'border-[#001b3d] shadow-md' : 'border-[#c4c6cf]'"
        @click="toggle(i)"
      >
        <!-- Checkbox -->
        <div
          class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded border-2 transition-all"
          :class="checked[i] ? 'border-[#001b3d] bg-[#001b3d]' : 'border-[#c4c6cf] bg-white'"
        >
          <svg v-if="checked[i]" width="11" height="9" viewBox="0 0 11 9" fill="none">
            <path d="M1 4.5L4 7.5L10 1" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>

        <!-- Label + description -->
        <div>
          <p
            class="font-body text-[13px] font-bold uppercase tracking-[-0.3px] text-[#191c1e]"
            :class="{ 'line-through opacity-50': checked[i] }"
          >{{ item.label }}</p>
          <p class="mt-1.5 whitespace-pre-line font-body text-[14px] leading-snug text-[#44474e]">{{ item.description }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
defineEmits<{ close: [] }>()

const items = [
  { label: 'Reusable Bags',    description: '2–3 sturdy ones\ngroceries can\nbe heavy' },
  { label: 'Photo ID',         description: 'Driver licence,\nMedicare or any\nphoto card' },
  { label: 'Concession Card',  description: 'If you have one,\nnot required' },
  { label: 'Cool Bag / Esky',  description: 'For frozen items if\nit\'s warm out' },
  { label: 'Phone Charged',    description: 'For directions,\ncalling ahead,\nfamily contact' },
  { label: 'Water Bottle',     description: 'Stay hydrated\nwhile you are out' },
  { label: 'PTV Card',         description: 'When you travel\nby public transport' },
  { label: 'Needs List',       description: 'Allergies, dietary,\nfamily size' },
]

const checked = ref<boolean[]>(Array(items.length).fill(false))
const checkedCount = computed(() => checked.value.filter(Boolean).length)

const toggle = (i: number) => {
  checked.value = checked.value.map((v, idx) => idx === i ? !v : v)
}
</script>
