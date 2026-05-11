# Applied Databases — Final Project

A small conference-management Python application that demonstrates working with both a relational database (MySQL) and a graph database (Neo4j). The app provides a simple menu-driven CLI to view and manage speakers, sessions, attendees, companies, rooms, and attendee connections.

This repository contains the application code, database seed files, Docker service definitions, and an innovation report (see `innovation.pdf`).

Key features
- Menu-driven CLI to inspect and manipulate conference data
- MySQL as the primary relational store (schema and seed SQL in `resources/appdbproj.sql`)
- Neo4j for relationship/graph queries (seed data `resources/appdbprojNeo4j.json` and `resources/neo4j_seed.sh`)
- Clean separation of concerns: DAO layer (`dao/`), services (`services/`), utils (`utils/`)

Tech stack
- Python 3.10+ (project was developed/tested on macOS)
- PyMySQL (MySQL client)
- Neo4j (Bolt) via appropriate Python driver
- Docker Compose for running MySQL and Neo4j locally

Quick start (local development)
1. Create and activate a Python virtual environment (recommended):

   python3 -m venv .venv
   source .venv/bin/activate

2. Install Python dependencies:

   pip install -r requirements.txt

3. Start the database services (from project root):

   docker compose -f resources/docker-compose.yml up -d

   Notes:
   - On first run MySQL initialization will load `resources/appdbproj.sql` into the container volume.
   - The compose file configures Neo4j authentication via `NEO4J_AUTH` and includes a healthcheck so a `neo4j-seed` helper service can wait until Neo4j is ready before running the seeding script.
   - Neo4j is seeded using `resources/neo4j_seed.sh`, which imports `resources/appdbprojNeo4j.json` once Neo4j is healthy.
   - If the Neo4j data volume is removed the container will be reinitialized and reseeded on next startup (the same applies to MySQL when its data volume is removed).

4. If you need to change database connection settings, edit `config/db_config.py`.

5. Run the application:

   python3 main.py

Application menu (in `main.py`)
- 1 — View Speakers & Sessions
- 2 — View Attendees by Company
- 3 — Add New Attendee
- 4 — View Connected Attendees
- 5 — Add Attendee Connection
- 6 — View Rooms
- 7 — Update Attendee Details (update name, DOB, gender, company)
- 8 — Delete Attendee (removes attendee from MySQL and Neo4j after confirmation)
- 9 — Show Connected Attendees in the same Session (displays connected attendees who share at least one session; includes session title, date, speaker, and room)
- x — Exit application

Project layout (important files/folders)
- `main.py` — CLI entry point
- `config/db_config.py` — DB configuration constants
- `dao/` — Data Access Objects (MySQL & Neo4j helpers)
- `services/` — Business logic built on top of DAOs
- `resources/` — SQL/JSON seed files and Docker Compose
  - `appdbproj.sql` — MySQL schema + seed data
  - `appdbprojNeo4j.json` — Neo4j seed JSON
  - `docker-compose.yml` — Docker Compose services for MySQL & Neo4j
  - `neo4j_seed.sh` — helper script to seed Neo4j
- `utils/` — helper utilities and enums

Database configuration details
- Default connection values are stored in `config/db_config.py`. `utils/db_utils.py` reads these and creates a PyMySQL connection with DictCursor. If your MySQL user uses modern authentication methods (`sha256_password` / `caching_sha2_password`) ensure the `cryptography` package is installed (it is included in `requirements.txt`).

Seeding and reloading data
- MySQL init scripts are executed only when the MySQL data volume is empty. To force a fresh reload of both database containers and their data volumes:

  docker compose -f resources/docker-compose.yml down -v
  docker compose -f resources/docker-compose.yml up -d

Development notes
- The codebase separates raw DB operations (DAOs) from higher-level application logic (services).
- If you add new DB fields or change schema, update `resources/appdbproj.sql` and re-seed the database.

About the innovation report
- See `innovation.pdf` in the project root for the project's new features.

Troubleshooting
- If the app cannot connect to MySQL, confirm the container is running and `config/db_config.py` host/port/credentials match the running container.
- If Neo4j imports fail, check permissions/credentials and that Neo4j container is up.