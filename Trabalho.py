from collections import defaultdict, deque

# Lê o arquivo de entrada e monta o grafo
def carregar_grafo(caminho):
    grafo = defaultdict(list)
    with open(caminho, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()
            if partes:
                grafo[partes[0]] += partes[1:]
    return grafo

# Verifica se o grafo possui ciclos (usando DFS)
def tem_ciclo(grafo):
    visitado = set()
    pilha = set()

    def dfs(v):
        visitado.add(v)
        pilha.add(v)
        for viz in grafo.get(v, []):
            if viz not in visitado:
                if dfs(viz):
                    return True
            elif viz in pilha:
                return True
        pilha.remove(v)
        return False

    for v in list(grafo.keys()):
        if v not in visitado:
            if dfs(v):
                return True
    return False

# Ordenação topológica (Kahn)
def ordenacao_topologica(grafo):
    grau = defaultdict(int)
    for u in grafo:
        for v in grafo[u]:
            grau[v] += 1
    fila = deque([v for v in grafo if grau[v] == 0])
    ordem = []

    while fila:
        atual = fila.popleft()
        ordem.append(atual)
        for viz in grafo[atual]:
            grau[viz] -= 1
            if grau[viz] == 0:
                fila.append(viz)

    if len(ordem) != len(grafo):
        return None
    return ordem

# Busca todas as dependências diretas e indiretas
def dependencias(grafo, pacote):
    visitado = set()
    def dfs(v):
        for viz in grafo.get(v, []):
            if viz not in visitado:
                visitado.add(viz)
                dfs(viz)
    dfs(pacote)
    return visitado

# Identifica ciclos usando algoritmo de Tarjan (SCC)
def encontrar_ciclos(grafo):
    index = [0]
    indices, lowlinks = {}, {}
    pilha, em_pilha, ciclos = [], set(), []

    def strongconnect(v):
        indices[v] = index[0]
        lowlinks[v] = index[0]
        index[0] += 1
        pilha.append(v)
        em_pilha.add(v)

        for w in grafo.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in em_pilha:
                lowlinks[v] = min(lowlinks[v], indices[w])

        if lowlinks[v] == indices[v]:
            componente = []
            while True:
                w = pilha.pop()
                em_pilha.remove(w)
                componente.append(w)
                if w == v:
                    break
            if len(componente) > 1:
                ciclos.append(componente)

    for v in grafo:
        if v not in indices:
            strongconnect(v)
    return ciclos

# Simula remoção de um pacote e seus impactados
def remover_pacote(grafo, pacote):
    grafo_reverso = defaultdict(list)
    for u in grafo:
        for v in grafo[u]:
            grafo_reverso[v].append(u)

    impactados = set()
    def dfs(v):
        for dep in grafo_reverso.get(v, []):
            if dep not in impactados:
                impactados.add(dep)
                dfs(dep)
    dfs(pacote)
    return impactados

# Identifica pacotes com mais dependentes
def pacotes_criticos(grafo):
    grafo_reverso = defaultdict(list)
    for u in grafo:
        for v in grafo[u]:
            grafo_reverso[v].append(u)

    def contar_dependentes(pacote):
        visitado = set()
        def dfs(v):
            for dep in grafo_reverso.get(v, []):
                if dep not in visitado:
                    visitado.add(dep)
                    dfs(dep)
        dfs(pacote)
        return len(visitado)

    dependentes = {p: contar_dependentes(p) for p in grafo}
    max_dep = max(dependentes.values(), default=0)
    criticos = [p for p, qtd in dependentes.items() if qtd == max_dep]
    return criticos, max_dep

# Menu principal do programa
def menu():
    grafo = carregar_grafo("TP_Grafos_1Sem2025_ArquivoEntrada.txt")

    while True:
        print("\nMenu:")
        print("1 - Verificar se há ciclos")
        print("2 - Mostrar ordem de instalação")
        print("3 - Mostrar dependências de um pacote")
        print("4 - Identificar ciclos (componentes fortemente conectados)")
        print("5 - Simular remoção de um pacote")
        print("6 - Identificar pacotes críticos")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            print("❌ Há ciclos!" if tem_ciclo(grafo) else "✅ Grafo é acíclico.")
        elif opcao == "2":
            ordem = ordenacao_topologica(grafo)
            if ordem:
                print("Ordem de instalação:", " -> ".join(ordem))
            else:
                print("Não é possível ordenar (há ciclos).")
        elif opcao == "3":
            pacote = input("Nome do pacote: ")
            if pacote not in grafo:
                print("Pacote não encontrado.")
            else:
                deps = dependencias(grafo, pacote)
                print("Dependências:", ", ".join(deps) if deps else "Nenhuma.")
        elif opcao == "4":
            ciclos = encontrar_ciclos(grafo)
            if ciclos:
                print("Ciclos encontrados:")
                for c in ciclos:
                    print(" - " + ", ".join(c))
            else:
                print("Nenhum ciclo encontrado.")
        elif opcao == "5":
            pacote = input("Nome do pacote a remover: ")
            if pacote not in grafo:
                print("Pacote não encontrado.")
            else:
                afetados = remover_pacote(grafo, pacote)
                print("Pacotes impactados:", ", ".join(afetados) if afetados else "Nenhum.")
        elif opcao == "6":
            criticos, qtd = pacotes_criticos(grafo)
            print(f"Pacotes críticos ({qtd} dependentes):", ", ".join(criticos))
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

# Executa o programa
if __name__ == "__main__":
    menu()
