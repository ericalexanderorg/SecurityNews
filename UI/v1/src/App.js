import React from 'react'
import { Admin, Resource } from 'react-admin'
import fakeDataProvider from 'ra-data-fakerest'
import { NewsList } from './News'
import './App.css'
import data from './data'

const dataProvider = fakeDataProvider(data)

const App = () => (  
  <Admin title="Security News" dataProvider={dataProvider}>
      <Resource name="All News" list={NewsList} />
      <Resource name="Breach News" list={NewsList} />
      <Resource name="Tool News" list={NewsList} />
      <Resource name="Vuln News" list={NewsList} />
  </Admin>
);

export default App;
