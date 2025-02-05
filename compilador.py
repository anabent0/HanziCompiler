import ply.lex as lex
import ply.yacc as yacc
from dicionario import DICIONARIO

# Definição dos tokens
tokens = ('PRONOME', 'VERBO', 'SUBSTANTIVO', 'PONTUACAO')

# Expressões regulares para cada categoria gramatical
def t_PRONOME(t):
    r'我|你|他|她|我们|你们|他们'
    return t

def t_VERBO(t):
    r'要|吃|喝|点|喜欢|去|看|学习|做'
    return t

def t_SUBSTANTIVO(t):
    r'米饭|茶|咖啡|饺子|牛肉面|果汁|蛋糕|学校|电影|书|朋友|老师|学生|饭馆|桌子|椅子'
    return t

t_PONTUACAO = r'[。，？！]'

t_ignore = ' \t'

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Regras gramaticais separadas em categorias
def p_frase(p):
    '''frase : pronome verbo substantivo PONTUACAO
             | pronome verbo substantivo'''
    p[0] = p[1:]  # Mantém a estrutura sintática

def p_pronome(p):
    'pronome : PRONOME'
    p[0] = p[1]

def p_verbo(p):
    'verbo : VERBO'
    p[0] = p[1]

def p_substantivo(p):
    'substantivo : SUBSTANTIVO'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe: Token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Entrada inesperada (fim do arquivo?)")

parser = yacc.yacc()

# Funções de tradução separadas
def traduzir_hanzi(frase):
    tokens = parser.parse(frase)
    return " ".join(tokens) if tokens else ""

def traduzir_pinyin(frase):
    tokens = parser.parse(frase)
    return " ".join(DICIONARIO.get(tok, (tok, tok))[0] for tok in tokens) if tokens else ""

def traduzir_pt(frase):
    tokens = parser.parse(frase)
    return " ".join(DICIONARIO.get(tok, (tok, tok))[1] for tok in tokens) if tokens else ""

frase_usuario = input("Digite uma frase em chinês: ")
print(f"\nEntrada: {frase_usuario}")
print(f"Hanzi: {traduzir_hanzi(frase_usuario)}")
print(f"Pinyin: {traduzir_pinyin(frase_usuario)}")
print(f"Tradução: {traduzir_pt(frase_usuario)}\n")
