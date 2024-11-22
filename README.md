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

---

## Setting Up the Environment

1. **Create the `.env` file**  
   Copy the contents of `.env-example` into a new `.env` file:
   ```bash
   cp .env-example .env
   ```

2. **Fill in Environment Variables**  
   Edit the `.env` file to provide the required values for the database and other application configurations.

---

## Running the Application

1. **Build and Start the Containers**  
   Run the following commands to build the Docker image and bring up the containers:
   ```bash
   bash
   ./start.sh
   ```

2. **Stop the Containers**  
   To stop all running containers and services:
   ```bash
   docker-compose down
   ```

---

## Creating the Superuser

After the application is running, create a Django superuser to access the admin panel:

1. Run the following command:
   ```bash
   docker exec -it condo_me_web_container python3 /app/src/manage.py createsuperuser
   ```

2. Follow the on-screen instructions to set up the email, username, and password for the superuser.

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

This project follows a Django and Docker-based structure optimized for scalability and portability.

```
├── src/                        # Django project source code
│   ├── project/                # Main project configurations
│   ├── apps/                   # Django apps
│   ├── manage.py               # Django management script
├── data/                       # Persistent data (volumes for static/media/db)
│   ├── web/                    # Static and media files
│   ├── postgres/               # PostgreSQL database data
├── docker-scripts/                     # Docker-related scripts
├── Dockerfile                  # Main Dockerfile
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment files
│   ├── .env-example/           # Example environment configuration
└── README.md                   # This file
```

---

## Technologies Used

This project was built using:

- **Python 3.10** with **Django 5.1**
- **PostgreSQL** as the database
- **Docker & Docker Compose** for containerization and orchestration
- **Poetry** for dependency and virtual environment management

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

