export type WellnessSide = "do" | "dont";
export type WellnessTableVariant = "plain" | "compare";

export type WellnessCommonItem = {
  label: string;
  iconSrc?: string;
};

export type WellnessPopupTable = {
  headers: string[];
  values: string[];
  headerHtml?: string[];
  valueHtml?: string[];
};

export type WellnessPopup = {
  category: "DO" | "DON'T";
  /** Set false to match Figma cards (no DO/DON'T label) */
  showCategory?: boolean;
  title: string;
  subtitle: string;
  intro: string[];
  tableTitle?: string;
  table?: WellnessPopupTable;
  tableVariant?: WellnessTableVariant;
  alert?: string;
  alertHtml?: string;
  commonTitle?: string;
  commonSources?: string[];
  commonItems?: WellnessCommonItem[];
  commonChips?: boolean;
  tips: {
    label: string;
    text: string;
  }[];
  note?: string;
  /** Bottom-left footnote (e.g. screen time disclaimer), outside the black frame */
  footerNote?: string;
  imageSrc: string;
  imageAlt: string;
  sources: string[];
};

export type OrbitItem = {
  label: string;
  iconSrc: string;
  side: WellnessSide;
  position: string;
  popup: WellnessPopup;
};

export const orbitItems: OrbitItem[] = [
  {
    label: "Hydrate",
    iconSrc: "/images/wellness/do-1.webp",
    side: "do",
    position: "do-hydrate",
    popup: {
      category: "DO",
      showCategory: false,
      title: "HYDRATE: Give Your Kids Water",
      subtitle: "THE CHEAPEST, HEALTHIEST DRINK IS ALREADY IN YOUR TAP",
      intro: [
        "The Australian Government (Department of Health) confirms that water is the best drink for children of all ages and should be available at all times. Tap water is free, widely available, and fluoridated in most Australian communities for oral health.",
        "Children are especially at risk of dehydration in hot weather, during play, or when sick. Signs of dehydration include fewer wet nappies or trips to the toilet, dry mouth, tiredness, and sunken eyes.",
      ],
      tips: [
        {
          label: "Free & easy",
          text: "Keep a reusable water bottle in the school bag. Refill from the tap - no cost, no sugar, no problem.",
        },
        {
          label: "Fussy drinker?",
          text: "The Raising Children Network suggests adding different-shaped ice cubes to make water more fun for young children.",
        },
        {
          label: "Make it normal",
          text: "Put a jug of water on the table at every meal. When kids see you drinking water, they copy you.",
        },
      ],
      imageSrc: "/images/wellness/popups/hydrate.webp",
      imageAlt: "Glass of water being filled",
      sources: [
        "health.gov.au",
        "betterhealth.vic.gov.au",
        "raisingchildren.net.au",
      ],
    },
  },

  {
    label: "Sleep",
    iconSrc: "/images/wellness/do-2.webp",
    side: "do",
    position: "do-sleep",
    popup: {
      category: "DO",
      showCategory: false,
      title: "SLEEP: consistent Bedtimes Cost Nothing",
      subtitle:
        "A WELL-RESTED CHILD IS AN ACTIVE CHILD – AND AN ACTIVE CHILD SLEEPS BETTER",
      intro: [
        "Getting enough good-quality sleep supports healthy growth, brain development, and emotional regulation in children.",
        "How much sleep does my child need each night?",
      ],
      table: {
        headers: [
          "Toddlers (1–2 years)",
          "Preschoolers (3–5 years)",
          "Primary School (5–13 years)",
          "Teenagers (14–17)",
        ],
        headerHtml: [
          "Toddlers<br>(1–2 years)",
          "Preschoolers<br>(3–5 years)",
          "Primary School<br>(5–13 years)",
          "Teenagers<br>(14–17)",
        ],
        values: ["11–14 hrs", "10–13 hrs", "9–11 hrs", "8–10 hrs"],
      },
      tips: [
        {
          label: "Free tip",
          text: "The single most effective thing you can do is keep the same bedtime and wake-up time every day - including weekends.",
        },
        {
          label: "Single Parent tip",
          text: "Set a 'wind-down' routine: bath, book, bed. Even 15 minutes of quiet reading before bed signals to children's brains that sleep is coming.",
        },
      ],
      imageSrc: "/images/wellness/popups/sleep.webp",
      imageAlt: "Child sleeping in bed",
      sources: ["health.gov.au", "betterhealth.vic.gov.au"],
    },
  },

  {
    label: "Veggies",
    iconSrc: "/images/wellness/do-3.webp",
    side: "do",
    position: "do-veggies",
    popup: {
      category: "DO",
      showCategory: false,
      title: "VEGGIES: cheap, filling, and powerful",
      subtitle:
        "FROZEN AND CANNED VEGETABLES ARE JUST AS NUTRITIOUS – AND MUCH CHEAPER",
      intro: [
        "Vegetables and fruit contain essential nutrients for children's health, growth, and development. Eating vegetables can help protect children against diseases including diabetes and some cancers.",
        "Most children do not eat enough vegetables. Small, regular servings across the day are easier than one large serve at dinner.",
      ],
      tableTitle: "How many serves does my child need per day?",
      table: {
        headers: [
          "Toddlers (1–3 years)",
          "Preschoolers (3–8 years)",
          "Primary School (9–11 years)",
          "Teenagers (12–18)",
        ],
        headerHtml: [
          "Toddlers<br>(1–3 years)",
          "Preschoolers<br>(3–8 years)",
          "Primary School<br>(9–11 years)",
          "Teenagers<br>(12–18)",
        ],
        values: ["2–3 serves", "4½ serves", "5 serves", "5–5½ serves"],
      },
      tips: [
        {
          label: "Budget tip",
          text: "Buy in-season vegetables — they are cheaper and fresher. Frozen vegetables like peas, corn, and mixed vegetables are nutritious, inexpensive, and last for weeks.",
        },
        {
          label: "Fussy kids",
          text: "Children may need to try a new food up to 10 times before accepting it. Keep offering — don't give up.",
        },
      ],
      note: "1 serve = ½ cup cooked veg · 1 cup raw salad · ½ cup beans or lentils",
      imageSrc: "/images/wellness/popups/veggies.webp",
      imageAlt: "Fresh vegetables",
      sources: [
        "raisingchildren.net.au",
        "eatforhealth.gov.au",
        "betterhealth.vic.gov.au",
      ],
    },
  },

  {
    label: "Fruits",
    iconSrc: "/images/wellness/do-4.webp",
    side: "do",
    position: "do-fruits",
    popup: {
      category: "DO",
      showCategory: false,
      title: "FRUITS: nature's cheapest snack",
      subtitle: "WHOLE FRUIT BEATS JUICE EVERY TIME - AND IT COSTS LESS TOO",
      intro: [
        "Fruit provides essential vitamins, minerals, fibre, and energy for growing children. Eating fruit regularly helps children have the energy they need to play, concentrate better, learn, sleep better.",
      ],
      tableTitle: "How many serves of fruit per day?",
      table: {
        headers: [
          "Toddlers (1-2 years)",
          "Preschoolers (2-3 years)",
          "Primary School (4-8 years)",
          "Teenagers (9-18)",
        ],
        headerHtml: [
          "Toddlers<br>(1-2 years)",
          "Preschoolers<br>(2-3 years)",
          "Primary School<br>(4-8 years)",
          "Teenagers<br>(9-18)",
        ],
        values: ["½ serve", "1 serve", "1½ serves", "2 serves"],
      },
      tips: [
        {
          label: "Skip the juice",
          text: "The Raising Children Network advises that whole fruit is better than juice - it keeps the fibre, satisfies hunger, and has no extra sugar. Fruit juice adds cost without the benefit.",
        },
        {
          label: "Lunchbox idea",
          text: "A banana, a small handful of grapes, or two mandarins costs less than a muesli bar and is far more nutritious.",
        },
      ],
      note: "1 serve = 1 medium fruit · 2 small pieces like kiwi · 1 cup diced fruit",
      imageSrc: "/images/wellness/popups/fruits.webp",
      imageAlt: "Bowl of mixed fruit",
      sources: ["raisingchildren.net.au", "betterhealth.vic.gov.au"],
    },
  },

  {
    label: "Food Variety",
    iconSrc: "/images/wellness/do-5.webp",
    side: "do",
    position: "do-variety",
    popup: {
      category: "DO",
      showCategory: false,
      title: "FOOD VARIETY: the five food groups made simple",
      subtitle:
        "YOU DON'T NEED EXPENSIVE FOOD TO EAT WELL - YOU NEED VARIETY FROM FIVE KEY FOOD GROUPS",
      intro: [
        "Children need to eat a variety of nutritious foods from the five food groups every day. Each group provides different nutrients that children's bodies need to grow and work properly.",
      ],
      tableTitle: "The Five Food Groups - budget-friendly options for each:",
      table: {
        headers: [
          "Vegetables & Legumes",
          "Fruits",
          "Grains & Cereals",
          "Lean Proteins",
          "Dairy",
        ],
        values: [
          "Fresh, frozen or canned",
          "Fresh, canned in juice or frozen",
          "Oats, bread, rice, pasta",
          "Eggs, tuna, chicken, tofu",
          "Milk, yoghurt, cheese",
        ],
      },
      tips: [
        {
          label: "Meal Planning tip",
          text: "Cook a big pot of soup, bolognese, or lentil stew on Sunday and use it across 2–3 meals during the week. Saves time and money.",
        },
        {
          label: "Lunchbox idea",
          text: "Eating for Health guidelines say lunchboxes should reflect the Five Food Groups - a sandwich (grains + protein), a piece of fruit, some vegetables sticks, and water. Simple and affordable.",
        },
      ],
      imageSrc: "/images/wellness/popups/food-variety.webp",
      imageAlt: "Five food groups plate",
      sources: ["eatforhealth.gov.au"],
    },
  },

  {
    label: "Stay Active",
    iconSrc: "/images/wellness/do-6.webp",
    side: "do",
    position: "do-active",
    popup: {
      category: "DO",
      showCategory: false,
      title: "STAY ACTIVE: free, fun, and essential",
      subtitle:
        "ACTIVE PLAY AT THE PARK COSTS NOTHING. IT IS ONE OF THE BEST THING YOU CAN DO FOR YOUR CHILD",
      intro: [
        "Being active has many social, emotional, intellectual, and health benefits for children. It helps children maintain a healthy weight, build strong bones and muscles, improve sleep, and feel better emotionally.",
        "Physical activity also helps children develop coordination, confidence, and social skills through play with others.",
      ],
      tableTitle: "How much physical activity does my child need?",
      table: {
        headers: [
          "Infants (0–12 months)",
          "Toddlers (1–3 years)",
          "Preschoolers (3–5 years)",
          "Children & Teens (5–17 years)",
        ],
        headerHtml: [
          "Infants<br>(0–12 months)",
          "Toddlers<br>(1–3 years)",
          "Preschoolers<br>(3–5 years)",
          "Children & Teens<br>(5–17 years)",
        ],
        values: [
          "Active play + 30 min tummy time",
          "At least 3 hrs/day",
          "3 hrs incl. 1 hr energetic play",
          "At least 60 min/day",
        ],
      },
      tips: [
        {
          label: "Single parent tip",
          text: "Combine activity with daily routines — walk instead of drive for short trips, kick a ball after school, or do active jobs together like sweeping or gardening.",
        },
        {
          label: "After school",
          text: "Break up long sitting times. Encourage kids to move every 30–60 minutes, especially after school screen time.",
        },
      ],
      imageSrc: "/images/wellness/popups/stay-active.webp",
      imageAlt: "Children running outside",
      sources: ["health.gov.au"],
    },
  },

  {
    label: "Lean Protein",
    iconSrc: "/images/wellness/do-7.webp",
    side: "do",
    position: "do-protein",
    popup: {
      category: "DO",
      showCategory: false,
      title: "LEAN PROTEIN: you don't need expensive meat",
      subtitle:
        "EGGS, FISH, LEGUMES ARE AMONG THE CHEAPEST PROTEINS AVAILABLE – AND JUST AS NUTRITIOUS",
      intro: [
        "Lean proteins are essential for children's growth, muscle development, and brain function. Iron and omega-3 fatty acids from red meat and oily fish are particularly important for a child's brain development and learning.",
      ],
      table: {
        headers: [
          "Eggs",
          "Canned Tuna or Salmon",
          "Canned Legumes",
          "Frozen Chicken",
          "Tofu",
        ],
        values: [
          "Cheap, Versatile & nutrient-rich",
          "High in omega-3",
          "High in iron",
          "Affordable, rich in lean protein",
          "Plant-based, iron & calcium",
        ],
      },
      tips: [
        {
          label: "Stretch the budget",
          text: "Add a can of lentils or chickpeas to salad, soups, or curries. It doubles the quantity, adds protein, and costs very little.",
        },
        {
          label: "Lunchbox idea",
          text: "Eggs are a valuable source of low-cost, easy-to-prepare protein — especially useful for children.",
        },
      ],
      imageSrc: "/images/wellness/popups/lean-protein.webp",
      imageAlt: "Protein foods",
      sources: [
        "raisingchildren.net.au",
        "eatforhealth.gov.au",
        "betterhealth.vic.gov.au",
      ],
    },
  },

  {
    label: "Saturated fats",
    iconSrc: "/images/wellness/dt-1.webp",
    side: "dont",
    position: "dont-fat",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "SATURATED FATS: Not the everyday choice",
      subtitle:
        "HEALTHIER COOKING FATS ARE AVAILABLE - AND SWAPPING THEM IS EASIER THANK YOU THINK",
      intro: [
        "The Australian Dietary Guidelines recommend replacing foods high in saturated fat with healthier alternatives. Low-fat diets are not suitable for children under 2 years of age.",
        "Regularly eating foods high in saturated fat, added sugars, and salt can increase the risk of excessive weight gain and diet-related diseases like obesity and type-2 diabetes in children.",
      ],
      table: {
        headers: ["AVOID", "CHOOSE INSTEAD"],
        values: [
          "Butter. Cream. Coconut Oil. Palm oil. Cooking Margarine. Pastries. Processed meats. Biscuits. Cakes. Pizza. Fried foods. Potato chips. Sausages.",
          "Olive oil. Canola oil. Nut butters. Sunflower seeds. Flax seeds. Avocado. Sesame seeds. Soybeans. Most nuts. Rice bran. Fish. Lean grass-fed meat.",
        ],
      },
      tableVariant: "compare",
      tips: [
        {
          label: "Budget tip",
          text: "Home-cooked meals are almost always lower in saturated fat than takeaway - and far cheaper. A simple pasta with tinned tomatoes, lentils, and frozen vegetables costs under $3 for a family meal.",
        },
      ],
      imageSrc: "/images/wellness/popups/saturated-fats.webp",
      imageAlt: "Comparison of healthy fats and fried foods",
      sources: ["raisingchildren.net.au", "eatforhealth.gov.au"],
    },
  },

  {
    label: "Added sugar",
    iconSrc: "/images/wellness/dt-2.webp",
    side: "dont",
    position: "dont-sugar",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "ADDED SUGAR: hidden and dangerous",
      subtitle:
        "ADDED SUGAR ADDS COST, KILOJOULES AND HEALTH RISK – WITH NO NUTRITIONAL BENEFIT",
      intro: [
        "The Australian Dietary Guidelines recommend limiting foods and drinks with added sugars. Sugar-sweetened drinks are the largest source of added sugars in children's diets in Australia.",
        "Added sugars add kilojoules without essential nutrients — increasing the risk of excess weight gain and tooth decay in children.",
      ],
      alertHtml:
        "Australian research found children who consumed more than one sugary drink per day (over 250ml) were <span class='alert-red'>26% more likely</span> to be overweight or obese.",
      commonTitle: "COMMON HIDDEN SOURCES:",
      commonChips: true,
      commonItems: [
        {
          label: "soft drinks & cordials",
          iconSrc: "/images/wellness/popups/pu-2.svg",
        },
        {
          label: "Cereals & Yogurt",
          iconSrc: "/images/wellness/popups/pu-3.svg",
        },
        {
          label: "Biscuits & Cakes",
          iconSrc: "/images/wellness/popups/pu-4.svg",
        },
        {
          label: "Sauces & Snack bars",
          iconSrc: "/images/wellness/popups/pu-5.svg",
        },
        {
          label: "Chocolates & Lollies",
          iconSrc: "/images/wellness/popups/pu-6.svg",
        },
      ],
      tips: [
        {
          label: "Label reading",
          text: "Check labels and choose options with less than 10g of sugar per 100g.",
        },
        {
          label: "Sweet swap",
          text: "Seasonal fruit or frozen berries – cheap and better for your teeth.",
        },
      ],
      imageSrc: "/images/wellness/popups/added-sugar.webp",
      imageAlt: "Sugar cubes and granulated sugar",
      sources: ["betterhealth.vic.gov.au", "eatforhealth.gov.au"],
    },
  },

  {
    label: "Sugary drinks",
    iconSrc: "/images/wellness/dt-3.webp",
    side: "dont",
    position: "dont-drinks",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "SUGARY DRINKS: the budget and health drain",
      subtitle:
        "SOFT DRINKS, SPORTS DRINKS, CORDIALS: NONE OF THEM NECESSARY FOR A CHILD'S HEALTH",
      intro: [
        "Limit all sugar-sweetened drinks for children including soft and energy drinks, cordials, fruit drinks, flavoured milks, vitamin-style waters. There is strong evidence of a link between sugary drink consumption and excess weight gain, tooth decay, and reduced bone strength in children.",
      ],
      tableTitle: "What are the best drinks for children?",
      table: {
        headers: [
          "Under 12 months",
          "12 Months–2 Years",
          "2 Years and older",
          "All Ages (Avoid)",
        ],
        values: [
          "Breast milk or infant formula",
          "full fat cow's milk and tap water",
          "reduced-fat milk and tap water",
          "soft drinks, sports drinks",
        ],
      },
      tips: [
        {
          label: "Transition tip",
          text: "If your child is used to sweet drinks, the Better Health Channel suggests gradually diluting drinks with more water over time until they are happy with plain water.",
        },
        {
          label: "Lunchbox idea",
          text: "Australian Government guidelines recommend water as the only drink in school lunchboxes – a reusable bottle from the tap is free and the healthy choice.",
        },
      ],
      imageSrc: "/images/wellness/popups/sugary-drinks.webp",
      imageAlt: "Sugary soft drinks",
      sources: ["raisingchildren.net.au", "betterhealth.vic.gov.au"],
    },
  },

  {
    label: "Fast food",
    iconSrc: "/images/wellness/dt-4.webp",
    side: "dont",
    position: "dont-fast",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "FAST FOOD: save it for special occasions",
      subtitle:
        "ADDED FAST FOOD COSTS MONEY AND MORE HEALTH RISKS — COOKING AT HOME WINS BOTH WAYS",
      intro: [
        "The Australian Guide to Healthy Eating classifies fast food, takeaway, and junk food as sometimes foods — meaning they are not recommended for regular eating.",
      ],
      alertHtml:
        "The Australian Dietary Guidelines recommend keeping fast food for <span class='alert-red'>special occasions only</span> — not as a regular part of a child's diet.",
      commonTitle: "COMMON SOURCES:",
      commonChips: true,
      commonItems: [
        {
          label: "Fried chips & burgers",
          iconSrc: "/images/wellness/popups/pu-7.svg",
        },
        {
          label: "Pizza and Burgers",
          iconSrc: "/images/wellness/popups/pu-8.svg",
        },
        {
          label: "Breads & fried buns",
          iconSrc: "/images/wellness/popups/pu-19.svg",
        },
        {
          label: "Ice creams & sundaes",
          iconSrc: "/images/wellness/popups/pu-9.svg",
        },
        {
          label: "Instant Noodles",
          iconSrc: "/images/wellness/popups/pu-10.svg",
        },
      ],
      tips: [
        {
          label: "Batch Cooking",
          text: "Cook extra and freeze meals for busy nights. This removes the temptation to buy takeaway when tired.",
        },
        {
          label: "Practical swap",
          text: "Pasta, canned tomatoes and frozen vegetables with cheese — under $3, under 20 minutes.",
        },
      ],
      imageSrc: "/images/wellness/popups/fast-food.webp",
      imageAlt: "Fast food meal",
      sources: ["raisingchildren.net.au", "eatforhealth.gov.au"],
    },
  },

  {
    label: "Screen Time",
    iconSrc: "/images/wellness/dt-5.webp",
    side: "dont",
    position: "dont-screen",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "SCREEN TIME: set limits before habits form",
      subtitle:
        "SCREEN TIME LIMITS COST NOTHING TO ENFORCE— BENEFITS FOR YOUR CHILD ARE ENORMOUS",
      intro: [
        "The Australian Government Department of Health recommends limiting sedentary recreational screen time for children. Less screen time is linked to healthier body weight, better sleep, and more active play.",
        "Sedentary screen time can have long-term impacts on a child's development, sleep, physical health, and mental wellbeing.",
      ],
      tableTitle:
        "Maximum recommended sedentary recreational screen time per day:",
      table: {
        headers: ["under 2 Years", "2-5 years", "5 -17 years"],
        values: [
          "no screen time at all",
          "no more than 1 hour per day",
          "no more than 2 hour per day",
        ],
      },
      tips: [
        {
          label: "Free Strategy",
          text: "Set a consistent family rule: no screens at the dinner table and no devices in bedrooms after a set time.",
        },
        {
          label: "Parent Tip",
          text: "Create a written family screen plan with your child. Children are more likely to follow rules they helped create.",
        },
        {
          label: "Sleep Link",
          text: "Screen use before bed affects how quickly and deeply children sleep. Charge devices in a common area — not the bedroom.",
        },
      ],
      footerNote:
        "School-related screen use is not included in these limits",
      imageSrc: "/images/wellness/popups/screen-time.webp",
      imageAlt: "Children using screens in bed",
      sources: ["raisingchildren.net.au", "health.gov.au"],
    },
  },

  {
    label: "Hidden Salt",
    iconSrc: "/images/wellness/dt-6.webp",
    side: "dont",
    position: "dont-salt",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "HIDDEN SALT: its already in the packet",
      subtitle: "MOST OF THE SALT YOUR CHILD EATS TODAY – THEY NEVER ADDED IT THEMSELVES",
      intro: [
        "Many packaged foods contain more salt than families realise. High salt intake in childhood can contribute to high blood pressure later in life.",
        "Choosing lower-salt options and cooking at home more often can support long-term heart health and healthier eating habits.",
      ],
      alertHtml:
        "The Australian Government's average sodium intake is about <span class='alert-red'>3,600mg per day</span> – almost double the recommended target of <span class='alert-green'>2,000mg</span>.",
      commonTitle: "COMMON HIDDEN SOURCES:",
      commonChips: true,
      commonItems: [
        {
          label: "Savoury snack foods",
          iconSrc: "/images/wellness/popups/pu-11.svg",
        },
        {
          label: "Processed meats",
          iconSrc: "/images/wellness/popups/pu-12.svg",
        },
        {
          label: "Pasta & soup sachets",
          iconSrc: "/images/wellness/popups/pu-13.svg",
        },
        {
          label: "Bread & Cereals",
          iconSrc: "/images/wellness/popups/pu-19.svg",
        },
        {
          label: "Sauces & condiments",
          iconSrc: "/images/wellness/popups/pu-14.svg",
        },
      ],
      tips: [
        {
          label: "Label Reading tip",
          text: "Choose products with less than 120mg sodium per 100g where possible — compare similar products side by side.",
        },
        {
          label: "For Babies",
          text: "Babies under 12 months should not have added salt. Breast milk or formula provides all the sodium they need.",
        },
      ],
      imageSrc: "/images/wellness/popups/hidden-salt.webp",
      imageAlt: "Salt crystals in a bowl",
      sources: [
        "betterhealth.vic.gov.au",
        "eatforhealth.gov.au",
        "health.gov.au",
      ],
    },
  },

  {
    label: "Late snacking",
    iconSrc: "/images/wellness/dt-7.webp",
    side: "dont",
    position: "dont-snack",
    popup: {
      category: "DON'T",
      showCategory: false,
      title: "LATE SNACKING: routine matters more than willpower",
      subtitle:
        "REGULAR DINNER TIME - ONE OF THE BEST THINGS YOU CAN DO FOR YOUR CHILD'S HEALTH",
      intro: [
        "Tiredness and late dinners push children toward poor food choices. Children who sleep less may eat more junk food and have higher rates of overweight. A simple early dinner routine can make a bigger difference than willpower.",
      ],
      alertHtml:
        "The Better Health Channel states that not enough sleep can affect children's <span class='alert-red'>behaviour, academics, concentration, and mood.</span>",
      commonTitle: "What disrupts sleep & triggers late snacking:",
      commonChips: true,
      commonItems: [
        {
          label: "screen(blue light) in bedroom",
          iconSrc: "/images/wellness/popups/pu-15.svg",
        },
        {
          label: "Irregular meal & snack times",
          iconSrc: "/images/wellness/popups/pu-16.svg",
        },
        {
          label: "Sugary foods close to bedtime",
          iconSrc: "/images/wellness/popups/pu-17.svg",
        },
        {
          label: "caffeine in chocolates",
          iconSrc: "/images/wellness/popups/pu-18.svg",
        },
      ],
      tips: [
        {
          label: "Label Reading tip",
          text: "If a child needs a snack before bed, give a small tub of yoghurt, a piece of fruit, or a glass of milk.",
        },
        {
          label: "For Babies",
          text: "The most effective strategy is a consistent daily food and sleep routine. It significantly reduces late-night snacking.",
        },
      ],
      imageSrc: "/images/wellness/popups/late-snacking.webp",
      imageAlt: "Child snacking at night",
      sources: ["betterhealth.vic.gov.au", "eatforhealth.gov.au"],
    },
  },
];