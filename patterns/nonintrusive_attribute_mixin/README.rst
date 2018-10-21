Nonintrusive Attribute Mixin
============================

A good mixin doesn't make its user worry about calling ``super().__init__()`` in the right order or any other hooks.
It just injects the functionality.

Descriptors and type hints were born for this.

.. code-block:: python

    class LogMixin:

        class _Log:
            def __set_name__(self, name, owner):
                self._attr_name = f"_log#{name}"

            def __get__(self, instance, owner):
                if instance is None:
                    return self
                if not hasattr(instance, self._attr_name):
                    setattr(instance, self._attr_name, logging.getLogger(owner.__name__))
                logger = getattr(instance, self._attr_name)
                logger.setLevel(instance.log_level)
                return logger

        log: logging.Logger = _Log()
        log_level: int = logging.INFO


Now your ``LogMixin`` user will have ``log`` attribute which will be of the right type and will
have the name of the class it belongs to.

.. code-block:: python

    class Reporter(LogMixin):
        pass

    class Worker(LogMixin):
        log_level = logging.DEBUG

    assert Reporter().log.name == "Reporter"
    assert Reporter().log.level == logging.INFO

    assert Worker().log.name == "Worker"
    assert Worker().log.level == logging.DEBUG


Why did we mention type hints? Because without saying ``log: logging.Logger`` your IDE probably
wouldn't know that ``Reporter().log`` is a logger (because ``_Log.__get__`` returns either a ``_Log``
or a ``logging.Logger``), but now it does.
