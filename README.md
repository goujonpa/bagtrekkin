# Bagtrekkin [![Build Status](https://travis-ci.org/goujonpa/bagtrekkin.svg?branch=master)](https://travis-ci.org/goujonpa/bagtrekkin) [![Coverage Status](https://coveralls.io/repos/goujonpa/bagtrekkin/badge.svg)](https://coveralls.io/r/goujonpa/bagtrekkin)

Bagtrekkin is a full-stack application involving both hardware and software.


This project takes place in a Lean Startup course at the University Federal of Pernambuco.

## Install Bagtrekkin Django Application

The application uses [Django 1.8](https://docs.djangoproject.com/en/1.8/) as main framework, [PyJade](https://github.com/syrusakbary/pyjade) as template rendering tool, [Tastypie](https://django-tastypie.readthedocs.org/en/latest/) as API resource provider, [UiKit](http://getuikit.com/index.html) as front-end style and [PostgreSQL](http://www.postgresql.org/download/) as database server.

The whole server-side application is currently hosted on [Heroku](https://devcenter.heroku.com/articles/getting-started-with-django). It uses `web` Dynos to run [`Procfile`](https://github.com/goujonpa/bagtrekkin/blob/master/Procfile) in order to start [`Gunicorn`](http://gunicorn.org) server.

### Required

By following those steps, you'll install the application development environment

1. Clone Git repository:
  ```bash
  $ git clone git@github.com:goujonpa/bagtrekkin.git
  ```

2. Create a [`virtualenv`](https://virtualenv.pypa.io/en/latest/index.html) to host the application:
  You may need `sudo` to install `virtualenv` globally
  ```bash
  # install virtualenv tool manager via pip
  $ [sudo] pip install virtualenv
  # create a new virtualenv folder called venv
  $ virtualenv venv
  # activate your virtualenv!
  $ source venv/bin/activate
  ```

3. Install application dependencies via pip:
  **/!\ Be sure to have your virtualenv activated /!\\**
  This is stipulated by `(venv)` in front of your terminal prompt.

  ```bash
  (venv) $ pip install -r requirements.txt
  (venv) $ pip install -r requirements-dev.txt
  ```

  Currently both Tastypie and PyJade are installed from master development branch. When both package will be released in pip. Requirements must be edited.

  Read more about [Tastypie](https://github.com/django-tastypie/django-tastypie/issues/1293) and [PyJade](https://github.com/syrusakbary/pyjade/issues/185) support on Django 1.8.

4. Install postgres database server
  On Debian based distributions, install from package manager:
  ```bash
  $ apt-get install postgresql-9.4
  ```

  On Mac OS X, install from Homebrew, MacPorts or use Postgres.app:
  ```bash
  $ brew install postgresql
  ```

  Initiate a fresh database granted for current user:
  ```bash
  $ initdb -D /usr/local/var/postgres
  ```

  Launch postgresql:
  ```bash
  $ pg_ctl -D /usr/local/var/postgres start
  ```

  Create a new user named bagtrekkin with a password prompted:
  ```bash
  $ createuser -W bagtrekkin
  ```

  Create a dedicated database for bagtrakkin user:
  ```bash
  $ createdb -O bagtrekkin -E UTF8 bagtrekkin
  ```

  We can now try a connection to be sure all is properly setup:

  ```bash
  $ psql -U bagtrekkin bagtrekkin
  ```

5. Setup your local environment variables
  * Create a `.env` file in the same folder as `manage.py`:
  ```bash
  cat >> .env <<EOF
  WEB_CONCURRENCY=2
  DEBUG=TRUE
  ALLOWED_HOSTS=localhost
  DATABASE_URL=postgres://bagtrekkin:<your_db_password>@localhost:5432/bagtrekkin
  SECRET_KEY=<your_secret_key>
  EOF
  ```

  * Replace `<your_secret_key>` with one generated, for instance, using [MiniWebTool](http://www.miniwebtool.com/django-secret-key-generator/).

  * Replace `<your_db_password>` with the password you setup for postgres bagtrekkin user.

6. Run Migrations to create and feed your database:
  ```bash
  (venv) $ python manage.py migrate
  ```

8. Test if everything runs well:
  ```bash
  (venv) $ python manage.py runserver
  ```

  You are now fully operational to join the developer team :)

  **/!\ Please read carefully [How to Contribute](https://github.com/goujonpa/bagtrekkin/blob/master/documentation/CONTRIBUTE.md) /!\\**

### Optional

In order to get closer to production environment, you can run python server the same way as Heroku actually do: using [`foreman`](https://github.com/ddollar/foreman).

Simply install globally Ruby foreman `gem`:
  ```bash
  $ gem install -g foreman
  ```

And run server:
  ```bash
  $ foreman start
  ```

## Getting Started

### Create your Employee Account (i.e. User)

The first thing you need to do is create a new user using `Sign Up` form. It is also an `Employee`. Once your account is created, you basically want to be a superuser in order to access django admin interface.

Enter in python shell
  ```bash
  (venv) $ python manage.py shell
  ```

Import the corresponding module
  ```python
  >>> from django.contrib.auth.models import User
  ```

Get your user instance from the models
  ```python
  >>> foo = User.objects.get(username = '<your_username>')
  ```

Set your `is_staff` property to `True`
  ```python
  >>> foo.is_staff = True
  ```

Set your `is_superuser` property to `True`
  ```python
  >>> foo.is_superuser = True
  ````

Save your changes
  ```python
  >>> foo.save()
  ```

Verification : load again your user instance from the models
  ```python
  >>> foo = User.objects.get(username = '<your_username')
  ```

Check that your changes are applied (next instruction should return `True`)
  ```python
  >>> foo.is_superuser
  ```

### Doing the same on heroku

You will have to do the same to be superuser on heroku.
Repeat the procedure above.

You can know update your local environment variables by adding:
  ```bash
  cat >> .env <<EOF
  API_URL=bagtrekkin.herokuapp.com
  API_USER=<your_username>
  API_KEY=<your_api_key>
  EOF
  ```

* Replace `<your_api_key>` with the one generated by the application when you'll create your account.

* Replace `<your_username>` with the one used when you'll create your account.

This configuration is used by `rfid_reader.py` micro-client.

### Understand application structure

* [`arduino`](https://github.com/goujonpa/bagtrekkin/blob/master/arduino/) folder contains hardware code currently not being used by application server-side (i.e. Hosted on Heroku)

* [`bagtrekkin`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/) folder contains the server-side application.

  * [`migrations`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/migrations/) folder contains all migrations run using `migrate` management command. If you want to create new migrations, please read carefully [How to write Migrations](https://github.com/goujonpa/bagtrekkin/blob/master/documentation/MIGRATIONS.md).

  * [`static`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/static/) folder contains all static resources (i.e. js, css, fonts and img files used by the application).

  * [`templates`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/templates/) folder contains all templates written in [Jade](http://jade-lang.com) and live time compiled using [PyJade](https://github.com/syrusakbary/pyjade).

* [`documentation`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/documentation/) folder contains documentation about the project

## Git Documentation

1. [Getting Started](http://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
2. [Git Basics](http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
3. [Git Branches](http://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
4. [Git on the server](http://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols)
5. [Distributed Git](http://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
