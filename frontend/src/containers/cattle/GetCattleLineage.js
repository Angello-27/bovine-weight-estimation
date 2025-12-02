// frontend/src/containers/cattle/GetCattleLineage.js

import { useState, useEffect } from 'react';
import { getCattleById } from '../../services/cattle';

/**
 * GetCattleLineage container hook - Obtiene el linaje (padre y madre) de un animal
 * @param {Object} cattle - Datos del animal con father_id y mother_id
 * @returns {Object} { father, mother, loading, error }
 */
function GetCattleLineage(cattle) {
    const [father, setFather] = useState(null);
    const [mother, setMother] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!cattle) {
            setFather(null);
            setMother(null);
            setLoading(false);
            return;
        }

        const fetchLineage = async () => {
            setLoading(true);
            setError(null);
            try {
                const promises = [];
                
                if (cattle.father_id) {
                    promises.push(
                        getCattleById(cattle.father_id)
                            .then(data => ({ type: 'father', data }))
                            .catch(err => ({ type: 'father', error: err }))
                    );
                }
                
                if (cattle.mother_id) {
                    promises.push(
                        getCattleById(cattle.mother_id)
                            .then(data => ({ type: 'mother', data }))
                            .catch(err => ({ type: 'mother', error: err }))
                    );
                }

                const results = await Promise.all(promises);
                
                results.forEach(result => {
                    if (result.type === 'father') {
                        if (result.error) {
                            console.error('Error al obtener padre:', result.error);
                        } else {
                            setFather(result.data);
                        }
                    } else if (result.type === 'mother') {
                        if (result.error) {
                            console.error('Error al obtener madre:', result.error);
                        } else {
                            setMother(result.data);
                        }
                    }
                });
            } catch (err) {
                setError(err.message);
                console.error('Error al obtener linaje:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchLineage();
    }, [cattle?.id, cattle?.father_id, cattle?.mother_id]);

    return { father, mother, loading, error };
}

export default GetCattleLineage;

