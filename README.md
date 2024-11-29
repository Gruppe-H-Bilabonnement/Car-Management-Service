# Car-management-service
Very cool

python3 -m venv .venv
source .venv/bin/adctivate
pip install -r requirements

docker build -t car_management_service .

docker run -d -p 80:80 --name car_management_app_container car_management_service