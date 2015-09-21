# Middle Man: a basic model generator

This server uses python 3.4

## Installation

using virtualenv:

virtualenv <destination> -ppython3

pip install -r <path_to_project>/requirements.txt

# Description

This is the basic architecture for an API which provides
a dynamic model framework and it's dynamically built relative REST endpoints. It's called Middle Man due lack of
creativity.

The server consists in two parts: api and application.

The api API will enable the developer to create dynamic models, assigning types to a specified project. This
 API will be accesed through a REST interface based on common username/password authorization.

## Running

python manage.py runserver

### Administrative API

Root endpoint:

/api/v1/

Enabled endpoints:

#### POST /api/v1/register
Registers a new user:
POST { "name" : "John", "email" : "doe@doe.com", "password" : "pocorn123" }

#### POST /api/v1/login
logs in a user:
POST { "email" : "doe@doe.com", "password" : "pocorn123" }

#### POST /api/v1/logout
logs out a user.

#### POST /api/v1/projects
Creates a new project:

````
POST { "name": "MyProject" }
````

#### GET /api/v1/projects
Lists all projects associated by a user:

````
GET
{
  "projects": [
    {
      "access_token": "20ab121ba0722f2c",
      "id": "eAx5236pZJ",
      "name": "MyProject"
    }
  ]
}
````

#### GET /api/v1/projects/\<hash-id\>
Lists all models associated by a project:

````
GET /api/v1/projects/eAx5236pZJ
{
  "access_token": "dc55415aed5651e4",
  "models": [
    {
      "attributes": [
        {
          "attrtype": "STRING",
          "id": "eAx5236pZJ",
          "name": "name"
        }
      ],
      "name": "Product"
    }
  ],
  "name": "MyProject2"
}
````

#### POST /api/v1/projects/\<hash-id\>/models
Adds models to a project:
````
POST /api/v1/projects/eAx5236pZJ/models
{
  "models": [
    {
      "attributes": [
        {
          "attrtype": "STRING",
          "name": "name"
        }
      ],
      "name": "Product"
    }
  ]
}
````


#### PUT /api/v1/projects/\<hash-id\>/models/\<hash-id\>
Updates a model:
````
POST /api/v1/projects/eAx5236pZJ/models/eAx5236pZJ
{
  "attributes": [
    {
      "attrtype": "STRING",
      "name": "new_attribute"
    }
  ]
}
````

#### POST /api/v1/projects/\<hash-id\>/deploy
Deploys a project. Will create all databases associated with each model.
````
POST /api/v1/projects/eAx5236pZJ/deploy
200 OK
````

#### POST /api/v1/projects/\<hash-id\>/undeploy
Undeploys a project. Will drop all databases associated with each model.
````
POST /api/v1/projects/eAx5236pZJ/undeploy
200 OK
````

### Application API

The application API will create common endpoints based on the specified models and provide basic authorization through
an Access Token associated with the project.

the endpoints will be accessed through this pattern:

Root endpoint:

/api/v1/apps/

Enabled endpoints for a specific app:

GET /\<model_name\>  - Fetches alls models

GET /\<model_name\>/{id} - Fetches a model by id

POST /\<model_name\> - Creates a new model

PUT /\<model_name\>/{id} - Edit a model

DELETE /\<model_name\>/{id} - Deletes a model

All acesses are validated through the X-Internal-AccessToken header, which can be recovered through the administrative API.

### Foretoughts:

* The application and the administration interface are running in the same server. This can be easily modified to specify
different servers. Also, all projects are on the same structure, which can be modified to enable per application as well
(on the case that the developer wants to run the model on his own server)

* The database models are created dynamically every time the server starts. This can be improved.

* There is no fine-grained acccess control. 

* Database errors are not properly handled on application endpoint.

## Tasks

- [x] Basic system structure
- [x] Models
    - [x] Administrative
    - [x] Application
- [x] Controllers
- [ ] Admin interface

@copywright Victor Vicente de Carvalho, 2015
