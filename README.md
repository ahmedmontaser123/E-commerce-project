<div align="center">

# 🛒 E-commerce System

A modern, high-performance **e-commerce backend API** built with **FastAPI** and **PostgreSQL**.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [API Reference](#api-reference)
- [Interactive Documentation](#interactive-documentation)
- [License](#license)

---

## Overview

The **E-commerce System** is a complete backend REST API that powers an online store. It provides a clean, layered architecture for managing users, products, categories, shopping carts, orders, reviews, payments, shipping addresses, and wishlists.

Built for **performance and scalability**, the API is fully asynchronous and backed by PostgreSQL (with pgvector support for future AI-powered features such as semantic product search).

---

## Features

- **User Management** — create, retrieve, update, and delete user accounts
- **Product Catalog** — full CRUD operations for products and categories
- **Shopping Cart** — add, update, and remove items from a user's cart
- **Order Management** — place orders and track ordered products
- **Reviews & Ratings** — users can rate products on a 1–5 scale
- **Payments** — record and track payment transactions per order
- **Shipping** — manage shipping addresses for orders
- **Wishlist** — save products for later purchase
- **Interactive API Docs** — auto-generated Swagger UI and ReDoc
- **Async-First** — non-blocking I/O throughout the request lifecycle
- **Dockerized Database** — one-command PostgreSQL setup

---

## Tech Stack

| Technology     | Purpose                                      | Version        |
| -------------- | -------------------------------------------- | -------------- |
| Python         | Programming language                         | 3.10+          |
| FastAPI        | Web framework                                | 0.110.2        |
| Uvicorn        | ASGI server                                  | 0.29.0         |
| SQLAlchemy     | ORM (async)                                  | 2.x            |
| asyncpg        | Async PostgreSQL driver                      | latest         |
| PostgreSQL     | Relational database (pgvector)               | 17             |
| Alembic        | Database migrations                          | latest         |
| Pydantic v2    | Data validation & settings                   | 2.x            |
| Docker         | Containerization & database provisioning     | latest         |

---

## Architecture

The project follows a **layered architecture** that separates concerns and keeps the codebase maintainable:

```
Client (HTTP Request)
        │
        ▼
┌──────────────────┐
│      Router      │  Defines API endpoints & request/response schemas
└────────┬─────────┘
        │
        ▼
┌──────────────────┐
│     Service      │  Contains business logic
└────────┬─────────┘
        │
        ▼
┌──────────────────┐
│   Repository     │  Encapsulates database queries (CRUD)
└────────┬─────────┘
        │
        ▼
┌──────────────────┐
│  PostgreSQL DB   │  pgvector-powered persistence layer
└──────────────────┘
```

Each layer is decoupled, which makes the system easy to test, extend, and maintain.

---

## Project Structure

```
E-commerce/
├── Docker/
│   └── docker-compose.yml       # PostgreSQL (pgvector) container config
├── src/
│   ├── main.py                  # FastAPI application entry point
│   ├── .env.example             # Environment variable template
│   ├── helpers/
│   │   └── config.py            # Pydantic-settings application config
│   ├── modules/
│   │   └── db/
│   │       ├── database.py      # Async engine & session management
│   │       └── e_commerce/
│   │           ├── alembic/     # Migration versions
│   │           ├── alembic.ini
│   │           └── schemas/     # SQLAlchemy ORM models (tables)
│   ├── routers/                 # API endpoints per module
│   ├── services/                # Business logic layer
│   ├── repositories/            # Data-access layer
│   ├── schemas/                 # Pydantic request/response models
│   └── requirements.txt        # Python dependencies
└── LICENSE                      # Apache License 2.0
```

---

## Getting Started

Follow these steps to run the project locally.

### Prerequisites

- **Python** 3.10 or higher
- **Docker** (for the PostgreSQL database)
- **Git**

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd E-commerce
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
cd src
pip install -r requirements.txt
```

### 4. Start the database

From the project root:

```bash
cd Docker
docker compose up -d
```

This starts a PostgreSQL 17 container with the pgvector extension enabled.

### 5. Configure environment variables

```bash
cd src
cp .env.example .env
```

Then edit the `.env` file and fill in your database credentials (see [Environment Variables](#environment-variables)).

### 6. Run database migrations

```bash
cd modules/db/e_commerce
alembic upgrade head
```

### 7. Start the server

```bash
cd src
uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.

---

## Environment Variables

All configuration is read from a `.env` file located inside `src/`. The application loads it through `helpers/config.py`.

| Variable                 | Description                        | Default     |
| ------------------------ | ---------------------------------- | ----------- |
| `APP_NAME`               | Application name                   | `E-commerce -System` |
| `APP_VERSION`            | Application version                | `0.1`       |
| `POSTGRES_USERNAME`      | Database user                      | —           |
| `POSTGRES_PASSWORD`      | Database password                  | —           |
| `POSTGRES_HOST`          | Database host                      | `localhost` |
| `POSTGRES_PORT`          | Database port                      | `5432`      |
| `POSTGRES_MAIN_DATABASE` | Database name                      | `E-commerce`|

---

## Database Migrations

This project uses [Alembic](https://alembic.sqlalchemy.org/) for schema versioning.

```bash
# Generate a new migration after changing models
alembic revision --autogenerate -m "description"

# Apply migrations to the database
alembic upgrade head

# Roll back the last migration
alembic downgrade -1
```

---

## API Reference

The API is organized into nine modules. All routes follow REST conventions.

### Users — `/users`

| Method | Endpoint        | Description             |
| ------ | --------------- | ----------------------- |
| POST   | `/users/`       | Create a new user       |
| GET    | `/users/{id}`   | Retrieve a user         |
| PUT    | `/users/{id}`   | Update a user           |
| DELETE | `/users/{id}`   | Delete a user           |

### Products — `/product`

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/product/{user_id}`      | Create a product         |
| GET    | `/product/`               | List all products        |
| GET    | `/product/{product_id}`   | Retrieve a product       |
| PUT    | `/product/{user_id}/{product_id}` | Update a product  |
| DELETE | `/product/{user_id}/{product_id}` | Delete a product  |

### Categories — `/category`

| Method | Endpoint                        | Description               |
| ------ | ------------------------------- | ------------------------- |
| POST   | `/category/{user_id}`           | Create a category         |
| GET    | `/category/{category_id}`       | Retrieve a category       |
| DELETE | `/category/{user_id}/{category_id}` | Delete a category     |

### Cart — `/cart`

| Method | Endpoint                          | Description                    |
| ------ | --------------------------------- | ------------------------------ |
| POST   | `/cart/{user_id}`                 | Create a cart for a user       |
| POST   | `/cart/{user_id}/items`           | Add an item to the cart        |
| GET    | `/cart/{user_id}/items`           | List items in a cart           |
| PUT    | `/cart/{user_id}/items/{item_id}` | Update cart item quantity      |
| DELETE | `/cart/{user_id}/items/{item_id}` | Remove an item from the cart   |
| DELETE | `/cart/{user_id}`                 | Clear / delete the cart        |

### Orders — `/orders`

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| POST   | `/orders/{user_id}`      | Create an order          |
| GET    | `/orders/{order_id}`     | Retrieve order products  |
| PUT    | `/orders/{order_id}/cancel` | Cancel an order       |

### Reviews — `/reviews`

| Method | Endpoint                    | Description             |
| ------ | --------------------------- | ----------------------- |
| POST   | `/reviews/{user_id}`        | Submit a product review |
| GET    | `/reviews/product/{product_id}` | List reviews for a product |
| DELETE | `/reviews/{user_id}/{review_id}` | Delete a review     |

### Payments — `/payments`

| Method | Endpoint             | Description              |
| ------ | -------------------- | ------------------------ |
| POST   | `/payments/{user_id}`| Create a payment         |
| GET    | `/payments/{order_id}` | Retrieve payment details |

### Shipping — `/shipping`

| Method | Endpoint                            | Description               |
| ------ | ----------------------------------- | ------------------------- |
| POST   | `/shipping/{user_id}`               | Add a shipping address    |
| PUT    | `/shipping/{user_id}/{address_id}`  | Update a shipping address |
| GET    | `/shipping/{address_id}`            | Retrieve a shipping address |

### Wishlist — `/wishlist`

| Method | Endpoint                          | Description              |
| ------ | --------------------------------- | ------------------------ |
| POST   | `/wishlist/{user_id}`             | Add product to wishlist  |
| GET    | `/wishlist/{user_id}`             | List wishlist items      |
| DELETE | `/wishlist/{user_id}/{product_id}`| Remove product from wishlist |

---

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
