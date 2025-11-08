import { useEffect, useState } from 'react';
import client from '../../api/client';
import { getDecodedToken } from '../../services/auth';
import { Link } from '@modern-js/runtime/router';
import styles from './page.module.css';


// Ticket 类型定义
type Ticket = {
  id: number;
  name: string;
  when: string;
  amount: number;
  link?: string;
  user_id: number;
  status: 'pending' | 'approved' | 'denied';
};

export default function TicketsPage() {
  // 1. 使用 useState 管理 tickets 数组，初始值为空数组
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // 2. 使用 useEffect 在组件挂载时获取数据
  useEffect(() => {
    // 定义一个异步函数来获取数据
    const fetchTickets = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await client.tickets.list();
        console.log("API Response Data:", response); // 打印获取到的数据
        
        // 直接使用获取到的数据来更新 state
        setTickets(response || []);
      } catch (err: any) {
        setError(err?.message || 'Failed to load tickets.');
      } finally {
        setIsLoading(false);
      }
    };

    // 设置用户角色
    const decodedToken = getDecodedToken();
    if (decodedToken) {
      setUserRole(decodedToken.role || null);
    }
    
    // 调用函数以执行数据获取
    fetchTickets();
  }, []); // 空依赖数组意味着这个 effect 只在组件第一次挂载时运行一次

  // 更新 ticket 状态的函数
  const changeStatus = async (id: number, status: string) => {
    try {
      await client.tickets.updateStatus(id, status);
      // 成功更新后，重新获取列表
      const response = await client.tickets.list();
      setTickets(response || []);
    } catch (err: any) {
      setError(err?.message || String(err));
    }
  };
  
  // 3. 渲染逻辑
  if (isLoading) {
    return <div className="page-container">Loading tickets...</div>;
  }

  if (error) {
    return <div className="page-container error">{error}</div>;
  }

  return (
    <div className="page-container">
      <div className={styles.header}>
        <h2>Tickets</h2>
        {userRole === 'employee'&& (
          <Link to="/tickets/create">
            <button>Create Ticket</button>
          </Link>
        )}
      </div>

      <table className={styles.styledTable}>
        <thead>
          <tr>
            <th>Name</th>
            <th>When</th>
            <th>Amount</th>
            <th>Link</th>
            <th>Status</th>
            {userRole === 'employer' && <th>Actions</th>}
          </tr>
        </thead>
        <tbody>
          {tickets.length === 0 ? (
            <tr>
              <td colSpan={userRole === 'employer' ? 6 : 5} className={styles.emptyCell}>
                No tickets found.
              </td>
            </tr>
          ) : (
            tickets.map(t => (
              <tr key={t.id}>
                <td>{t.name}</td>
                <td>{new Date(t.when).toLocaleString()}</td>
                <td>${t.amount.toFixed(2)}</td>
                <td>{t.link ? <a href={t.link} target="_blank" rel="noopener noreferrer">link</a> : '-'}</td>
                <td><span className={`status status-${t.status}`}>{t.status}</span></td>
                {userRole === 'employer' && (
                  <td>
                    {t.status === 'pending' && (
                      <>
                        <button className="approve" onClick={() => changeStatus(t.id, 'approved')}>Approve</button>
                        <button className="deny" onClick={() => changeStatus(t.id, 'denied')}>Deny</button>
                      </>
                    )}
                  </td>
                )}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}