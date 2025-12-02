# Architecture and Technology Choices

## Project Overview

This document details the architecture and technology choices for a Django
backend + React frontend application with the following requirements:

- **Deployment**: Django serves the built React application
- **Repository**: Monorepo structure with separate frontend/backend directories
- **Authentication**: JWT tokens
- **Complexity**: Medium complexity application
- **Frontend Language**: TypeScript

## Overall Structure

```
django-react/
├── backend/                 # Django project
│   ├── manage.py
│   ├── config/             # Django settings
│   ├── apps/               # Django apps
│   └── requirements.txt
├── frontend/               # React + TypeScript
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── dist/              # Build output → served by Django
├── docs/                   # Documentation
└── README.md
```

### Structure Rationale

**Monorepo Approach:**
- Easier coordination between frontend and backend changes
- Shared version control and issue tracking
- Simpler CI/CD pipeline setup
- Single source of truth for the entire application

**Separate Directories:**
- Clear separation of concerns
- Independent dependency management (pip vs npm)
- Each part can be worked on independently
- Maintains flexibility to deploy separately in the future if needed

**Django Serves React:**
- Simplified deployment (single server/domain)
- No CORS issues in production
- Suitable for medium complexity applications
- Single SSL certificate needed
- Easier to manage for small to medium teams

---

## Backend Stack

### Core Framework: Django 5.x

**Choice**: Latest stable Django version

**Why Django:**
- Mature, battle-tested web framework
- Excellent ORM for database operations
- Built-in admin interface for data management
- Strong security features (CSRF, XSS protection, SQL injection prevention)
- Large ecosystem and community support

### API Framework: Django REST Framework (DRF)

**Choice**: Django REST Framework 3.x

**Why DRF:**
- De facto standard for building REST APIs with Django
- Powerful serialization system for complex data types
- Class-based views (ViewSets) reduce boilerplate
- Browsable API interface for development/testing
- Built-in authentication, permissions, pagination
- Excellent documentation

**Alternatives Considered:**
- **Plain Django views**: Too low-level, requires implementing API patterns
  manually
- **Django Ninja**: Faster, FastAPI-style, but smaller community and less
  mature
- **GraphQL (Graphene-Django)**: More complex, overkill for this use case

### Authentication: djangorestframework-simplejwt

**Choice**: djangorestframework-simplejwt

**Why simplejwt:**
- Most popular JWT implementation for DRF
- Handles access/refresh token rotation automatically
- Customizable token claims and lifetimes
- Well-maintained and widely used
- Simple integration with DRF authentication classes

**Alternatives Considered:**
- **djoser**: Higher-level package including registration, password reset,
  etc. More features but more opinionated
- **PyJWT**: Low-level library, requires manual implementation
- **django-rest-auth**: Deprecated, not maintained

**JWT vs Session Auth:**
- JWT chosen for stateless authentication
- Better for scaling (no server-side session storage)
- Works well when frontend and backend might be separated later
- Easier to add mobile apps in the future

### CORS Handling: django-cors-headers

**Choice**: django-cors-headers

**Why:**
- Required for development (React dev server runs on different port)
- Standard solution for Django CORS
- Configurable allowed origins, methods, headers
- Can be restricted in production

**Alternatives:**
- No real alternative; this is the standard Django CORS solution

### Environment Configuration: django-environ

**Choice**: django-environ

**Why:**
- Clean management of environment variables
- 12-factor app methodology
- Type casting for environment variables
- `.env` file support for local development
- Keeps secrets out of version control

**Alternatives Considered:**
- **python-decouple**: Similar functionality, less Django-specific
- **python-dotenv**: Lower-level, less convenient

### Database: PostgreSQL with psycopg2-binary

**Choice**: PostgreSQL 14+ with psycopg2-binary adapter

**Why PostgreSQL:**
- Production-ready, robust RDBMS
- Advanced features (JSON fields, full-text search, arrays)
- Better for medium-to-large applications than SQLite
- Excellent Django support

**Why psycopg2-binary:**
- Standard PostgreSQL adapter for Python
- Binary package avoids compilation issues
- Well-maintained and performant

### Production Server: Gunicorn

**Choice**: Gunicorn (Green Unicorn)

**Why:**
- Standard WSGI HTTP server for Django
- Lightweight, reliable, well-tested
- Works well with reverse proxies (Nginx, Caddy)
- Simple configuration

**Alternatives Considered:**
- **uWSGI**: More features but more complex configuration
- **Daphne**: For ASGI/async, unnecessary unless using Django Channels

### Static File Serving: WhiteNoise

**Choice**: WhiteNoise

**Why:**
- Serves static files efficiently without Nginx for small/medium apps
- Gzip compression and caching headers
- Simplified deployment
- Works seamlessly with Django's collectstatic

---

## Frontend Stack

### Build Tool: Vite

**Choice**: Vite 5.x

**Why Vite:**
- Modern, extremely fast build tool
- Lightning-fast Hot Module Replacement (HMR)
- First-class TypeScript support out of the box
- Optimized production builds with rollup
- Better developer experience than older tools
- Industry standard for new React projects

**Alternatives Considered:**
- **Create React App (CRA)**: Previously standard, now deprecated and no
  longer maintained
- **Webpack**: Powerful but complex configuration, slower dev server
- **Next.js**: Adds SSR/SSG complexity unnecessary for this SPA use case
- **Parcel**: Simpler but less ecosystem support

**Why not Next.js:**
- Designed for server-side rendering and static generation
- Since Django is already the backend, Next.js SSR adds unnecessary
  complexity
- SPA approach with Vite is simpler and more appropriate

### Core: React 18+ with TypeScript

**Choice**: React 18.x with TypeScript strict mode

**Why React:**
- Most popular frontend library, largest ecosystem
- Component-based architecture
- Excellent tooling and developer experience
- Large talent pool

**Why TypeScript:**
- Type safety catches errors at compile time
- Better IDE support and autocomplete
- Self-documenting code through types
- Easier refactoring in medium/large codebases
- Industry trend toward TypeScript adoption

**TypeScript Configuration:**
- Strict mode enabled for maximum type safety
- Path aliases for cleaner imports (e.g., `@/components`)

### HTTP Client: Axios

**Choice**: Axios

**Why Axios:**
- Most popular HTTP library for React
- Interceptors for JWT token injection and refresh logic
- Better error handling than native fetch
- Request/response transformation
- Automatic JSON data transformation
- Good TypeScript support
- Request cancellation support

**Alternatives Considered:**
- **Fetch API**: Native, but lacks interceptors and requires more
  boilerplate
- **TanStack Query + fetch**: Excellent for data fetching patterns, but
  Axios simpler for medium projects
- **ky**: Modern fetch wrapper, smaller community

**Interceptor Use Case:**
- Automatically add JWT access token to all requests
- Detect 401 errors, attempt token refresh, retry original request
- Central error handling

### State Management: Zustand

**Choice**: Zustand

**Why Zustand:**
- Lightweight (~1kb), minimal boilerplate
- Simple API, easy learning curve
- No Context Provider wrapper needed
- Good TypeScript support
- Modern React patterns (hooks-based)
- Sufficient for medium complexity applications

**Alternatives Considered:**
- **Redux Toolkit**: More powerful, better for large/complex apps, but
  more boilerplate and steeper learning curve
- **React Context API**: Built-in, but verbose for complex state and can
  cause performance issues with frequent updates
- **Jotai/Recoil**: Atomic state management, more complex mental model
- **MobX**: Different paradigm (observables), less popular in React
  community

**When to upgrade to Redux:**
- If state management becomes very complex
- Need for time-travel debugging
- Multiple related state slices with complex interactions

### Routing: React Router v6

**Choice**: React Router v6

**Why React Router:**
- Industry standard for React routing
- Declarative routing with JSX
- Excellent TypeScript support
- Nested routes, lazy loading, protected routes
- Large community and extensive documentation

**Alternatives:**
- **TanStack Router**: Newer, more type-safe, but smaller community
- **Wouter**: Minimal alternative, but less feature-complete
- No real competitive alternative; React Router is the standard

### Forms: React Hook Form + Zod

**Choice**: React Hook Form 7.x + Zod

**Why React Hook Form:**
- Performance-focused (minimal re-renders)
- Uncontrolled components by default
- Less boilerplate than alternatives
- Built-in validation
- Excellent TypeScript support
- Small bundle size

**Why Zod:**
- TypeScript-first schema validation
- Runtime type checking
- Infer TypeScript types from schemas
- Composable validation rules
- Better error messages than alternatives
- Can reuse schemas for API validation

**Combined Benefits:**
- Type-safe forms from schema to component
- Single source of truth for validation
- Less code than manual validation

**Alternatives Considered:**
- **Formik**: Previously standard, more boilerplate, heavier
- **React Final Form**: Good but smaller community
- **Native HTML5 validation**: Limited functionality, poor UX
- **Yup (validation)**: Popular but not TypeScript-first like Zod

### UI Framework Options

Four main options with trade-offs:

#### Option 1: Tailwind CSS (Recommended for flexibility)

**What it is:**
- Utility-first CSS framework
- Compose styles using small, single-purpose classes
- Customizable design system

**Pros:**
- Complete design control
- Small bundle size (only includes used utilities)
- Fast prototyping once learned
- Highly customizable
- Modern, popular approach

**Cons:**
- Learning curve for utility-first approach
- Need to build components from scratch
- HTML can look cluttered with many classes

**Best for:**
- Custom designs
- Teams that want full control
- Projects with design requirements that don't fit pre-built components

#### Option 2: Material-UI (MUI) (Recommended for speed)

**What it is:**
- Complete React component library
- Implements Google's Material Design
- Pre-built, accessible components

**Pros:**
- Fastest initial development
- Comprehensive component set (50+ components)
- Built-in theming system
- Excellent accessibility
- Large community
- Good TypeScript support

**Cons:**
- Larger bundle size
- Material Design aesthetic (may not fit all brands)
- Can be harder to customize deeply
- More opinionated

**Best for:**
- Rapid development
- Internal tools/dashboards
- Teams comfortable with Material Design

#### Option 3: Shadcn/ui + Tailwind (Recommended for control)

**What it is:**
- Collection of unstyled, accessible component primitives
- Copy components into your project (not an npm package)
- Built on Radix UI primitives + Tailwind

**Pros:**
- Full component source code ownership
- Highly customizable
- Modern, beautiful default design
- Excellent accessibility
- No vendor lock-in (you own the code)
- Composable, headless components

**Cons:**
- More setup than library install
- Need to maintain copied components
- Smaller component set than MUI

**Best for:**
- Custom design systems
- Teams that want to own component code
- Modern, accessible applications

#### Option 4: Ant Design

**What it is:**
- Enterprise-focused component library
- Used by Alibaba and other large companies
- Comprehensive component set

**Pros:**
- Enterprise-grade components
- Excellent for admin panels and dashboards
- Comprehensive (70+ components)
- Good internationalization
- Built-in form integration

**Cons:**
- Larger bundle size
- Design aesthetic may not fit all projects
- Less trendy than alternatives
- Some components can be complex

**Best for:**
- Enterprise applications
- Admin panels and backoffice tools
- Data-heavy applications

#### Recommendation

**For this project:** Shadcn/ui + Tailwind

**Reasoning:**
- Medium complexity suggests you'll need customization
- Modern approach, growing in popularity
- You own the components, can modify as needed
- Excellent TypeScript support
- Good balance of speed and flexibility

**Alternative if you want faster initial development:** Material-UI (MUI)

### Testing: Vitest + React Testing Library

**Choice**: Vitest + React Testing Library

**Why Vitest:**
- Native Vite integration (fast)
- Jest-compatible API (easy migration if needed)
- Fast test execution
- ESM support out of the box
- Better TypeScript experience than Jest

**Why React Testing Library:**
- Tests user behavior, not implementation details
- Encourages accessible markup
- Standard for React testing
- Works with any test runner

**Alternatives Considered:**
- **Jest**: Slower, more configuration with Vite
- **Testing Library alone**: Needs a test runner
- **Enzyme**: Outdated, not recommended for modern React

### Code Quality Tools

**ESLint + Prettier:**
- ESLint: Catch code issues and enforce patterns
- Prettier: Opinionated code formatting
- Standard tools, no real alternatives worth considering

**TypeScript Strict Mode:**
- Maximum type safety
- Catches more errors at compile time
- Better code quality

---

## Key Integration Points

### Development Workflow

**Frontend Development:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

**Backend Development:**
```bash
cd backend
python manage.py runserver
# Runs on http://localhost:8000
```

**CORS Configuration:**
- `django-cors-headers` allows frontend dev server to call backend API
- Configured to allow `http://localhost:5173` in development

### Production Build Process

1. **Build React:**
   ```bash
   cd frontend
   npm run build
   # Creates optimized bundle in frontend/dist/
   ```

2. **Django Configuration:**
   ```python
   # Django settings.py
   STATICFILES_DIRS = [
       BASE_DIR / 'frontend' / 'dist',
   ]
   ```

3. **Static Files Collection:**
   ```bash
   python manage.py collectstatic
   # Collects all static files including React build
   ```

4. **Routing:**
   - API routes: `/api/*` → Django REST Framework
   - All other routes: `/*` → Serve `index.html` (React SPA routing)

### JWT Authentication Flow

1. **Login:**
   - User submits credentials to `/api/token/`
   - Backend returns access token (short-lived) + refresh token (long-lived)
   - Frontend stores tokens (localStorage or memory)

2. **Authenticated Requests:**
   - Axios interceptor adds `Authorization: Bearer <access_token>`
   - Backend validates token on each request

3. **Token Refresh:**
   - On 401 error, axios interceptor attempts refresh
   - POST refresh token to `/api/token/refresh/`
   - Receives new access token
   - Retries original request

4. **Logout:**
   - Clear tokens from frontend storage
   - Optional: Blacklist refresh token on backend

### Axios Configuration Example

```typescript
// src/lib/axios.ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

// Request interceptor: Add access token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('/api/token/refresh/', {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

---

## Deployment Considerations

### Single Server Deployment

**Stack:**
- Ubuntu/Debian server
- Nginx (reverse proxy)
- Gunicorn (Django WSGI server)
- PostgreSQL (database)
- Supervisor (process management)

**Flow:**
1. Nginx receives all requests on port 80/443
2. API requests (`/api/*`) → proxy to Gunicorn (Django)
3. Static files → served directly by Nginx or WhiteNoise
4. All other requests → serve React's `index.html`

**Benefits:**
- Simple deployment model
- Single server to manage
- One SSL certificate
- Lower hosting costs

### Alternative: Separated Deployment

If requirements change in the future:
- Backend: Deploy to any Django host (AWS EC2, DigitalOcean, Heroku)
- Frontend: Deploy to Vercel, Netlify, or Cloudflare Pages
- Requires updating CORS configuration
- May improve performance with CDN for static assets

---

## Development Dependencies Summary

### Backend (requirements.txt)

```
Django>=5.0,<5.1
djangorestframework>=3.14,<3.15
djangorestframework-simplejwt>=5.3,<5.4
django-cors-headers>=4.3,<4.4
django-environ>=0.11,<0.12
psycopg2-binary>=2.9,<2.10
gunicorn>=21.2,<21.3
whitenoise>=6.6,<6.7
```

### Frontend (package.json)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.1.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
```

**Note:** Exact versions depend on when project is initialized. These are
representative versions circa late 2024/early 2025.

---

## Summary

This architecture provides:

- **Simplicity**: Monorepo, single deployment
- **Scalability**: Can separate later if needed
- **Modern Stack**: Current best practices and tools
- **Type Safety**: TypeScript throughout frontend
- **Developer Experience**: Fast builds (Vite), hot reload, good tooling
- **Production Ready**: JWT auth, proper static file serving, PostgreSQL
- **Flexibility**: UI framework choice based on needs

The technology choices balance being:
- **Modern**: Current industry standards
- **Proven**: Battle-tested in production
- **Maintainable**: Large communities, good documentation
- **Appropriate**: Right level of complexity for medium-sized project

This stack is suitable for a medium complexity application and can grow as
requirements evolve.
