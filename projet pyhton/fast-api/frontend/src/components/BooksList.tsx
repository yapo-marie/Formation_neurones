import React, { useEffect, useState } from 'react'
import api from '../api'

type Book = {
  title: string
  author: string
  category: string
}

const BooksList: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await api.get<Book[]>('/books')
        setBooks(response.data)
      } catch (err) {
        console.error(err)
        setError('Failed to fetch books')
      } finally {
        setLoading(false)
      }
    }

    fetchBooks()
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <h2>Books List</h2>
      <ul>
        {books.map((book, idx) => (
          <li key={idx}>
            <strong>{book.title}</strong> by {book.author} ({book.category})
          </li>
        ))}
      </ul>
    </div>
  )
}

export default BooksList
