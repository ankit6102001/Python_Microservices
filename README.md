# Flask Microservice with JWT Authentication

This is a simple Flask microservice that includes JWT authentication for user login and interacts with an external API to retrieve product data.

## Features

- User authentication using JWT tokens
- Endpoint to authenticate users: `/auth` (POST)
- Secure endpoint to get products: `/products` (GET) - Requires authentication token
- Integration with an external API for product data retrieval

## Getting Started

- Python (3.6 or higher)
- Flask
- Requests
- JWT

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ankit6102001/flask-microservice.git
cd flask-microservice
