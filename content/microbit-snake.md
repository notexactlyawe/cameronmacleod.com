Title: Build a snake game on the BBC micro:bit
Subtitle: A detailed tutorial (simulator included)
Date: 2020-05-18
Slug: microbit-snake
Tags: micro:bit, Python, Games
Summary:![Header image](/images/microbitsnake/header.png) By the end of this tutorial, you'll have built your very own game and learned not only about game development, but Python and the BBC micro:bit too. What's more, you don't even need to own a micro:bit to follow along!
Category: Tutorials

![Header image](/images/microbitsnake/header.png)

By the end of this tutorial, you'll have built your very own game and learned not only about game development, but Python and the BBC micro:bit too. What's more, you don't even need to own a micro:bit to follow along!

Below is a preview of what we'll be building.

<video autoplay loop muted playsinline src="/images/microbitsnake/snakepreview.mp4"></video>

## Pre-requisites

This tutorial will assume that you know what Python is, and that you know some basic programming concepts. But don't worry, if you consider yourself a beginner then this tutorial is for you. In fact, I will try to over-explain things and provide solutions to every exercise, so there's nothing to fear!

With that out the way, let's get started.

**Quick links**

[TOC]

## What is a micro:bit?

A [micro:bit](https://microbit.org/) is a tiny computer that you can program in Python. It comes with an LED grid (for a screen), an accelerometer (to detect motion), electrical outputs (for controlling motors, lights etc) and a bunch of other cool features. They're also pretty cheap, and programming them is as simple as dragging a file to a USB stick.

![A micro:bit](/images/microbitsnake/microbit.svg)

If you don't already have one, don't worry! There are simulators available online and you'll be able to follow along with this whole tutorial.

## Setting up environment

Whether you have a micro:bit or not, the first step is to open the [create.withcode editor](https://www.cameronmacleod.com/createwithcode/). When you do, you should see a screen like the one below.

![create.withcode editor](/images/microbitsnake/createwithcode.png)

Most of the screen (1) is taken up with the editor. This is where you'll put your code. In the lower right corner (2) is a "+" button. When you click this, you'll get a list of options, including one to run your code which looks like a play button. Alternatively, you can run your code by pressing `Ctrl`+`Enter`.

Running your code will produce a pop-up that looks like the below.

![micro:bit create.withcode interface](/images/microbitsnake/microbitmodal.png)

Your code will be running on the virtual micro:bit you can see, and there are tabs along the top for your to control various inputs to the device, which will become important later.

If you are working with a physical micro:bit, then the "Download HEX" button in the top-left of the pop-up will allow you to download the file you need to program your micro:bit. You can drag this file to the "MICROBIT" device in your file manager to program it.

Before we start looking at some code, let's take a quick detour to look at the game of Snake.

## Snake

Fun fact - up until recently you could go to Google, search for "snake", and a snake game would appear. It doesn't appear for me any more, but you can still play it [here](https://www.google.com/fbx?fbx=snake_arcade). Below you can see it in action.

<video autoplay loop muted playsinline src="/images/microbitsnake/snakedemo.mp4"></video>

This is a good example of a snake game. It has all the necessary components:

 - A grid on which the snake moves.
    - The grid has cells, which can be identified by their X and Y co-ordinates.
 - A snake.
    - The snake occupies some cells of the grid (you can think of it as a list of co-ordinates).
    - The snake has a direction (up, down, left, right).
 - Some randomly generated food on a cell.
 - An end condition.
    - In the video this happens when the snake crashes into itself, losing the game.

So in theory, if we can build all these components, then we should have a snake game!

## Skeleton code

To make it easier to get started, we'll be working from a skeleton file. Find it at [this link](https://github.com/notexactlyawe/microbit-snake/blob/master/skeleton.py) and copy the contents into the [create.withcode editor](https://www.cameronmacleod.com/createwithcode/).

Let's take a look at each part of the code to figure out what it does.

```python
from microbit import *

class Snake:
...
```

At the very top of the file is an import. This is just a way of saying that we want to use some other code in our own. In this case, the other code we're using is the `microbit` library, which allows us to control various components of the micro:bit including the display and accelerometer.

Skipping the class definition for now, at the bottom of the file is our game loop.

```python
while True:
    game.handle_input()
    game.update()
    game.draw()
    sleep(500)
```

The game loop is the entry point for the game (the first bit of code to be executed). It defines a series of actions that we do repeatedly in order to make the game work. In this case, we get some input from the user, update the game state accordingly and then re-draw the screen. Updating the screen twice a second feels about right, and so at the end we sleep for 500 milliseconds (half a second).

The functions called in the game loop are part of the Snake class, which is defined above the game loop.

```python
class Snake:
    """ This class contains the functions that operate
        on our game as well as the state of the game.
        It's a handy way to link the two.
    """

    def __init__(self):
        ...

    def handle_input(self):
        ...

    def update(self):
        ...

    def draw(self):
        ...

game = Snake()
```

A class is a handy way of keeping some state, like the position of our snake, alongside the functions that operate on it. Our class has a few different functions that we'll have to write.

 - `__init__(self)`: This is a special Python function that is called when an "instance" of a class is created. We'll see an example of creating an instance later on. The function will initialise our variables ready for the game to run. For example, we need an initial position for the snake and a direction it will first be heading.

    You may notice that it takes an argument, `self`. This argument is a Python requirement for functions that are part of a class, and represents the instance of the class. This means we can use it to access the state that's part of the class.

 - `handle_input(self)`: This function gets input from the user and uses it to change the direction of the snake. We'll be using the accelerometer for this which means that the user will be tilting the device to make the snake move. Again, this function takes `self` since Python requires it to.
 - `update(self)`: Once we have the direction that the user wants the snake to move, we can update the state of the game. This means moving the snake, "eating" food and ending the game.
 - `draw(self)`: The `draw` function allows us to see the game state on the screen. In this function we'll be lighting up LEDs to represent the snake and the food.

Below the `Snake` class definition, we create an instance of it and assign it to the variable `game`. If you're not yet comfortable with classes and instances, take a look at the expandable panel below.

<details><summary>Classes and instances</summary>
<p>
A class is a way of linking functions to variables, but you can also think of it as defining the 'type' of something. Let's use cars as an analogy:

```python
class Car:
    def __init__(self, make, model, colour):
        self.make = make
        self.model = model
        self.colour = colour

    def print_info(self):
        print(f"This is a {self.colour} {self.make} {self.model}")

astra = Car("Vauxhall", "Astra", "white")
golf = Car("Volkswagen", "Golf", "blue")

astra.print_info()
# Prints "This is a white Vauxhall Astra"
golf.print_info()
# Prints "This is a blue Volkswagen Golf"
```

In this example, we've defined a `Car` _class_ that contains the make, model and colour of a car. The class represents the concept of a car, but note that it does not represent any actual cars, that's what instances are for.

Below the class definition, we create two _instances_ of `Car`. One that represents an Astra, and one that represents a Golf. An instance represents a specific thing, instead of the concept of a thing. So our `astra` variable does not represent the idea of a car, but instead a specific white Vauxhall Astra.

One thing you may notice about the class is that both of its functions take `self` as the first argument. This represents the instance of the class that the function is being called on. When we call `astra.print_info()`, Python passes the `astra` instance as the first argument to the `print_info()` function.

One other thing that often confuses people with classes is the `__init__` method. It's a special method in Python that gets called when you create an instance of a class. When we create an instance, you can think of the following happening.

1. We call `astra = Car("Vauxhall", "Astra", "white")`
2. Python creates an empty `Car`, let's call it `temp_car`.
3. Python runs `astra = Car.__init__(temp_car, "Vauxhall", "Astra", "white")`
4. `astra` now has the correct variables and `temp_car` is discarded.

For more discussion of classes, take a look a [Jeff Knupp's blog post](https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/).
</p>
</details>

Now that we have a template, our first step will be to initialise the game state.

## Creating the game state

Before we can intialise the game state, we need to learn a little bit about Python and the micro:bit. Feel free to skip these sections if you have done this before.

### Python lists

Lists are a way to store multiple values in the same variable in Python. If you haven't come across them before there's a more [detailed introduction here](http://openbookproject.net/thinkcs/python/english3e/lists.html). You may be able to get by with the cheat sheet below though.

```python
# define a list
>>> my_list = [1, 2, 3]
# access elements of a list (start counting at 0)
>>> my_list[0]
1
# -1 is the last element of the list
>>> my_list[-1]
3
# Add an item to a list
>>> my_list.append(4)
>>> my_list
[1, 2, 3, 4]
# Remove an item from a list
>>> my_list.pop(0)
1
>>> my_list
[2, 3, 4]
# list of lists
>>> list_of_coords = [[1, 2], [1, 3]]
>>> list_of_coords[0]
[1, 2]
>>> list_of_coords[0][1]
2
```

### The micro:bit co-ordinate system

On the front of a micro:bit is a grid of LEDs. When drawing something on the screen, we need a way to describe individual LEDs within this grid so that we know which one to light up. This is where the co-ordinate system comes in.

![The micro:bit co-ordinate system](/images/microbitsnake/displaycoords.svg)

Display co-ordinates on the micro:bit work a little like the graphs you may have plotted in school. There's an X axis that goes from left to right and a Y axis that goes from top to bottom. The main difference from the graphs in school is that the Y axis increases going down (towards the pins) whereas in school it would have increased going up.

In the image above, point A is at the co-ordinates `[3, 0]`. The left number in these co-ordinates is the position along the X axis and the right number is the position along the Y axis. Similarly, point B is at co-ordinates `[1, 2]`.

### <i class="fa fa-lightbulb-o"></i> Your turn 1: Filling in the state

If you now feel comfortable with these concepts, you'll notice that the `__init__` function has some commented out code. When you uncomment that, it looks like the below. Feel free to have a go at completing it and we'll look at the solution in the next section.

```python
# direction is a string with up, down, left or right
self.direction =
# snake is a list of the pixels that the snake is at
self.snake = [[2, 2]]
# food is the co-ords of the current food
self.food =
# whether or not to end the game, used after update
self.end =
```

<details><summary>Solution</summary>
<p>
Let's talk through the solution line by line.

```python
self.direction = "up"
```

We defined `self.direction` to be a string and I've chosen to make the snake go up at first. If you've put any other direction that's fine too.

```python
self.food = [0, 2]
```

I've put my food in the middle of the left-most column to start with. If you've put it elsewhere, that's fine as long as you've defined valid co-ordinates that aren't the same as the snake's starting position.

```python
self.end = False
```

This variable tells us whether the game has finished or not. It wouldn't be very helpful to set it to `True` before it's even started!
</p>
</details>

## Drawing to the screen

We have some initial state, but if you ran this code right now, you wouldn't see much happening. That's because we're not actually drawing anything to the screen.

So what do we need to draw on the screen? Thinking back to our Google Snake example, the snake, food and grid were visible. On the micro:bit the grid is already built for us since the LEDs form a grid naturally. That leaves the snake and the food to be drawn.

### Drawing the food

Ideally, then, we need a function to light up an individual LED using its co-ordinates. The snake and the food are both stored using co-ordinates, so if we can draw these on one at a time then we'll have completed our `draw` function.

The micro:bit offers us a number of different ways to [draw to the screen](https://microbit-micropython.readthedocs.io/en/latest/display.html), including one that does what we need. `display.set_pixel(x, y, value)` will set the pixel at `[x, y]` to the intensity `value`. `value` can be between 0 and 9, where 0 is off and 9 is fully on.

Now that we have a function to turn on a pixel, we can start to fill in our `draw` function.

```python
def draw(self):
    display.clear()
    display.set_pixel(self.food[0], self.food[1], 5)
    # TODO: draw snake
```

The first thing we do in this function is `display.clear()`. This sets all the LEDs off, which is important because this draw function will be called repeatedly and we want to draw something different each time. If we didn't clear the display, then the game state from the last iteration of the game loop would still be there.

Next we use the `self.food` co-ordinates to draw the food. We use the intensity `5` because that will help us to distinguish it from the snake.

Before we draw the snake, let's take a look at `for` loops in Python. Again, if you've done this before, feel free to skip it.

### Python `for` loops

`for` loops are great for when you want to do the same thing to multiple elements. In Python they're written like this:

```python
for variable_name in iterable_thing:
    do_things(variable_name)
```

`iterable_thing` is something with multiple elements, for example a list, tuple or even a `range(start, stop)`. `variable_name` is the name that you assign to the element that you are currently working on in the loop. To make this example more concrete, here's how you would print the numbers from one to five.

```python
>>> for i in range(1, 6):
>>>     print(i)
1
2
3
4
5
# alternatively
>>> nums = [1, 2, 3, 4, 5]
>>> for num in nums:
>>>     print(num)
1
2
3
4
5
```

### <i class="fa fa-lightbulb-o"></i> Your turn 2: Drawing the snake

Now you know how to light up individual pixels, and how to use a `for` loop to go over a list, you should be able to draw the snake to the screen. You'll want to draw the snake with intensity `9` so that it looks different from the food we drew earlier. As before, the solution is below.


<details><summary>Solution</summary>
<p>
```python
def draw(self):
    display.clear()
    display.set_pixel(self.food[0], self.food[1], 5)
    for part in self.snake:
      display.set_pixel(part[0], part[1], 9)
```

Since `self.snake` is a list of co-ordinates, we can use it in a `for` loop to get every co-ordinate that's part of the snake. We then use the `set_pixel` function to draw each part to the screen.
</p>
</details>

### Running our code

At this point, we should see some output, so let's go ahead and run our code. Whether or not you have a physical micro:bit, press `Ctrl`+`Enter` in the editor to bring up the micro:bit pop up. You can also click the cross in the corner and then click the green play button.

If you want to run the code on your physical micro:bit, click the "Download HEX" button in the top left corner. You can refer to the [Setting up environment section](#setting-up-environment) if you can't find it.

You should see something that looks like the below. If so, well done! If not, go back and check the solutions match your code exactly. Whitespace matters in Python as well, so check that carefully.

![Drawing to the screen](/images/microbitsnake/drawingtoscreen.svg)

Our snake is in the centre of the screen as a bright dot, and our food is at the left of the screen as a less bright dot. Yours might be in different positions depending on what you chose in [Creating the game state](#your-turn-1-filling-in-the-state). The next step is to make the snake move.

## Moving the snake

To understand how to move the snake, let's take a look at an example.

<video autoplay loop muted playsinline src="/images/microbitsnake/calcheadcuttail.mp4"></video>

The image shows a snake before and after moving down one cell. At first glance, moving the snake in this situation looks like it would be complicated, especially since it moves around a corner. Luckily for us though, it only consists of two actions.

1. Calculate the new head
2. Cut the tail off

So our first step will be to calculate the new head. We can do that with the help of `if` statements.

### Python `if` statements

Sometimes we want to choose what to do based on a condition. For example, you would want to wear a coat if it was raining outside, but if it was sunny you would put on sunglasses. You can do this in Python using `if` statements.

```python
# rain is a boolean variable (True or False)
if rain:
    put_on_coat()
else:
    # it must be sunny
    put_on_sunglasses()
# we'll go outside whether it's raining or sunny
go_outside()
```

You can even choose between more than two options. Sticking with the weather example, maybe it could be windy, rainy, or sunny. Being the responsible person that you are, you have clothes for each different possibility.

```python
# in this case, weather is a string
if weather == "rain":
    put_on_raincoat()
elif weather == "wind":
    put_on_jumper()
elif weather == "sunny":
    put_on_sunglasses()
go_outside()
```

### <i class="fa fa-lightbulb-o"></i> Your turn 3: Calculating the new head

We're going to be working in the `update()` function here, since that updates the game state before we draw the screen.

There are a few steps in calculating the new head of the snake.

1. Get current head of the snake (last item of the list)
2. Calculate a new head based on `self.direction`.
3. Add this head to the end of the list (`.append(item)` function)

The most difficult step here will be figuring out what to do for each direction. You might find this easier if you draw it out on a co-ordinate grid like the one in the [micro:bit co-ordinate system section](#the-microbit-co-ordinate-system).

**Important** - If you create the new head from the old head (e.g. `new_head = self.snake[-1]`), you will need to copy it. Otherwise you will have a really annoying bug. You can copy a list like so:

```python
# call list() to copy the old head
new_head = list(self.snake[-1])
```

<details><summary>What is the really annoying bug?</summary>
<p>
If you don't copy the head of the snake, then you will modify the existing head as well as creating a new one. Let's illustrate this with an example:

Let's imagine a snake at `[[1, 1], [2, 1], [2, 2]]` where `[2, 2]` is the head of the snake. Also let's say that the snake is moving south.

![Snake at `[[1, 1], [2, 1], [2, 2]]`](/images/microbitsnake/bugex1.png)

When we update the snake, we will take the head and update it to `[2, 3]` since it is heading downwards. Ordinarily this would mean the snake looks like this:

![Snake at `[[2, 1], [2, 2], [2, 3]]`](/images/microbitsnake/bugex2.png)

However, since we didn't copy the head, we'll end up modifying the existing one **and** appending it, so our snake will be at `[[2, 1], [2, 3], [2, 3]]`:

![Snake at `[[2, 1], [2, 3], [2, 3]]`](/images/microbitsnake/bugex3.png)

This is because lists in Python are _mutable_, which means that you can modify their values. When we type `new_head = self.snake[-1]` we're not creating a new list called `new_head`, we're assigning a new name to `self.snake[-1]`.

Some objects in Python, for example tuples, are _immutable_ which means their values cannot be changed. If we used tuples for the co-ordinates we would not have this problem. However, if we used tuples, the code wouldn't be as simple as incrementing or decrementing a co-ordinate, and it would introduce another concept to a beginner-friendly tutorial, something I'd like to keep to a minimum.
</p>
</details>

<details><summary>Solution</summary>
<p>
```python
def update(self):
    new_head = list(self.snake[-1])
    if self.direction == "up":
        # Y decreases as you go up the screen
        new_head[1] -= 1
    elif self.direction == "down":
        new_head[1] += 1
    elif self.direction == "left":
        # X decreases as you go left
        new_head[0] -= 1
    elif self.direction == "right":
        new_head[0] +=1
    # put the head on the end of the list
    self.snake.append(new_head)
```

Firstly we copy the old head of the snake, remember `-1` is the index of the last element of a list. Next we check what the current direction is, and increment or decrement the appropriate co-ordinate. Finally, we append the new head to the end of the snake list.
</p>
</details>

### <i class="fa fa-lightbulb-o"></i> Your turn 4: Removing the tail

Remember the `.pop(idx)` method on lists from before? You can remove an item from a list by calling this function with the index of the item that you want to remove.

```python
>>> my_list = [1, 2, 3]
>>> my_list.pop(0)
1
>>> my_list
[2, 3]
```

Your task is to remove the tail of the snake. Here's a hint, if we add the new head to the end of the snake list, then the tail will be at the start of it.

<details><summary>Solution</summary>
<p>
The full `update` function should now look like this:

```python
def update(self):
    new_head = list(self.snake[-1])
    if self.direction == "up":
        new_head[1] -= 1
    elif self.direction == "down":
        new_head[1] += 1
    elif self.direction == "left":
        new_head[0] -= 1
    elif self.direction == "right":
        new_head[0] +=1
    self.snake.append(new_head)
    # cut the tail of the snake
    self.snake.pop(0)
```
</p>
</details>

We're now ready to run this again, and our snake should now move!

<video autoplay loop muted playsinline src="/images/microbitsnake/microbiterror.mp4"></video>

Except, we get an error. The error on the simulator isn't very helpful, but on the micro:bit it makes more sense.

`ValueError: index out of bounds`

What's happening here is that our `new_head` is going out of bounds, which means it's becoming a value that can't be displayed on the screen. If you remember our co-ordinates diagram, the Y co-ordinate is getting smaller until it gets to -1. When we then try and call `display.set_pixel` with -1 as an input, it gives us an error, since there's no LED at `[2, -1]`.

We could fix this by ending the game if the snake goes out of bounds, but on a screen this small that wouldn't be much fun. Instead, let's fix it by wrapping our snake around the board.

## Wrapping

Wrapping just means that if the snake hits one side of the screen, then it should appear on the other side of the screen.

<video autoplay loop muted playsinline src="/images/microbitsnake/wrappingdemo.mp4"></video>

In the above example, the snake is moving up the screen. After the snake's head reaches `[3, 0]` it goes to `[3, 4]` and appears at the bottom of the screen. The snake continues to move upwards, just starting from the bottom of the screen now. We can implement this behaviour by checking the bounds of the `new_head`.

### <i class="fa fa-lightbulb-o"></i> Your turn 5: Wrap the screen

The bounds of our screen are 0-4 in both the X and Y axes. So you'll want to check if the X co-ordinate or the Y co-ordinate are less than/greater than these boundaries. If they are, reset them to the other edge of the screen.

Again, for this task we'll be working in our `update` method.

<details><summary>Solution</summary>
<p>
```python
def update(self):
    ... # the code from above
    elif self.direction == "right":
        new_head[0] +=1

    # X co-ordinate
    if new_head[0] > 4:
        new_head[0] = 0
    elif new_head[0] < 0:
        new_head[0] = 4
    # Y co-ordinate
    if new_head[1] > 4:
        new_head[1] = 0
    elif new_head[1] < 0:
        new_head[1] = 4

    self.snake.append(new_head)
    ...
```

We add a new `if` statement for both the X co-ordinate and the Y co-ordinate. In it, we check if they are above 4 or below 0 since those are the maximum co-ordinates of our display. This would also work if you only have a single `if/elif` block for both the X and Y since we'll only be changing one at a time.
</p>
</details>

When we add this code to our game, it should look like the below.

<video autoplay loop muted playsinline src="/images/microbitsnake/wrapping.mp4"></video>

## Getting input

At this point, we have an image on the screen and the snake moves! The user can't yet control the snake though, so let's add that in.

The micro:bit has a few different ways of getting input from the user and the world around it. Most visibly, it has two buttons on the front that the user can press. While we could use these for input, four directions doesn't map into two buttons in an intuitive way. Other inputs the micro:bit has include an accelerometer for detecting tilt and motion, a compass for direction relative to the earth, pins on the bottom for electrical input and a temperature sensor. Out of these, the accelerometer can provide the simplest method of control.

### Accelerometers

We won't try to understand how accelerometers work here, that would take a post of its own. However, we can understand what an accelerometer can do for us. If you've never heard of an accelerometer before, it's the bit of your phone that detects orientation and makes your videos landscape when you tilt your phone.

In short, an accelerometer can measure the tilt of a device, and we can use this for our game. To see how this will work, take a look at the video below.

<video autoplay loop muted playsinline src="/images/microbitsnake/accelphysdemo.mp4"></video>

The dot follows the tilt of the device here. When we tilt the device away from us, the dot heads up the screen (away from us). Tilting the device to the left, right or towards us have similar efects.

### Simulator only: How to use the accelerometer

> <video autoplay loop muted playsinline src="/images/microbitsnake/accelvirtdemo.mp4"></video>

> The micro:bit pop-up in the simulator has some tabs along the top for controlling the various components of the micro:bit. One of these tabs controls the accelerometer (seen in the video above). In the tab you will see three sliders, one for each axis, and a checkbox labelled "Move accelerometer with mouse". Go ahead and tick that checkbox.

> With the checkbox ticked, you'll notice that moving your mouse over the micro:bit's screen will change the accelerometer values in the sliders. As you head towards the lower-right corner of the micro:bit the values will increase, and as you head towards the upper-left corner they will decrease.

### <i class="fa fa-lightbulb-o"></i> Your turn 6: Updating direction

The accelerometer will return you values in the X and Y axes using the following functions. We don't care about the Z axis since our screen is 2D.

```python
# These functions return values in the range -2000 to 2000
accelerometer.get_x()
accelerometer.get_y()
```

The X axis increases going left to right, and the Y axis increases from top to bottom, just like the screen co-ordinates.

![Accelerometer axes](/images/microbitsnake/acceldir.png)

When deciding what direction to go in, you'll want to take the absolute maximum value of X and Y, so if X was 1700 and Y was -2000, you'd use the Y value and set direction to `"up"`. We're working in the `handle_input` function for this section.

You may find the absolute function, `abs(x)`, useful.

```python
# abs (the absolute function) will remove a minus sign if present
>>> abs(-30) == 30
True
# ... and leave the value alone if not
>>> abs(30) == 30
True
```

<details><summary>Solution</summary>
<p>
```python
def handle_input(self):
    # get accelerometer values
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    # compare the magnitude of X and Y
    if abs(x) > abs(y):
        # X is bigger than Y (maybe negative)
        if x < 0:
            self.direction = "left"
        else:
            self.direction = "right"
    else:
        # Y is bigger than X (maybe negative)
        if y < 0:
            self.direction = "up"
        else:
            self.direction = "down"
```

First we get the raw values from the accelerometer for X and Y, and then we compare their magnitudes using `abs()`. If X is bigger than Y, then we see whether X is negative (left) or positive (right). We do the equivalent checks when Y is bigger than X.
</p>
</details>

The user can now tilt the micro:bit to make the snake move! You may notice while playing with this that the snake will never grow, so now it's time to figure out how food works.

## Food

When the snake approaches some food, we want the snake to grow and the food to appear again in another location. Ideally, the process would look like the following animation.

<video autoplay loop muted playsinline src="/images/microbitsnake/food.mp4"></video>

Building our food mechanic can be split into two steps. Detecting and reacting to food being eaten, and then generating new food.

### <i class="fa fa-lightbulb-o"></i> Your turn 7: Eating food

The snake "eats" the food when its head is in the same cell as the food. When it eats the food, it should grow by one cell which can be done by not cutting the tail from the snake.

In the case that the snake is eating the food, you should leave some space in your code to generate the new food.

Hint: In Python you can compare two lists just with `list1 == list2`.

<details><summary>Solution</summary>
<p>
```python
def update(self):
    ...
    self.snake.append(new_head)
    if new_head == self.food:
        # generate new food
        pass
    else:
        # cut the tail of the snake
        self.snake.pop(0)
```

We compare the new head and the food. If they are the same then we leave some space in the code to generate the new food.

We cut the tail in the else block, which means that we only cut it when the snake isn't eating food.
</p>
</details>

### Random numbers

We want to generate new food randomly so that the game is interesting. We can do this using the `random` module in Python. Here's an example that guesses (poorly) how old you are.

```python
# import the function randint from the module random
from random import randint

# generate a random integer between 0 and 100 (inclusive)
age = randint(0, 100)

print(f"I bet you are {age} years old")
```

In this program we import then call the `randint(start, stop)` function. This will give us back a number between 1 and 100. We then print it out using an [f-string](https://realpython.com/python-f-strings/). Side note: if you haven't come across f-strings before, check out that link. They are very cool.

We'll be using this `randint` function to generate random co-ordinates.

### <i class="fa fa-lightbulb-o"></i> Your turn 8: Generating food

To generate new food, you'll need to generate an X co-ordinate and a Y co-ordinate. Remember, the axes run from 0 to 4.

One edge case you'll have to think about is what happens if the co-ordinates you generate are covered by the snake. The solution I'll recommend is to keep re-generating the co-ordinates until they are not in the snake, but feel free to come up with your own solutions here. You can check if the co-ordinates are inside the snake using the `in` keyword (`co_ords in self.snake`) and a `while` loop.

<details><summary>Solution</summary>
<p>
```python
def update(self):
    ...
    if new_head == self.food:
        self.food = [randint(0, 4), randint(0, 4)]
        while self.food in self.snake:
            self.food = [randint(0, 4), randint(0, 4)]
    ...
```

We use a `while` loop to check if the food we've generated is inside the snake or not. We keep generating the food until it's visible on the screen.
</p>
</details>

<details><summary>Is this really a valid solution?</summary>
<p>
In case you're having trouble believing that re-generating the food is a valid solution, let's take a look at some probabilities.

We can model generating the food successfully as a binomially distributed random variable. If the snake is of length two (the smallest case after eating food), then the probability of generating the food in an empty space is 23/25. This means that we have a 92% chance of success on the first go and a 99% chance of succeeding within two tries. The expected number of generations before our first success is just over 1.

Taking the worst case where the snake is length 24 after eating food, the probability of generating the food correctly is 1/25. This means that the expected number of trials before our first success is 25. In fact 63% of the time it will take 25 tries or fewer and 99% of the time it will take fewer than 113.

These numbers are very small for a computer, and we won't notice much delay in the snake's motion.
</p>
</details>

Our snake game is almost finished! The only step left is figuring out how to end the game.

## Ending the game

The game of snake ends in two situations. Firstly, if you crash into yourself (or the wall, in some versions) then you lose. Secondly, if you fill the entire grid with your snake then you win.

We'll worry about losing the game for now, and I'll leave winning the game as an extension to you.

### Loop control

We've seen `while` loops a couple of times so far. Most recently we used them to generate food, but at the very start we saw how our game loop is made of a `while` loop.

In Python, you have the ability to run a loop forever with `while True`. The complementary feature is that you have the ability to cut a loop short early using the `break` statement. Let's take a quick look at how it works.

In the below example, we wait for the micro:bit's button A to be pressed then show a happy face.

```python
# import all the microbit code
from microbit import *

while True:
    # check if button A was pressed since we last called this function
    if button_a.was_pressed():
        # if so, exit the loop
        break
    # wait for 100 milliseconds
    sleep(100)

# show a happy face
display.show(Image.HAPPY)
```

### <i class="fa fa-lightbulb-o"></i> Your turn 9: Ending the game

There are three steps to implementing losing the game.

1. Detect if you've crashed into yourself using the `in` keyword. This will be part of the `update` function.
2. Set `self.end` to `True` if the player has lost.
3. Use `break` in the game loop if the player has lost. `self.end` will be `game.end` inside the game loop.

You could also display a sad face, or scroll some text if the player loses. Get creative!

<details><summary>Solution</summary>
<p>
In our update function:

```python
def update(self):
    ...
    # after we calculate new_head
    if new_head in self.snake:
        self.end = True
    self.snake.append(new_head)
    ...
```

We've just added an `if` statement here to check whether the new head is already part of the snake.

In our game loop:

```python
while True:
    ...
    game.update()
    # now game.end will be set
    if game.end:
        display.show(Image.SAD)
        break
    game.draw()
    ...
```

We add an if statement to check whether `game.end` was set to `True` in `update` and if so we break. I've also added a sad face in there to make it more obvious that the player has lost, but that is optional.
</p>
</details>

## Final notes

Well done on making it this far! You've just built your very own game, and can be really proud of yourself. I hope you've enjoyed the experience and that it's inspired you to keep going with micro:bit, programming or game development. If you want some more material for learning, then check out the [Useful links](#useful-links) below. If you'd like to check your solution, I've put the [final code for this tutorial on GitHub](https://github.com/notexactlyawe/microbit-snake/blob/master/snake.py).

This tutorial was based off a workshop that I wrote while part of the Embedded and Robotics Society (EaRS) at Edinburgh. It was one of my favourite workshops there, and it's been fun to re-visit it and turn it into a full tutorial. If you like this, then they have more resources [on their website](http://ears-edi.com/) so you should check them out.

If you found any issues in this tutorial, have ideas for new tutorials you'd like to see, or have a question then feel free to [contact me](/contact). I'd love to hear from you.

## Extensions

Just because you finished this tutorial doesn't mean you have to stop working on the game. There are a number of extensions you could make to it, and you may even think of some of your own.

 - Implement a winning condition.
 - Stop the player from going in a direction opposite to the current one they're going in. This annoyed me while playing the game, since it means you lost when you go back into yourself, and most snake implementations prevent you from being able to do this.
 - Expand the game grid. Maybe you could have a grid that is bigger than the screen, and display a part of it at a time. You could show this by moving the food instead of the snake, or by flashing the screen when you drew a different area.

## Useful links

 - [Official Python editor for micro:bit](https://python.microbit.org/v/2.0)
 - [MakeCode for micro:bit (JavaScript/Scratch)](https://makecode.microbit.org/)
 - [Embedded and Robotics Society Edinburgh](http://ears-edi.com/)
 - [Original workshop slides](https://docs.google.com/presentation/d/1d5NM7Sf5eOalQJ1Otfe1fJ4gtUMj3hgkXyFJPTEyZik/edit?usp=sharing)
 - [UCL BBC micro:bit tutorial](https://microbit-challenges.readthedocs.io/en/latest/introduction/getting_started.html)

## Copyright

Pretty micro:bit SVG images were modified from the [Micro:bit Educational Foundation's GitHub repo](https://github.com/microbit-foundation/microbit-svg/) under the [CC BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/). Those images on this page are therefore licensed under the same terms.

All other content on this page is licensed under the <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">CC BY 4.0 license</a>.
