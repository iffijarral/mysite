# Property Rental Web Application

This repository contains the source code for a full-fledged web application for renting properties, similar to Airbnb. The application is developed using Bottle (a lightweight WSGI micro web-framework for Python), HTML, JavaScript, and CSS. The backend uses an SQLite database.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database](#database)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and authentication
- Property listing and search
- Property details with image gallery
- Booking functionality
- User profile management
- Reviews and ratings for properties

## Tech Stack
- **Backend**: Bottle, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Templating Engine**: Jinja2 (for HTML templates)
- **Database**: SQLite

## Installation
1. **Clone the repository**
    ```sh
    git clone https://github.com/your-username/property-rental-app.git
    cd property-rental-app
    ```

2. **Create a virtual environment and activate it**
    ```sh
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the SQLite database**
    ```sh
    python setup_database.py
    ```

## Usage
1. **Run the development server**
    ```sh
    python app.py
    ```

2. **Open your browser and navigate to**
    ```
    http://localhost:8080
    ```

## Database
The application uses SQLite as the database. The database schema is defined in `setup_database.py`. To reset or initialize the database, you can run:
```sh
python setup_database.py
