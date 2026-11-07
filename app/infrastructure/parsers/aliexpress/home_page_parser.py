from bs4 import BeautifulSoup


class HomePageParser:

    def clear_noise(self, html: str) -> str:
        html_page = BeautifulSoup(html, "html.parser")

        page_filter = html_page.find("main")

        if page_filter:
            return page_filter.prettify()

        return ""

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
            original_price = card.select_one(
                "._2024-price--oriMinPrice--E52xats"
            )
            image = card.select_one(".rc-modules--image--juUYhtJ")
            discount = card.select_one(
                ".src--sdCountContainer--1T0rebt"
            )

            image_url = None

            if image:
                image_url = (
                    image.get("src")
                    or image.get("data-src")
                    or image.get("data-lazy-src")
                )

            products[product_id] = {
                "product_id": product_id,
                "name": title.get_text(strip=True) if title else None,
                "price": price.get_text(strip=True) if price else None,
                "original_price": (
                    original_price.get_text(strip=True)
                    if original_price else None
                ),
                "discount": (
                    discount.get_text(strip=True)
                    if discount else None
                ),
                "image": image_url
            }

        return list(products.values())

    def offerts_day(self, html: str) -> list[dict[str, str | None]]:

        page_filter = self.clear_noise(html=html)

        if not page_filter:
            return []

        offers = self.parser_oferts_day(page_filter=page_filter)

        return offers