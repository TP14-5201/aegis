<template>
  <section class="nutrition-hero-section">
    <div class="nutrition-hero-inner">
      <!-- HERO CARD -->
      <div class="hero-card">
        <div class="hero-copy">
          <h1>
            Your family’s health,
            <span>made simple</span>
          </h1>

          <p>
            Feeding a family well on a tight budget is hard. These guides are
            here to make it a little easier — showing you what food does for
            your child’s body and helping you learn a little more about food.
          </p>
        </div>

        <div class="hero-image-wrap">
          <img
            src="/images/nutrition-guide/nh-1.png"
            alt="Healthy food bowl"
            class="hero-image"
          />
        </div>
      </div>

      <!-- QUICK ACCESS CARDS -->
      <div class="quick-access-grid">
        <article class="quick-card">
          <img
            src="/images/nutrition-guide/nh-2.png"
            alt="Body map icon"
            class="quick-icon"
          />

          <h3>Interactive Body Map</h3>

          <p>
            See how foods power each body part, from brain to bones.
          </p>

          <a href="#body-map" class="quick-btn">
            Explore Map
          </a>
        </article>

        <article class="quick-card">
          <img
            src="/images/nutrition-guide/nh-3.png"
            alt="Food guide icon"
            class="quick-icon"
          />

          <h3>Smart Nutrition Guide</h3>

          <p>
            What's really inside everyday foods for you and your family.
          </p>

          <a href="#food-guide" class="quick-btn">
            Explore Guide
          </a>
        </article>

        <article class="quick-card">
          <img
            src="/images/nutrition-guide/nh-4.png"
            alt="Wellness icon"
            class="quick-icon"
          />

          <h3>Wellness Tips</h3>

          <p>
            Quick, bite-sized advice that fits your busy family day.
          </p>

          <a href="#wellness-guide" class="quick-btn">
            Explore Tips
          </a>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.nutrition-hero-section {
  position: relative;
  width: 100%;
  margin-top: -72px;
  padding: 112px 0 44px;
  overflow: hidden;
  background: linear-gradient(
    180deg,
    #f8f9ff 0%,
    #eef3ff 45%,
    #e6eeff 100%
  );
}

.nutrition-hero-inner {
  width: min(1200px, calc(100% - 80px));
  margin: 0 auto;
}

/* HERO */
.hero-card {
  display: grid;
  grid-template-columns: 1.04fr 1fr;
  overflow: hidden;
  border-radius: 12px;
  background: #e6eeff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.hero-copy {
  min-height: 390px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 54px 56px;
}

.hero-copy h1 {
  margin: 0;
  color: #181e4b;
  font-family: 'Playfair Display', serif;
  font-size: 46px;
  font-weight: 700;
  line-height: 1.12;
  letter-spacing: -0.7px;
}

.hero-copy h1 span {
  display: block;
  color: #396477;
}

.hero-copy p {
  max-width: 520px;
  margin: 22px 0 0;
  color: #45464d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.62;
}

.hero-image-wrap {
  min-height: 390px;
}

.hero-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

/* QUICK ACCESS */
.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 28px;
}

.quick-card {
  min-height: 224px;
  padding: 28px 30px;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
}

.quick-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(24, 30, 75, 0.12);
}

.quick-icon {
  width: 30px;
  height: 30px;
  object-fit: contain;
  display: block;
}

.quick-card h3 {
  margin: 18px 0 0;
  color: #181e4b;
  font-family: 'Playfair Display', serif;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.32;
}

.quick-card p {
  max-width: 300px;
  margin: 10px 0 0;
  color: #45464d;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.48;
}

.quick-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  margin-top: 16px;
  padding: 0 24px;
  border-radius: 8px;
  background: #000000;
  color: #ffffff;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  text-decoration: none;
  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.quick-btn:hover {
  background: #181e4b;
  transform: translateY(-1px);
}

/* TABLET */
@media (max-width: 1024px) {
  .nutrition-hero-section {
    margin-top: -72px;
    padding-top: 108px;
  }

  .nutrition-hero-inner {
    width: min(100% - 40px, 900px);
  }

  .hero-card {
    grid-template-columns: 1fr;
  }

  .hero-copy {
    min-height: auto;
    padding: 44px 36px;
  }

  .hero-image-wrap {
    height: 340px;
    min-height: 340px;
  }

  .quick-access-grid {
    grid-template-columns: 1fr;
  }
}

/* DESKTOP NAV HEIGHT */
@media (min-width: 1024px) {
  .nutrition-hero-section {
    margin-top: -100px;
    padding-top: 132px;
  }
}

/* MOBILE */
@media (max-width: 640px) {
  .nutrition-hero-inner {
    width: calc(100% - 32px);
  }

  .hero-copy {
    padding: 36px 24px;
  }

  .hero-copy h1 {
    font-size: 36px;
    line-height: 1.15;
  }

  .hero-copy p {
    font-size: 15px;
    line-height: 1.55;
  }

  .hero-image-wrap {
    height: 280px;
    min-height: 280px;
  }

  .quick-card {
    padding: 26px 24px;
  }
}
</style>