import React from 'react';
import BookCard from '../BookCard/BookCard';
import styles from './ResultsDisplay.module.css';

/**
 * ResultsDisplay - Muestra las recomendaciones obtenidas del backend
 *
 * Props:
 * - recommendations: object - Respuesta del API con estructura:
 *   {
 *     original_book: string,
 *     recommendations: Array<{ title, author, sentiment_score, reason }>,
 *     analysis_summary: string
 *   }
 * - originalBook: string - Título del libro que el usuario buscó
 *
 * Renders:
 * - Encabezado con título del libro buscado
 * - Resumen del análisis
 * - Grid de BookCard para cada recomendación
 * - Footer con información
 */
function ResultsDisplay({ recommendations, originalBook }) {
  if (!recommendations || !recommendations.recommendations) {
    return null;
  }

  const books = recommendations.recommendations;

  return (
    <section className={styles.results}>
      <div className={styles.results__header}>
        <h2 className={styles.results__title}>
          📖 Recomendaciones para:
          <span className={styles.results__book}>{originalBook}</span>
        </h2>

        {recommendations.analysis_summary && (
          <p className={styles.results__summary}>
            {recommendations.analysis_summary}
          </p>
        )}
      </div>

      <div className={styles.results__grid}>
        {books.map((book, index) => (
          <BookCard key={`${book.title}-${index}`} book={book} position={index + 1} />
        ))}
      </div>

      <div className={styles.results__footer}>
        <p className={styles.results__footer__text}>
          ✨ Estos libros fueron seleccionados porque comparten impacto emocional
          similar basado en análisis de miles de reseñas
        </p>
      </div>
    </section>
  );
}

export default ResultsDisplay;
