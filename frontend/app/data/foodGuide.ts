export type FoodGuideMacro = {
  label: 'FAT' | 'CARBS' | 'PROTEIN'
  value: string
}

export type FoodGuideItem = {
  name: string
  officialName: string
  ingredientCode: string
  bodyPart: string
  foodGroup: string
  serveSize: string
  image: string
  tags: string[]
  macros: FoodGuideMacro[]
  howOften: string
  ageGroup: string
  source: string
}

export const foodGuideItems: FoodGuideItem[] = [
  {
    name: 'Salmon',
    officialName: 'Fresh Salmon Fins',
    ingredientCode: '4746694P',
    bodyPart: 'Brain',
    foodGroup: 'Fish / Lean Protein',
    serveSize: '60g raw OR 50g cooked fish',
    image: '/images/bodymap/bmp-4.webp',
    tags: ['Lean Protein', 'Seafood'],
    macros: [
      { label: 'FAT', value: '5.5g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '24.4g' },
    ],
    howOften: 'Fish 1–2 times per fortnight (preferably 2 times)',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Lean red meat(Beef)',
    officialName: 'Beef Scotch Fillet',
    ingredientCode: '3167410P',
    bodyPart: 'Brain',
    foodGroup: 'Lean Red Meat',
    serveSize: '50g raw OR 30g cooked lean red meat',
    image: '/images/bodymap/bmp-1.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '2.8g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '23.8g' },
    ],
    howOften: 'Lean red meat 4 times per fortnight',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Protein cereal',
    officialName: 'Weet-Bix Protein Cereal',
    ingredientCode: '3504601P',
    bodyPart: 'Brain',
    foodGroup: 'Grain / Cereal',
    serveSize: '30g (2 Weetbix or similar)',
    image: '/images/bodymap/bmp-3.webp',
    tags: ['Wholegrain', 'Energy Food'],
    macros: [
      { label: 'FAT', value: '5.6g' },
      { label: 'CARBS', value: '56.5g' },
      { label: 'PROTEIN', value: '12.5g' },
    ],
    howOften:
      "2 children's serves of grain foods per day. Wholegrain varieties at least 3 times per week — preferably every day",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Mushrooms',
    officialName: 'Organic Brown Mushrooms',
    ingredientCode: '3520845P',
    bodyPart: 'Brain',
    foodGroup: 'Vegetables',
    serveSize: '½ cup cooked (75g)',
    image: '/images/bodymap/bmp-2.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '3.1g' },
      { label: 'CARBS', value: '69.1g' },
      { label: 'PROTEIN', value: '7.6g' },
    ],
    howOften:
      "1–1½ children's serves of vegetables per day. At least 2–3 different types per day and 5 different types per week",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },

  {
    name: 'carrots',
    officialName: 'Kitchen Shredded Carrot',
    ingredientCode: '2470424P',
    bodyPart: 'Eyes',
    foodGroup: 'Vegetables',
    serveSize: '½ cup cooked (75g)',
    image: '/images/bodymap/bmp-5.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '6.3g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '22.9g' },
    ],
    howOften:
      "1–1½ children's serves of vegetables per day. At least 2–3 different types per day and 5 different types per week",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Spinach',
    officialName: 'Baby Spinach',
    ingredientCode: '1499486P',
    bodyPart: 'Eyes',
    foodGroup: 'Vegetables (Leafy Greens)',
    serveSize: '1 cup leafy greens',
    image: '/images/bodymap/bmp-6.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '2.8g' },
    ],
    howOften:
      "1–1½ children's serves of vegetables per day. At least 2–3 different types per day and 5 different types per week",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Silverbeet',
    officialName: 'Organic Silverbeet',
    ingredientCode: '4350944P',
    bodyPart: 'Eyes',
    foodGroup: 'Vegetables (Leafy Greens)',
    serveSize: '1 cup leafy greens',
    image: '/images/bodymap/bmp-7.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0.3g' },
      { label: 'CARBS', value: '1.7g' },
      { label: 'PROTEIN', value: '2.5g' },
    ],
    howOften:
      "1–1½ children's serves of vegetables per day. At least 2–3 different types per day and 5 different types per week",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Tomato (kumato)',
    officialName: 'Tomatoes Kumato',
    ingredientCode: '8933048P',
    bodyPart: 'Eyes',
    foodGroup: 'Vegetables',
    serveSize: '½ cup (75g)',
    image: '/images/bodymap/bmp-8.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '3g' },
      { label: 'PROTEIN', value: '0.9g' },
    ],
    howOften: '4–5 serves of vegetables each day',
    ageGroup: 'School-age (primary school)',
    source: 'RCH Healthy Eating for School-Age Children — rch.org.au',
  },

  {
    name: 'Milk',
    officialName: 'Fresh Skim Milk',
    ingredientCode: '9321047P',
    bodyPart: 'Bones',
    foodGroup: 'Dairy / Milk',
    serveSize: '100mL (childcare) OR 250mL (school-age)',
    image: '/images/bodymap/bmp-9.webp',
    tags: ['Dairy', 'Calcium'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '5.3g' },
      { label: 'PROTEIN', value: '3.6g' },
    ],
    howOften:
      "2 children's serves of dairy per day. Offered at morning tea and/or afternoon tea every day",
    ageGroup: '1–5 years (childcare) | School-age',
    source:
      'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au | RCH Healthy Eating for School-Age Children — rch.org.au',
  },
  {
    name: 'Cheddar cheese',
    officialName: 'Irish Cheddar',
    ingredientCode: '5362971P',
    bodyPart: 'Bones',
    foodGroup: 'Dairy / Cheese',
    serveSize: '15g (1 slice) childcare OR 40g school-age',
    image: '/images/bodymap/bmp-10.webp',
    tags: ['Dairy', 'Calcium'],
    macros: [
      { label: 'FAT', value: '33.4g' },
      { label: 'CARBS', value: '0.3g' },
      { label: 'PROTEIN', value: '24.6g' },
    ],
    howOften:
      '2–3 serves of dairy foods each day to provide enough calcium for bone development',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'RCH Healthy Eating for School-Age Children — rch.org.au',
  },
  {
    name: 'Eggs',
    officialName: 'Free Range Eggs 18 Pack',
    ingredientCode: '5346590P',
    bodyPart: 'Bones',
    foodGroup: 'Eggs / Lean Protein',
    serveSize: '1 egg = 1 serve',
    image: '/images/bodymap/bmp-11.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '5.7g' },
      { label: 'CARBS', value: '1.8g' },
      { label: 'PROTEIN', value: '17g' },
    ],
    howOften:
      "1 children's serve of lean protein per day. 1 egg equals one children's serve",
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Fish (Red Snapper)',
    officialName: 'Fresh Saddletail Snapper Fillet',
    ingredientCode: '1024106P',
    bodyPart: 'Bones',
    foodGroup: 'Fish / Lean Protein',
    serveSize: '60g raw OR 50g cooked fish',
    image: '/images/bodymap/bmp-12.webp',
    tags: ['Lean Protein', 'Seafood'],
    macros: [
      { label: 'FAT', value: '1.6g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '20.3g' },
    ],
    howOften: 'Fish 1–2 times per fortnight (preferably 2 times)',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },

  {
    name: 'Red meat(Beef Rump)',
    officialName: 'No Added Hormone Beef Rump Steak Half',
    ingredientCode: '3581952P',
    bodyPart: 'Muscles',
    foodGroup: 'Lean Red Meat',
    serveSize: '50g raw OR 30g cooked lean red meat',
    image: '/images/bodymap/bmp-14.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '4.5g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '32g' },
    ],
    howOften: 'Lean red meat 4 times per fortnight',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'chicken',
    officialName: 'Deli Chicken Thigh Fillet',
    ingredientCode: '3326445P',
    bodyPart: 'Muscles',
    foodGroup: 'Lean Poultry',
    serveSize: '40g cooked (skin off)',
    image: '/images/bodymap/bmp-13.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '8.7g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '24.2g' },
    ],
    howOften: 'Lean poultry 2 times per fortnight',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Lean red meat (Lamb)',
    officialName: 'Graze Lamb Leg Roast Half',
    ingredientCode: '3693843P',
    bodyPart: 'Muscles',
    foodGroup: 'Lean Red Meat (Lamb)',
    serveSize: '50g raw OR 30g cooked lean lamb',
    image: '/images/bodymap/bmp-15.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '6g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '30.6g' },
    ],
    howOften: 'Lean red meat 4 times per fortnight',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Fish( Basa fillets)',
    officialName: 'Basa Skin Off Fillet',
    ingredientCode: '3954404P',
    bodyPart: 'Muscles',
    foodGroup: 'Fish / Lean Protein',
    serveSize: '60g raw OR 50g cooked fish',
    image: '/images/bodymap/bmp-16.webp',
    tags: ['Lean Protein', 'Seafood'],
    macros: [
      { label: 'FAT', value: '0.4g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '24.6g' },
    ],
    howOften: 'Fish 1–2 times per fortnight (preferably 2 times)',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },

  {
    name: 'Brussel sprouts',
    officialName: 'Baby Brussels Sprouts Prepacked',
    ingredientCode: '9989810P',
    bodyPart: 'Immunity',
    foodGroup: 'Vegetables (Cruciferous)',
    serveSize: '½ cup cooked (75g)',
    image: '/images/bodymap/bmp-17.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0.3g' },
      { label: 'CARBS', value: '4.2g' },
      { label: 'PROTEIN', value: '3.8g' },
    ],
    howOften:
      'Vegetables every day at afternoon tea. At least 2–3 different types per day and 5 different types per week',
    ageGroup: 'School-age (OSHC)',
    source: 'HEAS Food and Drink Checklist for Outside School Hours Care — heas.health.vic.gov.au',
  },
  {
    name: 'Red Cabbage',
    officialName: 'Organic Red Cabbage Whole',
    ingredientCode: '3015015P',
    bodyPart: 'Immunity',
    foodGroup: 'Vegetables',
    serveSize: '½ cup cooked (75g)',
    image: '/images/bodymap/bmp-18.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '72.3g' },
      { label: 'PROTEIN', value: '0.3g' },
    ],
    howOften:
      'At least 2–3 different types of vegetables per day and 5 different types per week',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Prawns (black Tiger)',
    officialName: 'Fresh Australian Cooked Black Tiger Prawns',
    ingredientCode: '3950811P',
    bodyPart: 'Immunity',
    foodGroup: 'Seafood / Lean Protein',
    serveSize: '60g raw OR 50g cooked seafood',
    image: '/images/bodymap/bmp-19.webp',
    tags: ['Lean Protein', 'Seafood'],
    macros: [
      { label: 'FAT', value: '0.3g' },
      { label: 'CARBS', value: '7.4g' },
      { label: 'PROTEIN', value: '1.2g' },
    ],
    howOften: 'Fish and seafood 1–2 times per fortnight (preferably 2 times)',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Yellow nectarines',
    officialName: 'Yellow Nectarines',
    ingredientCode: '409808P',
    bodyPart: 'Immunity',
    foodGroup: 'Fruit',
    serveSize: '75g (1 small piece)',
    image: '/images/bodymap/bmp-20.webp',
    tags: ['Fruit', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '6.7g' },
      { label: 'PROTEIN', value: '0.8g' },
    ],
    howOften:
      'Fruit every day at afternoon tea. At least 2–3 different types per day and 5 different types per week. Dried fruit not every day',
    ageGroup: 'School-age (OSHC)',
    source: 'HEAS Food and Drink Checklist for Outside School Hours Care — heas.health.vic.gov.au',
  },

  {
    name: 'oats',
    officialName: 'Oats Sachets Original',
    ingredientCode: '3990838P',
    bodyPart: 'Energy',
    foodGroup: 'Grain / Cereal (Oats)',
    serveSize: '⅓ cup dry oats (30g)',
    image: '/images/bodymap/bmp-21.webp',
    tags: ['Wholegrain', 'Energy Food'],
    macros: [
      { label: 'FAT', value: '0.9g' },
      { label: 'CARBS', value: '74.4g' },
      { label: 'PROTEIN', value: '2.1g' },
    ],
    howOften: '4–5 serves of bread and cereal each day. Choose wholegrain varieties',
    ageGroup: 'School-age (primary school)',
    source: 'RCH Healthy Eating for School-Age Children — rch.org.au',
  },
  {
    name: 'wholemeal bread',
    officialName: 'Spelt Wholemeal Bread',
    ingredientCode: '6750637P',
    bodyPart: 'Energy',
    foodGroup: 'Grain / Bread (Wholegrain)',
    serveSize: '1 slice (40g)',
    image: '/images/bodymap/bmp-22.webp',
    tags: ['Wholegrain', 'Energy Food'],
    macros: [
      { label: 'FAT', value: '8.1g' },
      { label: 'CARBS', value: '59.1g' },
      { label: 'PROTEIN', value: '10.6g' },
    ],
    howOften:
      "2 children's serves of grain foods per day. Wholegrain varieties at least 3 times per week — preferably every day",
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Turkey',
    officialName: 'Frozen Turkey Hindquarter',
    ingredientCode: '5033288P',
    bodyPart: 'Energy',
    foodGroup: 'Lean Poultry',
    serveSize: '40g cooked (skin off)',
    image: '/images/bodymap/bmp-24.webp',
    tags: ['Lean Protein', 'High Protein'],
    macros: [
      { label: 'FAT', value: '7g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '26.8g' },
    ],
    howOften: 'Lean poultry 2 times per fortnight',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
  {
    name: 'Sourdough',
    officialName: 'Sourdough 7 Grain With Barleymax',
    ingredientCode: '5184909P',
    bodyPart: 'Energy',
    foodGroup: 'Grain / Bread (Wholegrain)',
    serveSize: '1 slice (40g)',
    image: '/images/bodymap/bmp-23.webp',
    tags: ['Wholegrain', 'Energy Food'],
    macros: [
      { label: 'FAT', value: '0.9g' },
      { label: 'CARBS', value: '74.4g' },
      { label: 'PROTEIN', value: '2.1g' },
    ],
    howOften:
      "2 children's serves of grain foods per day. Wholegrain varieties at least 3 times per week — preferably every day",
    ageGroup: '1–5 years (childcare)',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },

  {
    name: 'Yoghurt',
    officialName: 'Strawberry Mango Yoghurt 4 Pack',
    ingredientCode: '3823519P',
    bodyPart: 'Teeth',
    foodGroup: 'Dairy / Yoghurt',
    serveSize: '80g childcare OR 200g school-age',
    image: '/images/bodymap/bmp-25.webp',
    tags: ['Dairy', 'Calcium'],
    macros: [
      { label: 'FAT', value: '0.2g' },
      { label: 'CARBS', value: '5.6g' },
      { label: 'PROTEIN', value: '0.7g' },
    ],
    howOften:
      'Milk yoghurt cheese and/or calcium fortified alternatives every day. Mostly reduced fat varieties',
    ageGroup: 'School-age (OSHC)',
    source: 'HEAS Food and Drink Checklist for Outside School Hours Care — heas.health.vic.gov.au',
  },
  {
    name: 'Cheese. (Parmeasan)',
    officialName: 'Parmesan Cheese With Chilli',
    ingredientCode: '3946960P',
    bodyPart: 'Teeth',
    foodGroup: 'Dairy / Cheese',
    serveSize: '15g (1 slice) childcare OR 40g school-age',
    image: '/images/bodymap/bmp-26.webp',
    tags: ['Dairy', 'Calcium'],
    macros: [
      { label: 'FAT', value: '27.2g' },
      { label: 'CARBS', value: '0g' },
      { label: 'PROTEIN', value: '27.4g' },
    ],
    howOften: '2–3 serves of dairy foods such as cheese yoghurt and milk each day',
    ageGroup: 'School-age (primary school)',
    source: 'RCH Healthy Eating for School-Age Children — rch.org.au',
  },
  {
    name: 'Qukes',
    officialName: 'Organic Qukes',
    ingredientCode: '5088494P',
    bodyPart: 'Teeth',
    foodGroup: 'Vegetables',
    serveSize: '½ cup (75g)',
    image: '/images/bodymap/bmp-27.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '3.4g' },
      { label: 'CARBS', value: '47.4g' },
      { label: 'PROTEIN', value: '13.7g' },
    ],
    howOften:
      'Vegetables every day at afternoon tea. At least 2–3 different types per day and 5 different types per week',
    ageGroup: 'School-age (OSHC)',
    source: 'HEAS Food and Drink Checklist for Outside School Hours Care — heas.health.vic.gov.au',
  },
  {
    name: 'Onions',
    officialName: 'Baby Brown Onions',
    ingredientCode: '2552868P',
    bodyPart: 'Teeth',
    foodGroup: 'Vegetables',
    serveSize: '½ cup (75g)',
    image: '/images/bodymap/bmp-28.webp',
    tags: ['Vegetables', 'Everyday Food'],
    macros: [
      { label: 'FAT', value: '0g' },
      { label: 'CARBS', value: '9.6g' },
      { label: 'PROTEIN', value: '0.4g' },
    ],
    howOften:
      'At least 2–3 different types of vegetables per day and 5 different types per week',
    ageGroup: '1–5 years (childcare) | School-age',
    source: 'HEAS Menu Planning Guidelines for Long Day Care — heas.health.vic.gov.au',
  },
]

const normaliseFoodName = (value: string) =>
  value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()

export const findFoodGuideIndex = (foodName: string) => {
  const selected = normaliseFoodName(foodName)

  return foodGuideItems.findIndex((food) => {
    return normaliseFoodName(food.name) === selected
  })
}