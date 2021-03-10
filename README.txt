Useful functions: 

    python3 manage.py runserver
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser

When updating database make sure to run:

    python3 manage.py makemigrations
    python3 manage.py migrate

    If there are errors and you want fresh start:
        clear the "migrations/" folders  
        remove "db.sqlite3"
        run the above commands

    If you want a model to appear on the admin page please 
    register it on "admin.py"

Accesing admin page (CRUD GUI):

    Simply navigate to: 
        http://127.0.0.1:8000/admin
        https://cardcierge.herokuapp.com/admin

    use "createsuperuser" command if you forgot username/password


Useful resources: 

    Using Serializers:
    https://www.django-rest-framework.org/api-guide/serializers/

    Views/Viewsets: 
    Views:  https://www.django-rest-framework.org/api-guide/views/
    Viewsets: https://www.django-rest-framework.org/api-guide/viewsets/
    Documentation of both: http://www.cdrf.co

    Vishnu's Notebook: 
    https://docs.google.com/document/d/1H3MHndwjS0nKSu0Bx3I50-jvWCUWCWJZJhl908ahjys/edit