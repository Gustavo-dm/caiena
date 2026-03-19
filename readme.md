# Weather Gist API

API desenvolvida em **Python + FastAPI** que integra:

* **OpenWeatherMap API** para obter clima atual e previsão
* **GitHub Gist API** para publicar comentários automaticamente

A aplicação expõe um **endpoint HTTP** que recebe uma cidade e um `gist_id`, consulta o clima e publica um comentário com:

* temperatura atual
* descrição do clima
* média diária da previsão dos próximos 5 dias

**Exemplo de comentário publicado no Gist:**

```
34°C e nublado em São Paulo em 12/03. Média para os próximos dias:
32°C em 13/03, 25°C em 14/03, 29°C em 15/03, 33°C em 16/03 e 28°C em 17/03.
```

---

## Índice

- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Testes](#testes)
- [Documentação da API](#documentação-da-api)
- [Arquitetura](#arquitetura)

---

## Requisitos

* Python **3.12+**
* Docker (opcional)
* Conta no GitHub
* Conta no OpenWeatherMap

---

## Instalação

### Modo Local

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/weather-gist-api.git
cd weather-gist-api
```

**2. Crie ambiente virtual:**

```bash
python -m venv .venv
# No macOS/Linux:
source .venv/bin/activate
# No Windows:
.venv\Scripts\activate
```

**3. Instale dependências:**

```bash
pip install -r requirements.txt
```

### Com Docker

**Build da imagem:**

```bash
docker build -t weather-gist-api .
```

**Executar container:**

```bash
docker run -p 8000:8000 \
-e OPENWEATHER_API_KEY=your_key \
-e GITHUB_TOKEN=your_token \
weather-gist-api
```

**Ou usando docker-compose:**

```bash
docker compose up --build
```

---

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (ou copie de `.env-example`):

```bash
cp .env-example .env
```

**Conteúdo do `.env`:**

```
OPENWEATHER_API_KEY=your_openweather_key
GITHUB_TOKEN=your_github_token
```

### OpenWeather API

1. Acesse https://openweathermap.org/api
2. Crie uma conta e gere uma chave API
3. Cole a chave em `OPENWEATHER_API_KEY` no `.env`

### GitHub Token

1. Acesse GitHub → Settings → Developer Settings → Personal Access Tokens
2. Crie um novo token com permissão `gist`
3. Cole o token em `GITHUB_TOKEN` no `.env`

---

## Uso

### Iniciar a Aplicação

```bash
uvicorn app.main:app --reload
```

Ou:

```bash
make run
```

Servidor estará disponível em: **http://localhost:8000**

### Documentação Interativa (Swagger)

Acesse: **http://localhost:8000/docs**

---

## Testes

### Rodar Todos os Testes

```bash
pytest tests/ -v
```

### Com Cobertura

```bash
pytest tests/ --cov=app --cov-report=html
```

Ou:

```bash
make test-coverage
```

### Testes Individuais

```bash
# Testes da API
pytest tests/test_api.py -v

# Testes do cache
pytest tests/test_cache.py -v

# Testes do parser de previsão
pytest tests/test_forecast_parser.py -v

# Testes do serviço de clima
pytest tests/test_weather_service.py -v

# Testes do cliente OpenWeather
pytest tests/test_openweather_client.py -v

# Testes do serviço Gist
pytest tests/test_gist.py -v
```

### Cobertura de Testes

- **Total:** 33 casos de teste
- **Cobertura:** ~95%
- **Componentes Cobertos:**
  - API routes
  - Weather service
  - Gist service
  - Cache
  - Forecast parser
  - OpenWeather client

---

## Documentação da API

### Endpoint: POST /weather-comment

Publica um comentário em um Gist com informações climáticas.

#### Parâmetros

| Parâmetro | Tipo   | Descrição                                   |
| --------- | ------ | ------------------------------------------- |
| city      | string | Cidade para consulta (obrigatório)          |
| gist_id   | string | ID do Gist onde o comentário será publicado |

#### Resposta (201 Created)

```json
{
  "message": "Comment posted successfully",
  "comment": "34°C e nublado em São Paulo em 19/03. Média para os próximos dias: 32°C em 20/03, 25°C em 21/03, 29°C em 22/03, 33°C em 23/03 e 28°C em 24/03."
}
```

#### Erros

| Código | Descrição |
| ------ | --------- |
| 400    | Parâmetros inválidos ou faltando |
| 422    | Validação falhou |
| 500    | Erro ao processar requisição |

#### Exemplos de Requisição

##### cURL

```bash
curl -X POST "http://localhost:8000/weather-comment?city=São%20Paulo&gist_id=abc123def456"
```

##### Python (requests)

```python
import requests

response = requests.post(
    "http://localhost:8000/weather-comment",
    params={
        "city": "São Paulo",
        "gist_id": "abc123def456"
    }
)

print(response.json())
```

##### JavaScript (fetch)

```javascript
const response = await fetch(
  'http://localhost:8000/weather-comment?city=São Paulo&gist_id=abc123def456',
  { method: 'POST' }
);

const data = await response.json();
console.log(data);
```

##### Postman

1. Método: **POST**
2. URL: `http://localhost:8000/weather-comment`
3. Query Params:
   - `city`: São Paulo
   - `gist_id`: abc123def456
4. Clique em **Send**

---

## Arquitetura

### Estrutura de Diretórios

```
app
 ├── api
 │    ├── index.py
 │    └── routes.py
 │
 ├── services
 │    ├── weather_service.py
 │    └── gist.py
 │
 ├── sdk
 │    └── openweather_client.py
 │
 ├── schemas
 │    └── weather_schema.py
 │
 ├── utils
 │    ├── cache.py
 │    ├── cache_instance.py
 │    ├── comment_builder.py
 │    ├── forecast_parser.py
 │    └── retry.py
 │
 ├── config.py
 ├── __init__.py
 └── main.py

tests
 ├── test_api.py
 ├── test_cache.py
 ├── test_forecast_parser.py
 ├── test_gist.py
 ├── test_openweather_client.py
 └── test_weather_service.py
```

### Fluxo de Dados

```
1. Requisição HTTP
   ↓
2. API Route (POST /weather-comment)
   ↓
3. WeatherService.get_weather_summary()
   ├── Verifica cache
   ├── Se cache miss:
   │   ├── OpenWeatherClient.get_current_weather()
   │   ├── OpenWeatherClient.get_forecast()
   │   └── forecast_parser.calculate_daily_average()
   └── Salva em cache
   ↓
4. comment_builder.build_comment()
   ↓
5. GistService.comment_on_gist()
   ├── GitHub API
   └── Publica comentário
   ↓
6. Resposta JSON (201 Created)
```

### Componentes

#### SDK (OpenWeatherClient)

- `get_current_weather(city)`
- `get_forecast(city)`

#### WeatherService

- Obtém temperatura atual
- Calcula média diária da previsão
- Gerencia cache

#### GistService

- `comment_on_gist(gist_id, comment)`

#### Utils

- forecast_parser
- comment_builder
- cache

#### API (FastAPI)

- POST /weather-comment
- GET /

---

## Quality Assurance

### Type Checking

```bash
mypy app/
```

### Testes

- 33 casos
- ~95% cobertura
- mocks para APIs externas

---

## Troubleshooting

### Erro: "No module named 'app'"

```bash
cd weather-gist-api
source .venv/bin/activate
```

### Erro: "OPENWEATHER_API_KEY not found"

```bash
cp .env-example .env
```

### Tests falhando

```bash
pip install -r requirements.txt --upgrade
```

---

## Funcionalidades implementadas

✔ Integração com OpenWeatherMap
✔ SDK customizado
✔ Integração com GitHub Gist
✔ Endpoint HTTP
✔ Cache em memória
✔ Testes automatizados
✔ Dockerização
✔ Estrutura modular

---

## Possíveis melhorias

* Persistência de cache (Redis)
* Retry automático
* Logging estruturado
* Monitoramento
* Rate limiting

