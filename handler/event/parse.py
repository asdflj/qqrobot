class Parsetext:
    def __init__(self,text):
        self.text = text
        self._parseContent()

    def _parseContent(self):
        lines = self.text.splitlines()
        L = lines[0].split(' ')
        self._command = L[0]
        self._args = L[1:]
        self._content = '\n'.join(lines[1:])
    
    def command(self):
        try:
            if self._command[0] == '/':
                return self._command[1:]
            else:
                return None
        except Exception:
            return None
    
    def args(self):
        return self._args
    
    def content(self):
        return self._content
