from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from openpyxl import Workbook

class PessoaUploadViewTestCase(APITestCase):
    def setUp(self):
        
        self.valid_excel_file = self.create_excel_file([
            ('Nome', 'Email', 'Data de nascimento', 'Ativo'),            
            ('Rafael Rodrigues', 'rafael.rodrigues@exemplo.com', '1975-08-21', 1),
            ('Fernanda Silva', 'fernanda.silva@exemplo.com', '1991-08-17', 1),
            ('Maria Sousa', 'maria.sousa@exemplo.com', '1984-08-18', 1),
        ])
        self.upload_url = reverse('upload-excel')

    def create_excel_file(self, data):
        """
            Cria um arquivo Excel válido para teste.
        """
        wb = Workbook()
        ws = wb.active

        for row in data:
            ws.append(row)

        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        return SimpleUploadedFile(
            'test.xlsx', stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    def create_invalid_excel_file(self):
        """
            Cria um arquivo Excel inválido para teste.
        """
        wb = Workbook()
        ws = wb.active
        
        ws.append(['Nome', 'Email', 'Data de nascimento', 'Ativo'])
        ws.append(['Nome Inválido', 'email_invalido', 'data_invalida', 'texto_ao_invés_de_boolean'])

        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)
        return SimpleUploadedFile(
            'invalid_test.xlsx', stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    

    def test_valid_excel_upload(self):
        """
            Testa o upload de um arquivo Excel válido.
        """
        response = self.client.post(self.upload_url, {'file': self.valid_excel_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertIn('pessoas_ativas', data)
        pessoas_ativas = data['pessoas_ativas']
        self.assertEqual(len(pessoas_ativas), 3) 

        self.assertEqual(pessoas_ativas[0]['Nome'], 'Rafael Rodrigues')
        self.assertEqual(pessoas_ativas[0]['Data de nascimento'], "1975-08-21") 
        self.assertEqual(pessoas_ativas[0]['Valor'], 'R$ 150.00')

        self.assertEqual(pessoas_ativas[1]['Nome'], 'Fernanda Silva')
        self.assertEqual(pessoas_ativas[1]['Data de nascimento'], "1991-08-17")  
        self.assertEqual(pessoas_ativas[1]['Valor'], 'R$ 150.00')
        

    def test_invalid_excel_upload(self):        
        invalid_file = self.create_invalid_excel_file()
        response = self.client.post(self.upload_url, {'file': invalid_file}, format='multipart')        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertIn('file', data)
        self.assertIn("time data 'data_invalida' does not match format '%Y-%m-%d'", data['file'][0])
