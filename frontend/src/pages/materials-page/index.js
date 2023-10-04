import React, { useEffect, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup, Checkbox, Input } from '../../components';
import api from '../../api';
import MetaTags from 'react-meta-tags';

// Define the MaterialsPage component
const MaterialsPage = ({ updateOrders }) => {
  const [materials, setMaterials] = useState([]);
  const [materialsCount, setMaterialsCount] = useState(0);
  const [materialsPage, setMaterialsPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [isAvailable, setIsAvailable] = useState(true);

  // Set up WebSocket connection for real-time updates
  useEffect(() => {
    const rws = new ReconnectingWebSocket('ws://localhost/ws/material_status/');
  
    // Event listener for WebSocket connection open
    rws.addEventListener('open', () => {
      console.log('WebSocket connection opened');
    });
  
    // Event listener for WebSocket messages
    rws.addEventListener('message', (e) => {
      const data = JSON.parse(e.data);
      console.log('Received WebSocket message:', data);
  
      if (data.type === 'update_material_status') {
        // Update materials state based on message type
        setMaterials(prevMaterials => {
            console.log('Current materials inside state update:', prevMaterials);
            console.log('Update received:', data);
            
            const updatedMaterials = prevMaterials.map(material => {
                if (material.id === data.text.id) {
                    return { ...material, ...data.text };
                }
                return material;
            });
            
            console.log('Materials after update:', updatedMaterials);
            
            return updatedMaterials;
        });
      } else if (data.type === 'new_material') {
          // Add a new material to the list
          setMaterials(prevMaterials => {
              const newMaterials = [...prevMaterials, data.text];
              console.log('Materials after adding new one:', newMaterials);
              return newMaterials;
          });
      }
    });

    // Close the WebSocket connection when component unmounts
    return () => {
      rws.close();
    };
  }, []);

  // Fetch materials based on filters and page number
  useEffect(() => {
    getMaterials();
  }, [materialsPage, searchTerm, selectedTypes, isAvailable]);

   // Function to fetch materials using API
  const getMaterials = () => {
    console.log("Fetching materials with filters:", {
      page: materialsPage,
      limit: 6,
      search: searchTerm,
      type: selectedTypes.join(','),
      availability: isAvailable
    });

    api
      .getMaterials({
        page: materialsPage,
        limit: 6,
        search: searchTerm,
        type: selectedTypes.join(','),
        availability: isAvailable
      })
      .then(res => {
        const { results, count } = res;
        setMaterials(results);
        setMaterialsCount(count);
      })
      .catch(error => {
        console.error("Error fetching materials:", error);
      })
  };

  // Handle changes to selected material types
  const handleTypeChange = (id) => {
    if (selectedTypes.includes(id)) {
        setSelectedTypes(selectedTypes.filter((type) => type !== id));
    } else {
        setSelectedTypes([...selectedTypes, id]);
    }
  };

  // Handle changes to material availability filter
  const handleAvailabilityChange = (id) => {
    if (id === 'available') {
        setIsAvailable(prevIsAvailable => prevIsAvailable === true ? null : true);
    } else if (id === 'not_available') {
        setIsAvailable(prevIsAvailable => prevIsAvailable === false ? null : false);
    }
  };

  console.log("Rendering with materials state:", materials);
  
  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Materials</title>
          <meta name="description" content="Main - Materials" />
          <meta property="og:title" content="Materials" />
        </MetaTags>

        <div className="filters">
          <Input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search materials..."
            label="Search"
          />
          <CheckboxGroup
            label="Material Types"
            values={[
              { id: 'doors', name: 'Doors', value: selectedTypes.includes('doors') },
              { id: 'windows', name: 'Windows', value: selectedTypes.includes('windows') },
              { id: 'bricks', name: 'Bricks', value: selectedTypes.includes('bricks') },
              { id: 'blocks', name: 'Blocks', value: selectedTypes.includes('blocks') },
              { id: 'other', name: 'Other', value: selectedTypes.includes('other') },
            ]}
            handleChange={handleTypeChange}
          />
          <CheckboxGroup
            label="Availability"
            values={[
              { id: 'available', name: 'Available', value: isAvailable === true },
              { id: 'not_available', name: 'Not Available', value: isAvailable === false },
            ]}
            handleChange={handleAvailabilityChange}
          />
        </div>

        <div className="materials-list">
          <div className="title">
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
        </div>

        <Pagination
          count={materialsCount}
          limit={6}
          page={materialsPage}
          onPageChange={page => setMaterialsPage(page)}
        />
      </Container>
    </Main>
  );
}

export default MaterialsPage;
