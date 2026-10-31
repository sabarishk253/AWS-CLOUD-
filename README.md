# EduCloud: AI-Powered Student Document and Assignment Management System

**EduCloud** is a functional, full-stack, on-premise SaaS academic document and assignment management platform designed for colleges and universities. It streamlines student coursework submissions, assignment lifecycles, smart deadline tracking, faculty grading with qualitative feedback, and automated on-device AI document classification and summarization.

---

## 🏛️ System Architecture & Data Sovereignty

EduCloud is engineered under strict **Data Sovereignty** principles:
- **Frontend Hosting:** AWS Amplify is used **ONLY** to build and serve the static React/Vite single-page application.
- **Backend & AI Engine:** Runs locally on your own computer or private server using FastAPI and Python.
- **Local Database:** Application records are stored in a local SQLite database at `backend/data/educloud.db`.
- **Local File Storage:** Uploaded student documents are stored directly on your local computer at `backend/local_storage/<user_id>/<assignment_id>/<generated_file_uuid>.<ext>`.
- **No Cloud Database / Storage Lock-in:** **Zero** Amazon S3, DynamoDB, AWS AppSync, or Amazon RDS dependencies are used. All documents and student data remain under your direct control.

```
┌────────────────────────────────────────────────────────────────────────┐
│                          EduCloud Architecture                         │
└────────────────────────────────────────────────────────────────────────┘

 [ AWS Amplify Hosting ]
         │
         ▼
  React + Vite Frontend (SPA)
         │  (Authenticated REST API / JWT)
         ▼
 ┌───────────────────────────────────────────────────────────────────────┐
 │                   Local Host / Private Server                         │
 │                                                                       │
 │   ┌───────────────────────┐         ┌─────────────────────────────┐   │
 │   │   FastAPI Backend     │◄───────►│  Local AI Processing Engine │   │
 │   │   (Uvicorn / Python)  │         │  (scikit-learn / PyMuPDF)   │   │
 │   └──────────┬────────────┘         └─────────────────────────────┘   │
 │              │                                                        │
 │      ┌───────┴──────────────┐                                         │
 │      ▼                      ▼                                         │
 │ ┌───────────────┐   ┌───────────────────────────────────────────────┐ │
 │ │ SQLite DB     │   │ Local Disk Storage (Structured Directory)     │ │
 │ │ (educloud.db) │   │ backend/local_storage/<user>/<assign>/<uuid>  │ │
 │ └───────────────┘   └───────────────────────────────────────────────┘ │
 └───────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

### 1. Multi-Tier Role-Based Access Control (RBAC)
- **Student:** View enrolled courses and deadlines, upload assignments, inspect AI classification and extractive summaries, download submitted files, monitor version history, and view teacher feedback and grades.
- **Teacher (Faculty):** Create and configure assignments (deadlines, allowed formats, max marks, late submission rules), review student submissions, download student files, provide numeric marks and written qualitative feedback.
- **Administrator:** System-wide governance, user provisioning (Students, Teachers, Admins), activate/deactivate accounts, change user roles, monitor local storage usage, and inspect real-time security audit trails.
- *Public self-registration strictly permits Student and Teacher roles only; Administrator accounts are guarded by privileged provisioning.*

### 2. Local AI Document Processing
- **AI Document Classification:** Powered by a scikit-learn TF-IDF + Multinomial Naive Bayes pipeline trained on an educational corpus. Classifies documents into:
  - `Assignment`
  - `Project report`
  - `Certificate`
  - `Research paper`
  - `Notes`
  - `Other`
  - *Includes real confidence score estimation and allows students/teachers to manually correct predicted categories (recorded in audit logs).*
- **AI Document Summarization:** Lightweight on-device extractive summarization generating an executive summary paragraph, bulleted key highlights, and top domain keywords.
- **Scanned Document Detection:** Heuristic scanner detects image-based or rasterized PDFs and warns users that an Optical Character Recognition (OCR) pipeline is needed rather than hallucinating text.

### 3. Smart Deadline Management & Notifications
- Live indicators for **Due Soon** (< 72 hours), **Urgent** (< 24 hours with visual pulse), and **Overdue** assignments.
- Automated server-side validation tags submissions as **On-Time** vs **Late**.
- In-app notification center alerts faculty when submissions arrive and alerts students when feedback is published.

### 4. Version Control & Resubmission Management
- When a student resubmits an assignment, EduCloud does **not** overwrite the prior file.
- It increments the active version number (`v1`, `v2`, `v3`) while preserving all prior files and database metadata for auditing and review.

### 5. File Integrity, Security & Duplicate Detection
- **SHA-256 Hashing:** Automatically computes cryptographic checksums for uploaded files to detect identical uploads.
- **File Signature (Magic Bytes) Verification:** Validates true file byte headers to prevent renamed executable binaries (`.exe`, `.bat`, `.sh`) disguised as PDFs.
- **Path Traversal Guards:** Resolves canonical paths to ensure files are strictly confined to `backend/local_storage/`.
- **Authenticated Downloads:** Strict server-enforced permission checks ensure students cannot download other students' confidential files.

---

## 🔑 Demo User Credentials

The database seed script initializes the following demonstration accounts:

| Role | Email Address | Password | Description |
|---|---|---|---|
| **Administrator** | `admin@educloud.local` | `Admin@123456` | System Administrator (Full Access) |
| **Faculty / Teacher** | `prof.sharma@educloud.local` | `Teacher@123456` | Prof. Rajesh Sharma (CS Department) |
| **Faculty / Teacher** | `dr.patel@educloud.local` | `Teacher@123456` | Dr. Priya Patel (Data Science Department) |
| **Student** | `rahul.verma@educloud.local` | `Student@123456` | Rahul Verma (6th Semester CS) |
| **Student** | `ananya.singh@educloud.local` | `Student@123456` | Ananya Singh (6th Semester CS) |

*The login page also provides one-click autofill buttons for these demo accounts.*

---

## ⚡ Quick Start: Zero-Command One-Click Execution

You do not need to manually open the command prompt or type commands:

### Option 1: Double-Click the HTML File
1. In Windows File Explorer, double-click **`Launch_EduCloud.html`** (or **`index.html`**).
2. The Launch Portal will open in your browser, test server connectivity, and auto-redirect to the application.

### Option 2: One-Click Launcher (`Run_EduCloud.bat`)
1. In Windows File Explorer, double-click **`Run_EduCloud.bat`** (or **`Run_EduCloud_Silent.vbs`** for silent background execution).
2. It automatically sets up the environment, seeds the SQLite database, starts the unified server on `http://127.0.0.1:8000`, and opens your default browser!

---

## ☁️ Deploy to AWS Amplify (Instant Drag & Drop ZIP)

You can host EduCloud on AWS Amplify without connecting a Git repository:
1. Locate **`amplify_deploy.zip`** in the root of this project.
2. Open [AWS Amplify Console](https://console.aws.amazon.com/amplify).
3. Click **Create new app** &rarr; **Deploy without Git provider**.
4. Enter App name: `EduCloud`, Branch: `main`.
5. Drag and drop **`amplify_deploy.zip`** into the upload area.
6. Click **Save and deploy**. Your website is live with HTTPS and global CDN in ~15 seconds!
*(To re-generate this zip anytime after making code changes, simply run `python package_amplify.py` or double-click `package_amplify.py`)*

---

## 💻 Manual Developer Guide (Command Line)

### Prerequisites
- Python 3.10+ (Python 3.12 verified)
- Node.js 18+ and npm

### Step 1: Clone or Navigate to the Project Directory
```powershell
cd "c:\Users\krish\OneDrive\Documents\project aws"
```

### Step 2: Set Up Backend Virtual Environment
```powershell
# Create Python virtual environment
python -m venv backend/.venv

# Activate virtual environment
backend\.venv\Scripts\Activate.ps1
# (or in CMD: backend\.venv\Scripts\activate.bat)

# Install Python dependencies
backend\.venv\Scripts\pip.exe install -r backend\requirements.txt
```

### Step 3: Initialize & Seed the SQLite Database
```powershell
# Run the database seeder to create sample courses, users, assignments & submissions
backend\.venv\Scripts\python.exe backend\seed.py
```

### Step 4: Run Backend API & AI Engine
```powershell
# Start FastAPI with Uvicorn on port 8000
backend\.venv\Scripts\uvicorn.exe app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
*The API will be available at: `http://127.0.0.1:8000` (Interactive docs: `http://127.0.0.1:8000/docs`)*

### Step 5: Start the React Frontend (in a separate terminal)
```powershell
cd frontend

# Install npm dependencies (if not already installed)
npm install --legacy-peer-deps

# Start Vite development server
npm run dev
```
*The web application will open at: `http://localhost:5173`*

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite covering authentication, RBAC, file storage security, duplicate detection, and AI modules:

```powershell
backend\.venv\Scripts\pytest.exe backend/tests/test_educloud.py -v
```

---

## ☁️ AWS Amplify Frontend Deployment Guide

Only the frontend single-page application is hosted on AWS Amplify. The backend API and local SQLite/storage remain hosted on your private computer/server.

### 1. Build Verification
Before deploying, verify that the frontend builds cleanly:
```powershell
cd frontend
npm run build
```
*(Produces optimized static artifacts in `frontend/dist/`)*

### 2. Connect Repository to AWS Amplify
1. Open the [AWS Amplify Console](https://console.aws.amazon.com/amplify).
2. Click **Host web app** and connect your GitHub repository.
3. Select your repository and `main` branch.
4. AWS Amplify will automatically detect `amplify.yml` at the project root.

### 3. Configure Environment Variables in Amplify
In Amplify Console > **App settings** > **Environment variables**:
- Key: `VITE_API_BASE_URL`
- Value: `https://your-public-backend-url.com` (e.g., via Cloudflare Tunnel, ngrok, or a server with HTTPS)

### 4. Configure Single-Page Application (SPA) Rewrites
In Amplify Console > **App settings** > **Rewrites and redirects**, ensure the standard SPA rewrite rule is present:
- **Source address:** `</^[^.]+$|\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2|ttf|map|json)$)([^.]+$)/>`
- **Target address:** `/index.html`
- **Type:** `200 (Rewrite)`

---

## 📁 Project Directory Structure

```
project aws/
├── amplify.yml                       # AWS Amplify build specification
├── amplify/
│   └── README.md                     # Amplify hosting and rewrite instructions
├── backend/
│   ├── ai/                           # Local AI engine
│   │   ├── classifier.py             # scikit-learn TF-IDF + NB classification & baseline
│   │   ├── summarizer.py             # Extractive summarization & keyword extraction
│   │   ├── document_extractor.py     # PyMuPDF & docx text extractors
│   │   └── models/                   # Cached ML model artifacts
│   ├── app/
│   │   ├── api/                      # REST API endpoints (auth, assignments, submissions, etc.)
│   │   ├── core/                     # Database, security (bcrypt, JWT), and config
│   │   ├── models/                   # SQLAlchemy models (User, Assignment, Submission, etc.)
│   │   ├── schemas/                  # Pydantic serialization & request schemas
│   │   ├── services/                 # Local file storage & audit services
│   │   └── main.py                   # FastAPI application entrypoint
│   ├── data/
│   │   └── educloud.db               # Local SQLite database (Data sovereign)
│   ├── local_storage/                # Local document storage directory
│   ├── tests/
│   │   └── test_educloud.py          # Automated test suite
│   ├── requirements.txt              # Backend dependencies
│   └── seed.py                       # Database seeding script
├── frontend/
│   ├── src/
│   │   ├── components/               # Navbar, Badge, UploadModal, AIModal, FeedbackModal
│   │   ├── context/                  # AuthContext (JWT & session persistence)
│   │   ├── pages/                    # Dashboards (Student, Teacher, Admin), Assignments, etc.
│   │   ├── services/                 # Axios API client
│   │   ├── types/                    # TypeScript data models
│   │   ├── App.tsx                   # Routing & protected role wrappers
│   │   └── index.css                 # Tailwind CSS v4 styling & color tokens
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.app.json
├── .gitignore
└── README.md
```
