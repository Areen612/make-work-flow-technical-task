import { useQuery } from '@tanstack/react-query'
import { createFileRoute } from '@tanstack/react-router'

type User = {
  id: number
  name: string
  email: string
  created_at: string
  updated_at: string
}

async function fetchUsers(): Promise<User[]> {
  const response = await fetch('http://localhost:8000/users')

  if (!response.ok) {
    throw new Error('Failed to fetch users')
  }

  return response.json()
}

export const Route = createFileRoute('/')({
  component: HomePage,
})

function HomePage() {
  const {
    data: users,
    error,
    isFetching,
    refetch,
  } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    enabled: false, // Only fetch when the button is clicked.
  })

  return (
    <main>
      <h1>MAKE WORK FLOW Technical Task</h1>

      <button
        type="button"
        onClick={() => refetch()}
        disabled={isFetching}
      >
        {isFetching ? 'Loading...' : 'Load Users'}
      </button>

      {error && <p>Failed to load users.</p>}

      {users && (
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              <strong>{user.name}</strong>
              <br />
              {user.email}
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}