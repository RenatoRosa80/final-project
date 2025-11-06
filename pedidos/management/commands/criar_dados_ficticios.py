from django.core.management.base import BaseCommand
from pedidos.models import Categoria, ItemCardapio, Mesa

class Command(BaseCommand):
    help = 'Cria dados fictícios para o cardápio'

    def handle(self, *args, **options):
        # Criar categorias
        categorias_data = [
            {'nome': 'Entradas', 'tipo': 'ENTRADA'},
            {'nome': 'Pratos Principais', 'tipo': 'PRATO'},
            {'nome': 'Sobremesas', 'tipo': 'SOBREMESA'},
            {'nome': 'Bebidas', 'tipo': 'BEBIDA'},
        ]
        
        for cat_data in categorias_data:
            Categoria.objects.get_or_create(**cat_data)
        
        # Criar itens do cardápio
        itens_data = [
            # Entradas
            {'nome': 'Bruschetta', 'preco': 18.90, 'categoria': 'Entradas'},
            {'nome': 'Carpaccio', 'preco': 32.50, 'categoria': 'Entradas'},
            {'nome': 'Salada Caesar', 'preco': 24.90, 'categoria': 'Entradas'},
            
            # Pratos Principais
            {'nome': 'Filé Mignon', 'preco': 89.90, 'categoria': 'Pratos Principais'},
            {'nome': 'Risotto de Cogumelos', 'preco': 45.90, 'categoria': 'Pratos Principais'},
            {'nome': 'Salmão Grelhado', 'preco': 67.50, 'categoria': 'Pratos Principais'},
            {'nome': 'Lasanha Bolonhesa', 'preco': 38.90, 'categoria': 'Pratos Principais'},
            
            # Sobremesas
            {'nome': 'Tiramisu', 'preco': 22.90, 'categoria': 'Sobremesas'},
            {'nome': 'Brownie com Sorvete', 'preco': 18.50, 'categoria': 'Sobremesas'},
            {'nome': 'Cheesecake', 'preco': 19.90, 'categoria': 'Sobremesas'},
            
            # Bebidas
            {'nome': 'Suco Natural', 'preco': 12.90, 'categoria': 'Bebidas'},
            {'nome': 'Refrigerante', 'preco': 8.90, 'categoria': 'Bebidas'},
            {'nome': 'Cerveja Artesanal', 'preco': 18.90, 'categoria': 'Bebidas'},
            {'nome': 'Vinho da Casa', 'preco': 45.90, 'categoria': 'Bebidas'},
        ]
        
        for item_data in itens_data:
            categoria = Categoria.objects.get(nome=item_data.pop('categoria'))
            ItemCardapio.objects.get_or_create(
                categoria=categoria,
                nome=item_data['nome'],
                defaults=item_data
            )
        
        # Criar mesas
        for i in range(1, 11):
            Mesa.objects.get_or_create(
                numero=i,
                defaults={'capacidade': 4}
            )
        
        self.stdout.write(
            self.style.SUCCESS('Dados fictícios criados com sucesso!')
        )