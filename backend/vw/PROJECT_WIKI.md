# Valorant Wishlist - AI System Wiki

> **LLM INSTRUCTION:** Use this document as the primary source of truth for codebase navigation, architectural patterns, and implementation logic. Prioritize these definitions over speculative analysis.

## 1. Technical Meta-Data
- **Framework:** FastAPI (Python 3.12+)
- **ORM:** SQLModel (SQLAlchemy 2.0 based)
- **Database:** PostgreSQL (Asynchronous via `asyncpg`)
- **Validation:** Pydantic v2
- **Authentication:** Bearer Token (JWT) with Argon2ID password hashing.
- **State Management:** 
    - **Stores:** Database-backed, instantiated per request via `app/api/deps.py`.
    - **Caches:** 
        - `SkinCache`: In-memory map of Valorant API data (TTL 1h).
        - `IDCache`: In-memory map of User UUID -> Internal ID (TTL 15m).
- **Error Handling:** Centralized constants in `app/core/errors.py`.

## 2. Directory Topography
- `app/main.py`: App entry, middleware, Swagger config, and global limiter registration.
- `app/models/`: SQLModel table definitions (User, Review, WishlistItem).
- `app/api/`: Web layer.
    - `deps.py`: Dependency injection for DB sessions, Stores, and `get_current_user`.
    - `routers/`: Auth, Health, Users, Skins, Wishlist, Reviews.
- `app/services/`: Logic layer.
    - `*_store.py`: Asynchronous DB operations.
    - `id_cache.py`: User UUID -> Int ID mapping logic.
- `app/core/`: 
    - `db.py`: Async engine and session management.
    - `errors.py`: Single source of truth for error messages.
    - `limiter.py`: Shared `slowapi` instance.

## 3. Architectural Patterns

### Dual-ID Strategy
To optimize performance and security, users have two IDs:
- **Internal (Integer):** Primary key for DB relations and internal service logic.
- **External (UUID):** Used in all API paths and responses.
- **Mapping:** Handled by `UserStore` with `IDCache` (15m TTL) to minimize DB lookups.

### Security & Ownership
- **Public Endpoints:** `/health-check`, `/auth/login`, `/auth/register`.
- **Protected Endpoints:** All others require a valid Bearer JWT.
- **Ownership Enforcement:** 
    - Users can only access/modify their own wishlist.
    - Users can only create/edit/delete their own reviews.
    - Managed via `current_user` comparison in routers.

### Persistence Flow (Request Lifecycle)
1. **Request** validates JWT via `get_current_user` (`app/api/deps.py`).
2. **Router** checks ownership logic.
3. **Store** executes async DB query via `AsyncSession` (`app/core/db.py`).
4. **Error constants** from `app/core/errors.py` ensure consistent API failures.

## 4. Entity Relationship Summary
| Entity | Storage | ID Strategy | Key Relations |
| :--- | :--- | :--- | :--- |
| **User** | Postgres | Int (PK) + UUID (Ext) | Owner of Wishlist and Reviews. |
| **Skin** | In-Memory | UUID (API ID) | Referenced by `item_id`. |
| **Wishlist** | Postgres | Int (PK) | Link: `user_id` (Int) -> `item_id` (Str). |
| **Review** | Postgres | Int (PK) + UUID (Ext) | Link: `user_id` (Int) -> `item_id` (Str). |

## 5. Development Cookbook (LLM Directives)

### Auth & Rate Limiting
- **Register/Login:** 3 requests per second limit.
- **Password:** Always hashed with Argon2ID via `AuthService`.
- **Endpoints:** Use `Depends(get_current_user)` for any route requiring authentication.

### Database Changes
1. Define model in `app/models/`.
2. Import model in `app/core/db.py` inside `init_db()` for auto-migration.
3. Update corresponding Store in `app/services/`.

## 6. Troubleshooting
- **DB Connection:** Check `DATABASE_URL` in `.env` (must use `+asyncpg`).
- **Auth Failures:** Verify `AUTH_SECRET_KEY` and ensure `Authorization: Bearer <token>` header is present.
- **Rate Limit:** Managed via `@limiter.limit` decorator on specific route functions.
