# Weather Gist API

API desenvolvida em **Python + FastAPI** que integra:

* **OpenWeatherMap API** para obter clima atual e previsão
* **GitHub Gist API** para publicar comentários automaticamente

A aplicação expõe um **endpoint HTTP** que recebe uma cidade e um `gist_id`, consulta o clima e publica um comentário com:

* temperatura atual
* descrição do clima
* média diária da previsão dos próximos 5 dias

Exemplo de comentário publicado no Gist:

```
34°C e nublado em São Paulo em 12/03. Média para os próximos dias:
32°C em 13/03, 25°C em 14/03, 29°C em 15/03, 33°C em 16/03 e 28°C em 17/03.
```

---

# Arquitetura do Projeto

O projeto foi estruturado seguindo separação de responsabilidades:

```
app
 ├── api
 │    └── routes.py
 │
 ├── services
 │    ├── weather_service.py
 │    └── gist.py
 │
 ├── sdk
 │    └── openweather_client.py
 │
 ├── utils
 │    ├── cache.py
 │    ├── forecast_parser.py
 │    └── comment_builder.py
 │
 ├── config.py
 └── main.py

tests
 ├── test_api.py
 ├── test_cache.py
 ├── test_forecast_parser.py
 └── test_weather_service.py
```

## Componentes

### SDK (OpenWeatherClient)

Biblioteca responsável pela integração com a API do OpenWeatherMap.

### WeatherService

Camada de serviço responsável por:

* obter temperatura atual
* calcular média diária da previsão

### GistService

Integração com a API do GitHub utilizando **PyGithub** para publicar comentários.

### Utils

* `forecast_parser` → cálculo da média diária da previsão
* `comment_builder` → construção do texto do comentário
* `cache` → cache simples em memória para evitar múltiplas chamadas à API externa

### API (FastAPI)

Expõe o endpoint HTTP para uso da aplicação.

---

# Requisitos

* Python **3.12+**
* Docker (opcional)
* Conta no GitHub
* Conta no OpenWeatherMap

---

# Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
OPENWEATHER_API_KEY=your_openweather_key
GITHUB_TOKEN=your_github_token
```

## OpenWeather API

Crie uma chave em:

https://openweathermap.org/api

---

## GitHub Token

Gerar token em:

```
GitHub → Settings → Developer Settings → Personal Access Tokens
```

Permissões necessárias:

```
gist
```

---

# Instalação (modo local)

Clone o repositório:

```
git clone https://github.com/seu-usuario/weather-gist-api.git
cd weather-gist-api
```

Crie ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate
```

Instale dependências:

```
pip install -r requirements.txt
```

Execute a aplicação:

```
uvicorn app.main:app --reload
```

Servidor iniciará em:

```
http://localhost:8000
```

---

# Executando com Docker

Build da imagem:

```
docker build -t weather-gist-api .
```

Executar container:

```
docker run -p 8000:8000 \
-e OPENWEATHER_API_KEY=your_key \
-e GITHUB_TOKEN=your_token \
weather-gist-api
```

Ou usando docker-compose:

```
docker compose up --build
```

---

# Endpoint da API

## POST /weather-comment

Publica um comentário em um Gist com informações climáticas.

### Parâmetros

| Parâmetro | Tipo   | Descrição                                   |
| --------- | ------ | ------------------------------------------- |
| city      | string | Cidade para consulta                        |
| gist_id   | string | ID do Gist onde o comentário será publicado |

### Exemplo

```
POST /weather-comment?city=London&gist_id=123abc
```

### Resposta

```
{
  "status": "comment published",
  "city": "London"
}
```

---

# Endpoint de saúde

## GET /

Verifica se a API está ativa.

Resposta:

```
{
  "message": "Weather Gist API running"
}
```

---

# Testes

Para executar os testes automatizados:

```
pytest
```

Os testes incluem:

* API endpoint
* cálculo da média de previsão
* cache em memória
* service layer

Chamadas externas são **mockadas**, evitando dependência de APIs externas durante os testes.

---

# Funcionalidades implementadas

✔ Integração com OpenWeatherMap
✔ SDK customizado para API externa
✔ Integração com GitHub Gist
✔ Endpoint HTTP com FastAPI
✔ Cache em memória
✔ Testes automatizados
✔ Dockerização
✔ Estrutura modular de projeto

---

# Diferenciais

* Baixo número de dependências
* Arquitetura modular
* Testes automatizados
* Docker
* Cache simples para otimização de chamadas externas

---

# Possíveis melhorias

* Persistência de cache (Redis)
* Retry automático em chamadas externas
* Logging estruturado
* Monitoramento
* Rate limiting
