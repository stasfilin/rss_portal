class ParsingError(Exception):
    """
    Exception for parser when we can't get articles
    """

    message: str = "nodename nor servname provided, or not known"
