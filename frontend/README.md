# Valorant Wishlist - Frontend

A modern, responsive web application built with React and TypeScript, providing a premium interface for the Valorant community to track skins and share reviews.

## Design Philosophy

The application features a specialized Valorant-themed UI, characterized by:
- Dark, high-contrast color schemes.
- Sharp, aggressive geometric elements.
- Interactive feedback for all user actions.
- Responsive layouts for desktop and tablet agents.

## Key Features

- **Dynamic Catalog**: Browse all available skins with client-side pagination and real-time search.
- **Wishlist Tracking**: Add/remove items and update their status (e.g., "watching", "acquired") directly from the catalog.
- **Community Feed**: View and submit reviews for any skin, with support for anonymous feedback.
- **Agent Profile**: Customize your public identity, including display name, bio, and favorite weapon.
- **Secure Sessions**: Integrated with the Auth API for robust login, registration, and persistent sessions.

## Technology Stack

- **React 18**: Component-based UI library.
- **Vite**: Modern build tool for rapid development.
- **TypeScript**: Ensuring type safety across the entire data layer.
- **Tailwind CSS**: Utility-first styling for the custom Valorant theme.
- **Lucide React**: Clean, consistent iconography.
- **Axios**: Modular API client with interceptors for session management.
- **React Router 6**: Declarative routing with protected route guards.

## Getting Started

### 1. Installation
```bash
npm install
```

### 2. Configuration
Create a .env file in the root of the /frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_AUTH_API_URL=http://localhost:8001
```

### 3. Development
```bash
npm run dev
```

## Project Structure

- src/api: Modular service layer for API communication.
- src/components: Reusable UI components (SkinCard, Navbar, etc.).
- src/context: Global state management (AuthContext).
- src/pages: Top-level route components.
- src/types: Centralized TypeScript interfaces for API schemas.

## License
Developed for academic purposes at the University of Fortaleza (UNIFOR).
