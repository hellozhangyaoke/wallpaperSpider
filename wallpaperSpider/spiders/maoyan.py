import scrapy,json
from wallpaperSpider.items import MaoyanItem

class MaoyanSpider(scrapy.Spider):

    name = "maoyan"
    page = 1
    allowed_domains = ["zuimeix.com"]
    start_urls = [
        "https://wallpaper.zuimeix.com/wp-json/mp/v2/posts?per_page=50&page=1"
        # 潮图
        # "https://wallpaper.zuimeix.com/wp-json/mp/v2/posts?orderby=rand&per_page=15&categories=1&page=1",
        # # 热门
        # "https://wallpaper.zuimeix.com/wp-json/mp/v2/posts?custom=most&per_page=15&categories=1&page=1"
    ]


    def parse(self,response):

        result = response.body.decode()
        result = json.loads(result)
        
        for info in result:

            date = info["date"]
            cates = info["categories"]
            tags = info["tags"]
            color = info["color"]
            wallpaper = info["wallpaper"]

            for w in wallpaper:
                old_id = w["id"]
                meta = json.dumps(w["meta"])
                thumb = w["thumb"]
                large = w["large"]
                cover = w["cover"]
                full = w["full"]

            item = MaoyanItem()
            item["tag"] = tags
            item["categorie"] = cates
            item["date"] = date
            item["meta"] = meta
            item["thumb"] = thumb
            item["large"] = large
            item["cover"] = cover
            item["full"] = full
            item["color"] = color
            item["old_id"] = old_id
            # with open("text.json","a+",encoding="utf-8") as f:
            #     f.write(thumb)
            #     f.write("\n")
            #     f.write(large)
            #     f.write("\n")
            yield item

        self.page += 1
        url = "https://wallpaper.zuimeix.com/wp-json/mp/v2/posts?per_page=50&page=%d"%self.page
        yield scrapy.Request(url=url,callback=self.parse)
