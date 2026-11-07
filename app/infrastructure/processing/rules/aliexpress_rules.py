class RulesAliexpress:

    def __init__(self):
        self.worker_rules = {
            "Aliexpress": {
                "offersDayHomePage": "offers_day",
                "offersAllHomePage": "all_offers_home"
            }
        }

    def rules_worker(self, message: dict) -> str | None:
        app_name = message.get("app_name")
        service_name = message.get("service_name")

        return self.worker_rules.get(app_name, {}).get(service_name)

    def full(self) -> dict:
        return {
            "offers_day": self.worker_rules["Aliexpress"]["offersDayHomePage"],
            "offers_all": self.worker_rules["Aliexpress"]["offersAllHomePage"]
        }