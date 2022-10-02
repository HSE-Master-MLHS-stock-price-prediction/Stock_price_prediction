import yfinance as yf

class SimplePortfolioExperiment:
    
    def __init__(self, 
                 historical_data = None,
                 start_capital = 5000, 
                 stock_start_partial = 1.0, 
                 days_per_action = 30, 
                 days_to_add_money = 30, 
                 money_to_add = 500, 
                 window_size = 30):
        
        assert stock_start_partial >= 0.0 and stock_start_partial <= 1.0
        
        self.start_capital = start_capital
        self.stock_start_partial = stock_start_partial
        self.days_per_action = days_per_action
        self.days_to_add_money = days_to_add_money
        self.money_to_add = money_to_add
        
        self.historical_data = None
        if historical_data is None:
            self.historical_data = list(yf.Ticker('YNDX').history(period="max")['Close'][1412:-250])
        else:
            self.historical_data = historical_data
        
        self.number_of_stocks = int(start_capital*stock_start_partial//historical_data[0])
        self.free_money = start_capital - number_of_stocks*historical_data[0]
        
        self.history_capital = [self.free_money + self.number_of_stocks*historical_data[0]]
        self.history_free_money = [self.free_money]
        self.histiry_stocks = [self.number_of_stocks]
        
        self.window_size = window_size
        
    def buy_papers(self, number_of_papers, ind, partial_operation = False):
        need_money = self.historical_data[ind] * number_of_papers
        if need_money > self.free_money:
            if partial_operation:
                papers = int(self.free_money//self.historical_data[ind])
                self.free_money -= papers*self.historical_data[ind]
                self.number_of_papers += papers
                return True
            else:
                return False
        self.number_of_papers += papers
        self.free_money -= need_money
        return True
    
    def buy_stocks_per_money(self, money, ind, partial_operation = False):
        if self.free_money < money:
            if self.partial_operation:
                papers = int(self.free_money//self.historical_data[ind])
                self.free_money -= papers*self.historical_data[ind]
                self.number_of_papers += papers
                return True
            else:
                return False
        papers = int(money//self.historical_data[ind])
        self.free_money -= papers*self.historical_data[ind]
        self.number_of_papers += papers
        return True
    
    def buy_partial(self, partial, ind, partial_operation = False):
        assert abs(partial) <= 1 and partial > 0
        papers = int(self.number_of_papers * partial)
        possible_to_buy = int(self.free_money//self.historical_data[ind])
        if papers > possible_to_buy:
            if partial_operation:
                return self.buy_papers(possible_to_buy, ind, True)
            else:
                return False
        return self.buy_papers(papers, ind, True)
        
    def sell_papers(self, number_of_papers, ind, partial_operation = False):
        if self.number_of_stocks < number_of_papers:
            if partial_operation:
                money_to_add = self.historical_data[ind]*self.number_of_stocks
                self.number_of_papers = 0
                self.free_money += money_to_add
            else:
                return False
        money_to_add = self.historical_data[ind]*number_of_papers
        self.number_of_papers -= number_of_papers
        self.free_money += money_to_add
        return True
    
    def sell_stocks_per_money(self, money, ind, partial_operation = False):
        if money > self.free_money:
            if partial_operation:
                number_of_papers = int(self.free_money//self.historical_data[ind])
                return self.sell_papers(number_of_papers, ind, True)
            else:
                return True
        number_of_papers = int(money//self.historical_data[ind])
        return self.sell_papers(number_of_papers, ind, partial_operation)
    
    def sell_partial_papers(self, partial, ind, partial_operation = False):
        assert abs(partial) <= 1 and partial > 0
        papers = int(self.number_of_stocks*partial)
        return self.sell_papers(papers, ind, partial_operation)
    
    def start_experiment(self):
        for i in range(1, len(self.historical_data)):
            if i%self.days_to_add_money == 0:
                self.free_money += self.money_to_add
            if i%self.days_per_action == 0:
                self.make_action()
            self.history_capital = [self.free_money + self.number_of_stocks*historical_data[i]]
                
    def make_action(self):
        pass