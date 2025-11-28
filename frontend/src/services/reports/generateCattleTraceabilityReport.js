// frontend/src/services/reports/generateCattleTraceabilityReport.js

import jsPDF from 'jspdf';
import 'jspdf-autotable';

/**
 * Genera un reporte PDF de trazabilidad para un animal
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones de peso
 * @param {Array} timelineEvents - Eventos del timeline
 * @param {Object} father - Datos del padre (opcional)
 * @param {Object} mother - Datos de la madre (opcional)
 * @param {string} filename - Nombre del archivo (opcional)
 * @returns {Promise<void>}
 */
const generateCattleTraceabilityReport = async (
    cattle,
    estimations = [],
    timelineEvents = [],
    father = null,
    mother = null,
    filename = null
) => {
    if (!cattle) {
        throw new Error('Datos del animal son requeridos para generar el reporte');
    }

    // Crear documento PDF
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    let yPosition = 20;

    // Colores del proyecto
    const primaryColor = [37, 89, 70]; // #255946
    const secondaryColor = [73, 167, 96]; // #49A760

    // ===== ENCABEZADO =====
    doc.setFillColor(...primaryColor);
    doc.rect(0, 0, pageWidth, 40, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.text('Certificado de Trazabilidad', pageWidth / 2, 25, { align: 'center' });
    
    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    doc.text('Sistema de Gestión Ganadera', pageWidth / 2, 35, { align: 'center' });

    yPosition = 50;

    // ===== DATOS DEL ANIMAL =====
    doc.setTextColor(...primaryColor);
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Datos del Animal', 14, yPosition);
    yPosition += 10;

    doc.setTextColor(0, 0, 0);
    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');

    const calculateAge = (birthDate) => {
        if (!birthDate) return 'No registrada';
        const birth = new Date(birthDate);
        const today = new Date();
        const months = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
        return `${months} meses`;
    };

    const formatDate = (dateString) => {
        if (!dateString) return 'No registrada';
        return new Date(dateString).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const animalData = [
        ['Caravana:', cattle.ear_tag || 'N/A'],
        ['Nombre:', cattle.name || 'Sin nombre'],
        ['Raza:', cattle.breed || 'N/A'],
        ['Género:', cattle.gender === 'male' ? 'Macho' : 'Hembra'],
        ['Fecha de Nacimiento:', formatDate(cattle.birth_date)],
        ['Edad:', calculateAge(cattle.birth_date)],
        ['Peso al Nacer:', cattle.birth_weight_kg ? `${cattle.birth_weight_kg} kg` : 'No registrado'],
        ['Color:', cattle.color || 'No registrado'],
        ['Fecha de Registro:', formatDate(cattle.created_at || cattle.registration_date)],
    ];

    animalData.forEach(([label, value]) => {
        doc.setFont('helvetica', 'bold');
        doc.text(label, 14, yPosition);
        doc.setFont('helvetica', 'normal');
        doc.text(value, 70, yPosition);
        yPosition += 7;
    });

    yPosition += 5;

    // ===== LINAGE =====
    if (father || mother) {
        if (yPosition > pageHeight - 60) {
            doc.addPage();
            yPosition = 20;
        }

        doc.setTextColor(...primaryColor);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Linaje', 14, yPosition);
        yPosition += 10;

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(11);
        doc.setFont('helvetica', 'normal');

        if (father) {
            doc.setFont('helvetica', 'bold');
            doc.text('Padre:', 14, yPosition);
            doc.setFont('helvetica', 'normal');
            doc.text(`${father.ear_tag}${father.name ? ` - ${father.name}` : ''} (${father.breed})`, 50, yPosition);
            yPosition += 7;
        }

        if (mother) {
            doc.setFont('helvetica', 'bold');
            doc.text('Madre:', 14, yPosition);
            doc.setFont('helvetica', 'normal');
            doc.text(`${mother.ear_tag}${mother.name ? ` - ${mother.name}` : ''} (${mother.breed})`, 50, yPosition);
            yPosition += 7;
        }

        yPosition += 5;
    }

    // ===== HISTORIAL DE PESOS =====
    if (estimations && estimations.length > 0) {
        if (yPosition > pageHeight - 80) {
            doc.addPage();
            yPosition = 20;
        }

        doc.setTextColor(...primaryColor);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Historial de Pesos', 14, yPosition);
        yPosition += 10;

        // Preparar datos para la tabla
        const weightData = estimations.map(est => [
            formatDate(est.timestamp),
            `${est.estimated_weight?.toFixed(1) || 'N/A'} kg`,
            `${(est.confidence_score * 100).toFixed(0)}%`,
            est.method || 'tflite'
        ]);

        doc.autoTable({
            startY: yPosition,
            head: [['Fecha', 'Peso', 'Confianza', 'Método']],
            body: weightData,
            theme: 'striped',
            headStyles: {
                fillColor: primaryColor,
                textColor: [255, 255, 255],
                fontStyle: 'bold'
            },
            styles: {
                fontSize: 9
            }
        });

        yPosition = doc.lastAutoTable.finalY + 10;
    }

    // ===== TIMELINE DE EVENTOS =====
    if (timelineEvents && timelineEvents.length > 0) {
        if (yPosition > pageHeight - 60) {
            doc.addPage();
            yPosition = 20;
        }

        doc.setTextColor(...primaryColor);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Timeline de Eventos', 14, yPosition);
        yPosition += 10;

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');

        timelineEvents.forEach(event => {
            if (yPosition > pageHeight - 30) {
                doc.addPage();
                yPosition = 20;
            }

            const eventDate = formatDate(event.date);
            doc.setFont('helvetica', 'bold');
            doc.text(`${eventDate} - ${event.title}`, 14, yPosition);
            yPosition += 6;
            doc.setFont('helvetica', 'normal');
            doc.text(event.description, 20, yPosition);
            yPosition += 8;
        });
    }

    // ===== OBSERVACIONES =====
    if (cattle.observations) {
        if (yPosition > pageHeight - 50) {
            doc.addPage();
            yPosition = 20;
        }

        doc.setTextColor(...primaryColor);
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Observaciones', 14, yPosition);
        yPosition += 10;

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(11);
        doc.setFont('helvetica', 'normal');
        
        const splitObservations = doc.splitTextToSize(cattle.observations, pageWidth - 28);
        doc.text(splitObservations, 14, yPosition);
    }

    // ===== PIE DE PÁGINA =====
    const totalPages = doc.internal.pages.length - 1;
    for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(128, 128, 128);
        doc.text(
            `Generado el ${new Date().toLocaleDateString('es-ES')} - Página ${i} de ${totalPages}`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
        );
        doc.text(
            'Cumple normativas SENASAG - Sistema de Trazabilidad Ganadera',
            pageWidth / 2,
            pageHeight - 5,
            { align: 'center' }
        );
    }

    // ===== GUARDAR PDF =====
    const finalFilename = filename || `Trazabilidad_${cattle.ear_tag}_${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(finalFilename);
};

export default generateCattleTraceabilityReport;

