import redis
import json
import re
from redis_lru import RedisLRU
from models import Quote, Author


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def search_by_author(name: str) -> list[str]:
    pattern = re.compile(f".*{name}.*", re.IGNORECASE)
    authors = Author.objects(fullname__icontains=name)
    if not authors:
        authors = Author.objects(__raw__={"fullname": {"$regex": pattern}})
    quotes = Quote.objects(author__in=authors)
    result = [quote.quote for quote in quotes]
    return result


def search_by_tag(tag: str) -> list[str]:
    pattern = re.compile(f".*{tag}.*", re.IGNORECASE)
    quotes = Quote.objects(tags__icontains=tag)
    if not quotes:
        quotes = Quote.objects(__raw__={"tags": {"$regex": pattern}})
    result = [quote.quote for quote in quotes]
    return result


@cache
def cached_search_by_author(name: str) -> list[str]:
    return search_by_author(name)


@cache
def cached_search_by_tag(tag: str) -> list[str]:
    return search_by_tag(tag)


if __name__ == "__main__":
    while True:
        user_input: str = input("Enter command: ")
        if user_input.startswith("name:"):
            name: str = user_input.split(":", 1)[1].strip()
            results: list[str] = cached_search_by_author(name)
            print(json.dumps(results, ensure_ascii=False))
        elif user_input.startswith("tag:"):
            tag: str = user_input.split(":", 1)[1].strip()
            results: list[str] = cached_search_by_tag(tag)
            print(json.dumps(results, ensure_ascii=False))
        elif user_input.startswith("tags:"):
            tags: list[str] = user_input.split(":", 1)[1].strip().split(",")
            results: list[str] = []
            for tag in tags:
                results.extend(cached_search_by_tag(tag))
            print(json.dumps(results, ensure_ascii=False))
        elif user_input == "exit":
            break
