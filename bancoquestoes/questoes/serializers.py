from rest_framework import serializers
from .models import Categoria, Tag, Questao, Alternativa

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        # Não pedimos a 'questao' aqui pois ela será preenchida automaticamente
        fields = ['id', 'texto', 'is_correta'] 

class QuestaoSerializer(serializers.ModelSerializer):
    # Permite ler e criar as alternativas junto com a questão no mesmo JSON
    alternativas = AlternativaSerializer(many=True)

    class Meta:
        model = Questao
        fields = '__all__'
        read_only_fields = ['autor', 'criada_em', 'atualizada_em']

    def create(self, validated_data):
        # Separa as alternativas e tags dos dados da questão
        alternativas_data = validated_data.pop('alternativas')
        tags_data = validated_data.pop('tags', [])
        
        # Cria a questão
        questao = Questao.objects.create(**validated_data)
        
        # Adiciona as tags
        for tag in tags_data:
            questao.tags.add(tag)
            
        # Cria as alternativas vinculadas à questão
        for alt_data in alternativas_data:
            Alternativa.objects.create(questao=questao, **alt_data)
            
        return questao