
# PTA (Protocolo de Transferência de Arquivos)

Este projeto implementa um Protocolo de Transferência de Arquivos (PTA) para um ambiente de aprendizado, permitindo a autenticação de usuários, listagem de arquivos e download de arquivos via cliente-servidor.

## Configuração do Ambiente (ENV)

### Requisitos

- **Python 3.x**
- **Bibliotecas padrão**: `socket`, `threading`, `os`, `base64`

### Passos para Configurar o Ambiente

1. **Crie e ative um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   # Crie um ambiente virtual
   python -m venv venv

   # Ative o ambiente virtual
   # No Windows
   venv\Scripts\activate
   # No Linux ou macOS
   source venv/bin/activate
   ```

3. **Instale as dependências necessárias**:
   Neste caso, as dependências são todas bibliotecas padrão do Python, então não há necessidade de instalação de pacotes adicionais.

## Iniciar o Servidor

1. **Executar o servidor**:
   No terminal, execute o servidor com o seguinte comando:
   ```bash
   python server.py
   ```

   O servidor estará rodando no endereço `0.0.0.0` na porta `11550`, pronto para receber conexões de clientes.

## Executar o Cliente

Depois de iniciar o servidor, você pode conectar um cliente ao servidor e interagir com ele. Para isso, siga os passos abaixo:

1. **Iniciar o cliente**:
   
   No terminal, execute o cliente com o seguinte comando, passando o IP do servidor, a porta e o nome de usuário:
   ```bash
   python pta-client.py 127.0.0.1 11550 user1
   ```

   Onde:
   - `127.0.0.1` é o IP do servidor.
   - `11550` é a porta em que o servidor está escutando.
   - `user1` é o nome de usuário que está sendo autenticado.

2. **Interagir com o servidor**:
   
   Após iniciar o cliente, ele irá executar uma série de testes, como:
   - Verificar o comando `CUMP` (autenticação).
   - Listar arquivos disponíveis com o comando `LIST`.
   - Tentar baixar arquivos com o comando `PEGA`.
   - Encerrar a conexão com o comando `TERM`.

### saída esperada do cliente:

```bash
Testing command without CUMP
0 NOK
Points: 1/6
Testing CUMP with bad user
Points: 2/6
Testing CUMP with good user
Points: 3/6
Testing LIST
1 ARQS 16 dummyfile01-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile02-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile03-with-a-bigger-name-to-test-your-buffer-treatment.png,dummyfile04-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile05-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile06-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile07-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile08-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile09-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile10-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile11-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile12-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile13-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile14-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile15-with-a-bigger-name-to-test-your-buffer-treatment.txt,dummyfile16-with-a-bigger-name-to-test-your-buffer-treatment.txt
Points: 4/6
Testing ARQ with good file
136 136
Points: 5/6
Testing ARQ with bad file
Points: 6/6
Testing TERM
TERM is OK!
```