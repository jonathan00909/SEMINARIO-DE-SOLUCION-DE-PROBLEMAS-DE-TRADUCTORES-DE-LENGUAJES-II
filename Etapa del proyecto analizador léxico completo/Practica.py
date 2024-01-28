import re
import tkinter as tk

def analizador_lexico(expresion):
    # Definir patrones para identificadores, números enteros y reales, operadores, paréntesis, llaves y punto y coma
    patron_identificador = r'[a-zA-Z_][a-zA-Z0-9_]*'
    patron_entero = r'\d+'
    patron_real = r'\d+\.\d+'
    patron_operador = r'(<=|>=|!=|==|&&|\|\||[+\-*/=<>!;])'
    patron_parentesis_llaves = r'[()\{\}]'
    patron_palabras_reservadas = r'(if|while|return|else|int|float)'

    # Combinar patrones en una expresión regular total
    patron_total = f'({patron_identificador})|({patron_entero})|({patron_real})|({patron_operador})|({patron_parentesis_llaves})|({patron_palabras_reservadas})|(\S)'

    # Encontrar todos los tokens en la expresión
    tokens = re.findall(patron_total, expresion)

    # Procesar los tokens y construir el resultado
    resultado = ""
    for token in tokens:
        for i in range(len(token)):
            if token[i]:
                tipo_dato = obtener_tipo_dato(i, token[i])
                resultado += f'{token[i]} tipo de dato: {tipo_dato}\n'
                break

    return resultado

def obtener_tipo_dato(indice, valor):
    if valor in ['if', 'while', 'return', 'else', 'int', 'float']:
        return 'palabra reservada'
    elif valor in ['(', ')']:
        return 'paréntesis'

    tipos = ['identificador', 'número entero', 'número real', 'operador', 'paréntesis/llaves', 'desconocido']
    tipo = tipos[indice]
    
    # Añadir descripciones adicionales para algunos tipos
    if tipo == 'operador':
        tipo += f' ({obtener_tipo_operador(valor)})'

    return tipo


def obtener_tipo_operador(operador):
    if operador == '+':
        return 'suma'
    elif operador == '-':
        return 'resta'
    elif operador == '*':
        return 'multiplicación'
    elif operador == '/':
        return 'división'
    elif operador == '=':
        return 'asignación'
    elif operador == '<':
        return 'menor que'
    elif operador == '>':
        return 'mayor que'
    elif operador == '<=':
        return 'menor o igual que'
    elif operador == '>=':
        return 'mayor o igual que'
    elif operador == '!=':
        return 'diferente de'
    elif operador == '==':
        return 'igual a'
    elif operador == '&&':
        return 'AND lógico'
    elif operador == '||':
        return 'OR lógico'
    elif operador == '!':
        return 'NOT lógico'
    elif operador == ';':
        return 'punto y coma'
    else:
        return 'desconocido'

def analizar_expresion():
    expresion = entrada.get()
    resultado = analizador_lexico(expresion)
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    resultado_text.insert(tk.END, resultado)
    resultado_text.config(state=tk.DISABLED)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador Léxico")

# Crear elementos de la interfaz
etiqueta = tk.Label(ventana, text="Ingrese la expresión:")
etiqueta.pack(pady=10)

entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=10)

boton_analizar = tk.Button(ventana, text="Analizar", command=analizar_expresion)
boton_analizar.pack(pady=10)

resultado_text = tk.Text(ventana, height=10, width=40, state=tk.DISABLED)
resultado_text.pack(pady=10)

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
