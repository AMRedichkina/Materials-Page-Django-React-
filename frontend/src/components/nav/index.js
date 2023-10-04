import styles from './style.module.css'
import cn from 'classnames'
import { LinkComponent } from '../index'
import navigation from '../../configs/navigation'

const Nav = ({ loggedIn }) => {
  return (
    <nav className={styles.nav}>
      <div className={styles.nav__container}>
        <ul className={styles.nav__items}>
          {navigation.map(item => {
            if (!loggedIn && item.auth) { return null }
            return (
              <li 
                className={cn(styles.nav__item, {
                  [styles.nav__item_active]: false
                })} 
                key={item.href}
              >
                <LinkComponent
                  title={item.title}
                  activeClassName={styles.nav__link_active}
                  href={item.href}
                  exact
                  className={styles.nav__link}
                />
              </li>
            )
          })}
        </ul>
      </div>
    </nav>
  )
}

export default Nav
