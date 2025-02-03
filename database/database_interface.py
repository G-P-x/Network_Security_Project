from database.user_database import UserDatabaseSingleton as db_user
class db_interface:
    def __init__(self):
        self.user_db = db_user()
        pass

    def sign_in(self, **kwargs):
        '''Write to the database
        input format: write(username = 'username', password = 'password')'''
        if not self.check_input(**kwargs):
            return False
        return self.user_db.add_user(kwargs['username'], kwargs['password'])

    def login(self, **kwargs):
        if not self.check_input(**kwargs):
            return False
        return self.user_db.get_user(kwargs['username'], kwargs['password'])
        

    def check_input(self, **kwargs):
        '''Check if the input is correct'''
        error_message = 'Expected two strings as input'
        error_message_2 = 'Expected username and password as input'
        error_message_3 = r"you can not use the following characters: \", ;, --, /*, */, xp_, \t, \n, \r"
        try:
            assert (isinstance(kwargs, dict) and len(kwargs) == 2 
                    and all(isinstance(value, str) for value in kwargs.values())), error_message
            assert 'username' in kwargs and 'password' in kwargs, error_message_2
            forbidden_characters = ("'", '"', ";", "--", "/*", "*/", "xp_"," ", "\t", "\n", "\r")
            for forbidden in forbidden_characters:
                assert forbidden not in kwargs['username'], error_message_3
                # the password is hashed, so we can leave it as it is
            return True
        except(AssertionError) as e:
            print(e) # for debugging, eventually save the error message to a log file
            return False
    
if __name__ == '__main__':
    db = db_interface()

    assert db.check_input(username='username', password='password') == True
    assert db.check_input(username='username;', password='password') == False
    assert db.check_input(username='username"', password='password') == False
    assert db.check_input(username='username--', password='password') == False
    assert db.check_input(username='username/*', password='password') == False
    assert db.check_input(username='username*/', password='password') == False
    assert db.check_input(username='usernamexp_', password='password') == False
    assert db.check_input(username='username\t', password='password') == False
    assert db.check_input(username='username\n', password='password') == False
    assert db.check_input(username='username\r', password='password') == False
    assert db.check_input(username='username', password='password', another=2) == False
    assert db.check_input(username=' username ', password='ciao a tutti ') == False
    assert db.check_input(username='username', password=2) == False
    assert db.check_input(username=2, password='password') == False
    assert db.check_input(username='username', password = False) == False
    assert db.check_input(username=False, password='password') == False
    assert db.check_input(username='username') == False

    assert db.sign_in(username='my_name', password='password') == True
    assert db.login(username='username', password='password') == True

        