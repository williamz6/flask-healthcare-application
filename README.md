# Healthcare Survey Tool

## Overview

The Healthcare Survey Tool is a Flask-based web application designed to collect and analyze survey data for a healthcare product launch. It allows users to submit details such as age, gender, total income, and various expense categories (utilities, entertainment, school fees, shopping, and healthcare). The data is stored in a MongoDB Atlas database, exported to a CSV file for analysis, and visualized using Jupyter Notebook to provide insights into income and spending patterns.

### Features
- **Data Collection:** Web form to gather user survey data.
- **Data Storage:** Integrates with MongoDB Atlas for secure and scalable storage.
- **Data Export:** Exports survey data to a CSV file for further analysis.
- **Data Visualization:** Generates charts (e.g., income by age, spending by gender) using Matplotlib and Seaborn.
- **Deployment:** Hosted on AWS EC2 with Gunicorn and Nginx for production use.

### Technologies Used
- **Python:** Core programming language.
- **Flask:** Web framework for the application.
- **PyMongo:** MongoDB driver for Python.
- **MongoDB Atlas:** Cloud-hosted database.
- **Gunicorn:** WSGI HTTP server for deployment.
- **Nginx:** Web server for reverse proxy and load balancing.
- **Pandas, Matplotlib, Seaborn:** Data analysis and visualization libraries.
- **Jupyter Notebook:** Interactive environment for data analysis.

## Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.9+:** Install from [python.org](https://www.python.org/downloads/).
- **Git:** For version control (optional, [git-scm.com](https://git-scm.com/)).
- **AWS Account:** For EC2 deployment (optional, [aws.amazon.com](https://aws.amazon.com/)).
- **MongoDB Atlas Account:** For database hosting (optional, [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)).
- **Basic Command Line Knowledge:** For running scripts and managing the server.

## Installation

### Clone the Repository
```bash
git clone https://github.com/williamz6/flask-healthcare-application.git
cd survey-app
```

