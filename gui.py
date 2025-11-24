import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


class SalesReportGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Sales Report Generator")
        self.setGeometry(200, 200, 500, 300)
        self._init_()

    def _init_(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select Data Folder Containing CSV Files:")
        layout.addWidget(self.label)

        self.path_input = QLineEdit()
        layout.addWidget(self.path_input)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse_folder)
        layout.addWidget(browse_btn)

        generate_btn = QPushButton("Generate")
        generate_btn.clicked.connect(self._generate_reports)
        layout.addWidget(generate_btn)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_input.setText(folder)

    def _generate_reports(self):
        folder = self.path_input.text().strip()
        if not folder:
            self.status.setText("Please select a folder.")
            return

        files = glob.glob(os.path.join(folder, "*.csv"))

        df_list = [pd.read_csv(f) for f in files]
        df = pd.concat(df_list, ignore_index=True)

        df.columns = df.columns.str.strip().str.lower()
        if "date" not in df.columns or "quantity" not in df.columns:
            self.status.setText("Missing required columns: date, quantity")
            return

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.drop_duplicates()
        df = df.dropna(subset=["date", "quantity"])

        cleaned_path = os.path.join(folder, "clean_sales.csv")
        df.to_csv(cleaned_path, index= False)

        summary = df.groupby(df["date"].dt.month)["quantity"].sum()
        summary.to_csv(os.path.join(folder, "sales_summary.csv"))

        product_summary = df.groupby("product")["quantity"].sum()
        product_summary.to_csv(os.path.join(folder, "product_summary.csv"))

        plt.figure(figsize=(10,5))
        summary.plot(kind="line")
        plt.title("Monthly Sales overview")
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.grid(True)
        plt.savefig(os.path.join(folder, "sales_chart.png"))

        plt.figure(figsize=(8,5))
        product_summary.plot(kind="bar")
        plt.title("Sales by Product")
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.tight_layout()
        plt.savefig(os.path.join(folder, "sales_by_product.png"))
        plt.close()

        self.status.setText("Sales report generated successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SalesReportGui()
    gui.show()
    sys.exit(app.exec_())





