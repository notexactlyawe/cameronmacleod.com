Title: Better parameter validation in Flask with marshmallow
Date: 2019-04-25
Slug: better-validation-flask-marshmallow
Tags: Python, Flask, marshmallow, Web apps
Category: Tutorials

Recently I've had two Flask projects with endpoints that take lots of parameters. While working on the first project, I noticed that I was writing a lot of code for validation in each method, and it ended up looking ugly and probably full of bugs. When I started the second project, I thought that there had to be a way to fix this, and it turns out that there was!

To illustrate what I'm talking about, imagine you need to implement the following endpoint for a note taking app.

```
/api/note - POST

Parameters:
 - title (str) No longer than 60 characters
 - note (str) No longer than 1000 characters
 - user_id (int) No smaller than 1
 - time_created (datetime) Not in the future
```

In Flask without a library for validation, you might end up writing the following view function to implement this.

``` python
@app.route('/api/note', methods=['POST'])
def create_note():
    # we don't know that the 'title' parameter exists yet
    title = request.form.get('title', None)
    if title is None:
        abort(BAD_REQUEST)
    # we have to do manual validation on business requirements
    if len(title) > 60:
        abort(BAD_REQUEST)

    # now we have to do it again?!
    note = request.form.get('note', None)
    if note is None:
        abort(BAD_REQUEST)

    ... # more validation

    actually_create_note()
    return 'ok'
```

The two parameters I validated up there were strings which made this easier, the `integer` parameter would have additionally needed a type check and don't even think about parsing and validating the `datetime` there. The above code is long and very prone to bugs. Of course, you could abstract it all to cleaner methods, but that wouldn't solve the underlying problem of having to write all of this manually.

Thankfully, it turns out there is a library that does validation like this straight out of the box. It's called [marshmallow](https://marshmallow.readthedocs.io/) and is meant for object serialization. Alongside parsing and dumping, it also comes with some powerful validation functionality built-in.

<details><summary>What is object serialization?</summary>
<p>
[Serialization](https://en.wikipedia.org/wiki/Serialization) is the process of converting objects and data from the format used internally in your program into a format that can be stored or transmitted. For example, JSON data can be represented and easily accessed as a dictionary in Python, but it needs to be **serialized** to a string to send it anywhere. The reverse operation is called **deserialization** and is what we'll be dealing with in this article.
</p>
</details>

The core idea in marshmallow is that data structure is represented with a schema. A schema is a class that defines what format the data comes in. It dictates what fields exist, their types and validation on them. You create a schema by sub-classing `marshmallow.Schema` and creating attributes that will represent the fields in your data.

Using the note-taking endpoint as an example, we'll create a schema that represents the structure of incoming data to the endpoint.

``` python
from marshmallow import Schema, fields

class CreateNoteInputSchema(Schema):
    """ /api/note - POST

    Parameters:
     - title (str)
     - note (str)
     - user_id (int)
     - time_created (time)
    """
    # the 'required' argument ensures the field exists
    title = fields.Str(required=True)
    note = fields.Str(required=True)
    user_id = fields.Int(required=True)
    time_created = fields.DateTime(required=True)
```

This is a pretty simple class, but already it contains a lot of magic. This will check both existence of fields and their types for you. It's important to note that it won't do any business logic validation yet. You can use this in a view function like so:

``` python
create_note_schema = CreateNoteInputSchema()

@app.route('/api/note', methods=['POST'])
def create_note():
    errors = create_note_schema.validate(request.form)
    if errors:
        abort(BAD_REQUEST, str(errors))
    # now all required fields exist and are the right type
    # business requirements aren't necessarily satisfied (length, time bounds, etc)
    actually_create_note()
    return 'ok'
```

We don't have all of the functionality we need, but even still this has cleaned up the code considerably. The other thing we need to do is to add validation methods for the business requirements. You can do this in two ways with marshmallow. Firstly you could create a method in your schema that has the `@validates` decorator, or for simple cases, you could give the `validate` keyword argument to the field.

``` python
from marshmallow import Schema, fields
# import built-in validators
from marshmallow.validate import Length, Range

class CreateNoteInputSchema(Schema):
    ...
    # no longer than 60 chars
    title = fields.Str(required=True, validate=Length(max=60))
    # no longer than 1000 chars
    note = fields.Str(required=True, validate=Length(max=1000))
    # at least 1
    user_id = fields.Int(required=True, validate=Range(min=1))
    time_created = fields.DateTime(required=True)
```

You will notice above that marshmallow comes with a bunch of handy validators built-in. You can see a full list of them in the [API docs](https://marshmallow.readthedocs.io/en/3.0/api_reference.html#module-marshmallow.validate).

We're still missing a validator for checking that the date is not in the future. Luckily we can use the `@validates` decorator to write our own.

``` python
from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError
...

class CreateNoteInputSchema(Schema):
    ...
    time_created = fields.DateTime(required=True)

    @validates('time_created')
    def is_not_in_future(value):
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create notes in the future!")
        # if the function doesn't raise an error, the check is considered passed
```

We don't even have to use any extra code in our view function now to use the extra validation, we still just call the `validate` method.

``` python
@app.route('/api/note', methods=['POST'])
def create_note():
    errors = create_note_schema.validate(request.form)
    if errors:
        abort(BAD_REQUEST, str(errors))
    actually_create_note(request.form)
    return 'ok'
```

## Extra information

marshmallow is very powerful and contains much more than what I have covered here. Thankfully there are many good resources on the internet for you to research further.

 - [marshmallow Quickstart](https://marshmallow.readthedocs.io/en/3.0/quickstart.html)
 - [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) - An integration library that adds extra functionality (automatic schemas from models, extra field types, etc)
 - [How to Build RESTful APIs with Python and Flask | Codementor](https://www.codementor.io/dongido/how-to-build-restful-apis-with-python-and-flask-fh5x7zjrx) - A wider look at API building as opposed to just the validation.
