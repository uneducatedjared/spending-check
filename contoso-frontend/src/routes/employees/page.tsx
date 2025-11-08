import { useEffect, useState } from 'react';
import client from '../../api/client';
import styles from './page.module.css';

type Employee = {
  id: number;
  email: string;
  username: string;
  role: string;
  is_suspended: boolean;
};

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      const data = await client.employees.list();
      setEmployees(data || []);
    } catch (err: any) {
      setError(err?.message || String(err));
    }
  }

  useEffect(() => { load(); }, []);

  async function toggleSuspend(e: Employee) {
    try {
      await client.employees.updateStatus(e.id, !e.is_suspended);
      await load();
    } catch (err: any) {
      setError(err?.message || String(err));
    }
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Employees</h2>
      {error && <div className="error">{error}</div>}
      <table className={styles.styledTable}>
        <thead>
          <tr>
            <th>Email</th>
            <th>Username</th>
            <th>Role</th>
            <th>Suspended</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {employees.map(emp => (
            <tr key={emp.id} className={styles.rowDivider}>
              <td>{emp.email}</td>
              <td>{emp.username}</td>
              <td>{emp.role}</td>
              <td>{String(emp.is_suspended)}</td>
              <td className={styles.actionsCell}>
                <button onClick={() => toggleSuspend(emp)}>{emp.is_suspended ? 'Reactivate' : 'Suspend'}</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
