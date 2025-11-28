// frontend/src/containers/cattle/CombineCattleLoading.js

/**
 * CombineCattleLoading container hook - Combina estados de loading y error de múltiples containers
 * @param {...Object} containers - Múltiples objetos con propiedades loading y error
 * @returns {Object} { loading, error }
 */
function CombineCattleLoading(...containers) {
    const loading = containers.some(container => container?.loading === true);
    const error = containers
        .map(container => container?.error)
        .find(error => error !== null && error !== undefined) || null;

    return { loading, error };
}

export default CombineCattleLoading;

