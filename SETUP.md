# Setup and Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- Git

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/v-mart-inventory.git
cd v-mart-inventory
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install Flask==2.3.3 gunicorn==21.2.0 email-validator==2.0.0 psycopg2-binary==2.9.7
```

4. **Set environment variables:**
```bash
export SESSION_SECRET="your-secret-key-here"
# On Windows: set SESSION_SECRET=your-secret-key-here
```

5. **Run the application:**
```bash
python main.py
```

6. **Access the application:**
Open your browser and go to `http://localhost:5000`

## Production Deployment

### Using Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### Environment Variables for Production
```bash
export SESSION_SECRET="your-production-secret-key"
export DATABASE_URL="postgresql://user:password@localhost/vmart_db"
```

### Database Migration to PostgreSQL
For production, you can switch to PostgreSQL by:
1. Setting the `DATABASE_URL` environment variable
2. Installing PostgreSQL
3. Running the application (it will auto-create tables)

## File Structure
```
v-mart-inventory/
├── app.py                 # Main Flask application
├── main.py               # Entry point
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard
│   ├── add_product.html # Add product form
│   ├── edit_product.html# Edit product form
│   └── low_stock.html   # Low stock report
├── static/              # Static assets
│   ├── css/
│   │   └── custom.css   # Custom styles
│   └── js/
│       └── main.js      # JavaScript functionality
├── README.md            # Project documentation
├── LICENSE              # MIT License
├── .gitignore          # Git ignore rules
└── pyproject.toml      # Python dependencies
```

## Features Overview

### Core Functionality
- Product inventory management
- Category and supplier management
- Stock level tracking
- Search and filtering
- Low stock alerts and reporting

### Technical Features
- Responsive Bootstrap UI
- SQLite/PostgreSQL database support
- Form validation
- Error handling
- Chart.js visualizations
- Mobile-friendly design

## Development Notes

### Database Schema
The application automatically creates three main tables:
- `Categories` - Product categories
- `Suppliers` - Supplier information
- `Products` - Main inventory items

### Security Considerations
- Input validation on all forms
- SQL injection prevention with parameterized queries
- CSRF protection through Flask's built-in features
- Environment-based secret management

### Customization
- Modify `static/css/custom.css` for styling changes
- Update `templates/` for UI modifications
- Extend `app.py` for additional functionality