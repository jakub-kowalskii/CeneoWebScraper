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
        return f"{self.opinion_id}, {self.author}, {self.recommendation}, {self.stars}, {self.content}, {self.useful}, {self.useless},{self.published}, {self.purchased}, {self.pros}, {self.cons}"

    def __repr__(self) -> str:
        return self.__str__

    def to_dict(self) -> dict:
        return {
            "opinion_id": self.opinion_id,
            "author": self.author,
            "recommendation": self.recommendation,
            "stars": self.stars,
            "content": self.content,
            "useful": self.useful,
            "useless": self.useless,
            "published": self.published,
            "purchased": self.purchased,
            "pros": self.pros,
            "cons": self.cons
        }