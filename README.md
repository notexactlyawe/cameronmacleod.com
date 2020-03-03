cameronmacleod.com
==================

These are the source files that I use to generate my personal site with. [Pelican](https://docs.getpelican.com) is the static site generator that I use. The output from Pelican is also stored here on GitHub in a [separate repository](https://github.com/notexactlyawe/notexactlyawe.github.io) since I use GitHub pages to host.

To get up and running with this site, you need to install Pelican, which can be done with Pip.

`pip install pelican`

The version I am using is 3.7.1.

Developing
----------

Running `pelican` will use `pelicanconf.py` by default, which will output files to `develop-output`. When you want to publish, run `pelican -s publishconf.py` and it will output publishable files (including absolute URLS, feeds etc) to the folder `notexactlyawe.github.io`.

Contributing
------------

If you spot an error in content or a typo on my site anywhere, please feel free to correct it here and submit a pull request. I would appreciate it.
