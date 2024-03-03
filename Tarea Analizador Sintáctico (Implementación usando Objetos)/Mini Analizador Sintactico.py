import re

class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.reservadas = {'if': 19, 'while': 20, 'return': 21, 'else': 22, 'int': 4, 'float': 4, 'void': 4}
        self.patron_identificador = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')
        self.patron_entero = re.compile(r'\d+')
        self.patron_real = re.compile(r'\d+\.\d+')
        self.patron_operador = re.compile(r'[+\-*/=!<>]|&&|\|\|')
        self.patron_parentesis = re.compile(r'[()]')
        self.patron_llave = re.compile(r'[{}]')
        self.patron_punto_y_coma = re.compile(r';')
        self.patron_coma = re.compile(r',')
        self.patron_igual = re.compile(r'=')
        self.posicion = 0

    def analizar(self):
        while self.posicion < len(self.codigo_fuente):
            self.tokenizar()

    def tokenizar(self):
        if self.codigo_fuente[self.posicion].isspace():
            self.posicion += 1
        elif self.codigo_fuente[self.posicion].isalpha():
            match = self.patron_identificador.match(self.codigo_fuente, self.posicion)
            if match:
                lexema = match.group(0)
                tipo = self.reservadas.get(lexema, 0)
                self.tokens.append(('identificador', tipo))
                self.posicion = match.end()
            else:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")
        elif self.codigo_fuente[self.posicion].isdigit():
            match_entero = self.patron_entero.match(self.codigo_fuente, self.posicion)
            match_real = self.patron_real.match(self.codigo_fuente, self.posicion)
            if match_real and '.' in match_real.group(0):
                self.tokens.append(('real', 2))
                self.posicion = match_real.end()
            elif match_entero:
                self.tokens.append(('entero', 1))
                self.posicion = match_entero.end()
            else:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")
        else:
            match = None
            for patron, tipo in [(self.patron_operador, 'operador'), (self.patron_parentesis, 'parentesis'), 
                                 (self.patron_llave, 'llave'), (self.patron_punto_y_coma, 'punto_y_coma'),
                                 (self.patron_coma, 'coma'), (self.patron_igual, 'igual')]:
                match = patron.match(self.codigo_fuente, self.posicion)
                if match:
                    self.tokens.append((tipo, match.group(0)))
                    self.posicion = match.end()
                    break
            if not match:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")

    def obtener_tokens(self):
        return self.tokens

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def analizar(self):
        try:
            self.expresion()
            print("Análisis sintáctico exitoso.")
        except Exception as e:
            print(f"Error sintáctico: {e}")

    def expresion(self):
        self.termino()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion][1] in ('+', '-'):
            self.match(('operador', '+') if self.tokens[self.posicion][1] == '+' else ('operador', '-'))
            self.termino()

    def termino(self):
        self.factor()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion][1] in ('*', '/'):
            self.match(('operador', '*') if self.tokens[self.posicion][1] == '*' else ('operador', '/'))
            self.factor()

    def factor(self):
        if self.posicion < len(self.tokens) and self.tokens[self.posicion][0] in ('entero', 'real'):
            self.match((self.tokens[self.posicion][0], None))
        elif self.posicion < len(self.tokens) and self.tokens[self.posicion][1] == '(':
            self.match(('parentesis', '('))
            self.expresion()
            self.match(('parentesis', ')'))
        else:
            raise Exception("Error en el factor")



    def match(self, esperado):
        if self.posicion < len(self.tokens) and self.tokens[self.posicion] == esperado:
            self.posicion += 1
        else:
            raise Exception(f"Se esperaba {esperado}, pero se encontró {self.tokens[self.posicion]}")

codigo_fuente = """
int main() {
    int a = 10;
    float b = 3.14;
    if (a > 5 && b < 4.0) {
        return int(a + b);
    } else {
        return int(a * b);
    }
}
"""


analizador_lexico = AnalizadorLexico(codigo_fuente)
analizador_lexico.analizar()
tokens_resultantes = analizador_lexico.obtener_tokens()

analizador_sintactico = AnalizadorSintactico(tokens_resultantes)
analizador_sintactico.analizar()
