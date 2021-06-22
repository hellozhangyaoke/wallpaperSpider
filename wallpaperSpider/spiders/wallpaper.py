import scrapy
from wallpaperSpider.items import WallpaperspiderItem

class WPSpider(scrapy.Spider):

    name = "wpspider"
    allowed_domains = ["ilikewallpaper.net"]
    start_urls = [
        # "https://www.ilikewallpaper.net/iphone-12/Wallpapers/Trending/1"
        # "https://www.ilikewallpaper.net/4k-iphone-x-wallpapers/1",
        # "https://www.ilikewallpaper.net/girl-iphone-wallpapers/1"
        "https://www.ilikewallpaper.net/5k-ipad-pro-wallpapers/1",
        "https://www.ilikewallpaper.net/4k-ipad-pro-wallpapers/1",
        "https://www.ilikewallpaper.net/5k-ipad-air-wallpapers/1",
        "https://www.ilikewallpaper.net/4k-ipad-air-wallpapers/1"

    ]


    def parse(self,response):
        domain = "https://www.ilikewallpaper.net"
        urls = response.xpath("//div[@id='divWalllist']//dl//dd//a//@href").extract()
        for url in urls:
            yield scrapy.Request(url=domain+url,callback=self.get_img_url)
        try:
            next_link = response.xpath("//a[@class='next']/@href").extract()[0]
            yield scrapy.Request(url="https://www.ilikewallpaper.net/" + next_link,callback=self.parse)
        except:
            print("所有页面爬取完成！")

    def get_img_url(self,response):
        item = WallpaperspiderItem()
        try:
            item["img_url"] = "https:" + (response.xpath("//li[@class='download']//a/@href").extract())[0]
            _targets = response.xpath("//dl[@class='tags clearfix']//dd//text()").extract()
            item["targets"] = ",".join([i.replace("#","") for i in _targets])
            yield item
        except:
            pass


