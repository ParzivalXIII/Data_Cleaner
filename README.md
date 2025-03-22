# 🧹 Data Cleaning and Visualization Tool

A powerful and user-friendly Python tool for cleaning and visualizing CSV datasets — available via **command-line** and a **Streamlit-based web interface**.

---

👉 [Launch the Web App](https://parzivalxiii-data-cleaner.streamlit.app)  
*(No installation needed — runs in your browser)*

## ✨ Features

- 🧼 **Data Cleaning**:
  - Handle missing values intelligently
  - Remove duplicate rows
  - Convert column data types (object → numeric, datetime, categorical)

- 📊 **Smart Data Visualization**:
  - Detects column type and selects best chart (Bar, Histogram, Pie)
  - Set Seaborn styles, figure size, bin count, and plot title
  - View stats (mean, median, std dev) for numeric plots
  - Download cleaned CSV or plot PNG

- 🖥️ **Two Ways to Use**:
  - Command-line interface (CLI)
  - Web-based interface (Streamlit)

---

## 📦 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/ParzivalXIII/Data_Cleaner.git
   
   cd Data_cleaner
   ```

## 🚀 Usage
1. **Web Interface (Recommended)**
   ```bash
   streamlit run app.py
   ```
   * Upload any ```.csv``` file
   * Toggle cleaning options
   * Select column for visualization
   * Select chart type

2. **command-Line Interface**
   ```bash
   python main.py data.csv --all --plot-column purchase_count --sns-style whitegrid
   ```
   **CLI Options:**
   | Argument             | Description                                 |
|----------------------|---------------------------------------------|
| `--handle-missing`   | Fill missing values                         |
| `--remove-duplicates`| Remove duplicate rows                       |
| `--convert-types`    | Optimize data types                         |
| `--all`              | Apply all cleaning steps                    |
| `--plot-column`      | Column name to visualize                    |
| `--sns-style`        | Seaborn style (`darkgrid`, `whitegrid`, etc)|
| `--figsize`          | Figure size, e.g., `10,6`                   |
| `--title`            | Custom plot title                           |
| `--bins`             | Histogram bins for numeric columns         |

## 📁 Project Structure
```bash
.
├── data_cleaner.py        # Cleaning functions
├── data_visualizer.py     # Visualization functions
├── main.py                # CLI entry point
├── app.py                 # Streamlit web UI
├── requirements.txt
└── README.md
```

## 🛠️ Dependencies
* pandas
* numpy
* seaborn
* matplotlib
* streamlit

Install with:
```bash
pip install -r requirements.txt
```

## 📜 License
MIT License

## 💡 Author
[ParzivalXIII](https://github.com/ParzivalXIII)
