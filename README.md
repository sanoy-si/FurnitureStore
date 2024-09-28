# Furniture Store API

## Overview
The Furniture Store API is a RESTful API designed to provide a comprehensive solution for managing a furniture e-commerce platform. It enables developers to efficiently manage product listings, handle orders, and improve customer interactions.

## Technologies Used
- **Django**
- **Django Rest Framework**
- **SQLite**
- **Swagger**
- **JSON Web Tokens (JWT)**
- **Python**

  
## Features
- **Product Catalog**: Access detailed information about various furniture items, including descriptions, prices, images, and availability.
- **Search and Filter**: Advanced search functionality to filter products by categories, styles, materials, and price ranges.
- **Order Management**: Seamless order processing, including adding items to the cart, checking out, and tracking orders.
- **Inventory Management**: Real-time tracking of stock levels and notifications for low inventory.
- **User Authentication**: Secure user registration and login, with JSON Web Tokens (JWT) for session management.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sanoy-si/.git
    cd FurnitureStore
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

4. Create a superuser to access the admin panel:

    ```bash
    python manage.py createsuperuser
    ```

5. Collect static files:

    ```bash
    python manage.py collectstatic
    ```

### Running the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

### Visit http://127.0.0.1:8000/ in your web browser to see the application in action
![image](https://github.com/user-attachments/assets/3fd44e47-da42-4d1c-b61a-3a02c921da15)
