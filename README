# Como Executar o Projeto com Docker Compose

## Serviços e Função de Cada Container

- **servidor-web-sync**: Servidor síncrono na porta 8080 do host (80 interna), recebe e responde requisições HTTP de maneira tradicional.
- **servidor-web-async**: Servidor assíncrono na porta 8000 do host (80 interna), recebe e responde requisições de forma assíncrona.
- **client**: Cliente Python que faz requisições para os servidores acima e registra as respostas no arquivo `client_log.txt` dentro do próprio container.

---

## Passo a Passo para Subir o Ambiente

1. **Posicione-se na pasta raiz do projeto** (onde está o arquivo `docker-compose.yml`).
2. **Execute o Docker Compose:**

   ```bash
   docker compose up --build
   ```
   - Isso irá construir as imagens e iniciar todos os containers ao mesmo tempo.

3. **Veja os containers em execução:**

   ```bash
   docker ps
   ```
   - Certifique-se que aparecem:
     - `servidor-web-sync`
     - `servidor-web-async`
     - `client`

---

## Como visualizar o log do cliente

O log das requisições feitas pelo cliente é gravado em `client_log.txt` dentro do container chamado `client`.

Para copiar esse arquivo do container para o seu computador, execute:

```bash
docker cp client:/app/client_log.txt client_log.txt
```

Após executar o comando acima, basta abrir o arquivo `client_log.txt` gerado no seu computador.
