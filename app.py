from flask import Flask, request, jsonify
import logging
import re

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def numerarCPF(cpf: str) -> list[int]:
    return [int(a) for a in cpf]

def primeiro_digito(cpf_numerado: list[int]) -> bool:
    acumulador = sum(cpf_numerado[i] * (10 - i) for i in range(9))
    acumulador = (acumulador * 10) % 11
    return cpf_numerado[9] == (0 if acumulador == 10 else acumulador)

def segundo_digito(cpf_numerado: list[int]) -> bool:
    acumulador = sum(cpf_numerado[i] * (11 - i) for i in range(10))
    acumulador = (acumulador * 10) % 11
    return cpf_numerado[10] == (0 if acumulador == 10 else acumulador)

def formatar_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

@app.route('/validador_cpf', methods=['POST'])
def validador_cpf():
    data = request.json

    if 'cpf' not in data:
        return jsonify({"valid": False, "message": "CPF não fornecido"}), 400

    cpf = re.sub(r'\D', '', str(data.get("cpf")))  # Remove não dígitos

    if len(cpf) == 11:
        cpf_numerado = numerarCPF(cpf)
        primeiro = primeiro_digito(cpf_numerado)
        segundo = segundo_digito(cpf_numerado)

        logging.info(f"Validação iniciada para CPF: {cpf}")

        if primeiro and segundo:
            cpf_formatado = formatar_cpf(cpf)
            return jsonify({"validação": True, "cpf": cpf_formatado}), 200
        else:
            return jsonify({"validação": False}), 200
    else:
        return jsonify({"validação": False}), 200

if __name__ == '__main__':
    app.run(debug=True)
