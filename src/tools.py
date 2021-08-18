import random
import string
import wpc2

is_debug = False

def log_print(msg, level):
    global is_debug
    if not is_debug and level > 1:
        return

    print(msg)

def generate_random_string(length, digits_only = False):
    choices = string.digits
    if not digits_only:
        choices += string.ascii_uppercase
    return ''.join(random.choices(choices, k=length))
    
def generate_random_sender():
    sender = wpc2.Sender()
    
    first_names = [ "Kam", "Deann", "Emory", "Manual", "Josefa", "Eldon", "Marcos", "Tiera", "Thu", "Emilia", "Ozella", "Jonas", "Magdalena", "Lora", "Buena", "Roxane", "Nellie", "Doris", "Doria", "Paul", "Carrie", "Sadye", "Raylene", "Catherin", "Virgen", "Elli", "Jennell", "Tamica", "Zoila", "Lisha", "Audrie", "Dena", "Regan", "Elyse", "Perla", "Marquitta", "Carin", "Malcolm", "Elly", "Lovie", "Don", "Errol", "Corrine", "Marcene", "Laure", "Mathew", "Gwendolyn", "Catherine", "Velva", "Gayla" ]
    last_names = [ "Rodriguez", "Woolford", "Dixion", "Jourdan", "Cardone", "Fett", "Luth", "Cuellar", "Gennaro", "Bara", "Yelvington", "Geesey", "Bolland", "Sommers", "Orrell", "Krick", "Broce", "Gayton", "Castellanos", "Stirling", "Winchenbach", "Simonds", "Reding", "Wescott", "Godbee", "Sprague", "Uribe", "Ripple", "Eudy", "Roberto", "Seal", "Costanzo", "Shankles", "Pennypacker", "Heckathorn", "Kiernan", "Ruddock", "Norrell", "Kanne", "Esh", "Colas", "Yaple", "Byars", "Brian", "Donahoe", "Helbing", "Mainor", "Sward", "Cantor", "Muhammad" ]

    has_last_name = False
    if bool(random.getrandbits(1)):
        has_last_name = True
    
    can_have_spaces = False    
    if has_last_name and bool(random.getrandbits(1)):
        can_have_spaces = True

    extra_numbers = 0
    if not has_last_name:
        extra_numbers = random.randint(0, 6)

    random_name = first_names[random.randint(0, len(first_names) - 1)]

    if can_have_spaces:
        random_name += " "

    if has_last_name:
        random_name += last_names[random.randint(0, len(last_names) - 1)]

    if extra_numbers > 0:
        if can_have_spaces and has_last_name:
            random_name += " "

        random_name += generate_random_string(extra_numbers, True)

    sender.name = random_name

    sender.email = sender.name.lower()
    if " " in sender.email:
        if bool(random.getrandbits(1)):
            sender.email = sender.email.replace(" ", "_")
        else:
            sender.email = sender.email.replace(" ", ".")

    extra_numbers = random.randint(0, 3)
    if extra_numbers > 0:
        sender.email += generate_random_string(extra_numbers, True)
        
    email_list = [ "gmail.com", "yahoo.com", "hotmail.com" ]
    sender.email += "@" + email_list[random.randint(0, len(email_list) - 1)]

    return sender
        
                              
