import ply.lex as lex
import ply.yacc as yacc
from dicionario import DICIONARIO

# Definição dos tokens
tokens = ('HANZI', 'PONTUACAO')

def t_HANZI(t):
    r'[\u4e00-\u9fff]+'
    return t

t_PONTUACAO = r'[。？！]'

t_ignore = ' \t'

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Regras gramaticais para pedidos em restaurantes
def p_frase(p):
    'frase : frase HANZI'
    p[0] = p[1] + [p[2]]

def p_frase_hanzi(p):
    'frase : HANZI'
    p[0] = [p[1]]

def p_frase_pontuacao(p):
    'frase : frase PONTUACAO'
    p[0] = p[1]

def p_frase_composta(p):
    'frase : frase HANZI frase'
    p[0] = p[1] + [p[2]] + p[3]

def p_error(p):
    print("Erro de sintaxe")

parser = yacc.yacc()

def traduzir(frase):
    tokens = parser.parse(frase)
    if tokens:
        pinyin = [DICIONARIO.get(tok, (tok, tok))[0] for tok in tokens]
        traducao = [DICIONARIO.get(tok, (tok, tok))[1] for tok in tokens]
        return " ".join(pinyin), " ".join(traducao)
    return "", ""

# Testes com frases de restaurante
frases_teste = [
    "我要一份米饭。",
    "请给我一杯茶。",
    "我要点咖啡。",
    "谢谢，再见！",
    "这道菜好吃！",
    "我想吃饺子。",
    "请给我一份牛肉面。",
    "我要一杯果汁。",
    "这个蛋糕很甜。"
]

for frase in frases_teste:
    pinyin, traducao = traduzir(frase)
    print(f"Entrada: {frase}")
    print(f"Pinyin: {pinyin}")
    print(f"Tradução: {traducao}\n")
