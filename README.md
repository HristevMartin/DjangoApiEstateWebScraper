UK Estate Property API
======

Introduction
------------    

The UK Estate Property API is a Django-based RESTful API designed for managing real estate data. It features a variety of endpoints for handling property listings, inquiries, and area sorting, as well as supporting advanced functionalities like pagination and searching items. The API integrates user authentication mechanisms, including Google OAuth, ensuring secure access. Built using the Django REST Framework, it encompasses robust features such as data filtering and custom token-based authentication, 

***
Features
------------
* CRUD operations for property listings.
* Inquiry creation for properties.
* Sorting and filtering of property data.
* Unique area listing.
* User registration and authentication, including Google OAuth.
* Token-based authentication with JWT (JSON Web Tokens).
* Blacklisting of JWT tokens upon logout.

Technologies Used
------------

* Django and Django REST Framework
* MySQL (or specify your database)
* JWT for token-based authentication
* Google OAuth for authentication

Installation and Setup
------------
* Clone the repository:
```
git clone https://github.com/HristevMartin/DjangoApiEstateWebScraper.git
```
* Create a virtual environment:
```
python -m venv venv
```
* Activate the virtual environment:
```
venv\Scripts\activate
```
* Install the dependencies:
```
pip install -r requirements.txt
```
* Create a database and add the credentials to the settings.py file:


Endpoints
------------

POST /api/register: Register a new user.
POST /api/token: Obtain JWT tokens.
GET /api/properties: List all properties.
.......
