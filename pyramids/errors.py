from loguru import logger

class ReadOnlyError(Exception):
    """ReadOnlyError"""

    def __init__(self, error_message: str):
        logger.error(error_message)

    pass


class DatasetNoFoundError(Exception):
    """DatasetNoFoundError"""

    def __init__(self, error_message: str):
        logger.error(error_message)

    pass


class NoDataValueError(Exception):
    """NoDataValueError"""

    def __init__(self, error_message: str):
        logger.error(error_message)

    pass


class AlignmentError(Exception):
    """Alignment Error"""

    def __init__(self, error_message: str):
        logger.error(error_message)

    pass

class DriverNotExistError(Exception):

    def __init__(self, error_message: str):
        logger.error(error_message)

    pass