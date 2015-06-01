# Bagtrekkin

Bagtrekkin is a full-stack application involving both hardware and software.

This project takes place in a Lean Startup course at the University Federal of Pernambuco.

## Install Bagtrekkin Django Application

The application uses [Django 1.8](https://docs.djangoproject.com/en/1.8/) as main framework, [PyJade](https://github.com/syrusakbary/pyjade) as template rendering tool, [Tastypie](https://django-tastypie.readthedocs.org/en/latest/) as API resource provider, [UiKit](http://getuikit.com/index.html) as front-end style and [PostgreSQL](http://www.postgresql.org/download/) as database server.

The whole server-side application is currently hosted on [Heroku](https://devcenter.heroku.com/articles/getting-started-with-django). It uses `web` Dynos to run [`Procfile`](https://github.com/goujonpa/bagtrekkin/blob/master/Procfile) in order to start [`Gunicorn`](http://gunicorn.org) server.

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
	$ initdb -D /usr/local/var/postgres -E utf8
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
	DATABASE_URL=postgres://bagtrekkin:<your_password>@localhost:5432/bagtrekkin
	SECRET_KEY=<your_secret_key>
	API_USER=api
	API_KEY=<server_api_key>
	API_URL=bagtrekkin.herokuapp.com
	EOF
	```

	* Replace `<your_secret_key>` with one generated, for instance, using [MiniWebTool](http://www.miniwebtool.com/django-secret-key-generator/).

	* Replace `<server_api_key>` with the one from Slack file in #Web Channel.

	* Replace `<your_password>` with the password you setup for postgres bagtrekkin user.

6. Run Migrations to create and feed your database:

	```bash
	(venv) $ python manage.py migrate
	```

7. Collect static files each time you alter `static` folder:

	```bash
	(venv) $ python manage.py collectstatic
	```

8. Test if everything runs well:

	```bash
	(venv) $ python manage.py runserver
	```

	You are now fully operational to join the developer team :)

	**/!\ Please read carefully [How to Contribute](https://github.com/goujonpa/bagtrekkin/blob/master/CONTRIBUTE.md) /!\\**

## Optional

In order to get closer to production environment, you can run python server the same way as Heroku actually do: using [`foreman`](https://github.com/ddollar/foreman).

Simply install globally Ruby foreman `gem`:

```bash
$ gem install -g foreman
```

## Getting Started

### Create Employee (i.e. User)

The first thing you need to do is create a new user using `Sign Up` form. It is also an `Employee`.

### Understand application structure

*	[`arduino`](https://github.com/goujonpa/bagtrekkin/blob/master/arduino/) folder contains hardware code currently not being used by application server-side (i.e. Hosted on Heroku)

* [`bagtrekkin`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/) folder contains the server-side application.

	* [`migrations`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/migrations/) folder contains all migrations run using `migrate` management command. If you want to create new migrations, please read carefully [How to write Migrations](https://github.com/goujonpa/bagtrekkin/blob/master/MIGRATIONS.md).

	* [`static`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/static/) folder contains all static resources (i.e. js, css, fonts and img files used by the application).

	* [`templates`](https://github.com/goujonpa/bagtrekkin/blob/master/bagtrekkin/templates/) folder contains all templates written in [Jade](http://jade-lang.com) and live time compiled using [PyJade](https://github.com/syrusakbary/pyjade).
