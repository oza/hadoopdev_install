# What's this?

A setup script for hadoop development environment on Ubuntu/Debian.
This script installs:

1. Oracle JDK 1.7
2. protocol buffers 2.5.0 from source code
3. maven 3.0.5
4. git

## Prerequirements

* python (Confirmed that this script run with 2.7.6)
* [fabric](http://www.fabfile.org/)
    * It's an easy way to use pip to install fabric:

    pip install fabric

## How to use

Please use this script with fabric.

    $ fab setup_hadoopdev
    No hosts found. Please specify (single) host string for connection: <enter the host>
    ...<before installing JDK7, you need to press enter key.>...

Now, you can build hadoop!
[Document of Fabric](http://fabric.readthedocs.org/en/1.8/) is also useful.


## Misc.

This software is distributed under Apache License, Version 2.0.


