# Movie Ticket Availability Alert System  

## Overview  
This Python script continuously monitors movie ticket availability in preferred theaters and sends real-time alerts when tickets are released. It utilizes **Selenium** for web scraping and runs on **AWS EC2** to ensure uninterrupted execution. Notifications are sent via **Telegram bot**, providing instant updates on ticket availability.  

## Features  
- Tracks movie ticket availability in **desired theaters** based on user preferences.  
- Uses **Selenium** to scrape real-time data from the Paytm movie booking website.  
- Runs **continuously on AWS EC2**, ensuring round-the-clock monitoring.  
- Sends **Telegram notifications** for instant alerts when tickets become available.  
- Compares **previous and current show listings** to detect updates dynamically.  

## Prerequisites  
- **Python 3.x**  
- **Selenium WebDriver**  
- **Google Chrome** and **ChromeDriver**  
- **AWS EC2 instance** (for continuous execution)  
- **Telegram bot API** for notifications  

## Alerts & Notifications  
- The script sends **Telegram alerts** when new tickets are released.  
- It **tracks changes** in availability and **logs updates** dynamically.  

## Future Enhancements  
- Add **support for multiple booking platforms**.  
- Improve **real-time processing speed** with optimized scraping techniques.  
- Implement **SMS alerts** for additional notification options.  
