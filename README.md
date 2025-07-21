# FastAPI E-commerce API

A RESTful API for e-commerce applications built with FastAPI and MongoDB.

## Features

- Create and list products with filtering and pagination
- Create and list orders by user with pagination
- MongoDB integration

## API Endpoints

### Products
- **POST /products** - Create a new product
- **GET /products** - List products with optional filters

### Orders
- **POST /orders** - Create a new order
- **GET /orders/{user_id}** - List orders for a specific user

## Running Locally

1. Set up environment variables in .env file as specified in .env.example file.
2. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`
3. Run the application:
   \`\`\`
   uvicorn app.main:app --reload
   \`\`\`

