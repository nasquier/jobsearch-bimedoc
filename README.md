**<h1>Bimedoc directory API</h1>**

**<h2>Presentation</h2>**

<p>
This Django API allows a user to do several things (see <a href=./instructions.pdf>instructions.pdf</a> for details about this exercize):

- search Bimedoc's cloud based health care workers directory
- add a worker and its related organization (if any) to a database
- display the organizations saved in the database so far, as well as workers registered with no organization

</p>

<p>
In addition to the mandatory endpoints required for this exercize, a strandard REST CRUD API has been implemented to manipulate the workers entries, as well as a route to list all workers without their organization.
</p>

<p>
The use of the Django REST framework allows us to interact with the database with a GUI.
</p>

___

**<h2>Installation</h2>**

You only need **pip** and **python3** to install the project depencies on your local setup and launch the server.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

To initiate our database, we do our first data migration:

```bash
python3 manage.py migrate --run-syncdb
```

To navigate through our database with a GUI, we can create a super user via this prompt:

```bash
python3 manage.py createsuperuser
```


To run the Django server locally, we use:

```bash
python3 manage.py runserver
```

The server should now be running and you should be able to access the  <a href=http://localhost:8000/admin> admin back office </a> with the previously entered credentials.

___

**<h2>Using the API</h2>** 

You can use your browser or your favourite API client to make simple HTTP requests to the server.


***<h3>Search Bimedoc's directory</h3>***

This endpoint is located at http://localhost:8000/search/something/.  
*something* can be any string you want to search through the AWS cloud search API. The endpoint only accepts GET requests and returns a JSON list of health care workers, with the mandatory and optionnal fields our database will consume.

***<h3>Add health care worker to the database</h3>***
You can copy one the previously searched workers data and send it as is (JSON data) to http://localhost:8000/add/. This endpoint will create a corresponding health care worker entry in our database if possible. If the data had a *finess* field, it will automatically create the corresponding organization entry with the name entered in the optionnal *registered_name* field.
The endpoint only accepts POST requests and the body data must be JSON.

***<h3>Display health care workers in the database</h3>***
To list all organization and their workers saved in the database so far, visit http://localhost:8000/list/. It will return a JSON object of all organizations and theirs workers identified by the organization's finess. The workers with no known organization should be at the top of the object.

___

**<h2>Bonus routes</h2>** 

Two other endpoints are available to showcase what the Django REST framework is capable of in terms of GUI.  

You can list all the workers in your database at http://localhost:8000/healthcareworkers/ (GET request only).

A true REST CRUD API is also available at http://localhost:8000/healthcareworker/rpps_number/ where *rpps_number* is the rpps_number of the worker you try to manipulate. You can use this route and the Django REST framework GUI to manage workers with the standard REST protocol for **CRUD**:
- POST to **c**reate
- GET to **r**ead
- PUT to **u**pdate
- DELETE to **d**elete

The parameters are like the ones in the route */add/* discussed sooner and must be formatted as JSON in the body request. 

The *rpps_number* field of the body of the POST request will be ignored as the one in the endpoint route will be taken for the creation of the worker.

**IMPORTANT**: This route doesn't create or manage organization entry.