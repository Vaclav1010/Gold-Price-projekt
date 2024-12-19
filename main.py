from bs4 import BeautifulSoup
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Stáhnutí a parsování stránky
url = "https://www.kurzy.cz/komodity/zlato-graf-vyvoje-ceny/historie"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extrakce dat
roky = [row.get_text() for row in soup.select("tr td a") if row.get_text().isnumeric()]
ceny = [td.get_text().replace("\xa0", "").replace(",", ".") for td in soup.select("td.r.bold")]

# Extrakce průměrných cen (každý třetí prvek)
prumerne_ceny = ceny[2::3]

# Převod na DataFrame
df = pd.DataFrame({"Rok": list(map(int, roky)), "PrumernaCenaZlata": list(map(float, prumerne_ceny))})

# Seřazení podle roku
df = df.sort_values(by="Rok")

# Vytvoření grafu pomocí Seaborn
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="Rok", y="PrumernaCenaZlata", marker="o", color="gold", label="Průměrná cena zlata")

# Přizpůsobení grafu
plt.title("Vývoj průměrné ceny zlata (2005–2024)", fontsize=16, weight="bold")
plt.xlabel("Rok", fontsize=12)
plt.ylabel("Průměrná cena zlata (USD)", fontsize=12)
plt.xticks(df["Rok"], rotation=45)
plt.legend(title="Legenda", loc="upper left")
plt.tight_layout()

# Zobrazení grafu
plt.show()