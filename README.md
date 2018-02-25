
# Get Lazio Weather Data

Project to grab public historical weather data about the region of Lazio
in Italy. 

## Getting Started

This project is born to get data necessary for assignment *Becoming an Independent Data Scientist*
 in course [Applied Plotting, Charting & Data Representation in Python](https://www.coursera.org/learn/python-plotting) 
 at [Coursera](https://www.coursera.org/) , regarding the interest of the author
 about meteo in Rome, Lazio, Italy.

The project has four files:

* *gwd.py* to get data from web server using POST requests;
* *g2wd.py*, uses repeatedly *gwd.py* to obtain yearly data about stations 
and years listed in *config.py* file;
* *data.csv*, is an example of output from *g2wd.py*, used to develop
the course assignment.

These instructions will get you a copy of the project on your local machine.

### Prerequisites

This software needs [Python version 3.x](https://www.python.org/downloads/release/python-364/) 
and a couple of auxiliary libraries:

* [requests](https://pypi.python.org/pypi/requests/2.18.4) , used to send POST requests to web server;
* and [lxml](https://pypi.python.org/pypi/lxml/4.1.1) , in case of html parsing necessity.

### Installing

If you haven't Python installed, download and install it.

How to install Python depends on your operating system. On Windows and Mac OS X
you get the installer from https://www.python.org/downloads/release/python-364/ .

If you are on Linux, please refer to the documentation of your distribution.

Once Python is installed, to prepare the environment to run this project 
is so simple as:

* make a directory,
* optionally (but recommended) create and activate a virtual environment,
* install *requests* and *lxml*,
* copy the projects files, and use them.

As an example:

```
mkdir gwd
cd gwd
python -m venv venv
source venv/bin/activate           # in windows: venv\scripts\activate
pip install requests
pip install lxml
...

```

Some examples about how to use it.

First of all go to the project directory and activate the environment:

```
mkdir gwd
cd gwd
source venv/bin/activate           # in windows: venv\scripts\activate
```

How get help:

```
python gwd.py -h
```

How get the list of the meteo stations in Lazio:

```
python gwd.py -l
```

How get precipitation data about ACILIA station, year 2003, to standard output
(it's an html page):

```
python gwd.py -s ACILIA -y 2003
```

If you wish, you can redirect output to file and then open it using 
your web browser. For example, creating the *acilia-2003.html* file:

```
python gwd.py -s ACILIA -y 2003 >acilia-2003.html
```

How get only the total precipitation about ACILIA station, year 2003:

```
python gwd.py -s ACILIA -y 2003 -t
```


## Authors

* **Luciano De Falco Alfano** - *Initial work* - [l-dfa](http://github.com/l-dfa)

## License

This project is licensed under the [CC by 4.0](https://creativecommons.org/licenses/by/4.0/) License -
 see the [LICENSE.md](LICENSE.md) file for details
