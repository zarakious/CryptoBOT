def gain () :
    intial = 366
    for i in range(1,365,1):
        intial = intial + (intial*2.19)/100
        print(f'{i} - {intial}')
        

def outside_price(price):
    outside= price + ((price *3)/100)
    print(f'The exist price is : {outside}')
gain()  
outside_price(28.500)