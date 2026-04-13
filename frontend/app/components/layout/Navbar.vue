<template>
<div class="main-navigation-menu-subsection">
  <!-- Logo -->
  <div class="logo">
    <img
      class="OPEN-DOOR-VICTORIA"
      alt="Open DOOR VICTORIA"
      src="/images/open-door-victoria-1-4@2x.png"
    />
    <div class="logo-text">
      <div class="logo-opendoor">Open Door</div>
      <div class="logo-victoria">VICTORIA</div>
    </div>
  </div>

  <!-- Desktop / Tablet center nav -->
  <nav class="navigation desktop-nav">
    <NuxtLink class="nav-link" to="/home-page">Home</NuxtLink>
    <NuxtLink class="nav-link" to="/directory">Directory</NuxtLink>
  </nav>

  <!-- Quick Exit + hamburger row -->
  <div class="right-actions">
    <button class="button-quick-exit" @click="quickExit">
      <img class="icon" alt="Icon" src="/images/icon-2.svg" />
      <span class="qe-text">Quick Exit</span>
    </button>

    <!-- Hamburger (mobile only) -->
    <button class="hamburger" @click="menuOpen = !menuOpen" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>

  <!-- Mobile dropdown -->
  <div class="mobile-menu" :class="{ open: menuOpen }">
    <NuxtLink class="mobile-link" to="/home-page" @click="menuOpen = false">Home</NuxtLink>
    <NuxtLink class="mobile-link" to="/directory" @click="menuOpen = false">Directory</NuxtLink>
  </div>
</div>
</template>

<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "Navbar",
  
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
/* ── Base (all sizes) ─────────────────────────────────── */
.main-navigation-menu-subsection {
  align-items: center;
  background-color: #1e35104c;
  border-radius: 10px;
  display: flex;
  flex-wrap: nowrap;
  gap: 8px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 16px;
  position: absolute;
  top: 22px;
  width: min(1054px, calc(100% - 32px));
  box-sizing: border-box;
  z-index: 100;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
  flex: 1;
  min-width: 0;
  position: relative;
}

.OPEN-DOOR-VICTORIA {
  height: 66px;
  width: 56px;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.logo-opendoor {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(18px, 2.5vw, 30px);
  font-weight: 700;
  white-space: nowrap;
}

.logo-victoria {
  color: #ffb900;
  font-family: "Inter", Helvetica;
  font-size: clamp(12px, 1.6vw, 20px);
  font-weight: 700;
  letter-spacing: 1px;
  white-space: nowrap;
}

/* Center nav (tablet + desktop) */
.desktop-nav {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 2;
  justify-content: center;
}

.nav-link {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
}

/* Right side */
.right-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}

/* Quick Exit */
.button-quick-exit {
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

.button-quick-exit .icon {
  height: 20px;
  width: 20px;
  flex-shrink: 0;
}

.qe-text {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 500;
  white-space: nowrap;
}

/* Hamburger (hidden on tablet+) */
.hamburger {
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

.hamburger span {
  display: block;
  height: 3px;
  width: 100%;
  background: #ffffff;
  border-radius: 2px;
}

/* Mobile dropdown */
.mobile-menu {
  display: none;
  width: 100%;
  flex-direction: column;
  gap: 12px;
  padding: 8px 0 4px;
  /* break out of the nowrap row onto its own line */
  order: 99;
  flex-basis: 100%;
}

.mobile-menu.open {
  display: flex;
}

.mobile-link {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  padding: 6px 4px;
}

/* ── Mobile  (≤ 640px) ────────────────────────────────── */
@media (max-width: 640px) {
  .main-navigation-menu-subsection {
    /* keep everything on one row even on tiny screens */
    flex-wrap: wrap;
  }

  .desktop-nav {
    display: none;
  }

  .hamburger {
    display: flex;
  }

  .logo {
    flex: 1;
  }

  .OPEN-DOOR-VICTORIA {
    height: 44px;
    width: 37px;
  }

  .logo-opendoor {
    font-size: 16px;
  }

  .logo-victoria {
    font-size: 11px;
  }

  .qe-text {
    font-size: 13px;
  }

  .button-quick-exit {
    padding: 0 8px;
    height: 34px;
  }

  .right-actions {
    margin-left: auto;
    flex-shrink: 0;
  }
}

/* ── Tablet (641 – 1024px) ───────────────────────────── */
@media (min-width: 641px) and (max-width: 1024px) {
  .main-navigation-menu-subsection {
    gap: 16px;
  }
}
</style>
