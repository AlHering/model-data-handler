# -*- coding: utf-8 -*-
"""
****************************************************
*                model_data_handler                 
*            (c) 2023 Alexander Hering             *
****************************************************
"""
from logging import Logger
from typing import Any, Optional, List
import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped
from sqlalchemy import func
from sqlalchemy import Column, String, Boolean, Integer, JSON, Text, DateTime, CHAR, ForeignKey, Table, Float, BLOB, TEXT
from sqlalchemy.orm import Session, relationship
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

            self.base = automap_base()
            self.base.prepare(self.engine, reflect=True)

        else:
            raise sql_utility.UnsupportedDialectError(db_dialect)
        

DATABASE = Database()

if "model" in DATABASE.base.metadata.tables:
    Model = DATABASE.base.model
else:
    class Model(DATABASE.base):
        """
        Class, representing a model.
        """
        __tablename__ = 'model'
        id = Column('id', Integer, primary_key=True, autoincrement=True, comment="Model ID.")
        file = Column('file', String, required=True, comment="Model file.")
        extension = Column('extension', String, required=True, comment="Model file extension.")
        path = Column('path', Text, required=True, comment="Model path.")

        sha256 = Column('sha256', Text, required=True, comment="Model SHA256 hash.")
        status = Column('status', String, default="found", comment="Model status.")
        source = Column('source', String, comment="Model source.")
        api_url = Column('api_url', Text, comment="Model API URL.")
        metadata = Column('metadata', JSON, comment="Model metadata from source.")
        local_metadata = Column('local_metadata', JSON, comment="Local model metadata.")
        
        created = Column('created', DateTime, server_default=func.sysdate(), comment="Timestamp of creation.")
        updated = Column('updated', DateTime, server_default=func.sysdate(), server_onupdate=func.sysdate(), comment="Timestamp of last update.")
        inactive = Column('char', CHAR, default='', comment="Flag for marking inactive entries.")

    DATABASE.base.create_all()