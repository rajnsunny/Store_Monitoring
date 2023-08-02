# Store Monitoring Application

## Introduction

The Store Monitoring Application is a Django-based backend system that helps restaurant owners monitor the online status of their stores during business hours. The application provides APIs to generate reports that show the store's uptime and downtime for specific time intervals. The reports are based on data from various sources, including store activity status, business hours, and timezones.

## Features

- Trigger report generation using the `/trigger_report` API endpoint.
- Get the status of the report or the CSV file using the `/get_report` API endpoint.
- Calculate store uptime and downtime based on observed data.
- Extrapolate uptime and downtime for the entire time interval based on periodic polls.
- Handle time zone conversions to ensure accurate report generation.
- Store data in a SQLite database.(default)

## Getting Started

Follow the steps below to set up and run the Store Monitoring Application on your local machine.

### Prerequisites

- Python 3.6 or higher
- Django 3.2 or higher
- SQLite (with appropriate settings)

### Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/rajnsunny/Store-Monitoring.git
   ```

2. Navigate to the project directory:

   ```
   cd Store-Monitoring
   ```

3. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Create a SQLite database for the application.
2. Update the database settings in `settings.py` to match your database configuration.


### Database Migration

Run the following commands to perform the database migration:

```
python manage.py makemigrations
python manage.py migrate
```

### Loading Data

To load the provided CSV data into the database, use the custom management command:

```
python manage.py load_data
```

### Run the Server

Start the Django development server:

```
python manage.py runserver
```

The application will now be accessible at `http://localhost:8000/`.

## Usage

1. Trigger Report Generation:
   Use the `/trigger_report` API endpoint to trigger the generation of a store monitoring report. No input is required for this endpoint. It will return a unique `report_id`.

2. Get Report Status and CSV:
   Use the `/get_report` API endpoint to check the status of the report or download the CSV file. Provide the `report_id` as input. If the report generation is not complete, it will return "Running." Once the report is complete, it will return "Complete" along with the CSV file containing the store monitoring data.

## Report Schema

The report contains the following columns:

- `store_id`: The ID of the store.
- `uptime_last_hour (in minutes)`: Uptime of the store in the last hour (during business hours).
- `uptime_last_day (in hours)`: Uptime of the store in the last day (during business hours).
- `uptime_last_week (in hours)`: Uptime of the store in the last week (during business hours).
- `downtime_last_hour (in minutes)`: Downtime of the store in the last hour (during business hours).
- `downtime_last_day (in hours)`: Downtime of the store in the last day (during business hours).
- `downtime_last_week (in hours)`: Downtime of the store in the last week (during business hours).



## Contributors

rajnsunny9@gmail.com

## Acknowledgments

Special thanks to Loop Kitchen. for providing the data and an Amesome problem statement for this project.

---

Replace the placeholders with appropriate information, such as the actual URL of the repository, email addresses, contributors' names, etc. The README file provides essential information about the application, its features, and how to set it up and use it. It helps users understand the purpose of the application and how to interact with it.
