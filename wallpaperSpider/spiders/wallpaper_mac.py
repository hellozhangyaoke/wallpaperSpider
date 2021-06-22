import scrapy
from wallpaperSpider.items import WallpaperspiderItem

class WPSpider(scrapy.Spider):

    name = "wpspider_mac"
    allowed_domains = ["allmacwallpaper.com"]
    start_urls = [
        "https://www.instawallpaper.com/apple-iphone-11-pro-max-wallpapers/Views/1",
        "https://www.instawallpaper.com/samsung-galaxy-s10-plus-wallpapers/Views/1",
        "https://www.instawallpaper.com/xiaomi-mi-note-10-wallpapers/Views/1"
    ]


    def parse(self,response):
        domain = "https://www.allmacwallpaper.com/"
        urls = response.xpath("//article//dt//a//@href").extract()
        for url in urls:
            yield scrapy.Request(url=domain+url,callback=self.get_img_url)
        try:
            next_link = response.xpath("//a[@class='next']/@href").extract()[0]
            yield scrapy.Request(url=domain + next_link,callback=self.parse)
        except:
            print("所有页面爬取完成！")

    def get_img_url(self,response):
        item = WallpaperspiderItem()
        try:
            item["img_url"] = "https:" + response.xpath("//div[@class='downloadList']//a/@href").extract()[6]
            _targets = response.xpath("//dl[@class='tags clearfix']//dd//em/text()").extract()
            item["targets"] = ",".join([i.replace("#","") for i in _targets])
            yield item
        except:
            pass
