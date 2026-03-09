Tool installation guide
=======================

seastersdb is a Python tool publicly available on its
`GitHub repository <https://github.com/DesmetQuentin/seastersdb>`_.
It provides both the Python API to be used inside your Python scripts and the
interactive session program that allows accessing the database with no Python knowledge
requirements. This installation guide is thus essential to follow, whether you use
Python or not.

Before continuing further, make sure you can use:

- the ``git`` version control system;
- and some kind of virtual environment manager (examples below are given for ``venv`` and
  ``conda``).

If not, please install them manually or contact your administrator.


.. _venv:

Virtual environment
-------------------

First thing is to **create a virtual environment** to ensure seastersdb requirements
do not conflict with the Python tools already installed on your machine.
seastersdb supports Python versions 3.10 to 3.12. In the example below, we use the
version 3.12. Follow the adequate tab below according to your virtual environment
manager.

.. tab-set::

   .. tab-item:: Conda

      Create:

      .. code:: bash

         conda create --name seasters python=3.12

      Activate:

      .. code:: bash

         conda activate seasters

      To deactivate the environment
      (keep it activated for continuing the installation, though):

      .. code:: bash

         conda deactivate


   .. tab-item:: venv

      Create (you may need to adapt the directory below):

      .. code:: bash

         python3.12 -m venv ~/venv/seasters

      Activate:

      .. code:: bash

         source ~/venv/seasters/bin/activate

      To deactivate the environment
      (keep it activated for continuing the installation, though):

      .. code:: bash

         deactivate


.. _install-main:

Installation & setup
--------------------

From within your ``seasters`` virtual environment, you can now **install seastersdb**:

.. code:: shell

   pip install git+https://github.com/DesmetQuentin/seastersdb.git


This should install seastersdb and its dependencies.

Then, we need to **let seastersdb know where is the database** on your machine.
The database is currently deployed in three locations: CNRM, HILO and Calmip.
We use the ``seastersdb-locate`` command, indicating the adequate directory:

.. tab-set::

   .. tab-item:: CNRM

      .. code:: shell

         seastersdb-locate /cnrm/tropics/DATACOMMUN/SEASTERS


   .. tab-item:: HILO

      .. code:: shell

         seastersdb-locate /data/project/lotus/SEASTERS
      

   .. tab-item:: Calmip

      .. code:: shell

         seastersdb-locate /tmpdir/desmet/SEASTERS
     

This should output the following confirmation message:

.. code:: console

   API configuration completed!


Testing
-------

You should now be able to **run the interactive session** by typing in the terminal:

.. code:: shell

   seastersdb &

(The ``&`` symbol avoids to put your terminal session on hold.)


To **use the Python API**, simply import ``seastersdb`` in a Python script.
For instance:

.. code:: pycon

   >>> import seastersdb as sdb
   >>> sdb.VERSION
   '2.0.0'
