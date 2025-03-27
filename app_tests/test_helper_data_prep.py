# creates data to be used in test_data_prep

def create_stock_ex():
    '''
    Returns example similar to stock_prices
    '''
    return """Date,Close/Last
01/01/2021,$50.00
01/02/2021,$55.25
01/08/2021,$53.50
"""

def create_egg_price_ex():
    """
    Returns example similar to egg_price
    """
    return """Year,Jan,Feb
2020,1.50,1.60
2021,2.00,2.10
"""

def create_bird_flu_ex():
    """
    Returns example similar to bird_flu
    """
    return """State,County,Flock Size,lat,lng
Alabama,Montgomery,1000,32.3668052,-86.2999689
Georgia,Clarke,2000,33.9519347,-83.357567"""

def create_wild_bird_ex():
    """
    Returns example similar to wild bird data
    """
    return """State,County,lat,lng
Alabama,Montgomery,32.3668052,-86.2999689
Georgia,Clarke,33.9519347,-83.357567
Florida,Miami-Dade,25.7616798,-80.1917902
"""
