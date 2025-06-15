# V Mart Inventory Management System

## Overview

V Mart is a comprehensive inventory management system designed for grocery stores and retail businesses. Built with Flask and SQLAlchemy, it provides a web-based interface for managing products, tracking stock levels, and monitoring inventory status. The system features real-time inventory tracking, low stock alerts, and a responsive dashboard for business insights.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Database**: Configurable (SQLite for development, PostgreSQL for production)
- **WSGI Server**: Gunicorn for production deployment
- **Session Management**: Flask's built-in session handling with configurable secret keys

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **JavaScript**: Vanilla JavaScript for interactive features
- **Responsive Design**: Mobile-first approach using Bootstrap's grid system

### Application Structure
- **MVC Pattern**: Clear separation between models, views (templates), and controllers (routes)
- **Modular Design**: Separate files for models, routes, and application configuration
- **Database Seeding**: Automated initial data population for grocery store inventory

## Key Components

### Data Models
- **Product Model**: Core entity with attributes including name, description, category, price, quantity, minimum stock level, barcode, and timestamps
- **Stock Status Logic**: Automated classification of products as "in-stock", "low-stock", or "out-of-stock"
- **Category Management**: Dynamic category system for product organization

### Core Features
- **Inventory Management**: Add, edit, delete, and view products
- **Search and Filtering**: Real-time search with category and stock status filters
- **Stock Monitoring**: Automatic low stock and out-of-stock alerts
- **Dashboard Analytics**: Inventory value calculations and stock statistics
- **Barcode Support**: Unique barcode assignment and tracking

### User Interface Components
- **Responsive Navigation**: Bootstrap-based navigation with role-based menu items
- **Product Listing**: Paginated product grid with sorting capabilities
- **Forms**: Validated forms for product creation and editing
- **Status Indicators**: Visual stock status badges and alerts
- **Dashboard Widgets**: Key performance indicator cards and charts

## Data Flow

### Product Management Flow
1. User accesses product forms through navigation
2. Form validation occurs client-side and server-side
3. Data is processed through Flask routes
4. SQLAlchemy ORM handles database operations
5. Success/error messages are flashed to user
6. User is redirected to appropriate view

### Inventory Tracking Flow
1. Product quantities are updated through edit forms
2. Stock status is automatically calculated based on quantity vs. minimum stock level
3. Dashboard aggregates inventory data for analytics
4. Search and filter operations query the database with SQLAlchemy
5. Results are rendered through Jinja2 templates

### Database Operations
- **CRUD Operations**: Full create, read, update, delete functionality for products
- **Query Optimization**: Efficient filtering and sorting with SQLAlchemy
- **Data Integrity**: Unique constraints on barcodes, required field validation
- **Connection Pooling**: Configured for production performance

## External Dependencies

### Python Packages
- **Flask 3.1.1**: Web framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM integration
- **SQLAlchemy 2.0.41**: Database abstraction layer
- **Gunicorn 23.0.0**: WSGI HTTP server
- **psycopg2-binary 2.9.10**: PostgreSQL adapter
- **email-validator 2.2.0**: Email validation utilities
- **Werkzeug 3.1.3**: WSGI utilities

### Frontend Dependencies (CDN)
- **Bootstrap 5.3.0**: CSS framework for responsive design
- **Font Awesome 6.4.0**: Icon library for UI elements

### System Dependencies
- **Python 3.11**: Runtime environment
- **PostgreSQL**: Production database system
- **OpenSSL**: Security and encryption support

## Deployment Strategy

### Development Environment
- **Local Development**: Flask development server with debug mode
- **Database**: SQLite for rapid prototyping and testing
- **Auto-reload**: Enabled for development productivity

### Production Environment
- **WSGI Server**: Gunicorn with multiple workers
- **Database**: PostgreSQL with connection pooling
- **Process Management**: Configured for autoscaling deployment
- **Security**: Environment-based configuration for secrets
- **Proxy Support**: ProxyFix middleware for reverse proxy compatibility

### Deployment Configuration
- **Port Binding**: 0.0.0.0:5000 for container compatibility
- **Process Scaling**: Configured for Replit's autoscale deployment target
- **Environment Variables**: DATABASE_URL and SESSION_SECRET for configuration
- **Health Checks**: Database connection pre-ping for reliability

### Database Migration Strategy
- **Automatic Table Creation**: SQLAlchemy creates tables on application startup
- **Seed Data**: Automated population of initial grocery store inventory
- **Schema Evolution**: Ready for Alembic migrations if needed

## Changelog
- June 14, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.
