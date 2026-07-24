#!/usr/bin/env python3
"""
Sincronizar banco de dados do Railway com as 15 categorias padrão
Reorganiza todas as categorias no banco em produção
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

# Try to use psycopg2 for PostgreSQL
try:
    import psycopg2
except ImportError:
    print("Instalando psycopg2...")
    os.system("pip install psycopg2-binary")
    import psycopg2

# CATEGORIAS PADRAO (15 principais)
CATEGORIAS_PADRAO = {
    "Tech": ["tech", "technology", "tecnologia", "programming", "desenvolvimento"],
    "AI": ["ai", "ia", "artificial intelligence", "inteligência artificial", "machine learning"],
    "Business": ["business", "negócios", "empresa", "corporate", "empreendimento"],
    "Education": ["education", "educação", "course", "cursos", "aprendizado", "tutorial"],
    "Food": ["food", "receita", "comida", "cooking", "cozinha", "gastro", "chef"],
    "Video": ["video", "youtube", "vimeo", "vídeo", "canal", "tutorial video"],
    "Social Media": ["social media", "linkedin", "facebook", "instagram", "twitter"],
    "News": ["news", "notícia", "blog", "artigo", "medium", "dev.to"],
    "Entertainment": ["entertainment", "games", "jogos", "humor", "music", "música"],
    "Health": ["health", "saúde", "fitness", "wellness", "medical"],
    "Marketing": ["marketing", "advertising", "publicidade", "growth", "sales"],
    "Design": ["design", "ux", "ui", "figma", "graphics", "art"],
    "Finance": ["finance", "finança", "banking", "investimento", "crypto"],
    "Lifestyle": ["lifestyle", "travel", "viagem", "fashion", "diy"],
    "Other": ["other", "misc", "diversos", "outro", "general"]
}

KEYWORD_TO_CATEGORY = {}
for cat, keywords in CATEGORIAS_PADRAO.items():
    for kw in keywords:
        KEYWORD_TO_CATEGORY[kw.lower()] = cat

def agrupar_categoria_local(categoria_original):
    """Agrupa para categoria padrao"""
    if not categoria_original:
        return "Other"

    texto = categoria_original.lower()
    for keyword, categoria_padrao in KEYWORD_TO_CATEGORY.items():
        if keyword in texto:
            return categoria_padrao
    return "Other"

def get_railway_connection():
    """Conecta ao banco PostgreSQL do Railway"""

    # Tentar obter credenciais de variáveis de ambiente
    db_url = os.getenv("DATABASE_URL")

    if db_url:
        print(f"Conectando ao Railroad via DATABASE_URL...")
        try:
            conn = psycopg2.connect(db_url)
            return conn
        except Exception as e:
            print(f"❌ Erro ao conectar com DATABASE_URL: {e}")
            return None

    # Tentar credenciais individuais
    db_config = {
        'host': os.getenv("DB_HOST", "localhost"),
        'port': int(os.getenv("DB_PORT", "5432")),
        'database': os.getenv("DB_NAME", "banco"),
        'user': os.getenv("DB_USER", "postgres"),
        'password': os.getenv("DB_PASSWORD", ""),
    }

    try:
        print(f"Conectando a {db_config['host']}:{db_config['port']}...")
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\nVariáveis de ambiente esperadas:")
        print("  DATABASE_URL ou (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)")
        return None

def sincronizar_banco():
    """Sincroniza banco do Railway"""

    print("=" * 70)
    print("SINCRONIZAR BANCO - RAILWAY")
    print("=" * 70)

    # Conectar
    conn = get_railway_connection()
    if not conn:
        print("\n❌ Nao conseguiu conectar ao banco. Verifique as credenciais.")
        return False

    try:
        cursor = conn.cursor()

        # FASE 1: Agrupar
        print("\nFASE 1: Agrupando categorias...")
        cursor.execute("SELECT DISTINCT categoria FROM links ORDER BY categoria")
        categorias_originais = [row[0] for row in cursor.fetchall() if row[0]]

        mapeamento = {}
        for cat_original in categorias_originais:
            cat_padrao = agrupar_categoria_local(cat_original)
            mapeamento[cat_original] = cat_padrao

        print(f"  OK: {len(categorias_originais)} categorias agrupadas")

        # FASE 2: Atualizar
        print("\nFASE 2: Atualizando banco...")

        total_updated = 0
        for categoria_original, categoria_nova in mapeamento.items():
            if categoria_original != categoria_nova:
                cursor.execute(
                    "UPDATE links SET categoria = %s WHERE categoria = %s",
                    (categoria_nova, categoria_original)
                )
                count = cursor.rowcount
                if count > 0:
                    total_updated += count

        conn.commit()
        print(f"  OK: {total_updated} links atualizados")

        # FASE 3: Relatorio
        print("\nFASE 3: Relatorio final")
        print("-" * 70)

        cursor.execute("""
            SELECT categoria, COUNT(*) as count
            FROM links
            GROUP BY categoria
            ORDER BY count DESC
        """)

        total = 0
        for row in cursor.fetchall():
            cat = row[0] or 'NULL'
            count = row[1]
            print(f"  {cat}: {count}")
            total += count

        print("-" * 70)
        print(f"  TOTAL: {total} links")

        cursor.close()
        conn.close()

        print("\n" + "=" * 70)
        print("OK! Banco sincronizado com 15 categorias padrao")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"\nErro: {e}")
        conn.close()
        return False

if __name__ == "__main__":
    success = sincronizar_banco()
    sys.exit(0 if success else 1)
