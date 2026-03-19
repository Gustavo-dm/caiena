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
| gist_id   | string | ID do Gist onde o comentário será publicado (obrigatório) |

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
| 500    | Erro ao processar requisição (ex: API externa indisponível) |

### Exemplos de Requisição

#### cURL

```bash
curl -X POST "http://localhost:8000/weather-comment?city=São%20Paulo&gist_id=abc123def456"
```

#### Python (requests)

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

#### JavaScript (fetch)

```javascript
const response = await fetch(
  'http://localhost:8000/weather-comment?city=São Paulo&gist_id=abc123def456',
  { method: 'POST' }
);

const data = await response.json();
console.log(data);
```

#### Postman

1. Método: **POST**
2. URL: `http://localhost:8000/weather-comment`
3. Query Params:
   - `city`: São Paulo
   - `gist_id`: abc123def456
4. Clique em **Send**

---

## Arquitetura

## Arquitetura

### Estrutura de Diretórios

O projeto foi estruturado seguindo separação de responsabilidades:

```
app
 ├── api
 │    ├── index.py          # Root endpoint
 │    └── routes.py         # Weather comment endpoint
 │
 ├── services
 │    ├── weather_service.py # Lógica de clima
 │    └── gist.py            # Integração com GitHub
 │
 ├── sdk
 │    └── openweather_client.py # Cliente OpenWeather
 │
 ├── schemas
 │    └── weather_schema.py  # Validação Pydantic
 │
 ├── utils
 │    ├── cache.py           # Cache em memória
 │    ├── cache_instance.py  # Instância do cache
 │    ├── comment_builder.py # Construir texto do comentário
 │    ├── forecast_parser.py # Parser de previsão
 │    └── retry.py           # Lógica de retry
 │
 ├── config.py       # Configurações
 ├── __init__.py
 └── main.py         # App FastAPI

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

Biblioteca responsável pela integração com a API do OpenWeatherMap.

- `get_current_weather(city)` - Obtém clima atual
- `get_forecast(city)` - Obtém previsão de 5 dias

**Type hints:** ✅ Totalmente tipado

#### WeatherService

Camada de serviço responsável por:

- Obter temperatura atual
- Calcular média diária da previsão
- Gerenciar cache

**Features:**
- Cache em memória com TTL
- Case-insensitive cache keys
- Type hints completos

#### GistService

Integração com a API do GitHub utilizando **PyGithub**.

- `comment_on_gist(gist_id, comment)` - Publica comentário

**Error handling:**
- Trata exceções de autenticação
- Trata gists não encontrados

#### Utils

- **forecast_parser** → Calcula média diária da previsão (suporta timestamps e datetime strings)
- **comment_builder** → Constrói texto formatado do comentário
- **cache** → Cache simples em memória com TTL configurável
- **comment_builder** → Formata comentário para publicação

#### API (FastAPI)

- **POST /weather-comment** - Endpoint principal
- **GET /** - Health check
- Error handling com HTTPException
- Documentação automática em `/docs` (Swagger UI)

---

## Quality Assurance

### Type Checking

```bash
mypy app/
```

Fornece verificação estática de tipos.

### Linting & Formatting

O projeto inclui configurações para:
- Type hints completos
- Estrutura clara e organizada

### Testes

- **33 casos de teste**
- **~95% de cobertura**
- Testes de sucesso, erro e edge cases
- Uso de mocks para serviços externos

---

## Melhorias Futuras

- [ ] Adicionar autenticação JWT
- [ ] Implementar rate limiting
- [ ] Usar banco de dados para persistência
- [ ] Integrar Redis para cache distribuído
- [ ] Adicionar logging estruturado
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Testes de carga/performance
- [ ] Suporte a múltiplas cidades em uma requisição

---

## Troubleshooting

### Erro: "No module named 'app'"

**Solução:** Certifique-se que você está no diretório correto e ativou o ambiente virtual.

```bash
cd weather-gist-api
source .venv/bin/activate
```

### Erro: "OPENWEATHER_API_KEY not found"

**Solução:** Configure as variáveis de ambiente no `.env`.

```bash
cp .env-example .env
# Edite .env com suas chaves reais
```

### Tests falhando

**Solução:** Reinstale as dependências.

```bash
pip install -r requirements.txt --upgrade
```

---

## Contribuir

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

---

## Licença

MIT License

---

## Contato

Para dúvidas ou sugestões, entre em contato através de issues no repositório.

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
