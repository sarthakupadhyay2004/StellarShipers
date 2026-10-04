# STELLAR SHIPERS — Enterprise B2B Sourcing & Export Platform

> **“WHERE TRUST MEETS VALUE.”**
> 
> Production-quality B2B sourcing and export gateway for agro-industrial raw materials, natural fibers, and plant polymers.

---

## 🧱 Technology Stack

- **Backend:** Python 3.10+, Django 5.1 (modular architecture)
- **Frontend:** Django Templates + Tailwind CSS + Custom Design System
- **Database:** SQLite (development) & PostgreSQL-ready (production via dj-database-url)
- **Static Assets:** WhiteNoise with compressed manifest storage
- **Email System:** SMTP notification pipeline with console fallback for local development
- **Security:** CSRF, Honeypot bot trapping, Secure Cookie flags, Clickjacking protection
- **Deployment:** WSGI / Gunicorn / Procfile ready for traditional VPS, Docker, Render, Railway, or Heroku

---

## 🎯 Architecture Overview

STELLAR SHIPERS is strictly a **B2B sourcing and export platform** (not an e-commerce platform):
- **No e-commerce cart, checkout, or retail consumer payment gates.**
- Primary conversion objective: **Request for Quotation (RFQ) Generation** and **Technical Specification Verification**.
- **Specification Integrity Standard**: Uncompromising separation of **Laboratory-Verified Technical Data** (ASTM, ISO, TAPPI) from **Supplier-Reported / Provisional Data** with prominent disclaimer advisories.

### Modular App Structure

`
d:\Projects\StellarShiper\
├── manage.py
├── requirements.txt
├── .env.example
├── Procfile
├── stellar_shipers/            # Project configuration (settings, URLs, WSGI)
├── apps/
│   ├── core/                   # Context processors, sitemaps, system styling, tests
│   ├── products/               # Product catalog, images, documents, verified/provisional specs
│   ├── rfq/                    # B2B RFQ engine, CRM pipeline, validation, email notifications
│   └── pages/                  # Static & CMS content (Home, About, Quality, Services, FAQ, Legal)
├── templates/
│   ├── base.html
│   ├── components/             # Navbar, Footer
│   ├── pages/                  # Home, About, Quality, Services, Contact/RFQ, FAQ, Privacy, Terms
│   ├── products/               # Product List, Technical Data Sheet (Detail)
│   └── rfq/                    # RFQ Form, RFQ Success
├── static/
│   ├── css/styles.css          # Dark charcoal (#0B0F17) + Silver + White palette
│   └── js/main.js              # Spec switcher, mobile menu, FAQ accordions
└── media/                      # Product imagery, TDS documents, customer spec uploads
`

---

## 🚀 Getting Started

### 1. Environment Setup

`ash
# Clone or enter project directory
cd d:\Projects\StellarShiper

# Activate virtual environment
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# or: source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt
`

### 2. Environment Variables

Configure .env (defaults are provided in .env.example):

`ini
DEBUG=True
SECRET_KEY=stellar-shipers-insecure-dev-key-change-in-production-2026!#*
ALLOWED_HOSTS=localhost,127.0.0.1,testserver

# Email settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=STELLAR SHIPERS RFQ Desk <rfq@stellarshipers.com>
ADMIN_NOTIFICATION_EMAIL=admin@stellarshipers.com
`

### 3. Database Migration & Seeding

`ash
# Apply migrations
python manage.py migrate

# Seed database with production fixtures
python manage.py seed_data
`

The seed command creates:
- **Default Superuser**: dmin / stellar2026!
- **Catalog Products**:
  - Industrial Grade Banana Pseudostem Fiber (Grade A)
  - Areca Palm Leaf Raw Material & Natural Sheaths
  - High-Tensile Coconut Coir Geotextile Yarn
- **Categorized FAQs**: Sourcing, Specs, Samples, Logistics, Commercial
- **Sample RFQs**: Demonstrating CRM pipeline stages

### 4. Run Development Server

`ash
python manage.py runserver
`

Visit the platform:
- **Homepage:** http://127.0.0.1:8000/
- **Products Catalog:** http://127.0.0.1:8000/products/
- **Featured Banana Fiber Specs:** http://127.0.0.1:8000/products/banana-fiber/
- **RFQ Submission:** http://127.0.0.1:8000/rfq/
- **Quality & Process (4 Stages):** http://127.0.0.1:8000/quality-process/
- **Admin CRM:** http://127.0.0.1:8000/admin/ (Login: dmin / stellar2026!)

---

## 🧪 Testing Suite

Run all automated unit and integration tests:

`ash
python manage.py test
`

Tests cover:
- All 10 public pages returning HTTP 200
- SEO sitemap (/sitemap.xml) & crawler rules (/robots.txt)
- Specification Integrity (Certified vs Provisional separation)
- RFQ submission, validation, honeypot bot trap, and database storage
- Admin RFQ dashboard, CSV export action, and status transitions

---

## 🛡️ Admin Dashboard Features

Log into /admin/ with dmin / stellar2026!:
- **RFQ Pipeline Management**: Filter by status (NEW, REVIEWING, QUOTED, SAMPLE, etc.), sample request flags, and country.
- **Direct Status Updates**: Change RFQ status directly from the list table.
- **CSV Export Action**: Export selected RFQs to CSV formatted for corporate CRM.
- **Product Management**: Upload technical documents (TDS, COA), multiple images, and configure verified vs provisional parameters.
- **FAQ Management**: Edit and reorder FAQ items by category.

---

---

## 🚢 Deploying to Render (Zero External Database Setup)

The platform is engineered to deploy seamlessly on [Render](https://render.com) with **zero external database dependencies** (no Supabase, AWS RDS, or external PostgreSQL account needed). It runs self-contained SQLite by default and automatically switches to PostgreSQL if a `DATABASE_URL` is provided in the future.

### Method A: Blueprint Deployment (Recommended)

1. Push this repository to **GitHub** or **GitLab**.
2. Go to your [Render Dashboard](https://dashboard.render.com/) and click **New +** → **Blueprint**.
3. Connect your repository. Render will automatically detect [`render.yaml`](file:///d:/Projects/StellarShiper/render.yaml).
4. Click **Apply**. Render will:
   - Provision a free Python web service (`stellar-shipers`).
   - Run [`build.sh`](file:///d:/Projects/StellarShiper/build.sh) (installs packages, gathers static files via WhiteNoise, runs migrations, and seeds the catalog + superuser).
   - Start the service with `gunicorn stellar_shipers.wsgi:application`.
   - Automatically configure HTTPS and CSRF origins.

---

### Method B: Manual Web Service Setup

If you prefer setting up manually without a Blueprint:

1. In Render Dashboard, click **New +** → **Web Service**.
2. Connect your Git repository.
3. Configure the following service settings:
   - **Name:** `stellar-shipers`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn stellar_shipers.wsgi:application`
   - **Plan:** `Free`
4. In the **Environment Variables** section, add:
   | Key | Value | Notes |
   |---|---|---|
   | `PYTHON_VERSION` | `3.10.6` | Ensures compatible Python runtime |
   | `SECRET_KEY` | *(Click "Generate" or enter random string)* | Required Django secret key |
   | `DEBUG` | `False` | Enables production security headers |
   | `ALLOWED_HOSTS` | `.onrender.com,localhost,127.0.0.1` | Permits your Render subdomain |
   | `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Prevents CSRF 403 on RFQ submissions |
   | `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` | Logs RFQs in Render logs (or use SMTP) |
   | `DEFAULT_FROM_EMAIL` | `STELLAR SHIPERS <contact@stellarshipers.com>` | Sender address |
   | `ADMIN_NOTIFICATION_EMAIL` | `contact@stellarshipers.com` | RFQ recipient alert inbox |
5. Click **Create Web Service**.

---

### What Happens During Render Build (`build.sh`)
```bash
==> Installing Python dependencies...
==> Collecting static assets...           # WhiteNoise hashes 130+ production assets
==> Running database migrations...        # Creates self-contained SQLite schema
==> Seeding initial fixtures and admin...  # Populates Grade A Banana Fiber & superuser
==> Build completed successfully!
```

### Accessing Your Deployed Application
- **Public Website:** `https://stellar-shipers.onrender.com/` (or your chosen Render subdomain)
- **RFQ Submission:** `https://stellar-shipers.onrender.com/rfq/`
- **Django Admin & CRM:** `https://stellar-shipers.onrender.com/admin/`
  - **Username:** `admin`
  - **Password:** `stellar2026!`

> [!TIP]
> **Future PostgreSQL / Supabase Integration**:
> When you're ready to scale to a persistent managed PostgreSQL database, simply create your database on Render or Supabase and add the `DATABASE_URL` environment variable (e.g. `postgresql://user:pass@host:5432/dbname`) in the Render dashboard. The platform will automatically connect to PostgreSQL on the next deploy with zero code modifications needed.

