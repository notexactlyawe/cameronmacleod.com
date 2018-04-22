Title: Diagnosing performance issues in a Flask app
Date: 2018-04-22
Slug: sqlalchemy-speed
Category: Python

I was recently part of the team that ran [CreatED](https://createdhack.github.io), the UK’s first hardware hackathon of its kind. Organising it was stressful at times and incredibly rewarding at others, especially when it came to the event actually happening. During the run up to the event, we learned a lot about what actually needs to happen for a hackathon to run and one of those things was the setting up of event software.

It’s easy to overlook when you’re thinking about running your first hackathon, but things like registration systems, mentor allocation systems and hardware distribution systems all need to be put in place. Since we were a hardware hackathon, the last one was of particular importance to us. Thankfully HackMIT and MakeMIT, mostly through [Noah Moroze](http://noahmoroze.com/) had already put together a fantastic system for this, [Cog](https://github.com/techx/cog), which had been battle tested at much larger hackathons than ours.

Cog was a great gift to us, as we’d only started to think about a system for this quite late in the game (2 or 3 weeks to go) and it had pretty much all of the functionality we needed. There were, however, a few things that needed to be added and so I set about doing so.

 - We needed MyMLH, an OAuth provider, integrated since Cog only worked with HackMIT’s Quill registration system which we weren't using.
 - We needed participants to be able to upload CVs since Eventbrite had no functionality for this and it had been promised to sponsors.
 - We wanted a list of admin emails to be recognised by Cog so that not everyone had to use the same credentials.

Most of these were quite easy to integrate, thanks to some logical design on the part of the team at MIT. The CV upload functionality took me longer than the others though mostly due to my inexperience with front-end development. Before I was comfortable signing this off for use during the hack (due to it being so critical), I wanted to do some manual testing, and part of that was load testing since I was worried about a huge amount of users at the start of the hackathon.

I wrote up a quick script that started up a number of threads and used them all to fire a request at the home page of the application in a staggered fashion, hoping to simulate actual usage.

``` python
import time
import random
import requests
import threading

URL = "http://localhost:5000"

def time_to_get(url):
    print requests.get(url).elapsed.total_seconds()

def load_test(num_users):
    t_pool = []
    for num in range(num_users):
        t = threading.Thread(target=time_to_get, args=(URL,))
        t.start()
        t_pool.append(t)

    print "Waiting"

    for t in t_pool:
        t.join()


load_test(100)
```

The results I got from this quick test were mildly alarming. Each of these times (in seconds) is how long it took to receive a full response from the server.

```
cameron@isla:~/src/created/cog$ python load_test.py
Waiting
1.971983
3.797295
5.694615
7.800551
9.669649
...
```

To put this into context, this isn’t a particularly demanding page. It displays to the user a list of available hardware and does little else.

![The main page for Cog](/images/cog_main_page.png "The main page for Cog")

However, I wasn’t sure whether the problem was with my script or with Cog itself. To investigate this, I started Googling around profiling in Flask (the framework Cog is written in) and [this article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-debugging-testing-and-profiling) pointed me to some [Werkzeug middleware](http://werkzeug.pocoo.org/docs/0.14/contrib/profiler/) that did what I wanted. The output is below from one of the endpoint calls - pay attention to the top call.

```
PATH: '/inventory'
         1761654 function calls (1645404 primitive calls) in 2.829 seconds

   Ordered by: internal time, call count
   List reduced from 1183 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      759    0.375    0.000    0.377    0.000 {method 'execute' of 'psycopg2.extensions.cursor' objects}
     4536    0.062    0.000    0.280    0.000 /home/cameron/src/created/cog/venv/local/lib/python2.7/site-packages/sqlalchemy/sql/schema.py:898(__init__)
     6426    0.056    0.000    0.070    0.000 /home/cameron/src/created/cog/venv/local/lib/python2.7/site-packages/sqlalchemy/sql/elements.py:674(__getattr__)
...
```

The 2.829 seconds it took to serve the page suggested that the problem was somewhere in the application as opposed to my script and looked at the output. The most suspicious line to my eyes was the one that ended `{method 'execute' of 'psycopg2.extensions.cursor' objects}`, mostly because it was the most expensive, but also because it meant the database calls were taking a long time to execute. After a while going down the rabbit hole of trying different deployment options with the database in case the problem was with the database itself I went back and saw the `ncalls` column had 759 in it. This was fishy as all the page was doing was displaying a list of hardware available to the user, which shouldn’t have taken more than a couple of queries at most.

I was stumped as to what could be making this many queries in the application as the code all looked sensible, so I set SQLAlchemy to echo all queries to see whether I could see a pattern. Sparing you the output of 759 queries, a lot of COUNTs were popping up suggesting that the problem may be in the quantities of items since those were the only numbers on the page. Sure enough, looking at the code I found this:

``` python
class InventoryEntry(db.Model):
    ...
    @property
    def quantity(self):
        """Returns quantity of items that have not been 'claimed' by a request"""
        requests = RequestItem.query \
                   .filter_by(entry_id=self.id) \
                   .join(hardwarecheckout.models.request.Request) \
                   .filter_by(status=hardwarecheckout.models.request.RequestStatus.APPROVED) \
                   .with_entities(func.sum(RequestItem.quantity)).scalar()
        if not requests: requests = 0
        return Item.query.filter_by(entry_id = self.id, user = None).count() - requests
```

In the database, there was a table for inventory entries (roughly corresponding to 'classes' of items) and items (think instances of these classes). When calculating how many of a particular inventory entry was available it would check how many of an inventory entry existed in total and then subtract the number of approved requests for that item. This looks fine at first glance, and indeed it gives the correct result. However the issue is that this is calculated on a per-item basis, meaning each item makes 2 queries, when this could be done in a single query on a table basis.

The solution comes through the use of the GROUP BY clause. The following code selects all items that no user has claimed and groups them by the ID in `inventory_entry` before counting the groups (effectively returning how many of each inventory entry are free). The bottom line is a dictionary comprehension that puts them in a nice format for the Jinja template.

``` python
    counts = db.session.query(Item.entry_id, func.count(Item.entry_id))\
            .group_by(Item.entry_id)\
            .filter_by(user_id = None)\
            .all()
    counts = {id_: count for (id_, count) in counts}
```

The one important thing to note with this code is that `counts[“some_id”]` will error if `some_id` has no items free since `counts` won't have it as a key. The way to fix this is by using `counts.get(“some_id”, 0)` where `0` is a default value that’s returned when there’s no entry in the dictionary for `some_id`.

And as thought, the profiler output looks much better. The ncalls to `cursor.execute` has gone down to 4, which is much more sensible!

```
PATH: '/inventory'
         30824 function calls (29237 primitive calls) in 0.055 seconds

   Ordered by: internal time, call count
   List reduced from 677 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      297    0.003    0.000    0.010    0.000 /home/cameron/src/created/cog/venv/local/lib/python2.7/site-packages/sqlalchemy/orm/loading.py:30(instances)
        4    0.003    0.001    0.003    0.001 {method 'execute' of 'psycopg2.extensions.cursor' objects}
    162/1    0.003    0.000    0.025    0.025 {method 'join' of 'unicode' objects}
...
```

The final code that we deployed is now sitting on [GitHub](https://github.com/notexactlyawe/cog) so you can feel free to take a look.
