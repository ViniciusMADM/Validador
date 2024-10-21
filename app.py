from flask import Flask, request, jsonify

app = Flask(__name__)


def numerarCPF(cpf):
    return [int(a) for a in cpf]


def quantidade(cpf):
    return len(cpf) == 11


def primeiro_digito(cpf_numerado):
    acumulador = sum(cpf_numerado[i] * (10 - i) for i in range(9))
    acumulador = (acumulador * 10) % 11
    return cpf_numerado[9] == (0 if acumulador == 10 else acumulador)


def segundo_digito(cpf_numerado):
    acumulador = sum(cpf_numerado[i] * (11 - i) for i in range(10))
    acumulador = (acumulador * 10) % 11
    return cpf_numerado[10] == (0 if acumulador == 10 else acumulador)


def formatar_cpf(cpf):
    """Formata o CPF no padrão xxx.xxx.xxx-xx."""
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


@app.route('/validador_cpf', methods=['POST'])
def validador_cpf():
    data = request.json

    # Verificar se "cpf" está presente na requisição
    if 'cpf' not in data:
        return jsonify({"valid": False, "message": "CPF inválido"}), 400

    # Limpar CPF removendo pontos e traços
    cpf = str(data.get("cpf")).replace('-', '').replace('.', '').replace('_','')

    if quantidade(cpf):
        cpf_numerado = numerarCPF(cpf)

        # Verificações de dígitos
        primeiro = primeiro_digito(cpf_numerado)
        segundo = segundo_digito(cpf_numerado)

        # Log para verificar valores calculados
        print(f"CPF Numerado: {cpf_numerado}")
        print(f"Primeiro Dígito Calculado: {primeiro}")
        print(f"Segundo Dígito Calculado: {segundo}")

        if primeiro and segundo:
            cpf_formatado = formatar_cpf(cpf)  # Formata o CPF
            return jsonify({"validação": True, "cpf": cpf_formatado}), 200
        else:
            return jsonify({"validação": False}), 200
    else:
        return jsonify({"validação": False}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000) 