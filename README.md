# Análise de partidas de Dota 2

Projeto de dados desenvolvido para comparar o comportamento e o desempenho dos heróis em partidas públicas ranqueadas e nas partidas profissionais do The International 2026.

O projeto contempla a extração de dados da API OpenDota, tratamento com Python, armazenamento em PostgreSQL e análises utilizando SQL.

## Objetivo

Analisar as diferenças entre o cenário público e o cenário competitivo do Dota 2, respondendo perguntas como:

- Quais heróis apresentam os maiores win rates?
- Quais heróis são mais utilizados nas partidas públicas e no TI?
- Quais heróis ganharam ou perderam relevância no cenário profissional?
- Quais duplas de heróis apresentaram maior sinergia durante o TI?

## Tecnologias utilizadas

- Python
- PostgreSQL
- SQL
- API OpenDota
- JSON
- CSV
- Visual Studio Code
- Git e GitHub

## Etapas do projeto

1. Consulta dos endpoints da API OpenDota;
2. Extração de partidas públicas;
3. Extração das partidas do The International 2026;
4. Tratamento e validação dos dados com Python;
5. Transformação dos dados brutos em arquivos CSV;
6. Criação das tabelas no PostgreSQL;
7. Importação dos dados tratados;
8. Desenvolvimento das análises em SQL.

## Base de dados

O banco foi estruturado utilizando cinco tabelas:

- `herois`
- `partidas_publicas`
- `participacoes_publicas`
- `partidas_ti`
- `participacoes_ti`

As tabelas de participações fazem a ligação entre cada partida e os heróis utilizados por Radiant e Dire.

## Volume de dados

- 11.000 partidas públicas coletadas;
- 10.989 partidas públicas com escalações completas;
- 109.890 participações públicas;
- 147 partidas do The International 2026;
- 1.470 participações no TI;
- 127 heróis cadastrados.

## Estrutura do repositório

```text
Projeto_Dota/
├── python/
│   ├── scripts de extração
│   └── scripts de tratamento
│
└── sql/
    ├── criação das tabelas
    └── consultas analíticas
