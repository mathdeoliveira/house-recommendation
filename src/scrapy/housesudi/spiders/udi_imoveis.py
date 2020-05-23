# -*- coding: utf-8 -*-
import scrapy


class ImoveisSpider(scrapy.Spider):
    name = 'imoveis'
    allowed_domains = ['www.siteimoveis.com.br/venda/imoveis/mg+uberlandia/']
    start_urls = ['http://www.siteimoveis.com.br/venda/imoveis/mg+uberlandia/']

    def start_requests(self):
        pages = 278
        for i in range(1, pages+1):
            start_url = 'http://www.siteimoveis.com.br/venda/imoveis/mg+uberlandia/'
            url = start_url + '?pagina=%s' % i 
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        imoveis = response.xpath('.//*[@class="card-container"]')
        length = len(imoveis)
        for i in range(1, length+1):
            preco = imoveis.xpath('normalize-space(//*[@id="app"]/section/div/div/section/div/div[%s]/div/div[2]/div[1]/p/strong/text())' % i).extract_first()
            endereco = imoveis.xpath('//*[@id="app"]//div[%s]//div[3]//p/text()' % i).extract_first()
            area = response.xpath('normalize-space(//*[@id="app"]/section/div/div/section/div/div[%s]/div/div[2]/div[3]/ul/li[1]/span[2]/text())' % i).extract_first()
            quartos = response.xpath('normalize-space(//*[@id="app"]/section/div/div/section/div/div[%s]/div/div[2]/div[3]/ul/li[2]/span[2]/text())' % i).extract_first() 
            garagem = response.xpath('normalize-space(//*[@id="app"]/section/div/div/section/div/div[%s]/div/div[2]/div[3]/ul/li[3]/span[2]/text())' % i).extract_first() 
            banheiros = response.xpath('normalize-space(//*[@id="app"]/section/div/div/section/div/div[%s]/div/div[2]/div[3]/ul/li[4]/span[2]/text())' % i).extract_first()
            
            yield {
                'preco': preco,
                'endereco': endereco,
                'area': area,
                'quartos': quartos,
                'garagem': garagem,
                'banheiros': banheiros,
            }   