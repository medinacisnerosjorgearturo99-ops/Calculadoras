from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression', '')
    mode = data.get('mode', 'decimal')

    try:
        if mode == 'decimal':
            allowed = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed):
                return jsonify({'error': 'Caracteres inválidos'})
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return jsonify({'result': str(result)})
            
        elif mode == 'binario':
            allowed_bin = set("01+-*/&|^() ")
            if not set(expression).issubset(allowed_bin):
                return jsonify({'error': 'Solo 0, 1 y operadores'})
            py_expr = re.sub(r'\b([01]+)\b', r'0b\1', expression)
            result = eval(py_expr)
            res_str = bin(result)[3:] if result < 0 else bin(result)[2:]
            return jsonify({'result': ('-' if result < 0 else '') + res_str})
            
        elif mode == 'hexadecimal':
            # Permite números, letras A-F y operadores
            allowed_hex = set("0123456789abcdefABCDEF+-*/&|^() ")
            if not set(expression).issubset(allowed_hex):
                return jsonify({'error': 'Solo 0-9, A-F y operadores'})
            py_expr = re.sub(r'\b([0-9a-fA-F]+)\b', r'0x\1', expression)
            result = eval(py_expr)
            res_str = hex(result)[3:].upper() if result < 0 else hex(result)[2:].upper()
            return jsonify({'result': ('-' if result < 0 else '') + res_str})
            
        elif mode == 'octal':
            # Permite solo del 0 al 7
            allowed_oct = set("01234567+-*/&|^() ")
            if not set(expression).issubset(allowed_oct):
                return jsonify({'error': 'Solo 0-7 y operadores'})
            py_expr = re.sub(r'\b([0-7]+)\b', r'0o\1', expression)
            result = eval(py_expr)
            res_str = oct(result)[3:] if result < 0 else oct(result)[2:]
            return jsonify({'result': ('-' if result < 0 else '') + res_str})
                
    except ZeroDivisionError:
        return jsonify({'error': 'Div. por 0'})
    except Exception:
        return jsonify({'error': 'Sintaxis Error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)