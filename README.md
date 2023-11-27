## Project Overview

This project was developed as part of a technical challenge for a job interview. Its primary objective was to have a REST API using Django Rest Framework that serves as the backbone for a road traffic monitoring dashboard, allowing for informed decision-making regarding the traffic intensity recorded on local road segments.

In our world of ever-increasing urbanisation and traffic congestion, having real-time insights into road traffic conditions is crucial. This project addresses this need by providing a comprehensive set of data points for assessing traffic conditions and making informed decisions.


## Key Features
The API focuses on geographical representations of road segments, offering the following information:

**1. Road Segments**
- Overview of all road segments, with the count of traffic readings through that segment.
- Detailed view on individual road segments, with the all of the data from the traffic readings recorded in that segment.
- Specific views that only display data according to the last traffic reading's intensity (high, medium or low).

**2. Traffic Readings**
- Overview of all traffic readings, their intensity (calculated based on the speed), and the road segment in which it was recorded.
- Specific views that only display traffic readings according to their intensity (high, medium or low).

**3. Sensors**
- Overview of all sensors available, with their id, name and uuid.
- Overview of all registered sensor readings, indicating the road segment id, the car license plate and the timestamp.

**4. Cars**
- Overview of all cars that were registered through a sensor reading.
- Detailed view on individual cars (through id or license plate), indicating the car details, and its sensor readings from the last 24h, including data from the road segment and sensor.


## Prerequisites

To be able to run this API project, I used the following:
- Python *(version 3.11.5)*
- Django *(version 4.2.7)*
- Django Rest Framework *(version 3.14)*
- PostgreSQL *(version 16.0)*
- psycopg *(version 2.9.9)*
- drf-yasg *(version 1.21.7)*


## Getting Started

Next, I'll detail in a few points the steps needed to get this project and set it up properly.


### Clone the repository

You can download it directly from my GitHub repository or you can clone it to a folder of your choice with the following command:

```bash
git clone https://github.com/MPCaloba/traffic_monitoring_api
```


### Change the working directory

Once you have the the code, your folder tree should look something like this:

```bash
.
└── your_project_folder
    ├── traffic_monitoring_api
    │   ├── traffic_api
    │   ├── traffic_monitoring_api
    │   └── manage.py
    ├── traffic-speed-data
    │   ├── LICENSE
    │   ├── README.md
    │   ├── roadsegments.csv
    │   ├── sensors.csv
    │   ├── traffic_readings.csv
    │   └── traffic_speed.csv
    ├── venv
    │   ├── Include
    │   ├── Lib
    │   ├── Scripts
    │   └── pyvenv.cfg
    ├── .gitignore
    ├── README.md
    └── requirements.txt
```

Now you should change your working directory to your project folder:

```bash
cd your_project_folder
```


### Activate the virtual environement

Before moving on, activate the virtual environment to get the project dependencies:

```bash
venv\Scripts\activate
```

You should have `(venv)` at the beginning of your command line prompt. If, for some reason, there are problems with the dependencies and you need to install them manually, you can run the following command:

```bash
pip install -r requirements.txt
```


### Create a PostgreSQL database and load CSV data

The data we will use is already in your project folder, inside the *traffic-speed-data* folder. To import this dataset, first create a database inside PostgreSQL (I called mine 'traffic_monitoring_db') and then access it through:

```bash
psql -U postgres -d traffic_monitoring_db
```

It will prompt you to write your password. After doing so, copy the data from the CSV file:

```bash
\copy traffic_api_roadsegments FROM '..\your_project_folder\traffic_monitoring\Traffic-Speed\road_segments.csv' WITH CSV HEADER;
\copy traffic_api_trafficreadings FROM '..\your_project_folder\traffic_monitoring\Traffic-Speed\traffic_readings.csv' WITH CSV HEADER;
\copy traffic_api_sensors FROM '..\your_project_folder\traffic_monitoring\Traffic-Speed\sensors.csv' WITH CSV HEADER;
```

Still regarding the database, you now need to go to the *settings.py* file and update the default database information to match your database name, your user name and your user password.

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_database_name",
        "USER": "your_user_name",
        "PASSWORD": "your_user_password",
        "HOST": "localhost",
    }
}
```


### Migrate the database and apply initial data

Finally migrate and apply the data with following two commands:

```bash
python manage.py makemigrations
python manage.py migrate
```


### Start the development server

The project should be able to execute now. Prompt the following to get it up and running:

```bash
python manage.py runserver
```


## Using the API

When you start the server, the first local page (http://127.0.0.1:8000/) will show you all of the traffic readings from the dataset. Then, to authenticate yourself as the admin, you should use *admin* as the user and *admin_password* as the password.


### Endpoints

In the following table, you can find all of the endpoints that this API has.

| Endpoint   | URL       | Description                                   |
| :---------- | :--------- | :------------------------------------------ |
| All traffic readings | http://127.0.0.1:8000/traffic-readings/ | This page will display all traffic readings, as well as their intensity. |
| Individual traffic reading | http://127.0.0.1:8000/traffic-readings/10 | Here, you can access, edit and delete the information about any individual traffic reading (used 10 as an example). |
| Traffic readings with high intensity | http://127.0.0.1:8000/traffic-readings/high-intensity | This page will show only the traffic readings that are characterised as high intensity. |
| Traffic readings with medium intensity | http://127.0.0.1:8000/traffic-readings/medium-intensity | This page will show only the traffic readings that are characterised as medium intensity. |
| Traffic readings with low intensity | http://127.0.0.1:8000/traffic-readings/low-intensity | This page will show only the traffic readings that are characterised as low intensity. |
| Create a new traffic reading | http://127.0.0.1:8000/create-traffic-reading/ | Here you will be able to specify a road segment and speed value to create a new traffic reading. |
| ------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| All road segments | http://127.0.0.1:8000/road-segments/ | This page will display all road segments, and how many traffic readings each segment has. |
| Individual road segment | http://127.0.0.1:8000/road-segments/9 | Here, you can access, edit and delete the information about individual road segments, as well as details from its traffic readings. |
| Road segments with high intensity | http://127.0.0.1:8000/road-segments/high-intensity | This page will show only the road segments that are characterised as high intensity. |
| Road segments with medium intensity | http://127.0.0.1:8000/road-segments/medium-intensity | This page will show only the road segments that are characterised as medium intensity. |
| Road segments with low intensity | http://127.0.0.1:8000/road-segments/low-intensity | This page will show only the road segments that are characterised as low intensity. |
| Create a new road segments | http://127.0.0.1:8000/create-road-segment | Here you will be able to specify the coordinates and length values to create a new road segments. |
| ------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| All sensors | http://127.0.0.1:8000/sensors | This page will display all sensors available. |
| Individual sensor | http://127.0.0.1:8000/sensors/3 | Here, you can access, edit and delete the information about any individual sensor (used 3 as an example). |
| All sensor readings | http://127.0.0.1:8000/sensors-readings | This page will display all of the registered sensor readings. |
| Create a sensor reading | http://127.0.0.1:8000/create-sensor-reading | Here you will be able to specify a license plate, the timestamp, road segment and sensor to create a new sensor reading. |
| ------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| All cars registered | http://127.0.0.1:8000/cars | This page will display all cars registered, and when they were created. |
| Individual car | http://127.0.0.1:8000/cars/AA11AA | Here, you can access the car data by license plate and view details about readings from the last 24h (used 'AA11AA' as an example). |
| ------------------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Admin | http://127.0.0.1:8000/admin/ | This is for the admin to login/logout, and perform any kind of user management. |
| API Swagger | http://127.0.0.1:8000/api/docs | Here you will find interactive documentation regarding the API. |


## Testing the API

To test some of the functionalities (CRUD operations and permissions), I wrote 8 different tests in the *traffic_api/tests/test_permissions.py* file. So, you can use them to test the API with the following command:

```bash
  python manage.py test traffic_api.tests.test_permissions
```


## Improvements

There are a couple of features that need some improvement. I will write here the ones I am aware of:
- **Optimisation for scaling -** the methods used to get some properties are not suited for efficient use when considering large amounts of data.
- **Tokenize sensor readings -** I tried to implement a permission so that only POST requests with a certain token would be able to create new sensor readings, but it was not working with my tests.
- **Bulk sensor readings -** each sensor should accumulate a records and then send these records in bulk to the platform, but I only implemented single sensor reading creations.


## More Information

I wrote a blog post about this project that describres the code. If you'd like, you can read it [here](https://medium.com/@marco_caloba/traffic-monitoring-rest-api-c736b92f0a43).

Also, in case something is not working properly or you have any questions relating this project, you can get to me through the personal links below or my personal e-mail: marco_caloba@hotmail.com.


## Personal Links
- [Personal website](https://mcaloba-04272.stackbit.app/)
- [GitHub](https://github.com/MPCaloba)
- [LinkdIn](https://www.linkedin.com/in/marcocaloba/)
- [Medium](https://medium.com/@marco_caloba)
- [Linktree](https://linktr.ee/mcaloba)