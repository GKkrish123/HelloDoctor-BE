# HELLO DOCTOR APP - BE (Python/FastAPI)

- This project contains APIs related to features of the HELLO DOCTOR APP - BE.

- Setting up the environment

  1. Visual Studio Code (`https://code.visualstudio.com/download`)
  2. Python (`https://www.python.org/downloads/`)
  3. SQL Server (Example: PostgreSQL,SQLite) (Tested with PostgreSQL)
  4. Clone this repository into VSCode, open the CMD terminal in the installed path (inside the `HelloDoctor-BE` folder)
  5. Create your own virtual environment.
  6. Run the command `pipenv install` to install all Python dependencies.

- Creating the mock database tables (MANDATORY IF YOU DON'T HAVE THE SPECIFIED TABLES IN YOUR SQL SERVER)
  1. Start your local SQL server.
  2. Apply your SQL server configuration in the `.env`.
  3. Run the command `python mock_db_tables.py` to create the mock tables in your specified SQL server.

# Training rasa language model

- The rasa language model configs are available in `rasa_data` folder.
- Modify as per your requirements.
- Run the below command for training the rasa model
- `rasa train --data app/rasa_data --out app/rasa_models --fixed-model-name nlu_engine --config app/rasa_data/config.yml --domain app/rasa_data/domain.yml`

# Deploying the APP server

- Run the command `python -m app.startup` to start the app.
  - http://localhost:5000/docs -> Swagger URL
  - http://localhost:5000/redoc -> Documentation URL
