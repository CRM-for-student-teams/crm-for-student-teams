# Freelance Management System for Student Teams

## Project Overview

This is a freelance project management system designed for student teams who work as freelancers. The platform connects student teams with clients, allowing them to manage freelance projects, track tasks, and communicate with clients in real-time. The system is built using Django and Django REST Framework with WebSocket-based chat capabilities.

## Key Features

### User Management

- Custom user authentication system with three role types:
  - Student Captain (freelance team leader who manages the team)
  - Student Member (freelance team member who executes tasks)
  - Client (freelance project owner who hires student teams)
- JWT-based authentication
- Email-based user identification

### Team Management

- Student freelance teams can be created with multiple members
- Team membership with role-based access control
- Team captains manage their freelance teams and coordinate work
- Students can participate in multiple freelance teams

### Freelance Project Management

- Freelance projects are assigned to student teams by clients
- Each project contains:
  - Name and description
  - Deadline tracking
  - Creation and update timestamps
  - Team assignment

### Task Management

- Tasks belong to freelance projects and are distributed among team members
- Task properties:
  - Title and description
  - Priority levels: Low, Medium, High
  - Status tracking: To Do, In Progress, Done
  - Executor assignment (specific team member responsible)
  - Deadline management
  - Creation and update timestamps

### Real-time Chat

- WebSocket-based chat functionality using Django Channels
- Redis-based channel layer for real-time communication
- Enables direct communication between clients and student teams
- Team and project-specific chat channels

### API & Documentation

- RESTful API built with Django REST Framework
- API documentation using DRF Spectacular (OpenAPI/Swagger)
- Permission-based access control for all endpoints

## Technology Stack

- **Backend Framework**: Django
- **API**: Django REST Framework
- **Real-time Communication**: Django Channels with Redis
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: DRF Spectacular
- **Admin Panel**: Django Unfold
- **Containerization**: Docker & Docker Compose
- **Static Files**: WhiteNoise

## Architecture

The project follows a modular Django app structure:

- `apps.teams` - Student team and user management
- `apps.projects` - Freelance project and task management
- `apps.chat` - Real-time messaging between clients and teams
- `apps.clients` - Client management
- `apps.common` - Shared utilities

## Development Setup

The project includes:

- Docker Compose configuration for local development
- Separate settings for development and production environments
- PostgreSQL database with health checks
- Redis for WebSocket channel layer
- Debug toolbar for development
- CORS support for frontend integration

## Testing

- pytest configured for testing
- Test files included for teams and projects apps
- Separate development requirements
