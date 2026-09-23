from flask import Flask, render_template

app = Flask(__name__)

PROFILE_DATA = {
    "name": "Uttam Prajapati",
    "title": "Python Developer",
    "bio": (
        "Highly skilled Python Web Scraping Developer with 3.5+ years of experience in "
        "designing, developing, and maintaining scalable web scraping solutions. Strong expertise "
        "in data extraction, automation, parsing, and data processing using tools like Scrapy, "
        "Selenium, and Playwright. Experienced in handling dynamic websites, APIs, anti-bot mechanisms, "
        "and large-scale data pipelines. Proven ability to deliver accurate and structured data solutions "
        "to support business intelligence and analytics requirements."
    ),
    "contact": {
        "email": "uttamprajapati3000@gmail.com",
        "phone": "+91-7096991640",
        "location": "Mahesana, Gujarat, India",
        "linkedin": "https://www.linkedin.com/in/uttam-prajapati-682802259/",
        "github": "https://github.com/UttamPgithub"
    },
    "skills": {
        "Languages": ["Python", "SQL"],
        "Web Scraping & Automation": ["Scrapy", "Selenium", "Playwright", "Requests", "BeautifulSoup"],
        "Data Processing": ["Pandas", "NumPy", "hashlib", "ETL Pipelines"],
        "Databases": ["MySQL", "MongoDB"],
        "Tools & Technologies": ["Git", "Linux"]
    },
    "experience": [
        {
            "role": "Python Developer (E1)",
            "company": "Trailytics AI",
            "location": "Gurugram, Haryana, India (Remote)",
            "period": "August 2025 - Present",
            "highlights": [
                "Architected and deployed scalable web scraping solutions processing 500K+ records daily using Python, Scrapy, and Selenium, improving data acquisition efficiency by 40%.",
                "Designed and implemented distributed scraping systems using multi-threading and asynchronous operations, reducing data extraction time by 60% while maintaining 99.5% data accuracy.",
                "Built robust error-handling and retry mechanisms to manage rate limiting, CAPTCHA, and dynamic content, achieving a 95% success rate on complex, anti-bot-protected websites.",
                "Optimized database queries and indexing strategies in MongoDB and MySQL, reducing query execution time by 70% and improving overall system performance."
            ]
        },
        {
            "role": "Python Developer",
            "company": "Xbyte Technolab Pvt. Ltd.",
            "location": "Ahmedabad, Gujarat, India",
            "period": "January 2023 - August 2025",
            "highlights": [
                "Engineered end-to-end ETL pipelines extracting data from 100+ sources, including e-commerce websites, social media platforms, and APIs, processing 2M+ records monthly.",
                "Implemented automated data validation and cleaning workflows using Pandas and NumPy, improving data quality by 85% and reducing manual intervention by 90%.",
                "Developed custom web scraping frameworks to handle JavaScript-heavy SPAs using Playwright and Selenium, successfully bypassing advanced anti-scraping mechanisms.",
                "Collaborated with cross-functional teams to translate business requirements into technical specifications, delivering 15+ data extraction projects on time and within budget.",
                "Monitored and optimized scraper performance, improving execution speed, reducing server load, and ensuring consistent data delivery."
            ]
        }
    ],
    "project_domains": [
        "E-commerce",
        "Healthcare",
        "News & Articles",
        "Restaurant",
        "Automotive Websites",
        "Travel & Hotel Booking"
    ],
    "education": {
        "degree": "Master of Computer Applications (MCA) - Computer Science",
        "institution": "Sankalchand Patel University, Visnagar, Gujarat, India",
        "period": "June 2022 - April 2024",
        "coursework": "Data Structures & Algorithms, Database Management Systems, Operating Systems, Computer Networks, Distributed Systems, Cloud Computing."
    }
}

@app.route("/")
def home():
    return render_template("index.html", profile=PROFILE_DATA)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)