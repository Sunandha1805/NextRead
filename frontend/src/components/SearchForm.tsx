import React, { useState } from 'react';

interface SearchFormProps {
  onSearch: (query: string, category: string, emotion: string) => void;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [emotion, setEmotion] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query, category, emotion);
  };

  return (
    <form className="search-container" onSubmit={handleSubmit}>
      <div className="search-box">
        <input 
          type="text" 
          placeholder="What kind of books are you looking for?" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
        />
      </div>

      <div className="filters">
        <div className="filter-group">
          <label>Category</label>
          <input 
            list="category-options"
            placeholder="Any Category" 
            value={category} 
            onChange={(e) => setCategory(e.target.value)} 
          />
          <datalist id="category-options">
            <option value="Fiction" />
            <option value="Business" />
            <option value="Science" />
            <option value="Philosophy" />
            <option value="History" />
            <option value="Biography" />
          </datalist>
        </div>

        <div className="filter-group">
          <label>Mood/Emotion</label>
          <input 
            list="emotion-options"
            placeholder="Any Mood" 
            value={emotion} 
            onChange={(e) => setEmotion(e.target.value)} 
          />
          <datalist id="emotion-options">
            <option value="joy" />
            <option value="sadness" />
            <option value="fear" />
            <option value="surprise" />
            <option value="anger" />
            <option value="neutral" />
          </datalist>
        </div>
      </div>

      <button type="submit" className="btn-search">Get Recommendations</button>
    </form>
  );
};

export default SearchForm;
