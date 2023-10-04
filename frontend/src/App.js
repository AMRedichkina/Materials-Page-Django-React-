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
    // State variables for authentication and user data
    const [ loggedIn, setLoggedIn ] = useState(null);
    const [ user, setUser ] = useState({});

    // Registration function
    const registration = ({
      email,
      password,
      username,
      first_name,
      last_name
    }) => {
      // Sign up using API call
      api.signup({ email, password, username, first_name, last_name })
        .then(res => {
          history.push('/signin')
        })
        // Display error messages in case of registration failure
        .catch(err => {
          const errors = Object.values(err)
          if (errors) {
            alert(errors.join(', '))
          }
          setLoggedIn(false)
        })
    }
  
    // Change password function
    const changePassword = ({
      new_password,
      current_password
    }) => {
      // Call API to change user's password
      api.changePassword({ new_password, current_password })
        .then(res => {
          history.push('/signin')
        })
        .catch(err => {
          // Display error messages in case of password change failure
          const errors = Object.values(err)
          if (errors) {
            alert(errors.join(', '))
          }
        })
    }
  
    // Authorization function
    const authorization = ({
      email, password
    }) => {
      // Sign in using API call
      api.signin({
        email, password
      }).then(res => {
        if (res.auth_token) {
          localStorage.setItem('token', res.auth_token) // Store auth token in local storage
          api.getUserData()
            .then(res => {
              setUser(res)
              setLoggedIn(true) // Set user as logged in and provide user data
            })
            .catch(err => {
              setLoggedIn(false)
              history.push('/signin') // Redirect to sign in in case of data retrieval error
            })
        } else {
          setLoggedIn(false)
        }
      })
      .catch(err => {
        // Display error messages in case of sign in failure
        const errors = Object.values(err)
        if (errors) {
          alert(errors.join(', '))
        }
        setLoggedIn(false)
      })
    }

  // Use React Router's useHistory hook for navigation
  const history = useHistory()

  // Function to handle user sign out
  const onSignOut = () => {
    api
      .signout()
      .then(res => {
        localStorage.removeItem('token') // Remove auth token from local storage
        setLoggedIn(false)
      })
      .catch(err => {
        // Display error messages in case of sign out failure
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
