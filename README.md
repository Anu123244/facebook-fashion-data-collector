# 🛍️ Facebook Fashion Data Collector

A Python-based browser automation project for collecting publicly visible information from Facebook clothing and fashion Pages/Groups. The project focuses on automated data collection, extraction, cleaning, and structured dataset generation.

## 🚀 Features

* Keyword-based Facebook Page/Group URL discovery
* Browser-based data collection using Playwright
* Page-level information extraction
* Public post information extraction
* Public comment-text extraction
* Duplicate URL detection
* Missing-data handling
* Fashion relevance classification
* Access-status detection
* Incremental data processing
* CSV and Excel dataset generation
* No Facebook/Meta Graph API required

## 🛠️ Technologies Used

* Python
* Playwright
* Pandas
* BeautifulSoup
* OpenPyXL
* CSV
* Excel
* Git & GitHub
* VS Code

## 🔄 Methodology

### 1. Keyword-Based URL Discovery

Relevant Facebook clothing and fashion Pages/Groups are identified using predefined search keywords such as:

* Bangladesh clothing
* Bangladesh fashion
* Bangladesh boutique
* Bangladesh saree
* Bangladesh fashion house
* Bangladesh women's clothing
* Bangladesh men's clothing
* Bangladesh online clothing shop
* Bangladesh garments
* Bangladesh fashion store

### 2. Browser-Based Data Collection

Playwright is used to access publicly rendered Facebook content through a normal authenticated browser session.

Facebook/Meta APIs are not used, and login credentials are not stored in the project source code.

### 3. Data Extraction

**Page Data**

* Page name
* Page type
* Category
* Description
* Website
* Followers
* Location
* Address
* Business hours
* Public contact information

**Post Data**

* Post URL
* Post text
* Reactions
* Comment count
* Share count

**Comment Data**

* Publicly visible comment text

### 4. Data Processing

Collected information is cleaned and structured for analysis.

Unavailable information is represented as:

`Not Publicly Listed`

Pages are handled using evidence-based statuses such as:

* `UNVERIFIED_RELEVANT`
* `NEEDS_REVIEW`
* `ACCESS_RESTRICTED`
* `INACCESSIBLE`

The system does not automatically label a page as fake without sufficient evidence.

## 📂 Project Structure

```text
facebook-fashion-data-collector/
│
├── main.py
├── scraper.py
├── extractor.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── Local datasets excluded from GitHub
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd facebook-fashion-data-collector
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Install Chromium for Playwright:

```bash
playwright install chromium
```

## ▶️ Usage

Run the URL discovery process:

```bash
python discover_urls.py
```

Run the main data collection process:

```bash
python main.py
```

> Note: Some local data files and the browser profile are intentionally excluded from the GitHub repository for privacy and security.

## 🔐 Responsible Data Collection

This project is designed around responsible collection of publicly rendered information.

* Facebook/Meta API is not used.
* Login credentials are not stored in source code.
* Private or restricted information is not intentionally accessed.
* CAPTCHA, checkpoint, and security restrictions are not bypassed.
* Personal commenter profile information is not intentionally collected.
* Data availability depends on information publicly rendered by Facebook.
* Collected datasets are kept locally and excluded from the public/private code repository where appropriate.

## 🎯 Project Objective

The objective of this project is to develop a practical automated data-collection pipeline for building a structured dataset of Bangladesh-based clothing and fashion Pages/Groups while applying data cleaning, validation, classification, and responsible data-collection practices.

## 📌 Future Improvements

* Improved URL discovery
* Better Page/Post relationship mapping
* Additional data validation
Automated dataset quality reports
Data visualization and statistical analysis
Machine-learning-based fashion relevance classification
👨‍💻 Author

ANANNYA TITHI
Computer Science & Engineering
American Internation University of-
REPOSITORY_URL : https://github.com/Anu123244/facebook-fashion-data-collector