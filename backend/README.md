# Valorant-Wishlist

Project developed for UNIFOR (University of Fortaleza), a RESTful API that allows users to create and manage a wishlist of Valorant in-game items, enabling them to track desired skins and organize their preferred purchases.

## Features

- Create and manage users
- Add items to a user's wishlist
- Update wishlist entries
- Remove wishlist entries
- Create and manage skin reviews
- Retrieve available skins
- Check API health

## Installation:

Inside of `./doc`, there is a installation guide. [installation guide](./doc/INSTALL.md)

## API Endpoints

### Skins

| Method | Route  | Description                 |
| ------ | ------ | --------------------------- |
| GET    | /skins | Returns the available skins |

### Users

| Method | Route            | Description            |
| ------ | ---------------- | ---------------------- |
| POST   | /users           | Creates a new user     |
| GET    | /users/{user_id} | Retrieves a user by ID |
| PATCH  | /users/{user_id} | Updates a user by ID   |

### Wishlist

| Method | Route                         | Description                         |
| ------ | ----------------------------- | ----------------------------------- |
| POST   | /wishlist                     | Adds an item to a user's wishlist   |
| GET    | /wishlist/{user_id}           | Lists all wishlist items for a user |
| PATCH  | /wishlist/{user_id}/{item_id} | Updates a wishlist item             |
| DELETE | /wishlist/{user_id}/{item_id} | Deletes a wishlist item             |

### Reviews

| Method | Route                  | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| POST   | /reviews               | Creates a new review for a skin    |
| GET    | /reviews/skin/{item_id} | Lists all reviews for a skin       |
| GET    | /reviews/user/{user_id} | Lists all reviews by a user        |
| PATCH  | /reviews/{review_id}   | Updates a review                   |
| DELETE | /reviews/{review_id}   | Deletes a review                   |

### Health

| Method | Route         | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | /health-check | Returns the API health status |

## Data Models

### UserCreate

Required fields:

- `user_id`
- `username`
- `email`
- `bio`

Optional fields:

- `display_name`
- `favorite_weapon`

### UserUpdate

Required fields:

- `bio`

Optional fields:

- `username`
- `email`
- `display_name`
- `favorite_weapon`

### UserOut

Returned fields:

- `user_id`
- `username`
- `email`
- `display_name`
- `favorite_weapon`
- `wishlist_count`
- `status`
- `created_at`
- `updated_at`
- `bio`

### WishlistCreate

Required fields:

- `user_id`
- `item_id`

Optional fields:

- `notes`
- `priority` (default: `1`)
- `notify_on_sale` (default: `false`)

### WishlistUpdate

Optional fields:

- `notes`
- `favorite`
- `status`
- `notify_on_sale`
- `priority`

### WishlistOut

Returned fields:

- `user_id`
- `item_id`
- `notes`
- `priority`
- `notify_on_sale`
- `status`
- `created_at`
- `updated_at`
- `weapon_name`
- `skin_name`
- `image`

### ReviewCreate

Required fields:

- `user_id`
- `item_id`
- `rating` (1-5)
- `comment`
- `is_anonymous`

### ReviewOut

Returned fields:

- `review_id`
- `user_id`
- `username`
- `item_id`
- `weapon_name`
- `skin_name`
- `rating`
- `comment`
- `is_anonymous`
- `created_at`
- `updated_at`

## Example Requests

### Create user

```bash
curl -X 'POST' \
  'https://valorant-wishlist.onrender.com/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user-001",
  "username": "test",
  "email": "test@example.com",
  "display_name": "Test",
  "favorite_weapon": "Operator",
  "bio": "Valorant pro player"
}'
```

### Add item to wishlist

```bash
curl -X 'POST' \
  'https://valorant-wishlist.onrender.com/wishlist' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user-001",
  "item_id": "4e459b3b-4dab-934f-1d77-bdbe75b6fcca",
  "notes": "Awesome skin",
  "priority": 2,
  "notify_on_sale": true
}'
```

### Get a user

```bash
curl -X 'GET' \
  'https://valorant-wishlist.onrender.com/users/1' \
  -H 'accept: application/json'
```

### Get a user wishlist

```bash
curl -X 'GET' \
  'https://valorant-wishlist.onrender.com/wishlist/user-001' \
  -H 'accept: application/json'
```

### Update a wishlist item

```bash
curl -X 'PATCH' \
  'https://valorant-wishlist.onrender.com/wishlist/user-001/4e459b3b-4dab-934f-1d77-bdbe75b6fcca' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "notes": "Amazing skin (owned)",
  "favorite": true,
  "status": "acquired",
  "notify_on_sale": false,
  "priority": 0
}'
```

### Update user info

```bash
curl -X 'PATCH' \
  'https://valorant-wishlist.onrender.com/users/user-001' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test",
  "email": "test@example.com",
  "display_name": "Test",
  "favorite_weapon": "Operator",
  "bio": "Updated bios"
}'
```

### Delete a wishlist item

```bash
curl -X 'DELETE' \
  'https://valorant-wishlist.onrender.com/wishlist/user-001/4e459b3b-4dab-934f-1d77-bdbe75b6fcca' \
  -H 'accept: */*'
```

### Health Check

```bash
curl -X 'GET' \
  'https://valorant-wishlist.onrender.com/health-check' \
  -H 'accept: application/json'
```

### Create review

```bash
curl -X 'POST' \
  'https://valorant-wishlist.onrender.com/reviews' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "user-001",
  "item_id": "4e459b3b-4dab-934f-1d77-bdbe75b6fcca",
  "rating": 5,
  "comment": "Best skin in the game!",
  "is_anonymous": false
}'
```

### Get skin reviews

```bash
curl -X 'GET' \
  'https://valorant-wishlist.onrender.com/reviews/skin/4e459b3b-4dab-934f-1d77-bdbe75b6fcca' \
  -H 'accept: application/json'
```

## Responses

The API returns validation errors with a standard error payload when request data is invalid.

## License

This project was developed for academic purposes.
