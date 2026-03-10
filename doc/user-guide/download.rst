Data download & update
======================

.. _location:

Data location
-------------

If you are in the SEASTERS project, you should have access to a shared sDrive workspace
dedicated to the project. If not, you can contact the project's PIs so they can add you
to this workspace. Once in the group, you should see a ``DR14_UMR5566_SEASTERS`` shared
project. In this folder, the ``Database`` subfolder contains the data we want to access
with seastersdb. It is only about 5 GB and can thus easily be downloaded to work on it
offline.

This ``Database`` folder should already be synchronized on the three clusters used in
SEASTERS:

- At CNRM: ``/cnrm/tropics/commun/DATACOMMUN/SEASTERS``
- On HILO: ``/data/projects/LOTUS/SEASTERS``
- On Calmip: ``/tmpdir/desmet/SEASTERS``

.. note::

   This is the directory you will need to provide when running ``seastersdb-locate`` at
   :ref:`installation <install-main>`. You may also download the database locally; in
   this case, simply provide the corresponding local directory.


.. _rclone:

Download & update: ``rclone``
-----------------------------

You may download the database manually from your browser. However, depending on your
connection and browser, this may take a while and/or you may struggle in case of
network instability or interruption.
For this reason, we recommend using ``rclone`` to connect to sDrive using the WebDAV
protocol.


Installation
~~~~~~~~~~~~

If you have root permission, ``rclone`` can be installed with:

.. code:: shell

   sudo apt install rclone


Otherwise, it can also be installed inside a Conda environment using:

.. code:: shell

   conda install conda-forge::rclone


Retrieve WebDAV access information to sDrive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To configure a remote with ``rclone``, we need a link, login and password. Let us
retrieve those on sDrive.

#. Go online and login to your sDrive account
#. Click "File settings" in the lower left corner
#. In the WebDAV section: **save the link**
#. Click the link below that indicates something to do with 2FA
#. Create a new app password with a name relating to the machine you will connect from
#. A pop-up appears: save the provided **login** and **password**


Configure ``rclone``
~~~~~~~~~~~~~~~~~~~~

#. Run ``rclone config``
#. Create a new remote (e.g., with name "sdrive")
#. Follow to the instructions: you should choose stuff relating to "WebDAV", and enter
   the link, login and password you've previously saved
#. No bearer token
#. No advanced config


Download & update
~~~~~~~~~~~~~~~~~

We can now use `rclone copy <https://rclone.org/commands/rclone_copy/>`_ to download
our database locally, from the ``sdrive`` remote we have registered.
We recommend the following (changing the paths adequately):

.. code:: shell

   rclone copy sdrive:/DR14_UMR5566_SEASTERS/Database /path/to/SEASTERS --verbose --stats=5s --stats-one-line > rclone.log 2>&1 & 


.. error::

   It is possible that your machine badly supports multithreading, leading ``rclone`` to
   raise errors. In this case, simply add the ``--multi-thread-streams=0`` option.


``rclone copy`` copies files from source to destination, skipping identical files. The
same command is thus also relevant for updating.
