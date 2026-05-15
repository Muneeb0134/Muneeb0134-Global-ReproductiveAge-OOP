import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from analysis import df


class ReproductiveHealthAnalyzer:
    def __init__(self, repro_path, life_path):
        self.repro_path = repro_path
        self.life_path = life_path
        self.df_final = None

    def load_data(self):
        df = pd.read_csv(self.repro_path)
        df_ = pd.read_csv(self.life_path)
        df_sorted = df_.sort_values('Year', ascending=False)
        mapping = df_sorted.drop_duplicates(subset=['Country'])[['Country', 'Region', 'Life_expectancy']]
        self.df_final = pd.merge(df, mapping, how="left", left_on="Location", right_on="Country")
        print("Data is Loaded and Merge")
        print("\n--- Global Statistical Summary ---")
        print(self.df_final[['First Tooltip', 'Life_expectancy']].describe())
    def clean_data(self):
     self.df_final['Location'] = self.df_final['Location'].str.strip()
     if self.df_final.isnull().values.sum():
             print(f"There are null values in the CSV file. {self.df_final.isnull().sum()}")
             self.df_final['First Tooltip'] = self.df_final['First Tooltip'].fillna(self.df_final['First Tooltip'].mean())
             print("Data loaded")
     else:
            print("There are no null values in the CSV file")
    def perform_analysis(self):
        print(
            f"These Regions have good reproductive Ages. {self.df_final[self.df_final["First Tooltip"] > 75].groupby('Region')['First Tooltip'].count()}")
        print(
            f"The following analysis identifies nations that have achieved a high standard in reproductive healthcare, specifically where over 75% of women's needs for modern family planning methods are satisfied. This metric is a crucial indicator of a country's healthcare accessibility and the effectiveness of its public health policies.\nWhile developed regions often dominate these statistics, our data reveals that several emerging economies in Central and South America are making significant strides, outperforming their peers.\n The success in these regions can often be attributed to integrated community health programs and sustained government investment in maternal services.\n {self.df_final[self.df_final["First Tooltip"] > 75].groupby('Region')['Location'].apply(list)}")
        print(
            f"These Regions have bad reproductive Ages. {self.df_final[self.df_final["First Tooltip"] < 75].groupby('Region')['First Tooltip'].count()}")
        print(
            f"While some regions show progress, a significant portion of the analyzed data highlights a critical gap in reproductive healthcare services across various developing nations.\n In many parts of Africa and Asia, the satisfaction rate for modern family planning remains below 75%, indicating systemic challenges in healthcare delivery, cultural barriers, or limited supply chains.\nThis disparity suggests that economic growth alone is not sufficient to guarantee reproductive autonomy.\nThe data points towards a need for targeted policy interventions and increased international cooperation to bridge this gap.\nAddressing these low-performing regions is essential for achieving global health equity and improving overall life expectancy and maternal well-being.\n{self.df_final[self.df_final["First Tooltip"] < 75].groupby('Region')['Location'].apply(list)}")
    def generate_plot(self):
        sns.histplot(data=self.df_final["First Tooltip"], bins=20, kde=True, color="red")
        plt.xlabel("Family planning satisfaction Rate(%)")
        plt.ylabel("Number of Countries")
        plt.title("Distribution of Reproductive Health Satisfaction")
        plt.show()
        sns.scatterplot(data=self.df_final, x="Life_expectancy", y="First Tooltip", hue='Region', alpha=0.7)
        plt.xlabel("Life Expectancy (years)")
        plt.ylabel("Satisfaction Rate(%)")
        plt.title("Relationship: Life Expectancy vs Family Planning Satisfaction")
        plt.show()
        top_10 = self.df_final.sort_values("First Tooltip", ascending=False).head(10)
        sns.barplot(x = "First Tooltip" , y = "Location" , data = top_10)
        plt.xlabel("Satisfaction Rate(%)")
        plt.ylabel("Countries")
        plt.title("Relationship: First Tooltip vs Countries")
        plt.show()

repro_file = "reproductiveAgeWomen.csv"
life_file = "Life-Expectancy-Data-Updated.csv"


analyzer = ReproductiveHealthAnalyzer(repro_file, life_file)


analyzer.load_data()
analyzer.clean_data()
analyzer.perform_analysis()
analyzer.generate_plot()