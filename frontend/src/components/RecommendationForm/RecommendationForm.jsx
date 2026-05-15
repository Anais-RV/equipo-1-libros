import React, { useState } from 'react';
import styles from './RecommendationForm.module.css';

/**
 * RecommendationForm - Componente para capturar búsqueda del usuario
 *
 * Props:
 * - onSubmit: function(bookTitle, description) - callback cuando usuario envía
 * - disabled: boolean - deshabilita form mientras se procesa
 *
 * Estado interno:
 * - bookTitle: string - título del libro
 * - description: string - descripción por qué le gustó
 */
function RecommendationForm({ onSubmit, disabled }) {
  const [bookTitle, setBookTitle] = useState('');
  const [description, setDescription] = useState('Un libro que me encantó');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (bookTitle.trim()) {
      onSubmit(bookTitle, description);
      // Opcional: limpiar form después
      // setBookTitle('');
    }
  };

  return (
    <div className={styles.form}>
      <div className={styles.form__header}>
        <h2 className={styles.form__title}>¿Qué libro te encantó?</h2>
        <p className={styles.form__subtitle}>
          Cuéntanos un libro que amaste y descubriremos joyas similares
        </p>
      </div>

      <form onSubmit={handleSubmit} className={styles.form__content}>
        <div className={styles.form__group}>
          <label htmlFor="bookTitle" className={styles.form__label}>
            Título del libro
          </label>
          <input
            id="bookTitle"
            type="text"
            value={bookTitle}
            onChange={(e) => setBookTitle(e.target.value)}
            placeholder="Ej: The Midnight Library"
            disabled={disabled}
            required
            className={styles.form__input}
          />
        </div>

        <div className={styles.form__group}>
          <label htmlFor="description" className={styles.form__label}>
            ¿Por qué te gustó?
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe brevemente qué te emocionó de este libro..."
            disabled={disabled}
            className={styles.form__textarea}
            rows="3"
          />
          <p className={styles.form__hint}>
            Esta descripción nos ayuda a entender mejor el contexto emocional
          </p>
        </div>

        <button
          type="submit"
          disabled={disabled || !bookTitle.trim()}
          className={`${styles.form__button} ${
            disabled ? styles['form__button--loading'] : ''
          }`}
        >
          {disabled ? '✨ Analizando...' : '🔍 Obtener Recomendaciones'}
        </button>
      </form>

      <div className={styles.form__info}>
        <p className={styles.form__info__text}>
          💡 Nuestro sistema analiza más de 63,000 reseñas para encontrar libros
          con impacto emocional similar
        </p>
      </div>
    </div>
  );
}

export default RecommendationForm;
