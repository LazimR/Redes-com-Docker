# Projeto: Benchmark e Monitoramento de Servidores Web com Docker

## Visão Geral

Este projeto tem como objetivo comparar o desempenho entre servidores NGINX e Apache, utilizando métricas reais extraídas com Prometheus e visualizadas com Grafana. O ambiente simula cargas (leve, média, pesada e stress) utilizando a ferramenta k6. Todos os serviços são orquestrados via Docker Compose.

---

## Estrutura de Pastas

- **apache/**  
  - `Dockerfile`: Prepara imagem Apache customizada.  
  - `apache.conf`: Configuração personalizada do Apache.  
  - `html/`: Arquivos estáticos servidos (`index.html`, `leve.txt`, `medio.txt`, `pesado.txt`).

- **nginx/**  
  - `Dockerfile`: Cria imagem do NGINX com configuração e conteúdo.  
  - `nginx.conf`: Configuração NGINX expondo endpoints de arquivos e status.  
  - `html/`: Arquivos estáticos servidos.

- **k6/**  
  - `Dockerfile`: Prepara ambiente para os testes de carga.  
  - `teste_de_carga/`:  
    - `loop_tests.sh`: Script que executa todos os testes em loop.  
    - `teste_leve.js`, `teste_medio.js`, `teste_pesado.js`, `teste_de_stress.js`: Scripts de teste k6.

- **prometheus/**  
  - `prometheus.yml`: Targets e jobs para coleta de métricas.

- **grafana_model.json**  
  - Modelo de dashboard para monitoramento visual.

- **docker-compose.yml**  
  - Orquestração completa dos containers e redes.

---

## Serviços Principais

- **nginx**: Servidor web NGINX em `localhost:8080/main`.  
- **apache**: Servidor Apache em `localhost:8081/main`.  
- **prometheus**: Monitoramento em `localhost:9090`.  
- **grafana**: Painel gráfico em `localhost:3000` (login padrão: admin/admin).
- **node-exporter**: Métricas do SO para Prometheus.
- **nginx-exporter/apache-exporter**: Exportam métricas HTTP dos servidores para Prometheus.
- **k6**: Executor automatizado de testes de carga.

---

## Como Executar

1. **Build e inicialização:**
   ```sh
   docker compose up --build -d
   ```

2. **Acessos:**
    - **Nginx:** http://localhost:8080  
    - **Apache:** http://localhost:8081  
    - **Prometheus:** http://localhost:9090  
    - **Grafana:** http://localhost:3000  (login: admin/admin)

3. **Testes de carga:**
   - São executados automaticamente pelo serviço `k6`. O script `loop_tests.sh` cicla entre todos os testes (`leve`, `médio`, `pesado` e `stress`) definidos em `k6/teste_de_carga`.

4. **Dashboards e Métricas:**  
   - Importe o `grafana_model.json` para visualizar suas próprias métricas.

---

## Arquitetura Resumida

```
+---------+        +--------+        +-------------+      +----------+
|  k6     | <----> | nginx  | <----> | exporters   | <--> |prometheus|
| scripts | <----> | apache |        | node/nginx/ |      +----------+
+---------+        +--------+        | apache      |
                        |                        |
                        +------>  grafana  <-----+
```

---

## Observações Importantes

- Edite os arquivos de teste (`.js` no k6) para personalizar suas requisições.
- Todos os arquivos consumidos pelos testes devem estar presentes nas pastas `html/` de cada servidor.
- O serviço de carga (`k6`) pode ser personalizado com variáveis de ambiente ou mods no script.
- O dashboard Grafana pode ser ajustado ou substituído conforme suas análises e necessidades.
- Endereços IP internos e portas podem ser customizados no `docker-compose.yml`, inclusive a subrede inteira.

---

## Como contribuir/Testar

1. Fork e clone este repositório.
2. Tenha Docker e Docker Compose instalados.
3. Implemente melhorias, ajustes de cenários, amplie métricas ou novos scripts de teste!
4. Sugestões e Pull Requests são bem-vindos!

---

**Este projeto é ideal para estudar comparações práticas de servidores, visualizar gargalos em tempo real e experimentar ajuste fino de configuração em ambiente controlado via containers!**
