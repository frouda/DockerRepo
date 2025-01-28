#ΤΟ ΠΡΟΓΡΑΜΜΑ ΡΩΤΑ ΤΟ ΧΡΗΣΤΗ ΠΟΙΟ ΣΥΜΒΟΛΟ ΜΕΤΟΧΗΣ ΕΠΙΘΥΜΕΙ ΝΑ ΑΝΑΖΗΤΗΣΕΙ ΚΑΙ ΕΠΕΞΕΡΓΑΖΕΤΑΙ ΤΑ ΑΝΤΙΣΤΟΙΧΑ ΔΕΔΟΜΕΝΑ
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm

class StockDataProcessor:
    def __init__(self, stock_symbol):
        self.stock_symbol = stock_symbol

        # Get data with the minimum number of records to find the first date
        self.data = yf.download(stock_symbol, period="max", interval="1d")

        # Find first date of the dataset
        first_date = self.data.index.min()

        # Get all data from the beginning
        self.pfizer_data = yf.download(stock_symbol, start=first_date.date())

        # Descriptive
        print(self.pfizer_data.head())
        print(len(self.pfizer_data))
        print(self.pfizer_data.tail())

    def add_daily_percentage_change(self):
        # Add a column named 'Daily' with the calculated percentage variance
        self.pfizer_data['Daily'] = 100 * (
            (self.pfizer_data['Open'] - self.pfizer_data['Close']) / self.pfizer_data['Open']
        )

        # # Save excel
        # output_file = 'C:/Users/Ioanna/Downloads/pfizer_task_new_dataset.xlsx'
        # self.pfizer_data.to_excel(output_file)

    def plot_histogram_with_extremes(self):
        # Ensure the Daily column is added
        if 'Daily' not in self.pfizer_data.columns:
            self.add_daily_percentage_change()

        # Filter out infinite or NaN values
        self.pfizer_data = self.pfizer_data[np.isfinite(self.pfizer_data['Daily'])]

        # Data for plotting
        daily_changes = self.pfizer_data['Daily']

        # Identify extremes
        max_change = daily_changes.max()
        min_change = daily_changes.min()
        max_date = self.pfizer_data.loc[self.pfizer_data['Daily'] == max_change].index[-1]
        min_date = self.pfizer_data.loc[self.pfizer_data['Daily'] == min_change].index[-1]

        # Define bins dynamically
        bins = int((max_change - min_change) / 0.1)

        # Create the histogram
        plt.figure(figsize=(12, 6))
        sns.histplot(daily_changes, bins=bins, kde=False, color='skyblue', edgecolor='black')

        plt.title('Histogram of Daily Percentage Changes', fontsize=16)
        plt.xlabel('Daily Percentage Change (%)', fontsize=14)
        plt.ylabel('Number of Days', fontsize=14)

        # Annotate extremes
        plt.axvline(max_change, color='red', linestyle='--', label=f'Max: {max_change:.2f}% on {max_date.date()}')
        plt.axvline(min_change, color='blue', linestyle='--', label=f'Min: {min_change:.2f}% on {min_date.date()}')

        plt.legend(fontsize=12)
        plt.grid(alpha=0.5)
        plt.show()

    def plot_histogram_with_model(self):
        # Ensure the Daily column is added
        if 'Daily' not in self.pfizer_data.columns:
            self.add_daily_percentage_change()

        # Filter out infinite or NaN values
        self.pfizer_data = self.pfizer_data[np.isfinite(self.pfizer_data['Daily'])]

        # Data for plotting
        daily_changes = self.pfizer_data['Daily']

        # Fit a NORMAL DISTRIBUTION to the data
        mu, std = norm.fit(daily_changes)

        # Create the histogram
        plt.figure(figsize=(12, 6))
        sns.histplot(daily_changes, bins=int((daily_changes.max() - daily_changes.min()) / 0.1),
                     kde=False, color='skyblue', edgecolor='black', stat="density")

        # Plot the fitted normal distribution
        x = np.linspace(daily_changes.min(), daily_changes.max(), 1000)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'r-', label=f'Normal Fit: μ={mu:.2f}, σ={std:.2f}')

        plt.title('Histogram of Daily Percentage Changes with Normal Fit', fontsize=16)
        plt.xlabel('Daily Percentage Change (%)', fontsize=14)
        plt.ylabel('Density', fontsize=14)

        plt.legend(fontsize=12)
        plt.grid(alpha=0.5)
        plt.show()

    def process_and_print(self):
        self.add_daily_percentage_change()
        self.plot_histogram_with_extremes()
        self.plot_histogram_with_model()

if __name__ == '__main__':
    stock_symbol = "PFE"
    data_processor = StockDataProcessor(stock_symbol)
    data_processor.process_and_print()