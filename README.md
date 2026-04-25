# Applied Databases Final Project

A conference management system for handling speakers, sessions, attendees, companies, and rooms. This project demonstrates integration with MySQL and Neo4j databases, allowing users to view and manage conference data through a menu-driven Python application.

## Application Menu Options

The main menu in `main.py` provides the following options:

| Option | Description                    |
|--------|--------------------------------|
| 1      | View Speakers & Sessions       |
| 2      | View Attendees by Company      |
| 3      | Add New Attendee               |
| 4      | View Connected Attendees       |
| 5      | Add Attendee Connection        |
| 6      | View Rooms                     |
| x      | Exit application               |

## Database Configuration

- Connection settings live in `db_config.py` (`DB_CONFIG`).
- `db_utils.py` reads that config and creates a PyMySQL connection with `DictCursor`.
- `cryptography` is required for MySQL `sha256_password` / `caching_sha2_password` auth.

## Quick Start

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Start services from `resources/`:
   - `docker compose -f resources/docker-compose.yml up -d`
   - automatically MySQL loads `resources/appdbproj.sql` on first container initialization.
   - automatically Neo4j loads `resources/appdbprojNeo4j.json` via `resources/neo4j_seed.sh`.
3. If needed, update DB settings in `db_config.py`.
4. Run the app:
   - `python3 main.py`

## Reseed Data

- MySQL init scripts run only when `mysql-data` is empty.
- To force a clean reload for both databases:
  - `docker compose -f resources/docker-compose.yml down -v`
  - `docker compose -f resources/docker-compose.yml up -d`
