Title: How to read WAVE files in Python
Date: 2016-04-07
Slug: reading-wave-python
Category: Python

Any project that uses audio will usually start out using WAVE files for its on-disk presence, and as with many things in Python, there's a standard library module for that. Now don't get me wrong in the rest of this article - `wave` does the job. The thing is that it can be a bit confusing to get started with and it's not *always* the best tool for the job. This post will go over my journey in reading WAVEs and the various approaches I found.

When you read [the documentation](https://docs.python.org/2/library/wave.html) for `wave`, you quickly find the `readframes()` function for reading the meat of the file. This just as quickly poses a problem, that of how to parse the data it returns.

```
'\xd04\xd52\xd63\x824...'
```
Of course, this wouldn't pose even the hint of a problem if we bothered to read [the spec](http://www-mmsp.ece.mcgill.ca/documents/audioformats/wave/wave.html) for wave files, but who reads those? As a result, I found myself writing some convoluted string parser that was the textbook example of treating the symptom as opposed to the cause. It also didn't really work. It would technically be a valid solution, but there is little point getting it up and running because there are better ways.

The next level up is discovering the `struct` module. `struct` is a module that allows for the reading of raw binary data into native Python types that I discovered - after some pained googling - in [this Stack Overflow question]. `struct.unpack()` contains all of the magic that we need. It takes a format string and the data that you want to extract. The below is an example from the git history of [abracadabra](http://github.com/notexactlyawe/abracadabra).

```python
def read_whole(filename):
    wav_r = wave.open(filename, 'r')
    ret = []
    while wav_r.tell() < wav_r.getnframes():
        decoded = struct.unpack("<h", wav_r.readframes(1))
        ret.append(decoded)
    return ret
```

As a quick explanation of the format string, the `<` indicates little-endian data (defined in the spec) and the `h` 1 signed 16-bit int. Before you think "Hooray, a code snippet! I can leave now.", there are a few problems with this approach. Firstly, wave data is not guaranteed to contain int16s and so this would fall down on a good number of files. Second, it's horrendously slow.

Tackling the second issue first, you could minimise the number of calls to `unpack()`. Calling it with fmt as `"<hh"` it would expect two int16s, `"<hhhhh"` would expect 5. You could change the above code to use this as so:

```python
...
chunk_size = 16
while wav_r.tell() < wav_r.getnframes():
    fmt = "<" + "h" * chunk_size
    try:
        decoded = struct.unpack(fmt, wav_r.readframes(chunk_size))
    except struct.error:
        # (w.getnframes() - w.tell()) < chunk_size
        tmp_size = w.getnframes() - w.tell()
        tmp_fmt = "<" + "h" * chunk_size
        decoded = struct.unpack(tmp_fmt, wav_r.readframes(tmp_size))
...
```

Yet again, as this article is a journey as opposed to a straight out answer, this ugly hack does not come recommended. In general, I find that ugly code == doing things wrong. This example is no different, but is easily fixed.

```python
...
fmt = "<{0}h".format(chunk_size)
...
```

As an aside, if you are not already using this way to construct format strings, please take the time to internalise it. But back to the change, this works due to an unremarkable looking line in the docs for `struct`.

> A format character may be preceded by an integral repeat count. For example, the format string '4h' means exactly the same as 'hhhh'.

Much better, no?

Our next issue was that the data isn't guaranteed to come in signed 16-bit integers. The good news is that we can get what format it is in programmatically with our old friend, the `wave` module. The below code is from abracadabra.

```python
def __init__(self, filename, read=True, debug=False):
    mode = 'r' if read else 'w'
    sizes = {1: 'B', 2: 'h', 4: 'i'}
    self.wav = wave.open(filename, mode)
    ...
    self.channels = self.wav.getnchannels()
    self.fmt_size = sizes[self.wav.getsampwidth()]
    self.fmt = "<" + self.fmt_size * self.channels
```

If you have read the WAVE spec you will see that BitsPerSample is 2 bytes, suggesting that getsampwidth() could return an arbitrary value between 0 and 8192. In reality, you are not likely to encounter greater than 32 bit audio in the wild and `sizes` reflects this. Saying this, it would probably be good practice to catch KeyError when setting fmt_size and raising a more readable error.

So we now have a working solution, and I have used this in production code before now. There is, however, another optimisation you could make assuming that the files you are loading in aren't overly large and it involves the `array` module. `array` is advertised in the docs as memory efficent arrays, but for our purposes we care more that its implemented in straight C and is lightning fast. It's also pretty easy to use.

```python
a = array.array(self.fmt_size)
a.fromfile(open(self.filename, 'rb'), os.path.getsize(self.filename)/a.itemsize)
```

You just pass it a format string (of the same format as struct) and then call `fromfile` with a file object and the size of it. According to [this](http://stackoverflow.com/questions/5804052/improve-speed-of-reading-and-converting-from-binary-file-with-python) SO question it is up to 40X faster than `struct.unpack` *YMMV*.

This has been my journey in attempting to read WAVE files and hopefully it will help. Most of the code in here has been adapted from my repository [abracadabra](https://github.com/notexactlyawe/abracadabra) and if you are looking for an up-to-date version of what I am using there might be a good place to look. This article is [also on Github](https://github.com/notexactlyawe/cameronmacleod.com) so if you see something wrong, please submit an issue.
