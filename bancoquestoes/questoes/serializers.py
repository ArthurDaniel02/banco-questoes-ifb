from rest_framework import serializers
from .models import Categoria, Tag, Questao, Alternativa, Midia

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
        fields = ['id', 'texto', 'is_correta', 'feedback'] 

class QuestaoSerializer(serializers.ModelSerializer):
    alternativas = AlternativaSerializer(many=True)

    class Meta:
        model = Questao
        fields = '__all__'
        read_only_fields = ['autor', 'criada_em', 'atualizada_em']

    def validate_alternativas(self, alternativas):
        """
        Garante que a questão tenha exatamente 5 alternativas e apenas 1 correta.
        """
        if len(alternativas) != 5:
            raise serializers.ValidationError("Uma questão de múltipla escolha deve ter exatamente 5 alternativas.")

        # Conta quantas alternativas vieram com 'is_correta = True'
        qtd_corretas = sum(1 for alt in alternativas if alt.get('is_correta', False))
        
        if qtd_corretas != 1:
            raise serializers.ValidationError("A questão deve ter exatamente uma alternativa marcada como correta.")

        return alternativas


    def create(self, validated_data):
        alternativas_data = validated_data.pop('alternativas')
        tags_data = validated_data.pop('tags', [])

        questao = Questao.objects.create(**validated_data)

        for tag in tags_data:
            questao.tags.add(tag)
   
        for alt_data in alternativas_data:
            Alternativa.objects.create(questao=questao, **alt_data)
            
        return questao