import json
from math import ceil

from bson import ObjectId
from logzero import logger
from pymongo import MongoClient

import settings
from app.utils.format_encoder_object import format_encoder_object
from app.utils.singleton import Singleton


class MongoDB(object):
    def __init__(self):
        _config = settings.load_config()
        self.host = _config.MONGO_HOST
        self.port = _config.MONGO_PORT
        self.database = _config.MONGO_DATABASE
        self.username = _config.MONGO_USERNAME
        self.password = _config.MONGO_PASSWORD
        self.connect_timeout = _config.MONGO_CONNECT_TIMEOUT
        self.conn = self.get_instance

    def __del__(self):
        self.close_connection()

    @property
    def connection_database(self) -> MongoClient:
        return MongoClient(
            host=self.host,
            username=self.username,
            password=self.password,
            port=self.port,
            authSource="admin",
            authMechanism="SCRAM-SHA-1",
            connectTimeoutMS=self.connect_timeout,
            serverSelectionTimeoutMS=self.connect_timeout,
        )

    @property
    def get_instance(self):
        rw = Singleton()
        rw.conn = self.connection_database
        return rw.conn

    def close_connection(self):
        self.conn.close()

    def test_ping(self):
        try:
            x = self.conn[self.database].command("ping")
            return x.get("ok", "")
        except Exception as ex:
            logger.error(f"Error testing MongoDB ping. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def check_exists_collection(self, collection):
        try:
            db = self.conn[self.database]
            return db[collection]
        except Exception as ex:
            logger.error(
                f"Error checking if collection exists in MongoDB. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    def drop_collection(self, collection):
        try:
            db = self.conn[self.database]
            db[collection].drop()
        except Exception as ex:
            logger.error(f"Failed to delete MongoDB collection. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def save_one(self, obj: dict, collection: str, **kwargs) -> str:
        try:
            db = self.conn[self.database]

            objectid = kwargs.get("objectid", None)
            if objectid and ObjectId.is_valid(objectid):
                obj["_id"] = ObjectId(objectid)

            x = db[collection].insert_one(obj)
            return x.inserted_id
        except Exception as ex:
            logger.error(f"Failed to save data in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def save_list(self, obj_list: list, collection: str) -> list:
        try:
            db = self.conn[self.database]
            x = db[collection].insert_many(obj_list)
            return x.inserted_ids
        except Exception as ex:
            logger.error(
                f"Failed to save the data list in MongoDB. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    def update_one(
            self, collection: str, query: dict, obj: dict, upsert=False
    ) -> object:
        try:
            db = self.conn[self.database]
            x = db[collection].update_one(filter=query, update=obj, upsert=upsert)
            return x
        except Exception as ex:
            logger.error(f"Failed to update item in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def update_all(
            self, collection: str, query: dict, obj: dict, upsert=False
    ) -> object:
        try:
            db = self.conn[self.database]
            x = db[collection].update_many(query, obj, upsert=upsert)
            return x
        except Exception as ex:
            logger.error(f"Failed to update items in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def delete_one(self, collection: str, query: dict) -> object:
        try:
            db = self.conn[self.database]
            x = db[collection].delete_one(query)
            return x
        except Exception as ex:
            logger.error(f"Failed to delete the data in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def find_all(self, collection: str, query: dict = None, **kwargs) -> list:
        try:
            sort_key = kwargs.get("sort_key", "_id")
            sort_order = int(kwargs.get("sort_order", 1))

            if query is None:
                query = {}

            db = self.conn[self.database]

            x = (
                db[collection]
                    .find(query, kwargs.get("select", None))
                    .sort(sort_key, sort_order)
            )
            return list(x)
        except Exception as ex:
            logger.error(f"Failed to fetch data in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def find_one(self, collection: str, query: dict, **kwargs) -> dict:
        try:
            db = self.conn[self.database]
            x = db[collection].find_one(query, kwargs.get("select", None))
            return x
        except Exception as ex:
            logger.error(f"Failed to fetch data in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def find_all_pagination(
            self, collection: str, query: dict, fields: dict = None, **kwargs
    ) -> dict:
        try:
            db = self.conn[self.database]
            params = self._get_params_pagination(**kwargs)

            cursor = db[collection].find(query, fields)
            data = (
                cursor.sort(params.get("sort_key"), params.get("sort_asc_desc"))
                    .skip(params.get("skip"))
                    .limit(params.get("limit"))
            )
            data = list(data)
            total = cursor.count()

            return self._format_return_pagination(params, total, data)
        except Exception as ex:
            logger.error(
                f"Failed to fetch data from pages in MongoDB. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    def aggregate(self, collection: str, query: list):
        try:
            db = self.conn[self.database]
            return db[collection].aggregate(query)
        except Exception as ex:
            logger.error(
                f"Failed to fetch aggregate data in MongoDB. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    def count(self, collection, query):
        try:
            db = self.conn[self.database]
            return db[collection].count_documents(query)
        except Exception as ex:
            logger.error(f"Failed to count data in MongoDB. ERROR ---> {str(ex)}")
            raise Exception(ex)

    def aggregate_pagination(self, collection: str, **kwargs):
        try:
            db = self.conn[self.database]
            params = self._get_params_pagination(**kwargs)
            query = []

            self._set_add_filds_in_aggregation(query, kwargs)

            self._set_project_in_aggregation(query, kwargs)

            self._set_query_and_in_aggregation(query, kwargs)

            query.append(
                {
                    "$facet": {
                        "metadata": [{"$count": params.get("column_count")}],
                        "results": [
                            {
                                "$sort": {
                                    params.get("sort_key"): params.get("sort_asc_desc")
                                }
                            },
                            {"$skip": params.get("skip")},
                            {"$limit": params.get("limit")},
                        ],
                    }
                }
            )

            data = list(db[collection].aggregate(query))[0]

            total = 0
            if data.get("metadata", []):
                total = data.get("metadata")[0].get(params.get("column_count"), 0)

            return self._format_return_pagination(
                params, total, data.get("results", [])
            )
        except Exception as ex:
            logger.error(
                f"Failed to fetch aggregated data with page in MongoDB. ERROR ---> {str(ex)}"
            )
            raise Exception(ex)

    @staticmethod
    def _get_params_pagination(**kwargs) -> dict:
        args = {}

        sort_asc_desc = kwargs.get("sort_asc_desc", "desc")
        if sort_asc_desc == "desc":
            args["sort_asc_desc"] = -1
        else:
            args["sort_asc_desc"] = 1

        args["limit"] = 10
        if kwargs.get("limit", None) is not None:
            args["limit"] = int(kwargs.get("limit", 10))

        args["page"] = 1
        if kwargs.get("page", None) is not None:
            args["page"] = int(kwargs.get("page", 1))

        args["column_count"] = str(kwargs.get("column_count", "_id"))
        args["sort_key"] = str(kwargs.get("sort_key", "_id"))
        args["skip"] = int(args["limit"]) * (int(args["page"]) - 1)

        return args

    @staticmethod
    def _format_return_pagination(params: dict, total: int, results: list) -> dict:
        return {
            "results": json.loads(json.dumps(results, default=format_encoder_object)),
            "page": params.get("page"),
            "limit": params.get("limit"),
            "totalResults": total,
            "totalPages": ceil(total / params.get("limit")),
        }

    @staticmethod
    def _set_project_in_aggregation(query: list, kwargs: dict):
        if kwargs.get("project", []):
            query.append({"$project": kwargs.get("project")})

    @staticmethod
    def _set_query_and_in_aggregation(query: list, kwargs: dict):
        if kwargs.get("query_and", []):
            query.append({"$match": {"$and": kwargs.get("query_and", [])}})

    @staticmethod
    def _set_add_filds_in_aggregation(query, kwargs):
        if kwargs.get("add_fields", {}):
            query.append({"$addFields": kwargs.get("add_fields")})
