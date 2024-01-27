
# <center>Wikipedia_webCrawler_game</center>

### <center> A simple Wikipedia web Crawler </center> 
---

# <center> HOW TO SET IT UP </center>
:warning:  you MUST have BeautifulSoup4 intalled in order to run the code. requirements.txt will be available once the project is in satisfactory conditions :warning:
<center> To install execute the following code in Python Terminal
</center>

```python
pip install beautifulsoup4
```

1. Clone the GitHub repo:
```https://github.com/ErvinGrimaldi03/Wikipedia_webCrawler_game.git```

---

#### <center> what is this?</center>
This software is a simple Wikipedia web crawler. It starts from any valid wikipedia webpage, and it start exploring wikipedia. It selects 5 random wikiPages (valid Wikipedia articles) and explore the website.

---

#### <center> How is made? </center>
The software is entirely written in python 3. The main libraries used in the software are Beautifulsoup4, requests, re, and random. Beautifulsoup is used for the data retrieval of the pages, re is used to filter valid wikiPages throguh REGULAR EXPRESSIONS, requests to make a connection between user and server, and random to select the next wikiPage to visit. The software will retrieve the HTML of the current page and will produce a list of valid Wikipedia links. The list is later used to choose a random new link and repeat the process recursively until a stop criterion is met. Future updates might include new libraries and functionalities

---

#### <center> Can I just download the dataset without running the program? </center>
Not at the moment! 
unfortunately, the dataset is not ready yet. As soon it will be available I will work out a way to permit downoald of the dataset I gained.

---

#### <center> Who can use it? </cennter>
Most of the time, the answer is YES. however, if you are unsure about this type of matter, I would recommend to simply contact me in private.
This is an Open-Source-Software and everyone is free to use. If you'd like to use it, I'd love to hear about it. Feel free to shoot me an email about it. 


---

#### <center> Why this? </center>
While web crawling is not a complicated task, handling and storing massive data is. My intention is to map out Wikipedia and generate a graph map of every wikiPage article. This is no easy task, as today (01/26/2024), there are over 6.7 milion articles[^fn1].
The hardest task is to have an efficient graph search and visualization  The current python side of the project is mostly to mine the data needed, while the user interface has to be thought of.
My learning objectives are: efficient webcrawling, multithreading/multiprocessing, very large data visualization, very large database managment, data analytics.





[^fn1]: Wikimedia Foundation. (2024, January 20). Size of wikipedia. Wikipedia. https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia#:~:text=As%20of%2026%20January%202024,number%20of%20pages%20is%2059%2C868%2C987. 




