class VendingMachineDFA:
    def __init__(self, config_file):
        self.states = set()
        self.alphabet = set()
        self.start_state = ""
        self.accept_states = set()
        self.transitions = {}
        self.current_state = ""
        self.path = []  
        self.load_config(config_file)
        self.total_money = 0  
        self.prices = {"A": 3000, "B": 4000, "C": 6000}

    def load_config(self, file_path):
        with open(file_path, 'r') as file:
            transitions_section = False
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith("Transitions:"):
                    transitions_section = True
                    continue
                
                if not transitions_section:
                    key, value = line.split(": ")
                    if key == "States":
                        self.states = set(value.split(", "))
                    elif key == "Alphabet":
                        self.alphabet = set(map(str.strip, value.split(", ")))
                    elif key == "Start":
                        self.start_state = value
                        self.current_state = value
                        self.path.append(f"S{self.current_state}")
                    elif key == "Accept":
                        self.accept_states = set(value.split(", "))
                else:
                    state, input_val, next_state = line.split(", ")
                    if state not in self.transitions:
                        self.transitions[state] = {}
                    self.transitions[state][input_val] = next_state

    def transition(self, input_value):
        input_value = str(input_value)
        if input_value in self.alphabet and input_value in self.transitions.get(self.current_state, {}):
            self.current_state = self.transitions[self.current_state][input_value]
            self.path.append(f"S{self.current_state}000")  
            if input_value.isdigit():
                self.total_money += int(input_value)
            return True
        return False

    def is_accept_state(self):
        return self.current_state in self.accept_states

    def check_drink_availability(self):
        for drink, price in self.prices.items():
            if self.total_money >= price:
                print(f"ON: Minuman {drink}")

    def change(self):
        self.total_money -= self.prices[user_input]
        print(f"Kembalian: {self.total_money}")

    def reset(self):
        self.current_state = self.start_state
        self.path = [f"S{self.current_state}"]  
        self.total_money = 0  

# Simulasi Program
vending_machine = VendingMachineDFA("vending_dfa.txt")

while True:
    vending_machine.check_drink_availability()
    user_input = input("Masukkan uang atau pilih minuman (1000, 2000, 5000, 10000, A, B, C): ")
    if user_input.isdigit():
        user_input = int(user_input)
    elif user_input in {"A", "B", "C"}:
        print(f"Lintasan DFA: {' -> '.join(vending_machine.path)}")
        if vending_machine.total_money >= vending_machine.prices[user_input]:
            print(f"Minuman {user_input} dapat dibeli. Status: ACCEPTED.")
            if vending_machine.total_money == 0:
                break
            else:
                vending_machine.change()
            break
        else:
            print("Uang tidak cukup. Status: REJECTED.")
            break
    if vending_machine.transition(user_input):
        print(f"Total uang saat ini: {vending_machine.total_money}")
    else:
        print("Input tidak valid atau tidak tersedia dalam transaksi. Status: REJECTED.")
        vending_machine.reset()