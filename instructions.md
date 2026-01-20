```markdown
# Weekly Project: Mini Data Engineering Pipeline – API & SQL Focus

## Setup (bash, Python virtual environment)

```bash
# create a virtual environment
python -m venv .venv

# activate the virtual environment (bash)
source .venv/bin/activate

# install your project dependencies, for example:
# pip install -r requirements.txt
```

---

## Project Overview

This project focuses on building a **service-based mini data engineering pipeline** that simulates a real-world data pipeline for weather intelligence.

The emphasis is on:

- **Clear service design**
- **Transparent and traceable data flow**
- **Thoughtful use of `pandas` and SQL**
- **Translating simple business questions into HTTP endpoints**

The system you build acts as a **central environmental data infrastructure** for an operational planning unit (“Tactical Weather Intelligence”).  
It collects raw weather data, cleans and organizes it, stores it in a relational database, and exposes simple queries that provide a reliable environmental picture for decision-making.

---

## System Context – Tactical Weather Intelligence

The Tactical Weather Intelligence unit is responsible for understanding the **air and environmental space** in which operations take place.

- It does **not** engage in direct combat.
- It focuses on **environmental intelligence collection** supporting tactical decisions:
  - Timing of movement
  - Assessment of environmental risks
  - Adapting activity to actual weather conditions

Even small changes in **wind** or **temperature** can affect accuracy, stability, and maneuverability of operational systems.  
Your system serves as a **core data backbone** that:

1. Centralizes raw weather data.
2. Cleans and normalizes it.
3. Stores it in a well-structured database.
4. Exposes basic queries that answer environmental questions reliably and accessibly.

---

## Data Workflow – High-Level

In almost any real-world data engineering system, the data workflow can be divided into three foundational stages:

1. **Data Ingestion**
2. **Data Transformation / Cleaning**
3. **Data Preparation for Storage & Use**

### 1. Data Ingestion

*Goal:* **Collect and ingest data** from an external source into your system.

- Bring data from an **external source** into the system *as-is*.
- At this stage, the data is:
  - Raw
  - Not ordered
  - Not yet suitable for direct analytical use

### 2. Data Transformation / Cleaning

*Goal:* **Fix and normalize data** so it becomes clean and consistent.

- Fix basic data issues:
  - Formats
  - Types
  - Missing values
  - Duplicates
- The aim is **not** to analyze the data yet, but to turn it into:
  - Clean
  - Consistent
  - Clear

### 3. Data Preparation

*Goal:* **Prepare data for relational storage and future queries.**

- Structure the data so it fits a **tabular database schema**.
- Ensure the data supports **simple, reliable SQL queries**.
- In this project, **each stage is implemented in a separate service**, so you can:
  - Understand what happens to the data at each step.
  - Understand why each stage is important on its own.

---

## External Data Source – Open-Meteo Weather API

This project uses the **Open-Meteo Weather API** as an external weather data provider.

- It is an **HTTP API** that provides **real weather data** for locations around the world.
- It returns data (e.g., temperature, wind speed, humidity) in **JSON format**.
- It **does not require**:
  - API key
  - Special registration
- It is a **public, free, accessible service** suitable for server-side systems like the one you are building.

**Official documentation:**  
[Open-Meteo Weather API Docs](https://open-meteo.com/en/docs)

In this project:

- The **Ingestion Service (Service A)** calls this API.
- The data returned by the API is used as the **basis for:**
  - Data Cleaning
  - Data Preparation
  - Storage in **MySQL**
  - Subsequent **SQL queries** that answer simple environmental questions.

---

## System Architecture (High Level)

High-level system flow:

```text
External Data Source (Open-Meteo API)
            ↓
Service A – Data Ingestion
            ↓
Service B – Data Cleaning & Normalization
            ↓
Service C – Data Storage & Queries
```

**Key principles:**

- Each service is:
  - **Independent**
  - Has a **clear responsibility**
  - Communicates with other services **only via HTTP**

---

## Service A – Data Ingestion

### Responsibility

Service A is responsible for **fetching data from the external weather service** and passing it into your system.

### Endpoint

- `POST /ingest`

### Ingestion Logic

The ingestion mechanism is **based on a predefined list of locations**.

For each location, the service performs:

1. **Geocoding**
   - Translate the **location name** into **coordinates (latitude/longitude)**.
2. **Hourly Weather Fetch**
   - Fetch **hourly weather data** for those coordinates.

All results from these external calls are:

- Collected into **one list** with a **uniform structure**.
- Returned as the **input to the next processing stage**.

**Important constraints for Service A:**

- **No cleaning**
- **No calculations**
- **No change of structure** beyond organizing responses into a uniform list

You may receive **example code snippets** for:

- The geocoding API call
- The weather API call

They act only as a **starting point**.  
You are responsible for:

- Integrating the logic
- Managing the loop over locations
- Returning the final aggregated output

---

## Service B – Data Cleaning & Normalization (pandas)

### Responsibility

Service B prepares **raw, ingested data** for storage in a **tabular database**.

### Endpoint

- `POST /clean`

### Core Behavior

`POST /clean`:

- Accepts **raw data** exactly as it was produced by the Ingestion stage.
- Converts it into data that is:
  - **Clean**
  - **Consistent**
  - **Tabular and clear**

At this stage, the data moves from:

- A complex, multi-location **JSON structure**  
  → to a **flat, consistent representation** suited for:
  - Database storage
  - SQL queries

### Work Performed in Service B

- Iterate over the **list of ingested data**.
- Build **one unified `pandas.DataFrame`** from all locations and records.
- Handle **basic data-quality issues**:
  - Ensure fields are present and correctly typed.
  - Prepare the structure so it can be passed to the **Storage service**.

After cleaning and normalization, you must **add two simple derived columns** to the DataFrame:

#### 1. `category_temperature` – Temperature Category

A textual description of the temperature conditions (in °C):

- Temperature **above 25°C** → `"hot"`
- Temperature **between 18°C and 25°C (inclusive)** → `"moderate"`
- Temperature **below 18°C** → `"cold"`

This is a **coarse descriptive category**, not a scientific index or forecast.

#### 2. `status_wind` – Wind Status

A simple description of wind strength, based on **wind speed**:

- Wind speed **above 10** → `"windy"`
- Wind speed **up to 10** → `"calm"`

> Units are taken **as-is from the API** (no unit conversion is required).

### Important Implementation Note

At this stage you work with a `pandas.DataFrame`, but:

- You **cannot send a DataFrame directly** between services over HTTP.
- Part of your task is to decide how to **serialize the cleaned data** into a standard format suitable for HTTP transport, such as:
  - **JSON**

Choosing and implementing such a representation is **intentional**, simulating a real-world data engineering problem.

---

## Service C – Data Storage & Light Analytics (SQL)

### Responsibility

Service C handles:

1. **Storing the cleaned data** in a MySQL database.
2. Providing **simple analytical queries** over that data.

---

### Storage Endpoint

- `POST /records`

At this stage, the data received from Service B is:

- Stored in **MySQL** in a **flat, uniform table**.
- Each row represents **one weather measurement**:
  - For **one location**
  - At **one point in time**
- No additional calculations or logical transformations are done here.

#### Table Schema – `records_weather`

| Column                | Type          | Description                                   |
|-----------------------|---------------|-----------------------------------------------|
| `id`                  | INT, PK, AUTO_INCREMENT | Surrogate primary key               |
| `timestamp`           | DATETIME      | Measurement time                              |
| `location_name`       | VARCHAR       | Human-readable location name                  |
| `country`             | VARCHAR       | Country name or code                          |
| `latitude`            | FLOAT         | Latitude                                      |
| `longitude`           | FLOAT         | Longitude                                     |
| `temperature`         | FLOAT         | Measured temperature                          |
| `wind_speed`          | FLOAT         | Measured wind speed                           |
| `humidity`            | INT           | Measured humidity                             |
| `temperature_category`| VARCHAR       | Derived category (hot / moderate / cold)      |
| `wind_category`       | VARCHAR       | Derived wind status (calm / windy)           |

> Note: `temperature_category` and `wind_category` correspond to the derived logic from Service B  
> (`category_temperature` and `status_wind` in the DataFrame stage).

---

### Analytics Endpoints (Light Analytics)

Each analytics endpoint answers **one simple business question**.

#### 1. `GET /records`

- **Description:**  
  Retrieve **raw records** with optional filtering (e.g., by time range or by region).
- **Business question:**  
  *“Which data was collected during a specific time period or in a specific region?”*

#### 2. `GET /records/count`

- **Description:**  
  Return the **number of records per region**.
- **Business question:**  
  *“From which regions was the most information collected?”*

#### 3. `GET /records/avg-temperature`

- **Description:**  
  Return the **average temperature per region**, based on the data currently in the system.
- **Business question:**  
  *“What is the average measured temperature in each region?”*

#### 4. `GET /records/max-wind`

- **Description:**  
  Return the **maximum wind speed per region**, based on the data currently in the system.
- **Business question:**  
  *“What was the highest wind speed measured in each region?”*

#### 5. `GET /records/extreme`

- **Description:**  
  Return **locations classified as operationally challenging**, based on the most common combination of categories:
  - **Hot with calm winds** → `hot` & `calm`
  - **Cold with strong winds** → `cold` & `windy`
- **Business question:**  
  *“In which locations were measured extreme conditions that would be operationally challenging?”*

---

## Summary

This project guides you through building a **three-service data engineering pipeline**:

1. **Service A** – Ingests raw weather data from Open-Meteo for a list of locations.
2. **Service B** – Cleans and normalizes the data with `pandas`, adds simple descriptive categories, and prepares it for storage.
3. **Service C** – Stores the data in MySQL and exposes basic SQL-backed HTTP endpoints for environmental insights.

The architecture emphasizes:

- **Clear responsibilities per service**
- **HTTP-only communication**
- **Transparency of data flow**
- **Direct mapping from business questions to API endpoints**
```

Would you like me to adapt this README further—for example, add concrete bash commands for your actual project layout (folders, main scripts, Docker usage, etc.) or tailor the setup section to your exact Python version and tooling?