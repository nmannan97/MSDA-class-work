import re 

class regex():
    
    def __init__(self):
        self.text = "Today is 05/12/2025, and tomorrow will be 05/13/2025. Invalid: 5/2/25."
        self.emails = ["alice@gmail.com", "bob@yahoo.com", "carl@outlook.com"]
        self.passwords = ["Pass1234", "password", "12345678", "NoDigitsHere", "StrongPass1"]

    """
    Given a string that contains multiple dates in the format MM/DD/YYYY, extract all the valid dates in self.text
    """
    def date_extract(self):
        return_value = re.findall(r".[0-9]//.[0-9]*//.[0-9]*", self.text)
        return return_value


    """
    Given a list of email addresses, replace the domain with ***.com.
    """
    def email_thing(self):
        pass


    """
    Write a regex pattern that matches passwords that:

    Are 8–20 characters long
    Contain at least one uppercase letter
    Contain at least one lowercase letter
    Contain at least one digit
    """
    def password(self):
        pass


if __name__ == "__main__":
    print(regex().date_extract())