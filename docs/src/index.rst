.. skeleton documentation master file, created by
   sphinx-quickstart on Thu May 17 15:17:35 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SKA Base Images
===============

This repository contains the definition of the base image that's deprived of application level dependencies for SKAO developers to use as a base image when building their own products or other variant base images.

This will make possible to create and release a security patched Ubuntu 22.04 base image without any application dependencies and to implement a monthly security patch process for all ST services and images.

Currently, we provide the following images:

* ska-base: CIS hardened Ubuntu 22.04 base image
* ska-build: Ubuntu 22.04 based build image (with Python3)
* ska-build-python: Ubuntu 22.04 based build image for Python applications
* ska-python: Ubuntu 22.04 based base image for Python applications

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README

.. only:: on_gitlab

   .. toctree::
      :maxdepth: 2
      :caption: Reports:

      reports/oval
      reports/standard
      reports/cis_level2
      reports/stig
