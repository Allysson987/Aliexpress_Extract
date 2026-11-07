class ProductDetailsExtract:

    def __init__(self, http_client, parser):
        self.http_client = http_client
        self.parser = parser

    def build_product_url(self, product_id: str) -> str:
        return f"https://pt.aliexpress.com/item/{product_id}.html"
    

    def extract_product(self, product_id: str) -> dict:
        url = self.build_product_url(product_id)

        response = self.http_client.get(url)
        response.raise_for_status()
        

        return self.parser.details_product(response.text)