// frontend/src/containers/cattle/ManageCattleForm.js

import { useState } from 'react';
import { getCattleById } from '../../services/cattle';

/**
 * ManageCattleForm container hook - Maneja el estado y acciones del formulario de ganado
 * @param {Object} formProps - Props del formulario de CreateNewCattle
 * @returns {Object} { showForm, showDeleteDialog, deleteItem, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm, handleCloseDeleteDialog }
 */
function ManageCattleForm(formProps) {
    const [showForm, setShowForm] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);

    const resetForm = () => {
        formProps.setFormData({
            id: '',
            ear_tag: '',
            breed: '',
            birth_date: '',
            gender: '',
            name: '',
            color: '',
            birth_weight_kg: '',
            observations: '',
            farm_id: '',
            status: 'active',
            mother_id: '',
            father_id: ''
        });
        formProps.resetErrors();
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = async (animalId, animalData) => {
        try {
            // Obtener datos completos del animal desde el backend para asegurar que tenemos todos los campos
            const fullAnimalData = await getCattleById(animalId);
            
            // Formatear fecha para el input date
            let birthDate = '';
            if (fullAnimalData.birth_date) {
                const date = new Date(fullAnimalData.birth_date);
                birthDate = date.toISOString().split('T')[0];
            }

            formProps.setFormData({
                id: animalId,
                ear_tag: fullAnimalData.ear_tag || '',
                breed: fullAnimalData.breed || '',
                birth_date: birthDate,
                gender: fullAnimalData.gender || '',
                name: fullAnimalData.name || '',
                color: fullAnimalData.color || '',
                birth_weight_kg: fullAnimalData.birth_weight_kg ? String(fullAnimalData.birth_weight_kg) : '',
                observations: fullAnimalData.observations || '',
                farm_id: fullAnimalData.farm_id || '',
                status: fullAnimalData.status || 'active',
                mother_id: fullAnimalData.mother_id || '',
                father_id: fullAnimalData.father_id || ''
            });
            formProps.resetErrors();
            setShowForm(true);
        } catch (error) {
            console.error('Error al cargar datos del animal:', error);
            // Si falla la carga, usar los datos de la lista como fallback
            let birthDate = '';
            if (animalData.birth_date) {
                const date = new Date(animalData.birth_date);
                birthDate = date.toISOString().split('T')[0];
            }

            formProps.setFormData({
                id: animalId,
                ear_tag: animalData.ear_tag || '',
                breed: animalData.breed || '',
                birth_date: birthDate,
                gender: animalData.gender || '',
                name: animalData.name || '',
                color: animalData.color || '',
                birth_weight_kg: animalData.birth_weight_kg ? String(animalData.birth_weight_kg) : '',
                observations: animalData.observations || '',
                farm_id: animalData.farm_id || '',
                status: animalData.status || 'active',
                mother_id: animalData.mother_id || '',
                father_id: animalData.father_id || ''
            });
            formProps.resetErrors();
            setShowForm(true);
        }
    };

    const handleDeleteClick = (animalId, animalData) => {
        setDeleteItem({ id: animalId, ...animalData });
        setShowDeleteDialog(true);
    };

    const handleCloseForm = () => {
        setShowForm(false);
        resetForm();
    };

    const handleCloseDeleteDialog = () => {
        setShowDeleteDialog(false);
        setDeleteItem(null);
    };

    return {
        showForm,
        showDeleteDialog,
        deleteItem,
        handleCreateClick,
        handleEditClick,
        handleDeleteClick,
        handleCloseForm,
        handleCloseDeleteDialog
    };
}

export default ManageCattleForm;

