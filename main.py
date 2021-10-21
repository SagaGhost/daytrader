import random
import pandas

TYPES_OF_GOODS = ['corn', 'wheat', 'beans']
START_PRICE = 5
TRANSACTION_EFFECT = 1
START_CASH_MAX = 100
START_CASH_MIN = 50
START_GOODS_MAX = 20
START_GOODS_MIN = 5
# the trader class is the main operator in a market.


class Trader:
    variance_min = 1
    variance_max = 10
    confidence_max = 5
    confidence_min = -5
    confidence_step = 1

    def __init__(self, name,  confidence,
                 cash, quantitiy_good):
        self.name = name
        self.start_confidence = confidence
        self.confidence = self.start_confidence
        self.cash = cash
        self. quantitiy_good = quantitiy_good
        self.total_value = float(cash)
        self.last_total_value = self.total_value
        self.transaction_his_quantity = []
        self.transaction_his_price = []
        self.last_transaction = False

# the prediction returns a value defined by the variance and confidence values.
# if positive, the value indicates the price of a good is expected to increase.
# if negitive the price of a good is expected to decrease.

    def prediction(self):
        future = random.randint(Trader.variance_min, Trader.variance_max)
        return future + self.confidence

# the decide function takes a prediction and makes a decision to buy or sell.
# price is passed to calcuate quantitiy_good for buying.

    def decide(self, prediction, price):
        if self.last_transaction:
            amount_to_sell = self.sell(self.quantitiy_good, price)
            self.transaction_his_quantity.append(f'sell {amount_to_sell}')
            self.transaction_his_price.append(price)
            self.last_transaction = False
            return -amount_to_sell

        else:
            amount_to_buy = self.buy(int(self.cash/price), price)
            self.transaction_his_quantity.append(f'buy {amount_to_buy}')
            self.transaction_his_price.append(price)
            self.last_transaction = True
            return amount_to_buy
        if prediction > 0 and self.cash > 0:
            amount_to_buy = self.buy(int(self.cash/price), price)
            self.transaction_his_quantity.append(f'buy {amount_to_buy}')
            self.transaction_his_price.append(price)
            return amount_to_buy
        elif prediction < 0 and self.quantitiy_good > 0:
            amount_to_sell = self.sell(self.quantitiy_good, price)
            self.transaction_his_quantity.append(f'sell {amount_to_sell}')
            self.transaction_his_price.append(price)
            return -amount_to_sell
        elif prediction == 0:
            self.transaction_his_quantity.append(f'holding {0}')
            self.transaction_his_price.append(0)
            self.hold()
            return 0

# the update_total_value function is updating values to update confidence.

    def update_total_value(self, good_price):
        self.last_total_value = self.total_value
        self.total_value = float(self.cash) + \
            float(self.quantitiy_good * good_price)

# updating confidence values based on total value

    def update_confidence(self):
        if self.total_value == self.last_total_value:
            pass
        elif self.total_value > self.last_total_value:
            if self.confidence < Trader.confidence_max:
                self.confidence = self.confidence + Trader.confidence_step
            elif self.confidence >= Trader.confidence_max:
                self.confidence = Trader.confidence_max
        elif self.total_value < self.last_total_value:
            if self.confidence > Trader.confidence_min:
                self.confidence = self.confidence - Trader.confidence_step
            elif self.confidence <= Trader.confidence_min:
                self.confidence = Trader.confidence_min

# the return value for buy is to be passed to the market buy function

    def buy(self, quantity, price):
        self.cash = self.cash - quantity * price
        self.quantitiy_good = self.quantitiy_good + quantity
        return quantity

# the return value for sell is to be passed to the market sell function

    def sell(self, quantity, price):
        self.cash = self.cash + quantity * price
        self.quantitiy_good = self.quantitiy_good - quantity
        return quantity

# hold is a filler function, if some behavior wants to be added when holding.

    def hold(self):
        pass

# the market is the place that traders trade.
# the transacton effect is used to controll the change in price as a good is
# bought or sold.


class Market:
    def __init__(self, good, start_price, transaction_effect):
        self.good_type = good
        self.price = start_price
        self.last_price = start_price
        self.transaction_effect = transaction_effect
        self.traders = []

    def get_price(self):
        return float(self.price)

    def update_price_sell(self, quantity):
        self.last_price = self.price
        print(quantity)
        self.price = self.price - quantity * self.transaction_effect

    def update_price_buy(self, quantity):
        if type(quantity) != int:
            quantity = 0
        self.last_price = self.price
        self.price = self.price + quantity * self.transaction_effect

    def add_trader(self, trader):
        self.traders.append(trader)

# ask for markets


def get_markets():
    quantity_markets = int(input('How many markets would you like?'
                                 f'you may have {len(TYPES_OF_GOODS)}'))
    return quantity_markets

# ask user for traders


def get_traders():
    quantity_traders = int(input(
        'How many traders would you like in this market?'))
    return quantity_traders * 2

# helper function to randomly detirmeine good type


def generate_good():
    good_types = TYPES_OF_GOODS
    good_type = good_types.pop()
    return good_type

# consolidating data into a dict


def collect_data(traders):
    data_list = []
    for trader in traders:
        data = {trader.name + ' quantity': trader.transaction_his_quantity,
                trader.name + ' price': trader.transaction_his_price}
        data_list.append(data)
    return data_list


def name_generator(quantity):
    names = set()

    def first_name():
        first_names = ['Bill', 'Joe', 'Fred', 'Smith', 'Rob', 'Mo', 'Bob',
                       'Monty', 'Isac', 'Shep', 'Curly', 'Erik', 'Lief', 'Mat',
                       'Mike', 'Bruce', 'Creig', 'Jane', 'Jill', 'Mary']
        pick = random.randint(0, len(first_names)-1)
        return first_names[pick]

    def last_name():
        last_names = ['Smith', 'Door', 'Baker', 'Python', 'Erikson', 'Leifson',
                      'Quark', 'Hobb', 'Knave', 'Savano', 'Cheveron', 'Mink',
                      'Fox', 'Moss', ]
        pick = random.randint(0, len(last_names)-1)
        return last_names[pick]

    while len(names) < quantity:
        names.add(first_name() + ' ' + last_name())
    return names


def add_traders(quantity):
    trade_names = name_generator(quantity)
    traders = []
    for trader in range(quantity):
        trader = Trader(trade_names.pop(), 0,
                        random.randint(START_CASH_MIN, START_CASH_MAX),
                        random.randint(START_GOODS_MIN, START_GOODS_MAX))
        traders.append(trader)
    return traders


def create_market(quantity, trader_quantity):
    markets = set()
    for market in range(quantity):
        market = Market(generate_good(), START_PRICE, TRANSACTION_EFFECT)
        market.add_trader(add_traders(trader_quantity))
        markets.add(market)
    return markets


print('This is a market simulator')
market = Market(generate_good(), START_PRICE, TRANSACTION_EFFECT)
traders = add_traders(get_traders())
for trader in traders:
    market.add_trader(traders.pop())
days = int(input('How many days of trading do you want?'))
for day in range(days):
    for trader in market.traders:
        market.update_price_buy(trader.decide(trader.prediction(),
                                market.get_price()))
        trader.update_total_value(market.get_price())
        trader.update_confidence()
output = collect_data(market.traders)

data = pandas.DataFrame(output)
print(data)
data.to_excel('SimData.xlsx', index=False)
