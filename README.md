# Kumon Math Learning App

A Streamlit web application that uses the Kumon methodology to teach kids addition and multiplication. Built for KS2 students, the app features progressive difficulty levels, practice mode, and Kumon-style worksheets.

## Features

- **Two subjects**: Addition and Multiplication, each with 10 progressive levels
- **Practice mode**: Solve one problem at a time with instant feedback and streak tracking
- **Worksheet mode**: Complete batches of 5-20 problems, scored at the end like a real Kumon worksheet
- **Kumon methodology**: Mastery-based progression — achieve 90%+ accuracy before advancing
- **Progress tracking**: Accuracy, problems solved, and best streak displayed in the sidebar

### Addition Levels

| Level | Focus | Description |
|-------|-------|-------------|
| 1 | +1 facts | Adding 1 to small numbers |
| 2 | +2 facts | Adding 2 to numbers up to 8 |
| 3 | +3 facts | Adding 3 to numbers up to 10 |
| 4 | Small sums | Both numbers 1-5 |
| 5 | Sums to 10 | Any single digits |
| 6 | +10s | Adding multiples of 10 |
| 7 | 2-digit + 1-digit | Two-digit plus one-digit |
| 8 | No carrying | Two-digit addition without carrying |
| 9 | 2-digit + 2-digit | Any two-digit addition |
| 10 | 3-digit + 2-digit | Three-digit plus two-digit |

### Multiplication Levels

| Level | Focus | Description |
|-------|-------|-------------|
| 1-7 | Individual tables | x1 through x7, one table per level |
| 8 | x8 & x9 | Times-8 and times-9 tables |
| 9 | Mixed facts | All times tables mixed |
| 10 | Extended | Up to 12x12 |

## Getting Started

### Prerequisites

- Python 3.6 or later

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Yasser03/ks2_time_table.git
   cd ks2_time_table
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## License

This project is licensed under the MIT License.
