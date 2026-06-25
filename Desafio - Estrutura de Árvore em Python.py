class Node:
    def __init__(self, content):
        self.left: "Node" = None
        self.right: "Node" = None
        self.content: str = content


class Tree:
    def __init__(self):
        self.root: Node = None

    def add(self, content, root=None):
        if self.root is None:
            self.root = Node(content)
            return

        if root is None:
            root = self.root

        if content > root.content:
            if root.right is None:
                root.right = Node(content)
            else:
                self.add(content, root.right)
        else:
            if root.left is None:
                root.left = Node(content)
            else:
                self.add(content, root.left)

    def printTree(self, root=None):
        if root is None:
            root = self.root

        if root.left is not None:
            self.printTree(root.left)

        print(root.content)

        if root.right is not None:
            self.printTree(root.right)

    def PrintPreOrder(self, root=None):
        if root is None:
            root = self.root

        print(root.content)

        if root.left is not None:
            self.PrintPreOrder(root.left)

        if root.right is not None:
            self.PrintPreOrder(root.right)

    def remove_at(self, content: str) -> bool:
        if self.root is None:
            print("A árvore está vazia. Nenhum cargo para remover.")
            return False

        self.root, removed = self._delete_node(self.root, content)

        if removed:
            print(f"Cargo '{content}' removido com sucesso.")
        else:
            print(f"Cargo '{content}' não encontrado na árvore.")

        return removed

    def _delete_node(self, node: Node, content: str):
        if node is None:
            return None, False

        removed = False

        if content < node.content:
            node.left, removed = self._delete_node(node.left, content)
        elif content > node.content:
            node.right, removed = self._delete_node(node.right, content)
        else:
            removed = True

            if node.left is None:
                return node.right, removed
            if node.right is None:
                return node.left, removed

            successor = self._min_node(node.right)
            node.content = successor.content
            node.right, _ = self._delete_node(node.right, successor.content)

        return node, removed

    def _min_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current


def build_org_chart() -> Tree:
    org = Tree()

    org.add("CEO")
    org.add("CFO")
    org.add("COO")
    org.add("Diretor Financeiro")
    org.add("Diretor Operacional")
    org.add("Diretor de TI")
    org.add("Diretor de RH")
    org.add("Gerente de Contabilidade")
    org.add("Gerente de Logistica")
    org.add("Analista de Sistemas")
    org.add("Analista de RH")

    return org


def show_menu():
    print("\n" + "=" * 50)
    print("   ORGANOGRAMA EMPRESARIAL — MENU PRINCIPAL")
    print("=" * 50)
    print("  1. Exibir organograma (ordem crescente)")
    print("  2. Exibir organograma (pré-ordem)")
    print("  3. Remover cargo")
    print("  4. Adicionar cargo (inserção BST padrão)")
    print("  0. Sair")
    print("=" * 50)


def main():
    print("\nBem-vindo ao sistema de Organograma Empresarial!")
    print("Carregando estrutura inicial da empresa...")

    org = build_org_chart()
    print("Estrutura carregada com sucesso.\n")

    while True:
        show_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            print("\n--- Organograma (Ordem Crescente / In-Order) ---")
            org.printTree()

        elif choice == "2":
            print("\n--- Organograma (Pré-Ordem) ---")
            org.PrintPreOrder()

        elif choice == "3":
            emp = input("Nome do cargo a REMOVER: ").strip()
            org.remove_at(emp)

        elif choice == "4":
            emp = input("Nome do cargo a ADICIONAR (inserção BST automática): ").strip()
            org.add(emp)
            print(f"Cargo '{emp}' adicionado ao organograma.")

        elif choice == "0":
            print("\nEncerrando o sistema. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha um número entre 0 e 4.")


if __name__ == "__main__":
    main()