# Django-React Project

## Project Overview

This is a Django backend + React frontend application with JWT authentication.
The project uses a monorepo structure where Django serves the built React
application.

- **Architecture**: Django REST API backend serving React SPA frontend
- **Authentication**: JWT tokens (access + refresh)
- **Complexity**: Medium complexity application
- **Frontend Language**: TypeScript

---

## Project Structure

```
django-react/
├── backend/                 # Django project
│   ├── manage.py
│   ├── config/             # Django settings and configuration
│   ├── apps/               # Django apps
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment (not in git)
├── frontend/               # React + TypeScript application
│   ├── src/               # React source code
│   ├── public/            # Static assets
│   ├── dist/              # Build output (served by Django)
│   ├── package.json       # Node dependencies
│   └── node_modules/      # Node packages (not in git)
├── docs/                   # Project documentation
│   └── CHOICES.md         # Detailed technology choice rationale
├── CLAUDE.md              # This file
└── README.md              # Project readme
```

---

## Technology Stack

### Backend

- **Django 5.x**: Web framework
- **Django REST Framework (DRF)**: REST API framework
- **djangorestframework-simplejwt**: JWT authentication
- **django-cors-headers**: CORS handling for development
- **django-environ**: Environment variable management
- **PostgreSQL**: Database (via psycopg2-binary)
- **Gunicorn**: Production WSGI server
- **WhiteNoise**: Static file serving

### Frontend

- **React 18+**: UI library
- **TypeScript**: Type-safe JavaScript (strict mode)
- **Vite**: Build tool and dev server
- **React Router v6**: Client-side routing
- **Axios**: HTTP client with interceptors for JWT
- **Zustand**: State management
- **React Hook Form**: Form handling
- **Zod**: Schema validation
- **Shadcn/ui + Tailwind CSS**: UI components and styling
- **Vitest**: Testing framework
- **React Testing Library**: Component testing
- **ESLint + Prettier**: Code linting and formatting

---

## Python Environment

### Virtual Environment

**Environment name**: `django-react`

**Activation**:
```bash
pyenv activate django-react
```

### Dependency Management

**Installing packages**:
```bash
pip install package-name
```

**IMPORTANT**: All installed packages MUST be added to `requirements.txt`:
```bash
pip freeze > backend/requirements.txt
```

Or manually add with version to `backend/requirements.txt`:
```
package-name>=X.Y,<X.Z
```

### Code Formatting

**All Python code must be formatted with Black immediately after writing.**

**Format a file**:
```bash
black path/to/file.py
```

**Format entire backend**:
```bash
black backend/
```

**Black configuration** (if needed, create `pyproject.toml`):
```toml
[tool.black]
line-length = 94
target-version = ['py311']
```

---

## Development Workflow

### Backend Development

**Start Django dev server**:
```bash
cd backend
python manage.py runserver
# Runs on http://localhost:8000
```

**Run migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

**Create superuser**:
```bash
python manage.py createsuperuser
```

**Run tests**:
```bash
python manage.py test
```

### Frontend Development

**Install dependencies**:
```bash
cd frontend
npm install
```

**Start dev server**:
```bash
npm run dev
# Runs on http://localhost:5173
```

**Build for production**:
```bash
npm run build
# Creates optimized bundle in frontend/dist/
```

**Run tests**:
```bash
npm test
```

**Lint and format**:
```bash
npm run lint
npm run format
```

---

## Integration Points

### Development

- **Frontend dev server**: `http://localhost:5173` (Vite)
- **Backend API**: `http://localhost:8000` (Django)
- **CORS**: Enabled for `localhost:5173` in development via
  `django-cors-headers`

### Production

1. React build output (`frontend/dist/`) is served as static files by Django
2. Django `STATICFILES_DIRS` includes `frontend/dist/`
3. API routes: `/api/*` → Django REST Framework
4. All other routes: `/*` → Serve `index.html` (React handles routing)

---

## Authentication Flow

### JWT Implementation

1. **Login**:
   - POST credentials to `/api/token/`
   - Receive access token (short-lived) + refresh token (long-lived)
   - Store tokens in frontend (localStorage or memory)

2. **Authenticated Requests**:
   - Axios interceptor adds `Authorization: Bearer <access_token>` header
   - Backend validates token on each request

3. **Token Refresh**:
   - On 401 response, axios interceptor attempts refresh
   - POST refresh token to `/api/token/refresh/`
   - Receive new access token
   - Retry original request
   - If refresh fails, redirect to login

4. **Logout**:
   - Clear tokens from frontend storage
   - Optional: Blacklist refresh token on backend

---

## File Organization

### Backend Structure

```
backend/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py           # Root URL configuration
│   ├── wsgi.py           # WSGI config
│   └── asgi.py           # ASGI config
├── apps/                  # Django applications
│   ├── users/            # User management
│   ├── api/              # API endpoints
│   └── ...               # Other apps
├── static/               # Static files (after collectstatic)
├── media/                # User-uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/       # Reusable React components
│   ├── pages/           # Page components (route handlers)
│   ├── lib/             # Utilities (axios config, etc.)
│   ├── stores/          # Zustand stores
│   ├── types/           # TypeScript type definitions
│   ├── hooks/           # Custom React hooks
│   ├── App.tsx          # Root component
│   └── main.tsx         # Entry point
├── public/              # Static assets
├── dist/                # Build output (generated)
├── index.html           # HTML template
├── package.json         # Node dependencies and scripts
├── tsconfig.json        # TypeScript configuration
├── vite.config.ts       # Vite configuration
└── tailwind.config.js   # Tailwind CSS configuration
```

---

## Environment Variables

### Backend (.env)

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# CORS (development)
CORS_ALLOWED_ORIGINS=http://localhost:5173

# JWT
ACCESS_TOKEN_LIFETIME=5  # minutes
REFRESH_TOKEN_LIFETIME=1 # days
```

### Frontend (.env)

```bash
VITE_API_URL=/api  # Relative URL in production
```

---

## Coding Standards

### Python

- **Formatting**: Black with 94 character line length (per global CLAUDE.md)
- **Docstrings**: First line max 80 characters
- **Line length**: Max 94 characters
- **Style**: Follow PEP 8
- **Type hints**: Use where beneficial

### TypeScript/React

- **Line length**: Max 94 characters
- **Formatting**: Prettier
- **Linting**: ESLint
- **Naming**:
  - Components: PascalCase
  - Files: kebab-case or PascalCase for components
  - Functions/variables: camelCase
- **Imports**: Use path aliases (e.g., `@/components`)

---

## Testing

### Backend

```bash
python manage.py test
```

- Use Django's TestCase for model/view tests
- Use DRF's APITestCase for API endpoint tests
- Test authentication, permissions, serialization

### Frontend

```bash
npm test
```

- Vitest for unit tests
- React Testing Library for component tests
- Test user interactions, not implementation details
- Mock API calls with axios-mock-adapter or MSW

---

## Deployment

### Build Process

1. **Build frontend**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Collect static files**:
   ```bash
   cd backend
   python manage.py collectstatic --noinput
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start Gunicorn**:
   ```bash
   gunicorn config.wsgi:application
   ```

### Production Checklist

- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set secure `SECRET_KEY`
- [ ] Configure HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Configure static file serving (WhiteNoise or Nginx)
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring

---

## Common Commands

### Backend

```bash
# Activate virtual environment
pyenv activate django-react

# Install dependencies
pip install -r backend/requirements.txt

# Create new Django app
cd backend
python manage.py startapp appname

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Format code with Black
black backend/

# Run tests
python manage.py test
```

### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

---

## Key Files

### Backend Configuration

- `backend/config/settings.py`: Django settings (database, apps, middleware)
- `backend/config/urls.py`: URL routing
- `backend/requirements.txt`: Python dependencies

### Frontend Configuration

- `frontend/package.json`: Dependencies and scripts
- `frontend/vite.config.ts`: Vite build configuration
- `frontend/tsconfig.json`: TypeScript compiler options
- `frontend/tailwind.config.js`: Tailwind CSS configuration
- `frontend/src/lib/axios.ts`: Axios instance with interceptors

---

## Notes

- The project uses a monorepo structure for easier development
- Django serves the built React application in production
- CORS is only needed for development (different ports)
- JWT tokens provide stateless authentication
- Frontend routing is handled by React Router
- Backend routing handles API endpoints only
- All Python code must be formatted with Black
- All dependencies must be tracked in requirements.txt


## 🚨 MANDATORY POST-CODE-CHANGE TESTING AND COMMIT 🚨

**STOP! BEFORE ANYTHING ELSE, READ THIS:**

After ANY code changes in this repository, you MUST IMMEDIATELY follow the
appropriate workflow below:

---

### For Python/Backend Changes

After ANY code changes to Python files, you MUST IMMEDIATELY:

1. **RUN BLACK FORMATTER:**
   ```bash
   black <modified_file.py>
   ```

2. **RUN TESTS (if applicable):**
   ```bash
   cd backend
   python manage.py test
   ```

   If tests fail, FIX THE ISSUES before committing.

3. **UPDATE REQUIREMENTS (if new packages were installed):**
   If you installed any new Python packages via pip install, you MUST add
   them to:
   ```bash
   # Add the new package to requirements/deploy.txt
   echo "package_name==version" >> requirements/deploy.txt
   ```

   Always specify exact versions to ensure reproducible deployments.

4. **CREATE GIT COMMIT:**
   After completing the above steps, AUTOMATICALLY create a git commit with
   this EXACT format:
   ```
   ...CLAUDE - <one line summary>

   ---- prompt ----
   <complete user prompt>

   ---- summary ----
   <helpful summary and description of the changes>
   ```

   **COMMIT FORMAT REQUIREMENTS:**
   - The first line MUST start with three dots: `...CLAUDE -`
   - Include the COMPLETE original user prompt
   - If the user interrupts (Esc) and adds additional instructions, combine
     ALL prompts separated by a single empty line
   - Preface additional prompts with "Additional:"
   - Provide a detailed summary of changes made

---

### For React/Frontend Changes

After ANY code changes to TypeScript/React files, you MUST IMMEDIATELY:

1. **RUN PRETTIER FORMATTER:**
   ```bash
   cd frontend
   npm run format
   ```

   Or for specific files:
   ```bash
   npx prettier --write <modified_file.tsx>
   ```

2. **RUN ESLINT:**
   ```bash
   cd frontend
   npm run lint
   ```

   If linting errors are found, FIX THEM before committing.

3. **RUN TYPE CHECK:**
   ```bash
   cd frontend
   npm run type-check
   ```

   Or if type-check script doesn't exist:
   ```bash
   npx tsc --noEmit
   ```

   If type errors are found, FIX THEM before committing.

4. **RUN TESTS (if applicable):**
   ```bash
   cd frontend
   npm test
   ```

   If tests fail, FIX THE ISSUES before committing.

5. **UPDATE PACKAGE.JSON (if new packages were installed):**
   If you installed any new npm packages, they should AUTOMATICALLY be added
   to package.json and package-lock.json. Verify:
   ```bash
   git status
   # Should show package.json and package-lock.json as modified
   ```

   **IMPORTANT**: Always use exact versions or ^ for dependencies:
   - Use `npm install package-name` (adds ^ by default)
   - For exact versions: `npm install package-name@x.y.z --save-exact`

   **ALWAYS commit both package.json AND package-lock.json together.**

6. **CREATE GIT COMMIT:**
   After completing the above steps, AUTOMATICALLY create a git commit with
   this EXACT format:
   ```
   ...CLAUDE - <one line summary>

   ---- prompt ----
   <complete user prompt>

   ---- summary ----
   <helpful summary and description of the changes>
   ```

   **COMMIT FORMAT REQUIREMENTS:**
   - The first line MUST start with three dots: `...CLAUDE -`
   - Include the COMPLETE original user prompt
   - If the user interrupts (Esc) and adds additional instructions, combine
     ALL prompts separated by a single empty line
   - Preface additional prompts with "Additional:"
   - Provide a detailed summary of changes made

---

### For Changes Affecting Both Backend and Frontend

If you make changes to BOTH Python and React files in a single task:

1. **Follow BOTH workflows above** (Python steps + React steps)
2. **Create a SINGLE commit** that includes all changes
3. **In the commit summary**, clearly indicate both backend and frontend
   were modified

---

### Summary Checklist

Before EVERY commit, ensure you have:

**Backend (if Python files changed):**
- [ ] Ran Black formatter
- [ ] Ran tests (if applicable)
- [ ] Updated requirements/deploy.txt (if packages installed)

**Frontend (if React/TS files changed):**
- [ ] Ran Prettier formatter
- [ ] Ran ESLint
- [ ] Ran TypeScript type check
- [ ] Ran tests (if applicable)
- [ ] Committed package.json + package-lock.json (if packages installed)

**Always:**
- [ ] Created git commit with proper `...CLAUDE -` format
- [ ] Included complete user prompt in commit message
- [ ] Provided detailed summary of changes

---

**NO EXCEPTIONS. NO EXCUSES. ALWAYS RUN THESE CHECKS AND CREATE THE
COMMIT.**

If you fail to run these checks and create the commit after code changes,
you are violating the core requirements of this project. The user should
not have to remind you. This is MANDATORY and AUTOMATIC.

