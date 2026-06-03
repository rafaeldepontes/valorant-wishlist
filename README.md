# Valorant Wishlist

A high-performance, full-stack platform designed for the Valorant community. Users can explore a comprehensive skin catalog, manage personal wishlists with real-time tracking, and engage in meaningful community reviews.

Developed for the University of Fortaleza (UNIFOR), this project demonstrates a modern approach to web application architecture, combining a microservices-lite backend with a responsive, type-safe frontend.

## Architecture

The project follows a distributed architecture to separate concerns and ensure scalability:

- **Core API (/backend/vw)**: Handles the main business logic, including skin catalog management, user profiles, wishlist operations, and community reviews.
- **Auth API (/backend/vw-login)**: A dedicated service for secure user authentication, registration, and session management using JWT and HTTP-only cookies.
- **Frontend (/frontend)**: A modern React application built with Vite and TypeScript, featuring a specialized Valorant-themed UI and centralized state management.

## Key Features

- **Comprehensive Catalog**: Browse all Valorant skins with detailed metadata and high-quality imagery.
- **Smart Wishlist**: Track desired items, set priorities, and manage your collection progress.
- **Community Reviews**: Share feedback and ratings on skins, with support for anonymous contributions.
- **Agent Profiles**: Personalized user dashboards with favorite weapon highlights and wishcount metrics.
- **Secure Authentication**: Robust login/register system with rate limiting and secure session handling.

## Technologies

### Backend
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.10+.
- **PostgreSQL**: Relational database for persistent storage.
- **SQLAlchemy**: SQL Toolkit and Object-Relational Mapper.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Slowapi**: Rate limiting for enhanced security.

### Frontend
- **React 18**: UI library for building interactive user interfaces.
- **TypeScript**: Static typing for improved developer experience and code reliability.
- **Vite**: Ultra-fast build tool and development server.
- **Tailwind CSS**: Utility-first CSS framework for custom, responsive designs.
- **Axios**: Modular service layer for API communication.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js (Latest LTS recommended)
- PostgreSQL instance

### 1. Backend Services
Both services (vw and vw-login) require their own environment configuration.
- Navigate to each service directory: backend/vw and backend/vw-login.
- Follow the specific instructions in their respective README.md files for setup and database migrations.

### 2. Frontend Application
- Navigate to the frontend directory.
- Install dependencies: npm install
- Start the development server: npm run dev

## Documentation

Detailed technical documentation is available in the following locations:
- [Backend Wiki](./backend/PROJECT_WIKI.md)
- [Frontend Wiki](./frontend/PROJECT_WIKI.md)
- [Installation Guide](./backend/vw/doc/INSTALL.md)

## License

This project was developed for academic purposes at the University of Fortaleza.
