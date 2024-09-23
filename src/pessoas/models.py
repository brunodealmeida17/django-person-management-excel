from django.db import models


class Pessoa(models.Model):
    """
        Modelo para representar uma pessoa.

        Este modelo armazena informações sobre uma pessoa, incluindo nome, e-mail, data de nascimento, valor associado e um status de atividade.

        Atributos:

            - nome (CharField): O nome da pessoa, com um comprimento máximo de 255 caracteres.
            - email (EmailField): O endereço de e-mail da pessoa.
            - data_nascimento (CharField): A data de nascimento da pessoa, armazenada como uma string com um comprimento máximo de 10 caracteres.
            - valor (FloatField): Um valor associado à pessoa, armazenado como um número de ponto flutuante.
            - ativo (BooleanField): Um campo booleano que indica se a pessoa está ativa ou não.

        Métodos:
        
             __str__ (método): Retorna o nome da pessoa como uma representação em string do objeto.
    """
    
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField()
    data_nascimento = models.CharField(max_length=10, verbose_name='Data de nascimento')
    valor = models.FloatField()
    ativo = models.BooleanField()


    def __str__(self) -> str:
        return self.nome