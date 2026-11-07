import re
from bs4 import BeautifulSoup


class HomePageParser:

    def clear_noise(self, html: str) -> str:
        html_page = BeautifulSoup(html, "html.parser")

        page_filter = html_page.find("main")

        if page_filter:
            return page_filter.prettify()

        return ""

    def _safe_text(self, element) -> str | None:
        return element.get_text(strip=True) if element else None

    def _extract_price(self, price_container) -> str | None:

        if not price_container:
            return None

        price_text = price_container.get_text(" ", strip=True)

        match = re.search(r"R\$\s*\d+(?:\.\d+)*(?:,\d+)?", price_text)

        if match:
            return match.group()

        return price_text

    def all_products_home(
        self,
        page_filter: str
    ) -> list[dict[str, str | None]]:

        soup = BeautifulSoup(page_filter, "html.parser")

        products: dict[str, dict[str, str | None]] = {}

        for card in soup.select("._1y-V6"):

            title = card.select_one("h3._3nYCL")

            if not title:
                continue

            title_text = title.get_text(strip=True)

            product_id = title_text

            container = card.parent

            sold = container.select_one("._2Zrnc")
            rating = container.select_one("._1vTvZ")
            reviews = container.select_one("._2013a")
            price_container = container.select_one("._12hIe")
            economy = container.select_one("._3d7Fj")
            image = card.select_one("img._8Dn7W")

            image_url = None

            if image:
                image_url = (
                    image.get("src")
                    or image.get("data-src")
                    or image.get("data-lazy-src")
                )

            link = None

            parent_link = card.find_parent("a")

            if parent_link:
                link = parent_link.get("href")

            products[product_id] = {
                "product_id": product_id,
                "title": title_text,
                "price": self._extract_price(price_container),
                "original_price": self._safe_text(economy),
                "sold": self._safe_text(sold),
                "rating": self._safe_text(rating),
                "reviews": self._safe_text(reviews),
                "image": image_url,
                "link": link,
            }

        return list(products.values())

    def parser_oferts_day(
        self,
        page_filter: str
    ) -> list[dict[str, str | None]]:

        soup = BeautifulSoup(page_filter, "html.parser")

        products: dict[str, dict[str, str | None]] = {}

        for card in soup.select(".cards--cardContainer--17Zn_RB"):

            product = card.select_one("[data-product-ids]")

            if not product:
                continue

            product_id = product.get("data-product-ids")

            if not product_id:
                continue

            title = card.select_one(".src--title--3I7Ij6g")
            price = card.select_one("._2024-price--minPrice--1TI_LeH")
            original_price = card.select_one("._2024-price--oriMinPrice--E52xats")
            image = card.select_one(".rc-modules--image--juUYhtJ")
            discount = card.select_one(".src--sdCountContainer--1T0rebt")

            image_url = None

            if image:
                image_url = (
                    image.get("src")
                    or image.get("data-src")
                    or image.get("data-lazy-src")
                )

            link = None

            parent_link = card.find_parent("a")

            if parent_link:
                link = parent_link.get("href")

            products[product_id] = {
                "product_id": product_id,
                "title": self._safe_text(title),
                "price": self._safe_text(price),
                "original_price": self._safe_text(original_price),
                "discount": self._safe_text(discount),
                "image": image_url,
                "link": link,
            }

        return list(products.values())

    def offerts_day(
        self,
        html: str
    ) -> list[dict[str, str | None]]:

        page_filter = self.clear_noise(html)

        if not page_filter:
            return []

        return self.parser_oferts_day(page_filter)

    def products_home(
        self,
        html: str
    ) -> list[dict[str, str | None]]:

        page_filter = self.clear_noise(html)

        if not page_filter:
            return []

        return self.all_products_home(page_filter)