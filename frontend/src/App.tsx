import './App.css'
import { useState } from 'react'
import SearchForm from './components/SearchForm'
import BookList from './components/BookList'
import axios from 'axios'

interface Book {
  title: string
  authors: string
  thumbnail: string
}

function App() {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (query: string, category: string, emotion: string) => {
    setLoading(true)
    setError('')
    try{
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/recommend`, {
        query: query,
        category: category || null,
        emotion: emotion || null
      })
      setBooks(response.data.recommendations)
    } catch (err){
      setError('Something went wrong. Please try again.')
      console.error(err)
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <header className="hero">
        <h1>NextRead</h1>
        <p>Discover books that match your curiosity and mood.</p>
      </header>

      <SearchForm onSearch={handleSearch} />
      {loading && <p className='loading'>Finding books for you...</p>}
      {error && <p className='error'>{error}</p>}
      {books.length > 0 && <BookList books={books}/>}
    </div>
  )
}

export default App