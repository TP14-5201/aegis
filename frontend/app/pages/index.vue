<template>
  <div class="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4 text-center">
    <div class="max-w-2xl">
      <h1 class="text-5xl font-extrabold text-slate-800 mb-6 tracking-tight">
        Aegis
      </h1>
      <p class="text-lg text-slate-600 mb-10 leading-relaxed">
        Connecting you to the nearest local emergency relief services for food and shelter. Assisting in ensuring access to nutritious food for children.
      </p>
      <NuxtLink 
        to="/services" 
        class="inline-block bg-blue-600 text-white font-medium px-8 py-3 rounded-lg hover:bg-blue-700 hover:shadow-lg transition-all duration-200"
      >
        Find Emergency Services
      </NuxtLink>
    </div>
  </div>
</template>
