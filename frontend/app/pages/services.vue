<template>
  <div class="min-h-screen bg-slate-50 p-6 lg:p-12">
    <div class="max-w-4xl mx-auto">
      <NuxtLink 
        to="/" 
        class="text-blue-600 hover:text-blue-800 font-medium mb-8 inline-flex items-center gap-2 transition-colors"
      >
        &larr; Back to Home
      </NuxtLink>
      
      <div class="mb-10">
        <h1 class="text-3xl lg:text-4xl font-bold text-slate-800 tracking-tight">Nearest Emergency Relief Services</h1>
        <p class="text-slate-500 mt-2 text-lg">Find localized support for food, shelter, and child nutrition.</p>
      </div>
      
      <div class="space-y-4">
        <!-- Placeholder Item 1 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6 hover:shadow-md transition-shadow">
          <div class="flex justify-between items-start">
            <div>
              <h2 class="text-xl font-semibold text-slate-800">Community Food Bank</h2>
              <p class="text-slate-600 mt-1">123 Safe Haven Road, Melbourne</p>
              <p class="text-sm text-slate-500 mt-2 bg-slate-100 inline-block px-3 py-1 rounded-full">Food parcels, child nutrition</p>
            </div>
            <div class="text-green-600 font-medium text-sm flex flex-col items-end">
              <span>Open Now</span>
              <span class="text-slate-500 font-normal">1.2 km away</span>
            </div>
          </div>
        </div>

        <!-- Placeholder Item 2 -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6 hover:shadow-md transition-shadow">
          <div class="flex justify-between items-start">
            <div>
              <h2 class="text-xl font-semibold text-slate-800">Hope Shelter</h2>
              <p class="text-slate-600 mt-1">45 Kindness Ave, Melbourne</p>
              <p class="text-sm text-slate-500 mt-2 bg-slate-100 inline-block px-3 py-1 rounded-full">Temporary shelter, warm meals</p>
            </div>
            <div class="text-green-600 font-medium text-sm flex flex-col items-end">
              <span>Open Now</span>
              <span class="text-slate-500 font-normal">3.5 km away</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
