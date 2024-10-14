# TaskMaster Backend


### Prerequisites
Make sure you have the following installed on your local machine:
- **Python** (preferably Python 3.x)
- **pip** (Python package manager)
- **virtualenv** (for creating virtual environments)
- **Git** (to clone the repository)

It’s a good practice to use a virtual environment to isolate your project dependencies. Run the following commands:

### Create a virtual environment:
```
python -m venv venv
```

### Activate the virtual environment:
- MacOS\Linux
```
source venv/bin/activate
```
- Windows
```
venv\Scripts\activate
```
### install dependencies
```
pip install -r requirements.txt
```


### Apply Database Migrations
```
python manage.py migrate
```

### Create Superuser
```
python manage.py createsuperuser
```

### Run the Development Server
```
python manage.py runserver
```
