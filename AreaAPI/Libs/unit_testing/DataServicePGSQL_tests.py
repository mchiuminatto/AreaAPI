from Libs.TestBase import TestBase
from Libs.DataServicesPGSQL2 import DBServices

import json

class Tests(TestBase):

    def test_case_0(self):
        """
        Test connection through a simple query
        """
        _ds = DBServices("./geo_test.ini")
        qry = """SELECT id, name, email, phone, language, currency 
                FROM public."APIapp_provider"; 
              """
        _result  = _ds.get_query_exec(qry)
        print(_result)

        _j_result = json.dumps(_result)
        print(_j_result)


    def test_case_1(self):
        """
        Insert an area in the area table (POST)

        """
        _geo_json = '''{
                        "type":"Polygon",
                        "coordinates":[[
                            [-34.886621568455034, -54.93596792941215],
                            [-34.892890893424536, -54.96703299841725],
                            [-34.912202299332165, -54.95320059945277],
                            [-34.89926205617112, -54.93014125313999],
                            [-34.886621568455034, -54.93596792941215]
                        ]],
                        "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
                        }'''

        _area_name = "Maldonado Centro (Uruguay)"
        _provider_id = 1
        _price = 100000.00

        _sql =      f""" INSERT INTO area (provider_id, area_name, area_price, polygon)
                    VALUES ({_provider_id},
                            '{_area_name}',
                            {_price},
                            ST_TRANSFORM(ST_GeomFromGeoJSON(
                                            '{ _geo_json}'
                                            ),4326));
                    """

        print(_sql)

        _ds = DBServices('./geo_test.ini')
        _result = _ds.execute_update(_sql, [])

    def test_case_2(self):
        """
        Get areas that contain a point

        """
        _geo_json = '''{
                        "type":"Polygon",
                        "coordinates":[[
                            [-34.886621568455034, -54.93596792941215],
                            [-34.892890893424536, -54.96703299841725],
                            [-34.912202299332165, -54.95320059945277],
                            [-34.89926205617112, -54.93014125313999],
                            [-34.886621568455034, -54.93596792941215]
                        ]],
                        "crs":{"type":"name","properties":{"name":"EPSG:4326"}}
                        }'''

        _area_name = "Maldonado Centro (Uruguay)"
        _provider_id = 1
        _price = 100000.00

        _sql =      f""" INSERT INTO area (provider_id, area_name, area_price, polygon)
                    VALUES ({_provider_id},
                            '{_area_name}',
                            {_price},
                            ST_TRANSFORM(ST_GeomFromGeoJSON(
                                            '{ _geo_json}'
                                            ),4326));
                    """


        _ds = DBServices('./geo_test.ini')
        _result = _ds.execute_update(_sql, [])

    def test_case_3(self):
        """select areas containing one point"""
        _point = [-34.898367277145404, -54.949073254346146]

        _geo_json = '{"type":"Point", '
        _geo_json += f'"coordinates":{_point}, '
        _geo_json += '"crs":{"type":"name","properties":{"name":"EPSG:4326"}}}'


        _sql = f"""
                    SELECT P.name as Provider, A.area_name, A.area_price 
                    FROM public."area" as A, public."APIapp_provider" as P
                    WHERE 1 = 1
                    AND ST_Contains(polygon, ST_TRANSFORM(ST_GeomFromGeoJSON('{_geo_json}'),4326))
                    AND A.provider_id = P.id; """

        _ds = DBServices('./geo_test.ini')
        _result = _ds.get_query_exec(_sql)
        print(json.dumps(_result))

    def test_case_4(self):
        """
        delete area
        """

        _area_id = 19
        _sql = f"DELETE FROM area WHERE id = {_area_id}"

        _ds = DBServices('./geo_test.ini')
        _result = _ds.execute_update(_sql, [])



if __name__ == "__main__":
    _test = Tests()
    _test.run([1])