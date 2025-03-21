# CondoMe

**CondoMe** is an application that facilitates the organized and respectful use of shared spaces in condominiums.  
Administrators can set specific rules, enabling residents to book, reschedule, and cancel timeslots, ensuring transparency and fostering collective well-being.

## Features

- 📅 **Shared Space Scheduling**: Total control for residents and administrators over time slots.
- 🔄 **Customizable Rules**: Flexible rules to adapt to different condominium requirements.
- 📊 **Reports and Logs**: Keep track of bookings for transparency.
- 🌎 **Production-Ready**: Fully configured with Docker for portability and rapid deployment.

---

## Prerequisites

Make sure you have the following software installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- **Poetry** 
  - please, run the following command in order to instal poetry: 
    - curl -sSL https://install.python-poetry.org | python3 -
---

## Technologies Used

This project was built using:

- **Python 3.10** with **Django 5.1**
- **PostgreSQL** as the database
- **Docker & Docker Compose** for containerization and orchestration
- **Poetry 1.8.4** for dependency and virtual environment management

---
## Development Environment

This project is still in development. 

1. **Git Usage**  
   It is recommended to use **Git** on the host machine instead of within the container. This ensures a more seamless version control experience.

2. **VS Code Extensions**  
   You may not want to use them, but since the project is under development, several important extensions are used to improve the development experience. These include:
   - **Better Jinja**
   - **Black Formatter**
   - **Django**
   - **isort**
   - **Mypy Type Checker**
   - **Pylance**
   - **Python**
   - **Ruff**  
   
   More details about the extensions and their configuration can be found in the `pyproject.toml` file.

---
## Testing Strategy

This project embraces a balanced approach to testing, with test development occurring alongside the main codebase development. While strict Test-Driven Development (TDD) practices are still being progressively incorporated as the development team grows in expertise, we maintain a strong commitment to testing through:

- **Coverage Analysis**: Using the `coverage` library to track and improve test coverage
- **Continuous Testing**: Tests are developed in parallel with new features
- **Testing Tools**:
  - `pytest` for test execution
  - `coverage` for test coverage analysis
  - `pytest-django` for Django-specific testing utilities

### Running Tests

To run the tests and generate a coverage report:

```bash
# Activate virtual environment
poetry shell

# Run tests with coverage
poetry run coverage run -m pytest

# Generate coverage report
poetry run coverage report

# Generate HTML coverage report
poetry run coverage html
```

The HTML coverage report will be available in the `htmlcov/index.html` directory.

---
## Setting Up the Environment

1. **Create the `.env` file**  
   Copy the contents of `.env-example` into a new `.env` file:
   ```bash
   cp .env-example .env
   ```

2. **Fill in Environment Variables**  
   Edit the `.env` file to provide the required values ("CHANGE_ME") for the database and other application configurations.

---

## Running the Application

1. **Make "setup_postgres_volume.sh" executable**  
   ```bash
   chmod +x setup_postgres_volume.sh
   ```

2. **Execute "setup_postgres_volume.sh" script**  
   ```bash
   ./setup_postgres_volume.sh
   ```
3. **Initiate docker compose**
   ```bash
   docker compose up
   ```
4. **Install project dependencies**
   ```bash
   poetry install
   ```
5. **On terminal change directory to "src" folder (where manage.py file bellongs)**
   ```bash
   cd src
   ```
6. **DB Migrations**  
   **Inside src directory** on terminal, run both following commands to migrate DB Data:
   ```bash
   poetry shell
   poetry run python manage.py makemigrations
   poetry run python manage.py migrate 
   ```
7. **Create Superuser**
   **Inside src directory**, run the following commands (and follow the instructions)**
   ```bash
   poetry run python manage.py createsuperuser
   ```
8. **Collect Static Files**  
   **Inside src directory** on terminal, run the following commands to copy static files into specific folder:
   ```bash
   poetry run python manage.py collectstatic
   ```
9. **Run Server**  
   **Inside src directory** on terminal, run the following commands:
   ```bash
   poetry run python manage.py **runserver**
   ```
10. **Stop the Containers**  
   If needed, run the following command in order to stop all running containers and services:
   ```bash
   docker-compose stop
   ```
---
## Getting Started with the App

The first steps to start using the app are:

1. On the homepage's top menu, select **"Pricing"**.
2. Click on **"Sign up now"** or **"Get started"**.
3. Fill in the following fields: **First Name**, **Last Name**, **E-mail**, and **Confirm your e-mail**.  
   *(Note: Since the app is still in development, it is not necessary to provide payment details.)*
4. Click on **"Continue to checkout"**.
5. In your terminal, a message identical to what would be sent to a paying user's e-mail will appear, containing login instructions. Copy the login link and paste it into your browser.
6. Fill in the **registration form** to gain access to the program.
7. Complete the **login form**.

By following the steps above, you will obtain access to the system as a user belonging to the **"manager"** group. Keep in mind that there are two additional user groups available: **"caretaker"** and **"resident"**. Each of these three groups has specific permissions and privileges. You can find more details about these groups through the **Django Admin Panel**.

--- 

## Project Structure
```
This project follows a Django and Docker-based structure optimized for scalability and portability.
├── .env                                      # Environment variables configuration file
├── .gitignore                                # Git ignored files and directories
├── docker-compose.yml                        # Docker Compose configuration file
├── production_config/                        # To be used later on (for production environment)
├── data/                                     # Persistent data (e.g., database volumes)
├── static/                                   # Static files for the project
│   ├── htmlcov/                              # HTML reports for test coverage
│   ├── .coverage                             # Test coverage data
│   ├── .coveragerc                           # Test coverage configuration
├── src/                                      # Main Django project source code. Django apps are inside here.
├── LICENSE                                   # Project license
├── poetry.lock                               # Dependency lock file managed by Poetry
├── pyproject.toml                            # Main configuration file for Poetry and Python tools
├── pytest.ini                                # Pytest configuration file
├── README.md                                 # Project documentation
├── setup_postgres_volume.sh                  # Shell script. Sets up postgres volume before docker compose
```
---

## What's been done so far (MAR/2025)

- **prelogin** Basicaly static templates, basic info about the product, faq, prices, etc.
- **Registration and authentication** Although payment features are not implemented yet, a user may "buy" the product, register and login. This user will belong to the "manager" group. There are also two more groups (already programmed), "caretaker" and "resident", but they are not in use yet.
- **Condominium Setup** 
   ├── "manager" user may create the condominium object.
   ├── "manager" user may create block objects.
   ├── "manager" user may create apartment objects.
   ├── "manager" user may create common_area objects (IN PROGRESS).

---
## Main things that are yet to be done
- **Condominium Setup** 
   ├── "manager" user may define an create rules for reservation objects.
   ├── "manager" user may send invitations for caretakers and residents in order to join the system.
   ├── Program and configure Reports.

---

## License

This project is licensed under the MIT License. Check the section below for full license details.

---

## MIT License

```
Copyright (c) 2024 Rodrigo Lagrotta Silva Farah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

