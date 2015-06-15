# Bagtrekkin API

## Postman Chrome Application

In order to play with API easily, you can use [Postman](https://www.getpostman.com). Install the app on your computer and let's get a ride on our API!

### Import data

1. Click on Settings on top-right corner.

![Postman Settings](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/img/postman_1_import.png)

2. Copy url of desired environement
  * Heroku [JSON](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/files/postman_bagtrekkin_heroku.json) URL
  * Local [JSON](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/files/postman_bagtrekkin_local.json) URL
  To use local you'll need to update `Authorization Header` by replacing `ApiKey username:api_key` according to your local account.

3. Import Data by pasting the URL

![Postman Settings](https://raw.githubusercontent.com/goujonpa/bagtrekkin/master/documentation/img/postman_2_paste.png)

## API Usage

How to communicate with the API the right way.

### Chekin

1. Check Log in credentials
  Use `Employee List` Postman request using Basic Authentication.
  Response should be `200 OK` if user is authorized and authenticated. If not, response is `401 UNAUTHORIZED`.
  Notice you retrieve a list of user objects containing only you.

2. Send Chekin data
  Use `Checkin Submit` Postman request using Basic Authentication.
  Response should be `201 CREATED`. Otherwise an error occured.
  First addition for a given passenger will take some time due to AlfredPNR API call. Be sure to set an enought high timeout (~3s).

### Ramp


