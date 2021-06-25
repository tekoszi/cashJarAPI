# This is a JAR REST API
I have build a postman collection which enables you to verify all the queries, it is available here: https://www.getpostman.com/collections/c1fa7d9a0fb694afc87d <br>
Api is available at https://herokuapp.com <br>
# You can create and run local docker container for this application by running docker-compose up
### Avaiable Endpoints:<br>
# /jar<br>
Enables to add new jar
#### Available queries:<br>
POST with body:
```json
 {
    "name": "Jar 3",
    "cash": "1000",
    "currency": "USD"
}
```
example response:
```json
{
'Jar was added to the database'
}
```
# /jars<br>
#### Available queries:<br>
GET <br>
Enables to query for all of the jars in the DB
example response:
```json
{
    "jar_list": [
        {
            "id": 1,
            "name": "Jar 3",
            "cash": 1000.0,
            "currency": "PLN"
        },
        {
            "id": 2,
            "name": "Jar 3",
            "cash": 1000.0,
            "currency": "PLN"
        },
        {
            "id": 3,
            "name": "Jar 3",
            "cash": 1000.0,
            "currency": "USD"
        }
    ]
}
```
#
# /cashin<br>
Enables to cash in, using jar id, cash, currency
#### Available queries:<br>
POST with body:
```json
{"id": 1,
"cash": 4,
"currency": "PLN"
}
```

example responses: <br>
```json
{
    'There is no jar with that id''
}
```
```json
{
    'Select same currency jar'
}
```

#
# /withdraw<br>
Enables to withdraw, using jar id, cash
#### Available queries:<br>
POST with body:
```json
{"id": 1,
"cash": 2
}
```

example responses: <br>
```json
{
    'There is no jar with that id''
}
```
```json
{
    'Select same currency jar'
}
```

# /tranactions<br>
Enables to see all the transactions from all jars
#### Available queries:<br>
GET http://127.0.0.1:8000/transactions
```json
{
    "history": [
        {
            "id": 1,
            "jar": "Jar object (1)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 03:31:01.916602+00:00"
        },
        {
            "id": 2,
            "jar": "Jar object (1)",
            "name": "Cash in",
            "cash": 4.0,
            "date": "2021-06-23 03:32:24.340088+00:00"
        },
        {
            "id": 3,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 03:32:38.048865+00:00"
        },
        {
            "id": 4,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 03:32:39.235891+00:00"
        },
        {
            "id": 5,
            "jar": "Jar object (2)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 23:34:08.845157+00:00"
        },
        {
            "id": 6,
            "jar": "Jar object (3)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 23:34:16.806955+00:00"
        },
        {
            "id": 7,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 23:49:49.692555+00:00"
        }
    ]
}
```

GET http://127.0.0.1:8000/transactions/<jarID>
Example: http://127.0.0.1:8000/transactions/2
Enables to see all the transactions from specific jar

```json
{
    "history": [
        {
            "id": 5,
            "jar": "Jar object (2)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 23:34:08.845157+00:00"
        }
    ]
}
```

You can also add sorting by adding field name and if it should be descending.

Example:
http://127.0.0.1:8000/transactions/1/date/desc
http://127.0.0.1:8000/transactions/1/date
http://127.0.0.1:8000/transactions/date/desc
http://127.0.0.1:8000/transactions/date

It enables you to sort response by selected field and order:

```json
{
    "history": [
        {
            "id": 7,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 23:49:49.692555+00:00"
        },
        {
            "id": 6,
            "jar": "Jar object (3)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 23:34:16.806955+00:00"
        },
        {
            "id": 5,
            "jar": "Jar object (2)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 23:34:08.845157+00:00"
        },
        {
            "id": 4,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 03:32:39.235891+00:00"
        },
        {
            "id": 3,
            "jar": "Jar object (1)",
            "name": "Withdraw",
            "cash": 2.0,
            "date": "2021-06-23 03:32:38.048865+00:00"
        },
        {
            "id": 2,
            "jar": "Jar object (1)",
            "name": "Cash in",
            "cash": 4.0,
            "date": "2021-06-23 03:32:24.340088+00:00"
        },
        {
            "id": 1,
            "jar": "Jar object (1)",
            "name": "Jar created",
            "cash": 1000.0,
            "date": "2021-06-23 03:31:01.916602+00:00"
        }
    ]
}
```

# /transfer<br>
Enables to transfer cash between jars
#### Available queries:<br>
POST with body:
```json
{"from_id": 2,
"to_id": 3,
"cash": 1
}
```
###NOTE Only same currency jars can take place in transfer <br>
