<template>
  <div class="relative w-full rounded-2xl border border-[#c4c6cf] bg-[#DCE9FF]/50 shadow-sm transition hover:shadow-md">
    <!-- Status badge + expand arrow -->
    <div class="flex items-start justify-between px-8 pt-8">
      <span
        :class="[badgeBg, badgeTextColor, 'inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[13px] font-bold leading-none']"
        :style="{ borderColor: badgeBorderColor }"
      >
        <span :class="[dotBg, 'h-[6px] w-[6px] shrink-0 rounded-full']" />
        {{ statusLabel }}
      </span>

      <button
        class="mt-0.5 text-[#44474e] transition-colors hover:text-[#001b3d]"
        @click="$emit('select')"
        aria-label="Expand"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path d="M7 17L17 7M17 7H7M17 7v10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- Service name -->
    <h3 class="px-8 pt-3 font-display text-[22px] font-bold leading-snug text-[#001b3d]">{{ name }}</h3>

    <!-- Address + website -->
    <div class="px-8 pt-4 space-y-3">
      <div v-if="address" class="flex items-start gap-4">
        <svg class="mt-0.5 shrink-0" width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M12 21C12 21 4 13.5 4 9a8 8 0 1 1 16 0c0 4.5-8 12-8 12z" stroke="#44474e" stroke-width="1.8"/>
          <circle cx="12" cy="9" r="2.5" stroke="#44474e" stroke-width="1.8"/>
        </svg>
        <p class="text-[12px] font-medium leading-snug text-[#44474e]">{{ address }}</p>
      </div>
      <div v-if="website" class="flex items-center gap-4">
        <svg class="shrink-0" width="18" height="18" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="#44474e" stroke-width="1.8"/>
          <ellipse cx="12" cy="12" rx="4" ry="10" stroke="#44474e" stroke-width="1.8"/>
          <path d="M2 12h20" stroke="#44474e" stroke-width="1.8"/>
        </svg>
        <a
          :href="website"
          target="_blank"
          rel="noopener noreferrer"
          class="max-w-[220px] truncate text-[12px] font-medium text-blue-700 hover:underline"
        >{{ websiteDisplay }}</a>
      </div>
      <div v-if="phone" class="flex items-center gap-4">
        <svg class="shrink-0" width="18" height="18" viewBox="0 0 24 24" fill="none">
          <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 11.5 19.79 19.79 0 0 1 1.61 2.84 2 2 0 0 1 3.59 1h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.96a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 15.92z" stroke="#44474e" stroke-width="1.8"/>
        </svg>
        <span class="text-[12px] font-medium text-[#44474e]">{{ phone }}</span>
      </div>
    </div>

    <!-- Get Directions button -->
    <div class="px-8 pt-5">
      <a
        :href="mapsUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="flex w-full items-center justify-center gap-2 rounded-xl bg-black py-4 text-[15px] font-bold text-white transition hover:bg-neutral-900 active:scale-[0.98]"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
          <path d="M12 21C12 21 4 13.5 4 9a8 8 0 1 1 16 0c0 4.5-8 12-8 12z" stroke="white" stroke-width="2"/>
          <circle cx="12" cy="9" r="2.5" stroke="white" stroke-width="2"/>
        </svg>
        Get directions
      </a>
    </div>

    <!-- Divider -->
    <div class="mx-0 mt-5 h-px bg-gray-200" />

    <!-- Description -->
    <p v-if="description" class="px-8 py-4 text-[12px] font-medium leading-snug text-[#44474e]">{{ description }}</p>

    <!-- Hours -->
    <div v-if="hours" class="flex items-center gap-2 px-8 pb-7 text-[12px] font-medium text-[#45464d]" :class="{ 'pt-1': !description }">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.8"/>
        <path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
      <span>Open: {{ hours }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  name: string
  status: 'open' | 'closed' | 'unlisted'
  openUntil?: string
  address?: string
  phone?: string
  website?: string
  description?: string
  hours?: string
}>()

defineEmits<{ select: [] }>()

const statusLabel = computed(() => {
  if (props.status === 'open') return props.openUntil ? `Open until ${props.openUntil}` : 'Open now'
  if (props.status === 'closed') return 'Closed'
  return 'Hours not listed'
})

const badgeBg = computed(() => {
  if (props.status === 'open') return 'bg-[#f0fdf4]'
  if (props.status === 'closed') return 'bg-[#fff1f1]'
  return 'bg-[#f2f4f6]'
})

const badgeTextColor = computed(() => {
  if (props.status === 'open') return 'text-[#15803d]'
  if (props.status === 'closed') return 'text-[#f40e0e]'
  return 'text-[#45464d]'
})

const badgeBorderColor = computed(() => {
  if (props.status === 'open') return '#bbf7d0'
  if (props.status === 'closed') return '#fca5a5'
  return '#c4c6cf'
})

const dotBg = computed(() => {
  if (props.status === 'open') return 'bg-[#16a34a]'
  if (props.status === 'closed') return 'bg-[#f40e0e]'
  return 'bg-[#45464d]'
})

const websiteDisplay = computed(() =>
  props.website?.replace(/^https?:\/\/(www\.)?/, '') ?? ''
)

const mapsUrl = computed(() =>
  props.address ? `https://maps.google.com?q=${encodeURIComponent(props.address)}` : '#'
)
</script>
