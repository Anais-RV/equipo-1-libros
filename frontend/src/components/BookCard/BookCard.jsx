import React from 'react';
import styles from './BookCard.module.css';

/**
 * BookCard - Tarjeta individual para mostrar una recomendación
 *
 * Props:
 * - book: object - Objeto con { title, author, sentiment_score, reason }
 * - position: number - Número de posición (1-5) para ranking visual
 *
 * Muestra:
 * - Número de ranking
 * - Título y autor
 * - Barra visual de sentiment score
 * - Razón de la recomendación
 */
function BookCard({ book, position }) {
  // Colores según similaridad emocional
  const getSentimentColor = (score) => {
    if (score >= 0.8) return 'var(--color-success)';     // Verde
    if (score >= 0.65) return 'var(--color-accent)';     // Dorado
    if (score >= 0.5) return 'var(--color-warning)';     // Ámbar
    return 'var(--color-secondary)';                      // Cobre
  };

  const percentageScore = Math.min(book.sentiment_score * 100, 100);
  const sentimentColor = getSentimentColor(book.sentiment_score);

  return (
    <article className={styles.card}>
      <div className={styles.card__rank}>
        <span className={styles.card__rank__number}>{position}</span>
      </div>

      <div className={styles.card__content}>
        <div className={styles.card__header}>
          <h3 className={styles.card__title}>{book.title}</h3>
          <p className={styles.card__author}>— {book.author}</p>
        </div>

        <div className={styles.card__sentiment}>
          <div className={styles.card__sentiment__bar}>
            <div
              className={styles.card__sentiment__fill}
              style={{
                width: `${percentageScore}%`,
                backgroundColor: sentimentColor
              }}
              role="progressbar"
              aria-valuenow={percentageScore}
              aria-valuemin="0"
              aria-valuemax="100"
              aria-label={`Similitud emocional: ${percentageScore.toFixed(0)}%`}
            />
          </div>
          <span className={styles.card__sentiment__label}>
            {percentageScore.toFixed(0)}% Match
          </span>
        </div>

        <p className={styles.card__reason}>
          <span className={styles.card__reason__icon}>💭</span>
          {book.reason}
        </p>
      </div>
    </article>
  );
}

export default BookCard;
