from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExcelUploadSerializer
from rest_framework import status
import openpyxl
from io import BytesIO
import base64
from .models import Pessoa



class PessoaUploadView(APIView):
    """
        View para lidar com o upload de arquivos Excel contendo dados de Pessoa.

        Esta view é responsável por processar requisições POST que fazem o upload de arquivos Excel, validando os dados usando o ExcelUploadSerializer e retornando respostas apropriadas com base na validade dos dados enviados.

        Atributos:
            post (método): Lida com requisições POST. Utiliza o ExcelUploadSerializer para validar e processar os dados enviados. Retorna uma resposta com status HTTP_200_OK se os dados forem válidos, ou HTTP_400_BAD_REQUEST se os dados forem inválidos.
    """
    serializer_class = ExcelUploadSerializer  

    def post(self, request, *args, **kwargs):
        serializer = ExcelUploadSerializer(data=request.data)
        if serializer.is_valid():
            people = serializer.validate_file(request.FILES['file'])
            return Response({"pessoas_ativas": people}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PessoaExportView(APIView):
    """
    View para exportar dados de Pessoa em formato de planilha Excel.

    Esta view é responsável por gerar e retornar um arquivo Excel contendo as informações de todas as pessoas ativas no banco de dados.

    Métodos:
        get(request, *args, **kwargs):
            Gera um arquivo Excel com as informações das pessoas ativas e o retorna como resposta em formato base64.
    """
    
    def get(self, request, *args, **kwargs):
        # Gerar a planilha Excel
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Pessoas Ativas'
        
        sheet.append(['Nome', 'Email', 'Data de Nascimento', 'Valor', 'Status'])

        pessoas = Pessoa.objects.filter(ativo=True)
        for pessoa in pessoas:
            status_ativo = "Ativo" if pessoa.ativo else "Inativo"
            sheet.append([
                pessoa.nome,
                pessoa.email,
                pessoa.data_nascimento.strftime("%d/%m/%Y"),
                f"R$ {pessoa.valor:.2f}",
                status_ativo
            ])

        file_stream = BytesIO()
        workbook.save(file_stream)
        file_stream.seek(0)
        file_base64 = base64.b64encode(file_stream.getvalue()).decode('utf-8')
        base64_link = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_base64}"        
        return Response({'link': base64_link}, status=status.HTTP_200_OK)
    

