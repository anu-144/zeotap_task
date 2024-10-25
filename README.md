# zeotap_task

# Project: 3-Tier Rule Engine & Real-Time Weather Monitoring System

## Introduction
This repository contains two distinct applications:
1. A **3-Tier Rule Engine Application** that determines user eligibility based on various attributes such as age, income, department, and experience.
2. A **Real-Time Data Processing System** for weather monitoring, which fetches data from the OpenWeatherMap API and provides insights through rollups, aggregates, and alerts.

## Application 1: 3-Tier Rule Engine

### Features
- **Create and Evaluate Rules**: Define rules based on user attributes and evaluate them using Abstract Syntax Trees (AST).
- **Combine Rules**: Combine multiple rules efficiently to form a more complex decision engine.
- **Dynamic Rule Modifications**: Modify rules dynamically at runtime.
  
### Installation
1. Clone the repository:

   git clone [https://github.com/your-username/your-repo.git](https://github.com/anu-144/zeotap_task.git)
   cd your-repo
  
2. Set up a virtual environment (optional but recommended):

   python3 -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   
3. Install dependencies:
   pip install -r requirements.txt

### Usage
1. To create a rule, use the `create_rule` function:
   
   from rule_engine import create_rule, evaluate_rule

   rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
   ast_rule1 = create_rule(rule1)
   data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
   result = evaluate_rule(ast_rule1, data)
   print("Result:", result)

3. You can also combine multiple rules using the `combine_rules` function:

   from rule_engine import combine_rules

   combined_ast = combine_rules([rule1, rule2])
   combined_result = evaluate_rule(combined_ast, data)
   print("Combined Result:", combined_result)

### Testing
You can test the application using the provided test cases. Run the tests with:

python -m unittest discover

## Application 2: Real-Time Weather Monitoring System

### Features
- **Real-Time Data Fetching**: Fetch weather data at configurable intervals from OpenWeatherMap API.
- **Daily Summaries**: Calculate daily aggregates (average temperature, min/max temperature, dominant weather condition).
- **Alert System**: Define user-configurable thresholds for alerts (e.g., high temperature).
- **Data Visualization**: View daily summaries and historical trends.

### Installation
1. Clone the repository:
   
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

3. Set up a virtual environment (optional):

   python3 -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
  
4. Install dependencies:
   
   pip install -r requirements.txt

5. Sign up for an API key from [OpenWeatherMap](https://openweathermap.org/api) and add it to your environment variables or directly to the configuration file.

### Usage
1. Configure the API key and city names in the `weather_monitor.py` file.
2. Run the real-time weather monitoring system:
   
   python weather_monitor.py
  
3. The system will start fetching data at intervals and store daily summaries. Alerts will be displayed in the console if thresholds are exceeded.

### Testing
Run the unit tests to ensure correct functionality:

python -m unittest test_weather_monitor.py


You can simulate API data and thresholds to check if the alerting and daily summaries are working as expected.


## Dependencies
Both applications use the following dependencies, which are included in the `requirements.txt` file:

requests==2.28.0
unittest==1.1.0
json==2.0.9
flask==2.0.1  # If using Flask for API integration

Install them by running:
pip install -r requirements.txt
