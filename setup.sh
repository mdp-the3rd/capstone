#!/bin/bash


export AUTH0_DOMAIN="dev-udnd.uk.auth0.com"
export API_AUDIENCE="capstone"
export AUTH0_CLIENT_ID="TF3HKFpCkVVeIEGFiGRP1kXqGcaDkWc5"
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres"
export EXCITED="true"

echo "setup.sh script executed successfully!"