# Rider Tracker

A Django REST API application for tracking and managing ride-sharing operations. This system allows administrators to manage users (riders and drivers), track rides through their lifecycle, and generate reports on ride data.

## Features

- **User Management**: Support for three user roles (Admin, Driver, Rider) with role-based access control
- **Ride Management**: Create, update, and track rides through various status transitions
- **Ride Events**: Automatic event logging for ride status changes
- **JWT Authentication**: Secure API access using JSON Web Tokens
- **Ride Filtering & Sorting**: Filter rides by status and rider email, sort by pickup time or distance
- **Reporting**: Generate reports on ride statistics (e.g., trips longer than 1 hour)

## Technology Stack

- **Django 5.0.3**: Web framework
- **Django REST Framework**: REST API toolkit
- **djangorestframework-simplejwt**: JWT authentication
- **SQLite**: Database (default, can be configured for production)

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Rider-Tracker
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Run migrations**
   ```bash
   cd rider_tracker
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data (optional)**
   ```bash
   python populate_data.py
   ```
   This creates:
   - 1 admin user (username: `admin`, password: `password`)
   - 4 driver users
   - 7 rider users
   - Sample rides with events across multiple months

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

- `POST /api/login/` - Obtain JWT access and refresh tokens
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```
  Response:
  ```json
  {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
  ```

- `POST /api/token/refresh/` - Refresh access token
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

### Users

All user endpoints require admin authentication.

- `GET /api/users/` - List all users (paginated)
- `POST /api/users/` - Create a new user
- `GET /api/users/<id>/` - Retrieve a specific user
- `PUT /api/users/<id>/` - Update a user (full update)
- `PATCH /api/users/<id>/` - Update a user (partial update)
- `DELETE /api/users/<id>/` - Delete a user

**User Model:**
```json
{
  "username": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string (optional)",
  "role": "admin|driver|rider"
}
```

### Rides

All ride endpoints require admin authentication.

- `GET /api/rides/` - List all rides (paginated)
  - Query parameters:
    - `status`: Filter by ride status (accepted, en-route, pickup, dropoff, completed, cancelled)
    - `rider_email`: Filter by rider email (case-insensitive partial match)
    - `sort_by`: Sort by `pickup_time` or `distance`
    - `lat` & `lng`: Required when sorting by distance
  - Example: `/api/rides/?status=completed&rider_email=test&sort_by=distance&lat=14.6&lng=121.0`

- `POST /api/rides/` - Create a new ride
- `GET /api/rides/<id>/` - Retrieve a specific ride
- `PUT /api/rides/<id>/` - Update a ride (full update)
- `PATCH /api/rides/<id>/` - Update a ride (partial update)
- `DELETE /api/rides/<id>/` - Delete a ride
- `PATCH /api/rides/<id>/status/` - Update ride status (validates status transitions)

**Ride Model:**
```json
{
  "status": "accepted|en-route|pickup|dropoff|completed|cancelled",
  "rider": <user_id>,
  "driver": <user_id>,
  "pickup_latitude": <float>,
  "pickup_longitude": <float>,
  "dropoff_latitude": <float>,
  "dropoff_longitude": <float>,
  "pickup_datetime": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Valid Status Transitions:**
- `accepted` → `en-route`, `cancelled`
- `en-route` → `pickup`, `cancelled`
- `pickup` → `dropoff`, `cancelled`
- `dropoff` → `completed`
- `completed` → (terminal state)
- `cancelled` → (terminal state)

### Ride Events

All ride event endpoints require admin authentication.

- `GET /api/ride-events/` - List all ride events (paginated)
- `POST /api/ride-events/` - Create a new ride event
- `GET /api/ride-events/<id>/` - Retrieve a specific ride event
- `PUT /api/ride-events/<id>/` - Update a ride event (full update)
- `PATCH /api/ride-events/<id>/` - Update a ride event (partial update)
- `DELETE /api/ride-events/<id>/` - Delete a ride event

**Ride Event Model:**
```json
{
  "ride": <ride_id>,
  "description": "string",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ (auto-generated)"
}
```

## Authentication

All API endpoints (except login and token refresh) require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Access tokens expire after 4 hours. Use the refresh token endpoint to obtain a new access token.

## Database Models

### User
- Extends Django's `AbstractUser`
- Fields: `username`, `email`, `first_name`, `last_name`, `phone`, `role`
- Roles: `admin`, `driver`, `rider`

### Ride
- Fields: `status`, `rider`, `driver`, `pickup_latitude`, `pickup_longitude`, `dropoff_latitude`, `dropoff_longitude`, `pickup_datetime`
- Automatically creates events when status changes
- Validates status transitions

### RideEvent
- Fields: `ride`, `description`, `created_at`
- Automatically created when ride status changes

## Scripts

### populate_data.py

Populates the database with sample data:
- Creates admin, driver, and rider users
- Generates rides across multiple months (January-April 2024)
- Creates ride events for each ride

**Usage:**
```bash
cd rider_tracker
python populate_data.py
```

### reports.py

Generates a report showing the count of trips longer than 1 hour per driver per month.

**Usage:**
```bash
cd rider_tracker
python reports.py
```

**Output:**
```
Month       Driver          Count of Trips > 1 hour
2024-01     John Carter     3
2024-01     Tim Holland     2
...
```

## Permissions

- All API endpoints require authentication (except login/token refresh)
- Only users with the `admin` role can access the API endpoints
- Custom permission class `IsAdmin` enforces admin-only access

## Pagination

The API uses custom pagination classes:
- `UserPagination`: For user listings
- `RidePagination`: For ride listings
- `RideEventPagination`: For ride event listings


### Logging

Database queries are logged to `debug.log` in the project root directory. This is useful for debugging and performance analysis.
