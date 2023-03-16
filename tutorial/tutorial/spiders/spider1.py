import scrapy
count = 0
linksVisited = []

class QuotesSpider(scrapy.Spider):
    name = "Biodiversity"
    allowed_domains = [
        'wikipedia.org'
    ]
    start_urls = [
        "https://en.wikipedia.org/wiki/Main_Page",
        ""
    ]

    def parse(self, response):
        terms = ["Walt Disney", "Hollywood ", "United States", "Academy Awards"]
        anchors = response.css("a")
        global count
        global linksVisited
        count += 1
        print("No of linkks", len(anchors))
        for anchor in anchors:
            text = anchor.xpath('.//text()').get()
            link = anchor.xpath('.//@href').get()
            if text == None:
                continue
            # print("text", text)
            # print("link", link)
            for term in terms:
                if term in text:
                    print("\nEver reached here\n")
                    if link == "/wiki/Walt_Disney":
                        yield {"found":"found the page"}
                    else:
                        if(link not in linksVisited):
                            linksVisited.append(link)
                            yield response.follow(link, self.recursive, meta={'terms': terms})

        yield {'counts': count}

    def recursive(self, response):
        global count
        global linksVisited
        count += 1

        anchors = response.css("a")
        # if(anchors == None):
        #     yield {"error":"Not able to reach"}
        # terms = response.meta.get('terms')
        terms = response.meta["terms"]
        print("am i getting terms", terms)
        print("No of links", len(anchors))
        for anchor in anchors:
            text = anchor.xpath('.//text()').get()
            link = anchor.xpath('.//@href').get()
            if text == None or link == None:
                continue
            for term in terms:
                if term in text:
                    if link == "/wiki/Walt_Disney":
                        yield {"found":"able to reach"}
                    else:
                        if link not in linksVisited:
                            linksVisited.append(link)
                            yield response.follow(link, callback=self.recursive, meta = {"terms":terms})
        yield {"message":"Can't Follow"}