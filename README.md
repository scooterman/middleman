# Middle Man: a basic model generator

This server uses python 3.4

## Installation

using virtualenv:

virtualenv <destination> -ppython3
pip install -r <path_to_project>/requirements.pip

# Description

This is the basic architecture for an API which provides
a dynamic model framework and it's dynamically built relative REST endpoints. It's called Middle Man due lack of
creativity.

The server consists in two parts: administrative and application.

The administrative API will enable the developer to create dynamic models, assigning types to a specified project. This
 API will be accesed through a REST interface based on common username/password authorization.

### Application API

The application API will create common endpoints based on the specified models and provide basic authorization through
an Access Token associated with the project.

the endpoints will be accessed through this pattern:

Root endpoint:

/api/middleman/v1/<APP-HASHID>/

Enabled endpoints for a specific app:

GET /<model_name>  - Fetches all model
GET /<model_name>/{id} - Fetches a model by id
POST /<model_name> - Creates a new model
PUT /<model_name>/{id} - Edit a model
DELETE /<model_name>/{id} - Deletes a model

APP-HASHID is a hash for the application ID with enough entropy that it will prevent unwanted web spiders to leech
the entire domain.

### Foretoughts:

* The application and the administration interface are running in the same server. This can be easily modified to specify
different servers. Also, all projects are on the same structure, which can be modified to enable per application as well
(on the case that the developer wants to run the model on his own server)

* The database models are created dynamically every time the server starts. This can be improved.

## Tasks

- [x] Basic system structure
- [ ] Models
    - [ ] Administrative
    - [ ] Application
- [ ] Controllers
- [ ] Admin interface

@copywright Victor Vicente de Carvalho, 2015