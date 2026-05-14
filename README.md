# CRM API

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Cache%20%2F%20Broker-DC382D?logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-Background%20Tasks-37814A?logo=celery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?logo=jsonwebtokens&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-Documentation-6BA539?logo=openapiinitiative&logoColor=white)

Production-style REST API for a B2B CRM system focused on corporate course sales, customer management, deal tracking, contracts, and sales analytics.

Built as the main portfolio project.

## Tech Stack

**Backend:** Python, Django, Django REST Framework  
**Database:** PostgreSQL  
**Authentication:** JWT, RBAC  
**Async / Background Jobs:** Redis, Celery, Celery Beat  
**Infrastructure:** Docker, Docker Compose  
**Testing:** Pytest  
**API Documentation:** OpenAPI, Swagger UI, ReDoc  

## Features

- User roles and JWT-based authentication (RBAC)
- Domain-oriented architecture (DDD)
- Pagination
- Basic throttling configuration
- Background tasks with Celery, asynchronous email service
- Optimized lightweight Docker images based on Alpine Linux

## Main Use Cases

- Create and manage companies/accounts
- Store contacts linked to corporate clients
- Maintain a catalog of courses/products
- Track deals through the sales pipeline
- Add course (product) items to deals
- Close deals as won or lost
- Auto-generate contracts
- Monitor revenue and conversion analytics

## API Docs
Class, ER diagrams, and api specification available in the "documentation" directory
After running the project, live API documentation is available at:

```text
http://localhost:8080/api/schema/redoc/
http://localhost:8080/api/schema/swagger-ui/
