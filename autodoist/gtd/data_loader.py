import yaml
from autodoist.gtd.models import GTDState

class GTDDataLoader:
    def __init__(self, yaml_file: str):
        self.yaml_file = yaml_file

    def load_gtd_state_from_yaml(self) -> GTDState:
        with open(self.yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        # Perform semantic validations here if needed
        gtd_state = GTDState(**data)
        return gtd_state
