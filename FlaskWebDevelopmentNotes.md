
#Introduction

**Flask** is an extensible microframework. It consists of a core of basic services; you may extend it with extensions. The result is a **lean stack**. It has only two dependencies: **Werkzeug** (WSGI, routing, debuggin) and **Jinja2** (template support).

It's good practice to use `virtualenv` and freeze environment packages into `requirements.txt`.

#Basic Application Structure

Flask applications need an **application instance**. The web server uses the **WSGI protocol** to pass client requests to the application instance. The instance only needs the name of the application to initialize; `__name__` is the root path of the application.


```
from flask import Flask
app = Flask(__name__)
```

A **route** is the association between a URL and a function that handles it. This is how the application instance knows what to do with incoming requests. Flask has a function **decorator** to indicate routes. The function decorated is a **view function**, which creates and returns a **response** to go back to the client.

```
@app.route('/')
def index()
	return '<p>Hello World<p>'
```

Flask supports **dynamic endpoints** with special syntax in the route decorator: `@app.route('/user/<name>')`. Flask will send the dynamic component as an argument to the view function. The default dynamic component type is string but int float and path can be specified `@app.route('/user/<int:id>')`.

The application instance has a run method to launch the development web server:

```
if __name__ == '__main__':
	app.run(debug=True)
```

Once a server starts up, it enters a loop that waits for requests and services them.

When Flask receives a request, it must create a couple objects to pass to the view function. Instead of passing these objects to every single view function, Flask uses **contexts** to make certain objects temporarily globally accessible. Technically it is globally accessible within the thread dealing with that request. A multi-threaded server would have different threads handling different requests by accessing different contexts.

Flask has an **application context** and a **request context**. Flask pushes (activates) both contexts before dispatching a request; it pops them after a request is handled. When application context is pushed, `current_app` (the app instance) and `g` (temporary storage) become available to the thread. When a request context is pushed, `request` (contents of an HTTP request) and `session` (user session) become available.


Flask routes are written in a **URL map**. `app.url_map` reveals them. `/static/<filename>` is a special route for giving access to static files. The map also shows the **request methods**; `HEAD` and `OPTIONS` are automatically handled by Flask but the HTTP request type can be specified.

A **request hook** is a function that is hooked to request before or after a request is made. Flask uses decorators like `before_first_request` to indicate request hook functions.

View functions must return a response to a request, which must include a status code. Add the numeric code of the status code as the second return to a view function. View functions can also return a dictionary of headers (but this is rare). The returned values are converted into a `response` object; however you may create this object within the view function (handy if you need to configure it) before returning it.

A **redirect** is a response that specifies a new URL for the client to redirect to. The **abort** response is used for error handling.

You can specify the **host** for `flask run` to make the web server accessible to any computer in the network.

#Templates



