class WorkerAliexpress:

    def __init__(self, controller, rules):
        self.controller = controller
        self.rules = rules

    def start_worker(self, message: dict):

        handler = self.rules.rules_worker(message)

        if handler is None:
            return None

        return self.controller.execute_service(handler)