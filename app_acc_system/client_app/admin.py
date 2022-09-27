from django.contrib import admin
from .models import (ClientFiles, ContractFiles, EquipmentFiles, ContactPersons,
                     EquipmentType, EquipmentAttribute, Equipments, Contracts, Clients)


@admin.register(ClientFiles)
class ClientFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'client', 'title', 'file', 'created_at']
    list_display_links = ['id', 'slug']
    list_filter = ['client', 'created_at', 'title']
    search_fields = ['title']
    save_as = True


@admin.register(ContractFiles)
class ContractFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'contract', 'title', 'file', 'created_at']
    list_display_links = ['id', 'slug']
    list_filter = ['contract', 'created_at', 'title']
    search_fields = ['title']
    save_as = True


@admin.register(EquipmentFiles)
class EquipmentFilesAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'equipment', 'title', 'file', 'created_at']
    list_display_links = ['id', 'slug']
    list_filter = ['equipment', 'created_at', 'title']
    search_fields = ['title']
    save_as = True


@admin.register(ContactPersons)
class ContactPersonsAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'first_name', 'second_name', 'post', 'email', 'phone', 'created_at']
    list_display_links = ['id']
    list_filter = ['client', 'created_at']
    search_fields = ['first_name', 'second_name']
    save_as = True


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    list_display_links = ['id', 'code']
    list_filter = ['code', 'name']
    search_fields = ['name', 'code']
    save_as = True


@admin.register(EquipmentAttribute)
class EquipmentAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'type_a']
    list_display_links = ['id', 'code']
    list_filter = ['code', 'name']
    search_fields = ['name', 'code']
    save_as = True


@admin.register(Equipments)
class EquipmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'client', 'name', 'type']
    list_display_links = ['id', 'slug']
    list_filter = ['client', 'type']
    search_fields = ['name']
    save_as = True


@admin.register(Contracts)
class ContractsAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'client', 'title', 'price', 'created_at', 'is_end', 'date_end']
    list_display_links = ['id', 'slug']
    list_filter = ['client', 'created_at', 'title', 'is_end']
    search_fields = ['title']
    save_as = True


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'name', 'email', 'phone', 'created_at']
    list_display_links = ['id', 'slug']
    list_filter = ['name', 'created_at']
    search_fields = ['name']
    save_as = True
