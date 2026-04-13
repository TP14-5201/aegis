<template>
<div class="main-navigation-menu-wrapper-subsection">
  <!-- Logo -->
  <NuxtLink class="logo-3" to="/">
    <img
      class="OPEN-DOOR-VICTORIA-3"
      alt="Open DOOR VICTORIA"
      src="/images/open-door-victoria-1-4@2x.png"
    />
    <div class="logo-text-dir">
      <div class="logo-opendoor-dir">Open Door</div>
      <div class="logo-victoria-dir">VICTORIA</div>
    </div>
  </NuxtLink>

  <!-- Desktop / Tablet center nav -->
  <nav class="navigation-2 desktop-nav-dir">
    <NuxtLink class="link-3" to="/home-page">Home</NuxtLink>
    <NuxtLink class="dir-link" to="/directory">Directory</NuxtLink>
  </nav>

  <!-- Quick Exit + hamburger -->
  <div class="right-actions-dir">
    <button class="button-quick-exit-2" @click="quickExit">
      <img class="icon-2" alt="Icon" src="/images/icon-2.svg" />
      <span class="qe-text-dir">Quick Exit</span>
    </button>
    <button class="hamburger-dir" @click="menuOpen = !menuOpen" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>

  <!-- Mobile dropdown -->
  <div class="mobile-menu-dir" :class="{ open: menuOpen }">
    <NuxtLink class="mobile-link-dir" to="/home-page" @click="menuOpen = false">Home</NuxtLink>
    <NuxtLink class="mobile-link-dir" to="/directory" @click="menuOpen = false">Directory</NuxtLink>
  </div>
</div>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "NavbarDirectory",
  
  setup() {
    const menuOpen = ref(false);
    function quickExit() {
      window.location.replace("https://www.google.com");
    }
    return { menuOpen, quickExit };
  },
});
</script>

<style scoped>
.main-navigation-menu-wrapper-subsection {
  align-items: center;
  background-color: #1e3510;
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  padding: 10px 16px;
  position: relative;
  width: 100%;
  box-sizing: border-box;
  z-index: 100;
}

.logo-3 {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  flex: 1;
  min-width: 0;
  text-decoration: none;
}

.OPEN-DOOR-VICTORIA-3 {
  height: 66px;
  width: 56px;
  flex-shrink: 0;
}

.logo-text-dir {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.logo-opendoor-dir {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(18px, 2.5vw, 30px);
  font-weight: 700;
  white-space: nowrap;
}

.logo-victoria-dir {
  color: #ffb900;
  font-family: "Inter", Helvetica;
  font-size: clamp(12px, 1.6vw, 20px);
  font-weight: 700;
  letter-spacing: 1px;
  white-space: nowrap;
}

.desktop-nav-dir {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 2;
  justify-content: center;
}

.link-3,
.dir-link {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
}

.right-actions-dir {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

.button-quick-exit-2 {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: #e7000b;
  border: none;
  border-radius: 10px;
  box-shadow: 0px 4px 6px -4px #0000001a, 0px 10px 15px -3px #0000001a;
  cursor: pointer;
  height: 40px;
  padding: 0 12px;
  flex-shrink: 0;
  min-width: 0;
}

.icon-2 {
  height: 20px;
  width: 20px;
  flex-shrink: 0;
}

.qe-text-dir {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 500;
  white-space: nowrap;
}

.hamburger-dir {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 28px;
  height: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  flex-shrink: 0;
}

.hamburger-dir span {
  display: block;
  height: 3px;
  width: 100%;
  background: #ffffff;
  border-radius: 2px;
}

.mobile-menu-dir {
  display: none;
  width: 100%;
  flex-direction: column;
  gap: 12px;
  padding: 8px 0 4px;
  order: 99;
  flex-basis: 100%;
}

.mobile-menu-dir.open {
  display: flex;
}

.mobile-link-dir {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  padding: 6px 4px;
}

@media (max-width: 640px) {
  .main-navigation-menu-wrapper-subsection {
    flex-wrap: wrap;
  }
  .desktop-nav-dir {
    display: none;
  }
  .hamburger-dir {
    display: flex;
  }
  .logo-3 {
    flex: 1;
  }
  .right-actions-dir {
    margin-left: auto;
    flex-shrink: 0;
  }
  .OPEN-DOOR-VICTORIA-3 {
    height: 44px;
    width: 37px;
  }
  .logo-opendoor-dir {
    font-size: 16px;
  }
  .logo-victoria-dir {
    font-size: 11px;
  }
  .qe-text-dir {
    font-size: 13px;
  }
  .button-quick-exit-2 {
    padding: 0 8px;
    height: 34px;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .main-navigation-menu-wrapper-subsection {
    gap: 16px;
  }
}
</style>
