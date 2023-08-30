import { Container, Input, Title, Main, Form, Button } from '../../components'
import styles from './styles.module.css'
import { useFormWithValidation } from '../../utils'
import { AuthContext } from '../../contexts'
import { Redirect } from 'react-router-dom'
import { useContext } from 'react'
import MetaTags from 'react-meta-tags'

const SignIn = ({ onSignIn }) => {
  const { values, handleChange, errors, isValid, resetForm } = useFormWithValidation()
  const authContext = useContext(AuthContext)

  return <Main>
    {authContext && <Redirect to='/materials' />}
    <Container>
      <MetaTags>
        <title>Sign In</title>
        <meta name="description" content="Main - Sign In" />
        <meta property="og:title" content="Sign In" />
      </MetaTags>
      <Title title='Sign In' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          onSignIn(values)
        }}
      >
        <Input
          required
          label='Email'
          name='email'
          onChange={handleChange}
        />
        <Input
          required
          label='Password'
          type='password'
          name='password'
          onChange={handleChange}
        />
        <Button
          modifier='style_dark-blue'
          disabled={!isValid}
          type='submit'
          className={styles.button}
        >
          Sign In
        </Button>
      </Form>
    </Container>
  </Main>
}

export default SignIn