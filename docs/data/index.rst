

Data
====

The SEASTERS database includes data from four station networks across Southeast Asia.
The cards below point the networks' description, with useful links and references.

.. toctree::
   :maxdepth: 1
   :hidden:

   ghcnd
   ghcnh
   gsdr
   bsrn


.. grid:: 2
   :gutter: 2

   .. grid-item-card:: GHCNd
      :link: ghcnd
      :link-type: doc
      :text-align: center
      :class-card: intro-card

      Global daily station records

   .. grid-item-card:: GHCNh
      :link: ghcnh
      :link-type: doc
      :text-align: center
      :class-card: intro-card

      Global hourly-ish station records

   .. grid-item-card:: GSDR
      :link: gsdr
      :link-type: doc
      :text-align: center
      :class-card: intro-card

      Dense hourly gauge data in Australia, India, Japan and Malaysia

   .. grid-item-card:: BSRN
      :link: bsrn
      :link-type: doc
      :text-align: center
      :class-card: intro-card

      Minutely radiation data from a few remote stations


.. tip::

   Download all reference papers as a ``.bib`` file:
   :download:`references.bib <../_static/references.bib>`.


Each network has independent relational tables, such that the database can be
represented with the relational schema below:

.. code:: shell

   Image TODO


TODO: footnote

Data was curated considering an extended Southeast Asian area, including stations from
the following territories:

.. hlist::
   :columns: 3

   * Australia
   * Bangladesh
   * Bhutan
   * Brunei
   * Cambodia
   * China
   * Christmas Island
   * Cocos (Keeling) Islands
   * Federated States of Micronesia
   * Guam
   * Hong Kong
   * India
   * Indonesia
   * Japan
   * Laos
   * Macau
   * Malaysia
   * Myanmar
   * Nepal
   * Northern Mariana Islands
   * Palau
   * Papua New Guinea
   * Philippines
   * Singapore
   * Solomon Islands
   * Sri Lanka
   * Taiwan
   * Thailand
   * Timor-Leste
   * Vietnam

