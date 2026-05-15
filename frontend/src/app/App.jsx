import React, { useState } from 'react';
import axios from 'axios';
import { Book } from 'lucide-react';
import '../styles/global.css';
import styles from './App.module.css';
import RecommendationForm from '../components/RecommendationForm/RecommendationForm';
import ResultsDisplay from '../components/ResultsDisplay/ResultsDisplay';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';

function App() {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [originalBook, setOriginalBook] = useState('');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleSubmit = async (bookTitle, description) => {
    setLoading(true);
    setError(null);
    setOriginalBook(bookTitle);

    try {
      const response = await axios.post(`${API_URL}/recommend`, {
        title: bookTitle,
        description: description
      });

      setRecommendations(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Error al conectar con el backend. ¿Está corriendo el servidor?'
      );
      setRecommendations(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.app}>
      <header className={styles.app__header}>
        <div className={styles.app__titleContainer}>
          <Book className={styles.app__icon} size={40} />
          <h1 className={styles.app__title}>Sistema de Recomendación de Libros</h1>
        </div>
        <p className={styles.app__subtitle}>
          Descubre joyas ocultas basado en análisis de sentimientos emocionales
        </p>
      </header>

      <main className={styles.app__main}>
        <div className={styles.app__container}>
          <RecommendationForm onSubmit={handleSubmit} disabled={loading} />

          {loading && <LoadingSpinner />}
          {error && <div className={styles.app__error}>{error}</div>}
          {recommendations && (
            <ResultsDisplay
              recommendations={recommendations}
              originalBook={originalBook}
            />
          )}
        </div>
      </main>

      <footer className={styles.app__footer}>
        <p>Análisis de 63,014 reviews de Goodreads | Data Analyst Bootcamp</p>
      </footer>
    </div>
  );
}

export default App;
