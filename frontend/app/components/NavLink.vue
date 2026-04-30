<template>
  <NuxtLink
    :to="to"
    class="nav-link relative inline-flex items-center font-roboto text-[18px] lg:text-[20px] font-medium leading-none whitespace-nowrap px-4 lg:px-6 py-2 transition-colors"
    :class="isActive ? 'text-sky-active' : 'text-black hover:text-sky-active'"
    @click="$emit('navigate')"
  >
    <slot />
    <!-- Underline for desktop only -->
    <span
      v-if="isActive"
      class="hidden lg:block absolute left-4 right-4 -bottom-[6px] h-1 bg-navy rounded-full"
    />
  </NuxtLink>
</template>

<script setup lang="ts">
const props = defineProps<{ to: string }>()
defineEmits<{ navigate: [] }>()

const route = useRoute()
const isActive = computed(() => route.path === props.to)
</script>
