from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# data which we are going to display as tables
DATA = [[ "Item Number" , "Name", "Quantity", "Price" ]]

ORDER = []

ITEM_NUM = 0

def pdf_builder():
   
    # creating a Base Document Template of page size A4
    pdf = SimpleDocTemplate( "receipt.pdf" , pagesize = A4 )
    
    # standard stylesheet defined within reportlab itself
    styles = getSampleStyleSheet()
    
    # fetching the style of Top level heading (Heading1)
    title_style = styles[ "Heading1" ]
    
    # 0: left, 1: center, 2: right
    title_style.alignment = 1
    
    # creating the paragraph with
    # the heading text and passing the styles of it
    title = Paragraph( "Order Reciept" , title_style )
    
    # creates a Table Style object and in it,
    # defines the styles row wise
    # the tuples which look like coordinates
    # are nothing but rows and columns
    style = TableStyle(
        [
            ( "BOX" , ( 0, 0 ), ( -1, -1 ), 1 , colors.black ),
            ( "GRID" , ( 0, 0 ), ( -1 , -2 ), 1 , colors.black ),
            ( "BACKGROUND" , ( 0, 0 ), ( 3, 0 ), colors.gray ),
            ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.whitesmoke ),
            ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ),
            ( "BACKGROUND" , ( 0 , 1 ) , ( -1 , -1 ), colors.beige ),
        ]
    )
    
    # creates a table object and passes the style to it
    table = Table( DATA , style = style )
    
    # final step which builds the
    # actual pdf putting together all the elements
    pdf.build([ title , table ])
    return 0

def detect_meals():
    
    global ORDER, DATA
    

    price = 0;
    word_used = "";

    if (ORDER.count('number') > 0):
        i = ORDER.index('number')
        word_used = "number"
        quantity = ORDER[i-1]

    elif (ORDER.count('meal') > 0):
        i = ORDER.index('meal')
        word_used = "meal"
        meal_number = (ORDER[i+ 1])
        quantity = ORDER[i-2]

    else:
        return 0


    if meal_number == 1:
        price = 7
    
    if meal_number == 2:
        price = 12
    
    if meal_number == 3:
        price = 5

    global ITEM_NUM
    ITEM_NUM += 1

    price = price * int(quantity)

    DATA.append([ITEM_NUM , ('meal' + meal_number), quantity, "$ " + str(price)])

    ORDER.remove(word_used)
    return price

def detect_fries():

    price = 0;

    global ORDER, DATA

    if (ORDER.count('fries') > 0):
        i = ORDER.index('fries')
        fry_size = (ORDER[i-1])
        quantity = ORDER[i-2]

    else:
        return 0

    if fry_size == 'small':
        price = 1
    
    if fry_size == 'medium':
        price = 1.5
    
    if fry_size == 'large':
        price = 2

    global ITEM_NUM
    ITEM_NUM += 1;

    price = price * int(quantity)

    DATA.append([ITEM_NUM , (" fries - " + fry_size), quantity, "$ " + str(price)])

    ORDER.remove('fries')
    return price

def detect_icecream():
 
    price = 0;

    global ORDER, DATA

    if (ORDER.count('ice') > 0):
        i = ORDER.index('icecream')
        cream_size = (ORDER[i-2])
        cream_type = ORDER[i-1] 
        quantity = ORDER[i-3]

    else:
         return 0

    if cream_size == 'small':
        price = 2
    
    if cream_size == 'medium':
        price = 2.5
    
    if cream_size == 'large':
        price = 3

    global ITEM_NUM
    ITEM_NUM += 1;

    price = price * int(quantity)

    DATA.append([ITEM_NUM , (cream_type + ' ice cream - ' + cream_size), quantity, "$ " + str(price)])

    ORDER.remove('ice')
    return price

def call_func(order):

    global ORDER, DATA

    ORDER = order

    old_price = -1
    new_price = 0
    while old_price != new_price:

        old_price = new_price

        #new_price += detect_meals()
        new_price +=  detect_fries()
        new_price += detect_icecream()

    DATA.append([ "Sub Total", "", "", str(new_price)])
    DATA.append([ "Tax", "", "", str((new_price*0.085))])
    DATA.append([ "Total", "", "", str(new_price*1.085)])

    pdf_builder()
