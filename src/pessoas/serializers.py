# people_uploader/serializers.py
from rest_framework import serializers
import openpyxl
from datetime import datetime
from .models import Pessoa

   

class ExcelUploadSerializer(serializers.Serializer):
    """
        Serializer para upload de arquivos Excel.

        Este serializer é utilizado para validar e processar arquivos Excel carregados na API, extraindo
        informações das pessoas e aplicando regras de negócios específicas antes de armazená-las no banco de dados.

        Atributos:
            file (FileField): O campo de upload de arquivo para o arquivo Excel.

        Métodos:
            validate_file(file):
                Valida e processa o arquivo Excel, extraindo dados das linhas da planilha.
                - Verifica a data de nascimento e calcula a idade de cada pessoa.
                - Ignora pessoas menores de 18 anos.
                - Calcula o valor para cada pessoa ativa com base na idade.
                - Armazena as informações no banco de dados para pessoas ativas.
                - Retorna uma lista de dicionários contendo as informações das pessoas ativas.

            to_representation(validated_data):
                Formata a resposta final, retornando as informações das pessoas ativas processadas.
    """
    
    file = serializers.FileField()

    def validate_file(self, file):
        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            people = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                nome, email, data_nascimento, ativo = row
                
                if isinstance(data_nascimento, datetime):
                    data_nascimento = data_nascimento.date()
                elif isinstance(data_nascimento, str):
                    data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()

                idade = (datetime.today().date() - data_nascimento).days // 365
                
                if idade < 18:
                    continue              
                if idade < 21:
                    valor = 100.00
                elif idade < 60:
                    valor = 150.00
                else:
                    valor = 200.00

                if ativo:
                    pessoa = Pessoa.objects.create(
                        nome=nome,
                        email=email,
                        data_nascimento=data_nascimento.strftime('%Y-%m-%d'),
                        valor=valor,
                        ativo=True
                    )

                    people.append({
                        "Nome": pessoa.nome,
                        "Email": pessoa.email,
                        "Data de nascimento": pessoa.data_nascimento,
                        "Idade": idade,
                        "Valor": f"R$ {pessoa.valor:.2f}"
                    })

            return people
        except Exception as e:
            raise serializers.ValidationError(f"Erro ao processar o arquivo: {str(e)}")

    def to_representation(self, validated_data):
        return {"pessoas_ativas": validated_data['file']}


