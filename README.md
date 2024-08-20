# projeto-backend-mais1code

## Como começar

- Fork este repositorio para sua conta pessoal no Github.
    - Navegue para https://github.com/gabrielfior/projeto-backend-mais1code > clique no botao Fork > na nova página que se abre, clicar botão verde `Create Fork'.
    - Copie o URL do seu repositorio novo - clique no botao verde Code (deve ser similar a https://github.com/<SEU_USERNAME_GITHUB>/projeto-backend-mais1code)

- Adicione o novo repositorio (que esta na sua conta pessoal) como remote neste repositorio,.
  - No terminal, digite os comandos (substitua <SEU_NOME> pelo seu nome, por exemplo, maria)
    ```commandline
    git remote add <SEU_NOME> https://github.com/<SEU_USERNAME_GITHUB>/projeto-backend-mais1code
    ```

Instale os pacotes necessários

```
pip install -r requirements.txt
```

Rode os testes
```
pytest
```

- Crie uma nova branch
```commandline
git checkout -b "<INSIRA NOME AQUI>"
```
- Faca as alteracoes nos arquivos de forma a implementar o ticket
- Adicione as mudancas no git
```commandline
git add .
```
- Transmita as alteracoes para o seu repositorio (lembre do nome que voce usou quando executou o comando `git remote add`)
```commandline
git push <SEU_NOME>
```
- Crie uma Pull Request (PR) usando o site do Github.
  - Navegue para https://github.com/gabrielfior/projeto-backend-mais1code e voce ja deve encontrar um pop-up sugerindo a criacao do PR.
  - Apos cria-lo, avise no grupo de Whatsapp que um PR foi criado. O PR sera revisado por um administrador.

## Como inicializar o backend

- No terminal, navegue para o root do repositorio (onde o arquivo `requirements.txt` esta localizado)
- Execute o comando abaixo
```
python -m server.server
```
- Abra o link a seguir no seu navegador, onde os endpoints estao disponiveis - http://localhost:8000/docs