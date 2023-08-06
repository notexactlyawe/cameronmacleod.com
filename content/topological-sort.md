Title: How to sort parent nodes before child nodes? - Topological sort
Date: 2023-08-06
Slug: topological-sort
Tags: Python, Graph theory
Category: Tutorials
header_image: images/toposort/header.png

![](/images/toposort/header.png)

Dependencies between things are common, but they can be tricky to manage in code.
You might think of using a graph to model your system, but how can you ensure that
thing A happens before thing B? This is where the idea of a topological sort comes in.

This article is aimed at programmers who want to use topological sorting. I won't
explain the maths but I will give code examples. There are also [links](http://localhost:8001/blog/topological-sort#how-do-you-use-a-topological-sort)
to help you find an implementation for your language. The examples will be in Python, but the
concepts should apply generally.

[TOC]

## Why would you need a topological sort?

A package manager is a piece of software that installs other software. For example,
a user could ask a package manager to install a text editor. It would then be the
package manager's job to know where to find the text editor and how to install it.

Software packages almost always have dependencies. To install a text editor, you
might first need to install a UI library and that UI library might require a C++
compiler. This dependency graph would look like the following:

![A text editor package depending on gcc, a C++ compiler](/images/toposort/simpledependency.svg)

This example is simple, but in the general case each package might have many dependencies
and packages may share dependencies. This quickly becomes a tangled mess, and
making sure that dependencies are installed before the software that needs them
becomes difficult.

You can phrase this problem more generally. Given a graph, with dependencies between
parent nodes and child nodes, how do you produce a list of nodes such that parent
nodes come before their child nodes?

You can sort nodes of a graph in this way using a topological sort.

## What is a topological sort?

A topological sort is a fancy name for:

1. Taking a graph that has parent and child nodes (a **directed** graph)
1. Making a list of nodes in that graph such that:
    - Each parent node will always appear before its children
    - Each child node will come after its parents in the list

So taking a graph like the following:

![A more complex dependency graph](/images/toposort/complexdependencies.svg)

A topological sort might look like:

| Package            | Depends on                                   |
|--------------------|----------------------------------------------|
| 1. gcc             | N/A                                          |
| 2. Network library | gcc                                          |
| 3. UI library      | gcc                                          |
| 4. Python          | gcc                                          |
| 5. Language server | gcc, Python                                  |
| 6. Text editor     | Network library, UI library, Language server |

In the above ordering, a package always comes after its dependencies.

In the case of a package manager, this would mean that topological sorting produces
an installation order that ensures dependencies are always installed before the
software that depends on them. This is great, because there will never be missing
dependency errors!

<details>
<summary>Why is it called a topological sort?</summary>
<br>
<p>
<b><i>hand-waving begins</i></b>
</p>
<p>
There is a branch of maths called topology which deals with shape and structure.
Graph theory originally came out of topology.
</p>
<p>
Dependencies give structure to a graph, and topology is structure. Sorting a graph
by its dependencies, therefore, can be considered a <i>topological</i> sort.
</p>
<p>
There are a lot of Wikipedia pages with topology in their name in this area, so it
feels like the name intuitively fits, but I can't give you a more concrete
answer unfortunately. Further reading below!
</p>
<ul>
<li><a href="https://en.wikipedia.org/wiki/Topological_graph_theory">Topological graph theory</a></li>
<li><a href="https://en.wikipedia.org/wiki/Network_topology">Network topology</a></li>
<li><a href="https://en.wikipedia.org/wiki/Topological_sorting">Topological sorting</a></li>
</ul>
<b><i>hand-waving ends, back to the coding</i></b>
</details>
<a name="how-to-cycles"></a>

## Cycles and topological sorts

You can't apply a topological sort to a graph with a cycle in it.
A cycle is where two or more nodes depend on each other. For example, `A` depends
on `B`, but `B` also depends on `A`. In this case you can't produce a topological
sort, because both `A, B` and `B, A` have a child node before a parent node.

![A cycle with two nodes](/images/toposort/cycle.svg)

What can you do about cycles? Fundamentally, cycles cannot be topologically sorted.
That said, there are a few things you could do depending on what problem you are solving:

**Manually remove the cycle**

If you are building a graph by hand, then the easiest way to fix a problem like this
is to manually remove the cycle. This can be done by removing conflicting edges.

For example, in the `A->B->A` graph above, you could remove `A`'s dependency on `B`,
or `B`'s dependency on `A`.

**Throw an error to the user/caller of your code**

If the graph is being passed from outside your code, then it might be acceptable to
throw an error in case of a cycle.

**Algorithmically remove cycles**

The problem of removing cycles from a graph while keeping the maximum number of
edges is called the [feedback arc set](https://en.wikipedia.org/wiki/Feedback_arc_set).
There are algorithms for the feedback arc set, but they are not for the faint of
heart! Proceed with caution:

 - [How to remove cycles in an unweighted directed graph, such that the number of edges is maximised? - Stack Overflow](https://stackoverflow.com/questions/6284469/how-to-remove-cycles-in-an-unweighted-directed-graph-such-that-the-number-of-ed)
 - [How to remove cycles from a directed graph? - Computer Science Stack Exchange](https://cs.stackexchange.com/questions/90481/how-to-remove-cycles-from-a-directed-graph)

## How do you use a topological sort?

*For those who just want Python code, I've compiled it in [this gist](https://gist.github.com/notexactlyawe/606734bcffdaa7d0c091dfbe55f09baa).*

The below examples are all in Python, however, here are some links for libraries in
other languages. I have not used any of the below, but hopefully they can provide a
starting point for your research.

 - JavaScript: [toposort - npm](https://www.npmjs.com/package/toposort)
 - Java: [TopologicalOrderIterator - JGraphT](https://jgrapht.org/javadoc/org.jgrapht.core/org/jgrapht/traverse/TopologicalOrderIterator.html)
 - Rust: [petagraph::algo::toposort](https://docs.rs/petgraph/latest/petgraph/algo/fn.toposort.html)

Thankfully Python ([from version 3.9](https://docs.python.org/3/whatsnew/3.9.html)) comes
with topological sort in the standard library! The wonderful [graphlib](https://docs.python.org/3/library/graphlib.html)
provides everything you need.

Going back to the package manager example from earlier, you could model a package and
its dependencies with the below class:

```python
from dataclasses import dataclass    
from typing import List    


@dataclass          
class Package:      
    name: str                   
    depends_on: List[str]
```

The above code defines a class `Package` that has two fields, `name` and `depends_on`.
`name` is the name of the package and `depends_on` is a list of other package names
that this package depends on. The fields have type hints on them for readability.

[`@dataclass`](https://docs.python.org/3/library/dataclasses.html) is a really powerful
decorator that creates a lot of boilerplate methods, such as `__init__` for free. Thanks
to `@dataclass`, you can use `Package` like so:

```python
text_editor = Package("editor", ["ui_lib"])
ui_lib = Package("ui_lib", ["gcc"])
gcc = Package("gcc", [])
```

This will create three packages. A text editor which depends on a UI library which in
turn depends on GCC:

![A text editor package depending on gcc, a C++ compiler](/images/toposort/simpledependency.svg)

After creating the packages, the next job is to create a [`TopologicalSorter`](https://docs.python.org/3.9/library/graphlib.html#graphlib.TopologicalSorter).
A `TopologicalSorter` has methods for topologically sorting a graph. The below code
creates one and tells it about the packages:

```python
ts = TopologicalSorter()
ts.add(text_editor.name, *text_editor.depends_on)
ts.add(ui_lib.name, *ui_lib.depends_on)
ts.add(gcc.name, *gcc.depends_on)
```

In the above snippet, the `add` method takes a node as the first argument, and its dependencies
as the following arguments. The code uses an asterisk `*` to unpack the `depends_on` fields
into separate arguments. If you've not seen this syntax before, check out
[the Python docs](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists).

There are a couple of things to note in the above code snippet. Firstly, all arguments
provided to `add` represent nodes and must be [hashable](https://stackoverflow.com/questions/42203673/in-python-why-is-a-tuple-hashable-but-not-a-list).
This means that strings and tuples are valid nodes, but lists are not.

Secondly, you may notice that the `text_editor` node was added before the nodes it
depends on. This is because `TopologicalSorter` is very forgiving and allows you to
add nodes in any order. From the [docs](https://docs.python.org/3.9/library/graphlib.html#graphlib.TopologicalSorter.add):

> If a node that has not been provided before is included among _predecessors_ it will be automatically added to the graph with no predecessors of its own.

The next step is to call `static_order` on the `TopologicalSorter` to produce a
topological sort of the package graph:

```python
for node in ts.static_order():
    print(node)
```

This will print:

```
gcc
ui_lib
editor
```

Great! This prints packages in the correct installation order. GCC can be installed
first because it has no dependencies, and installing it unblocks installing the UI library
which, in turn, unblocks installing the text editor.

`static_order()` returns an [iterator](https://realpython.com/python-iterators-iterables/),
which is why the code uses a `for` loop to get the resulting nodes. Iterators are usually
more efficient than lists, but if you wanted the result in a list, you could do
the following:

```python
nodes = list(ts.static_order())

# nodes = ["gcc", "ui_lib", "editor"]
```

For a more complex example, imagine the text editor had more dependencies:

![A more complex dependency graph](/images/toposort/complexdependencies.svg)

In the dependency graph above, there are a lot more packages, and some of them
even share dependencies! Luckily, `TopologicalSorter` will handle them without a problem:

```python
text_editor = Package("editor", ["ui_lib", "lang_server", "network_lib"])
lang_server = Package("lang_server", ["gcc", "python"])
network_lib = Package("network_lib", ["gcc"])
ui_lib = Package("ui_lib", ["gcc"])
python = Package("python", ["gcc"])
gcc = Package("gcc", [])

ts = TopologicalSorter()
ts.add(text_editor.name, *text_editor.depends_on)
... # more add()s here
ts.add(gcc.name, *gcc.depends_on)

for node in ts.static_order():
    print(node)
```

This will print:

```
gcc
network_lib
ui_lib
python
lang_server
editor
```

`TopologicalSorter` is a powerful tool indeed! However, what happens when you accidentally
pass it a cycle? The below code example creates a cycle to demonstrate what happens:

```python
text_editor = Package("editor", ["lang_server"])
lang_server = Package("lang_server", ["editor"])

ts = TopologicalSorter()
ts.add(text_editor.name, *text_editor.depends_on)
ts.add(lang_server.name, *lang_server.depends_on)

for node in ts.static_order(): # raises CycleError
    print(node)
```

When the code calls `static_order`, it raises a `CycleError`:

```
Traceback (most recent call last):
 File "/home/cameron/src/scratch/cycle-toposort.py", line 21, in <module>
   for node in ts.static_order():
 File "/usr/lib/python3.9/graphlib.py", line 242, in static_order
   self.prepare()
 File "/usr/lib/python3.9/graphlib.py", line 104, in prepare
   raise CycleError(f"nodes are in a cycle", cycle)
graphlib.CycleError: ('nodes are in a cycle', ['editor', 'lang_server', 'editor'])
```

Take a look at the section above on [dealing with cycles](#how-to-cycles) for pointers
on handling this error.

## Multi-threading and TopologicalSorter

Calling `static_order`, as in the examples above, produces a list that works well
with single-threaded code. However, it doesn't tell you which nodes can be processed
at the same time.

To take the package manager example, a naive implementation using `static_order`
may end up installing a package at the same time as its dependency. This could cause
problems.

A naive implementation using two threads and `static_order` would break on the
simple dependencies example from earlier. It would try to install gcc at the same
time as the UI library, which would fail as the UI library depends on gcc:

![An example of a naive multi-threaded implementation causing problems](/images/toposort/multithreadconflict.svg)

Processing multiple nodes at once is useful as it can speed up your code, but
is incompatible with `static_order()`. You can still use `graphlib` in multi-threaded
code, though. Below are steps from the docs to use `TopologicalSorter` in a
parallel way:

> 1. Create an instance of the `TopologicalSorter` with an optional initial graph.
2. Add additional nodes to the graph.
3. Call `prepare()` on the graph.
4. While `is_active()` is True, iterate over the nodes returned by `get_ready()` and process them. Call `done()` on each node as it finishes processing.

You've already seen how to do steps 1 and 2, that's the same as in the earlier code.
To recap, here's how to add nodes to the `TopologicalSorter`:

```python
ts = TopologicalSorter()
ts.add(text_editor.name, *text_editor.depends_on)
...
```

After creating a `TopologicalSorter` and adding nodes to it, step 3 is to call
`prepare()` on it. `prepare()` marks the graph as ready for processing and
checks for cycles:

```python
try:
  ts.prepare()
except graphlib.CycleError:
  # do something with the error
  ...
```

This is where a `graphlib.CycleError` may be raised, so the code uses a
`try`/`except` to deal with the error. After calling `prepare()`, you can't add
any more nodes to the graph.

Before writing the code to get packages from `TopologicalSorter`, there needs to
be a way of simulating package installation. Since installing packages takes time,
the code can simulate it with `time.sleep`:

```python
import time
from queue import Queue

installed_packages_queue = Queue()

def install_package(package):
    print(f"* Installing package {package}...")
    time.sleep(1)
    installed_packages_queue.put(package)
```

The above code defines a function `install_package` that [sleeps](https://docs.python.org/3/library/time.html#time.sleep) for a second and
then puts the package that it just 'installed' onto a [queue](https://docs.python.org/3/library/queue.html).

The queue is used to communicate to the `TopologicalSorter` that packages depending
on the now installed package can be processed. A queue allows the code to wait
for any package to be installed even if multiple threads are installing packages.

Step 4 is where things get a little more complicated as it introduces three new
functions, `is_active()`, `get_ready()` and `done()`. Let's take a look at the
code and then step through it to see what it does:

```python
from concurrent.futures import ThreadPoolExecutor

...

with ThreadPoolExecutor() as executor:
    while ts.is_active():
        ready_packages = ts.get_ready()
        print(f"Ready to install {ready_packages}")
        executor.map(install_package, ready_packages)

        installed_package = installed_packages_queue.get()
        ts.done(installed_package)
        print(f"Installed package {installed_package}")
```

[`ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)
is a convenient way to work with threads. You can submit jobs to a `ThreadPoolExecutor`
and have them automatically run in different threads. It simplifies a lot of the
boilerplate and clean-up that typically comes with threaded code.

The code creates a `ThreadPoolExecutor` which will get cleaned up automatically
once execution leaves the `with` block. `ThreadPoolExecutor` is a [**context manager**](https://docs.python.org/3/reference/datamodel.html#context-managers):

```python
with ThreadPoolExecutor() as executor:
    ...
```

The code then enters into the loop that the `graphlib` docs described:

> While `is_active()` is True, iterate over the nodes returned by `get_ready()` and process them. Call `done()` on each node as it finishes processing.

`is_active()` reports whether there are nodes left to process. Until all
the nodes have been returned by `get_ready()`, `is_active()` will return `True`.
The code uses `is_active()` to stop once all packages are installed.

`get_ready()` gets a tuple of nodes that can be processed right now. A node can be
processed if all of its parents have been processed or if it has no parents:

```python
...
while ts.is_active():
    ready_packages = ts.get_ready()
    print(f"Ready to install {ready_packages}")
    executor.map(install_package, ready_packages)
```

The above code snippet gets a list of currently ready packages and then submits them
as jobs to the `ThreadPoolExecutor` using `map(func, iterable)`. This creates a new
`install_package` job for each package that `get_ready` returns. Note that `map` is
non-blocking.

The code then blocks on a package being put onto `installed_packages_queue`. The
`.get()` call will return after the first `install_package` returns:

```python
...

installed_package = installed_packages_queue.get()
ts.done(installed_package)
print(f"Installed package {installed_package}")
```

`done(package)` marks a node as processed. This enables `get_ready()` to return
any child nodes of the processed node. In the above code, `done` marks a package as
installed, which allows `get_ready()` to return packages that depend on the
installed package.

With all these pieces in place, here's the English version of the above code:

- While there are packages left to install  
    1. Get the packages that can currently be installed
    1. Start an installation thread for each package
    1. Wait for a package to be installed by listening on `installed_packages_queue`
    1. Mark that package as done in the `TopologicalSorter`
    1. Go round again to see whether any more package can now be installed

It took me a little while to wrap my head around this example, so don't be afraid
to re-read the above a couple of times! It's worth noting that if your
use case works with single-threaded processing, then `static_order` is an easier
option.

Running the code in the attached [gist](https://gist.github.com/notexactlyawe/606734bcffdaa7d0c091dfbe55f09baa)
produces the following output:

<script async id="asciicast-600838" src="https://asciinema.org/a/600838.js"></script>

## Conclusion

Topological sorting is a really powerful tool. It allows you to order nodes in a graph
by their dependencies, making sure that parent nodes come before their children.

In this article, you learned:  

 - What a topological sort is and what it's useful for
 - How to use `graphlib.TopologicalSorter` in the Python standard library
 - How to deal with cycles in graphs when topologically sorting them

All the code in this article is available in a [GitHub Gist](https://gist.github.com/notexactlyawe/606734bcffdaa7d0c091dfbe55f09baa).
