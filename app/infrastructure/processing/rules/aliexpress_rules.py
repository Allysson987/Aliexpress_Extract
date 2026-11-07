class RulesAliexpress:

    def __init__(self, home_page):
        self.worker_rules = {
            "Aliexpress": {
                "homePage": home_page.navigator_homePage,
            }
        }

    def rules_worker(self, message: dict):
        app_name = message.get("app_name")
        service_name = message.get("service_name")

        return self.worker_rules.get(app_name, {}).get(service_name)