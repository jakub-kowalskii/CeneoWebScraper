import requests
from app.utils import get_item

class Opinion():
    def __init__(self, opinion_id, author, recommendation, stars, content,
    useful, useless, published, purchased, pros, cons):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content 
        self.useful = useful
        self.useless = useless
        self.published = published
        self.purchased = purchased
        self.pros = pros 
        self.cons = cons
        return self

    def extract_opinion(self):
        for key, value in selector.items():
            setattr(self, key, get_item(opinion, *value))
            self.opinion_id = opinion["data-entry-id"]
            return self

    def __str__(self) -> str:
        pass
    def __repr__(self) -> str:
        pass
    def to_dict(self) -> dict:
        pass