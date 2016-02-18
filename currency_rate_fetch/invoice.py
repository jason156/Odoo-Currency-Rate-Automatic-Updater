from openerp.osv import fields, osv
from openerp import api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp
import urllib2

class res_currency(osv.osv):
    
    _inherit = 'res.currency'
    
    
    def get_latest_rates(self, source_currency, target_currency):
        api_url = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=%s%s=X"
        query_url = api_url % (source_currency, target_currency)
        currency_csv = urllib2.urlopen(query_url).read()
        currency_rate = currency_csv.split(",")[1]
        if currency_rate == "0.00":
            print("Error...Please check your currency codes")
        return float(currency_rate)
    
    def do_run_scheduler(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        currencies = ['USD','INR','SGD','EUR']
        for currency in currencies:
            rate = self.get_latest_rates('AED', currency)
            currency_id = self.search(cr,uid, [('name','=',currency)])[0]
            self.pool.get('res.currency.rate').create(cr, uid, {
                                                            'name': fields.datetime.now(),
                                                            'rate': rate,
                                                            'currency_id': currency_id
                                                                })
        return True
