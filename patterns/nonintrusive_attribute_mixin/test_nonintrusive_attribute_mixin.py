import logging


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


def test_example():
    class Reporter(LogMixin):
        pass

    class Worker(LogMixin):
        log_level = logging.DEBUG

    assert Reporter().log.name == "Reporter"
    assert Reporter().log.level == logging.INFO

    assert Worker().log.name == "Worker"
    assert Worker().log.level == logging.DEBUG
