Compatibility table
```````````````````

.. |unknown| image:: assets/grey.png
    :width: 16
    :height: 16

.. |none| image:: assets/black.png
    :width: 16
    :height: 16

.. |low| image:: assets/red.png
    :width: 16
    :height: 16

.. |partial| image:: assets/yellow.png
    :width: 16
    :height: 16

.. |most| image:: assets/blue.png
    :width: 16
    :height: 16

.. |full| image:: assets/green.png
    :width: 16
    :height: 16

Key
^^^

.. note:: This color system is subjective.

============    ===========
Color           Meaning
============    ===========
|unknown|       unknown
|none|          none
|low|           low
|partial|       partial
|most|          most
|full|          full
============    ===========

Status
^^^^^^

=======================   =====================   ============   ========================================================================================================  =============================================
Parser                    Status                  Alias of       Supported parser version                                                                                  Source
=======================   =====================   ============   ========================================================================================================  =============================================
``cmark``                 |most|                                 Version 0.28 (2017-08-01)                                                                                 https://github.com/commonmark/cmark
``commonmarker``          |most|                  ``github``                                                                                                               https://github.com/gjtorikian/commonmarker
``github``                |most|                                 Version 0.28-gfm (2017-08-01)                                                                             https://github.com/github/cmark
``gitlab``                |partial|               ``github``                                                                                                               https://docs.gitlab.com/ee/user/markdown.html
``redcarpet``             |low|                                  `Redcarpet v3.5.0 <https://github.com/vmg/redcarpet/tree/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae>`_      https://github.com/vmg/redcarpet
Gogs                      |unknown|                                                                                                                                        https://gogs.io/
NotABug Gogs fork         |unknown|                                                                                                                                        https://notabug.org/hp/gogs/
Marked                    |unknown|                                                                                                                                        https://github.com/markedjs/marked
kramdown                  |unknown|                                                                                                                                        https://kramdown.gettalong.org/
=======================   =====================   ============   ========================================================================================================  =============================================
