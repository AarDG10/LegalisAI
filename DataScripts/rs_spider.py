import scrapy

class IndianKanoonSpider(scrapy.Spider):
    name = "indian_kanoon"
    start_urls = ['https://indiankanoon.org/search/?formInput=Maharashtra+Real+estate+cases']  # Adjust the query as needed

    def parse(self, response):
        # Extract case summaries from the search results
        citations=[]
        cntr=0
        for case in response.css('div.result'):  # this for citation count with its redirected link
            cntr+=1
            vari=case.css('div.hlbottom a.cite_tag::attr(href)').get()
            citations.append({
                'link':vari,
                'citation_num':cntr
            })
            
        for case in response.css('div.result'):
            linky = response.urljoin(case.css('div.result_title a::attr(href)').get())
            yield {
                'title': case.css('div.result_title a::text').getall(),  #title extracts keywords in the title
                'link': linky,
                'summary': case.css('div.headline::text').getall(),
                'source':case.css('div.hlbottom span.docsource::text'),
                'citation_links':citations
            }

        # Pagination: follow the link to the next page
        next_page = response.css('a.next::attr(href)').get()  # Adjust for the next page link
        if next_page:
            yield response.follow(next_page, self.parse)
