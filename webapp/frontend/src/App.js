import './App.css';
import { Switch, Route, useHistory, Redirect } from 'react-router-dom';
import React, { useState } from 'react';
import api from './api';
import styles from './styles.module.css';
import { Header, Footer, ProtectedRoute } from './components';

import {
    SignIn,
    SignUp,
    ChangePassword,
    MaterialsPage
} from './pages';

import { AuthContext, UserContext } from './contexts';

function App() {
    const [ loggedIn, setLoggedIn ] = useState(null);
    const [ user, setUser ] = useState({});

    const registration = ({
      email,
      password,
      username,
      first_name,
      last_name
    }) => {
      api.signup({ email, password, username, first_name, last_name })
        .then(res => {
          history.push('/signin')
        })
        .catch(err => {
          const errors = Object.values(err)
          if (errors) {
            alert(errors.join(', '))
          }
          setLoggedIn(false)
        })
    }
  
    const changePassword = ({
      new_password,
      current_password
    }) => {
      api.changePassword({ new_password, current_password })
        .then(res => {
          history.push('/signin')
        })
        .catch(err => {
          const errors = Object.values(err)
          if (errors) {
            alert(errors.join(', '))
          }
        })
    }
  
    const authorization = ({
      email, password
    }) => {
      api.signin({
        email, password
      }).then(res => {
        if (res.auth_token) {
          localStorage.setItem('token', res.auth_token)
          api.getUserData()
            .then(res => {
              setUser(res)
              setLoggedIn(true)
            })
            .catch(err => {
              setLoggedIn(false)
              history.push('/signin')
            })
        } else {
          setLoggedIn(false)
        }
      })
      .catch(err => {
        const errors = Object.values(err)
        if (errors) {
          alert(errors.join(', '))
        }
        setLoggedIn(false)
      })
    }

  const history = useHistory()
  const onSignOut = () => {
    api
      .signout()
      .then(res => {
        localStorage.removeItem('token')
        setLoggedIn(false)
      })
      .catch(err => {
        const errors = Object.values(err)
        if (errors) {
          alert(errors.join(', '))
        }
      })
  }

    return (
        <AuthContext.Provider value={loggedIn}>
            <UserContext.Provider value={user}>
                <div className={styles.App}>
                    <Header loggedIn={loggedIn} onSignOut={onSignOut} />
                    <Switch>
                        <ProtectedRoute
                            exact
                            path='/materials'
                            component={MaterialsPage}
                            loggedIn={loggedIn}
                        />

                        <Route exact path='/signin'>
                            <SignIn onSignIn={authorization} />
                        </Route>

                        <Route exact path='/signup'>
                            <SignUp onSignUp={registration} />
                        </Route>

                        <ProtectedRoute
                            exact
                            path='/change-password'
                            component={ChangePassword}
                            loggedIn={loggedIn}
                            onPasswordChange={changePassword}
                        />

                        <Route path='/'>
                            {loggedIn ? <Redirect to='/materials' /> : <Redirect to='/signin'/>}
                        </Route>
                    </Switch>
                    <Footer />
                </div>
            </UserContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;
