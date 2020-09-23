## Flask Restful API

This is a small example of a Flask API which has a couple endpoints in which you can perform full CRUD. The two endpoints are:
* ```/budgetitems```
* ```/lineitems```
  * ```BudgetItems``` allows you to create a new budget, read all or any specfic budget, add line items to the budget, and delete the budget. When viewing a specific budget, the endpoint will also respond with the corresponding ```lineitems``` extended on the budget instance.
  *  ```Lineitems``` has similar functionality, allowing you to create a new line item and assign it to a budget, edit a line item, and delete a line item.


## Set Up/ Running Project

1. ```git clone git@github.com:MattCrook/flaskapi.git```
2. ```cd flaskapi```
3. ```docker build -t flaskapi:latest .```
4. ```docker run -it -d -p 5000:5000 flaskapi```


### Technology Used

* Flask
* SQLAlchemy
* Marshmallow
* Docker
* Docker-compose
* Flask-Admin
* Migrations

## Flask Admin
To view the Admin Dashboard, navigate to the below link:
* http://localhost:5000/admin/


## Api Endpoints
* http://localhost:5000/api/budgetitems
* http://localhost:5000/api/lineitems


## Scripts / CRUD
To popluate the database and get started making some POST requests, you can either open post man, or run the below ```curl``` requests.

**Create Some Budgets**
* ```curl http://localhost:5000/api/budgetitems -X POST -H "Content-Type: application/json" -d '{"budget_name": "Construction Budget", "description": "Sample Line Item Budget for Construction"}'```
  
* ```curl http://localhost:5000/api/budgetitems -X POST -H "Content-Type: application/json" -d '{"budget_name": "Construction Budget Number 2", "description": "Line Item Budget for Construction Budget 2"}'```

* ```curl http://localhost:5000/api/budgetitems -X POST -H "Content-Type: application/json" -d '{"budget_name": "Construction Budget Number 3", "description": "Line Item Budget for Construction Budget 2"}'```

Sample response object should look like the following:

```sh
{
  "budget_name": "Construction Budget",
  "description": "Sample Line Item Budget for Construction",
  "id": 1
}
```


**Add some Line Items to the newly created Budgets**

* ```curl http://localhost:5000/api/lineitems -X POST -H "Content-Type: application/json" -d '{"budget_id": 1, "cost": "2000", "name": "Plans and Specs", "percent_of_total": "2"}'```

* ```curl http://localhost:5000/api/lineitems -X POST -H "Content-Type: application/json" -d '{"budget_id": 1, "cost": "3000", "name": "Permits, Inspections, Fees", "percent_of_total": "3"}'```

* ```curl http://localhost:5000/api/lineitems -X POST -H "Content-Type: application/json" -d '{"budget_id": 1, "cost": "1000", "name": "Survey", "percent_of_total": "1"}'```

Sample response object of POST Line Item should look like the following:
```sh
{
  "budget_id": 1,
  "cost": "2000",
  "id": 1,
  "name": "Plans and Specs",
  "percent_of_total": "2"
}
```

### Read Budget
To read all budgets (or line items):
* ```curl http://localhost:5000/api/budgetitems```
* ```curl http://localhost:5000/api/lineitems```

Or, to GET single Budget showing all line items belonging to that budget:
* ```curl http://localhost:5000/api/budgetitems/1```

Sample Respose:
```sh
{
  "budget_name": "Construction Budget",
  "description": "Sample Line Item Budget for Construction",
  "id": 1,
  "lineitems": [
    {
      "budget_id": 1,
      "cost": "2000",
      "id": 1,
      "name": "Plans and Specs",
      "percent_of_total": "2"
    }
  ]
}
```
### Update Budget or Line Item

**Update the first budget we created:**
* ```curl http://localhost:5000/api/budgetitems/1 -X PUT -H "Content-Type: application/json" -d '{"budget_name": "Updated Construction Budget", "description": "Updated Sample Line Item Budget for Construction"}'```


**Update the first Line Item we Created:**
* ```curl http://localhost:5000/api/lineitems/1 -X PUT -H "Content-Type: application/json" -d '{"budget_id": 1, "cost": "5000", "name": "Updated Line Item", "percent_of_total": "100"}'```

Sample response from updating a budget:
```sh
{
  "budget_name": "Updated Construction Budget",
  "description": "Updated Sample Line Item Budget for Construction",
  "id": 1
}
```
### Delete a Budget or Line Item
You can delete a single line item from a budget, or delete a budget entirely, causing a cascading delete of deleting all line items tied to that budget as well. 

* ```curl http://localhost:5000/api/budgetitems/1 -X DELETE -I```
* ```curl http://localhost:5000/api/lineitems/1 -X DELETE -I```

Sample response:
```sh
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/0.16.1 Python/3.7.3
Date: Wed, 23 Sep 2020 16:40:50 GMT
```
