import scrapy


class MangaSpider(scrapy.Spider):
    name = "manga"
    allowed_domains = ["itadakima.su"]
    start_urls = ["https://itadakima.su/index.php?cat=1"]

    def parse(self, response):
        for product in response.css('.ProductsList'):
            product_page = response.urljoin(product.css('.ProductsListName a::attr(href)').get())
            yield response.follow(product_page, self.parse_product)

        next_page = response.css('a.pageResults[title=" Следующая страница "]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        price = response.css('.price p').xpath('span[@class="leftsymbol"]/following-sibling::text()[1]').get()
        if price:
            price = price.strip()
        yield {
            'name': response.css('h1.contentBoxHeading::text').get(),
            'price': price,
            'series': response.css('dl:contains("Серия:") dd a::text').getall(),
            'authors': response.css('dl:contains("Авторы:") dd a::text').getall(),
            'genres': response.css('dl:contains("Жанр:") dd a::text').getall(),
            'formats': response.css('dl:contains("Формат:") dd::text').get(),
            'producer': response.css('dl:contains("Производитель:") dd a::text').get(),
            'description': response.css('dl.productsDescription dd p::text').getall(),
        }