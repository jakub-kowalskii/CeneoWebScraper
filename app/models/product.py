from bs4 import BeautifulSoup
from app import parameters
from app.models.opinion import Opinion
from app.utils import get_item
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import json 
import os
import requests
from flask import render_template, redirect, url_for, request

class Product():
    def __init__(self, product_id=0, product_name="", opinions=[], opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score

    def opinions_do_df(self):
        opinions = pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))
        opinions.stars = opinions.stars.map(lambda x: float(x.split("/")[0].replace(",", ".")))
        return opinions

    def calculate_stats(self):
        opinions = self.opinions_to_df()
        opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",",".")))
        self.opinions_count: len(opinions)
        self.pros_count: opinions["pros"].map(bool).sum()
        self.cons_count: opinions["cons"].map(bool).sum()
        self.average_score: opinions["stars"].mean().round(2)
        return self

    def draw_charts(self): 
        recommendation = self.opinions_do_df().recommendation.value_counts(dropna = False).sort_index().reindex(["Nie polecam", "Polecam", None])
        recommendation.plot.pie(
            label="", 
            autopct="%1.1f%%", 
            colors=["crimson", "forestgreen", "lightskyblue"],
            labels=["Nie polecam", "Polecam", "Nie mam zdania"]
        )
        plt.title("Rekomendacja")
        plt.savefig(f"app/static/plots/{self.product_id}_recommendations.png")
        plt.close()
        stars = self.opinions_do_df().stars.value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar()
        plt.title("Oceny produktu")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True)
        plt.xticks(rotation=0)
        plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
        plt.close()

    def extract_name(self):
        url = "https://www.ceneo.pl/" + self.product_id + "#tab=reviews"
        response = requests.get(url)
        page = BeautifulSoup(response.text,"html.parser")
        self.product_name = get_item(page, "h1.product-top__product-info__name")
        
        
    def extract_opinions(self):
        url = "https://www.ceneo.pl/" + self.product_id + "#tab=reviews"
        while(url):
            response = requests.get(url)
            page = BeautifulSoup(response.text,"html.parser")
            opinions = page.select("div.js_product-review")
            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            try:
                url = "https://www.ceneo.pl/"+get_item(page,"a.pagination__next","href")
            except TypeError:
                url = None
        return self

    def __str__(self) -> str:
        return f'product id: {self.product_id} <br> product name: {self.procuct_name} <br> opinions <br>' + '<br>'.join(str(opinion) for opinion in self.opinions)

    def __repr__(self) -> str:
        return f"Product(product_id={self.product_id}, product_name={product_name}, opinions+["+",".join(opinion.__repr__() for opinion in self.opinions) +"])"

    def to_dict(self) -> dict:
        return{
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }

    def export_opinions(self):
        if not os.path.exists("app/opinions"):
            os.makedirs("app/opinions")
        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as file:
            json.dump([opinion.to_dict for opinion in self.opinions()], file, indent=4, ensure_ascii=False)
        
    def export_product(self):
        if not os.path.exists("app/products"):
            os.makedirs("app/products")
        with open(f"app/products/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump(self.stats_to_dict(), jf, indent=4, ensure_ascii=False)
        

    def stats_to_dict(self):
        pass

    def import_product(self):
        if not os.path.exists(f"app/products/{self.product_id}.json"):
            with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as jf:
                product = json.load(jf)
            self.product_id = product["product_id"]
            self.product_name = product["product_name"]
            self.opinions_count = product["opinions_count"]
            self.pros_count = product["pros_count"]
            self.cons_count = product["cons_count"]
            self.average_score = product["average_score"]
        with open(f"app/opinions/{self.product_id}.json", "r", encoding="UTF-8") as jf:
            opinions = json.load(jf)
        for opinion in opinions:
            self.opinions.append(Opinion(**opinion))