import { Card, Title, Pagination, CardList, Container, Main } from '../../components'
import styles from './styles.module.css'
import { useEffect, useState } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const MaterialsPage = ({ updateOrders }) => {
  const [materials, setMaterials] = useState([]);
  const [materialsCount, setMaterialsCount] = useState(0);
  const [materialsPage, setMaterialsPage] = useState(1);

  const getMaterials = () => {
    api
      .getMaterials({ page: materialsPage, limit: 6 })
      .then(res => {
        const { results, count } = res;
        setMaterials(results);
        setMaterialsCount(count);
      })
  }

  useEffect(() => {
    getMaterials();
  }, [materialsPage]);

  useEffect(() => {
    getMaterials({ page: materialsPage })
  }, [materialsPage]);

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Materials</title>
          <meta name="description" content="Main - Materials" />
          <meta property="og:title" content="Materials" />
        </MetaTags>
        <div className={styles.title}>
          <Title title='Materials' />
        </div>
        <CardList>
          {materials.map(card => 
            <Card
              {...card}
              key={card.id}
              updateOrders={updateOrders}
            />
          )}
        </CardList>
        <Pagination
          count={materialsCount}
          limit={6}
          page={materialsPage}
          onPageChange={page => setMaterialsPage(page)}
        />
      </Container>
    </Main>
  )
}

export default MaterialsPage;
