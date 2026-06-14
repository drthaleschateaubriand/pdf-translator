# pdf-translator

## O que é este projeto

Script Python que traduz PDFs acadêmicos de inglês para português preservando layout idêntico ao original, usando a biblioteca `pdf2zh` com Claude como motor de tradução.

## Estrutura

```
pdf-translator/
├── translate.py       # Script principal - PONTO DE ENTRADA
├── traduzir.sh        # Wrapper Mac/Linux
├── traduzir.bat       # Wrapper Windows
├── requirements.txt   # Dependências: pdf2zh, python-dotenv
├── .env.example       # Modelo de configuração
├── .env               # Configuração real (NÃO commitar)
└── CLAUDE.md          # Este arquivo
```

## Como usar

```bash
# Instalação
pip install -r requirements.txt

# Configuração (copiar e preencher com chave Anthropic)
cp .env.example .env

# Tradução
python translate.py artigo.pdf
```

## Variáveis de ambiente (.env)

- `ANTHROPIC_API_KEY`: chave da API Anthropic (obrigatória)
- `TRANSLATE_MODEL`: modelo Claude padrão (padrão: claude-haiku-4-5-20251001)
- `LANG_OUT`: idioma de saída (padrão: pt)
- `THREADS`: threads paralelas (padrão: 4)

## Fluxo interno

1. `translate.py` lê o PDF e carrega variáveis de ambiente
2. Configura o serviço `openailiked` apontando para `https://api.anthropic.com/v1`
3. Chama `pdf2zh` que detecta layout (modelo ONNX), extrai texto e traduz via Claude
4. Gera `saida/NOME-mono.pdf` (só português) e `saida/NOME-dual.pdf` (EN + PT)

## Dependências chave

- `pdf2zh`: biblioteca de tradução com preservação de layout
- `python-dotenv`: carrega variáveis do arquivo .env
- `onnx`, `onnxruntime`: detecta regiões de layout no PDF (baixado automaticamente na 1ª execução)

## Tarefas comuns que o Claude Code pode ajudar

- Adicionar suporte a novos idiomas de saída
- Criar interface web com Gradio ou Streamlit
- Adicionar processamento em lote (múltiplos PDFs)
- Criar relatório de custo estimado antes de traduzir
- Adicionar prompt customizado para terminologia médica
- Integrar com Google Drive para upload automático do resultado

## Prompt médico recomendado

Para artigos médicos, usar `--prompt` com:
```
Você é um tradutor médico especializado. Ao traduzir, mantenha os termos técnicos corretos em português brasileiro. Preserve valores numéricos, estatísticas, siglas de exames e nomes de medicamentos exatamente como no original.
```

## Contexto do usuário

Médico intensivista e nutrólogo. Usa a ferramenta principalmente para traduzir artigos científicos e revisões sistemáticas da área médica (nutrição esportiva, terapia intensiva, nutrologia).
