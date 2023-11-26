# Course_Recomendation

## Overview

Welcome to Course Adviser, a web application designed to assist students in choosing the right courses for their desired career paths across various academic streams. This project utilizes the Flask web framework, PostgreSQL for the database, and HTML for dynamic page rendering.

## Features

- **User Authentication:** Secure user accounts and profiles to personalize the course recommendations.

- **Stream Selection:** Choose from a variety of academic streams, including but not limited to Computer Science, Business, Medicine, and more.

- **Role Aspiration:** Define your desired role within the chosen stream to receive tailored course recommendations.

- **Dynamic Course Suggestions:** The application dynamically generates course suggestions based on the selected stream and role aspiration.

- **Search and Filter:** Users can search for specific courses and apply filters to narrow down their options.

## Setup Instructions

### Prerequisites

- Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

- Install Flask using the following command:
     ->pip install Flask
  
- Install PostgreSQL and set up a database. Update the database configuration.
    ```bash
   ->pip install psycopg2-binary
   ->sudo apt-get install libpq-dev
   ->pip install psycopg2
    ```
  
### Installation

1. Clone the repository:

    ```bash
    git clone [https://github.com/ssaral/Course_Recomendation.git](https://github.com/ssaral/Course_Recomendation.git)
    ```

2. Navigate to the project directory:

    ```bash
    cd Course_Recommendation
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    #We used PGsql Admin which is a GUI of database management.
   Below are few common commands you can use to initialize database in flask application
   
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the application:
    You can use anyone of the three ways below-
   ```bash
   - python app.py
   - ./run.sh
   - flask run
     ```

8. Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the Course Adviser web application.

## Contributing

We welcome contributions! If you find any bugs or have suggestions for improvement, please create an issue or submit a pull request.

## Acknowledgments

- Thanks to the Flask and PostgreSQL communities for their excellent and detailed documentation.
- Inspired by the passion of students seeking the right path for their academic and career aspirations.
