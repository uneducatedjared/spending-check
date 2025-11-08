import { useState } from 'react';
import client from '../../../api/client';
import styles from './page.module.css';
import { Link } from '@modern-js/runtime/router';

export default function CreateTicket() {
  const [name, setName] = useState('');
  const [when, setWhen] = useState('');
  const [amount, setAmount] = useState('');
  const [link, setLink] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const payload = { name, when: new Date(when).toISOString(), amount: Number(amount), link };
      const data = await client.tickets.create(payload);
      window.location.href = '/tickets';
    } catch (err: any) {
      setError(err?.message || String(err));
    }
  }

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.heading}>Create Ticket</h2>

        <form onSubmit={submit} className={styles.form}>
          <label className={styles.label}>
            Name
            <input className={styles.input} value={name} onChange={(e) => setName(e.target.value)} required />
          </label>

          <div className={styles.grid2}>
            <label className={styles.label}>
              When
              <input className={styles.input} value={when} onChange={(e) => setWhen(e.target.value)} type="datetime-local" required />
            </label>

            <label className={styles.label}>
              Amount
              <input className={styles.input} value={amount} onChange={(e) => setAmount(e.target.value)} type="number" step="0.01" required />
            </label>
          </div>

          <label className={styles.label}>
            Link
            <input className={styles.input} value={link} onChange={(e) => setLink(e.target.value)} />
          </label>

          <div className={styles.actions}>
            <button type="button" className={styles.cancel} onClick={() => (window.location.href = '/tickets')}>Cancel</button>
            <button type="submit" className={styles.submit}>Create</button>
          </div>

          {error && <div className={styles.errorText}>{error}</div>}
        </form>
      </div>
    </div>
  );
}
