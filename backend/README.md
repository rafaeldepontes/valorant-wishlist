# Valorant Wishlist - Backend Workspace

This directory contains the distributed backend services for the Valorant Wishlist platform. The architecture is split into two specialized FastAPI services to decouple authentication from core business logic.

## Directory Structure

- **/vw (Core API)**: The primary service handling skin data, user profiles, wishlist management, and community reviews.
- **/vw-login (Auth API)**: A dedicated service focused on secure user registration, authentication (JWT/Cookies), and identity management.

## Architecture Overview

The backend uses a shared PostgreSQL database but separates responsibilities at the service layer:

1.  **Authentication**: Handled by `vw-login`. It manages password hashing (Argon2id), JWT generation, and cookie-based session persistence.
2.  **Resource Management**: Handled by `vw`. It manages the skin catalog (cached from external Valorant APIs), user-specific wishlists, and the relational data for community feedback.

Both services share similar design patterns:
- **Dependency Injection**: Heavy use of FastAPI dependencies for service and store management.
- **Data Integrity**: Pydantic schemas for rigorous request/response validation.
- **Resilience**: Integrated rate limiting (Slowapi) and standardized error handling.

## General Requirements

- **Python 3.10+**
- **PostgreSQL**
- **Virtual Environment** (recommended for each service)

## Getting Started

Each service is independent and requires its own configuration. Please refer to the specific documentation for each:

- [Core API Setup](./vw/README.md)
- [Auth API Setup](./vw-login/README.md)

---
*Developed for academic purposes at the University of Fortaleza (UNIFOR).*
