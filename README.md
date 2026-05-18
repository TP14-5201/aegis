<div align="center">

<img src="frontend/public/logo/favicon.ico" alt="Cherebowl Logo" width="80" height="80" />

# Cherebowl

**Help is here when you need it.**

Cherebowl is a web platform that helps Victorians experiencing food insecurity find nearby food banks, emergency food relief outlets, housing support services, and access nutrition guidance — all in one place.

[![Python](https://img.shields.io/badge/python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Nuxt](https://img.shields.io/badge/nuxt-4.x-00DC82?style=flat&logo=nuxt.js&logoColor=white)](https://nuxt.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)
[![Tests Status](https://img.shields.io/github/actions/workflow/status/TP14-5201/aegis/backend_tests.yml?branch=main&label=Backend%20CI&logo=github-actions&logoColor=white&style=flat)](https://github.com/TP14-5201/aegis/actions/workflows/app_ci_cd.yml)
[![codecov](https://codecov.io/gh/TP14-5201/aegis/graph/badge.svg?token=JC4L80XQVA)](https://codecov.io/gh/TP14-5201/aegis)

---

### Built With

**Frontend**

[![Nuxt](https://img.shields.io/badge/Nuxt_4-00DC82?style=for-the-badge&logo=nuxt.js&logoColor=white)](https://nuxt.com/)
[![Vue](https://img.shields.io/badge/Vue_3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black)](https://pinia.vuejs.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![D3.js](https://img.shields.io/badge/D3.js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white)](https://d3js.org/)

**Backend**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

**Infrastructure & Deployment**

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)

</div>

---

## Table of Contents

- [Cherebowl](#cherebowl)
    - [Built With](#built-with)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Backend Setup](#backend-setup)
      - [Frontend Setup](#frontend-setup)
      - [Utility Scripts](#utility-scripts)
  - [Usage](#usage)
    - [Running Backend Tests](#running-backend-tests)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

---

## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

| Tool        | Version                   | Notes              |
| ----------- | ------------------------- | ------------------ |
| **Python**  | ≥ 3.10 (3.11 recommended) | Backend runtime    |
| **Node.js** | ≥ 18.x                    | Frontend runtime   |
| **npm**     | ≥ 9.x                     | Comes with Node.js |
| **Git**     | Any                       | Version control    |

> **Optional:** [conda](https://docs.conda.io/) or Python `venv` for environment isolation.

---

### Installation

Clone the repository under the "develop" branch:

```bash
git clone --branch underdevelopment https://github.com/TP-5201/aegis.git
cd aegis
```

#### Backend Setup

**Using `conda`:**

```bash
cd backend
conda create -n cherebowl python=3.11 -y && conda activate cherebowl
pip install -r requirements.txt
```

**Using `venv`:**

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

**Configure environment variables:**

Copy the example `.env` and fill in the required values:

```bash
# backend/.env
DATABASE_URL=postgresql://[YOUR_USERNAME]:[YOUR_PASSWORD]@localhost:5432/postgres
LOGIN_PASSWORD_HASH=[YOUR_BCRYPT_PASSWORD_HASH]
```

To set your own local login password, generate a bcrypt hash and add the printed value to `LOGIN_PASSWORD_HASH` in `backend/.env`:

```bash
conda run -n aegis python -c "import bcrypt, getpass; print(bcrypt.hashpw(getpass.getpass('Password: ').encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))"
```

**Seed the database:**

```bash
# From the backend/ directory
python -m src.services.data_seeding
```

**Checking the Database**

**Visual way (recommended):**
- Install [Postgres](https://www.postgresql.org/download/) locally.
- Install [PostgreSQL pgAdmin](https://www.pgadmin.org/download/) locally.
- Open pgAdmin and connect to your local Postgres instance.
- Open a new query tool and run the following SQL:
    ```sql
    SELECT * FROM support_services LIMIT 10;
    ```

**Command line:**

```bash
cd backend
psql -U <username> -d <database_name> -h <hostname> -p <port>
SELECT * FROM support_services LIMIT 10;
```

**Start the backend server:**

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

#### Frontend Setup

```bash
cd frontend
npm install
```

**Configure environment variables:**

```bash
# frontend/.env
NUXT_PUBLIC_API_BASE=http://localhost:8000
NUXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
```

**Start the development server:**

```bash
npm run dev
```

The app will be available at `http://localhost:3000`.

#### Utility Scripts

**Convert images to webp:**

```bash
cd backend
python -m src.scripts.convert_images_to_webp
```

---

## Usage

Once both servers are running, open your browser and navigate to `http://localhost:3000`.

| Page                | Route              | Description                                                                                                                                                                          |
| ------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Home**            | `/`                | Landing page with an overview of the platform                                                                                                                                        |
| **Find Food Banks** | `/food-banks`      | Interactive map to locate nearby food banks and emergency food relief outlets. Search by suburb or use "Locate Me" for GPS-based results. Supports turn-by-turn directions via OSRM. |
| **Learn More**      | `/learn-more`      | Data visualizations on food insecurity statistics across Victorian LGAs — health outcomes, diet indicators, and cost-of-living data.                                                 |
| **Nutrition Guide** | `/nutrition-guide` | Age-based macronutrient guidance for children and families, with visual portion-size guides.                                                                                         |
| **Get Food**        | `/get-food`        | Curated resources and links for accessing food assistance.                                                                                                                           |

See the full list of available APIs through the [API contract](https://docs.google.com/document/d/157Gx2cOxRReVCb1s5IcyLXWBRx5GuAZPmbPKo-Zvv8U/edit?usp=sharing)

### Running Backend Tests

After any changes to the backend, run the test suite to verify nothing is broken:

```bash
cd backend
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Roadmap

- [x] Landing page
- [x] Interactive food bank map with locations (opening hours, contact info, etc.) and real-time directions
- [x] Interactive body map, food guide, and wellness habits guide page 
- [x] Food insecurity data visualisation by Victorian LGA
- [x] Children nutrition guide with age-based macronutrient breakdowns
- [x] Hidden costs of food insecurities visualisation 
- [x] Backend REST API with SQLite (dev) and PostgreSQL (prod) support
- [x] CI/CD pipeline with GitHub Actions (test on PR, deploy on merge)
- [x] Automated deployment to Vercel (frontend) and Render (backend)
- [ ] Action list
- [ ] Virtual baby for the user to keep track of what children ate

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make** your changes and ensure all tests pass:
   ```bash
   cd backend && pytest tests/ -v --cov=src
   ```
4. **Commit** your changes with a descriptive message:
   ```bash
   git commit -m "feat: add your feature description"
   ```
5. **Push** to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open** a Pull Request against the `underdevelopment` branch

> **Note:** All PRs targeting `underdevelopment` or `main` will automatically trigger the backend test suite via GitHub Actions. Merges to those branches trigger automatic deployments to the respective Vercel environments.

Please follow the existing code style and add/update unit tests as appropriate under `backend/tests/`.

---

## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

```
MIT License

Copyright (c) 2026 Cherebowl Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Contact

**Project:** Cherebowl — FIT5120 Industry Experience Project, Monash University

- 🌐 **Live App:** [cherebowl.vercel.app](https://cherebowl.vercel.app)
- 🐛 **Issues:** [GitHub Issues](https://github.com/TP14-5201/aegis/issues)
- 📧 **Email:** ylii0721@student.monash.edu (Yanghao), dsus0006@student.monash.edu (Dominica), yche0814@student.monash.edu (Yuqing/Chloe), asut0032@student.monash.edu (Archel), rkup0001@student.monash.edu (Rukma), pdha0010@student.monash.edu (Priyank).

<div align="center">

Made with ❤️ by the Cherebowl team · Monash University FIT5120 · Copyright 2026

</div>
