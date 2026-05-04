<template>
    <TopNavigation />    
    <section class="w-full bg-sky-tint py-16 lg:py-24">
    <div class="max-w-5xl mx-auto px-5 lg:px-12 text-center">


        <!-- Subheading -->
        <p class="mt-4 font-roboto font-bold text-coral text-[18px] lg:text-[22px]">
        This page is currently under development
        </p>

        <!-- Body -->
        <p class="mt-6 font-roboto text-[16px] lg:text-[18px] text-ash leading-relaxed max-w-2xl mx-auto">
        We are working on sharing more about our mission, our team, and how ChereBowl supports
        families facing food insecurity across Victoria. 
        <br class="hidden lg:block" />
        Thank you for your patience while we continue to improve this experience.
        </p>

        <!-- Optional CTA (keeps consistency with rest of site) -->
        <NuxtLink
        to="/"
        class="group mt-10 inline-flex items-center justify-center gap-3
                bg-sky rounded-[20px]
                h-[52px] lg:h-[60px] px-6 lg:px-8
                font-roboto font-bold text-navy-deep
                text-[16px] lg:text-[18px]
                shadow-[0_12px_28px_rgba(68,154,196,0.22)]
                transition-transform duration-300 ease-out
                hover:-translate-y-1"
        >
        Back to Home
        <span class="transition-transform duration-300 group-hover:translate-x-1">
        </span>
        </NuxtLink>

    </div>
    </section>
</template>