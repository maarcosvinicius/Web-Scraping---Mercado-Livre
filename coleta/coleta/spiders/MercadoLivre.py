import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css('div.ui-search-result__content')  # 54 itens

        for product in products:

            prices = product.css(
                'span.andes-money-amount__fraction::text').getall()
            cents = product.css(
                'span.andes-money-amount__cents::text').getall()

            # Função para chamar varias vezes e fazer todas as coletas
            yield {
                'marca': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'nome': product.css('h2.ui-search-item__title::text').get(),
                # A questão do if else, é para se não encontrar valor, colocar nulo e seguir para a proxima condicional,
                # Porque tem casos que não vai ter todas as informações
                'preco_antigo_reais': prices[0] if len(prices) > 0 else None,
                'preco_antigo_centavos': cents[0] if len(cents) > 0 else None,
                'preco_novo_reais': prices[1] if len(prices) > 1 else None,
                'preco_novo_centavos': cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get()
            }

        if self.page_count < self.max_pages:
            next_page = response.css(
                'li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
