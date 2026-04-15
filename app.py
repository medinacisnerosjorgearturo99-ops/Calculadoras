from flask import Flask, render_template, request, jsonify
import re
import logging
import os

# --- CONFIGURACIÓN DE LOGS PARA PRODUCCIÓN ---
# Crea la carpeta automáticamente si no existe en el contenedor/servidor
if not os.path.exists('logs'):
    os.makedirs('logs')

# Define cómo y dónde se guardará el registro
logging.basicConfig(
    filename='logs/calculadora.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression', '')
    mode = data.get('mode', 'decimal')

    # Registramos qué intenta hacer el usuario
    logging.info(f"Operacion solicitada: '{expression}' en modo [{mode.upper()}]")

    try:
        if mode == 'decimal':
            allowed = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed):
                logging.warning(f"Intento fallido (Caracteres invalidos): {expression}")
                return jsonify({'error': 'Caracteres inválidos'})
            
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            logging.info(f"Resultado exitoso: {result}")
            return jsonify({'result': str(result)})
            
        elif mode == 'binario':
            allowed_bin = set("01+-*/&|^() ")
            if not set(expression).issubset(allowed_bin):
                logging.warning(f"Intento fallido (No binario): {expression}")
                return jsonify({'error': 'Solo 0, 1 y operadores'})
                
            py_expr = re.sub(r'\b([01]+)\b', r'0b\1', expression)
            result = eval(py_expr)
            res_str = bin(result)[3:] if result < 0 else bin(result)[2:]
            final_res = ('-' if result < 0 else '') + res_str
            
            logging.info(f"Resultado exitoso: {final_res}")
            return jsonify({'result': final_res})
            
        elif mode == 'hexadecimal':
            allowed_hex = set("0123456789abcdefABCDEF+-*/&|^() ")
            if not set(expression).issubset(allowed_hex):
                logging.warning(f"Intento fallido (No hex): {expression}")
                return jsonify({'error': 'Solo 0-9, A-F y operadores'})
                
            py_expr = re.sub(r'\b([0-9a-fA-F]+)\b', r'0x\1', expression)
            result = eval(py_expr)
            res_str = hex(result)[3:].upper() if result < 0 else hex(result)[2:].upper()
            final_res = ('-' if result < 0 else '') + res_str
            
            logging.info(f"Resultado exitoso: {final_res}")
            return jsonify({'result': final_res})
            
        elif mode == 'octal':
            allowed_oct = set("01234567+-*/&|^() ")
            if not set(expression).issubset(allowed_oct):
                logging.warning(f"Intento fallido (No octal): {expression}")
                return jsonify({'error': 'Solo 0-7 y operadores'})
                
            py_expr = re.sub(r'\b([0-7]+)\b', r'0o\1', expression)
            result = eval(py_expr)
            res_str = oct(result)[3:] if result < 0 else oct(result)[2:]
            final_res = ('-' if result < 0 else '') + res_str
            
            logging.info(f"Resultado exitoso: {final_res}")
            return jsonify({'result': final_res})
                
    except ZeroDivisionError:
        logging.error(f"Error matematico: Division por cero en '{expression}'")
        return jsonify({'error': 'Div. por 0'})
    except Exception as e:
        logging.error(f"Error de sintaxis al evaluar '{expression}'. Detalle tecnico: {e}")
        return jsonify({'error': 'Sintaxis Error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)