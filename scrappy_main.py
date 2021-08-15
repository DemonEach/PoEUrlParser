import scrapy
import colorama
from urllib.parse import urlparse

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW


class PoeSprider(scrapy.Spider):
    name = 'arakali'
    start_urls = ['https://pathofexile.fandom.com/wiki/Path_of_Exile_Wiki']
    allowed_domains = ['pathofexile.fandom.com', 'static.wikia.nocookie.net', '']
    visited_links = set()

    def parse(self, response, **kwargs):
        # for title in response.css('.title'):
        #     print(f"{GREEN}GOING TO: {title}{RESET}")
        #     yield {'title': title.css('::text').get()}

        for next_page in response.css('a'):
            # print(f"{next_page}")
            try:
                ref = next_page.attrib['href']
                if self.domain_check(ref):
                    is_good_domain, domain = self.check_for_duplicates(ref)
                    if is_good_domain:
                        print(f"{YELLOW}NEXT PAGE IS: {next_page.attrib['href']}{RESET}")
                        if domain == '':
                            self.visited_links.add('pathofexile.fandom.com' + ref)
                        else:
                            self.visited_links.add(ref)
            except:
                pass

            yield response.follow(next_page, self.parse)

        # for img_url in response.css('img'):
        #     print(f"{RED}ImgUrl: {img_url.attrib['src']} {RESET}")

        with open(f"poe_wiki.txt", "w") as f:
            for visited_link in self.visited_links:
                print(visited_link.strip(), file=f)

    def check_for_duplicates(self, ref):
        return ref not in self.visited_links

    def domain_check(self, ref):
        domain = urlparse(ref).netloc
        # print(f"REF: {ref} PARSED DOMAIN: {domain} GOOD DOMAIN: {domain in self.allowed_domains}")

        return domain in self.allowed_domains, domain
