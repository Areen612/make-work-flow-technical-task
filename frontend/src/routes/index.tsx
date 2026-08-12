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
    <main className="page-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Technical Task</p>
          <h1>MAKE WORK FLOW</h1>
          <p className="page-description">
            Load and review the users currently in the system.
          </p>
        </div>

        <button
          type="button"
          onClick={() => refetch()}
          disabled={isFetching}
        >
          {isFetching ? 'Loading...' : users ? 'Refresh users' : 'Load users'}
        </button>
      </header>

      {error && (
        <p className="message message-error" role="alert">
          Failed to load users. Please try again.
        </p>
      )}

      {users && (
        <section className="users-panel" aria-labelledby="users-heading">
          <div className="panel-heading">
            <h2 id="users-heading">Users</h2>
            <span className="user-count">
              {users.length} {users.length === 1 ? 'user' : 'users'}
            </span>
          </div>

          {users.length > 0 ? (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td>{user.name}</td>
                      <td>
                        <a href={`mailto:${user.email}`}>{user.email}</a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="empty-state">No users found.</p>
          )}
        </section>
      )}
    </main>
  )
}
