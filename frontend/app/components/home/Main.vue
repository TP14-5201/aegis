<template>
<div class="main-subsection">
<div class="main-navigation-menu">
  <!-- Logo -->
  <router-link class="logo-4" to="/landing-page">
    <img
      class="OPEN-DOOR-VICTORIA-4"
      alt="Open DOOR VICTORIA"
      src="/images/open-door-victoria-1-4@2x.png"
    />
    <div class="logo-text-hp">
      <div class="logo-opendoor-hp">Open Door</div>
      <div class="logo-victoria-hp">VICTORIA</div>
    </div>
  </router-link>

  <!-- Desktop / Tablet center nav -->
  <nav class="navigation-3 desktop-nav-hp">
    <router-link class="hp-nav-link" to="/home-page">Home</router-link>
    <router-link class="hp-nav-link" to="/directory">Directory</router-link>
  </nav>

  <!-- Quick Exit + hamburger -->
  <div class="right-actions-hp">
    <button class="button-quick-exit-3" @click="quickExit">
      <img class="icon-3" alt="Icon" src="/images/icon-2.svg" />
      <span class="qe-text-hp">Quick Exit</span>
    </button>
    <button class="hamburger-hp" @click="menuOpen = !menuOpen" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>

  <!-- Mobile dropdown -->
  <div class="mobile-menu-hp" :class="{ open: menuOpen }">
    <router-link class="mobile-link-hp" to="/home-page" @click="menuOpen = false">Home</router-link>
    <router-link class="mobile-link-hp" to="/directory" @click="menuOpen = false">Directory</router-link>
  </div>
</div>
<div class="hero-section">
<img
        class="istock"
        alt="Istock"
        src="/images/istock-1482584637-1.png"
      />
<div class="gradient" />
<div class="container-35">
<div class="div-wrapper-4">
<p class="you-belong-here">
<span class="span">You Belong </span>
<span class="text-wrapper-49">Here.</span>
</p>
</div>
<div class="our-doors-are-always-wrapper">
<p class="our-doors-are-always">
Our doors are always open. No shame, no judgment – this is
            <br />
your right. Choose the support you need below.
          </p>
</div>
<div class="background-6">
<div class="overlay-shadow" />
<div class="container-36">
<img
              class="container-37"
              alt="Container"
              src="/images/container-11.svg"
            />
<div class="container-wrapper">
<input
                class="search-for-food"
                placeholder="Search for food & shelter"
                type="text"
              />
</div>
</div>
<router-link to="/directory">
<button class="find-resources-wrapper">
<div class="find-resources">
Find
                <br />
Resources
              </div>
</button>
</router-link>
</div>
</div>
</div>
<div class="container-38">
<div class="heading-6">
<div class="text-wrapper-50">Discover Local Resources</div>
</div>
<div class="search-our-wrapper">
<p class="search-our">
Search our comprehensive directory of food banks and emergency
          shelters.
          <br />
Whatever you&#39;re looking for, we&#39;re here to help you find it.
        </p>
</div>
<div class="container-39" />
</div>
<div class="section-primary">
<div class="locate-food-bank">
<div class="container-40">
<div class="abaxucwswhbwi">
<img
              class="istock-2"
              alt="Istock"
              src="/images/istock-1440772090-1.png"
            />
</div>
<div class="gradient-2" />
</div>
<div class="container-41">
<div class="div-wrapper-4">
<div class="text-wrapper-51">FOOD RELIEF</div>
</div>
<div class="div-wrapper-4">
<div class="text-wrapper-52">Locate a Food Bank</div>
</div>
<div class="container-42">
<p class="text-wrapper-53">
Access free groceries and ready-to-eat meals across Victoria.
            </p>
</div>
<router-link class="link-5" to="/directory">
<div class="text-wrapper-54">Find Nearby Food</div>
<img
              class="container-37"
              alt="Container"
              src="/images/container-12.svg"
            />
</router-link>
</div>
</div>
<div class="find-a-shelter">
<div class="frame">
<img
            class="istock-3"
            alt="Istock"
            src="/images/istock-1129739496-1.png"
          />
<div class="gradient-3" />
</div>
<div class="container-43">
<div class="div-wrapper-4">
<div class="text-wrapper-51">HOUSING RELIEF</div>
</div>
<div class="div-wrapper-4">
<div class="text-wrapper-55">Locate a Housing Service</div>
</div>
<div class="container-42">
<p class="text-wrapper-53">
Find emergency and transitional housing options in Victoria.
            </p>
</div>
<router-link class="link-6" to="/directory">
<div class="text-wrapper-56">Check Availability</div>
<div class="image-wrapper">
<img
                class="image-4"
                alt="Image"
                src="/images/image-4-2@2x.png"
              />
</div>
</router-link>
</div>
</div>
</div>
<div class="community-sanctuary">
<div class="container-44">
<div class="abaxudlbodqnbg" />
<div class="img-margin">
<div class="div-5" />
</div>
</div>
<div class="container-45">
<div class="overlay-blur" />
<div class="container-46">
<div class="background-7" />
<div class="div-wrapper-5">
<p class="true-resilience-is">
&#34;True resilience is built
              <br />
through dignity. We
              <br />
don&#39;t just provide
              <br />
shelter; we offer a<br />
foundation for the
              <br />
human spirit to flourish
              <br />
once again.&#34;
            </p>
</div>
</div>
<div class="container-47">
<div class="div-wrapper-4">
<div class="text-wrapper-57">Elizabeth Montgomery</div>
</div>
<div class="div-wrapper-4">
<p class="text-wrapper-58">
Director of Community Resilience, Victoria
            </p>
</div>
</div>
</div>
</div>
<div class="latest-stories">
<div class="container-48">
<div class="container-49">
<div class="div-wrapper-4">
<div class="voices-of-victoria">VOICES OF VICTORIA</div>
</div>
<div class="div-wrapper-4">
<div class="text-wrapper-59">Read Our Latest Stories</div>
</div>
</div>
<div class="link-7">
<div class="text-wrapper-60">Read All</div>
</div>
</div>
<div class="container-50">
<div class="featured-story-left">
<div class="margin">
<div class="container-51">
<div class="div-6" />
</div>
</div>
<div class="container-52">
<div class="div-wrapper-4">
<div class="building-bridges">
Building Bridges through Shared
                <br />
Traditions
              </div>
</div>
<div class="div-wrapper-4">
<p class="our-community">
Our community thrives when we embrace the diverse traditions that
                <br />
make Victoria unique. From seasonal festivals to daily
                <br />
gatherings, we find strength in our shared humanity and the
                commitment to support
                <br />
one another.
              </p>
</div>
<div class="link-8">
<div class="text-13">Learn More</div>
<img
                class="container-37"
                alt="Container"
                src="/images/container-13.svg"
              />
</div>
</div>
</div>
<div class="side-stories-right">
<div class="story-card">
<div class="container-53">
<div class="div-7" />
</div>
<div class="container-54">
<div class="container-55">
<p class="text-14">
The Empowerment Initiative aims to build a strong
                  <br />
community through specialized skills training,
                  <br />
emphasizing the significant role of digital literacy in
                  <br />
modern resilience.
                </p>
</div>
<div class="link-9">
<div class="text-15">Learn More</div>
<img
                  class="container-37"
                  alt="Container"
                  src="/images/container-15.svg"
                />
</div>
</div>
</div>
<div class="story-card">
<div class="container-53">
<div class="div-8" />
</div>
<div class="container-54">
<div class="container-55">
<p class="text-16">
Ensuring every child in Victoria has access to
                  <br />
nutrition and a stable environment is our priority.
                  <br />
Together, we are shaping a brighter future for the
                  <br />
next generation.
                </p>
</div>
<div class="link-9">
<div class="text-15">Learn More</div>
<img
                  class="container-37"
                  alt="Container"
                  src="/images/container-15.svg"
                />
</div>
</div>
</div>
</div>
</div>
</div>
<div class="FAQ-section">
<div class="container-56">
<div class="heading-wrapper">
<div class="div-wrapper-4">
<div class="text-wrapper-61">FAQS</div>
</div>
</div>
<div class="container-57">
<div class="button-FAQ-item">
<div class="div-wrapper-5">
<div class="text-17">How can I help?</div>
</div>
<img
              class="container-37"
              alt="Container"
              src="/images/container-19.svg"
            />
</div>
<div class="button-FAQ-item">
<div class="div-wrapper-5">
<p class="text-18">What will Open Door Victoria focus on?</p>
</div>
<img
              class="container-37"
              alt="Container"
              src="/images/container-19.svg"
            />
</div>
<div class="button-FAQ-item">
<div class="div-wrapper-5">
<div class="text-19">What is the Vision?</div>
</div>
<img
              class="container-37"
              alt="Container"
              src="/images/container-19.svg"
            />
</div>
<div class="button-FAQ-item">
<div class="div-wrapper-5">
<p class="text-20">
What is the Mission of Open Door Victoria?
              </p>
</div>
<img
              class="container-37"
              alt="Container"
              src="/images/container-19.svg"
            />
</div>
</div>
</div>
</div>
</div>
</template>
<script>
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "Main",
  props: {},
  setup() {
    const menuOpen = ref(false);
    function quickExit() {
      window.location.replace("https://www.google.com");
    }
    return { menuOpen, quickExit };
  },
});
</script>
<style>
.main-subsection {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 0px 0px 96px;
  position: relative;
  width: 100%;
}

.main-subsection .main-navigation-menu {
  align-items: center;
  background-color: #1e3510;
  display: flex;
  flex-wrap: nowrap;
  flex: 0 0 auto;
  gap: 8px;
  padding: 10px 16px;
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

.main-subsection .logo-4 {
  align-items: center;
  display: inline-flex;
  flex: 1;
  flex-shrink: 0;
  min-width: 0;
  gap: 10px;
  position: relative;
  text-decoration: none;
}

.main-subsection .OPEN-DOOR-VICTORIA-4 {
  aspect-ratio: 0.85;
  display: block;
  height: 66px;
  position: relative;
  width: 56px;
  flex-shrink: 0;
}

.main-subsection .text-11 {
  align-items: flex-start;
  display: flex;
  height: 28px;
  left: 60px;
  position: absolute;
  top: 38px;
  width: 155px;
}

.main-subsection .text-wrapper-44 {
  color: #ffb900;
  flex: 1;
  font-family: "Inter", Helvetica;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 1px;
  line-height: 28px;
  margin-top: -1px;
  position: relative;
}

.main-subsection .text-12 {
  height: 38px;
  left: 60px;
  position: absolute;
  top: 0;
  width: 155px;
}

.main-subsection .text-wrapper-45 {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 30px;
  font-weight: 700;
  left: 0;
  letter-spacing: 0;
  line-height: 37.5px;
  position: absolute;
  top: -3px;
  white-space: nowrap;
}

.main-subsection .navigation-3 {
  align-items: center;
  display: flex;
  gap: 24px;
  position: relative;
  flex: 1;
  justify-content: center;
}

.main-subsection .link-4 {
  height: 24px;
  position: relative;
  width: 44px;
}

.main-subsection .text-wrapper-46 {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  left: 0;
  letter-spacing: 0;
  line-height: 24px;
  position: absolute;
  top: -2px;
  white-space: nowrap;
}

.main-subsection .button-10 {
  all: unset;
  box-sizing: border-box;
  flex: 1;
  flex-grow: 1;
  height: 24px;
  position: relative;
}

.main-subsection .text-wrapper-47 {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  left: -6px;
  letter-spacing: 0;
  line-height: 24px;
  position: absolute;
  text-align: center;
  top: -2px;
  white-space: nowrap;
}

/* nav responsive helpers */
.main-subsection .logo-text-hp {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}
.main-subsection .logo-opendoor-hp {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: clamp(18px, 2.5vw, 30px);
  font-weight: 700;
  white-space: nowrap;
}
.main-subsection .logo-victoria-hp {
  color: #ffb900;
  font-family: "Inter", Helvetica;
  font-size: clamp(12px, 1.6vw, 20px);
  font-weight: 700;
  letter-spacing: 1px;
  white-space: nowrap;
}
.main-subsection .desktop-nav-hp {
  display: flex;
  align-items: center;
  gap: 24px;
  flex: 2;
  justify-content: center;
}
.main-subsection .hp-nav-link {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
}
.main-subsection .right-actions-hp {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  margin-left: auto;
}
.main-subsection .button-quick-exit-3 {
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
}
.main-subsection .icon-3 {
  height: 20px;
  width: 20px;
  flex-shrink: 0;
}
.main-subsection .qe-text-hp {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 500;
  white-space: nowrap;
}
.main-subsection .hamburger-hp {
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
.main-subsection .hamburger-hp span {
  display: block;
  height: 3px;
  width: 100%;
  background: #ffffff;
  border-radius: 2px;
}
.main-subsection .mobile-menu-hp {
  display: none;
  width: 100%;
  flex-direction: column;
  gap: 12px;
  padding: 8px 0 4px;
  order: 99;
  flex-basis: 100%;
}
.main-subsection .mobile-menu-hp.open {
  display: flex;
}
.main-subsection .mobile-link-hp {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 500;
  text-decoration: none;
  padding: 6px 4px;
}

.main-subsection .hero-section {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  justify-content: flex-start;
  min-height: 520px;
  padding: 140px 24px 60px;
  position: relative;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.main-subsection .istock {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 520px;
}

.main-subsection .gradient {
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(150, 144, 144, 0.6) 100%
  );
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .container-35 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 896px;
  padding: 0 0 0 clamp(0px, 4vw, 80px);
  position: relative;
  z-index: 1;
  width: 100%;
}

.main-subsection .div-wrapper-4 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
  width: 100%;
}

.main-subsection .you-belong-here {
  align-items: center;
  align-self: stretch;
  color: transparent;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 700;
  line-height: 1.1;
  margin-top: -1px;
  position: relative;
  flex-wrap: wrap;
}

.main-subsection .span {
  color: #ffffff;
  letter-spacing: -1.3px;
}

.main-subsection .text-wrapper-49 {
  color: #ffb900;
  letter-spacing: 0;
}

.main-subsection .our-doors-are-always-wrapper {
  align-items: flex-start;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  max-width: 576px;
  padding: 0px 0px 16px;
  position: relative;
  width: 100%;
}

.main-subsection .our-doors-are-always {
  color: #ffffffcc;
  font-family: "Inter", Helvetica;
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 400;
  letter-spacing: 0;
  line-height: 1.5;
  margin-top: -1px;
  position: relative;
  width: 100%;
}

.main-subsection .background-6 {
  align-items: center;
  background-color: #ffffff;
  border-radius: 10px;
  display: flex;
  flex: 0 0 auto;
  gap: 8px;
  max-width: 672px;
  padding: 8px;
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

.main-subsection .overlay-shadow {
  background-color: #ffffff01;
  border-radius: 4px;
  box-shadow: 0px 8px 10px -6px #0000001a, 0px 20px 25px -5px #0000001a;
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .container-36 {
  align-items: center;
  display: flex;
  flex: 1;
  flex-grow: 1;
  gap: 1.07e-14px;
  padding: 0px 16px;
  position: relative;
}

.main-subsection .container-37 {
  flex: 0 0 auto;
  position: relative;
}

.main-subsection .container-wrapper {
  align-items: flex-start;
  display: flex;
  flex: 1;
  flex-direction: column;
  flex-grow: 1;
  padding: 18px 12px;
  position: relative;
}

.main-subsection .search-for-food {
  align-self: stretch;
  background: none;
  border: none;
  color: #6b7280;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: normal;
  margin-top: -1px;
  padding: 0;
  position: relative;
  width: 100%;
}

.main-subsection .find-resources-wrapper {
  all: unset;
  align-items: center;
  background-color: #4a7c2b;
  border-radius: 10px;
  box-sizing: border-box;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  justify-content: center;
  padding: 16px 35.2px 16px 35.19px;
  position: relative;
}

.main-subsection .find-resources {
  color: #ffffff;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 700;
  height: 48px;
  letter-spacing: 0.4px;
  line-height: 24px;
  margin-top: -1px;
  position: relative;
  text-align: center;
  width: 86.22px;
}

.main-subsection .container-38 {
  align-items: center;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 768px;
  position: relative;
  padding: 32px 24px 0;
  box-sizing: border-box;
}

.main-subsection .heading-6 {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
  width: 100%;
}

.main-subsection .text-wrapper-50 {
  align-items: center;
  color: #000000;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(28px, 4vw, 48px);
  font-weight: 700;
  justify-content: center;
  letter-spacing: 0;
  line-height: 1.1;
  margin-top: -1px;
  position: relative;
  text-align: center;
  width: fit-content;
}

.main-subsection .search-our-wrapper {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 12px 0px 0px;
  position: relative;
  width: 100%;
}

.main-subsection .search-our {
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 26px;
  margin-top: -1px;
  position: relative;
  text-align: center;
  width: fit-content;
}

.main-subsection .container-39 {
  height: 16px;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .section-primary {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(2, 1fr);
  padding: 20px 24px 0;
  width: 100%;
  max-width: 1280px;
  box-sizing: border-box;
}

.main-subsection .locate-food-bank {
  background-color: #ffffff;
  border-radius: 10px;
  min-height: 420px;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.main-subsection .container-40 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .abaxucwswhbwi {
  align-self: stretch;
  background-image: url(/images/ab6axucws3whbwi-yauiwh4-p1bki3d0xydsoqf6rknpcqbswzdcpxmxeckgtfrp.png);
  background-position: 50% 50%;
  background-size: cover;
  flex: 1;
  flex-grow: 1;
  opacity: 0.8;
  position: relative;
  width: 100%;
}

.main-subsection .istock-2 {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 420px;
}

.main-subsection .gradient-2 {
  background: linear-gradient(
    0deg,
    rgba(4, 22, 39, 0.9) 0%,
    rgba(4, 22, 39, 0.2) 50%,
    rgba(4, 22, 39, 0) 100%
  );
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .container-41 {
  align-items: flex-start;
  bottom: 0;
  display: inline-flex;
  flex-direction: column;
  gap: 8px;
  left: 0;
  padding: 40px;
  position: absolute;
}

.main-subsection .text-wrapper-51 {
  align-items: center;
  align-self: stretch;
  color: #ffb900;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 700;
  height: 16px;
  letter-spacing: 1.2px;
  line-height: 16px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
}

.main-subsection .text-wrapper-52 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(22px, 3vw, 36px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.2;
  margin-top: -1px;
  position: relative;
  width: 100%;
  flex-wrap: wrap;
}

.main-subsection .container-42 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  height: 67px;
  max-width: 448px;
  padding: 8px 0px 16px;
  position: relative;
  width: 100%;
}

.main-subsection .text-wrapper-53 {
  color: #ffffffb2;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 400;
  height: 48px;
  letter-spacing: 0;
  line-height: 24px;
  margin-bottom: -4px;
  margin-top: -1px;
  position: relative;
  width: 412.78px;
}

.main-subsection .link-5 {
  align-items: center;
  background-color: #4a7c2b;
  border-radius: 10px;
  display: flex;
  flex: 0 0 auto;
  gap: 8px;
  padding: 12px 24px;
  position: relative;
  width: 240px;
}

.main-subsection .text-wrapper-54 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 700;
  height: 24px;
  letter-spacing: 0;
  line-height: 24px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 168px;
}

.main-subsection .find-a-shelter {
  background-color: #041627;
  border-radius: 10px;
  min-height: 420px;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.main-subsection .frame {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 420px;
}

.main-subsection .istock-3 {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  min-height: 420px;
}

.main-subsection .gradient-3 {
  background: linear-gradient(
    90deg,
    rgba(0, 0, 0, 0.8) 0%,
    rgba(139, 139, 139, 0.8) 100%
  );
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
}

.main-subsection .container-43 {
  align-items: flex-start;
  bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  left: 0;
  padding: 40px;
  position: absolute;
  width: 513px;
}

.main-subsection .text-wrapper-55 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(22px, 3vw, 36px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.2;
  margin-top: -1px;
  position: relative;
  width: 100%;
  flex-wrap: wrap;
}

.main-subsection .link-6 {
  align-items: center;
  border: 3px solid;
  border-color: #4a7c2b;
  border-radius: 10px;
  display: flex;
  flex: 0 0 auto;
  gap: 8px;
  padding: 12px 24px;
  position: relative;
  width: 240px;
}

.main-subsection .text-wrapper-56 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 700;
  height: 24px;
  letter-spacing: 0;
  line-height: 24px;
  margin-top: -3px;
  position: relative;
  white-space: nowrap;
  width: 168px;
}

.main-subsection .image-wrapper {
  align-items: flex-start;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  margin-right: -2px;
  position: relative;
}

.main-subsection .image-4 {
  aspect-ratio: 1;
  height: 18px;
  position: relative;
  width: 18px;
}

.main-subsection .community-sanctuary {
  display: grid;
  gap: 40px;
  grid-template-columns: repeat(2, 1fr);
  height: fit-content;
  padding: 40px 24px 32px;
  width: 100%;
  box-sizing: border-box;
}

.main-subsection .container-44 {
  align-self: center;
  display: grid;
  gap: 16px;
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: 421.33px;
  height: fit-content;
  position: relative;
  width: 100%;
}

.main-subsection .abaxudlbodqnbg {
  background-image: url(/images/ab6axudlbodq8nbg2-wnptgnmhyyrukf8o2jx2do5tfvx1asfrnh0xbvyficcgjk@2x.png);
  background-position: 50% 50%;
  background-size: cover;
  border-radius: 4px;
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  height: 100%;
  position: relative;
  width: 100%;
}

.main-subsection .img-margin {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  height: 100%;
  padding: 48px 0px 0px;
  position: relative;
  width: 100%;
}

.main-subsection .div-5 {
  align-self: stretch;
  aspect-ratio: 0.75;
  background-image: url(/images/ab6axud4g8sgsuabed9zc0h-1hcscrcny4-mxd7yoghn1qmdfch0jfxlvvqkkmqt@2x.png);
  background-position: 50% 50%;
  background-size: cover;
  border-radius: 4px;
  margin-bottom: -0.01px;
  position: relative;
  width: 100%;
}

.main-subsection .container-45 {
  align-items: flex-end;
  align-self: center;
  display: flex;
  flex-direction: column;
  gap: 32px;
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  height: fit-content;
  position: relative;
  width: 100%;
}

.main-subsection .overlay-blur {
  background-color: #fed48833;
  border-radius: 12px;
  filter: blur(32px);
  height: 160px;
  left: -40px;
  position: absolute;
  top: -40px;
  width: 160px;
}

.main-subsection .container-46 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  gap: 24px;
  position: relative;
  width: 100%;
}

.main-subsection .background-7 {
  background-color: #ffb900;
  height: 192px;
  position: relative;
  width: 4px;
}

.main-subsection .div-wrapper-5 {
  align-items: flex-start;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
}

.main-subsection .true-resilience-is {
  color: #000000;
  font-family: "Inter", Helvetica;
  font-size: clamp(20px, 3.5vw, 48px);
  font-weight: 400;
  letter-spacing: 0;
  line-height: 1.3;
  margin-top: -1px;
  position: relative;
  width: 100%;
}

.main-subsection .container-47 {
  align-items: flex-start;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  position: relative;
  width: 100%;
}

.main-subsection .text-wrapper-57 {
  align-items: center;
  align-self: stretch;
  color: #000000;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 28px;
  margin-top: -1px;
  position: relative;
}

.main-subsection .text-wrapper-58 {
  align-items: center;
  align-self: stretch;
  color: #44474c;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 24px;
  margin-top: -1px;
  position: relative;
}

.main-subsection .latest-stories {
  align-items: flex-start;
  border-color: #0416271a;
  border-top-style: solid;
  border-top-width: 1px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 48px;
  max-width: 1536px;
  padding: 47px 24px 0px;
  position: relative;
  width: 100%;
}

.main-subsection .container-48 {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  justify-content: space-between;
  position: relative;
  width: 100%;
}

.main-subsection .container-49 {
  align-items: flex-start;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 12px;
  position: relative;
}

.main-subsection .voices-of-victoria {
  align-items: center;
  color: #ffb900;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 12px;
  font-weight: 700;
  height: 16px;
  letter-spacing: 1.2px;
  line-height: 16px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 146.98px;
}

.main-subsection .text-wrapper-59 {
  align-items: center;
  color: #000000;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 48px;
  font-weight: 700;
  height: 48px;
  letter-spacing: 0;
  line-height: 48px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 572.8px;
}

.main-subsection .link-7 {
  align-items: flex-start;
  background-color: #4a7c2b;
  border-radius: 12px;
  display: inline-flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 14px 32px;
  position: relative;
}

.main-subsection .text-wrapper-60 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 700;
  height: 20px;
  letter-spacing: 0;
  line-height: 20px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 55.81px;
}

.main-subsection .container-50 {
  display: grid;
  gap: 32px;
  grid-template-columns: repeat(2, 1fr);
  height: fit-content;
  width: 100%;
}

.main-subsection .featured-story-left {
  align-items: flex-start;
  background-color: #efedef80;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  height: fit-content;
  padding: 32px;
  position: relative;
  width: 100%;
}

.main-subsection .margin {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  padding: 0px 0px 32px;
  position: relative;
  width: 100%;
}

.main-subsection .container-51 {
  align-items: flex-start;
  align-self: stretch;
  border-radius: 8px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.main-subsection .div-6 {
  align-self: stretch;
  background-image: url(/images/ab6axuawhzh8zgq3u9vliwla7-rbxxnxo6pg-ltwdvlmnclgy3dihi9s6wa0xf6-.png);
  background-position: 50% 50%;
  background-size: cover;
  height: 400px;
  position: relative;
  width: 100%;
}

.main-subsection .container-52 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  gap: 16px;
  position: relative;
  width: 100%;
}

.main-subsection .building-bridges {
  align-self: stretch;
  color: #000000;
  font-family: "Inter", Helvetica;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 36px;
  margin-top: -1px;
  position: relative;
}

.main-subsection .our-community {
  align-self: stretch;
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 26px;
  margin-top: -1px;
  position: relative;
}

.main-subsection .link-8 {
  align-items: center;
  display: inline-flex;
  flex: 0 0 auto;
  gap: 4px;
  padding: 8px 0px 0px;
  position: relative;
}

.main-subsection .text-13 {
  align-items: center;
  color: #1e3510;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 16px;
  font-weight: 700;
  height: 24px;
  letter-spacing: 0;
  line-height: 24px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 88.78px;
}

.main-subsection .side-stories-right {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 32px;
  grid-column: 2 / 3;
  grid-row: 1 / 2;
  height: fit-content;
  padding: 0px 0px 224px;
  position: relative;
  width: 100%;
}

.main-subsection .story-card {
  align-items: flex-start;
  align-self: stretch;
  background-color: #efedef80;
  border-radius: 16px;
  display: flex;
  flex: 0 0 auto;
  gap: 24px;
  padding: 24px;
  position: relative;
  width: 100%;
}

.main-subsection .container-53 {
  align-items: flex-start;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  width: 140px;
  flex-shrink: 0;
}

.main-subsection .div-7 {
  align-self: stretch;
  background-image: url(/images/ab6axub8sipb0uxgszdegoxxkpy-y34qw1dde5fbeum6v3jr0widahqd72ym6zy9@2x.png);
  background-position: 50% 50%;
  background-size: cover;
  height: 192px;
  position: relative;
  width: 100%;
}

.main-subsection .container-54 {
  position: relative;
  flex: 1;
  min-width: 0;
}

.main-subsection .container-55 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  padding: 0px 0px 8px;
  width: 100%;
}

.main-subsection .text-14 {
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 22.8px;
  margin-top: -1px;
  position: relative;
  width: 100%;
}

.main-subsection .link-9 {
  align-items: center;
  display: inline-flex;
  gap: 4px;
  padding-top: 8px;
}

.main-subsection .text-15 {
  align-items: center;
  color: #1e3510;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 700;
  height: 20px;
  letter-spacing: 0;
  line-height: 20px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  width: 77.69px;
}

.main-subsection .div-8 {
  align-self: stretch;
  background-image: url(/images/ab6axuamhhc0ixwwnaehuewxeydhxsba6uw062oc4rg1m3z3ywwyyg-5ohbmcohi@2x.png);
  background-position: 50% 50%;
  background-size: cover;
  height: 192px;
  position: relative;
  width: 100%;
}

.main-subsection .text-16 {
  color: #44474c;
  font-family: "Inter", Helvetica;
  font-size: 14px;
  font-weight: 400;
  letter-spacing: 0;
  line-height: 22.8px;
  margin-top: -1px;
  position: relative;
  width: 100%;
}

.main-subsection .FAQ-section {
  align-items: flex-start;
  border-color: #0416271a;
  border-top-style: solid;
  border-top-width: 1px;
  display: flex;
  flex: 0 0 auto;
  flex-direction: column;
  max-width: 1536px;
  padding: 96px 24px;
  position: relative;
  width: 100%;
}

.main-subsection .container-56 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex-wrap: wrap;
  flex: 0 0 auto;
  gap: 48px;
  position: relative;
  width: 100%;
}

.main-subsection .heading-wrapper {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  position: relative;
  width: clamp(160px, 30%, 380px);
  flex-shrink: 0;
}

.main-subsection .text-wrapper-61 {
  align-items: center;
  align-self: stretch;
  color: #000000;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 1;
  margin-top: -1px;
  position: relative;
}

.main-subsection .container-57 {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
  flex: 1;
  min-width: 280px;
}

.main-subsection .button-FAQ-item {
  align-items: center;
  align-self: stretch;
  background-color: #4a7c2b;
  border-radius: 4px;
  display: flex;
  flex: 0 0 auto;
  justify-content: space-between;
  padding: 24px;
  position: relative;
  width: 100%;
}

.main-subsection .text-17,
.main-subsection .text-18,
.main-subsection .text-19,
.main-subsection .text-20 {
  align-items: center;
  color: #ffffff;
  display: flex;
  font-family: "Inter", Helvetica;
  font-size: clamp(15px, 1.8vw, 20px);
  font-weight: 700;
  letter-spacing: 0;
  line-height: 1.4;
  margin-top: -1px;
  position: relative;
  width: 100%;
  flex-wrap: wrap;
}

/* ── Responsive breakpoints ────────────────── */
@media (max-width: 1024px) {
  .main-subsection .section-primary {
    grid-template-columns: 1fr;
    padding: 20px 16px 0;
  }
  .main-subsection .community-sanctuary {
    grid-template-columns: 1fr;
    padding: 32px 16px;
  }
  .main-subsection .container-44 {
    grid-column: auto;
    grid-row: auto;
  }
  .main-subsection .container-45 {
    grid-column: auto;
    grid-row: auto;
  }
  .main-subsection .latest-stories {
    padding: 32px 16px 0;
  }
  .main-subsection .container-50 {
    grid-template-columns: 1fr;
  }
  .main-subsection .side-stories-right {
    padding-bottom: 0;
  }
  .main-subsection .FAQ-section {
    padding: 48px 16px;
  }
}

@media (max-width: 640px) {
  .main-subsection .main-navigation-menu {
    flex-wrap: wrap;
  }
  .main-subsection .desktop-nav-hp {
    display: none;
  }
  .main-subsection .hamburger-hp {
    display: flex;
  }
  .main-subsection .logo-4 {
    flex: 1;
  }
  .main-subsection .right-actions-hp {
    margin-left: auto;
    flex-shrink: 0;
  }
  .main-subsection .OPEN-DOOR-VICTORIA-4 {
    height: 44px;
    width: 37px;
  }
  .main-subsection .logo-opendoor-hp {
    font-size: 16px;
  }
  .main-subsection .logo-victoria-hp {
    font-size: 11px;
  }
  .main-subsection .qe-text-hp {
    font-size: 13px;
  }
  .main-subsection .button-quick-exit-3 {
    padding: 0 8px;
    height: 34px;
  }
  .main-subsection .hero-section {
    padding: 100px 16px 40px;
    min-height: 420px;
  }
  .main-subsection .background-6 {
    flex-wrap: wrap;
  }
  .main-subsection .find-resources-wrapper {
    width: 100%;
    justify-content: center;
  }
  .main-subsection .container-38 {
    padding: 24px 16px 0;
  }
  .main-subsection .section-primary {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  .main-subsection .community-sanctuary {
    grid-template-columns: 1fr;
    padding: 24px 16px;
  }
  .main-subsection .story-card {
    flex-direction: column;
  }
  .main-subsection .container-53 {
    width: 100%;
  }
  .main-subsection .container-54 {
    width: 100%;
  }
  .main-subsection .container-56 {
    flex-direction: column;
    gap: 24px;
  }
  .main-subsection .heading-wrapper {
    width: 100%;
  }
  .main-subsection .container-57 {
    min-width: unset;
    width: 100%;
  }
  .main-subsection .text-wrapper-59 {
    font-size: clamp(24px, 6vw, 48px);
    white-space: normal;
    width: 100%;
  }
}
</style>