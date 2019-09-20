# Django PfiProject in Docker

Using Django, a high-level Python Web framework that encourages rapid development and clean, pragmatic design, launch Lassaress web server.

## Table of contents

 - [TL;DR](#tldr)
 - [About](#about)
 - [Authentication using gmail](#auth)

## <a name="about"></a>About
Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source. Refer [Django](https://www.djangoproject.com/) for more details.

## <a name="tldr"></a>TL;DR
 I just want to run everything in Docker and don't care for an explanation

 1. Update `pfiProject/secrets/secrets.py` file 

     ```python
     # SECURITY WARNING: keep the secret key used in production secret!
     SECRET_KEY = 'xxxxxxxxxxxxxxxxxx'  # generate a secret key
     GOOGLE_MAP_API_KEY = 'xxxxxxxxxxxxxxxx'
     ```
 1. Update `quasar/src/assets/mbtoken.json` file

     ```python
     "MB_KEY":"YOU NEED TO REPLACE THIS WITH A MAP BOX TOKEN"

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
Configure Admin site with following info to enable GMAIL authentication.

1. Configure GMAIL API Cloud credentials
To allow users to log in with their Gmail credentials we need to register our new website with Google. Go to the Google Developers Console and enter the name of your new project. I’ve called this one “Django Login Mega-Tutorial.” The click on the “Create” button.

Google console
![Console](../../master/images/google-console.png)

You’ll be sent to the Google “API & Services” page. We want to use Gmail so click on it.
![Dashboard](../../master/images/google-dashboard.png)

The next screen shows all the details of the Gmail API. Click on the “Enable” button.
![GmailApi](../../master/images/gmail-api.png)

You may be asked for credentials at this point.
![credentials](../../master/images/credentials.png)

If so click on the “Create credentials” button. Make sure the fields are correct that we’re using the “Gmail API” with a “Web server” and accessing “User data.” Then click “What credentials do I need?”
![add-credentials](../../master/images/add-credentials.png)

Step 2 is to add a Name and Authorized Redirect URLs. The name I’ve just repeated the name of my overall project here. The redirect URL should be http://<domainname>/accounts/google/login/callback/. Then click on the “Create client ID” button.
  ![consent](../master/images/consent.png)  
  
Third and final step is to configure the consent screen. This is the information shown to users after they click on the login button. They’ll be redirected to a Google site that shows the Product name and asks if the site has permission to access their Google account.
![oauth-client-id](../../master/images/oauth-client-id.png)  

Now we have what we want: a client ID (I’ve hidden mine in red). I recommend downloading it and storing somewhere secure. You don’t want this information public.
![api-keys](../../master/images/api-keys.png) 
  
2. Configure Site and Social Apps
  Go to the Admin site http://<domainname>/admin and notice Allauth has added a number of new sections for us.
  Go into “Sites” on this page.
  ![site](../../master/images/site.png) 
  
  Click on the existing Domain Name of “example.com”. Update it so the “Domain name” is <domainname>.
  Click save.
  ![site-edit](../../master/images/site-edit.png) 
  
  Now for each third-party application we want to add we just need to click on the “Add” button next to “Social applications” under “Social Accounts.”
  ![social-app](../../master/images/social-app.png) 
   
On this page we need to select the provider (Google), provide a Name (Gmail), a Client ID, and a Secret Key. If you downloaded your API keys previously and open the file with a text editor you’ll see it is in JSON format and has both your Client ID and Client Secret. Enter both in here. Finally on the bottom of the page under “Sites” select “domainname” and click the -> arrow to add it to the Chosen Sites section. Now click on the “Save” button in the lower right of the screen.
