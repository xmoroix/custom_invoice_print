from odoo import models, _
from collections import defaultdict

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_bundled_lines(self):
        self.ensure_one()
        bundled = defaultdict(float)
        
        lines_to_report = self._get_order_lines_to_report()
        for line in lines_to_report:
            # Skip lines without products or with display_type (section/note lines)
            if not line.product_id or line.display_type:
                continue
            
            # Get category name with proper error handling
            category = 'Other'
            if line.product_id.categ_id:
                category = line.product_id.categ_id.name or 'Other'
            
            # Simple bundling by category only (no tax differentiation)
            bundled[category] += line.price_subtotal
        
        return [
            {
                'name': name, 
                'total': total
            } 
            for name, total in bundled.items()
        ]

    def amount_to_words(self, amount):
        """Convert amount to words in current language"""
        try:
            # Get language from multiple sources
            lang = self.env.context.get('lang', 'en_US')
            
            # Check user language if context doesn't have it
            if not lang or lang == 'en_US':
                if self.env.user.lang:
                    lang = self.env.user.lang
            
            # Force our custom conversion for French
            if lang and lang.startswith('fr'):
                return self._amount_to_words_fr(amount)
            else:
                return self._amount_to_words_en(amount)
                
        except Exception:
            # Fallback if conversion fails
            return f"{amount:.2f} {self.currency_id.name or 'USD'}"

    def _amount_to_words_en(self, amount):
        """Convert amount to English words"""
        try:
            # Simple number-to-words conversion for basic amounts
            currency_name = self.currency_id.name or 'USD'
            
            dollars = int(amount)
            cents = int((amount - dollars) * 100)
            
            # Basic conversion for common numbers
            dollars_text = self._convert_number_to_words_en(dollars)
            cents_text = self._convert_number_to_words_en(cents)
            
            currency_word = 'Dollars' if currency_name == 'USD' else currency_name
            
            if cents == 0:
                return f"{dollars_text} {currency_word} Only"
            else:
                return f"{dollars_text} {currency_word} and {cents_text} Cents"
        except Exception:
            # Fallback if conversion fails
            return f"{amount:.2f} {self.currency_id.name or 'USD'}"

    def _amount_to_words_fr(self, amount):
        """Convert amount to French words"""
        try:
            currency_name = self.currency_id.name or 'USD'
            
            dollars = int(amount)
            cents = int((amount - dollars) * 100)
            
            dollars_text = self._convert_number_to_words_fr(dollars)
            cents_text = self._convert_number_to_words_fr(cents)
            
            # Use proper French currency names
            if currency_name == 'DZD':
                currency_word = 'Dinar'
            elif currency_name == 'USD':
                currency_word = 'Dollars'
            else:
                currency_word = currency_name
            
            if cents == 0:
                return f"{dollars_text} {currency_word}"
            else:
                return f"{dollars_text} {currency_word} et {cents_text} Centimes"
        except Exception:
            return f"{amount:.2f} {self.currency_id.name or 'USD'}"

    def _convert_number_to_words_en(self, number):
        """Enhanced English number to words converter"""
        if number == 0:
            return "Zero"
        
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", 
                "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                "Seventeen", "Eighteen", "Nineteen"]
        
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        
        if number < 20:
            return ones[number]
        elif number < 100:
            return tens[number // 10] + ("" if number % 10 == 0 else "-" + ones[number % 10])
        elif number < 1000:
            hundreds = number // 100
            remainder = number % 100
            result = ones[hundreds] + " Hundred"
            if remainder > 0:
                result += " " + self._convert_number_to_words_en(remainder)
            return result
        elif number < 1000000:
            thousands = number // 1000
            remainder = number % 1000
            result = self._convert_number_to_words_en(thousands) + " Thousand"
            if remainder > 0:
                result += " " + self._convert_number_to_words_en(remainder)
            return result
        elif number < 1000000000:
            millions = number // 1000000
            remainder = number % 1000000
            result = self._convert_number_to_words_en(millions) + " Million"
            if remainder > 0:
                result += " " + self._convert_number_to_words_en(remainder)
            return result
        else:
            return f"{number}"  # For extremely large numbers

    def _convert_number_to_words_fr(self, number):
        """Enhanced French number to words converter"""
        if number == 0:
            return "Zéro"
        
        ones = ["", "Un", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit", "Neuf", 
                "Dix", "Onze", "Douze", "Treize", "Quatorze", "Quinze", "Seize", 
                "Dix-sept", "Dix-huit", "Dix-neuf"]
        
        tens = ["", "", "Vingt", "Trente", "Quarante", "Cinquante", "Soixante", "Soixante-dix", "Quatre-vingts", "Quatre-vingt-dix"]
        
        if number < 20:
            return ones[number]
        elif number < 100:
            if number < 70:
                return tens[number // 10] + ("" if number % 10 == 0 else "-" + ones[number % 10])
            elif number < 80:
                return "Soixante-" + ones[number - 60]
            elif number < 90:
                return "Quatre-vingt" + ("" if number == 80 else "-" + ones[number - 80])
            else:
                return "Quatre-vingt-" + ones[number - 80]
        elif number < 1000:
            hundreds = number // 100
            remainder = number % 100
            result = ""
            if hundreds == 1:
                result = "Cent"
            else:
                result = ones[hundreds] + " Cent"
            if remainder > 0:
                result += " " + self._convert_number_to_words_fr(remainder)
            return result
        elif number < 1000000:
            thousands = number // 1000
            remainder = number % 1000
            result = ""
            if thousands == 1:
                result = "Mille"
            else:
                result = self._convert_number_to_words_fr(thousands) + " Mille"
            if remainder > 0:
                result += " " + self._convert_number_to_words_fr(remainder)
            return result
        elif number < 1000000000:
            millions = number // 1000000
            remainder = number % 1000000
            result = ""
            if millions == 1:
                result = "Un Million"
            else:
                result = self._convert_number_to_words_fr(millions) + " Millions"
            if remainder > 0:
                result += " " + self._convert_number_to_words_fr(remainder)
            return result
        else:
            return f"{number}"  # For extremely large numbers
