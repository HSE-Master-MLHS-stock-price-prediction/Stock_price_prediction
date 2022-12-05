import yfinance as yf
from tqdm import tqdm
from math import ceil


class SimplePortfolioExperiment:
    def __init__(self,
                 historical_data=None,
                 start_capital=5000,
                 stock_start_partial=1.0,
                 days_per_action=30,
                 days_to_add_money=30,
                 money_to_add=500,
                 window_size=30):

        assert stock_start_partial >= 0.0 and stock_start_partial <= 1.0

        self.start_capital = start_capital
        self.stock_start_partial = stock_start_partial
        self.days_per_action = days_per_action
        self.days_to_add_money = days_to_add_money
        self.money_to_add = money_to_add

        # If no data is provided, we will use the Yandex ticker as a
        # default one.

        self.historical_data = historical_data
        if historical_data is None:
            self.historical_data = list(yf.Ticker('YNDX').history(period="max")['Close'][1412:-250])
        else:
            self.historical_data = historical_data

        self.number_of_stocks = int(self.start_capital * stock_start_partial // self.historical_data[0])
        self.free_money = self.start_capital - self.number_of_stocks * self.historical_data[0]

        self.history_capital = [self.free_money + self.number_of_stocks * self.historical_data[0]]
        self.history_free_money = [self.free_money]
        self.histiry_stocks = [self.number_of_stocks]

        self.window_size = window_size

        self.version = '0.0.1'

    def buy_papers(self, number_of_papers, ind, partial_operation=False):
        '''
        Try to make a purchase of papers.

        :param number_of_papers: number of papers to buy
        :param ind: moment of time purchase is made (index of a time series)
        :param partial_operation: if a partial operation (buying less than wanted) is allowed
        :return: True if purchase has been carried (and params were updated), else False
        '''
        current_price = self.historical_data[ind]
        need_money = current_price * number_of_papers  # Money required to make a purchase
        if need_money > self.free_money:
            if partial_operation:
                papers = int(self.free_money // current_price)  # Assuming we can only buy
                # integer amount of papers
                self.free_money -= papers * current_price
                self.number_of_stocks += papers
                return True
            else:
                return False
        else:
            self.number_of_stocks += number_of_papers
            self.free_money -= need_money
            return True

    def buy_stocks_per_money(self, money, ind, partial_operation=False):
        '''
        Spend `money` to buy as many papers as you possibly can.

        :param money: money wishing to spend on papers.
        :param ind: moment of time purchase is made (index of a time series)
        :param partial_operation: if a partial operation (buying less than wanted) is allowed
        :return: True if purchase has been carried (and params were updated), else False
        '''
        current_price = self.historical_data[ind]
        if self.free_money < money:
            # If you requested to spend more money than you have
            if partial_operation:
                papers = int(self.free_money // current_price)  # Assuming we can only buy
                # integer amount of papers
                self.free_money -= papers * current_price
                self.number_of_stocks += papers
                return True
            else:
                return False
        papers = int(money // current_price)
        self.free_money -= papers * current_price
        self.number_of_stocks += papers
        return True

    def buy_partial(self, partial, ind, partial_operation=False):
        '''
        Purchase papers based on the current amount of papers you have.

        :param partial: ratio you want to purchase
        :param ind: moment of time purchase is made (index of a time series)
        :param partial_operation: if a partial operation (buying less than wanted) is allowed
        :return: True if purchase has been carried (and params were updated), else False
        '''
        assert abs(partial) <= 1 and partial > 0
        papers = int(self.number_of_stocks * partial)
        possible_to_buy = int(self.free_money // self.historical_data[ind])
        if papers > possible_to_buy:
            if partial_operation:
                return self.buy_papers(possible_to_buy, ind, True)
            else:
                return False
        return self.buy_papers(papers, ind, True)

    def sell_papers(self, number_of_papers, ind, partial_operation=False):
        '''
        Sell selected number of papers.

        :param number_of_papers: number of papers to sell.
        :param ind: moment of time selling is made (index of a time series)
        :param partial_operation: if a partial operation (selling less than wanted) is allowed
        :return: True if papers were sold successfully (and params were updated), else False
        '''
        current_price = self.historical_data[ind]
        if self.number_of_stocks < number_of_papers:
            if partial_operation:
                money_to_add = self.number_of_stocks * current_price
                self.number_of_stocks = 0
                self.free_money += money_to_add
                return True
            else:
                return False
        else:
            money_to_add = number_of_papers * current_price
            self.number_of_stocks -= number_of_papers
            self.free_money += money_to_add
            return True

    def sell_stocks_per_money(self, money, ind, partial_operation=False):
        '''
        Sell the amount of stocks necessary to get the money amount provided.

        :param money: the money you want to get
        :param ind: moment of time selling is made (index of a time series)
        :param partial_operation: if a partial operation (selling less than wanted) is allowed
        :return: True if papers were sold successfully (and params were updated), else False
        '''
        current_price = self.historical_data[ind]
        papers_to_cell = ceil(money / current_price)  # Ceil since if we get less it is not value

        return self.sell_papers(papers_to_cell, ind, partial_operation)

    def sell_partial_papers(self, partial, ind, partial_operation=False):
        '''
        Purchase papers based on the current amount of papers you have.

        :param partial: ratio you want to sell
        :param ind: moment of time purchase is made (index of a time series)
        :param partial_operation: if a partial operation (selling less than wanted) is allowed
        :return: True if purchase has been carried (and params were updated), else False
        '''
        assert abs(partial) <= 1 and partial > 0
        papers = int(self.number_of_stocks * partial)
        return self.sell_papers(papers, ind, partial_operation)

    def start_experiment(self):
        print('Start portfolio experiment.')
        for i in tqdm(range(1, len(self.historical_data))):
            if i % self.days_to_add_money == 0:
                self.free_money += self.money_to_add
            if i % self.days_per_action == 0 and self.window_size <= i:
                self.make_action(i)
            self.history_capital.append(self.free_money + self.number_of_stocks * self.historical_data[i])
            self.history_free_money.append(self.free_money)
            self.histiry_stocks.append(self.number_of_stocks)

    def make_action(self, ind):
        pass
