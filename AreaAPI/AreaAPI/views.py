
from rest_framework.views import APIView
from rest_framework.response import Response

from Libs.DataServicesPGSQL2 import DBServices
import json


class AreasView(APIView):

    def get(self, request, *args, **kwargs):

        print("request ---> ", request.data)
        _sql = """SELECT A.id, P.id As Provider_id, P.name as Provider, A.area_name, A.area_price, 
                    ST_AsGeoJSON(A.polygon) 
                 FROM public."area" as A, public."APIapp_provider" as P
                 WHERE 1 = 1"""
        if 'point' in request.data:
            _geo_json = '{"type":"Point", '
            _geo_json += f'"coordinates":{request.data["point"]}, '
            _geo_json += '"crs":{"type":"name","properties":{"name":"EPSG:4326"}}}'
            _sql += f" AND ST_Contains(polygon, ST_TRANSFORM(ST_GeomFromGeoJSON('{_geo_json}'),4326)) "
        if 'provider_id' in request.data:
            _sql += f" AND provider_id = {request.data['provider_id']}"

        _sql += " AND A.provider_id = P.id; "

        print(_sql)

        _ds = DBServices('geo.ini')

        _result = _ds.get_query_exec(_sql)
        _response = json.dumps(_result)

        return Response(json.loads(_response))

    def post(self, request, *args, **kwargs):

        _area = request.data['area']
        _area_name = request.data['area_name']
        _price = request.data['price']
        _provider_id = request.data['provider_id']

        _sql = f""" INSERT INTO area (provider_id, area_name, area_price, polygon)
                            VALUES ({_provider_id},
                                    '{_area_name}',
                                    {_price},
                                    ST_TRANSFORM(ST_GeomFromGeoJSON(
                                                    '{_area}'
                                                    ),4326));
                            """

        _ds = DBServices('geo.ini')
        _result = _ds.execute_update(_sql, [])

        _response = {"area" : _area, "area_name" : _area_name, "price" : _price, "provider_id" : _provider_id}

        return Response(f"Area {_area_name} added")

    def put(self, request, *args, **kwargs):

        _area_id = request.data['area_id']
        _area = request.data['area']
        _area_name = request.data['area_name']
        _price = request.data['price']
        _provider_id = request.data['provider_id']

        _sql = f"""
        UPDATE public."area"
        SET provider_id={_provider_id},
	    area_name = '{_area_name}',
	    area_price = {_price},
	    polygon =  ST_TRANSFORM(ST_GeomFromGeoJSON(
                                            '{_area}'
                      ),4326)
        WHERE id = {_area_id}
        """

        _ds = DBServices('geo.ini')
        _result = _ds.execute_update(_sql, [])

        return Response(f"Area {_area_id} updated")

    def delete(self, request, *args, **kwargs):

        _area_id = request.data['area_id']
        _sql = f'DELETE FROM public."area" WHERE id = {_area_id}'

        _ds = DBServices('geo.ini')
        _result = _ds.execute_update(_sql, [])

        return Response(f"Area {_area_id} deleted")

