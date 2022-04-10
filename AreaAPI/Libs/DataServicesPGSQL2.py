import sqlite3
import pandas as pd
import os
import psycopg2
import psycopg2.extras
import configparser

class DBServices:
    def __init__(self, config_file):

        self.conn = None

        if config_file == None:
            config = "styng.ini"

        config = configparser.ConfigParser()

        configFilePath =  config_file



        config.read(configFilePath)

        try:
            self._dbname = config.get('SectionOne', 'dbname')
            _conn_string = "dbname='"+ self._dbname + "'"
        except Exception:
            raise Exception("Error: Database name should be specified")

        try:
            self._user = config.get('SectionOne', 'user')
            _conn_string += "user='" + self._user + "'"
        except Exception:
            raise Exception("Error: database user should be specified")

        try:
            self._password = config.get('SectionOne', 'password')
            _conn_string += "password='" + self._password + "'"
        except Exception:
            raise Exception("Error database password should be specified")

        try:
            self._host = config.get('SectionOne', 'host')
            _conn_string += "host='" + self._host + "'"
        except Exception:
            raise Exception("Error: host should be specified")

        try:
            self._port = config.get('SectionOne', 'port')
            _conn_string += "port='" + self._port + "'"
        except Exception:
            raise Exception("ERROR: database port should be specified ")


        # self.dbname = "fusix"
        # self.user = "postgres"
        # self.password = "dptg@123"
        # self.host = "localhost"
        # self.port = "5432"
        # self.conn = None
        #
        # # build connection string
        # _conn_string = "dbname='" + self.dbname + "'"
        # _conn_string += "user='" + self.user + "'"
        # _conn_string += "password='" + self.password + "'"
        # _conn_string += "host='" + self.host + "'"
        # _conn_string += "port='" + self.port + "'"

        try:
            self.conn = psycopg2.connect(_conn_string)
        except Exception as e:
            raise Exception("ERROR: Opening database connection " + str(e))

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def get_data_2(self, service, params):
        """
        Execute a query that returns data

        Generic method to execute query that returns one or more rows

        :param service: The service to be executed
        :param params: The parameters for the service as a dictionary
        :return: A dictionary with results
        """

        # def dict_factory(cursor, row):
        #     d = {}
        #     for idx, col in enumerate(cursor.description):
        #         d[col[0]] = row[idx]
        #     return d



        # self.conn.row_factory = dict_factory

        #_cursor = self.conn.cursor()


        _cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:  # to execute sql
            _cursor.callproc(service, params)
            _result = _cursor.fetchall()
            #dictRows = {n['id']: n for n in _cursor}
            self.conn.rollback()
            return _result
        except Exception as e:
            print(e.__str__())
            raise e

    # def upd_multiple_records(self, service, records):
    #     """
    #     Update multiple records
    #
    #     Update multiple records in the database
    #
    #     :param service: The service that update the data
    #     :param records: The list of parameter's vectors
    #     :return:
    #     """
    #
    #     _service = self.db_path + self.catalog[service]
    #     with psycopg2.connect(self.db_file) as conn:
    #         try:
    #             with open(_service) as sql:
    #                 _cursor = conn.cursor()
    #                 try:
    #                     _qry = sql.read()
    #                     for record in records:
    #                         _cursor.execute(_qry, record)
    #                     conn.commit()
    #                 except Exception as e:
    #                     conn.rollback()
    #                     print(e.__str__())
    #                     raise e
    #         except FileNotFoundError as e:
    #             print(e.__str__())
    #             raise FileNotFoundError(service + " file not found")

    def update_record(self, service, params):
        """
        Generic service database modification

        Executes a query that modify the database
        INSERT / DELETE / UPDATE or combinations
        of all fo then


        :param fields:
        :return: Nothing
        """

        _cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:  # to execute sql
            _cursor.callproc(service, params)
            self.conn.commit()
            _result = _cursor.fetchall()
            print(_result)
        except Exception as e:
            raise Exception("ERROR executing service " + service + " " + str(e))


        return _result

    def execute_update(self, service, params):
        """
        Generic service database modification

        Executes a query that modify the database
        INSERT / DELETE / UPDATE or combinations
        of all fo then


        :param fields:
        :return: Nothing
        """

        _cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:  # to execute sql
            _cursor.execute(service, params)
            self.conn.commit()
        except Exception as e:
            raise Exception("ERROR executing service " + service + " " + str(e))


        return True


    def execute(self, command, params):
        """
        Execute a query that returns data

        Generic method to execute query that returns one or more rows

        :param service: The service to be executed
        :param params: The parameters for the service as a dictionary
        :return: A dictionary with results
        """

        # def dict_factory(cursor, row):
        #     d = {}
        #     for idx, col in enumerate(cursor.description):
        #         d[col[0]] = row[idx]
        #     return d



        # self.conn.row_factory = dict_factory

        #_cursor = self.conn.cursor()

        _cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:  # to execute sql
            _cursor.execute(command, params)

            _result = _cursor.fetchall()
            #  dictRows = {n['id']: n for n in _cursor}
            return _result
        except Exception as e:
            print(e.__str__())
            raise e

    def get_query_exec(self, query):

        _cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:  # to execute sql
            _cursor.execute(query,)
            _result = _cursor.fetchall()
            #dictRows = {n['id']: n for n in _cursor}
            self.conn.rollback()
            return _result
        except Exception as e:
            print(e.__str__())
            raise Exception(e)