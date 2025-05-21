run ./build.sh to create container and launch app

Directory Structure
=============================================================
- tests.sh: used to run app container and run tests.py for testing via CI/CD
- tests.py: contains the unit tests
- app.py: contains the flask application server code
- db.py: contains the sqlite3 database server code
- curls: directory containing some curl commands used during initial manual testing
- requirements.txt, Dockerfile, docker-compose.yml, .github/workflow/build.yml etc are self explanatory
