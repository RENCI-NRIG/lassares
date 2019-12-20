# Django PfiProject in Docker

Using Django, a high-level Python Web framework that encourages rapid development and clean, pragmatic design, launch Lassaress web server.

## Table of contents

 - [TL;DR](#tldr)
 - [About](#about)
 - [Authentication using auth0](#auth)

## <a name="about"></a>About
Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source. Refer [Django](https://www.djangoproject.com/) for more details.

## <a name="tldr"></a>TL;DR
 I just want to run everything in Docker and don't care for an explanation

 1. Update `pfiProject/secrets/secrets.py` file 

     ```python
     # SECURITY WARNING: keep the secret key used in production secret!
     SECRET_KEY = 'xxxxxxxxxxxxxxxxxx'  # generate a secret key
     PUBHOST_URL = '127.0.0.1:8443' # URL of you website, for auth0
     AUTH0_DOMAIN= 'xxxxxxxxxx.auth0.com' # auth0 domain name
     API_IDENTIFIER= 'https://xxxxxxxx' # auth0 API Identifier
     ```
 1. Update `quasar/src/assets/secrets.json` file

     ```quasar
     "MB_KEY":"YOU NEED TO REPLACE THIS WITH A MAP BOX TOKEN"
     "CLIENT_ID":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", # auth0 client ID
     "AUTH0_DOMAIN":"xxxxxxxxxx.auth0.com", # auth0 domain name
     "API_IDENTIFIER":"https://xxxxxxxx" # auth0 API identifier
    ```
 3. Update `pfiProject/.env` file as per your need 

     ```
     # debug
     export DEBUG=true                 # set to false in production

     # database PostgreSQL
     export POSTGRES_PASSWORD=postgres
     export POSTGRES_USER=postgres
     export PGDATA=/var/lib/postgresql/data
     export POSTGRES_DB=postgres
     export POSTGRES_HOST=database
     export POSTGRES_PORT=5432
     export ADMIN_PWD=abcd1234!
     ```
 4. Update the `nginx` section of the `docker-compose.yml` file, if you want to run the operational version on your local machine. If you want to run the development version the docker-compose-dev.yml already has these changes.

     ```
     ...
       nginx:
         build:
           context: .
           dockerfile: nginx/Dockerfile
         image: quasar 
         container_name: quasar 
         ports:
           - 8080:80                    # change http port as needed
           - 8443:443                   # change https port as needed
         depends_on:
           - django
         volumes:
           - .:/code
           - ./static:/code/static
           - ./media:/code/media
           - /LOCAL_PATH_TO/your-ssl.crt:/etc/ssl/SSL.crt               # path to your SSL cert
           - /LOCAL_PATH_TO/your-ssl.key:/etc/ssl/SSL.key               # path to your SSL key
     ```
     If you don't have a valid SSL certificate pair, you can generate a self-signed pair using the `generate-certificates.sh` script

     ```console
     $ ./generate-certificates.sh
     Generating a 4096 bit RSA private key
     ...
     $ tree ./certs
     ./certs
     ├── self.signed.crt
     └── self.signed.key
     ```
 5. Run `docker-compose up -d` if you want to run the operational version, or run 'docker-compose -f docker-compose-dev.yml up -d' if you want to run the development version.

     ```console
     $ docker-compose -f docker-compose-dev.yml up -d
     Creating django   ... done
     Creating database ... done
     Creating quasar    ... done
     ```
    After a few moments the docker containers will have stood up and configured themselves.
 Naviage to [https://127.0.0.1:8443/](https://127.0.0.1:8443/) (or whatever you've configured your host to be).
 
## <a name="auth"></a>Authentication

The Lassaress application uses auth0.com for authentication. The frontend of this application has a sign in button: 
![sign-in](../../master/images/LassaresAppNotLoggedIn.png) 
which when used will bring up a auth0 login screen that gives you the choice of using your gmail account to login or to use a login provided by Lassares. 
![auth0-sign-in](../../master/images/auth0-sign-in.png)
Signing in will authenticate you for the frontend (quasar) of the application, giving you access to the data entry drawer on the left side of the app. Signing in will also authenticate you on the backend (django) of the app enabling you to entire data into the backend database through the frontend data entry drawer. 

To enable this authentication system you will first need to get an auth0 account, which you can learn more about getting an auth0 account by going to auth0.com. When you have an account you can create an auth0 custom API, which will enable you to create an API_IDENTIFIER for both the secrets.py and secrets.json files described above. You then need to create a auth0 single page application. 
![auth0-client](../../master/images/auth0-client.png)
This will provide you with a CLIENT_ID and AUTH0_DOMAIN, which you will use as described above. Finally, in the auth0 application you need to put the url, where the lassress app will be accesible, in "Allowed Callback URLs", "Allowed Web Origins", and "Allowed Logout URLs". 

For a deeper read into this subject check out [Building Modern Applications with Django and Vue.js by Ahmed Bouchefra](https://auth0.com/blog/building-modern-applications-with-django-and-vuejs/).

## <a name="webapp"></a>Web Application

After loging in the left side draw will appear which containes access to lists of measurements, a data entry form, and data upload interface. In addition to these, the image below points out other components for the web interface.
![web-interface](../../master/images/LassaresApp.png)
If you click on the "View List of Measurement" button a dropdown menu will appear, where you can select the instrument in which you want to see its measurements.
![list-choice](../../master/images/LassaresAppListChoice.png)
When you select an instrument a list of measurements for that instrument will appear, where you will be able to delete a measurement, edit or update the measurement, and change page.
![list-measurements](../../master/images/LassaresAppListMeasurements.png)
Inputs in "Input Measurement Data" form that have additional windows are "Instrument" input which has a dropdown menu to select the instrument.
![instrument-input](../../master/images/LassaresAppInstrument.png)
In the "Date" and "Time" inputs fields you can select the icon on the right side of the input field to get a calendar or clock popup.
![calendar-input](../../master/images/LassaresAppCalendar.png)
In the "Longitude" and "Latitude" fields you can select the globe, on the right side of the fields, to get a popup menu where you can select the longitude and latitude for you current physical location, or you can select a location on the map. When you select a location on the map a blue dot will appear beneath your mouse arrow, which you can move to the location for the measurement and then click. The longitude and latitude for that location will appear
in the appropriate fields.
![location-input](../../master/images/LassaresAppLegendSearchLocation.png)
The image above also shows the "legend" menu, and "search measurement" menu fully opened on the right side drawer.
The right side drawer also has a "state" menu which shows additional information about the map, including the coordinates of the device you are using, or you physical location, and the coordinates for a feature you select, which also show a popup. You can use the button in the bottom right hand corner to access the barchart selectionn tool, which enables you to create barcharts of data you selected.
![app-pop-state](../../master/images/LassaresAppPopState.png)
After selecting the barchart selection tool, a window will appear where you can first select the instrument in which you want to chart its data. You then select the "Draw Polygon Around Features" button. The will produce a blue dot beneath you mouse arrow, which you can use to draw a square around the instruments data you want to plot. Double click when you select the last corner of the square, and a popup showing the bargraph will appear.
![app-pop-up](../../master/images/LassaresAppPopUp.png)
