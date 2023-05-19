# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from logging import Logger
from typing import Any, Optional, List
from ..utility.silver import sql_utility
from ..configuration import configuration as cfg


class Database(object):
    """
    Class, representing database.
    """
    def __init__(self, db_uri: str = cfg.DB_URI, db_dialect: str = cfg.DB_DIALECT) -> None:
        """
        Initiation method.
        :param db_uri: Database URI. Defaults to sqlite DB, which is created under data/model_data_handlers.db.
        :param db_flavor: Database flavor. Defaults to 'sqlite'.
        """
        if db_dialect in sql_utility.SUPPORTED_DIALECTS:
            self.uri = db_uri
            self.dialect = db_dialect
            self.engine = sql_utility.get_engine(self.uri)
            self.session_factory = sql_utility.get_session_factory(self.engine)
        else:
            raise sql_utility.UnsupportedDialectError(db_dialect)