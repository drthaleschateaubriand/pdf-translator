#!/usr/bin/env python3
"""
pdf-translator: Traduz PDFs preservando layout usando pdf2zh + Claude API
Repositório: https://github.com/drthaleschateaubriand/pdf-translator
"""

import argparse
import os
import sys
from pathlib import Path

# Carregar .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_env(key, default=None):
    return os.environ.get(key, default)


def configure_anthropic():
    """Configura variáveis para usar Claude via compatibilidade OpenAI."""
    api_key = get_env("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERRO: ANTHROPIC_API_KEY não encontrada.")
        print("  1. Copie .env.example para .env")
        print("  2. Adicione sua chave em https://console.anthropic.com/settings/keys")
        sys.exit(1)

    os.environ["OPENAILIKED_BASE_URL"] = "https://api.anthropic.com/v1"
    os.environ["OPENAILIKED_API_KEY"] = api_key
    return "openailiked"


def translate(
    pdf_path: str,
    lang_in: str = "en",
    lang_out: str = None,
    model: str = None,
    service: str = None,
    output: str = None,
    pages: str = None,
    threads: int = None,
):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"ERRO: Arquivo não encontrado: {pdf_path}")
        sys.exit(1)

    lang_out = lang_out or get_env("LANG_OUT", "pt")
    model    = model    or get_env("TRANSLATE_MODEL", "claude-haiku-4-5-20251001")
    threads  = threads  or int(get_env("THREADS", "4"))
    output   = output   or str(pdf_path.parent / "saida")

    # Configurar serviço
    if service is None or service == "claude":
        service = configure_anthropic()
        os.environ["OPENAILIKED_MODEL"] = model
        print(f"Motor: Claude ({model})")
    elif service == "google":
        print("Motor: Google Translate (gratuito, sem chave)")
    else:
        print(f"Motor: {service}")

    print(f"Arquivo: {pdf_path.name}")
    print(f"Idioma: {lang_in} → {lang_out}")
    print(f"Saída:  {output}/")
    print()

    # Montar argumentos para pdf2zh
    args = [
        str(pdf_path),
        "--lang-in", lang_in,
        "--lang-out", lang_out,
        "--service", service,
        "--output", output,
        "--thread", str(threads),
    ]

    if pages:
        args += ["--pages", pages]

    # Chamar pdf2zh
    try:
        from pdf2zh.pdf2zh import main as pdf2zh_main
        import sys as _sys
        old_argv = _sys.argv
        _sys.argv = ["pdf2zh"] + args
        pdf2zh_main()
        _sys.argv = old_argv
    except SystemExit as e:
        if e.code != 0:
            print(f"\nErro durante tradução (código {e.code})")
            sys.exit(e.code)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        raise

    # Mostrar resultado
    output_path = Path(output)
    stem = pdf_path.stem
    mono = output_path / f"{stem}-mono.pdf"
    dual = output_path / f"{stem}-dual.pdf"

    print()
    print("=" * 50)
    print("Tradução concluída!")
    if mono.exists():
        size = mono.stat().st_size / 1024 / 1024
        print(f"  Versão PT:        {mono}  ({size:.1f} MB)")
    if dual.exists():
        size = dual.stat().st_size / 1024 / 1024
        print(f"  Versão EN+PT:     {dual}  ({size:.1f} MB)")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Traduz PDFs preservando layout usando pdf2zh + Claude API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python translate.py artigo.pdf
  python translate.py artigo.pdf --model claude-sonnet-4-5
  python translate.py artigo.pdf --pages 1-5
  python translate.py artigo.pdf --service google
  python translate.py artigo.pdf --output ./resultado --threads 8
        """
    )
    parser.add_argument("pdf", help="Caminho para o arquivo PDF")
    parser.add_argument("--lang-in",  default="en",   help="Idioma de entrada (padrão: en)")
    parser.add_argument("--lang-out", default=None,   help="Idioma de saída (padrão: pt)")
    parser.add_argument("--model",    default=None,   help="Modelo Claude (padrão: claude-haiku-4-5-20251001)")
    parser.add_argument("--service",  default=None,   help="Serviço: claude (padrão), google, deepl, openai")
    parser.add_argument("--output",   default=None,   help="Pasta de saída (padrão: ./saida)")
    parser.add_argument("--pages",    default=None,   help="Páginas (ex: 1-5 ou 1,3,5)")
    parser.add_argument("--threads",  default=None, type=int, help="Threads paralelas (padrão: 4)")

    args = parser.parse_args()

    translate(
        pdf_path=args.pdf,
        lang_in=args.lang_in,
        lang_out=args.lang_out,
        model=args.model,
        service=args.service,
        output=args.output,
        pages=args.pages,
        threads=args.threads,
    )


if __name__ == "__main__":
    main()
