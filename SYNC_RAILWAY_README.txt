================================================================================
                    SINCRONIZAR BANCO DO RAILWAY
================================================================================

SITUACAO:
  ✓ Codigo atualizado com Fable 5 (10x mais barato)
  ✓ Push feito para Railway (deploy em progresso)
  ✓ Agora precisa sincronizar o banco de dados

================================================================================
COMO SINCRONIZAR:
================================================================================

OPCAO A: Via Railway Console (Recomendado)
──────────────────────────────────────────────

1. Acesse: https://railway.app
2. Entre no projeto "Banco de Links"
3. Vá para a aba "PostgreSQL"
4. Clique em "Connect" ou "Query"
5. Use o Query Editor e execute:

   -- Reorganizar categorias para 15 padrao
   -- Tech
   UPDATE links SET categoria = 'Tech' WHERE categoria IN
   ('Tecnologia', 'Technology', 'Tech', 'programming', 'desenvolvimento');

   -- AI
   UPDATE links SET categoria = 'AI' WHERE categoria IN
   ('IA', 'AI', 'artificial intelligence', 'machine learning');

   -- Food
   UPDATE links SET categoria = 'Food' WHERE categoria IN
   ('Food', 'Receita', 'comida', 'cooking', 'cozinha');

   -- [continuar para as outras 11...]

Veja arquivo: categorias_padrao.json para lista completa

================================================================================
OPCAO B: Via Script Python (Automatico)
──────────────────────────────────────────────

1. Configure as variáveis de ambiente do Railway:

   Opção B1: Usar DATABASE_URL
   ──────────────────────────
   Copie a DATABASE_URL do Railway:

   a) Railway → PostgreSQL → Variables
   b) Copie o valor de DATABASE_URL
   c) Execute no PowerShell:

      $env:DATABASE_URL = "postgresql://user:pass@host:5432/dbname"
      python sync_railway_db.py

   Opção B2: Usar credenciais individuais
   ──────────────────────────────────────

   $env:DB_HOST = "seu-host-railway.railway.app"
   $env:DB_PORT = "5432"
   $env:DB_NAME = "seu-banco"
   $env:DB_USER = "seu-user"
   $env:DB_PASSWORD = "sua-senha"

   python sync_railway_db.py

================================================================================
COMO OBTER AS CREDENCIAIS DO RAILWAY:
================================================================================

1. Acesse: https://railway.app
2. Entre no projeto "Banco de Links"
3. Clique em "PostgreSQL"
4. Clique em "Variables" ou "Data"
5. Procure por:
   - DATABASE_URL (tem tudo junto)
   OU
   - Postgres_User
   - Postgres_Password
   - Postgres_Host
   - Postgres_Port
   - Postgres_DB

6. Copie os valores

================================================================================
VERIFICAR SE SINCRONIZOU:
================================================================================

Após sincronizar, acesse o site:

https://seu-railway-url/api/search?q=python

E verifique se os links agora tem categorias PADRAO:
✓ Tech (não "Tecnologia")
✓ AI (não "IA")
✓ Food (não "Receita")
✓ Video (não "Vídeo")
etc.

Se ainda estão as categorias antigas, sincronização falhou.

================================================================================
SE FALHAR:
================================================================================

1. Verifique as credenciais:
   - DATABASE_URL está correta?
   - Senha não tem caracteres especiais não escapados?

2. Tente pelo Railway Console (Opção A) manualmente

3. Contate suporte do Railway se problema persistir

================================================================================
PRONTO!
================================================================================

Após sincronizar:
  ✓ Novo codigo com Fable 5 está rodando
  ✓ Banco tem 15 categorias padrão
  ✓ Novos links serão categorizados corretamente
  ✓ Custo de API reduzido em 90%

Próximo passo: Redesign Cards v3! 🎨

================================================================================
