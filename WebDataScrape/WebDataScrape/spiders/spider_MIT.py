import scrapy
from WebDataScrape.items import WebdatascrapeItem

class SpiderMitSpider(scrapy.Spider):
    name = 'spider_MIT'
    # allowed_domains = ['example.com']
    start_urls = ['https://ocw.mit.edu/courses/6-780-semiconductor-manufacturing-spring-2003/', 'https://ocw.mit.edu/courses/6-824-distributed-computer-systems-engineering-spring-2006/', 'https://ocw.mit.edu/courses/6-5830-database-systems-fall-2023/', 'https://ocw.mit.edu/courses/6-5060-algorithm-engineering-spring-2023/', 'https://ocw.mit.edu/courses/18-s191-introduction-to-computational-thinking-fall-2022/', 'https://ocw.mit.edu/courses/6-s980-machine-learning-for-inverse-graphics-fall-2022/', 'https://ocw.mit.edu/courses/14-15-networks-spring-2022/', 'https://ocw.mit.edu/courses/res-6-013-ai-101-fall-2021/', 'https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020/', 'https://ocw.mit.edu/courses/6-801-machine-vision-fall-2020/', 'https://ocw.mit.edu/courses/18-s191-introduction-to-computational-thinking-fall-2020/', 'https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/', 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/', 'https://ocw.mit.edu/courses/6-s191-introduction-to-deep-learning-january-iap-2020/', 'https://ocw.mit.edu/courses/6-s897-machine-learning-for-healthcare-spring-2019/', 'https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/', 'https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/', 'https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/', 'https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/', 'https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/', 'https://ocw.mit.edu/courses/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/', 'https://ocw.mit.edu/courses/6-005-software-construction-spring-2016/', 'https://ocw.mit.edu/courses/18-405j-advanced-complexity-theory-spring-2016/', 'https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/', 'https://ocw.mit.edu/courses/6-820-fundamentals-of-program-analysis-fall-2015/', 'https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/', 'https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/', 'https://ocw.mit.edu/courses/6-857-network-and-computer-security-spring-2014/', 'https://ocw.mit.edu/courses/6-s096-effective-programming-in-c-and-c-january-iap-2014/', 'https://ocw.mit.edu/courses/6-s096-introduction-to-c-and-c-january-iap-2013/', 'https://ocw.mit.edu/courses/6-837-computer-graphics-fall-2012/', 'https://ocw.mit.edu/courses/6-02-introduction-to-eecs-ii-digital-communication-systems-fall-2012/', 'https://ocw.mit.edu/courses/6-828-operating-system-engineering-fall-2012/', 'https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/', 'https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/', 'https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/', 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/', 'https://ocw.mit.edu/courses/18-337j-parallel-computing-fall-2011/', 'https://ocw.mit.edu/courses/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2011/', 'https://ocw.mit.edu/courses/6-096-introduction-to-c-january-iap-2011/', 'https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/', 'https://ocw.mit.edu/courses/6-092-introduction-to-programming-in-java-january-iap-2010/', 'https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/', 'https://ocw.mit.edu/courses/6-254-game-theory-with-engineering-applications-spring-2010/', 'https://ocw.mit.edu/courses/6-852j-distributed-algorithms-fall-2009/', 'https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2008/', 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2008/']

    def parse(self, response):
        # Extract the title from the webpage
        course = WebdatascrapeItem()
        course['title'] = response.css('title::text').get().split('|')[0].strip()
        paragraphs_expanded = response.css('#expanded-description p::text').getall()
        paragraphs_full = response.css('#expanded-description::text, #full-description::text').getall()
        course['des'] = ' '.join(paragraphs_expanded) if paragraphs_expanded else ' '.join(paragraphs_full)
        course['inst_name'] = response.css('.strip-link-offline::text').get()
        course['url'] = response.url
        tags = response.css('.text-black.course-info-topic.strip-link-offline::text').getall()
        new_tags = []
        for tag_original in tags:
            if tag_original not in new_tags:
                new_tags.append(tag_original)
        lowercase_tags = [item.lower() for item in new_tags]
        # For debug purpose
        print(lowercase_tags)
        print(tags)
        course['tags'] = [tag.strip() for tag in lowercase_tags] if lowercase_tags else None
        yield course
        # pass

