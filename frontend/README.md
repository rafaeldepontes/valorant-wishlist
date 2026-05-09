# Valorant-Wishlist Frontend

Project developed for UNIFOR (University of Fortaleza), a web application built with React and Vite that interfaces with the Valorant Wishlist API. It provides a visual and interactive experience for users to manage their desired Valorant skins, track their collection, and share feedback with the community.

## Features

- User authentication and session management
- Searchable skin catalog with client-side pagination
- Real-time wishlist management (add, remove, update status)
- Comprehensive skin review system with community feedback
- Agent profile customization (display name, bio, favorite weapon)
- Responsive UI with specialized Valorant-themed design
- In-app notifications for user actions

## Technologies

- Vite: Build tool and development server
- React: UI library
- TypeScript: Static typing for maintainable code
- Tailwind CSS: Utility-first styling framework
- Axios: Promise-based HTTP client for API communication
- Lucide React: Modern icon set
- React Router DOM: Declarative routing for single-page applications

## Installation

Inside the `./frontend` directory, follow these steps:

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

Ensure the backend API is running at the expected address (default: http://localhost:8000). The Vite configuration includes a proxy to handle CORS during development.

### 3. Start development server

```bash
npm run dev
```

### 4. Build for production

```bash
npm run build
```

## Application Structure

### Pages

| Route | Name | Description |
| --- | --- | --- |
| /login | Login | Authenticate existing users |
| /register | Register | Create new agent accounts |
| / | Skins | Explore the full skin catalog (Protected) |
| /wishlist | Wishlist | Manage personal tracked items (Protected) |
| /profile | Profile | Update agent identity and bio (Protected) |

### Components

- Layout: Consistent wrapper with navigation
- Navbar: Responsive header with auth-aware links and wishlist counter
- SkinCard: Interactive display for individual skins with contextual actions
- ReviewModal: Integrated interface for viewing and submitting reviews
- ReviewList: Community feedback feed for specific items
- Toast: Custom notification system for asynchronous feedback

## Data Flow

The application utilizes React Context (AuthContext) to manage global authentication state and user synchronization. API requests are handled by a modular service layer located in `src/api/services`, ensuring a clean separation between logic and UI.

## License

This project was developed for academic purposes.
