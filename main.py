import multiprocessing
import hashlib

accounts = {}


def create_acc(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    accounts[ username ] = hashed_password
    print(f'Account created for {username}')


def login(username, password):
    hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
    if username in accounts and accounts[ username ] == hashed_pwd:
        print(f'Welcome {username}')
        return True
    else:
        print('Invalid credentials')
        return False


def check_balance(balance, lock):
    lock.acquire()
    print(f'Current balance: {balance.value}')
    lock.release()


def withdraw(balance, lock, amaount):
    lock.acquire()
    if balance.value >= amaount:
        print(f'Withdrawing {amaount}....')
        balance.value -= amaount
        print(f'New balance: {balance.value}')
    else:
        print('Insufficient Funds')
    lock.release()


def deposit(balance, lock, amount):
    lock.acquire()
    print(f'Depositing {amount}...')
    balance.value += amount
    print(f'New balance: {balance.value}')
    lock.release()


if __name__ == '__main__':
    create_acc('johndoe', 'pass1234')
    logged_in = False
    balance = multiprocessing.Value('i', 100)
    lock = multiprocessing.Lock()
    while True:
        logged_in = False
        while not logged_in:
            username = input('Enter username: ')
            password = input('Enter password: ')
            logged_in = login(username, password)

        while logged_in:
            print('1.Check Balance\n2.Withdraw\n3.Deposit\n4.Logout')
            transaction_type = input("What transaction would you like to perform: ")

            if transaction_type == '1':
                check_balance(balance, lock)
            elif transaction_type == '2':
                withdraw(balance, lock, 50)
            elif transaction_type == '3':
                deposit(balance, lock, 25)
            elif transaction_type == '4':
                print('Thank You, bye!')
                logged_in = False

# balance = multiprocessing.Value('i', 100)
# lock = multiprocessing.Lock()
#
# p1 = multiprocessing.Process(target=check_balance, args=(balance,lock))
# p2 = multiprocessing.Process(target=withdraw, args=(balance,lock,50))
# p3 = multiprocessing.Process(target=deposit, args=(balance,lock,25))
#
# p1.start()
# p2.start()
# p3.start()
#
# p1.join()
# p2.join()
# p3.join()
