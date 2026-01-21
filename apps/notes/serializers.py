from rest_framework import serializers
from .models import Note, Tag


class TagSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'owner']

    def validate(self, attrs):
        owner = self.context['request'].user
        name = attrs.get('name')

        qs = Tag.objects.filter(owner=owner, name=name)
        # исключаем себя при update
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({"name": "You already have a tag with this name."})
        
        return attrs


class NoteSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tags_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False  # необязательное поле
    )

    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'owner', 'tags', 'tags_ids', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        owner = self.context['request'].user
        title = attrs.get('title')
        tags = attrs.get('tags_ids', [])

        qs = Note.objects.filter(owner=owner, title=title)
        # исключаем себя при update
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({"title": "You already have a note with this title."})

        # проверяем, что все теги принадлежат владельцу
        for tag in tags:
            if tag.owner != owner:
                raise serializers.ValidationError({"tags_ids": f"Tag '{tag.id}' does not belong to you."})

        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags_ids', [])
        note = Note.objects.create(**validated_data)
        note.tags.set(tags)
        return note

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance