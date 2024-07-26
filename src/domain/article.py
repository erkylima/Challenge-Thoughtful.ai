class NewsArticle:
    def __init__(self, title, date, description, image_filename):
        self.title = title
        self.date = date
        self.description = description
        self.search_term_count = 0        
        self.image_filename = image_filename
    
    def analyze_content(self, search_term):
        self.search_term_count = self.title.count(search_term) + (self.description or "").count(search_term)
        self.contais_money = self._contains_money()
    
    def _contains_money(self):
        import re
        patterns = [
            r'\$\s?d{1,3}(\.\d{3})*(,\d{1,2})?',
            r'\d+\s?dollars',
            r'\d+\s?USD'
        ]
        for pattern in patterns:
            if re.search(pattern, self.title, re.IGNORECASE) or re.search(pattern, self.description or '', re.IGNORECASE):
                return True
        return False