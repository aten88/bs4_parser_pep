class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserGetResponseException(Exception):
    """ Вызывается, когда парсер не может найти страницу """
    pass
