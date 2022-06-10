from bs4 import BeautifulSoup
from app import parameters
from app.models.opinion import opinion
from app.uttils import get_item
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import json 
import os

class Product():
    def __init__(product_id, stats, opinions):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score

        def opinion_to_df(self):
            return pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))

        def calculate_stats(self):
            opinions = self.opinions_to_df()
            opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",",".")))
            self.opinions_count: len(opinions)
            self.pros_count: opinions["pros"].map(bool).sum()
            self.cons_count: opinions["cons"].map(bool).sum()
            self.average_score: opinions["stars"].mean().round(2)

            return self

        def draw_chart(self):
            if not os.path.exists("app/opinions"):
                    os.makedirs("app/opinions")
            recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
            recommendation.plot.pie(
                label="",
                autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
                colors = ["crimson", "forestgreen", "lightskyblue"],
                labels = ["Polecam", "Nie polecam","Nie mam zdania"]
            )
            plt.title("Rekomendacje")
            plt.savefig(f"app/plots/{item_id}_recommendations.png")
            plt.close()
            stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
            stars.plot.bar(
                color = "pink"
            )
            plt.xlabel("Liczba gwiazdek")
            plt.ylabel("Liczba opinii")
            plt.grid(True, axis="y")
            plt.xticks(rotation=0)
            plt.savefig(f"app/plots/{product_id}_stars.png")
            plt.close()

        def extract_name():
            url = "https://www.ceneo.pl/" + product_id + "#tab=reviews"
            response = requests.get(url)
            page = BeautifulSoup(response.text,"html.parser")
            self.product_name = get_item()
            product-top__product-info__name
            return self

        def extract_opinions(self):
            url = "https://www.ceneo.pl/" + product_id + "#tab=reviews"
            while(url):
                response = requests.get(url)
                page = BeautifulSoup(response.text,"html.parser")
                opinions = page.select("div.js_product-review")
                for opinion in opinions:

                    single_opinion = Opinion().extract_opinion(opinion)
                    self_opinions.append(single_opinion)
                try:
                    url = "https://www.ceneo.pl/"+get_item(page,"a.pagination__next","href")
                except TypeError:
                    url = None
            return self

    def __str__(self) -> str:
        pass
    def __repr__(self) -> str:
        pass
    def to_dict(self) -> dict:
        pass

    def export_opinions(self):
        if not os.path.exists("app/opinions"):
            os.makedirs("app/opinions")
        
    def export_product(self):
        pass