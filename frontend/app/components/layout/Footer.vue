<template>
  <footer class="w-full" style="background-color: #1e3510; font-family: 'Noto Serif', serif;">
    <div class="max-w-screen-xl mx-auto px-6 sm:px-10 py-16 flex flex-col sm:flex-row items-start justify-between gap-12">
      <!-- Left: Logo + tagline -->
      <div class="flex flex-col gap-5" style="max-width: 380px;">
        <NuxtLink to="/" class="flex items-center gap-3 cursor-pointer" style="text-decoration: none;">
          <div style="width: 46px; height: 56px; position: relative; overflow: hidden; flex-shrink: 0;">
            <img
              src="/images/logo.png"
              alt="Open Door Victoria"
              style="position: absolute; max-width: none; width: 283.99%; height: 240.96%; top: -48.28%; left: -92.05%; pointer-events: none;"
            />
          </div>
          <div style="display: flex; flex-direction: column; line-height: 1;">
            <span style="color: white; font-weight: 700; font-size: 26px;">Open Door</span>
            <span style="color: #ffb900; font-weight: 700; font-size: 17px; letter-spacing: 1px;">VICTORIA</span>
          </div>
        </NuxtLink>
        <p style="font-size: 14px; color: rgba(255,255,255,0.6); line-height: 1.75;">
          Providing dignified support for those who need it most. Our community is built on the belief that everyone deserves a seat at the table.
        </p>
      </div>

      <!-- Right: Links (static) -->
      <div class="flex gap-12 sm:gap-16">
        <div class="flex flex-col gap-4">
          <p style="font-size: 13px; font-weight: 700; color: white; letter-spacing: 1.4px; text-transform: uppercase;">Resources</p>
          <span class="footer-link" style="font-size: 15px; color: rgba(255,255,255,0.6); cursor: default;">Food Map</span>
          <span class="footer-link" style="font-size: 15px; color: rgba(255,255,255,0.6); cursor: default;">Shelter List</span>
        </div>
        <div class="flex flex-col gap-4">
          <p style="font-size: 13px; font-weight: 700; color: white; letter-spacing: 1.4px; text-transform: uppercase;">Connect</p>
          <span class="footer-link" style="font-size: 15px; color: rgba(255,255,255,0.6); cursor: default;">Contact Us</span>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div
      class="max-w-screen-xl mx-auto px-6 sm:px-10 py-6 flex flex-col sm:flex-row items-center justify-between gap-4"
      style="border-top: 1px solid rgba(255,255,255,0.1);"
    >
      <p style="font-size: 11px; color: rgba(255,255,255,0.4);">© 2026 Open Door Victoria. All rights reserved.</p>
      <div class="flex gap-6">
        <span style="font-size: 11px; color: rgba(255,255,255,0.4); cursor: default;">Privacy Policy</span>
        <span style="font-size: 11px; color: rgba(255,255,255,0.4); cursor: default;">Terms of Service</span>
      </div>
    </div>
  </footer>
</template>
