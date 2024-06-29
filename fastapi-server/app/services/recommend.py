from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_HOST

es = Elasticsearch([ELASTICSEARCH_HOST])

def recommend_news(user_id: str):
    user_data = es.get(index="users", id=user_id)["_source"]
    interests = user_data["interests"]
    dislikes = user_data["dislikes"]

    query = {
        "bool": {
            "must": [
                {"terms": {"tags": interests}}
            ],
            "must_not": [
                {"terms": {"tags": dislikes}}
            ]
        }
    }

    res = es.search(index="news", body={"query": query})
    recommendations = [hit["_source"] for hit in res["hits"]["hits"]]
    return recommendations

def recommend_popular_news():
    query = {
        "sort": [
            {"views": {"order": "desc"}}
        ],
        "size": 10
    }

    res = es.search(index="news", body={"query": {"match_all": {}}, **query})
    popular_news = [hit["_source"] for hit in res["hits"]["hits"]]
    return popular_news

def recommend_based_on_demographics(gender: str, age_group: str):
    query = {
        "bool": {
            "must": [
                {"term": {"gender": gender}},
                {"term": {"age_group": age_group}}
            ]
        }
    }

    res = es.search(index="news", body={"query": query})
    recommendations = [hit["_source"] for hit in res["hits"]["hits"]]
    return recommendations

def recommend_based_on_new_words():
    query = {
        "aggs": {
            "keywords": {
                "terms": {
                    "field": "content",
                    "size": 10
                }
            }
        }
    }

    res = es.search(index="news", body={"query": {"match_all": {}}, **query})
    keywords = [bucket["key"] for bucket in res["aggregations"]["keywords"]["buckets"]]
    return keywords

def recommend_for_job_seekers():
    query = {
        "bool": {
            "must": [
                {"match": {"content": "job"}},
                {"match": {"content": "interview"}}
            ]
        }
    }

    res = es.search(index="news", body={"query": query})
    recommendations = [hit["_source"] for hit in res["hits"]["hits"]]
    return recommendations
