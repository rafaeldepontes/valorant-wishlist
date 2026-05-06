# Valorant-Wishlist

A full-stack application developed for UNIFOR (University of Fortaleza) that allows users to explore Valorant skins, manage a personal wishlist, and share community reviews. The project consists of a high-performance FastAPI backend and a responsive React frontend.

## Project Structure

- `/backend`: FastAPI (Python) RESTful API with PostgreSQL and JWT authentication.
- `/frontend`: Vite + React (TypeScript) SPA with Tailwind CSS.

## Core Features

- Full user authentication system (Login/Register).
- Real-time skin wishlist management.
- Community review system for all in-game items.
- Searchable skin catalog with pagination.
- Personalized agent profiles.

## Quick Start

### 1. Backend Setup
Navigate to the `/backend` directory:
- Follow the instructions in [backend/README.md](./backend/README.md) to set up your Python environment.
- Ensure your PostgreSQL database is configured.
- Run the server: `uvicorn app.main:app --reload`

### 2. Frontend Setup
Navigate to the `/frontend` directory:
- Follow the instructions in [frontend/README.md](./frontend/README.md) to install dependencies.
- Run the development server: `npm run dev`

## API Reference

The backend provides a complete Swagger UI documentation available at `/docs` when the server is running. Key modules include:
- Skins: `/skins`
- Users: `/users`
- Wishlist: `/wishlist`
- Reviews: `/reviews`

## License

This project was developed for academic purposes at the University of Fortaleza.
