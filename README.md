# Job Scheduler Manager

**Índice**
1. [Introdução](#intr)
2. [Configuração de ambiente](#cs1)
3. [Rodar projeto](#run)


## Introdução <a name="intr"></a>

Esse serviço é responsável por gerenciar a criação e consulta dos jobs. 
Se um job com os parâmetros corretos for sumetido, o serviço vai:
* Adicioná-lo a um banco de dados(que no momento é MongoDB, mas pode ser facilmente trocado, pois a comunicação com o banco foi desacoplada das regras de negócio). 
* Publicar em uma exchange do rabbitmq responsável por rotear para o worker designado a executar o Job. A routing-key é a descrição do job.


O arquivo `settings.py` é responsável por capturar as variáveis de ambiente requeridas para o projeto.
 * Atenção para as seguintes variáveis:
     - DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA: Uma string de descrições possíveis para o Job separadas por vírgula. No momento de criação do Job, o schema é validado e a descrição precisa ser uma das permitidas. 
     - ENVIRONMENT: Uma string que vai dizer qual ambiente a aplicação está rodando, por se tratar de uma aplicação Web, algumas funcionalidades são desabilidatas por padrão quando o ambiente é produtivo. 
## Configuração de ambiente <a name="cs1"></a>
Instalar dependências(rodar na raíz do projeto, versão do Python é 3.7)
````bash
pip install -r requirements.txt
````

## Rodar Projeto <a name="run"></a>
Comando para iniciar aplicação
````bash
python main.py
````
Acessando /docs é possível interagir com o swagger do serviço. Lá estão as descrições das rotas disponíveis, seus modelos e etc.


