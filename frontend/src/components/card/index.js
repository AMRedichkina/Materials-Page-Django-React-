import styles from './style.module.css';
import { useContext } from 'react';
import { AuthContext } from '../../contexts';

const Card = ({
  name = 'Unknown',
  id,
  image,
  description,
  amount,
  availability,
}) => {
  const authContext = useContext(AuthContext);
  
  return (
    <div className={styles.card}>
      <div className={styles.card__image} style={{ backgroundImage: `url(${ image })` }} />
      
      <div className={styles.card__body}>
        <h2>{name}</h2>
        <p>{description}</p>
        <div>Amount: {amount}</div>
        <div>Available: {availability ? 'Yes' : 'No'}</div>
      </div>
    </div>
  );
};

export default Card;
