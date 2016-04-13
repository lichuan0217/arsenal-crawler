# -*- coding: utf-8 -*-
import scrapy
from arsenal.items import ArsenalCardItem, ArsenalArticalItem, ArsenalArticalVideoItem


class ArsenalSpiderSpider(scrapy.Spider):
    name = "arsenal_spider"
    allowed_domains = ["hupu.com"]
    start_urls = (
        'http://voice.hupu.com/o/arsenal',
    )
    close_down = False

    def convert_content(self, orginal):
        return orginal[0].strip() if len(orginal) > 0 else ""

    def convert_main_content(self, paragraph):
        if len(paragraph) > 0:
            return "\n".join(paragraph)

    def convert_artical_id(self, url):
        return url.split('.html')[0].split('/')[-1]

    def parse(self, response):
        card_list = response.xpath(
            "//body/div[@class='hp-wrap']/div[@class='voice-main']/div[@class='voice-msg-card-list']/div")
        for card in card_list:
            if self.close_down:
                # raise scrapy.exceptions.CloseSpider(reason = "No newer item")
                return
            content = card.xpath("div[@class='voice-card-list']/div")
            full_text_url = content.xpath(
                "div[@class='card-fullText-hd']/a/@href").extract()
            card_header = content.xpath(
                "div[@class='card-fullText-hd']/a/text()").extract()
            card_content = content.xpath(
                "div[@class='card-inner']/div[@class='voice-card-content']/span/text()").extract()
            card_small_photo = content.xpath(
                "div[@class='card-inner']/div[@class='card-smaillPhoto']/a/img/@src").extract()
            card_src = content.xpath(
                "div[@class='voice-card-otherInfo']/span[@class='comeFrom']/a/text()").extract()

            item = ArsenalCardItem()
            item['full_text_url'] = self.convert_content(full_text_url)
            item['card_header'] = self.convert_content(card_header)
            item['card_content'] = self.convert_content(card_content)
            item['card_small_photo'] = self.convert_content(card_small_photo)
            item['card_src'] = self.convert_content(card_src)
            item['artical_id'] = self.convert_artical_id(item['full_text_url'])

            yield item
            print "yield item"
            yield scrapy.Request(item['full_text_url'], callback=self.parse_full_content)
            print "yield artical"
            # yield item

        # Next page to be crwaled
        next_page = response.xpath("//body/div[@class='hp-wrap']/div[@class='voice-main']/div[@class='voice-paging']/a/@href")
        print response.urljoin(next_page[0].extract())



    def parse_full_content(self, response):
        artical = response.xpath("//body/div[@class='hp-wrap']/div[@class='voice-main']")
        artical_title = artical.xpath("div[@class='artical-title']/h1/text()").extract()
        artical_src = artical.xpath("div[@class='artical-title']/div[@class='artical-info']/span/span[@class='comeFrom']/a/text()").extract()
        artical_date = artical.xpath("div[@class='artical-title']/div[@class='artical-info']/span/a/span/text()").extract()
        artical_content = artical.xpath("div[@class='artical-content']")
        artical_content_read = artical_content.xpath("div[@class='artical-content-read']")
        artical_content_video = artical_content.xpath("div[@class='artical-content-video']")

        if len(artical_content_read) > 0:
            print "read item"
            artical_important_pic = artical_content_read.xpath("div[@class='artical-importantPic']/img/@src").extract()
            artical_main_content = artical_content_read.xpath("div[@class='artical-main-content']//p/text()").extract()
            artical_editor = artical_content_read.xpath("div[@class='artical-main-content']/span/text()").extract()
            item = ArsenalArticalItem()
            item['artical_type'] = "read"
        elif len(artical_content_video) > 0:
            print "video item"
            artical_important_pic = artical_content_video.xpath("div[@class='artical-video-play']/a/img/@src").extract()
            artical_main_content = artical_content_video.xpath("div[@class='artical-main-content']//p/text()").extract()
            artical_editor = artical_content_video.xpath("div[@class='artical-main-content']/span/text()").extract()
            artical_video_play = artical_content_video.xpath("div[@class='artical-video-play']/a/@href").extract()
            item = ArsenalArticalVideoItem()
            item['artical_type'] = "video"
            item['artical_video_play'] = self.convert_content(artical_video_play)
        

        # item = ArsenalArticalItem()
        item['artical_title'] = self.convert_content(artical_title)
        item['artical_src'] = self.convert_content(artical_src)
        item['artical_date'] = self.convert_content(artical_date)
        item['artical_important_pic'] = self.convert_content(artical_important_pic)
        item['artical_main_content'] = self.convert_main_content(artical_main_content)
        item['artical_editor'] = self.convert_content(artical_editor)
        item['artical_id'] = self.convert_artical_id(response.url)

        yield item
