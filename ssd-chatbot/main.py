import random
from typing import Optional
from webcrawl import kbsearch
from laptop_lookup import get_laptop_spec
from parsing import parse_laptop_name, IntentExtractor, main_preprocessor, sample_queries
from csv_parser import ssd_list
from feature_parsing import SSDRequirements, feature_intent_extractor, feature_preprocessor, capacity_gb_to_str
import json
import os


class UserModel:
    """Model of the user"""

    def __init__(self, name: str):
        self.name = name
        self.ssd_requirements = SSDRequirements()
        self.selected_ssd_index = -1
        self.laptop_selected = False


USER_MODELS_FILE = 'users.json'

# create the file if it doesn't exist
if not os.path.exists(USER_MODELS_FILE):
    with open(USER_MODELS_FILE, 'w') as f:
        f.write(json.dumps({}))


def load_user_model(username: str) -> UserModel:
    """Read a user from the database, or create them if they don't exist"""

    # get all users from the file
    with open(USER_MODELS_FILE, 'r') as f:
        users = json.loads(f.read())

    user_id = username.lower()

    # if the user exists, load them
    if user_id in users:
        json_user = users[user_id]

        # create a new user object
        requirements = SSDRequirements()
        requirements.__dict__ = json_user['requirements']
        user = UserModel(username)
        user.__dict__ = json_user
        user.ssd_requirements = requirements
        return user

    # otherwise, make a new user
    else:
        return UserModel(username)


def save_user_model(user_model: UserModel):
    """Store the user model to the database"""

    user_id = user_model.name.lower()
    with open(USER_MODELS_FILE, 'r') as f:
        users = json.loads(f.read())
    with open(USER_MODELS_FILE, 'w') as f:
        requirements = dict(user_model.ssd_requirements.__dict__)
        json_user = dict(user_model.__dict__)
        del json_user['ssd_requirements']
        json_user['requirements'] = requirements
        users[user_id] = json_user
        f.write(json.dumps(users))


class AbstractUserInterface:
    """This is an abstract class representing the terminal object the user types into"""

    def __init__(self, initial_state):
        self.state = initial_state
        self.user_model: Optional[UserModel] = None

    def print(self, message):
        raise RuntimeError("Print method not implemented")

    def input(self) -> str:
        raise RuntimeError("Input method not implemented")

    def start(self):
        while True:
            self.state.prompt_user(self)


class TerminalInterface(AbstractUserInterface):
    """Command line terminal"""

    def print(self, message):
        print(f"Chatbot:\t{message}")

    def input(self) -> str:
        return input("You:\t\t")


class ChatbotState:
    """This is an abstract class representing the current mode / stage of the chatbot"""

    def prompt_user(self, ui: AbstractUserInterface):
        raise RuntimeError("Prompt user method not implemented")


# Train the main intent extractor
main_intent_extractor = IntentExtractor(main_preprocessor)
for intent, queries in sample_queries.items():
    main_intent_extractor.add_intent(intent, queries)
main_intent_extractor.train()


class LaptopModelState(ChatbotState):
    """In this state, the user enters their laptop, specifies what specs they want, and the system suggests a SSD"""

    def prompt_user(self, ui: AbstractUserInterface):
        requirements = ui.user_model.ssd_requirements

        # Make sure we know the interface & form factor of the SSD
        if not ui.user_model.laptop_selected:
            # Obtain the model name
            ui.print("I can help with that. What is your laptop's brand and model?")
            user_request = ui.input()
            model = parse_laptop_name(user_request)
            if not model:
                ui.print("Sorry we were not able to parse the Brand and model number")
                ui.print("Please type the Brand followed by the model like, ")
                ui.print("MSI Titan GT77 - 12U")
                return
            ui.print(f"Your Model is: {model}")

            # Get SSD specs of laptop given the model name
            spec_intf, spec_formfactor = get_laptop_spec(model)
            requirements.set_nn_requirement(key='Interface', value=spec_intf)
            requirements.set_nn_requirement(key='Form Factor', value=spec_formfactor)
        else:
            ui.print("I remember the storage interface of your laptop!")

        ui.user_model.laptop_selected = True

        # Get ssd specs
        while True:
            save_user_model(ui.user_model)
            ui.print("Tell me what SSD specs you want")
            ui.print("I can filter by: capacity, read or write speed, nand type (TLC or QLC), and DRAM (yes/no)")
            if str(requirements):
                ui.print(f"So far, you want: {requirements}")
                satisfactory_ssds = requirements.filter(ssd_list)
                ui.print(f"There are {len(satisfactory_ssds)} that satisfy your requirements")

            query = ui.input()
            intent = feature_intent_extractor.get_intent(query)
            if intent == 'done':
                break

            data = {}
            feature_preprocessor(query, data)

            if intent == 'capacity':
                if '$size' in data:
                    size_gb = data['$size']
                    requirements.set_capacity_requirement(size_gb)
                    ui.print(f"Ah, so you need it to have at least {capacity_gb_to_str(size_gb)}. Good call.")
                    continue
            elif intent == 'read_speed':
                if '$speed' in data:
                    speed = data['$speed']
                    requirements.set_read_speed_requirement(speed)
                    ui.print(f"I will make sure that the reading speed is at least {speed} MB/s")
                    continue
            elif intent == 'write_speed':
                if '$speed' in data:
                    speed = data['$speed']
                    requirements.set_write_speed_requirement(speed)
                    ui.print(f"Okay, I'll only find SSDs with a write speed of at least {speed} MB/s")
                    continue
            elif intent == 'yes_dram':
                requirements.set_dram_requirement(True)
                ui.print("We'll make sure your SSD has DRAM.")
                continue
            elif intent == 'no_dram':
                requirements.set_dram_requirement(False)
                ui.print("Got it, no DRAM.")
                continue
            elif intent == 'nand_type':
                if '$nand' in data:
                    nand_type = data['$nand']
                    requirements.set_nn_requirement(key='NAND Type', value=nand_type)
                    ui.print(f"Got it, you want {nand_type} nand.")
                    continue

            ui.print("Sorry, I don't understand.")

        # Print out a good ssd for the user
        satisfactory_ssds = ui.user_model.ssd_requirements.filter(ssd_list)
        if len(satisfactory_ssds) == 0:
            ui.print("Sorry, I didn't find any SSDs meeting your requirements.")
            ui.print("Maybe try narrowing your search.")
        else:
            selected_ssd = random.choice(satisfactory_ssds)
            ui.print("I found an SSD I think you'll like!")
            ui.print(f"Check out the {selected_ssd}")
            ui.state = MainChatbotState()


# Fact dictionary
FACT_DATABASE = kbsearch.FactDatabase('webcrawl/database.pickle')


class MainChatbotState(ChatbotState):
    """In this state, the user has logged in. They can ask to look up facts or upgrade their laptop."""

    def prompt_user(self, ui: AbstractUserInterface):
        ui.print(
            "I can either help you find a new SSD for your laptop, or I can provide basic information about SSD technology.")
        ui.print("How can I help you today?")
        user_request = ui.input()
        intent = main_intent_extractor.get_intent(user_request)
        topic = FACT_DATABASE.extract_term(user_request)

        if topic and topic not in ('storage', 'ssd', 'card', 'drive'):
            intent = 'research'

        if intent == "purchase":
            ui.state = LaptopModelState()
        else:
            if topic:
                ui.print(f"Here's something interesting about {topic}:")
                ui.print(FACT_DATABASE.query_database(topic))
            else:
                ui.print("Here's a list of topics I can tell you about:")
                ui.print(', '.join(FACT_DATABASE.terms))


class InitialChatbotState(ChatbotState):
    def prompt_user(self, ui: AbstractUserInterface):
        ui.print("Hello, my name is Charles!")
        ui.print("I am a chatbot designed to help you upgrade your laptop memory.")

        while True:
            ui.print("Enter your username to begin:")
            user_name = ui.input()
            if not user_name:
                ui.print("Sorry, I didn't get that.")
            else:
                break

        ui.user_model = load_user_model(user_name)

        ui.print(f"Welcome, {ui.user_model.name}!")
        ui.state = MainChatbotState()


def start():
    # initialize the terminal, current state
    ui = TerminalInterface(InitialChatbotState())
    ui.start()


if __name__ == '__main__':
    start()
