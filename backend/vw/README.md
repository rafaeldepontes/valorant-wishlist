# Valorant Wishlist - Core API

The Core API service for the Valorant Wishlist platform. This service manages the skin catalog, user profiles, wishlists, and community reviews.

## Features

- **Skin Catalog**: Search and retrieve the full database of Valorant skins.
- **User Profiles**: Manage agent identities, bios, and favorite weapons.
- **Wishlist Management**: Real-time tracking of desired items with priority and status updates.
- **Community Reviews**: Share and browse community feedback for all in-game items.
- **Health Monitoring**: Standardized health check endpoints.

## Setup & Installation

Detailed installation instructions can be found in the [Installation Guide](./doc/INSTALL.md).

### Quick Start
1. Ensure PostgreSQL is running.
2. Configure your .env file based on .env.example.
3. Install dependencies: pip install -r requirements.txt.
4. Run the server: uvicorn app.main:app --reload.

## API Endpoints

### Skins
| Method | Route | Description |
| :--- | :--- | :--- |
| GET | /skins | Returns a paginated list of available skins |

### Users
| Method | Route | Description |
| :--- | :--- | :--- |
| GET | /users | Lists all agents (paginated) |
| GET | /users/me | Retrieves the authenticated user's profile |
| GET | /users/{user_id} | Retrieves a specific agent's profile by UUID |
| PATCH | /users/{user_id} | Updates agent profile info (Bio, Display Name, etc.) |

### Wishlist
| Method | Route | Description |
| :--- | :--- | :--- |
| POST | /wishlist | Adds a new item to the user's wishlist |
| GET | /wishlist/{user_id} | Lists all wishlist items for a specific user |
| PATCH | /wishlist/{user_id}/{item_id} | Updates a wishlist item (Notes, Status, Priority) |
| DELETE | /wishlist/{user_id}/{item_id} | Removes an item from the wishlist |

### Reviews
| Method | Route | Description |
| :--- | :--- | :--- |
| POST | /reviews | Submits a new community review for a skin |
| GET | /reviews/skin/{item_id} | Lists all reviews for a specific skin |
| GET | /reviews/user/{user_id} | Lists all reviews submitted by a specific user |
| PATCH | /reviews/{review_id} | Updates an existing review |
| DELETE | /reviews/{review_id} | Deletes a review |

## Data Models

### UserOut
- user_id: UUID string
- username: Unique identifier
- display_name: Agent's public name
- favorite_weapon: Highlighted weapon
- wishlist_count: Number of items in wishlist
- bio: Agent biography

### WishlistOut
- user_id: Owner's UUID
- item_id: Skin UUID
- notes: Personal notes
- priority: Numeric priority (0-3)
- status: Tracking status (e.g., "watching", "acquired")
- skin_name: Human-readable name
- image: URL to skin asset

### ReviewOut
- review_id: Review UUID
- username: Author's name
- rating: 1-5 star rating
- comment: Review text
- is_anonymous: Privacy flag

## License
Developed for academic purposes at the University of Fortaleza (UNIFOR).
