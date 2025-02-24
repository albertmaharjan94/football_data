# Football Data On-Prem Setup Guide

This guide explains how to set up and run the Football Data project on your local machine using Docker and Docker Compose. Follow the steps below to clone the repository, build and run the containers, and configure your environment.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Cloning the Repository](#cloning-the-repository)
3. [Building and Running the Containers](#building-and-running-the-containers)
4. [Configuration Settings](#configuration-settings)
5. [Accessing the Database](#accessing-the-database)
6. [Adding and Registering a Server](#adding-and-registering-a-server)
7. [On Connection Details](#on-connection-details)
8. [Conclusion](#conclusion)

---

## Prerequisites

- **Docker**  
  For installation and more details, visit the [Docker Desktop Documentation](https://docs.docker.com/desktop/).

- **Docker Compose**

Ensure Docker and Docker Compose are installed and properly configured on your system.

---

## Cloning the Repository

Open your terminal and execute the following commands:

```bash
git clone https://github.com/albertmaharjan94/football_data
```

## Building and Running the Containers
```bash
cd football_data
docker compose up -d --build
```
This will scrape the data daily at 12:00, if your machine and docker containers are up, it will automatically scrape the data.

## Configuration Settings
There are few configuration changes

Host: 
```copy
localhost
```
Port: 
```copy
5432
```
Database: 
```copy
football_db
```
Username:
```copy
football_read
```
Password:
```copy
footBallIreAD
```
Note: Go through the init.sql for more information about users
---

## Accessing the Database

You can also check your database using the following URL:
```copy
http://localhost:15433
```
Login with:
Email: 
```copy
admin@softwarica.com
```
Password: 
```copy
pgF00tB@!!AdM!nn
```
---
## Adding and Registering a Server

Add the Server

<img width="595" alt="Screenshot 2025-02-24 at 2 57 30 PM" src="https://github.com/user-attachments/assets/67255282-f58f-4928-96bc-f74815d9625e" />

---
Register a Server

<img width="691" alt="Screenshot 2025-02-24 at 2 58 03 PM" src="https://github.com/user-attachments/assets/8899c16c-09d6-49f4-8991-96f4420d587a" />

---
On Connection

<img width="691" alt="Screenshot 2025-02-24 at 2 59 41 PM" src="https://github.com/user-attachments/assets/fbddff4d-6c68-43e6-a485-373278c8e319" />

---

## On Connection Details

Host: 
```copy
database
```
Port: 
```copy
5432
```
Database: 
```copy
football_db
```
Username:
```copy
football_read
```
Password:
```copy
footBallIreAD
```

## Conclusion
You now have the Football Data project up and running on your local machine. The system is configured to automatically scrape data daily at 12:00, provided your Docker containers are active. For further customization or troubleshooting, refer to the documentation within the repository and the configuration files provided.
