.. _bsrn:

TODO (BSRN)
===========

Description
-----------

.. epigraph::

   TODO

   **Source:** TODO.

      
Variable overview
-----------------

Four dataset types were included in the database. 

.. tab-set::

   .. tab-item:: ``SYNOP``

      **Query:**

      .. code:: sql

         SELECT variable, long_name, units
         FROM bsrn_var()
         WHERE dataset == 'SYNOP'
         ORDER BY variable


      **Response:**

      .. code:: console

         ┌──────────┬───────────────────────────────────────┬─────────┐
         │ variable │               long_name               │  units  │
         │ varchar  │                varchar                │ varchar │
         ├──────────┼───────────────────────────────────────┼─────────┤
         │ CH       │ High cloud                            │ code    │
         │ CL       │ Low cloud                             │ code    │
         │ CM       │ Middle cloud                          │ code    │
         │ N        │ Total cloud amount                    │ code    │
         │ Nh       │ Low/middle cloud amount               │ code    │
         │ PPPP     │ Station pressure reduced to sea level │ hPa     │
         │ TTT      │ Temperature, air                      │ °C      │
         │ TdTdTd   │ Dew/frost point                       │ °C      │
         │ VV       │ Horizontal visibility                 │ code    │
         │ dd       │ Wind direction                        │ deg     │
         │ ff       │ Wind speed                            │ m/s     │
         │ h        │ Cloud base height                     │ code    │
         │ ww       │ Present weather                       │ code    │
         ├──────────┴───────────────────────────────────────┴─────────┤
         │ 13 rows                                          3 columns │
         └────────────────────────────────────────────────────────────┘
   

   .. tab-item:: ``radiation``

      **Query:**

      .. code:: sql

         SELECT variable, long_name, units
         FROM bsrn_var()
         WHERE dataset == 'radiation'
         ORDER BY variable


      **Response:**

      .. code:: console

         ┌─────────────┬────────────────────────────────────────────────────────────┬─────────┐
         │  variable   │                         long_name                          │  units  │
         │   varchar   │                          varchar                           │ varchar │
         ├─────────────┼────────────────────────────────────────────────────────────┼─────────┤
         │ DIF         │ Diffuse radiation                                          │ W/m**2  │
         │ DIF max     │ Diffuse radiation, maximum                                 │ W/m**2  │
         │ DIF min     │ Diffuse radiation, minimum                                 │ W/m**2  │
         │ DIF std dev │ Diffuse radiation, standard deviation                      │ W/m**2  │
         │ DIR         │ Direct radiation                                           │ W/m**2  │
         │ DIR max     │ Direct radiation, maximum                                  │ W/m**2  │
         │ DIR min     │ Direct radiation, minimum                                  │ W/m**2  │
         │ DIR std dev │ Direct radiation, standard deviation                       │ W/m**2  │
         │ LWD         │ Long-wave downward radiation                               │ W/m**2  │
         │ LWD max     │ Long-wave downward radiation, maximum                      │ W/m**2  │
         │ LWD min     │ Long-wave downward radiation, minimum                      │ W/m**2  │
         │ LWD std dev │ Long-wave downward radiation, standard deviation           │ W/m**2  │
         │ PoPoPoPo    │ Station pressure                                           │ hPa     │
         │ RH          │ Humidity, relative                                         │ %       │
         │ SWD         │ Short-wave downward (GLOBAL) radiation                     │ W/m**2  │
         │ SWD max     │ Short-wave downward (GLOBAL) radiation, maximum            │ W/m**2  │
         │ SWD min     │ Short-wave downward (GLOBAL) radiation, minimum            │ W/m**2  │
         │ SWD std dev │ Short-wave downward (GLOBAL) radiation, standard deviation │ W/m**2  │
         │ T2          │ Air temperature at 2 m height                              │ °C      │
         ├─────────────┴────────────────────────────────────────────────────────────┴─────────┤
         │ 19 rows                                                                  3 columns │
         └────────────────────────────────────────────────────────────────────────────────────┘


   .. tab-item:: ``radiosonde``

      **Query:**

      .. code:: sql

         SELECT variable, long_name, units
         FROM bsrn_var()
         WHERE dataset == 'radiosonde'
         ORDER BY variable


      **Response:**

      .. code:: console

         ┌──────────┬─────────────────────────────┬─────────┐
         │ variable │          long_name          │  units  │
         │ varchar  │           varchar           │ varchar │
         ├──────────┼─────────────────────────────┼─────────┤
         │ Altitude │ ALTITUDE                    │ m       │
         │ PPPP     │ Pressure, at given altitude │ hPa     │
         │ TTT      │ Temperature, air            │ °C      │
         │ TdTdTd   │ Dew/frost point             │ °C      │
         │ dd       │ Wind direction              │ deg     │
         │ ff       │ Wind speed                  │ m/s     │
         └──────────┴─────────────────────────────┴─────────┘


   .. tab-item:: ``radiation_10m``

      **Query:**

      .. code:: sql

         SELECT variable, long_name, units
         FROM bsrn_var()
         WHERE dataset == 'radiation_10m'
         ORDER BY variable


      **Response:**

      .. code:: console

         ┌──────────┬──────────────────────────────────────┬─────────┐
         │ variable │              long_name               │  units  │
         │ varchar  │               varchar                │ varchar │
         ├──────────┼──────────────────────────────────────┼─────────┤
         │ LWU      │ Long-wave upward radiation           │ W/m**2  │
         │ SWU      │ Short-wave upward (REFLEX) radiation │ W/m**2  │
         └──────────┴──────────────────────────────────────┴─────────┘


.. _bsrn-cite:

How to cite?
------------

TODO.


References
----------

.. bibliography::
   :list: bullet
   :filter: key % "BSRN:"
