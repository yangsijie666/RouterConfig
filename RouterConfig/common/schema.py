from jsonschema import validate, ValidationError


def validate_schema(data_schema, logger=None):
    """
    validate if the data that user input is valid
    :param data_schema: the schema
    :param logger: the logger
    :return:
    """
    def decorator(main_func):

        def wrapper(*args, **kwargs):

            try:
                validate(kwargs.get('body'), data_schema)
            except ValidationError as e:
                if logger is not None:
                    logger.error(e.message, exc_info=True)
                raise
            return main_func(*args, **kwargs)

        return wrapper

    return decorator